# Module 002: Secure Authentication

## Architecture

Authentication is implemented as a dedicated module across the FastAPI backend, PostgreSQL database, and Next.js frontend.

Backend flow:

```text
FastAPI auth route
  -> AuthService
  -> UserRepository / AuditLogRepository
  -> PostgreSQL users + audit_logs
```

Security services:

- `PasswordService`: Argon2id password hashing through `pwdlib`.
- `TokenService`: signed JWT access tokens with issuer, expiry, subject, email, role, and token type claims.
- `get_current_user`: validates bearer tokens or the HttpOnly auth cookie.
- `require_roles`: enforces role-based access for `USER`, `ADMIN`, and `ANALYST` workflows.

Frontend flow:

```text
/login or /register
  -> auth API client
  -> FastAPI sets HttpOnly cookie
  -> /dashboard protected by middleware + API session check
```

## Folder Structure

```text
apps/api/app/application/auth_dto.py
apps/api/app/application/services/auth_service.py
apps/api/app/domain/auth.py
apps/api/app/infrastructure/database/models/user.py
apps/api/app/infrastructure/database/models/audit_log.py
apps/api/app/infrastructure/persistence/user_repository.py
apps/api/app/infrastructure/persistence/audit_log_repository.py
apps/api/app/interfaces/api/auth_dependencies.py
apps/api/app/interfaces/api/v1/auth.py

apps/web/src/app/login/page.tsx
apps/web/src/app/register/page.tsx
apps/web/src/app/dashboard/page.tsx
apps/web/src/app/admin/page.tsx
apps/web/src/app/analyst/page.tsx
apps/web/src/components/auth/
apps/web/src/lib/auth-client.ts
apps/web/src/middleware.ts
```

## Database Changes

This module uses the existing product schema:

- `users`
- `audit_logs`

The `users.password_hash` column stores password hashes only. Public registration always creates a `USER`; `ADMIN` and `ANALYST` should be assigned by a controlled admin workflow or migration.

Example local role update:

```sql
UPDATE users SET role = 'admin' WHERE email = 'admin@example.com';
UPDATE users SET role = 'analyst' WHERE email = 'analyst@example.com';
```

## API

### `POST /api/v1/auth/register`

Creates a `USER`, returns a bearer token payload, and sets an HttpOnly cookie.

### `POST /api/v1/auth/login`

Authenticates email/password, returns a bearer token payload, and sets an HttpOnly cookie.

### `POST /api/v1/auth/logout`

Deletes the auth cookie.

### `GET /api/v1/auth/me`

Returns the authenticated user.

### `GET /api/v1/auth/admin-check`

Requires `ADMIN`.

### `GET /api/v1/auth/analyst-check`

Requires `ADMIN` or `ANALYST`.

## Validation

Registration validates:

- name length and whitespace
- email format
- password length between 12 and 128 characters
- lowercase, uppercase, number, and symbol requirements
- unique email at the database boundary

Login uses a generic invalid credential error so attackers cannot distinguish missing users from wrong passwords.

## Security Best Practices

- Passwords are hashed with Argon2id via `pwdlib`.
- JWTs include `sub`, `email`, `role`, `iat`, `exp`, `iss`, and `type` claims.
- Tokens are accepted as either bearer tokens or HttpOnly cookies.
- Frontend uses `credentials: "include"` and does not store tokens in `localStorage`.
- Cookies are `HttpOnly`, `SameSite=Lax`, and `Secure` in production.
- Production startup rejects the default JWT secret.
- Failed login and registration conflict events are written to `audit_logs`.
- Role assignment is not user-controlled during public registration.

## Testing Steps

Backend:

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

Frontend:

```powershell
cd apps/web
npm install
npm run dev
```

Manual API smoke test:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/api/v1/auth/register `
  -ContentType "application/json" `
  -Body '{"name":"Demo User","email":"demo@example.com","password":"StrongPass!123"}' `
  -SessionVariable session

Invoke-RestMethod -Method Get `
  -Uri http://127.0.0.1:8000/api/v1/auth/me `
  -WebSession $session
```