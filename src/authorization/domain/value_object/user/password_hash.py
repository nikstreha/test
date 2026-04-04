from dataclasses import dataclass, field

from authorization.domain.exception.user import PasswordHashInvalidError
from authorization.domain.value_object.common import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class PasswordHash(ValueObject):
    value: str = field(repr=False)

    def __post_init__(self) -> None:
        if not self.value:
            raise PasswordHashInvalidError("Password hash cannot be empty")
