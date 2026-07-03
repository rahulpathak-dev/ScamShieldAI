# Security Policy

## Supported Versions

Security updates are currently provided for the `main` branch.

## Reporting a Vulnerability

Please do not report security vulnerabilities through public GitHub issues.

Send a private report to the project maintainer with:

- Affected component
- Reproduction steps
- Expected impact
- Suggested mitigation, if available

Do not include real victim data, private credentials, or live malicious payloads unless they are safely redacted.

## Security Expectations

- Never commit `.env` files or real secrets.
- Use placeholders in examples.
- Keep dependencies updated.
- Validate and sanitize all user-controlled input.
- Avoid logging sensitive user content, passwords, API keys, JWTs, or database URLs.