from abc import ABC, abstractmethod

from authorization.domain.enum.audit.event import AuditEvent


class IAuditLogWriter(ABC):
    @abstractmethod
    async def add(self, *, user_id: int | None, event: AuditEvent, ip: str) -> None: ...
