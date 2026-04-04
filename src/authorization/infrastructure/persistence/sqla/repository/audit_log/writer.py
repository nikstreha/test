from datetime import UTC, datetime

from sqlalchemy import insert

from authorization.application.port.persistence.repository.audit_log.writer import (
    IAuditLogWriter,
)
from authorization.domain.enum.audit.event import AuditEvent
from authorization.infrastructure.persistence.sqla.table.audit_log import (
    audit_log_table,
)
from authorization.infrastructure.persistence.sqla.type import WriterSession


class SQLAAuditLogWriter(IAuditLogWriter):
    def __init__(self, session: WriterSession) -> None:
        self._session = session

    async def add(self, *, user_id: int | None, event: AuditEvent, ip: str) -> None:
        stmt = insert(audit_log_table).values(
            user_id=user_id,
            event=event,
            ip=ip,
            created_at=datetime.now(UTC),
        )
        await self._session.execute(stmt)
