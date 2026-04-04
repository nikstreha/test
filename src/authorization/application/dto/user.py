from dataclasses import dataclass
from datetime import datetime

from authorization.domain.enum.user.role import UserRoles


@dataclass(frozen=True, slots=True)
class UpdateUserDataRequestDTO:
    user_id: int
    phone: str | None
    full_name: str | None


@dataclass(frozen=True, slots=True)
class UserResponseDTO:
    id: int
    email: str
    phone: str | None
    full_name: str | None
    role: UserRoles
    is_active: bool
    created_at: datetime
