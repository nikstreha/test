from authorization.infrastructure.persistence.sqla.mapper.user import map_user_table
from authorization.infrastructure.persistence.sqla.table.audit_log import (
    audit_log_table,  # noqa: F401
)


def map_table() -> None:
    map_user_table()
