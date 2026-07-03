# Module 005: Psychological Persuasion Detection

## Goal

Detect psychological persuasion strategies used in scam and social engineering messages.

Input:

```json
{
  "message": "Urgent: your bank account is suspended. Verify OTP now."
}
```

Primary output shape:

```json
{
  "strategy": ["Fear", "Urgency"]
}
```

The API also returns evidence and model metadata for explainability.

## Strategies

The module detects:

- Urgency
- Fear
- Authority manipulation
- Greed
- Scarcity
- Emotional pressure
- Fake trust
- Social engineering
- Impersonation

## Architecture

```text
FastAPI route
  -> PersuasionDetectionService
  -> keyword analysis
  -> optional transformer classification
  -> response with strategy + evidence
```

Files:

```text
apps/api/app/application/persuasion_dto.py
apps/api/app/application/services/persuasion_detection_service.py
apps/api/app/interfaces/api/v1/persuasion.py
```

## Detection Methods

### Keyword Analysis

The baseline detector uses normalized text and curated phrase sets for each persuasion strategy. It returns matched terms, scores, and explanations.

### NLP Preprocessing

The module reuses:

```text
apps/api/app/ml/preprocessing.py
```

This provides Unicode normalization, URL/email/phone/money token replacement, lowercasing, and whitespace normalization.

### Transformer Classification

The service can load an optional transformer classifier from:

```text
ml/models/transformers/persuasion
```

Config:

```text
SCAMSHIELD_PERSUASION_CLASSIFIER_MODEL_PATH=ml/models/transformers/persuasion
```

When the artifact exists and `transformers` is installed, the service uses transformer-based multi-label classification alongside keyword analysis. Without an artifact, the API remains functional with keyword analysis.

## API

### `POST /api/v1/persuasion/detect`

Request:

```json
{
  "message": "This is your bank. Urgent: your account will be suspended unless you verify OTP now."
}
```

Response:

```json
{
  "strategy": ["Urgency", "Fear", "Authority manipulation", "Impersonation"],
  "evidence": [
    {
      "strategy": "Urgency",
      "score": 0.53,
      "matched_terms": ["urgent"],
      "explanation": "The message pressures the recipient to act quickly.",
      "source": "keyword_analysis"
    }
  ],
  "model": {
    "model_name": "keyword_persuasion_baseline",
    "model_type": "keyword_analysis",
    "artifact_loaded": false,
    "artifact_path": ".../ml/models/transformers/persuasion"
  }
}
```

## Training Data Shape For Transformer Upgrade

Use a multi-label dataset:

```csv
text,labels
"Urgent bank alert, verify OTP now","Urgency|Fear|Authority manipulation"
"Guaranteed 300% crypto profit today","Greed|Scarcity"
```

Future training should fine-tune BERT/RoBERTa or another transformer for multi-label classification and save the artifact to `ml/models/transformers/persuasion`.

## Security Notes

- Treat messages as untrusted input.
- Do not render detected URLs as clickable links.
- Keep evidence concise; explanations should help users recognize manipulation without teaching evasion.
- Use the transformer output as assistive signal, not as the only control for high-risk user decisions.