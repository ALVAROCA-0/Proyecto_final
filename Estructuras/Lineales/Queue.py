from collections.abc import Iterable, Iterator
from .SingleLinkedList import SingleLinkedList as SLList
from typing import TypeVar, overload

T = TypeVar("T")
class Queue(Iterable[T]):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, values: Iterator[T]) -> None: ...
    @overload
    def __init__(self, values: Iterable[T]) -> None: ...
    @overload
    def __init__(self, value1: T, *values: T) -> None: ...
    def __init__(self, itr: Iterator[T] | Iterable[T] | T | None = None, *values: T) -> None:
        self.__list: SLList[T] = SLList(itr, *values)
    def enqueue(self, value: T) -> None:
        self.__list.push_back(value)
    def dequeue(self) -> T:
        return self.__list.remove(0)
    def peek(self) -> T:
        return self.__list.get(0)
    def is_empty(self) -> bool:
        return self.__list.is_empty()
    def copy(self) -> Iterable[T]:
        return Queue(iter(self.__list))
    def __str__(self) -> str:
        return f"<objeto Queue; siguiente = {repr(self.peek()) if self else 'Empty'}>"
    def __iter__(self) -> Iterator[T]:
        return self.__iterator__(self)
    def __bool__(self) -> bool:
        return not self.is_empty()
    class __iterator__(Iterator[T]):
        def __init__(self, queue) -> None:
            self.queue: Queue[T] = queue
        def __next__(self) -> T:
            if self.queue.is_empty():
                raise StopIteration("Final alcanzado")
            return self.queue.dequeue()