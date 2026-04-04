from dataclasses import dataclass, field

from authorization.domain.exception.user import PasswordInvalidError
from authorization.domain.value_object.common import ValueObject

MIN_PASSWORD_LENGTH = 8


@dataclass(frozen=True, slots=True, repr=False)
class RawPassword(ValueObject):
    value: str = field(repr=False)

    def __post_init__(self) -> None:
        if len(self.value) < MIN_PASSWORD_LENGTH:
            raise PasswordInvalidError(
                f"Password must be at least {MIN_PASSWORD_LENGTH} character long"
            )
