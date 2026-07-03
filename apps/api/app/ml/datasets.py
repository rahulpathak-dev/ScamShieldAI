from __future__ import annotations

import argparse
import csv
from pathlib import Path

from app.ml.config import DEFAULT_DATASET_PATH, RAW_DATA_DIR, SCAM_LABEL, SAFE_LABEL, ensure_ml_directories
from app.ml.preprocessing import clean_text

SCAM_VALUES = {"1", "spam", "phishing", "fraud", "scam", "malicious", "bad", "yes", "true"}
SAFE_VALUES = {"0", "ham", "safe", "legitimate", "benign", "good", "no", "false"}


def normalize_label(value: str) -> str:
    normalized = str(value).strip().casefold()
    if normalized in SCAM_VALUES:
        return SCAM_LABEL
    if normalized in SAFE_VALUES:
        return SAFE_LABEL
    raise ValueError(f"Unsupported label value: {value!r}")


def load_csv_rows(path: Path, text_column: str, label_column: str, source: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            text = clean_text(row.get(text_column, ""))
            if not text:
                continue
            rows.append(
                {
                    "text": text,
                    "label": normalize_label(row.get(label_column, "")),
                    "source": source,
                }
            )
    return rows


def write_dataset(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    seen: set[tuple[str, str]] = set()
    deduped: list[dict[str, str]] = []
    for row in rows:
        key = (row["text"], row["label"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["text", "label", "source"])
        writer.writeheader()
        writer.writerows(deduped)


def build_dataset(inputs: list[tuple[Path, str, str, str]], output_path: Path = DEFAULT_DATASET_PATH) -> Path:
    ensure_ml_directories()
    rows: list[dict[str, str]] = []
    for path, text_column, label_column, source in inputs:
        rows.extend(load_csv_rows(path, text_column, label_column, source))
    write_dataset(rows, output_path)
    return output_path


def parse_input(value: str) -> tuple[Path, str, str, str]:
    parts = value.split(":")
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("Input must be path:text_column:label_column:source")
    return Path(parts[0]), parts[1], parts[2], parts[3]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build normalized ScamShieldAI training dataset.")
    parser.add_argument(
        "--input",
        action="append",
        type=parse_input,
        required=True,
        help="CSV mapping as path:text_column:label_column:source. Example: ml/data/raw/sms.csv:v1:v2:sms_spam",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_DATASET_PATH)
    args = parser.parse_args()

    output = build_dataset(args.input, args.output)
    print(f"Wrote normalized dataset to {output}")


if __name__ == "__main__":
    main()