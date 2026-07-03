# Module 006: Intelligent Scam Risk Scoring

## Goal

Generate a scam risk score from `0` to `100` and classify it into a user-friendly risk level.

Levels:

- `0-30`: Safe
- `31-70`: Suspicious
- `71-100`: Dangerous

## Factors

The scoring engine combines:

- ML prediction
- Persuasion techniques
- Suspicious keywords
- URL analysis
- Threat database matches
- User reports

## Architecture

```text
FastAPI route
  -> RiskScoringService
  -> ScamPredictionService
  -> PersuasionDetectionService
  -> keyword / URL / threat / report factors
  -> score + level + reasons
```

Files:

```text
apps/api/app/application/risk_dto.py
apps/api/app/application/services/risk_scoring_service.py
apps/api/app/interfaces/api/v1/risk.py
```

## API

### `POST /api/v1/risk/score`

Request:

```json
{
  "message": "Urgent bank alert. Verify OTP now or your account will be suspended.",
  "threat_matches": ["bit.ly/secure-bank"],
  "user_report_count": 3
}
```

Response:

```json
{
  "Risk Score": 92,
  "Level": "Dangerous",
  "Reasons": [
    "Urgency detected",
    "Fake authority detected"
  ],
  "factors": []
}
```

The `factors` array provides traceability for the score.

## Scoring Weights

Current weights:

- ML prediction: `35%`
- Persuasion techniques: `20%`
- Suspicious keywords: `15%`
- URL analysis: `12%`
- Threat database: `12%`
- User reports: `6%`

The final score is the weighted sum, clamped to `0-100`.

## Reason Generation

Reasons are ranked by factor contribution and deduplicated. Examples:

- `ML model predicted scam with 87% probability`
- `Urgency detected`
- `Fake authority detected`
- `Shortened URL detected`
- `Threat database match: bit.ly/secure-bank`
- `Reported by 3 user(s)`

## Threat Database and Reports

This first backend service accepts `threat_matches` and `user_report_count` as request inputs. When the threat intelligence and scan history modules are expanded, these values should be loaded from PostgreSQL tables:

- `threat_database`
- `scan_threat_matches`
- `scam_reports`

## Security Notes

- Treat messages and URLs as untrusted input.
- Do not fetch URLs during scoring in the request path.
- Do not render suspicious URLs as clickable links.
- Keep score factors explainable for analysts and users.
- Use the score as decision support; do not make irreversible user-impacting decisions from a single model signal.