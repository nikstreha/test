from abc import ABC, abstractmethod
from typing import Literal

from authorization.domain.enum.user.role import UserRoles
from authorization.domain.value_object.user.id import UserId

TokenType = Literal["access", "refresh"]


class ITokenProvider(ABC):
    @abstractmethod
    def create_access_token(self, user_id: UserId, role: UserRoles) -> str:
        pass

    @abstractmethod
    def create_refresh_token(self, user_id: UserId, role: UserRoles) -> str:
        pass

    @abstractmethod
    def get_user_id_from_token(
        self, token: str, token_type: TokenType = "access"
    ) -> UserId:
        pass
