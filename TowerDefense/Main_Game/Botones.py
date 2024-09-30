import pygame as py
from math import sqrt

class Boton():
    def __init__(self,x: int,y: int, imagen: py.Surface, offy):
        self.step_frames: int = 30 #frames que tienen que pasar para completar la animacion
        self.pos: py.Vector2 = py.Vector2(x, y)
        self.base_offy = offy
        self.offy_step = 0
        self.image: py.Surface = imagen
        self.rect: py.Rect = self.image.get_rect()
        self.max_offy = self.rect.height - offy
        self.rect.center = (x,y + offy)
        self.clicked: bool = False

    def update(self, mouse_pos: tuple[int,int]) -> None:
        if self.rect.collidepoint(mouse_pos):
            if self.offy_step < self.step_frames:
                self.offy_step = min(self.step_frames, self.offy_step + 1)
                self.rect.centery = self.pos.y + self.base_offy + self.max_offy*sqrt(self.offy_step/self.step_frames)
        else:
            if self.offy_step > 0:
                # se recoge el doble de rapido
                self.offy_step = max(0, self.offy_step - 2)
                self.rect.centery = self.pos.y + self.base_offy + self.max_offy*sqrt(self.offy_step/self.step_frames)
    
    def on_click(self, evento: py.event.Event, mouse_pos: tuple[int,int]) -> bool:
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
    def draw(self, surface: py.Surface):
        surface.blit(self.image, self.rect)