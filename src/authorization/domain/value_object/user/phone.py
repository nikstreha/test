from dataclasses import dataclass

from authorization.domain.exception.user import PhoneInvalidError
from authorization.domain.value_object.common import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class UserPhone(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if self.value is None:
            return
        if len(self.value) > 20:
            raise PhoneInvalidError("Phone is too long")
