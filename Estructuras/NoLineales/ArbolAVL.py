class Nodo:
    def __init__(self,valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.altura = 1

class ArbolBinarioAVL:
    def __init__(self):
        self.raiz = None
    
    def insertar(self,valor):
        self.raiz = self.insertar_diferente(self.raiz,valor)
    
    def insertar_diferente(self, nodo, valor):
        if nodo is None:
            return Nodo(valor)
        
        if valor < nodo.valor:
            nodo.izquierdo = self.insertar_diferente(nodo.izquierdo, valor)
        else:
            nodo.derecho = self.insertar_diferente(nodo.derecho, valor)
        
        nodo.altura = 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))
        
        return self.balancear(nodo)
    
    def _altura(self, nodo):
        return nodo.altura if nodo else 0
    
    def equilibrio(self, nodo):
        return self._altura(nodo.izquierdo) - self._altura(nodo.derecho) if nodo else 0
    
    def rotar_derecha(self, y):
        x = y.izquierdo
        y.izquierdo = x.derecho
        x.derecho = y
        y.altura = 1 + max(self._altura(y.izquierdo), self._altura(y.derecho))
        x.altura = 1 + max(self._altura(x.izquierdo), self._altura(x.derecho))
        return x
    
    def rotar_izquierda(self, x):
        y = x.derecho
        x.derecho = y.izquierdo
        y.izquierdo = x
        x.altura = 1 + max(self._altura(x.izquierdo), self._altura(x.derecho))
        y.altura = 1 + max(self._altura(y.izquierdo), self._altura(y.derecho))
        return y
    
    def balancear(self, nodo):
        factor = self.equilibrio(nodo)
        
        if factor > 1 and self.equilibrio(nodo.izquierdo) >= 0:
            return self.rotar_derecha(nodo)
        
        if factor < -1 and self.equilibrio(nodo.derecho) <= 0:
            return self.rotar_izquierda(nodo)
        
        if factor > 1 and self.equilibrio(nodo.izquierdo) < 0:
            nodo.izquierdo = self.rotar_izquierda(nodo.izquierdo)
            return self.rotar_derecha(nodo)
        
        if factor < -1 and self.equilibrio(nodo.derecho) > 0:
            nodo.derecho = self.rotar_derecha(nodo.derecho)
            return self.rotar_izquierda(nodo)
        
        return nodo
                
    def preorder(self):
        return self.preorder_recorrido(self.raiz)

    def preorder_recorrido(self, nodo):
        elementos = []
        if nodo:
            elementos.append(nodo.valor)  
            elementos.extend(self.preorder_recorrido(nodo.izquierdo)) 
            elementos.extend(self.preorder_recorrido(nodo.derecho))  
        return elementos
