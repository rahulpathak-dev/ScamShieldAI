from fastapi import FastAPI
from app.routes.analyzer import router as analyzer_router

app = FastAPI(title="ScamShieldAI", version="0.1.0")
app.include_router(analyzer_router)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
