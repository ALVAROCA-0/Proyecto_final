import pygame as py
from pygame import Vector2
import math
from .Enemigos_Datos import Datos_Enemigos
from Estructuras.Lineales import SingleLinkedList as SLL

class Enemigo(py.sprite.Sprite):
    def __init__(self,tipo_enemigo,vertices: SLL[Vector2],imagenes, mundo):
        self.mundo = mundo
        py.sprite.Sprite.__init__(self)
        self.vertices = iter(vertices)
        self.desplazamiento = 0
        self.pos: Vector2 = Vector2(next(self.vertices))
        self.target: Vector2 = Vector2(next(self.vertices))
        self.direccion: Vector2 = self.target - self.pos
        self.hp = Datos_Enemigos.get(tipo_enemigo)["hp"]
        self.velocidad = Datos_Enemigos.get(tipo_enemigo)["velocidad"]
        self.dinero = Datos_Enemigos.get(tipo_enemigo)["dinero"]
        self.angulo = 0
        self.imagen_original = imagenes.get(tipo_enemigo)
        #generar overlay para mostrar daño
        imagen_mask = py.mask.from_surface(self.imagen_original)
        self.golpe_imagen_og = imagen_mask.to_surface(setcolor=(255,0,0,100), unsetcolor=(0,0,0,0))
        self.golpe_imagen = self.golpe_imagen_og
        self.rect = self.imagen_original.get_rect()
        self.rect.center = self.pos
        self.golpeado = False
        self.golpe_frames = 0
        self.past_time = py.time.get_ticks()
    
    def update(self):
        self.movimiento()
        self.rotar()
        self.past_time = py.time.get_ticks()

    def golpe(self, daño: int) -> None:
        self.golpe_frames = 5
        self.golpeado = True
        self.hp -= daño
        if self.hp <= 0:
            self.mundo.enemigos_asesinados += 1
            self.mundo.dinero += self.dinero
            self.kill()
    
    def movimiento(self):
        self.direccion = self.target - self.pos
        #Calcular distancia al objetivo   
        distancia = self.direccion.length()
        #Calcular si le falta recorrido para llegar al vertice
        if distancia > self.velocidad:
            step = self.direccion.normalize() * self.velocidad
            self.pos += step
            self.desplazamiento += step.length()
        else: #Llego al vertice
            self.desplazamiento += distancia
            self.pos = self.target
            #iterar al siguiente vertice
            self.target = Vector2(next(self.vertices, False))
            if not self.target:
                #El enemigo ha llegado al final del camino
                self.kill()
                self.mundo.vida_jugador -= 1
                self.mundo.enemigos_perdidos += 1
        self.rect.center = self.pos
    
    def rotar(self):
        #Usar direccion para calcular el angulo
        self.angulo = -self.direccion.as_polar()[1]
        #Rotar imagen y actualizar el rectangulo
        self.image = py.transform.rotate(self.imagen_original, self.angulo)
        self.golpe_imagen = py.transform.rotate(self.golpe_imagen_og, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    
    def draw(self, surface: py.Surface) -> None:
        surface.blit(self.image, self.rect)
        if self.golpeado:
            surface.blit(self.golpe_imagen, self.rect)
            if self.golpe_frames <= 0:
                self.golpeado = False
                self.golpe_frames = 0
            self.golpe_frames-=1
            