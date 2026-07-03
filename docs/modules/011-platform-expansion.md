# Module 011: Platform Expansion

## Purpose

This module extends ScamShieldAI beyond the web dashboard into browsing, mobile, voice, multilingual analysis, and enterprise API usage.

## 1. Browser Extension

Location: `apps/browser-extension`

Architecture:

- Manifest V3 extension
- Content script extracts visible page text
- Background service worker calls `POST /api/v1/browser-extension/scan-page`
- High-risk results trigger browser notifications

Security decisions:

- The extension sends visible text only, capped at 50,000 characters.
- Host permissions are explicit for local development and future production API domains.
- The extension should avoid collecting passwords, hidden fields, cookies, and local storage.

## 2. Mobile App

Location: `apps/mobile`

Architecture:

- Expo-style React Native scaffold
- SMS scanning calls `POST /api/v1/mobile/scan-sms`
- Screenshot analysis calls `POST /api/v1/mobile/scan-screenshot`
- Screenshot endpoint accepts OCR text now and can later connect native OCR or cloud OCR

Production additions:

- Secure Android SMS permission flow
- iOS share extension
- Native screenshot picker
- OCR integration
- Secure auth token storage

## 3. Voice Scam Detection

Endpoint: `POST /api/v1/voice/scan-audio`

Pipeline:

1. Audio upload as base64
2. Speech recognition transcript
3. NLP scam analysis
4. Risk prediction response

Current implementation accepts an optional transcript and includes a speech-recognition placeholder. Production integration can use Whisper, AWS Transcribe, Google Speech-to-Text, or Azure Speech.

## 4. Multi-language Support

Endpoints:

- `GET /api/v1/i18n/languages`
- `POST /api/v1/i18n/detect-language`

Supported languages:

- English: `en`
- Hindi: `hi`
- Spanish: `es`
- German: `de`
- French: `fr`
- Chinese: `zh`

Language normalization is centralized in `MultilingualService` so all clients use the same supported language policy.

## 5. Enterprise API

Endpoint: `POST /api/v1/enterprise/batch-analyze`

Architecture:

- API-key protected endpoint using `X-API-Key`
- Tenant-aware batch request shape
- Max batch size controlled by `SCAMSHIELD_ENTERPRISE_MAX_BATCH_SIZE`
- Uses the same analysis pipeline as consumer channels

Environment:

- `SCAMSHIELD_ENTERPRISE_API_KEYS`
- `SCAMSHIELD_ENTERPRISE_MAX_BATCH_SIZE`

Future enterprise work:

- Per-tenant API keys in PostgreSQL
- Rate limiting in Redis
- Usage metering
- Webhook callbacks
- SIEM export formats
- SLA-aware async job queues