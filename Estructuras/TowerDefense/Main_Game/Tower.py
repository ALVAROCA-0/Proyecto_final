import pygame as py
from Enemigos import Enemigo
import Constantes as c
py.init()

frecuencia = py.time.Clock()
ventana = py.display.set_mode((c.VENTANA_ANCHO,c.VENTANA_ALTURA))
py.display.set_caption("Tower Defense")

enemigo_imagen = py.image.load("TowerDefense/Assets/Imagenes/Enemigos/enemy_2.png").convert_alpha()
grupo_enemigos = py.sprite.Group()
vertices = [
    (400,100),
    (400,200),
    (200,200),
    (200,300)
]
enemigo = Enemigo(vertices,enemigo_imagen)
grupo_enemigos.add(enemigo)

run = True
while run:
    frecuencia.tick(c.FPS)
    ventana.fill("grey100")
    py.draw.lines(ventana,"grey0",False,vertices)
    grupo_enemigos.update()
    grupo_enemigos.draw(ventana)
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
    py.display.update()

py.quit()