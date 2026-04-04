from datetime import UTC, datetime
from typing import Self

from authorization.domain.entity.common import Entity
from authorization.domain.enum.user.role import UserRoles
from authorization.domain.value_object.user.email import UserEmail
from authorization.domain.value_object.user.full_name import FullUserName
from authorization.domain.value_object.user.id import UserId
from authorization.domain.value_object.user.password_hash import PasswordHash
from authorization.domain.value_object.user.phone import UserPhone


class User(Entity[UserId]):
    def __init__(
        self,
        *,
        id_: UserId,
        email: UserEmail,
        password_hash: PasswordHash,
        created_at: datetime,
        role: UserRoles,
        full_name: FullUserName | None = None,
        phone: UserPhone | None = None,
        is_active: bool = True,
    ) -> None:
        super().__init__(id_=id_)
        self.email = email
        self.password_hash = password_hash
        self.full_name = full_name
        self.phone = phone
        self.role = role
        self.is_active = is_active
        self.created_at = created_at

    @classmethod
    def create(
        cls,
        email: UserEmail,
        password_hash: PasswordHash,
        role: UserRoles,
        is_active: bool = True,
        full_name: FullUserName | None = None,
        phone: UserPhone | None = None,
    ) -> Self:
        now = datetime.now(UTC)
        return cls(
            id_=UserId(),
            email=email,
            password_hash=password_hash,
            role=role,
            created_at=now,
            is_active=is_active,
            full_name=full_name,
            phone=phone,
        )
