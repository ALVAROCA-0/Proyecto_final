import pygame as py

class Boton():
    def __init__(self,x,y,imagen):
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    
    def draw(self,surface):
        accion = False
        posicion = py.mouse.get_pos()
        
        if self.rect.collidepoint(posicion):
            if py.mouse.get_pressed()[0] == 1 and self.clicked == False:
                accion = True
                self.clicked = True
        if py.mouse.get_pressed()[0] == 0:
            self.clicked = False
        surface.blit(self.image,self.rect)
        return accion