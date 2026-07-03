# Contributing to ScamShieldAI

Thank you for your interest in contributing. ScamShieldAI is an AI cybersecurity project, so security, clarity, and responsible behavior matter.

## Development Workflow

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Install backend and frontend dependencies.
4. Make focused changes.
5. Run tests and checks before opening a pull request.

## Local Checks

Backend:

```bash
cd apps/api
pytest
```

Frontend:

```bash
cd apps/web
npm run lint
npm run typecheck
npm run build
```

## Pull Request Guidelines

- Keep pull requests small and focused.
- Include tests for behavior changes.
- Never commit secrets, real credentials, private user data, or proprietary datasets.
- Document new environment variables in `.env.example` and README.
- Prefer clear, maintainable code over clever shortcuts.

## Security Contributions

If you find a vulnerability, do not open a public issue. Follow `SECURITY.md`.