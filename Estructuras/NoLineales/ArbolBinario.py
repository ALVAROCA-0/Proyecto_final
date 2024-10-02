from typing import Iterable, Generic, TypeVar, overload, Iterator
from ..Lineales import Queue

T = TypeVar("T")

class Nodo(Generic[T]):
    def __init__(self, valor):
        self.valor: T = valor 
        self.izquierda: Nodo[T] | None = None
        self.derecha: Nodo[T] | None = None
        self.nivel: int = 0
class ArbolBinario(Generic[T]):
    @overload
    def __init__(self, valores: Iterator[T]):...
    @overload
    def __init__(self, valores: Iterable[T]):...
    @overload
    def __init__(self, raiz: Nodo[T]):...
    def __init__(self, lista_valores: Iterable[T] | Nodo):
        if isinstance(lista_valores, Nodo):
            self._raiz = lista_valores
            return
        elif isinstance(lista_valores, Iterable):
            lista_valores = iter(lista_valores)
        if isinstance(lista_valores, Iterator):
            self._raiz: Nodo[T] = Nodo(next(lista_valores))
            cola: Queue[Nodo[T]] = Queue()
            cola.enqueue(self._raiz)

            for valor in lista_valores:
                nodo_actual = cola.dequeue()
                nodo_actual.izquierda = Nodo(valor)
                cola.enqueue(nodo_actual.izquierda)
                try:
                    siguiente = next(lista_valores)
                    nodo_actual.derecha = Nodo(siguiente)
                    cola.enqueue(nodo_actual.derecha)
                except:
                    break
        else:
            raise TypeError("Se debe recibir o un nodo, un iterable o un iterador")
    
    def get_root(self):
        return self._raiz.valor

    def set_root(self, valor: T):
        self._raiz.valor = valor
    
    def izquierda(self):
        return ArbolBinario(self._raiz.izquierda)
    def derecha(self):
        return ArbolBinario(self._raiz.derecha)