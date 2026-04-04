from dataclasses import dataclass

from authorization.domain.value_object.common import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class UserId(ValueObject):
    value: int | None = None
