import base64
from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, NewType, Optional, Union

import pytest

from dataclass_codec import encode, decode


def optional(cls: Any) -> Any:
    raise NotImplementedError


def get_class_or_type_name(cls: Any) -> str:
    raise NotImplementedError


class LocatedValidationErrorCollection(Exception):
    def __init__(self, errors: Dict[str, Exception]) -> None:
        self.errors = errors


class TestJsonDeserializerCodec:
    def test_decode_True_false(self) -> None:
        assert decode((True), bool) is True

    def test_decode_false(self) -> None:
        assert decode(False, bool) is False

    def test_decode_int(self) -> None:
        assert decode(("1"), int) == 1

    def test_decode_int_str(self) -> None:
        assert decode(("1"), int) == 1

    def test_decode_decimal(self) -> None:
        assert decode(("1"), Decimal) == Decimal("1")
        assert decode(("1.1"), Decimal) == Decimal("1.1")

    def test_decode_float(self) -> None:
        assert decode(("1.1"), float) == 1.1

    def test_decode_str(self) -> None:
        assert decode(("1.1"), str) == "1.1"

    def test_decode_int_list(self) -> None:
        assert decode(([1, 1]), List[int]) == [1, 1]

    def test_frozen_dataclass(self) -> None:
        @dataclass(frozen=True)
        class User:
            name: str
            age: int

        assert decode({"name": "John", "age": 30}, User) == User(
            name="John", age=30
        )

    def test_decode_generic_list(self) -> None:
        assert decode(([1, 1]), List[int]) == [1, 1]

    def test_decode_generic_dict(self) -> None:
        assert decode(({"a": 1}), Dict[str, int]) == {"a": 1}

    def test_basic_dataclass(self) -> None:
        @dataclass
        class Dummy:
            text_list: List[str]
            text_dict: Dict[str, Decimal]
            optional_text: Optional[str]

        dummy_dict = {
            "text_list": ["a", "b", "c"],
            "text_dict": {"a": 1.0, "b": 2, "c": "3.3", "d": 2.2},
            "optional_text": "hello",
        }

        parsed = decode(dummy_dict, Dummy)

        assert parsed.text_list == ["a", "b", "c"]
        assert parsed.text_dict["a"] == Decimal("1.0")
        assert parsed.text_dict["b"] == Decimal("2.0")
        assert parsed.text_dict["c"] == Decimal("3.3")
        assert parsed.text_dict["d"].quantize(Decimal("1.0")) == Decimal("2.2")
        assert parsed.optional_text == "hello"

    def test_nested_dataclass(self) -> None:
        @dataclass
        class NestedDummy:
            text: str
            number: Decimal

            boolean: bool

        @dataclass
        class Dummy:
            text_list: List[str]
            text_dict: Dict[str, Decimal]
            nested: NestedDummy

        dummy_dict = {
            "text_list": ["a", "b", "c"],
            "text_dict": {"a": 1.0, "b": 2, "c": "3.3", "d": 2.2},
            "nested": {"text": "hello", "number": 1.1, "boolean": True},
        }

        parsed = decode(dummy_dict, Dummy)

        assert parsed.text_list == ["a", "b", "c"]
        assert parsed.text_dict["a"] == Decimal("1.0")
        assert parsed.text_dict["b"] == Decimal("2.0")
        assert parsed.text_dict["c"] == Decimal("3.3")
        assert parsed.text_dict["d"].quantize(Decimal("1.0")) == Decimal("2.2")
        assert parsed.nested.text == "hello"
        assert parsed.nested.number.quantize(Decimal("1.0")) == Decimal("1.1")
        assert parsed.nested.boolean is True

    def test_raise_when_type_not_mapped(self) -> None:
        with pytest.raises(TypeError):

            class NonMappedDummy:
                pass

            @dataclass
            class Dummy:
                text: str
                non_mapped: NonMappedDummy

            dummy_dict = {"text": "hello", "non_mapped": {}}

            decode(dummy_dict, Dummy)

    def test_enum(self) -> None:
        class MyEnum(Enum):
            A = "A"
            B = "B"

        @dataclass
        class Dummy:
            my_enum: MyEnum

        dummy_dict = {"my_enum": "A"}

        a = decode(dummy_dict, Dummy)

        assert a.my_enum == MyEnum.A

    def test_date(self) -> None:
        @dataclass
        class Dummy:
            date_time: datetime
            date_: date
            time_: time

        dummy_dict = {
            "date_": "2020-01-01",
            "date_time": "2020-01-01T00:00:00+00:00",
            "time_": "00:00:00",
        }

        a = decode(dummy_dict, Dummy)

        assert a.date_ == date(2020, 1, 1)
        assert a.date_time == datetime(
            2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc
        )
        assert a.time_ == time(0, 0, 0)

    def test_primitive_class_inheritance(self) -> None:
        class MyInt(int):
            pass

        @dataclass
        class Dummy:
            my_int: MyInt

        dummy_dict = {"my_int": 1}

        a = decode(dummy_dict, Dummy)

        assert a.my_int == MyInt(1)

    def test_primitive_class_inheritance_class_match(self) -> None:
        class MyInt(int):
            pass

        @dataclass
        class Dummy:
            my_int: MyInt

        dummy_dict = {"my_int": "1"}

        parsed = decode(dummy_dict, Dummy)

        assert parsed.my_int == MyInt(1)
        assert isinstance(parsed.my_int, MyInt)

    def test_decode_newtype(self) -> None:
        UserId = NewType("UserId", int)

        assert decode(("1"), UserId) == UserId(1)
        assert isinstance(decode(("1"), UserId), int)

    def test_encode_and_decode_bytes(self) -> None:
        hello_bytes = b"hello"

        base64_hello_bytes = base64.b64encode(hello_bytes).decode("utf-8")

        assert encode(hello_bytes) == base64_hello_bytes

        assert decode(base64_hello_bytes, bytes) == hello_bytes

        @dataclass
        class Dummy:
            bytes_: bytes

        dummy_dict = {"bytes_": "aGVsbG8="}

        parsed = decode(dummy_dict, Dummy)

        assert parsed.bytes_ == hello_bytes

    def test_encode_str(self) -> None:
        assert encode("hello") == "hello"

    def test_encode_int(self) -> None:
        assert encode(1) == 1

    def test_encode_float(self) -> None:
        assert encode(1.0) == 1.0

    def test_encode_bool(self) -> None:
        assert encode(True) is True

    def test_encode_none(self) -> None:
        assert encode(None) is None

    def test_encode_list(self) -> None:
        assert encode([1, 2, 3]) == [1, 2, 3]

    def test_encode_tuple(self) -> None:
        assert encode((1, 2, 3)) == [1, 2, 3]

    def test_encode_dict(self) -> None:
        assert encode({"a": 1}) == {"a": 1}

    def test_encode_datetime(self) -> None:
        assert (
            encode(datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc))
            == "2020-01-01T00:00:00+00:00"
        )

    def test_encode_date(self) -> None:
        assert encode(date(2020, 1, 1)) == "2020-01-01"

    def test_encode_time(self) -> None:
        assert encode(time(0, 0, 0)) == "00:00:00"

    def test_encode_enum(self) -> None:
        class MyEnum(Enum):
            A = "A"
            B = "B"

        assert encode(MyEnum.A) == "A"

    def test_encode_newtype(self) -> None:
        UserId = NewType("UserId", int)

        assert encode(UserId(1)) == 1

    def test_encode_bytes(self) -> None:
        hello_bytes = b"hello"

        base64_hello_bytes = base64.b64encode(hello_bytes).decode("utf-8")

        assert encode(hello_bytes) == base64_hello_bytes

    def test_encode_dataclass(self) -> None:
        @dataclass
        class Dummy:
            a: int

        assert encode(Dummy(1)) == {"a": 1}

    def test_encode_nested_dataclass(self) -> None:
        @dataclass
        class Dummy:
            a: int

        @dataclass
        class Dummy2:
            dummy: Dummy

        assert encode(Dummy2(Dummy(1))) == {"dummy": {"a": 1}}

    def test_cu(self) -> None:
        a = {
            "id": 7,
            "created_on": "2023-06-18 00:40:24",
            "modified_on": "2023-06-18 00:40:24",
            "owner_user_id": 1,
            "domain_names": [
                "brutus.example.com",
                "casca.example.com",
                "cassius.example.com",
                "decius.example.com",
                "metellus.example.com",
            ],
            "forward_host": "localhost",
            "forward_port": 8080,
            "access_list_id": 0,
            "certificate_id": 0,
            "ssl_forced": 0,
            "caching_enabled": 0,
            "block_exploits": 0,
            "advanced_config": "",
            "meta": {},
            "allow_websocket_upgrade": 0,
            "http2_support": 0,
            "forward_scheme": "http",
            "enabled": 1,
            "locations": [],
            "hsts_enabled": 0,
            "hsts_subdomains": 0,
            "certificate": None,
            "owner": {
                "id": 1,
                "created_on": "2023-06-17 20:01:58",
                "modified_on": "2023-06-17 20:01:58",
                "is_deleted": 0,
                "is_disabled": 0,
                "email": "admin@example.com",
                "name": "Administrator",
                "nickname": "Admin",
                "avatar": "",
                "roles": ["admin"],
            },
            "access_list": None,
            "use_default_location": True,
            "ipv6": True,
        }

        @dataclass
        class Location:
            path: str
            advanced_config: str
            forward_scheme: str
            forward_host: str
            forward_port: str

        @dataclass
        class ProxyHostAddResponse:
            id: int
            created_on: str
            modified_on: str
            owner_user_id: int
            domain_names: List[str]
            forward_host: str
            forward_port: int
            access_list_id: int
            certificate_id: int
            ssl_forced: int
            caching_enabled: int
            block_exploits: int
            advanced_config: str
            meta: Dict[str, Union[bool, str, int]]
            allow_websocket_upgrade: int
            http2_support: int
            forward_scheme: str
            enabled: int
            locations: List[Location]
            hsts_enabled: int
            hsts_subdomains: int
            # certificate: Optional[Certificate]
            # owner: User
            # access_list: AccessList
            use_default_location: bool
            ipv6: bool

        decode(a, ProxyHostAddResponse)
