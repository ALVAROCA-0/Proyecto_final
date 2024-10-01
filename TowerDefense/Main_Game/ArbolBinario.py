from typing import Optional
class Nodo:
    def __init__(self, valor):
        self.valor = valor 
        self.izquierda: Optional['Nodo'] = None
        self.derecha: Optional['Nodo'] = None
        self.nivel = 0

class Queue:
    def __init__(self):
        self.items = []
    
    def enqueue(self, value):
        self.items.append(value)
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue de una cola vacía")
        return self.items.pop(0)
    
    def is_empty(self):
        return len(self.items) == 0

def construir_arbol_binario_completo(lista_valores):
    if not lista_valores:
        return None

    raiz = Nodo(lista_valores[0])
    cola = Queue()  
    cola.enqueue(raiz)

    i = 1
    while i < len(lista_valores):
        nodo_actual = cola.dequeue()
        nodo_actual.izquierda = Nodo(lista_valores[i])
        cola.enqueue(nodo_actual.izquierda)
        i += 1
        if i < len(lista_valores):
            nodo_actual.derecha = Nodo(lista_valores[i])
            cola.enqueue(nodo_actual.derecha)
            i += 1

    return raiz
def encontrar_nodo(raiz: Nodo, valor_buscado):
    if raiz is None:
        return None
    if raiz.valor == valor_buscado:
        return raiz
    nodo_encontrado = encontrar_nodo(raiz.izquierda, valor_buscado)
    if nodo_encontrado:
        return nodo_encontrado
    return encontrar_nodo(raiz.derecha, valor_buscado)

def obtener_hijos(nodo: Nodo):
    if nodo:
        izquierda = nodo.izquierda.valor if nodo.izquierda else None
        derecha = nodo.derecha.valor if nodo.derecha else None
        return izquierda, derecha
    return None, None

def obtener_primera_imagen(spritesheet):
    ancho_imagen = spritesheet.get_height() 
    alto_imagen = spritesheet.get_height()
    primera_imagen = spritesheet.subsurface((0, 0, ancho_imagen, alto_imagen))
    return primera_imagen

def asignar_niveles_en_orden(raiz: Nodo):
    if raiz is None:
        return
    cola = Queue()
    cola.enqueue(raiz)
    
    nivel_actual = 1

    while not cola.is_empty():
        nodo_actual = cola.dequeue()
        nodo_actual.nivel = nivel_actual
        nivel_actual += 1
        if nodo_actual.izquierda:
            cola.enqueue(nodo_actual.izquierda)
        if nodo_actual.derecha:
            cola.enqueue(nodo_actual.derecha)