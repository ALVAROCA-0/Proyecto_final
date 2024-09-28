import pygame as py
from . import Constantes as c
class Torreta(py.sprite.Sprite):
    def __init__(self,imagen: py.Surface, pos_x: int, pos_y: int) -> None:
        py.sprite.Sprite.__init__(self)
        self.x = pos_x
        self.y = pos_y
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.center = py.Vector2(self.x,self.y)