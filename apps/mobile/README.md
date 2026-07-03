# ScamShieldAI Mobile

Expo-style React Native scaffold for mobile scam detection.

## Included flows

- SMS text scanning through `/api/v1/mobile/scan-sms`
- Screenshot OCR text analysis through `/api/v1/mobile/scan-screenshot`

Native production work still needed:

- Android SMS permission and secure message picker
- iOS share extension for copied messages and screenshots
- On-device OCR or cloud OCR integration
- Secure token storage and enterprise MDM configuration