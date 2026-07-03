# Installation Guide

## Prerequisites

- Docker and Docker Compose
- Node.js 22 for frontend development
- Python 3.12 for backend development
- PostgreSQL client tools for manual backup and restore work

## Local Docker Setup

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Open:

- Web: `http://localhost:3000`
- API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

## Production-style Docker Setup

```powershell
Copy-Item .env.production.example .env.production
# Edit secrets and image names first.
docker compose --env-file .env.production -f docker-compose.prod.yml up -d
```

## Backend Development

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-ml.txt -r requirements-assistant.txt
uvicorn app.main:app --reload
```

## Frontend Development

```powershell
cd apps/web
npm install
npm run dev
```

## Mobile Scaffold

```powershell
cd apps/mobile
npm install
npm run start
```

## Browser Extension

1. Start the API.
2. Open Chrome or Edge extensions.
3. Enable developer mode.
4. Load `apps/browser-extension` as an unpacked extension.
5. Open a suspicious page and scan from the extension popup.