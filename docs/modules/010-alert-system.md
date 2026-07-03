# Module 010: Alert System

## Purpose

The ScamShieldAI alert system warns users when a scan produces a high-risk scam result. It supports browser notifications immediately and email notifications through configurable SMTP settings.

## Backend Components

- `NotificationService` creates high-risk warning messages and delivery records.
- `POST /api/v1/notifications/high-risk-warning` accepts risk context and requested delivery channels.
- Email delivery is disabled by default and only sends when SMTP settings are configured.

## Frontend Components

- The scam analyzer requests a high-risk warning after dangerous scan results.
- Browser notifications use the Web Notifications API after user permission.
- Email warning delivery is available from the analyzer result panel for high-risk scans.

## Warning Example

```text
Warning: This message has 95% scam probability.
```

## Security Decisions

- Email notifications are opt-in through configuration.
- Message content is limited to a short excerpt to reduce sensitive-data exposure.
- Notification payloads include reasons and safety actions, but do not expose model internals or secrets.
- Browser notifications are permission-based and degrade gracefully when blocked or unsupported.

## Environment Variables

- `SCAMSHIELD_NOTIFICATION_HIGH_RISK_THRESHOLD`
- `SCAMSHIELD_NOTIFICATION_CRITICAL_THRESHOLD`
- `SCAMSHIELD_EMAIL_NOTIFICATIONS_ENABLED`
- `SCAMSHIELD_NOTIFICATION_FROM_EMAIL`
- `SCAMSHIELD_SMTP_HOST`
- `SCAMSHIELD_SMTP_PORT`
- `SCAMSHIELD_SMTP_USERNAME`
- `SCAMSHIELD_SMTP_PASSWORD`
- `SCAMSHIELD_SMTP_USE_TLS`