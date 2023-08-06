from enum import Enum
from typing import Any, Type


def is_dataclass_predicate(_type: Type[Any]) -> bool:
    return hasattr(_type, "__dataclass_fields__")


def is_enum_predicate(_type: Type[Any]) -> bool:
    return issubclass(_type, Enum)
