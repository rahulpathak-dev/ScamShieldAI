import logging
import time
from collections import defaultdict, deque
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

logger = logging.getLogger("scamshieldai.request")


class RequestContextMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, request_id_header: str) -> None:
        super().__init__(app)
        self._request_id_header = request_id_header

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get(self._request_id_header) or str(uuid4())
        request.state.request_id = request_id
        started_at = time.perf_counter()
        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
            response.headers[self._request_id_header] = request_id
            return response
        finally:
            duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
            logger.info(
                "request_completed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                },
            )


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        response.headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")
        if request.url.scheme == "https":
            response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        return response


class InMemoryRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *, requests_per_minute: int) -> None:
        super().__init__(app)
        self._requests_per_minute = max(1, requests_per_minute)
        self._window_seconds = 60
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in {"/health", "/ready"}:
            return await call_next(request)

        now = time.time()
        client_key = self._client_key(request)
        hits = self._hits[client_key]

        while hits and now - hits[0] > self._window_seconds:
            hits.popleft()

        if len(hits) >= self._requests_per_minute:
            request_id = getattr(request.state, "request_id", None)
            body = {
                "error": {
                    "code": "rate_limit_exceeded",
                    "message": "Too many requests. Please wait before trying again.",
                    "details": {},
                    "request_id": request_id,
                }
            }
            headers = {"Retry-After": str(self._window_seconds)}
            if request_id:
                headers["X-Request-ID"] = request_id
            return JSONResponse(status_code=429, content=body, headers=headers)

        hits.append(now)
        return await call_next(request)

    @staticmethod
    def _client_key(request: Request) -> str:
        forwarded_for = request.headers.get("x-forwarded-for", "").split(",")[0].strip()
        if forwarded_for:
            return forwarded_for
        if request.client:
            return request.client.host
        return "unknown"