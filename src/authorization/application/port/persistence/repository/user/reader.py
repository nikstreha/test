from abc import ABC, abstractmethod

from authorization.application.query_model.user import UserQueryModel


class IUserReader(ABC):
    @abstractmethod
    async def read_by_id(self, *, user_id: int) -> UserQueryModel | None: ...

    @abstractmethod
    async def read_by_email(self, *, email: str) -> UserQueryModel | None: ...
