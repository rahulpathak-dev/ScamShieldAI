# Module 003: User Dashboard

## Architecture

The user dashboard is implemented in the Next.js app as protected client-side workspace pages. Authentication is enforced by middleware and by `ProtectedRoute`, which confirms the session through `GET /api/v1/auth/me`.

Current scan history is stored in browser local storage because the backend scan-history API has not been built yet. The analyzer still calls the FastAPI scam analysis endpoint, then stores a compact local record for dashboard metrics and history views.

## Pages

- `/dashboard`: total scans, scam detections, average risk, critical scans, risk distribution, recent scans.
- `/analyzer`: message/email/chat input with scam probability, risk score, category, explanation, and evidence.
- `/history`: filterable scan history table.
- `/profile`: account role, email, account activity, and security posture.

## Frontend Structure

```text
src/app/dashboard/page.tsx
src/app/analyzer/page.tsx
src/app/history/page.tsx
src/app/profile/page.tsx
src/components/workspace/
src/components/dashboard/
src/hooks/use-scan-history.ts
src/lib/scan-history.ts
```

## Security

- All user workspace routes require the auth cookie before rendering.
- Protected pages also call `/api/v1/auth/me` before showing user data.
- JWTs are not stored in `localStorage`.
- Local scan history is browser-scoped and should be replaced by PostgreSQL-backed history when the scan-history backend module is implemented.