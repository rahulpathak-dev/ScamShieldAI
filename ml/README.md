# ScamShieldAI NLP Engine

This folder stores datasets, trained models, and evaluation reports for the NLP scam detection engine.

## Layout

```text
ml/data/raw/             Raw SMS spam, phishing, and financial fraud datasets
ml/data/processed/       Normalized CSVs with text,label,source
ml/models/classical/     TF-IDF + classical model artifacts
ml/models/transformers/  BERT/RoBERTa fine-tuned artifacts
ml/reports/              Evaluation metrics and model reports
```

## Dataset Format

Training scripts expect:

```csv
text,label,source
urgent verify otp now,scam,sms_spam
meeting is confirmed,safe,email_safe
```

Allowed labels:

- `scam`
- `safe`

## Recommended Dataset Sources

Use legally permitted local copies of:

- SMS spam datasets
- phishing message or phishing URL/text datasets
- financial fraud and scam message datasets

Normalize each source into `text,label,source` before training.