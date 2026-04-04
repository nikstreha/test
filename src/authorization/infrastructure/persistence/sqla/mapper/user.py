from sqlalchemy.orm import composite

from authorization.domain.entity.user import User
from authorization.domain.value_object.user.email import UserEmail
from authorization.domain.value_object.user.full_name import FullUserName
from authorization.domain.value_object.user.id import UserId
from authorization.domain.value_object.user.password_hash import PasswordHash
from authorization.domain.value_object.user.phone import UserPhone
from authorization.infrastructure.persistence.sqla.registry import mapping_registry
from authorization.infrastructure.persistence.sqla.table.user import user_table


def map_user_table() -> None:
    mapping_registry.map_imperatively(
        User,
        user_table,
        properties={
            "_id": composite(UserId, user_table.c.id),
            "email": composite(UserEmail, user_table.c.email),
            "password_hash": composite(PasswordHash, user_table.c.password_hash),
            "full_name": composite(FullUserName, user_table.c.full_name),
            "role": user_table.c.role,
            "phone": composite(UserPhone, user_table.c.phone),
            "is_active": user_table.c.is_active,
            "created_at": user_table.c.created_at,
        },
        column_prefix="_raw_",
    )
