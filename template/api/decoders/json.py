from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import TypeVar

import dataclasses
from typing import get_origin

from template.utils.types import is_optional

Item = TypeVar('Item')


class JSONDecodeException(Exception):

    def __init__(self, error: str):
        self._error = error

    @property
    def message(self):
        return self._error

    @classmethod
    def fields_decode_exception(cls, type: Type[Item], errors: Dict[str, str]) -> 'JSONDecodeException':
        return cls(f'Cannot decode fields for "{type}": {str(errors)}')

    @classmethod
    def missing_fields_exception(cls, type: Type[Item], field_names: List[str]) -> 'JSONDecodeException':
        missing_fields_serialized = '", "'.join(field_names)
        return cls(f'Missing fields for "{type}": {missing_fields_serialized}')

    @classmethod
    def cannot_decode(cls, value: Any, type_name: str) -> 'JSONDecodeException':
        return cls(f'Cannot decode "{value}" to {type_name}')

    @classmethod
    def cannot_find_decoder(cls, type: Type[Item]) -> 'JSONDecodeException':
        return cls(f'Cannot find decoder for type  "{type}"')


def json_decode(value, type_: Type) -> Item:
    type__: Type[Item] = type_
    decoder = _get_decoder(type__)

    return decoder(value, type__)


def _get_decoder(type_: Type[Item]):
    if is_optional(type_):
        return decode_optional

    origin_type = get_origin(type_) or type_

    decoder = _decoders.get(origin_type, None)
    if decoder:
        return decoder

    if dataclasses.is_dataclass(origin_type):
        return decode_dataclass

    raise JSONDecodeException.cannot_find_decoder(type=origin_type)


def decode_dataclass(value: Dict[str, Any], type_: Type[Item]) -> Item:
    errors = {}
    decoded_data = {}

    missing_fields = [field.name for field in dataclasses.fields(type_)
                      if not is_optional(field.type) and value.get(field.name,  dataclasses.MISSING) == dataclasses.MISSING]

    if missing_fields:
        raise JSONDecodeException.missing_fields_exception(type_, missing_fields)

    for field in dataclasses.fields(type_):
        try:
            decoded_data[field.name] = json_decode(value.get(field.name), field.type)
        except JSONDecodeException as e:
            errors[field.name] = e.message

    if errors:
        raise JSONDecodeException.fields_decode_exception(type_, errors)

    return type_(**decoded_data)


def decode_optional(value, type_: Type[Item]) -> Item:
    if value is None:
        return None
    type_ = type_.__args__[0]
    return json_decode(value, type_)


def decode_bool(value, type_) -> bool:
    if isinstance(value, bool):
        return value

    if isinstance(value, str) and value.lower() in ['true', 'false']:
        return value.lower() == 'true'

    if value == 0:
        return False

    if value == 1:
        return True

    raise JSONDecodeException.cannot_decode(value=value, type_name='bool')


def decode_int(value, type_) -> int:
    try:
        return type_(value)
    except (TypeError, ValueError):
        raise JSONDecodeException.cannot_decode(value=value, type_name='integer')


def decode_float(value, type_) -> float:
    try:
        return type_(value)
    except (TypeError, ValueError):
        raise JSONDecodeException.cannot_decode(value=value, type_name='float')


def decode_str(value, type_) -> str:
    if not isinstance(value, str):
        raise JSONDecodeException.cannot_decode(value=value, type_name='string')
    return type_(value)


_decoders = {
    str: decode_str,
    float: decode_float,
    int: decode_int,
    bool: decode_bool,
}
