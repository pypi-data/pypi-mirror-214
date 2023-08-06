import json
import logging
import random
from typing import Any

import numpy as np
import torch
from peft import (
    LoraConfig,
    PeftModelForTokenClassification,
    TaskType,
    get_peft_model,
)
from transformers import AutoModelForTokenClassification

from partial_tagger.data import CharBasedTags, Dataset
from partial_tagger.data.batch.text import TaggerInputs
from partial_tagger.encoders import BaseEncoder
from partial_tagger.recognizer import Recognizer
from partial_tagger.training import Trainer
from partial_tagger.utils import Metric, create_tag


class PeftEncoder(BaseEncoder):
    def __init__(self, model: PeftModelForTokenClassification):
        super(PeftEncoder, self).__init__()

        self.model = model

    def forward(self, inputs: TaggerInputs) -> torch.Tensor:
        return self.model(**inputs).logits

    def get_hidden_size(self) -> int:
        return self.model.num_labels


def create_encoder(
    encoder_type: str, model_name: str, hidden_size: int, dropout: float
) -> PeftEncoder:
    peft_config = LoraConfig(
        task_type=TaskType.TOKEN_CLS,
        inference_mode=False,
        target_modules=["query", "value"],
        r=8,
        lora_alpha=16,
        lora_dropout=0.0,
        bias="all",
    )

    model = AutoModelForTokenClassification.from_pretrained(
        model_name, num_labels=hidden_size, hidden_dropout_prob=dropout
    )
    model = get_peft_model(model, peft_config)
    return PeftEncoder(model)


def fix_state(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


class JSONAdapter(logging.LoggerAdapter):
    def process(self, msg: Any, kwargs: Any) -> Any:
        return json.dumps(msg), kwargs


def get_logger(log_name: str, log_file: str) -> JSONAdapter:
    logging.shutdown()
    logger = logging.getLogger(log_name)

    logger.setLevel(logging.INFO)

    logger.addHandler(logging.StreamHandler())
    logger.addHandler(logging.FileHandler(log_file, mode="w", encoding="utf-8"))

    return JSONAdapter(logger, {})


def load_dataset(path: str) -> Dataset:
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
    device: torch.device,
    num_epochs: int,
    batch_size: int,
    learning_rate: float,
    gradient_clip_value: float,
    padding_index: int,
    unknown_index: int,
    log_file: str,
) -> Recognizer:
    from partial_tagger import utils

    utils.create_encoder = create_encoder

    logger = get_logger(f"{__name__}.train", log_file)

    train_dataset = load_dataset(train_path)
    validation_dataset = load_dataset(validation_path)

    trainer = Trainer(
        model_name,
        batch_size,
        num_epochs,
        learning_rate,
        gradient_clip_value,
        padding_index,
        unknown_index,
        encoder_type="default",
    )

    return trainer(train_dataset, validation_dataset, device, logger)  # type:ignore


def evaluate(
    test_path: str,
    recognizer: Recognizer,
    device: torch.device,
    batch_size: int,
    log_file: str,
) -> None:
    logger = get_logger(f"{__name__}.evaluate", log_file)

    test_dataset = load_dataset(test_path)

    texts, ground_truths = zip(*test_dataset)

    predictions = recognizer(texts, batch_size, device)

    metric = Metric()
    metric(predictions, ground_truths)

    logger.info({f"test_{key}": value for key, value in metric.get_scores().items()})


def main() -> None:
    seed = 0
    fix_state(seed)

    train_log_file = "log_lora_large.jsonl"
    test_scores_file = "scores_lora_large.json"

    train_path = "entity.train_r0.5_p0.9.jsonl"
    validation_path = "entity.dev.jsonl"
    test_path = "entity.test.jsonl"

    model_name = "roberta-large"
    batch_size = 15
    learning_rate = 4e-5
    num_epochs = 20
    gradient_clip_value = 5.0
    padding_index = -1
    unknown_index = -100

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    recognizer = train(
        train_path,
        validation_path,
        model_name,
        device,
        num_epochs,
        batch_size,
        learning_rate,
        gradient_clip_value,
        padding_index,
        unknown_index,
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
