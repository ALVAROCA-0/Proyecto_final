import pygame as py
from pygame import Vector2
import math
class Enemigo(py.sprite.Sprite):
    def __init__(self,vertices,imagen):
        py.sprite.Sprite.__init__(self)
        self.vertices = vertices
        self.pos = Vector2(self.vertices[0])
        self.trayectoria_vertice = 1
        self.velocidad = 2
        self.angulo = 0
        self.imagen_original = imagen
        self.image = py.transform.rotate(self.imagen_original,self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    
    def update(self):
        self.movimiento()
        self.rotar()
    
    def movimiento(self):
        #Definir el vertices de llegada
        if self.trayectoria_vertice < len(self.vertices):
            self.target = Vector2(self.vertices[self.trayectoria_vertice])
            self.camino = self.target - self.pos
        else:
            #El enemigo ha llegado al final del camino
            self.kill()
        
        #Calcular distancia al objetivo   
        distancia = self.camino.length()
        #Calcular si la distancia es mayor que la velocidad
        if distancia >= self.velocidad:
            self.pos += self.camino.normalize() * self.velocidad
        else:
            if distancia != 0:
                self.pos += self.camino.normalize() * distancia
            self.trayectoria_vertice += 1
        self.rect.center = self.pos
    
    def rotar(self):
        #Calcular la distancia al siguiente vertice
        distancia = self.target - self.pos
        #Usar la distancia para calcular el angulo
        self.angulo = math.degrees(math.atan2(-distancia[1],distancia[0]))
        #Rotar imagen y actualizar el rectangulo
        self.image = py.transform.rotate(self.imagen_original,self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos