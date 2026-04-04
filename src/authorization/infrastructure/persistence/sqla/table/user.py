from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, Table

from authorization.domain.enum.user.role import UserRoles
from authorization.infrastructure.persistence.sqla.registry import mapping_registry

user_table = Table(
    "user",
    mapping_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String(255), nullable=False, unique=True, index=True),
    Column("password_hash", String(128), nullable=False),
    Column("full_name", String(100), nullable=True),
    Column(
        "role", Enum(UserRoles, name="user_role", native_enum=False), nullable=False
    ),
    Column("phone", String(20), nullable=True),
    Column("is_active", Boolean, nullable=False, default=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
)
