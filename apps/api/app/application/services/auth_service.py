from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from pwdlib import PasswordHash

from app.application.auth_dto import AuthTokenResponse, LoginRequest, RegisterUserRequest, UserResponse
from app.core.config import Settings
from app.core.errors import AuthenticationError, ConflictError
from app.domain.auth import UserRole
from app.infrastructure.database.models.user import User
from app.infrastructure.persistence.audit_log_repository import AuditLogRepository
from app.infrastructure.persistence.user_repository import UserRepository


@dataclass(frozen=True)
class RequestMetadata:
    ip_address: str | None = None
    user_agent: str | None = None


class PasswordService:
    _password_hash = PasswordHash.recommended()
    _dummy_hash = _password_hash.hash("DummyPasswordForTiming!123")

    def hash_password(self, password: str) -> str:
        return self._password_hash.hash(password)

    def verify_password(self, plain_password: str, password_hash: str) -> bool:
        return self._password_hash.verify(plain_password, password_hash)

    def verify_dummy(self, plain_password: str) -> None:
        self._password_hash.verify(plain_password, self._dummy_hash)


class TokenService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    @property
    def expires_in_seconds(self) -> int:
        return self._settings.jwt_access_token_expire_minutes * 60

    def create_access_token(self, user: User) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.api_value if isinstance(user.role, UserRole) else str(user.role).upper(),
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=self._settings.jwt_access_token_expire_minutes)).timestamp()),
            "iss": "scamshieldai-api",
            "type": "access",
        }
        return jwt.encode(payload, self._settings.jwt_secret_key, algorithm=self._settings.jwt_algorithm)

    def decode_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                self._settings.jwt_secret_key,
                algorithms=[self._settings.jwt_algorithm],
                issuer="scamshieldai-api",
            )
        except jwt.ExpiredSignatureError as exc:
            raise AuthenticationError("Access token has expired.") from exc
        except jwt.InvalidTokenError as exc:
            raise AuthenticationError("Invalid access token.") from exc

        if payload.get("type") != "access":
            raise AuthenticationError("Invalid token type.")
        return payload


class AuthService:
    def __init__(
        self,
        *,
        settings: Settings,
        user_repository: UserRepository,
        audit_log_repository: AuditLogRepository,
        password_service: PasswordService | None = None,
        token_service: TokenService | None = None,
    ) -> None:
        self._settings = settings
        self._users = user_repository
        self._audit_logs = audit_log_repository
        self._passwords = password_service or PasswordService()
        self._tokens = token_service or TokenService(settings)

    def register(self, request: RegisterUserRequest, metadata: RequestMetadata) -> AuthTokenResponse:
        existing = self._users.get_by_email(request.email)
        if existing is not None:
            self._audit_logs.record(
                action="auth.register.conflict",
                ip_address=metadata.ip_address,
                user_agent=metadata.user_agent,
                metadata={"email": request.email},
            )
            raise ConflictError("An account with this email already exists.", {"field": "email"})

        user = self._users.create_user(
            name=request.name,
            email=request.email,
            password_hash=self._passwords.hash_password(request.password),
            role=UserRole.user,
        )
        self._audit_logs.record(
            action="auth.register.success",
            actor_user_id=user.id,
            entity_type="users",
            entity_id=user.id,
            ip_address=metadata.ip_address,
            user_agent=metadata.user_agent,
        )
        return self._token_response(user)

    def login(self, request: LoginRequest, metadata: RequestMetadata) -> AuthTokenResponse:
        user = self._users.get_by_email(request.email)
        if user is None:
            self._passwords.verify_dummy(request.password)
            self._record_failed_login(request, metadata)
            raise AuthenticationError("Invalid email or password.")

        if not self._passwords.verify_password(request.password, user.password_hash):
            self._record_failed_login(request, metadata)
            raise AuthenticationError("Invalid email or password.")

        if not user.is_active:
            self._audit_logs.record(
                action="auth.login.inactive_user",
                actor_user_id=user.id,
                ip_address=metadata.ip_address,
                user_agent=metadata.user_agent,
            )
            raise AuthenticationError("Account is inactive.")

        self._users.touch_last_login(user)
        self._audit_logs.record(
            action="auth.login.success",
            actor_user_id=user.id,
            entity_type="users",
            entity_id=user.id,
            ip_address=metadata.ip_address,
            user_agent=metadata.user_agent,
        )
        return self._token_response(user)

    def get_user_from_token(self, token: str) -> User:
        payload = self._tokens.decode_access_token(token)
        subject = payload.get("sub")
        if not subject:
            raise AuthenticationError("Invalid access token.")

        try:
            user_id = UUID(subject)
        except ValueError as exc:
            raise AuthenticationError("Invalid access token subject.") from exc

        user = self._users.get_by_id(user_id)
        if user is None or not user.is_active:
            raise AuthenticationError("Authenticated user was not found.")
        return user

    def _token_response(self, user: User) -> AuthTokenResponse:
        return AuthTokenResponse(
            access_token=self._tokens.create_access_token(user),
            expires_in=self._tokens.expires_in_seconds,
            user=UserResponse.from_model(user),
        )

    def _record_failed_login(self, request: LoginRequest, metadata: RequestMetadata) -> None:
        self._audit_logs.record(
            action="auth.login.failed",
            ip_address=metadata.ip_address,
            user_agent=metadata.user_agent,
            metadata={"email": request.email},
        )