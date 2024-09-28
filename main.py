import pygame as py
from TowerDefense.Main_Game.Enemigos import Enemigo
import TowerDefense.Main_Game.Constantes as c
from TowerDefense.Main_Game.Constantes import vertices
from Estructuras.Lineales import SingleLinkedList as SLL
from TowerDefense.Main_Game.Torreta import Torreta
from TowerDefense.Main_Game.Mundo import World

py.init()

frecuencia = py.time.Clock()
ventana = py.display.set_mode((c.VENTANA_ANCHO,c.VENTANA_ALTURA))
py.display.set_caption("Tower Defense")

mapa_imagen: py.Surface = py.image.load("TowerDefense/Assets/Imagenes/Zona/Mapa1.png").convert_alpha()
torreta_cursor: py.Surface = py.image.load("TowerDefense/Assets/Imagenes/Torretas/Torreta_Cursor.png").convert_alpha()
torreta_imagen: py.Surface = py.transform.scale(torreta_cursor, (32,32))
enemigo_imagen: py.Surface = py.image.load("TowerDefense/Assets/Imagenes/Enemigos/enemy_2.png").convert_alpha()
grupo_enemigos = py.sprite.Group()
grupo_torretas = py.sprite.Group()

enemigo = Enemigo(vertices, enemigo_imagen)
grupo_enemigos.add(enemigo)
run = True
while run:
    ventana.fill("grey100")
    mundo.draw(ventana)
    #py.draw.lines(ventana,"grey0",False,vertices)
    grupo_enemigos.update()
    grupo_enemigos.draw(ventana)
    grupo_torretas.draw(ventana)
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            posicion_mouse = py.mouse.get_pos()
            if posicion_mouse[0] < c.VENTANA_ANCHO and posicion_mouse[1] < c.VENTANA_ALTURA:
                crear_torreta(posicion_mouse)
    py.display.update()
    frecuencia.tick(c.FPS)

py.quit()
