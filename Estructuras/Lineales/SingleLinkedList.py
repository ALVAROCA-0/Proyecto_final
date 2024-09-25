from typing import Generic, TypeVar, overload
from collections.abc import Iterator, Iterable

T = TypeVar("T")

class SLLNode(Generic[T]):
    def __init__(self, value: T, next = None):
        self.value: T = value
        self.next: SLLNode[T]|None = next

class SingleLinkedList(Iterable[T]):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, values: Iterator[T]) -> None: ...
    @overload
    def __init__(self, values: Iterable[T]) -> None: ...
    @overload
    def __init__(self, value1: T, value2: T, *values: T) -> None: ...
    def __init__(self, itr: Iterator[T] | Iterable[T] | T | None = None, *values: T) -> None:
        self.__size: int = 0
        self.__head: SLLNode[T] = None
        self.__tail: SLLNode[T] = None
        if values:
            #asume itr es un valor tipo T y el primer valor
            self.push_back(itr)
            for val in values:
                self.push_back(val)
        else:
            if isinstance(itr, Iterable): #convertir a iterator
                itr = iter(itr)
            if isinstance(itr, Iterator):
                for val in itr:
                    self.push_back(val)
            elif itr != None:
                #si no es iterador añadirlo como primer valor
                self.push_back(itr)

    def add(self, index: int, value: T) -> None:
        if index < 0 or index > self.__size:
            raise IndexError("Indice fuera de la lista")
        if index == 0:
            self.__head = SLLNode(value, self.__head)
            if self.__size == 0:
                self.__tail = self.__head
        elif index == self.__size:
            self.__tail.next = SLLNode(value)
            self.__tail = self.__tail.next
        else:
            i: int = 0
            current_Node: SLLNode[T] = self.__head
            while i < index - 1:
                current_Node = current_Node.next
                i += 1
            current_Node.next = SLLNode(value, current_Node.next)
        self.__size += 1

    def push(self, value: T):
        self.add(0, value)

    def push_back(self, value: T):
        self.add(self.__size, value)

    def remove(self, index: int) -> T:
        if index < 0 or index >= self.__size:
            raise IndexError("Indice fuera de la lista")
        ret: T
        if index == 0:
            ret = self.__head.value
            self.__head = self.__head.next
        else:
            i: int = 0
            current_Node: SLLNode[T] = self.__head
            while i < index - 1:
                current_Node = current_Node.next
                i += 1
            if index == self.__size-1:
                self.__tail = current_Node
            ret = current_Node.next.value
            current_Node.next = current_Node.next.next
        self.__size -= 1
        return ret

    def get(self, index: int) -> T:
        if index < 0 or index >= self.__size:
            raise IndexError("Indice fuera de la lista")
        if index == self.__size-1: return self.__tail.value
        i: int = 0
        current_Node: SLLNode[T] = self.__head
        while i < index:
            current_Node = current_Node.next
            i += 1
        return current_Node.value

    def set(self, index: int, value: T) -> None:
        if index < 0: index += self.__size
        if index >= self.__size:
            raise IndexError("Indice fuera de la lista")
        if index == self.__size-1: 
            self.__tail.value = value
        else:
            i: int = 0
            current_Node: SLLNode[T] = self.__head
            while i < index:
                current_Node = current_Node.next
                i += 1
            current_Node.value = value
    
    def is_empty(self):
        return self.__size == 0
    
    def copy(self):
        return SingleLinkedList(self)
    #operator overloads----------------------------------------------
    @overload
    def __getitem__(self, key: int) -> T: ...
    @overload
    def __getitem__(self, Sequence: slice) -> Iterable[T]: ...
    def __getitem__(self, item: int | slice) -> T | Iterable[T]:
        if isinstance(item, slice):
            ret: SingleLinkedList[T] = SingleLinkedList()
            index, end, step = item.indices(self.__size)
            add = ret.push_back
            #cambiar direccion ya que solo puede ir hacia adelante
            if step < 0:
                step *= -1
                temp = end + 1
                end = index +1
                index = temp
                #añadir elementos al inicio en vez del final
                add = ret.push
            itr: Iterable[T] = iter(self)
            #mover el iterador a index
            i: int = 0
            while i < index:
                next(itr)
                i += 1
            while index < end:
                add(next(itr))
                i = 1
                #mover el iterador 'step' posiciones
                while i < step: next(itr)
                index += step
            return ret
        elif not isinstance(item, int):
            raise TypeError("Los indices deben ser enteros")
        return self.get(item)
    def __setitem__(self, key, value):
        return self.set(key, value)
    def __len__(self):
        return self.__size
    def __iter__(self) -> Iterator[T]:
        return self.__iterator(self.__head)
    def __str__(self):
        return "["+", ".join(repr(x) for x in self)+"]"
    def __delitem__(self, key: int):
        self.remove(key)
    def __bool__(self) -> bool:
        return not self.is_empty()
    class __iterator(Iterator[T]):
        def __init__(self, node: SLLNode) -> None:
            self.__node: SLLNode[T] = node
        def __next__(self) -> T:
            if self.__node == None:
                raise StopIteration("Final alcanzado")
            ret: T =  self.__node.value
            self.__node = self.__node.next
            return ret
        def set(self, value: T) -> None:
            self.__node.value = value
        def get(self) -> T:
            return self.__node.value
        def copy(self) -> Iterator[T]:
            return SingleLinkedList.__iterator(self.__node)
