from ..Lineales import Array, SingleLinkedList as SLL
from collections.abc import Iterable
from .pair import *

class HashmapSeparateChaining(Iterable[KT, VT]):
    def __init__(self, buckets: int = 29) -> None:
        if buckets < 2: raise ValueError("Buckets debe ser un entero positivo")
        self.__size = 0
        self.buckets = buckets
        self.arr: Array[SLL[pair[KT,VT]]] = Array(buckets)
        for i in range(buckets):
            self.arr[i] = SLL()
    def __hash_func(self, key: KT) -> int:
        return hash(key) % self.buckets
    def insert(self, key: KT, value: VT) -> None:
        l: SLL[pair[KT,VT]] = self.arr[self.__hash_func(key)]
        inside: bool = False
        for p in l:
            if p.key == key:
                p.value = value
                inside = True
                break
        if not inside:
            l.push_back(pair(key, value))
        self.__size += 1
    def search(self, key: KT, default: VT = None) -> VT:
        l = self.arr[self.__hash_func(key)]
        for p in l:
            if p.key == key:
                return p.value
        return default
    def remove(self, key: KT) -> VT:
        l = self.arr[self.__hash_func(key)]
        for i, p in enumerate(l):
            if p.key == key:
                l.remove(i)
                return p.value
        raise KeyError("Llave no encontrada")
    def load_factor(self):
        return self.__size/self.buckets
    def rehash(self, new_buckets: int) -> None:
        past_buckets: int = self.buckets
        if new_buckets < 2: raise ValueError("Buckets debe ser un entero positivo")
        self.buckets = new_buckets
        temp: Array[SLL[pair]] = Array(new_buckets)
        for i in range(past_buckets):
            for p in self.arr[i]:
                temp[self.__hash_func(p.key)].push_back(p.value)
        self.arr = temp
    def keys(self) -> Iterator[KT]:
        for i in range(self.buckets):
            for p in self.arr[i]:
                yield p.key
        return
    def values(self) -> Iterator[VT]:
        for i in range(self.buckets):
            for p in self.arr[i]:
                yield p.value
        return
    def items(self) -> Iterator[pair[KT, VT]]:
        for i in range(self.buckets):
            for p in self.arr[i]:
                yield p
        return
    def __str__(self) -> str:
        return "{"+", ".join(map(str, self.items())) + "}"
    def __getitem__(self, key: KT) -> VT:
        return self.search(key)
    def __setitem__(self, key: KT, value: VT) -> None:
        self.insert(key, value)
    def __delitem__(self, key: KT) -> None:
        self.remove(key)
    def __iter__(self) -> Iterator[KT]:
        return self.keys()
    def __bool__(self) -> bool:
        return self.__size > 0