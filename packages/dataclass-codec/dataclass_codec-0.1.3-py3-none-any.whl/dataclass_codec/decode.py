import base64
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Optional,
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


@dataclass
class DecodeContext:
    strict: bool = False
    primitive_cast_values: bool = True
    dataclass_unset_as_none: bool = True
    collect_errors: bool = False


decode_context_cxt_var = ContextVar(
    "decode_context_cxt_var", default=DecodeContext()
)


def decode_context() -> DecodeContext:
    return decode_context_cxt_var.get()


@contextmanager
def decode_context_scope(
    decode_context: DecodeContext,
) -> Generator[None, Any, None]:
    token = decode_context_cxt_var.set(decode_context)
    try:
        yield
    finally:
        decode_context_cxt_var.reset(token)


error_list_cxt_var = ContextVar[List[Tuple[str, Exception]]](
    "error_list_cxt_var", default=[]
)


def error_list() -> List[Tuple[str, Exception]]:
    return error_list_cxt_var.get()


@contextmanager
def error_list_scope(
    error_list: Optional[List[Tuple[str, Exception]]] = None,
) -> Generator[List[Tuple[str, Exception]], Any, None]:
    if error_list is None:
        error_list = []
    token = error_list_cxt_var.set(error_list)
    try:
        yield error_list
    finally:
        error_list_cxt_var.reset(token)


current_path_cxt_var = ContextVar("current_path_cxt_var", default="$")


def current_path() -> str:
    return current_path_cxt_var.get()


@contextmanager
def current_path_scope(path: str) -> Generator[None, Any, None]:
    token = current_path_cxt_var.set(path)
    try:
        yield

    except Exception as e:
        error_list().append((current_path(), e))
        if not decode_context().collect_errors:
            raise
    finally:
        current_path_cxt_var.reset(token)


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
        ctx = decode_context()

        if ctx.primitive_cast_values:
            return _type(obj)

        if ctx.strict and _type(obj) != obj:
            raise TypeError(f"Cannot decode {obj} as {_type}")

        return obj

    return decode_primitive


def list_hook(obj: Any, _type: ANYTYPE, decode_it: DECODEIT) -> Any:
    return [decode_it(i, _type) for i in obj]


def dict_hook(obj: Any, _type: ANYTYPE, decode_it: DECODEIT) -> Any:
    assert isinstance(obj, dict)

    def make_value(k: str) -> Any:
        with current_path_scope(current_path() + "." + k):
            return decode_it(obj[k], _type)

    return {k: make_value(v) for k, v in obj.items()}


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
    cxt = decode_context()
    assert is_dataclass_predicate(_type)
    assert isinstance(obj, dict)

    def make_value(k: str) -> Any:
        with current_path_scope(current_path() + "." + k):
            if k not in obj:
                if cxt.dataclass_unset_as_none:
                    return None
                else:
                    raise ValueError(f"Missing key {k}")

            return decode_it(obj[k], _type.__dataclass_fields__[k].type)

    return _type(
        **{k: make_value(k) for k in _type.__dataclass_fields__.keys()}
    )


def decimal_from_str(obj: Any, _type: ANYTYPE, _decode_it: DECODEIT) -> Any:
    assert isinstance(obj, (str, int, float))
    return Decimal(obj)


def is_generic_list_predicate(_type: ANYTYPE) -> bool:
    return hasattr(_type, "__origin__") and _type.__origin__ is list


def generic_list_decoder(obj: Any, _type: ANYTYPE, decode_it: DECODEIT) -> Any:
    assert is_generic_list_predicate(_type)
    assert isinstance(obj, list)

    def make_value(i: int) -> Any:
        with current_path_scope(current_path() + f"[{i}]"):
            return decode_it(obj[i], _type.__args__[0])

    return [make_value(i) for i in range(len(obj))]


def is_generic_dict_predicate(_type: ANYTYPE) -> bool:
    return hasattr(_type, "__origin__") and _type.__origin__ is dict


def generic_dict_decoder(obj: Any, _type: ANYTYPE, decode_it: DECODEIT) -> Any:
    assert is_generic_dict_predicate(_type)
    assert isinstance(obj, dict)

    def make_value(k: str) -> Any:
        with current_path_scope(current_path() + "." + k):
            return decode_it(obj[k], _type.__args__[1])

    return {k: make_value(k) for k in obj.keys()}


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
    (is_generic_dict_predicate, generic_dict_decoder),
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
    with current_path_scope("$"):
        return raw_decode(
            obj, _type, DEFAULT_DECODERS, DEFAULT_DECODERS_BY_PREDICATE
        )
