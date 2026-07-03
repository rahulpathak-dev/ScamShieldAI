from dataclasses import dataclass
from uuid import uuid4

from app.application.services.auth_service import PasswordService, TokenService
from app.core.config import Settings
from app.domain.auth import UserRole


@dataclass
class TokenUser:
    id: object
    email: str
    role: UserRole


def test_password_hash_does_not_store_plaintext_and_verifies():
    service = PasswordService()

    password_hash = service.hash_password("StrongPass!123")

    assert password_hash != "StrongPass!123"
    assert service.verify_password("StrongPass!123", password_hash)
    assert not service.verify_password("WrongPass!123", password_hash)


def test_access_token_contains_expected_claims():
    settings = Settings(jwt_secret_key="unit-test-secret-key-that-is-long-enough")
    service = TokenService(settings)
    user_id = uuid4()
    user = TokenUser(id=user_id, email="analyst@example.com", role=UserRole.analyst)

    token = service.create_access_token(user)  # type: ignore[arg-type]
    payload = service.decode_access_token(token)

    assert payload["sub"] == str(user_id)
    assert payload["email"] == "analyst@example.com"
    assert payload["role"] == "ANALYST"
    assert payload["iss"] == "scamshieldai-api"
    assert payload["type"] == "access"