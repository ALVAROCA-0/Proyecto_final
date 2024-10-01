import pygame as py

class Boton():
    def __init__(self,x,y,imagen):
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    
    def on_click(self, evento: py.event.Event, mouse_pos: tuple[int,int]) -> bool:
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
    def draw(self, surface: py.Surface):
        surface.blit(self.image, self.rect)