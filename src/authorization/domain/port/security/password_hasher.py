from abc import ABC, abstractmethod

from authorization.domain.value_object.user.password_hash import PasswordHash
from authorization.domain.value_object.user.raw_password import RawPassword


class IPasswordHasher(ABC):
    @abstractmethod
    async def hash(self, *, raw_password: RawPassword) -> PasswordHash: ...

    @abstractmethod
    async def verify(
        self, *, raw_password: RawPassword, hashed_password: PasswordHash
    ) -> bool: ...
