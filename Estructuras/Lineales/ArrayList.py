#va a molestar pero realmente no es un problema
from Array.Array import Array

from typing import TypeVar, overload
from collections.abc import Iterator, Iterable

T = TypeVar("T")

class ArrayList(Iterable[T]):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, values: Iterator[T]) -> None: ...
    @overload
    def __init__(self, values: Iterable[T]) -> None: ...
    @overload
    def __init__(self, value1: T, *values: T) -> None: ...
    def __init__(self, itr: Iterator[T] | Iterable[T] | T |  None = None, *values: T) -> None:
        self.__arr__: Array = Array(2)
        self.__size__ = 0
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
            
    def add(self, index: int, value: T):
        if not isinstance(index, int):
            raise TypeError("Los indices deben ser enteros")
        if index < 0: index = self.__size__ + index
        if 0 > index or index > self.__size__:
            raise IndexError("Indice fuera de la lista")
        if len(self.__arr__) <= self.__size__: #extender array
            temp: Array = Array(2*len(self.__arr__))
            i:int = 0
            #copia todos los valores menores a index
            while i < index:
                temp[i] = self.__arr__[i]
                i += 1
            #copia valores una posicion adelante para dar espacio en index
            while i < self.__size__:
                temp[i+1] = self.__arr__[i]
                i += 1
            del self.__arr__
            self.__arr__ = temp
        else:
            #mueve valores mayores a index una posicion adelante para dar espacio en index
            i: int = self.__size__
            while i > index:
                self.__arr__[i] = self.__arr__[i-1]
                i -= 1
        self.__arr__[index] = value
        self.__size__ += 1
    
    def push(self, value: T):
        self.add(0, value)
    def push_back(self, value: T):
        self.add(self.__size__, value)
    
    def remove(self, index) -> T:
        if not isinstance(index, int):
            raise TypeError("Los indices deben ser enteros")
        if index < 0: index = self.__size__ + index
        if 0 > index or index >= self.__size__:
            raise IndexError("Indice fuera de la lista")
        
        ret: T = self.__arr__[index]
        #mueve valores una posicion atras desde index para quitar valor en index
        i:int = index
        while i < self.__size__:
            self.__arr__[i] = self.__arr__[i+1]
        self.__size__ -= 1
        return ret
    
    def get(self, index: int) -> T:
        if not isinstance(index, int):
            raise TypeError("Los indices deben ser enteros")
        if index < 0: index = self.__size__ + index
        if 0 > index or index >= self.__size__:
            raise IndexError("Indice fuera de la lista")
        return self.__arr__[index]
    
    def set(self, index: int, value: T) -> None:
        if not isinstance(index, int):
            raise TypeError("Los indices deben ser enteros")
        if index < 0: index = self.__size__ + index
        if 0 > index or index >= self.__size__:
            raise IndexError("Indice fuera de la lista")
        self.__arr__[index] = value
    
    def copy(self) -> Iterable[T]:
        return ArrayList(self)
    
    @overload
    def __getitem__(self, key: int) -> T:...
    @overload
    def __getitem__(self, slice: slice) -> Iterable[T]:...
    def __getitem__(self, key: int|slice) -> T | Iterable[T]:
        if isinstance(key, int):
            return self.get(key)
        elif isinstance(key, slice):
            start, end, step = key.indices(self.__size__)
            ret: ArrayList = ArrayList(self.get(index) for index in range(start, end, step))
            return ret
        else:
            raise TypeError("Key debe ser un entero o un objeto tipo slice")
    def __setitem__(self, key: int, value: T) -> None:
        self.set(key, value)
    def __delitem__(self, key: int) -> None:
        self.remove(key)
    def __str__(self):
        return "("+", ".join(repr(x) for x in self)+")"
    def __iter__(self) -> Iterator[T]:
        return self.__iterator__(self.__arr__, self.__size__)
    class __iterator__(Iterator[T]):
        def __init__(self, arr: Array, size: int, start:int = 0) -> None:
            self.arr:Array = arr
            self.index: int = start
            self.size: int = size
        def __next__(self) -> T:
            if self.index >= self.size:
                raise StopIteration("Final alcanzado")
            ret:T = self.arr[self.index]
            self.index += 1
            return ret
        def copy(self) -> Iterator[T]:
            return ArrayList.__iterator__(self.arr, self.size, self.index)

    