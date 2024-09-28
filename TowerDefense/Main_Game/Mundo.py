import pygame as py

class World():
    def __init__(self, imagen_mapa):
        self.image = imagen_mapa

    def draw(self, surface):
        surface.blit(self.image, (0,0))        