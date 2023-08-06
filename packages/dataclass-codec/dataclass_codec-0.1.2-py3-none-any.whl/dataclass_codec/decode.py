import base64
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

from dataclass_codec.types_predicates import (
    is_dataclass_predicate,
    is_enum_predicate,
)


ANYTYPE = Type[Any]


TYPEMATCHPREDICATE = Callable[[ANYTYPE], bool]
DECODEIT = Callable[[Any, ANYTYPE], Any]
TYPEDECODER = Callable[[Any, ANYTYPE, DECODEIT], Any]


T = TypeVar("T")


def raw_decode(
    obj: Any,
    obj_type: Type[T],
    decoders: Dict[ANYTYPE, TYPEDECODER],
    decoders_by_predicate: List[Tuple[TYPEMATCHPREDICATE, TYPEDECODER]],
) -> T:
    def decode_it(obj: Any, _type: ANYTYPE) -> Any:
        return raw_decode(obj, _type, decoders, decoders_by_predicate)

    if obj_type in decoders:
        return cast(T, decoders[obj_type](obj, obj_type, decode_it))

    for predicate, decoder in decoders_by_predicate:
        if predicate(obj_type):
            return cast(T, decoder(obj, obj_type, decode_it))

    raise TypeError(f"Cannot decode {obj_type}")


def primitive_hook(_type: ANYTYPE) -> TYPEDECODER:
    def decode_primitive(
        obj: Any, _type: ANYTYPE, _decode_it: DECODEIT
    ) -> Any:
        # Strict?
        # Convert?
        # Cast?
        return _type(obj)

    return decode_primitive


def list_hook(obj: Any, _type: ANYTYPE, decode_it: DECODEIT) -> Any:
    return [decode_it(i, _type) for i in obj]


def dict_hook(obj: Any, _type: ANYTYPE, decode_it: DECODEIT) -> Any:
    return {k: decode_it(v, _type) for k, v in obj.items()}


def base64_to_bytes(obj: Any, _type: ANYTYPE, _decode_it: DECODEIT) -> Any:
    assert isinstance(obj, str)
    return base64.b64decode(obj)


def iso_datetime_to_datetime(
    obj: Any, _type: ANYTYPE, _decode_it: DECODEIT
) -> Any:
    assert isinstance(obj, str)
    return datetime.fromisoformat(obj)


def iso_date_to_date(obj: Any, _type: ANYTYPE, _decode_it: DECODEIT) -> Any:
    assert isinstance(obj, str)
    return datetime.fromisoformat(obj).date()


def iso_time_to_time(obj: Any, _type: ANYTYPE, _decode_it: DECODEIT) -> Any:
    assert isinstance(obj, str)
    return time.fromisoformat(obj)


def dataclass_from_primitive_dict(
    obj: Any, _type: ANYTYPE, decode_it: DECODEIT
) -> Any:
    assert is_dataclass_predicate(_type)
    assert isinstance(obj, dict)

    return _type(
        **{
            k: decode_it(
                obj[k],
                _type.__dataclass_fields__[k].type,
            )
            if k in obj
            else None
            for k in _type.__dataclass_fields__.keys()
        }
    )


def decimal_from_str(obj: Any, _type: ANYTYPE, _decode_it: DECODEIT) -> Any:
    assert isinstance(obj, (str, int, float))
    return Decimal(obj)


def is_generic_list_predicate(_type: ANYTYPE) -> bool:
    return hasattr(_type, "__origin__") and _type.__origin__ is list


def generic_list_decoder(obj: Any, _type: ANYTYPE, decode_it: DECODEIT) -> Any:
    assert is_generic_list_predicate(_type)
    assert isinstance(obj, list)

    return [decode_it(i, _type.__args__[0]) for i in obj]


def is_dict_predicate(_type: ANYTYPE) -> bool:
    return hasattr(_type, "__origin__") and _type.__origin__ is dict


def generic_dict_decoder(obj: Any, _type: ANYTYPE, decode_it: DECODEIT) -> Any:
    assert is_dict_predicate(_type)
    assert isinstance(obj, dict)

    return {k: decode_it(v, _type.__args__[1]) for k, v in obj.items()}


def is_union_predicate(_type: ANYTYPE) -> bool:
    return hasattr(_type, "__origin__") and _type.__origin__ is Union


def generic_union_decoder(
    obj: Any, _type: ANYTYPE, decode_it: DECODEIT
) -> Any:
    assert is_union_predicate(_type)

    obj_type = type(obj)
    allowed_types = _type.__args__

    if obj_type in allowed_types:
        return decode_it(obj, obj_type)

    raise TypeError(f"Cannot decode {obj_type} as {allowed_types}")


def enum_decoder(obj: Any, _type: ANYTYPE, decode_it: DECODEIT) -> Any:
    assert issubclass(_type, Enum)
    assert isinstance(obj, str)

    return _type[obj]


def inherits_some_class_predicate(_type: ANYTYPE) -> bool:
    return hasattr(_type, "__bases__") and len(_type.__bases__) > 0


def generic_inheritance_decoder(
    obj: Any, _type: ANYTYPE, decode_it: DECODEIT
) -> Any:
    assert inherits_some_class_predicate(_type)

    type(obj)
    parent_types = _type.__bases__
    first_parent_type = parent_types[0]

    return _type(decode_it(obj, first_parent_type))


def is_new_type_predicate(_type: ANYTYPE) -> bool:
    return hasattr(_type, "__supertype__")


def generic_new_type_decoder(
    obj: Any, _type: ANYTYPE, decode_it: DECODEIT
) -> Any:
    assert is_new_type_predicate(_type)

    type(obj)
    supertype = _type.__supertype__

    return _type(decode_it(obj, supertype))


DEFAULT_DECODERS: Dict[ANYTYPE, TYPEDECODER] = {
    **{
        t: primitive_hook(t)
        for t in (
            int,
            float,
            str,
            bool,
            type(None),
        )
    },
    list: list_hook,
    dict: dict_hook,
    bytes: base64_to_bytes,
    datetime: iso_datetime_to_datetime,
    date: iso_date_to_date,
    time: iso_time_to_time,
    Decimal: decimal_from_str,
}

DEFAULT_DECODERS_BY_PREDICATE: List[Tuple[TYPEMATCHPREDICATE, TYPEDECODER]] = [
    (is_dataclass_predicate, dataclass_from_primitive_dict),
    (is_generic_list_predicate, generic_list_decoder),
    (is_dict_predicate, generic_dict_decoder),
    (is_union_predicate, generic_union_decoder),
    # This must be before is_enum_predicate
    (is_new_type_predicate, generic_new_type_decoder),
    (is_enum_predicate, enum_decoder),
    # This must be last
    (inherits_some_class_predicate, generic_inheritance_decoder),
]


def decode(obj: Any, _type: Type[T]) -> T:
    if _type is None:
        _type = type(obj)

    return raw_decode(
        obj, _type, DEFAULT_DECODERS, DEFAULT_DECODERS_BY_PREDICATE
    )
