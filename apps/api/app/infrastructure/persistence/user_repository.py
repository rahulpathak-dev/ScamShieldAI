from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import ConflictError
from app.domain.auth import UserRole
from app.infrastructure.database.models.user import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, user_id: UUID) -> User | None:
        return self._session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == self._normalize_email(email))
        return self._session.scalar(statement)

    def create_user(self, *, name: str, email: str, password_hash: str, role: UserRole = UserRole.user) -> User:
        user = User(
            name=name,
            email=self._normalize_email(email),
            password_hash=password_hash,
            role=role,
        )
        self._session.add(user)
        try:
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()
            raise ConflictError("An account with this email already exists.", {"field": "email"}) from exc
        self._session.refresh(user)
        return user

    def touch_last_login(self, user: User) -> None:
        user.last_login_at = datetime.now(UTC)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)

    def _normalize_email(self, email: str) -> str:
        return email.strip().casefold()