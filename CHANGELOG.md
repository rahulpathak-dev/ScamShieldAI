# Changelog

All notable changes to ScamShieldAI will be documented in this file.

## [0.1.0] - 2026-07-02

### Added

- Professional ScamShieldAI landing page.
- Next.js dashboard, analyzer, history, profile, analyst, and admin pages.
- FastAPI backend with health, readiness, authentication, scan analysis, persuasion, risk, notification, assistant, mobile, browser extension, and enterprise routes.
- PostgreSQL migrations for scan history and core product schema.
- Docker Compose setup for local development.
- Security middleware for request IDs, secure headers, CORS, validation, and rate limiting.
- GitHub-ready documentation, workflows, and community files.

### Security

- Removed local-only `.env` from the repository workspace.
- Replaced committed development credentials with placeholders.
- Added secret-safe `.gitignore` rules.