import pygame as py
import Constantes as c
class Torreta(py.sprite.Sprite):
    def __init__(self,imagen, pos_x, pos_y):
        py.sprite.Sprite.__init__(self)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.x = (self.pos_x + 0.5) * c.TAMAÑO_PIXEL
        self.y = (self.pos_y + 0.5)* c.TAMAÑO_PIXEL
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)