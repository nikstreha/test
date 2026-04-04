from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Table

from authorization.domain.enum.audit.event import AuditEvent
from authorization.infrastructure.persistence.sqla.registry import mapping_registry

audit_log_table = Table(
    "audit_log",
    mapping_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "user_id", Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    ),
    Column(
        "event", Enum(AuditEvent, name="audit_event", native_enum=False), nullable=False
    ),
    Column("ip", String(45), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
)
