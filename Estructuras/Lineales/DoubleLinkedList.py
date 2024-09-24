from typing import Generic, TypeVar, overload
from collections.abc import Iterator, Iterable, Callable

T = TypeVar("T")

class DLLNode(Generic[T]):
    @overload
    def __init__(self, value: T) -> None:...
    @overload
    def __init__(self, value: T, before) -> None:...
    @overload
    def __init__(self, value: T, before, next) -> None:...
    def __init__(self, value: T, before = None, next = None) -> None:
        self.value: T = value
        self.before: DLLNode[T] = before
        self.next: DLLNode[T] = next
    def push_front(self, value: T):
        new_Node: DLLNode = DLLNode(value, self, self.next)
        if self.next: self.next.before = new_Node
        self.next = new_Node
        return new_Node
    def push_back(self, value: T):
        new_Node: DLLNode = DLLNode(value, self.before, self)
        if self.before: self.before.next = new_Node
        self.before = new_Node
        return new_Node
    def remove(self):
        self.next.before = self.before
        self.before.next = self.next

class DoubleLinkedList(Iterable[T]):
    def __init__(self, itr: Iterable[T] | Iterator[T] | T | None = None,*values: T) -> None:
        self.__head: DLLNode[T] = None
        self.__tail: DLLNode[T] = None
        self.__size: int = 0
        if values:
            self.push_back(itr)
            for val in values:
                self.push_back(val)
        else:
            if isinstance(itr, Iterable): itr = iter(itr)
            if isinstance(itr, Iterator):
                for val in itr:
                    self.push_back(val)
            elif itr != None: self.push_back(itr)
    
    def __go_to(self, index: int) -> DLLNode:
        i: int
        current_Node: DLLNode 
        i_dir: int
        go_to: Callable[[DLLNode], DLLNode]
        if index <= (self.__size-1)/2:
            i: int = 0
            i_dir = 1
            current_Node: DLLNode = self.__head
            go_to = lambda x: x.next
        else:
            i = self.__size - 1
            i_dir = -1
            current_Node = self.__tail
            go_to = lambda x: x.before
        while i != index:
            current_Node = go_to(current_Node)
            i += i_dir
        return current_Node

    def add(self, index: int, value: T) -> None:
        if index < 0: index += self.__size
        if index > self.__size: raise IndexError("Indice fuera de la lista")
        if index == 0: #O(1)
            if self.__size > 0:
                self.__head = self.__head.push_back(value)
            else:
                self.__head = DLLNode(value)
                self.__tail = self.__head
        elif index == self.__size: #O(1)
            self.__tail = self.__tail.push_front(value)
        else: #O(n) realmente O(n/2)
            if index <= (self.__size-1)/2:
                self.__go_to(index - 1).push_front(value)
            else:
                self.__go_to(index + 1).push_back(value)
        self.__size += 1
    
    def push(self, value: T) -> None:
        self.add(0, value)
    def push_back(self, value: T) -> None:
        self.add(self.__size, value)
    
    def remove(self, index: int) -> T:
        if index < 0: index += self.__size
        if index >= self.__size: raise IndexError("Indice fuera de la lista")
        rm: DLLNode = self.__go_to(index)
        rm.remove()
        self.__size -= 1
        return rm.value
    
    def get(self, index: int) -> T:
        if index < 0: index += self.__size
        if index >= self.__size: raise IndexError("Indice fuera de la lista")
        return self.__go_to(index).value

    def set(self, index: int, value: T) -> None:
        if index < 0: index += self.__size
        if index >= self.__size: raise IndexError("Indice fuera de la lista")
        self.__go_to(index).value = value
    
    def is_empty(self) -> bool:
        return self.__size == 0
    
    def copy(self) -> Iterable[T]:
        return DoubleLinkedList(self)
    
    @overload
    def __getitem__(self, key: int) -> T: ...
    @overload
    def __getitem__(self, Sequence: slice) -> Iterable[T]: ...
    def __getitem__(self, item: int | slice) -> T | Iterable[T]:
        if isinstance(item, slice):
            ret: DoubleLinkedList[T] = DoubleLinkedList()
            index, end, step = item.indices(self.__size)
            add: Callable[[T], None]
            move: Callable[[DLLNode], DLLNode]
            if step < 0:
                move = lambda x: x.before if x.before else x
            else: 
                move = lambda x: x.next if x.next else x
            current_Node: DLLNode = self.__go_to(index)
            while index*step < end*step:
                ret.push_back(current_Node.value)
                for _ in range(abs(step)):
                    current_Node = move(current_Node)
                index += step
            return ret
        elif not isinstance(item, int):
            raise TypeError("Los indices deben ser enteros")
        return self.get(item)
    def __setitem__(self, key:int, value: T) -> None:
        self.set(key, value)
    def __delitem__(self, key: int) -> None:
        self.remove(key)
    def __len__(self) -> int:
        return self.__size
    def __iter__(self) -> Iterator[T]:
        return self.__iterator(self.__head)
    def __str__(self) -> str:
        return "["+", ".join(repr(x) for x in self)+"]"
    def __bool__(self) -> bool:
        return not self.is_empty()
    
    class __iterator(Iterator[T]):
        def __init__(self, node: DLLNode, forward: bool = True) -> None:
            self.node: DLLNode = node
            self.forward: bool = forward
            self.next: Callable[[DLLNode],DLLNode] = (lambda x: x.next) if forward else (lambda x: x.before)
        def __next__(self) -> T:
            if self.node == None:
                raise StopIteration("Final alcanzado")
            val: T = self.node.value
            self.node = self.next(self.node)
            return val
        def copy(self) -> Iterator[T]:
            return DoubleLinkedList.__iterator(self.node, self.forward)