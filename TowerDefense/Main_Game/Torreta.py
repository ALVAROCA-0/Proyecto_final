from typing import Any
import pygame as py

from . import Constantes as c
from time import time

class Torreta(py.sprite.Sprite):
    def __init__(self,imagen: py.Surface, pos_x: int, pos_y: int, radio: int) -> None:
        py.sprite.Sprite.__init__(self)
        
        self.selected = False
        self.radio: int = radio #radio de disparo en pixeles
        
        self.pos = py.Vector2(pos_x,pos_y)
        
        self.imagen_original: py.Surface = imagen
        self.imagen: py.Surface = imagen
        self.rect = self.imagen.get_rect()
        self.rect.center = self.pos
        
        self.borde = py.mask.from_surface(imagen)
        self.borde = self.borde.convolve(py.mask.Mask((5,5), True))
        self.borde = self.borde.to_surface(setcolor="black",unsetcolor=(0,0,0,0))
        self.borde_original = self.borde
        self.b_rect = self.borde.get_rect()
        self.b_rect.center = self.pos
        
        self.imagen_rango: py.Surface = py.Surface((radio*2, radio*2), py.SRCALPHA)
        self.imagen_rango.fill((0,0,0,0))
        py.draw.circle(self.imagen_rango, (100,100,100, 50), (radio, radio), radio)
        self.rect_rango: py.rect.Rect = self.imagen_rango.get_rect()
        self.rect_rango.center = self.pos
        
        self.cooldown: int = 0
        self.past_time = time()
    def rotar(self, target: py.Vector2):
        #Usar direccion para calcular el angulo
        self.angulo = -(target-self.pos).as_polar()[1] -90
        #Rotar imagen y actualizar el rectangulo
        self.imagen = py.transform.rotate(self.imagen_original, self.angulo)
        self.borde = py.transform.rotate(self.borde_original, self.angulo)
        self.rect = self.imagen.get_rect()
        self.rect.center = self.pos
        self.b_rect = self.borde.get_rect()
        self.b_rect.center = self.pos
    def update(self, grupo_enemigos: py.sprite.Group) -> None:
        delta_time = time() - self.past_time
        if self.cooldown == 0:
            primero = None
            primero_desp = 0
            for enemigo in grupo_enemigos:
                if (enemigo.pos-self.pos).length() -10 < self.radio and primero_desp < enemigo.desplazamiento:
                    primero = enemigo
                    primero_desp = enemigo.desplazamiento
            if primero:
                self.rotar(primero.pos)
                primero.hp -= 10
                self.cooldown = 1000
        else:
            self.cooldown = max(0, self.cooldown - int(delta_time*1000))
        self.past_time = time()
    def draw(self, surface0: py.Surface, surface1: py.Surface):
        if self.selected:
            surface1.blit(self.borde, self.b_rect)
            surface1.blit(self.imagen, self.rect)
            surface1.blit(self.imagen_rango, self.rect_rango)
        else:
            surface0.blit(self.imagen, self.rect)