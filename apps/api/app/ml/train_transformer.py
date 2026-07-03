from __future__ import annotations

import argparse
import json
from pathlib import Path

import evaluate
import numpy as np
import pandas as pd
from datasets import Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding, Trainer, TrainingArguments

from app.ml.config import DEFAULT_DATASET_PATH, LABEL_TO_ID, MODEL_DIR, REPORT_DIR, ensure_ml_directories


def compute_metrics(eval_prediction):
    logits, labels = eval_prediction
    predictions = np.argmax(logits, axis=-1)
    accuracy = evaluate.load("accuracy")
    precision = evaluate.load("precision")
    recall = evaluate.load("recall")
    f1 = evaluate.load("f1")
    return {
        "accuracy": accuracy.compute(predictions=predictions, references=labels)["accuracy"],
        "precision": precision.compute(predictions=predictions, references=labels, zero_division=0)["precision"],
        "recall": recall.compute(predictions=predictions, references=labels, zero_division=0)["recall"],
        "f1": f1.compute(predictions=predictions, references=labels, zero_division=0)["f1"],
    }


def train_transformer(dataset_path: Path, model_checkpoint: str, output_dir: Path, epochs: int, batch_size: int) -> dict:
    ensure_ml_directories()
    frame = pd.read_csv(dataset_path).dropna(subset=["text", "label"])
    frame["label"] = frame["label"].map(LABEL_TO_ID).astype(int)
    dataset = Dataset.from_pandas(frame[["text", "label"]])
    dataset = dataset.train_test_split(test_size=0.2, seed=42, stratify_by_column="label")

    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

    def tokenize_batch(batch):
        return tokenizer(batch["text"], truncation=True, max_length=256)

    tokenized = dataset.map(tokenize_batch, batched=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_checkpoint,
        num_labels=2,
        id2label={0: "safe", 1: "scam"},
        label2id={"safe": 0, "scam": 1},
    )

    args = TrainingArguments(
        output_dir=str(output_dir),
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=epochs,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["test"],
        tokenizer=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
        compute_metrics=compute_metrics,
    )
    trainer.train()
    metrics = trainer.evaluate()
    trainer.save_model(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))

    report = {
        "model_checkpoint": model_checkpoint,
        "artifact_path": str(output_dir),
        "metrics": metrics,
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / f"{output_dir.name}_metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune BERT/RoBERTa for ScamShieldAI scam classification.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET_PATH)
    parser.add_argument("--checkpoint", choices=["bert-base-uncased", "roberta-base"], default="bert-base-uncased")
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=16)
    args = parser.parse_args()

    output_dir = args.output_dir or MODEL_DIR / "transformers" / args.checkpoint.replace("/", "_")
    report = train_transformer(args.dataset, args.checkpoint, output_dir, args.epochs, args.batch_size)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()