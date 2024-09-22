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
    def __init__(self, value1: T, *values: T) -> None: ...
    def __init__(self, itr: Iterator[T] | Iterable[T] | T | None = None, *values: T) -> None:
        self.__size__: int = 0
        self.__head__: SLLNode[T] = None
        self.__tail__: SLLNode[T] = None
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
        if index < 0 or index > self.__size__:
            raise IndexError("Indice fuera de la lista")
        if index == 0:
            self.__head__ = SLLNode(value, self.__head__)
            if self.__size__ == 0:
                self.__tail__ = self.__head__
        elif index == self.__size__:
            self.__tail__.next = SLLNode(value)
            self.__tail__ = self.__tail__.next
        else:
            i: int = 0
            current_Node: SLLNode[T] = self.__head__
            while i < index - 1:
                current_Node = current_Node.next
                i += 1
            current_Node.next = SLLNode(value, current_Node.next)
        self.__size__ += 1

    def push(self, value: T):
        self.add(0, value)

    def push_back(self, value: T):
        self.add(self.__size__, value)

    def remove(self, index: int) -> T:
        if index < 0 or index >= self.__size__:
            raise IndexError("Indice fuera de la lista")
        ret: T
        if index == 0:
            ret = self.__head__.value
            self.__head__ = self.__head__.next
        else:
            i: int = 0
            current_Node: SLLNode[T] = self.__head__
            while i < index - 1:
                current_Node = current_Node.next
                i += 1
            if index == self.__size__-1:
                self.__tail__ = current_Node
            ret = current_Node.next.value
            current_Node.next = current_Node.next.next
        return ret

    def get(self, index: int) -> T:
        if index < 0 or index >= self.__size__:
            raise IndexError("Indice fuera de la lista")
        if index == self.__size__-1: return self.__tail__.value
        i: int = 0
        current_Node: SLLNode[T] = self.__head__
        while i < index:
            current_Node = current_Node.next
            i += 1
        return current_Node.value

    def set(self, index: int, value: T) -> None:
        if index < 0: index += self.__size__
        if index >= self.__size__:
            raise IndexError("Indice fuera de la lista")
        if index == self.__size__-1: 
            self.__tail__.value = value
        else:
            i: int = 0
            current_Node: SLLNode[T] = self.__head__
            while i < index:
                current_Node = current_Node.next
                i += 1
            current_Node.value = value
    
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
            index, end, step = item.indices(self.__size__)
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
        return self.__size__
    def __iter__(self) -> Iterator[T]:
        return self.__iterator__(self.__head__)
    def __str__(self):
        return "["+", ".join(repr(x) for x in self)+"]"
    def __deliter__(self, key: int):
        self.remove(key)
    class __iterator__(Iterator[T]):
        def __init__(self, node: SLLNode) -> None:
            self.__node__: SLLNode[T] = node
        def __next__(self) -> T:
            if self.__node__ == None:
                raise StopIteration("Final alcanzado")
            ret: T =  self.__node__.value
            self.__node__ = self.__node__.next
            return ret
        def copy(self) -> Iterator[T]:
            return SingleLinkedList.__iterator__(self.__node__)
