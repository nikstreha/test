import dataclasses
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Any


# noinspection PyBroadException
def convert_to_primitive(obj: Any) -> Any:
    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj

    if hasattr(obj, "to_dict") and callable(obj.to_dict):
        return obj.to_dict()

    if isinstance(obj, int):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, (date, time)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, Enum):
        return obj.value

    if dataclasses.is_dataclass(obj):
        return {
            f.name: convert_to_primitive(getattr(obj, f.name))
            for f in dataclasses.fields(obj)
        }

    if isinstance(obj, (list, tuple, set)):
        return [convert_to_primitive(i) for i in obj]
    if isinstance(obj, dict):
        return {str(k): convert_to_primitive(v) for k, v in obj.items()}

    try:
        return str(obj)
    except Exception:
        return f"<Unserializable object of type {type(obj).__name__}>"
