import pygame as py
import Constantes as c
import math
from Niveles_Torretas import Nivel
import ArbolBinario as AB
class Torreta(py.sprite.Sprite):
    def __init__(self,sprite_sheets,nodo,arbol, pos_x, pos_y):
        py.sprite.Sprite.__init__(self)
        self.arbol = arbol
        self.nodo = AB.encontrar_nodo(self.arbol,nodo)
        self.nivel = self.nodo.nivel
        self.rango = Nivel[self.nivel].get("rango")
        self.cooldown = Nivel[self.nivel].get("cooldown")
        self.daño = Nivel[self.nivel].get("daño")
        self.ultimo_tiro = py.time.get_ticks()
        self.selected = False
        self.objetivo = None
        
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.x = (self.pos_x + 0.5) * c.TAMAÑO_PIXEL
        self.y = (self.pos_y + 0.5)* c.TAMAÑO_PIXEL
        
        self.sprite_sheets = sprite_sheets
        self.lista_animacion = self.cargar_imagenes(self.sprite_sheets[self.nivel-1])
        self.frame_index = 0
        self.update_time = py.time.get_ticks()
        
        self.angulo = 90
        self.imagen_original = self.lista_animacion[self.frame_index]
        self.image = py.transform.rotate(self.imagen_original,self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        
        self.rango_imagen = py.Surface((self.rango*2, self.rango*2))
        self.rango_imagen.fill((0,0,0))
        self.rango_imagen.set_colorkey((0,0,0))
        py.draw.circle(self.rango_imagen,"grey100",(self.rango,self.rango),self.rango)
        self.rango_imagen.set_alpha(100)
        self.rango_rect = self.rango_imagen.get_rect()
        self.rango_rect.center = self.rect.center
        
    def cargar_imagenes(self,sprite_sheet):
        tamaño = sprite_sheet.get_height()
        animacion = sprite_sheet.get_width() // tamaño
        lista_animacion = []
        for x in range(animacion):
            imagen_temporal = sprite_sheet.subsurface(x*tamaño,0,tamaño,tamaño)
            lista_animacion.append(imagen_temporal)
        return lista_animacion
    
    def update(self,grupo_enemigos):
        if self.objetivo:
            self.empezar_animacion()
        else:
            if py.time.get_ticks() - self.ultimo_tiro > self.cooldown:
                self.apuntar(grupo_enemigos)
    def apuntar(self, grupo_enemigos):
        dist_x = 0
        dist_y = 0
        for enemigo in grupo_enemigos:
            if enemigo.hp > 0:
                dist_x = enemigo.pos[0] - self.x
                dist_y = enemigo.pos[1] - self.y
                dist = math.sqrt(dist_x**2 + dist_y**2)
                if dist < self.rango:
                    self.objetivo = enemigo
                    self.angulo = math.degrees(math.atan2(-dist_y,dist_x))
                    self.objetivo.hp -= self.daño
                    break
    def empezar_animacion(self):
        self.imagen_original = self.lista_animacion[self.frame_index]
        if py.time.get_ticks() - self.update_time > c.DELAY_ANIMACION:
            self.update_time = py.time.get_ticks()
            self.frame_index += 1 
            if self.frame_index >= len(self.lista_animacion):
                self.frame_index = 0
                self.ultimo_tiro = py.time.get_ticks()
                self.objetivo = None
    
    def subir_nivel(self,nodo,hijo):
        self.nivel = hijo.nivel
        self.nodo = nodo
        self.daño = Nivel[self.nivel].get("daño")
        self.rango = Nivel[self.nivel].get("rango")
        self.cooldown = Nivel[self.nivel].get("cooldown")
        self.lista_animacion = self.cargar_imagenes(hijo.valor)
        self.imagen_original = self.lista_animacion[self.frame_index]
        
        self.rango_imagen = py.Surface((self.rango*2, self.rango*2))
        self.rango_imagen.fill((0,0,0))
        self.rango_imagen.set_colorkey((0,0,0))
        py.draw.circle(self.rango_imagen,"grey100",(self.rango,self.rango),self.rango)
        self.rango_imagen.set_alpha(100)
        self.rango_rect = self.rango_imagen.get_rect()
        self.rango_rect.center = self.rect.center
    
    def draw(self,superficie):
        self.image = py.transform.rotate(self.imagen_original,self.angulo - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        superficie.blit(self.image,self.rect)
        if self.selected:
            superficie.blit(self.rango_imagen,self.rango_rect)
            self.selected = False