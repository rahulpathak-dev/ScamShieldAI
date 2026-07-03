import logging
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import get_settings
from app.core.errors import AppError

logger = logging.getLogger("scamshieldai.errors")


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return _error_response(
        request=request,
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
        details=exc.details,
        headers=exc.headers,
    )


async def http_error_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return _error_response(
        request=request,
        status_code=exc.status_code,
        code="http_error",
        message=str(exc.detail),
        details={},
        headers=getattr(exc, "headers", None) or {},
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return _error_response(
        request=request,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        code="validation_error",
        message="Request validation failed.",
        details={"errors": exc.errors()},
        headers={},
    )


async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = _request_id(request)
    logger.exception("unhandled_exception", extra={"request_id": request_id})
    settings = get_settings()
    details: dict[str, Any] = {}
    if not settings.is_production:
        details["exception"] = exc.__class__.__name__

    return _error_response(
        request=request,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        code="internal_server_error",
        message="An unexpected error occurred.",
        details=details,
        headers={},
    )


def _error_response(
    *,
    request: Request,
    status_code: int,
    code: str,
    message: str,
    details: dict[str, Any],
    headers: dict[str, str],
) -> JSONResponse:
    request_id = _request_id(request)
    response = JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "details": details,
                "request_id": request_id,
            }
        },
        headers=headers,
    )
    if request_id:
        response.headers[get_settings().request_id_header] = request_id
    return response


def _request_id(request: Request) -> str | None:
    return getattr(request.state, "request_id", None)