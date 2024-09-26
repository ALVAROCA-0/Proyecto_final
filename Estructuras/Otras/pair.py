from typing import TypeVar, Generic
from collections.abc import Iterator

KT = TypeVar("KT")
VT = TypeVar("VT")

class pair(Generic[KT, VT]):
    def __init__(self, key: KT, value: VT) -> None:
        self.key: KT = key
        self.value: VT = value
    def __str__(self) -> str:
        return f"{self.key!r}:{self.value!r}"
    def __iter__(self) -> Iterator[KT|VT]:
        yield self.key
        yield self.value
        return