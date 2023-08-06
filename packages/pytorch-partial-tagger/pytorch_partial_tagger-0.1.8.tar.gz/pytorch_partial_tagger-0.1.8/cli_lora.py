from __future__ import annotations

import json
import logging
import random
import sys
from collections.abc import MutableMapping
from contextlib import contextmanager
from typing import Any, Iterator, cast

import numpy as np
import torch
from peft import (
    LoraConfig,
    PeftModelForTokenClassification,
    TaskType,
    get_peft_model,
)
from transformers import AutoModelForTokenClassification, AutoTokenizer

from partial_tagger.data import CharBasedTags, LabelSet
from partial_tagger.data.batch.text import TransformerTokenizer
from partial_tagger.encoders import BaseEncoder, BaseEncoderFactory
from partial_tagger.metric import Metric
from partial_tagger.recognizer import Recognizer
from partial_tagger.training import Trainer
from partial_tagger.utils import create_tag


class LoraTransformerEncoder(BaseEncoder):
    def __init__(self, model: PeftModelForTokenClassification):
        super(LoraTransformerEncoder, self).__init__()

        self.model = model

    def forward(self, inputs: dict[str, torch.Tensor]) -> torch.Tensor:
        return self.model(**inputs).logits

    def get_hidden_size(self) -> int:
        return self.model.num_labels


class LoraTransformerEncoderFactory(BaseEncoderFactory):
    def __init__(self, model_name: str, dropout: float):
        self.__model_name = model_name
        self.__dropout = dropout

    def create(self, label_set: LabelSet) -> LoraTransformerEncoder:
        peft_config = LoraConfig(
            task_type=TaskType.TOKEN_CLS,
            inference_mode=False,
            target_modules=["query", "value"],
            r=8,
            lora_alpha=8,
            lora_dropout=0.0,
            bias="all",
        )

        model = AutoModelForTokenClassification.from_pretrained(
            self.__model_name,
            num_labels=label_set.get_tag_size(),
            hidden_dropout_prob=self.__dropout,
        )
        model = get_peft_model(model, peft_config)
        return LoraTransformerEncoder(model)


def fix_state(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


class JSONAdapter(logging.LoggerAdapter):
    def process(
        self, msg: Any, kwargs: MutableMapping[str, Any]
    ) -> tuple[Any, MutableMapping[str, Any]]:
        return json.dumps(msg), kwargs


@contextmanager
def get_logger(log_name: str, log_file: str) -> Iterator[logging.Logger]:
    logger = logging.getLogger(log_name)
    logger.propagate = False

    logger.setLevel(logging.INFO)

    handlers: list[logging.Handler] = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file, mode="w", encoding="utf-8"),
    ]

    for handler in handlers:
        logger.addHandler(handler)

    try:
        yield cast(logging.Logger, JSONAdapter(logger, {}))
    finally:
        for handler in handlers:
            handler.close()
            logger.removeHandler(handler)
        logging.shutdown()


def load_dataset(path: str) -> list[tuple[str, CharBasedTags]]:
    with open(path) as f:
        dataset = []

        for line in f:
            data = json.loads(line.rstrip())

            text = " ".join(data["tokens"])

            mapping = {}
            now = 0
            for i, token in enumerate(data["tokens"]):
                mapping[i] = now
                # Add one for a space
                now += len(token) + 1

            tags = tuple(
                create_tag(
                    mapping[annotation["start"]],
                    len(annotation["mention"]),
                    annotation["type"],
                )
                for annotation in data["gold_annotations"]
            )

            dataset.append((text, CharBasedTags(tags, text)))

    return dataset


def train(
    train_path: str,
    validation_path: str,
    model_name: str,
    dropout: float,
    device: torch.device,
    num_epochs: int,
    batch_size: int,
    learning_rate: float,
    gradient_clip_value: float,
    padding_index: int,
    log_file: str,
) -> Recognizer:
    with get_logger(f"{__name__}.train", log_file) as logger:
        train_dataset = load_dataset(train_path)
        validation_dataset = load_dataset(validation_path)

        trainer = Trainer(
            TransformerTokenizer(AutoTokenizer.from_pretrained(model_name)),
            LoraTransformerEncoderFactory(model_name, dropout),
            batch_size,
            num_epochs,
            learning_rate,
            gradient_clip_value,
            padding_index,
        )

        recognizer = trainer(train_dataset, validation_dataset, device, logger)

    return recognizer


def evaluate(
    test_path: str,
    recognizer: Recognizer,
    device: torch.device,
    batch_size: int,
    log_file: str,
) -> None:
    with get_logger(f"{__name__}.evaluate", log_file) as logger:
        test_dataset = load_dataset(test_path)

        texts, ground_truths = zip(*test_dataset)

        predictions = recognizer(texts, batch_size, device)

        metric = Metric()
        metric(predictions, ground_truths)

        logger.info(
            {f"test_{key}": value for key, value in metric.get_scores().items()}
        )


def main() -> None:
    seed = 0
    fix_state(seed)

    train_log_file = "log_lora.jsonl"
    test_scores_file = "scores_lora.json"

    train_path = "entity.train_r0.5_p0.9.jsonl"
    validation_path = "entity.dev.jsonl"
    test_path = "entity.test.jsonl"

    model_name = "distilroberta-base"
    dropout = 0.2
    batch_size = 15
    learning_rate = 2e-5
    num_epochs = 20
    gradient_clip_value = 5.0
    padding_index = -1

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    recognizer = train(
        train_path,
        validation_path,
        model_name,
        dropout,
        device,
        num_epochs,
        batch_size,
        learning_rate,
        gradient_clip_value,
        padding_index,
        train_log_file,
    )

    evaluate(
        test_path,
        recognizer,
        device,
        batch_size,
        test_scores_file,
    )


if __name__ == "__main__":
    main()
