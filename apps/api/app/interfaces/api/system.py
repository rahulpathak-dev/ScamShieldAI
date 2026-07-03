from fastapi import APIRouter

from app.core.config import get_settings
from app.core.errors import ServiceUnavailableError
from app.infrastructure.database.session import check_database

router = APIRouter(tags=["system"])


@router.get("/health", summary="Health check")
def health() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "environment": settings.environment,
        "version": settings.app_version,
    }


@router.get("/ready", summary="Readiness check")
def readiness() -> dict[str, object]:
    if not check_database():
        raise ServiceUnavailableError("database")

    return {
        "status": "ready",
        "services": {
            "database": "ok",
        },
    }
