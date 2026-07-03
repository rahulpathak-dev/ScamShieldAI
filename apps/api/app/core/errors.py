from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AppError(Exception):
    code: str
    message: str
    status_code: int = 400
    details: dict[str, Any] = field(default_factory=dict)
    headers: dict[str, str] = field(default_factory=dict)

    def __str__(self) -> str:
        return self.message


class AuthenticationError(AppError):
    def __init__(self, message: str = "Authentication failed.") -> None:
        super().__init__(
            code="authentication_failed",
            message=message,
            status_code=401,
            headers={"WWW-Authenticate": "Bearer"},
        )


class AuthorizationError(AppError):
    def __init__(self, message: str = "You do not have permission to access this resource.") -> None:
        super().__init__(
            code="authorization_failed",
            message=message,
            status_code=403,
        )


class ConflictError(AppError):
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(
            code="conflict",
            message=message,
            status_code=409,
            details=details or {},
        )


class ResourceNotFoundError(AppError):
    def __init__(self, resource: str, identifier: str) -> None:
        super().__init__(
            code="resource_not_found",
            message=f"{resource} was not found.",
            status_code=404,
            details={"resource": resource, "identifier": identifier},
        )


class ServiceUnavailableError(AppError):
    def __init__(self, service: str) -> None:
        super().__init__(
            code="service_unavailable",
            message=f"{service} is unavailable.",
            status_code=503,
            details={"service": service},
        )