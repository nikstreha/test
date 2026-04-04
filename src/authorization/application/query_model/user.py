from dataclasses import dataclass
from datetime import datetime

from authorization.domain.enum.user.role import UserRoles


@dataclass(frozen=True, slots=True)
class UserQueryModel:
    id: int
    email: str
    phone: str | None
    full_name: str | None
    role: UserRoles
    is_active: bool
    created_at: datetime
    password_hash: str
