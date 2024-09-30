import pygame as py
from pygame import Vector2
import math
from Enemigos_Datos import Datos_Enemigos

class Enemigo(py.sprite.Sprite):
    def __init__(self,tipo_enemigo,vertices,imagenes):
        py.sprite.Sprite.__init__(self)
        self.vertices = vertices
        self.pos = Vector2(self.vertices[0])
        self.trayectoria_vertice = 1
        self.hp = Datos_Enemigos.get(tipo_enemigo)["hp"]
        self.velocidad = Datos_Enemigos.get(tipo_enemigo)["velocidad"]
        self.dinero = Datos_Enemigos.get(tipo_enemigo)["dinero"]
        self.angulo = 0
        self.imagen_original = imagenes.get(tipo_enemigo)
        self.image = py.transform.rotate(self.imagen_original,self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    
    def update(self,mundo):
        self.movimiento(mundo)
        self.rotar()
        self.check_vida(mundo)
    
    def movimiento(self,mundo):
        #Definir el vertices de llegada
        if self.trayectoria_vertice < len(self.vertices):
            self.target = Vector2(self.vertices[self.trayectoria_vertice])
            self.camino = self.target - self.pos
        else:
            #El enemigo ha llegado al final del camino
            self.kill()
            mundo.vida_jugador -= 1
            mundo.enemigos_perdidos += 1
        
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
    
    def check_vida(self,mundo):
        if self.hp <= 0:
            mundo.dinero += self.dinero
            mundo.enemigos_asesinados += 1
            self.kill()
            