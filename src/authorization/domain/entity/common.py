from typing import Any, Self

from authorization.domain.common.util import convert_to_primitive
from authorization.domain.value_object.common import ValueObject


class Entity[T: ValueObject]:
    def __new__(cls, *_args: Any, **_kwargs: Any) -> Self:
        if cls is Entity:
            raise TypeError("'Entity' cannot be instantiated directly.")
        return object.__new__(cls)

    def __init__(self, *, id_: T) -> None:
        self._id = id_

    @property
    def id_(self) -> T:
        return self._id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.id_ == other.id_

    def __hash__(self) -> int:
        return hash((type(self), self.id_))

    def __repr__(self) -> str:
        class_name = type(self).__name__
        item_collection = [f"id_={self.id_!r}"]

        for k, v in self.__dict__.items():
            if not k.startswith("_"):
                item_collection.append(f"{k}={v!r}")

        return f"{class_name}({', '.join(item_collection)})"

    def to_dict(self) -> dict[str, Any]:
        data = {"id": convert_to_primitive(self.id_)}

        for k, v in self.__dict__.items():
            if not k.startswith("_"):
                clean_key = k.rstrip("_")
                data[clean_key] = convert_to_primitive(v)

        return data
