from enum import StrEnum


class UserRole(StrEnum):
    user = "user"
    admin = "admin"
    analyst = "analyst"

    @property
    def api_value(self) -> str:
        return self.value.upper()

    @classmethod
    def from_api_value(cls, value: str) -> "UserRole":
        return cls(value.lower())