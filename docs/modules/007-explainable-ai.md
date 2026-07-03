# Module 007: Explainable AI

## Purpose

Explain why ScamShieldAI detected a message as scam or suspicious.

The module generates human-readable explanations and exposes technical explainability metadata for:

- SHAP
- LIME
- Attention visualization

## Architecture

```text
Prediction API
  -> ScamPredictionService
  -> ExplainabilityService
  -> persuasion signals
  -> sensitive-info / URL / keyword signals
  -> SHAP / LIME / attention adapters
  -> human-readable explanation
```

Files:

```text
apps/api/app/application/explainability_dto.py
apps/api/app/application/services/explainability_service.py
apps/api/app/application/nlp_dto.py
apps/api/app/application/services/nlp_prediction_service.py
```

## Human-Readable Explanation

Example output:

```text
The message is suspicious because:
1. It creates urgency.
2. It requests sensitive information.
3. It appears to impersonate a trusted organization or role.
```

Reasons are derived from:

- persuasion strategies
- sensitive information requests
- suspicious keywords
- URLs
- risk score
- model prediction label

## SHAP

When `shap` is installed and a probability-capable model artifact is loaded, the service attempts token attribution for scam probability.

If SHAP is unavailable or incompatible with the current artifact, the response marks SHAP as unavailable and explains why.

## LIME

When `lime` is installed and a probability-capable model artifact is loaded, the service generates a local text explanation for the scam class.

If LIME is unavailable or the model cannot provide probabilities, the response marks LIME as unavailable.

## Attention Visualization

Attention visualization requires a transformer model plus tokenizer and attention tensors. The current service exposes the response slot and reports availability. Full attention heatmaps should be enabled when transformer inference is promoted into the production prediction path.

## Prediction API Integration

`POST /api/v1/ml/predict` now returns:

```json
{
  "label": "scam",
  "is_scam": true,
  "risk_score": 92,
  "explanation": "The message is suspicious because:\n1. It creates urgency.",
  "explainability": {
    "human_readable": "The message is suspicious because:\n1. It creates urgency.",
    "reasons": ["It creates urgency."],
    "shap": {
      "method": "SHAP",
      "available": false,
      "summary": "SHAP requires a loaded probability-capable model artifact.",
      "tokens": []
    },
    "lime": {
      "method": "LIME",
      "available": false,
      "summary": "LIME requires a loaded probability-capable model artifact.",
      "tokens": []
    },
    "attention": {
      "method": "Attention",
      "available": false,
      "summary": "Attention visualization requires a loaded transformer model artifact.",
      "tokens": []
    }
  }
}
```

## Dependencies

Optional explainability dependencies are in:

```text
apps/api/requirements-ml.txt
```

They include:

- `shap`
- `lime`

## Security Notes

- Explanations should help users understand risk without teaching evasion.
- Do not expose raw model internals that reveal detection thresholds or proprietary rules.
- Do not render suspicious URLs as clickable links.
- Keep user-facing explanations concise and action-oriented.