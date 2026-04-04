import re
from dataclasses import dataclass

from authorization.domain.exception.user import UserEmailInvalidError
from authorization.domain.value_object.common import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class UserEmail(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise UserEmailInvalidError("Email cannot be empty")

        self._validate_format()

    def _validate_format(self) -> None:
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$"

        if not re.match(pattern, self.value):
            raise UserEmailInvalidError(f"Unexpected email format: {self.value}")

        if len(self.value) > 254:
            raise UserEmailInvalidError("Email is too long")
