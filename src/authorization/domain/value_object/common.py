from dataclasses import dataclass, fields
from typing import Any, Self

from authorization.domain.common.util import convert_to_primitive


@dataclass(frozen=True, slots=True, repr=False)
class ValueObject:
    def __new__(cls, *_args: Any, **_kwargs: Any) -> Self:
        if cls is ValueObject:
            raise TypeError("'ValueObject' cannot be instantiated directly.")
        if not fields(cls):
            raise TypeError(f"{cls.__name__} must have at least one field.")
        return object.__new__(cls)

    def __post_init__(self) -> None:
        pass

    def __repr__(self) -> str:
        value_collection = self._get_visible_value()

        if not value_collection:
            return f"{type(self).__name__}(<hidden>)"

        if len(value_collection) == 1:
            val = next(iter(value_collection.values()))
            return f"{type(self).__name__}({val!r})"

        items = [f"{k}={v!r}" for k, v in value_collection.items()]
        return f"{type(self).__name__}({', '.join(items)})"

    def to_dict(self) -> Any:
        values = self._get_visible_value()

        if not values:
            return "<hidden>"

        if len(values) == 1:
            val = next(iter(values.values()))
            return convert_to_primitive(val)

        return {k: convert_to_primitive(v) for k, v in values.items()}

    def _get_visible_value(self) -> dict[str, Any]:
        return {f.name: getattr(self, f.name) for f in fields(self) if f.repr}
