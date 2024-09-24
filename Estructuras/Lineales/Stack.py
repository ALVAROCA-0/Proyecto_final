from collections.abc import Iterable, Iterator
from SingleLinkedList import SingleLinkedList as SLList
from typing import TypeVar, overload

T = TypeVar("T")
class Stack(Iterable[T]):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, values: Iterator[T]) -> None: ...
    @overload
    def __init__(self, values: Iterable[T]) -> None: ...
    @overload
    def __init__(self, value1: T, value2: T, *values: T) -> None: ...
    def __init__(self, itr: Iterator[T] | Iterable[T] | T | None = None, *values: T) -> None:
        self.__list: SLList[T] = SLList()
        if values:
            self.__list.push(itr)
            for val in values:
                self.__list.push(val)
        else:
            if isinstance(itr, Iterable): itr = iter(itr)
            if isinstance(itr, Iterator):
                for val in itr:
                    self.__list.push(val)
            else:
                self.__list.push(val)
    def push(self, value: T) -> None:
        self.__list.push(value)
    def pop(self) -> T:
        return self.__list.remove(0)
    def peek(self) -> T:
        return self.__list.get(0)
    def is_empty(self) -> bool:
        return self.__list.is_empty()
    def copy(self) -> Iterable[T]:
        return Stack(self.__list[::-1])
    def __str__(self) -> str:
        return f"<objeto Stack; siguiente = {repr(self.peek()) if self else 'Empty'}>"
    def __iter__(self) -> Iterator[T]:
        return self.__iterator__(self)
    def __bool__(self) -> bool:
        return not self.is_empty()
    class __iterator__(Iterator[T]):
        def __init__(self, stack) -> None:
            self.stack: Stack[T] = stack
        def __next__(self) -> T:
            if self.stack.is_empty():
                raise StopIteration("Final alcanzado")
            return self.stack.pop()