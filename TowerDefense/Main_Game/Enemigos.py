import pygame as py
from pygame import Vector2
import math
from Estructuras.Lineales import Queue, SingleLinkedList as SLL
from time import time

class Enemigo(py.sprite.Sprite):
    def __init__(self,vertices: SLL,imagen: py.Surface):
        py.sprite.Sprite.__init__(self)
        self.pos: Vector2 = Vector2(self.vertices.dequeue())
        #atributos para moverse
        self.vertices: Queue[tuple[int, int]] = Queue(vertices)
        self.target: Vector2 = Vector2(self.vertices.dequeue())
        self.direccion: Vector2 = self.target - self.pos
        self.velocidad: int = 100 #pixeles por segundo
        self.angulo = 0
        self.imagen_original = imagen
        self.image = py.transform.rotate(self.imagen_original,self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.past_time = time()
    def update(self):
        self.movimiento()
        self.rotar()
    
    def movimiento(self) -> None:
        #importante para fluctuaciones en fps
        delta_time = time() - self.past_time
        #Direccion al vertice
        self.direccion = self.target - self.pos
        
        #Calcular distancia al vertice
        distancia = self.direccion.length()
        #Calcular si le falta recorrido para llegar al vertice
        if distancia >= self.velocidad * delta_time:
            self.pos += self.direccion.normalize() * self.velocidad * delta_time
        else: #Llego al vertice
            self.pos = self.target
            if self.vertices:
                #Ir al siguiente vertice
                self.target = Vector2(self.vertices.dequeue())
                # print(self.target)
            else:
                #El enemigo ha llegado al final del camino
                self.kill()
        self.rect.center = self.pos
        self.past_time = time()
    
    def rotar(self):
        #Usar direccion para calcular el angulo
        self.angulo = math.degrees(math.atan2(self.direccion[1], -self.direccion[0]))
        #Rotar imagen y actualizar el rectangulo
        self.image = py.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos