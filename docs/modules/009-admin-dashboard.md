# Module 009: Admin Dashboard

## Purpose

The Admin Dashboard gives ScamShieldAI administrators a protected operational console for monitoring users, scam activity, threat intelligence, model health, and system logs.

## Frontend Scope

- Route: `/admin`
- Access: `ADMIN` role only through the existing `ProtectedRoute` guard
- Framework: Next.js App Router with TypeScript
- Styling: Tailwind CSS
- Charts: Recharts

## Dashboard Areas

1. Overview
   - Total users
   - Scam detections
   - Active threats
   - Model F1 score
   - Scam category distribution
   - Attack trend line chart
   - Risk distribution chart

2. User Management
   - Account name and email
   - Role badge
   - Status badge
   - Scan volume
   - Current risk posture

3. Threat Intelligence
   - Indicator type
   - URL, phone, sender, or keyword indicator
   - Severity
   - Confidence
   - Last seen timestamp

4. Model Monitoring
   - Accuracy
   - Precision
   - Recall
   - F1 score
   - Deployment status

5. System Logs
   - Timestamp
   - Severity level
   - Event description
   - Actor
   - Source IP

## Data Integration Plan

The current dashboard uses local operational datasets so the UI can be developed independently from backend admin endpoints. Replace these datasets with API calls when the backend admin module is implemented.

Recommended backend endpoints:

- `GET /api/v1/admin/summary`
- `GET /api/v1/admin/users`
- `GET /api/v1/admin/analytics/scam-categories`
- `GET /api/v1/admin/analytics/attack-trends`
- `GET /api/v1/admin/analytics/risk-distribution`
- `GET /api/v1/admin/threat-intelligence`
- `GET /api/v1/admin/models/metrics`
- `GET /api/v1/admin/audit-logs`

## Security Decisions

- The route is hidden behind role-based authorization on the client.
- Backend endpoints must independently enforce `ADMIN` role authorization before returning admin data.
- System logs should redact tokens, passwords, reset links, and message contents unless explicitly needed for forensics.
- User management actions should require audit logging and should not expose password hashes or authentication secrets.