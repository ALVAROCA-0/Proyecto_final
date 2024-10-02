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
    # def encontrar_nodo(self, valor_buscado: T) -> T | None:
    #     if self.raiz is None:
    #         return None
    #     cola: Queue[Nodo[T]] = Queue(self.raiz)
    #     while cola:
    #         if 
        # if self.raiz.valor == valor_buscado:
        #     return self.raiz
        # nodo_encontrado = encontrar_nodo(self.raiz.izquierda, valor_buscado)
        # if nodo_encontrado:
        #     return nodo_encontrado
        # return encontrar_nodo(self.raiz.derecha, valor_buscado)

    # def obtener_hijos(nodo: Nodo):
    #     if nodo:
    #         izquierda = nodo.izquierda.valor if nodo.izquierda else None
    #         derecha = nodo.derecha.valor if nodo.derecha else None
    #         return izquierda, derecha
    #     return None, None

    # def obtener_primera_imagen(spritesheet):
    #     ancho_imagen = spritesheet.get_height() 
    #     alto_imagen = spritesheet.get_height()
    #     primera_imagen = spritesheet.subsurface((0, 0, ancho_imagen, alto_imagen))
    #     return primera_imagen

    # def asignar_niveles_en_orden(raiz: Nodo):
    #     if raiz is None:
    #         return
    #     cola = Queue()
    #     cola.enqueue(raiz)
        
    #     nivel_actual = 1

    #     while not cola.is_empty():
    #         nodo_actual = cola.dequeue()
    #         nodo_actual.nivel = nivel_actual
    #         nivel_actual += 1
    #         if nodo_actual.izquierda:
    #             cola.enqueue(nodo_actual.izquierda)
    #         if nodo_actual.derecha:
    #             cola.enqueue(nodo_actual.derecha)