import re
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.domain.auth import UserRole
from app.infrastructure.database.models.user import User


class RegisterUserRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned = " ".join(value.strip().split())
        if not cleaned:
            raise ValueError("Name is required.")
        return cleaned

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        checks = [
            (r"[a-z]", "one lowercase letter"),
            (r"[A-Z]", "one uppercase letter"),
            (r"\d", "one number"),
            (r"[^A-Za-z0-9]", "one symbol"),
        ]
        missing = [label for pattern, label in checks if not re.search(pattern, value)]
        if missing:
            raise ValueError(f"Password must contain at least {', '.join(missing)}.")
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    @classmethod
    def from_model(cls, user: User) -> "UserResponse":
        role = user.role.api_value if isinstance(user.role, UserRole) else str(user.role).upper()
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            role=role,
            is_active=user.is_active,
            created_at=user.created_at,
        )


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse