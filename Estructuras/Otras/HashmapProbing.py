from .pair import *
from collections.abc import Iterable
from ..Lineales import Array

class HashmapProbing(Iterable[KT]):
    def __init__(self, buckets: int = 29, quadratic: bool = False) -> None:
        self.buckets = buckets
        self.__size = 0
        self.arr: Array[pair[KT,VT]] = Array(buckets)
        self.quadratic = quadratic
    
    def __hash_func(self, key: KT, intentos: int = 0) -> int:
        return (hash(key)+intentos*(intentos if self.quadratic else 1)) % self.buckets
    
    def insert(self, key: KT, value: VT) -> None:
        i: int = 0
        pos:int = self.__hash_func(key)
        val: None|pair[KT,VT] = self.arr[pos]
        while not (val == None or val.key == key):
            i += 1
            pos = self.__hash_func(key, i)
            val = self.arr[pos]
            if i >= self.buckets: raise MemoryError(f"No se ha encontrado espacio de {i} intentos")
        if val != None:
            val.value = value
        else:
            self.arr[pos] = pair(key, value)
        self.__size += 1
    def search(self, key: KT, default: VT = None) -> VT:
        i: int = 0
        pos:int = self.__hash_func(key)
        val: None|pair[KT,VT] = self.arr[pos]
        while val == None or val.key != key:
            i += 1
            pos = self.__hash_func(key, i)
            val = self.arr[pos]
            if i >= self.buckets: break
        if val.key == key: return val.value
        return default
    def remove(self, key: KT) -> VT:
        i: int = 0
        pos:int = self.__hash_func(key)
        val: None|pair[KT,VT] = self.arr[pos]
        while val == None or val.key != key:
            i += 1
            pos = self.__hash_func(key, i)
            val = self.arr[pos]
            if i >= self.buckets: raise KeyError(f"No se ha encontrado la llave despues de {i} intentos")
        ret: VT = val.value
        self.arr[pos] = None
        self.__size -= 1
        return ret
    def load_factor(self) -> int:
        return self.__size/self.buckets
    def rehash(self, new_buckets: int) -> None:
        if new_buckets < 2: raise ValueError("Buckets debe ser un entero positivo")
        past_buckets: int = self.buckets
        self.buckets = new_buckets
        temp: Array[pair[KT, VT]] = self.arr
        self.arr = Array(new_buckets)
        for i in range(past_buckets):
            value: None|pair[KT,VT] = temp[i]
            if value != None:
                self.insert(*value)
        self.arr
    def keys(self) -> Iterator[KT]:
        for i in range(self.buckets):
            if self.arr[i] != None:
                yield self.arr[i].key
        return
    def values(self) -> Iterator[VT]:
        for i in range(self.buckets):
            if self.arr[i] != None:
                yield self.arr[i].value
        return
    def items(self) -> Iterator[pair[KT,VT]]:
        for i in range(self.buckets):
            if self.arr[i] != None:
                yield self.arr[i]
        return
    def __str__(self) -> str:
        return "{"+", ".join(self.items()) + "}"
    def __getitem__(self, key: KT) -> VT:
        return self.search(key)
    def __setitem__(self, key: KT, value: VT) -> None:
        self.insert(key, value)
    def __delitem__(self, key: KT) -> None:
        self.remove(key)
    def __iter__(self) -> Iterator[KT]:
        return self.keys()