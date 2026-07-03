from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

import joblib
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from app.ml.config import DEFAULT_CLASSICAL_MODEL_PATH, DEFAULT_DATASET_PATH, DEFAULT_MODEL_CARD_PATH, LABEL_TO_ID, REPORT_DIR, ensure_ml_directories


def vectorizer() -> TfidfVectorizer:
    return TfidfVectorizer(
        lowercase=False,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95,
        sublinear_tf=True,
        max_features=100_000,
    )


def build_models(random_state: int) -> dict[str, Pipeline]:
    return {
        "tfidf_logistic_regression": Pipeline(
            [
                ("tfidf", vectorizer()),
                ("classifier", LogisticRegression(max_iter=2000, class_weight="balanced", random_state=random_state)),
            ]
        ),
        "tfidf_random_forest": Pipeline(
            [
                ("tfidf", vectorizer()),
                ("classifier", RandomForestClassifier(n_estimators=300, class_weight="balanced", n_jobs=-1, random_state=random_state)),
            ]
        ),
        "tfidf_svm": Pipeline(
            [
                ("tfidf", vectorizer()),
                ("classifier", CalibratedClassifierCV(LinearSVC(class_weight="balanced", random_state=random_state))),
            ]
        ),
    }


def metrics(y_true, y_pred) -> dict[str, float]:
    return {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
    }


def train(dataset_path: Path, output_path: Path, model_card_path: Path, random_state: int = 42) -> dict:
    ensure_ml_directories()
    dataset = pd.read_csv(dataset_path)
    dataset = dataset.dropna(subset=["text", "label"])
    dataset["target"] = dataset["label"].map(LABEL_TO_ID)
    dataset = dataset.dropna(subset=["target"])

    x_train, x_test, y_train, y_test = train_test_split(
        dataset["text"],
        dataset["target"].astype(int),
        test_size=0.2,
        random_state=random_state,
        stratify=dataset["target"].astype(int),
    )

    results: dict[str, dict[str, float]] = {}
    trained_models: dict[str, Pipeline] = {}
    for name, model in build_models(random_state).items():
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)
        results[name] = metrics(y_test, predictions)
        trained_models[name] = model

    best_name = max(results, key=lambda name: results[name]["f1"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(trained_models[best_name], output_path)

    model_card = {
        "model_name": best_name,
        "model_type": "tfidf_classical_binary_classifier",
        "task": "scam_message_classification",
        "labels": {"0": "safe", "1": "scam"},
        "dataset_path": str(dataset_path),
        "trained_at": datetime.now(UTC).isoformat(),
        "selection_metric": "f1",
        "metrics": results,
        "best_metrics": results[best_name],
        "artifact_path": str(output_path),
    }
    model_card_path.parent.mkdir(parents=True, exist_ok=True)
    model_card_path.write_text(json.dumps(model_card, indent=2), encoding="utf-8")
    (REPORT_DIR / "classical_metrics.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    return model_card


def main() -> None:
    parser = argparse.ArgumentParser(description="Train ScamShieldAI classical NLP models.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_CLASSICAL_MODEL_PATH)
    parser.add_argument("--model-card", type=Path, default=DEFAULT_MODEL_CARD_PATH)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    model_card = train(args.dataset, args.output, args.model_card, args.random_state)
    print(json.dumps(model_card, indent=2))


if __name__ == "__main__":
    main()