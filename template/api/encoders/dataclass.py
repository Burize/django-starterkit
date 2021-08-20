import dataclasses
from collections import Iterable
from typing import List
from typing import TypeVar
from typing import Union

ValueToDecode = TypeVar('Item')

DecodedDataclass = Union[tuple, dict]


def encode_dataclass(value: ValueToDecode) -> Union[ValueToDecode, DecodedDataclass, List[DecodedDataclass]]:
    if dataclasses.is_dataclass(value):
        return dataclasses.asdict(value)

    if isinstance(value, Iterable):
        return [encode_dataclass(item) for item in value]

    return value