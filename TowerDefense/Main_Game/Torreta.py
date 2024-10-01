import pygame as py
from . import Constantes as c
from .Niveles_Torretas import Nivel
import Estructuras.NoLineales import ArbolBinario as AB
class Torreta(py.sprite.Sprite):
    def __init__(self,sprite_sheets,nodo, arbol, pos_x, pos_y):
        py.sprite.Sprite.__init__(self)
        self.arbol = arbol
        self.nodo = AB.encontrar_nodo(self.arbol,nodo)
        self.nivel = self.nodo.nivel
        self.rango = Nivel[self.nivel].get("rango")
        self.cooldown = Nivel[self.nivel].get("cooldown")
        self.daño = Nivel[self.nivel].get("daño")
        self.ultimo_tiro = py.time.get_ticks()
        self.seleccionado = False
        self.objetivo = None
        
        self.x = pos_x
        self.y = pos_y
        
        self.sprite_sheets = sprite_sheets
        self.lista_animacion = self.cargar_imagenes(self.sprite_sheets[self.nivel-1])
        self.frame_index = 0
        self.update_time = py.time.get_ticks()
        
        self.angulo = 0
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
        lista_animacion = []
        for x in range(c.ANIMACION_TORRETAS):
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
        for enemigo in grupo_enemigos:
            dist = py.Vector2(*enemigo.pos)
            dist -= py.Vector2(self.x, self.y)
            if dist.length()-5 < self.rango: #-5 por un pequeño radio del enemigo
                self.objetivo = enemigo
                self.angulo = -dist.as_polar()[1] - 90
                enemigo.golpe(self.daño)
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
    
    def draw(self, superficie: py.Surface, capa: py.Surface):
        self.image = py.transform.rotate(self.imagen_original,self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        if self.seleccionado:
            capa.blit(self.rango_imagen,self.rango_rect)
            capa.blit(self.image,self.rect)
        else:
            superficie.blit(self.image,self.rect)
