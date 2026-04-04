from dataclasses import dataclass

from authorization.domain.exception.user import UserNameInvalidError
from authorization.domain.value_object.common import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class FullUserName(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if self.value is None:
            return
        if len(self.value) > 100:
            raise UserNameInvalidError("Full name is too long")
