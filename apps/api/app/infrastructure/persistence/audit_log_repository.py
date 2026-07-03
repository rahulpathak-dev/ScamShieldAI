from uuid import UUID

from sqlalchemy.orm import Session

from app.infrastructure.database.models.audit_log import AuditLog


class AuditLogRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def record(
        self,
        *,
        action: str,
        actor_user_id: UUID | None = None,
        entity_type: str | None = None,
        entity_id: UUID | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        self._session.add(
            AuditLog(
                action=action,
                actor_user_id=actor_user_id,
                entity_type=entity_type,
                entity_id=entity_id,
                ip_address=ip_address,
                user_agent=user_agent,
                event_metadata=metadata or {},
            )
        )
        self._session.commit()