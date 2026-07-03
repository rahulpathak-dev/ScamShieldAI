# Module 004: NLP Scam Detection Engine

## Goal

Classify submitted text as `scam` or `safe` using a full NLP pipeline and expose predictions through the FastAPI backend.

## Pipeline

```text
Data collection
  -> cleaning
  -> tokenization
  -> feature extraction
  -> model training
  -> evaluation
  -> artifact saving
  -> prediction API
```

## Dataset Plan

Use local, legally permitted copies of:

- SMS spam datasets
- phishing datasets
- financial fraud datasets

Raw files go in:

```text
ml/data/raw
```

The normalized training dataset is:

```text
ml/data/processed/scam_messages.csv
```

Required columns:

```text
text,label,source
```

Labels:

- `scam`
- `safe`

## Data Collection and Normalization

Build a normalized dataset from raw CSVs:

```powershell
cd apps/api
python -m app.ml.datasets `
  --input ../../ml/data/raw/sms_spam.csv:v2:v1:sms_spam `
  --input ../../ml/data/raw/phishing.csv:text:label:phishing `
  --input ../../ml/data/raw/financial_fraud.csv:message:label:financial_fraud
```

Each `--input` value follows:

```text
path:text_column:label_column:source
```

## Cleaning

Implemented in:

```text
apps/api/app/ml/preprocessing.py
```

The cleaner:

- normalizes Unicode
- lowercases text
- replaces URLs with `url_token`
- replaces emails with `email_token`
- replaces phone numbers with `phone_token`
- replaces money values with `money_token`
- collapses whitespace

## Tokenization

The baseline tokenizer uses cleaned whitespace tokens. Classical models use `TfidfVectorizer` with unigram and bigram features.

## Feature Extraction

Classical feature extraction:

- TF-IDF
- ngrams: 1 to 2
- sublinear term frequency
- max 100,000 features

## Baseline Models

Implemented in:

```text
apps/api/app/ml/train_classical.py
```

Models:

- TF-IDF + Logistic Regression
- TF-IDF + Random Forest
- TF-IDF + SVM

Training command:

```powershell
cd apps/api
pip install -r requirements-ml.txt
python -m app.ml.train_classical
```

The trainer evaluates every model and saves the best model by F1 score.

Artifacts:

```text
ml/models/classical/best_model.joblib
ml/models/classical/model_card.json
ml/reports/classical_metrics.json
```

## Advanced Models

Implemented in:

```text
apps/api/app/ml/train_transformer.py
```

Supported checkpoints:

- `bert-base-uncased`
- `roberta-base`

Training examples:

```powershell
cd apps/api
pip install -r requirements-ml.txt
python -m app.ml.train_transformer --checkpoint bert-base-uncased
python -m app.ml.train_transformer --checkpoint roberta-base
```

Artifacts are saved under:

```text
ml/models/transformers
```

## Evaluation

Metrics reported:

- Accuracy
- Precision
- Recall
- F1 score

Classical results are written to:

```text
ml/reports/classical_metrics.json
```

Transformer results are written to:

```text
ml/reports/*_metrics.json
```

## Prediction API

### `POST /api/v1/ml/predict`

Request:

```json
{
  "text": "Urgent bank alert. Verify OTP now or account will be suspended."
}
```

Response:

```json
{
  "label": "scam",
  "is_scam": true,
  "scam_probability": 0.87,
  "confidence": 0.87,
  "risk_score": 87.0,
  "model": {
    "model_name": "tfidf_logistic_regression",
    "model_type": "tfidf_classical_binary_classifier",
    "artifact_loaded": true
  },
  "explanation": "The trained NLP classifier found scam-like language with a risk score of 87."
}
```

### `GET /api/v1/ml/model`

Returns active model metadata and metrics when a model card exists.

## Runtime Behavior

If `ml/models/classical/best_model.joblib` exists, the API loads it and serves trained model predictions. If no model artifact exists, the API falls back to the existing explainable rule baseline so the endpoint remains usable during development.

## Security and Quality Notes

- Do not train on datasets without proper license rights.
- Deduplicate messages before splitting.
- Keep raw datasets out of source control if licensing or privacy is unclear.
- Track model card metadata for every deployed artifact.
- Use recall and F1 heavily; missing real scams is more damaging than occasional safe-message review.
- Evaluate per source dataset so SMS-heavy performance does not hide phishing-email weakness.