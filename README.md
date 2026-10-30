# ScamShieldAI

Professional AI-powered Scam Detection Platform.

ScamShieldAI is a full-stack cybersecurity product for analyzing suspicious messages, emails, URLs, chats, and financial scam content. It combines NLP, risk scoring, persuasion strategy detection, explainable AI, PostgreSQL persistence, and a modern web dashboard.

## Features

- AI Scam Detection
- Email Scam Detection
- SMS Scam Detection
- URL Detection
- Risk Score
- Persuasion Strategy Detection
- AI Explanation
- Dashboard
- Scan History
- PostgreSQL Database
- FastAPI Backend
- Modern Frontend
- Docker Support

## Screenshots

Add screenshots after running the project locally:

- Landing page: `docs/screenshots/landing-page.png`
- Scam analyzer: `docs/screenshots/scam-analyzer.png`
- Dashboard: `docs/screenshots/dashboard.png`
- Scan history: `docs/screenshots/history.png`
- Admin dashboard: `docs/screenshots/admin-dashboard.png`

## Architecture

ScamShieldAI uses a modular monorepo architecture:

- `apps/api`: FastAPI backend with clean API, application, domain, and infrastructure layers.
- `apps/web`: Next.js frontend for landing page, dashboard, scanner, auth, and history views.
- `infra/db`: PostgreSQL schema migrations.
- `infra/monitoring`: Prometheus monitoring configuration.
- `infra/nginx`: Reverse proxy configuration.
- `knowledge`: RAG-ready scam knowledge sources.
- `docs`: Architecture, API, operations, and module documentation.

The backend exposes REST APIs for scan analysis, authentication, persuasion detection, notifications, assistant workflows, multilingual support, browser extension flows, mobile flows, and enterprise batch analysis.

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | Next.js, TypeScript, Tailwind CSS, Recharts, lucide-react |
| Backend | FastAPI, Pydantic, SQLAlchemy, JWT authentication |
| AI/NLP | Scikit-learn, Transformers-ready services, explainability scaffolds |
| Database | PostgreSQL |
| Infrastructure | Docker Compose, Nginx, Prometheus |
| Testing | Pytest, ESLint, TypeScript checks |

## Installation

Requirements:

- Python 3.11+
- Node.js 20+
- Docker Desktop
- Git

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ScamShieldAI.git
cd ScamShieldAI
```

Create local environment files from examples:

```bash
cp .env.example .env
cp apps/api/.env.example apps/api/.env
cp apps/web/.env.example apps/web/.env.local
```

Update the copied `.env` files with your own local passwords and secrets. Never commit real `.env` files.

## Local Development

Start PostgreSQL with Docker:

```bash
docker compose up -d postgres
```

Run database migrations:

```bash
cat infra/db/migrations/0001_create_scam_analyses.sql | docker exec -i scamshieldai-postgres psql -U scamshield -d scamshieldai
cat infra/db/migrations/0002_create_core_product_schema.sql | docker exec -i scamshieldai-postgres psql -U scamshield -d scamshieldai
```

Run the backend:

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-ml.txt -r requirements-assistant.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

On Windows PowerShell, activate the backend virtual environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run the frontend:

```bash
cd apps/web
npm install
npm run dev
```

Open:

- Frontend: `http://localhost:3000`
- Backend docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`
- Readiness check: `http://localhost:8000/ready`

## Docker Setup

Run the full stack with Docker Compose:

```bash
cp .env.example .env
docker compose up --build
```

Services:

- Web: `http://localhost:3000`
- API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

## API Documentation

FastAPI automatically serves OpenAPI documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Important endpoints:

- `GET /health`
- `GET /ready`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/analyze/text`
- `GET /api/v1/analyze/history`
- `POST /api/v1/persuasion/detect`
- `POST /api/v1/risk/score`
- `POST /api/v1/notifications/high-risk-warning`
- `POST /api/v1/assistant/ask`
- `POST /api/v1/enterprise/batch-analyze`

## Database

ScamShieldAI uses PostgreSQL for users, audit logs, scan history, reports, alerts, threat intelligence, and model results.

Migration files live in:

```text
infra/db/migrations/
```

Use lowercase database name `scamshieldai`. Avoid mixed-case database names because PostgreSQL treats quoted and unquoted identifiers differently.

## Environment Variables

Do not commit real secrets. Use `.env.example` files as templates only.

Key variables:

| Variable | Purpose |
| --- | --- |
| `POSTGRES_DB` | PostgreSQL database name |
| `POSTGRES_USER` | PostgreSQL user |
| `POSTGRES_PASSWORD` | PostgreSQL password for local Docker only |
| `SCAMSHIELD_DATABASE_URL` | Backend database connection string |
| `SCAMSHIELD_JWT_SECRET_KEY` | JWT signing secret |
| `SCAMSHIELD_CORS_ORIGINS` | Allowed frontend origins |
| `SCAMSHIELD_RATE_LIMIT_REQUESTS_PER_MINUTE` | API request throttle |
| `NEXT_PUBLIC_API_BASE_URL` | Public frontend API base URL |

## Deployment

Production deployment should use managed secrets and managed infrastructure:

- Store database URLs, JWT secrets, SMTP credentials, and API provider keys in a secret manager.
- Use HTTPS behind a reverse proxy or cloud load balancer.
- Run PostgreSQL with automated backups.
- Enable monitoring and alerting.
- Rotate credentials regularly.

See:

- `docs/production-readiness.md`
- `docs/operations-runbook.md`
- `infra/cloud/aws/production-checklist.md`

## Folder Structure

```text
ScamShieldAI/
  apps/
    api/                  FastAPI backend
    web/                  Next.js frontend
    mobile/               Mobile app scaffold
    browser-extension/    Browser extension scaffold
  docs/                   Architecture and module documentation
  infra/
    db/migrations/        PostgreSQL migrations
    monitoring/           Prometheus config
    nginx/                Reverse proxy config
    backup/               Backup scripts
  knowledge/              Scam guidance and RAG knowledge sources
  ml/                     ML documentation and artifact folders
  .github/workflows/      CI/CD workflows
```


## Deployment Guide

Recommended production path:

- Frontend: deploy `apps/web` to Vercel or Netlify.
- Backend: deploy `apps/api` to Render, Railway, Fly.io, or a Docker host.
- Database: use Supabase, Neon, Railway PostgreSQL, Render PostgreSQL, or managed AWS RDS.
- Set `NEXT_PUBLIC_API_BASE_URL` in the frontend host to the deployed backend URL.
- Set `SCAMSHIELD_DATABASE_URL`, `SCAMSHIELD_JWT_SECRET_KEY`, and `SCAMSHIELD_CORS_ORIGINS` in the backend host.
- Never upload `.env` files to GitHub or a public frontend runtime.

Production checklist:

- Use HTTPS for frontend and backend.
- Use a strong 32+ character JWT secret.
- Use managed PostgreSQL backups.
- Restrict CORS to the real frontend domain.
- Rotate secrets before public demos.
- Confirm `/health`, `/ready`, and `/docs` work after deployment.

## Troubleshooting

- If PostgreSQL says the database does not exist, use lowercase `scamshieldai` and rerun migrations.
- If the backend cannot connect from local Windows, use `localhost` in `apps/api/.env`.
- If the backend runs inside Docker, use `postgres` as the database hostname.
- If frontend requests fail, check `NEXT_PUBLIC_API_BASE_URL`.
- If `npm run build` fails with `ENOSPC`, free disk space and rerun install/build.
- If Git tries to add `.env`, stop and check `.gitignore` before committing.

## Browser Test Checklist

- Open landing page on desktop and mobile viewport.
- Open dashboard, analyzer, and history routes.
- Scan a suspicious message and confirm score, category, explanation, and advice render.
- Confirm browser console has no secret values or stack traces.
- Test in Chrome, Edge, and Firefox where available.

## Future Roadmap

- Production-trained transformer classifier and model registry
- Redis-backed distributed rate limiting
- OCR pipeline for screenshot scam detection
- Speech-to-text integration for voice scam detection
- Enterprise tenant management and API keys
- Model drift monitoring and feedback loops
- Full observability dashboards
- Cloud deployment templates for AWS, Azure, and GCP

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Author

ScamShieldAI was created as a professional AI cybersecurity project for scam detection, explainability, and user protection.