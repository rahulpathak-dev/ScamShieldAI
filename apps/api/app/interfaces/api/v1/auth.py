from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status

from app.application.auth_dto import AuthTokenResponse, LoginRequest, RegisterUserRequest, UserResponse
from app.application.services.auth_service import AuthService, RequestMetadata
from app.core.config import Settings, get_settings
from app.domain.auth import UserRole
from app.infrastructure.database.models.user import User
from app.interfaces.api.auth_dependencies import get_auth_service, get_current_user, require_roles

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthTokenResponse, status_code=status.HTTP_201_CREATED)
def register(
    payload: RegisterUserRequest,
    request: Request,
    response: Response,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> AuthTokenResponse:
    token_response = auth_service.register(payload, _request_metadata(request))
    _set_auth_cookie(response, token_response.access_token, token_response.expires_in, settings)
    return token_response


@router.post("/login", response_model=AuthTokenResponse)
def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> AuthTokenResponse:
    token_response = auth_service.login(payload, _request_metadata(request))
    _set_auth_cookie(response, token_response.access_token, token_response.expires_in, settings)
    return token_response


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response, settings: Annotated[Settings, Depends(get_settings)]) -> Response:
    response.delete_cookie(
        key=settings.auth_cookie_name,
        secure=settings.is_production,
        httponly=True,
        samesite="lax",
    )
    return response


@router.get("/me", response_model=UserResponse)
def me(current_user: Annotated[User, Depends(get_current_user)]) -> UserResponse:
    return UserResponse.from_model(current_user)


@router.get("/admin-check", response_model=UserResponse)
def admin_check(current_user: Annotated[User, Depends(require_roles(UserRole.admin))]) -> UserResponse:
    return UserResponse.from_model(current_user)


@router.get("/analyst-check", response_model=UserResponse)
def analyst_check(
    current_user: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.analyst))],
) -> UserResponse:
    return UserResponse.from_model(current_user)


def _set_auth_cookie(response: Response, token: str, max_age: int, settings: Settings) -> None:
    response.set_cookie(
        key=settings.auth_cookie_name,
        value=token,
        max_age=max_age,
        expires=max_age,
        secure=settings.is_production,
        httponly=True,
        samesite="lax",
    )


def _request_metadata(request: Request) -> RequestMetadata:
    client_host = request.client.host if request.client else None
    return RequestMetadata(
        ip_address=client_host,
        user_agent=request.headers.get("user-agent"),
    )