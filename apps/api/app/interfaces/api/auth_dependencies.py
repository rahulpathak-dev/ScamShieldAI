from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.application.services.auth_service import AuthService
from app.core.config import get_settings
from app.core.errors import AuthenticationError, AuthorizationError
from app.domain.auth import UserRole
from app.infrastructure.database.models.user import User
from app.infrastructure.database.session import get_db_session
from app.infrastructure.persistence.audit_log_repository import AuditLogRepository
from app.infrastructure.persistence.user_repository import UserRepository

bearer_scheme = HTTPBearer(auto_error=False)


def get_auth_service(session: Annotated[Session, Depends(get_db_session)]) -> AuthService:
    settings = get_settings()
    return AuthService(
        settings=settings,
        user_repository=UserRepository(session),
        audit_log_repository=AuditLogRepository(session),
    )


def get_current_user(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    token = None
    if credentials is not None and credentials.scheme.lower() == "bearer":
        token = credentials.credentials
    else:
        token = request.cookies.get(get_settings().auth_cookie_name)

    if not token:
        raise AuthenticationError("Missing authentication token.")

    return auth_service.get_user_from_token(token)


def require_roles(*roles: UserRole) -> Callable[[User], User]:
    allowed_roles = set(roles)

    def dependency(current_user: Annotated[User, Depends(get_current_user)]) -> User:
        user_role = current_user.role if isinstance(current_user.role, UserRole) else UserRole(str(current_user.role))
        if user_role not in allowed_roles:
            raise AuthorizationError()
        return current_user

    return dependency