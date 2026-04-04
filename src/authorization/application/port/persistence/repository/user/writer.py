from abc import ABC, abstractmethod

from authorization.domain.entity.user import User
from authorization.domain.value_object.user.email import UserEmail
from authorization.domain.value_object.user.id import UserId


class IUserWriter(ABC):
    @abstractmethod
    async def add(self, *, user: User) -> None: ...

    @abstractmethod
    async def find_by_id(
        self, *, user_id: UserId, for_update: bool = False
    ) -> User | None: ...

    @abstractmethod
    async def find_by_email(self, *, email: UserEmail) -> User | None: ...
