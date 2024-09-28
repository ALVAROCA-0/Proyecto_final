import pygame as py
from TowerDefense.Main_Game.Enemigos import Enemigo
from TowerDefense.Main_Game import Constantes as c
from Estructuras.Lineales import SingleLinkedList as SLL
from Estructuras.Otras import HashmapProbing as HP
from TowerDefense.Main_Game.Torreta import Torreta
from TowerDefense.Main_Game.Mundo import World
from os.path import dirname

py.init()

#para importar correctamente los archivos sin importar la posicion en conslola
path: str = dirname(__file__)
frecuencia = py.time.Clock()
ventana = py.display.set_mode((c.VENTANA_ANCHO,c.VENTANA_ALTURA))
py.display.set_caption("Tower Defense")

mapa_imagen: py.Surface = py.image.load(path+"\TowerDefense\Assets\Imagenes\Zona\Mapa1.png").convert_alpha()
torreta_cursor: py.Surface = py.image.load(path+"\TowerDefense\Assets\Imagenes\Torretas\Torreta_Cursor.png").convert_alpha()
torreta_imagen: py.Surface = py.transform.scale(torreta_cursor, (32,32))
enemigo_imagen: py.Surface = py.image.load(path+"\TowerDefense\Assets\Imagenes\Enemigos\enemy_2.png").convert_alpha()
grupo_enemigos = py.sprite.Group()
grupo_torretas = py.sprite.Group()

espacios_ocupados: HP[int, bool] = HP(c.COLUMNAS*c.FILAS)

#inicializacion de espacios ocupados basado en camino
for key in range(c.COLUMNAS*c.FILAS):
    y = key//c.COLUMNAS
    x = key - y*c.COLUMNAS
    y *= c.TAMAÑO_PIXEL
    x *= c.TAMAÑO_PIXEL
    ocupado = False
    for caja in c.cajas_camino:
        ocupado = caja.colliderect(x, y, c.TAMAÑO_PIXEL, c.TAMAÑO_PIXEL)
        if ocupado: break
    espacios_ocupados.insert(key, ocupado)

def crear_torreta(pos: tuple[int, int]) -> None:
    x, y = pos
    x //= c.TAMAÑO_PIXEL
    y //= c.TAMAÑO_PIXEL
    if not espacios_ocupados.search(y*c.COLUMNAS+x):
        espacios_ocupados.insert(y*c.COLUMNAS+x, True)
        x = (x + 0.5) * c.TAMAÑO_PIXEL
        y = (y + 0.5) * c.TAMAÑO_PIXEL
        grupo_torretas.add(Torreta(torreta_imagen, x, y))

enemigo = Enemigo(c.vertices, enemigo_imagen)
grupo_enemigos.add(enemigo)
mundo = World(mapa_imagen)
run = True
while run:
    ventana.fill("grey100")
    mundo.draw(ventana)
    # for caja in c.cajas_camino: #wireframe de cajas de collsion del camino
    #     py.draw.rect(ventana, "grey", caja, width= 1)
    # py.draw.lines(ventana,"grey0",False,c.vertices)
    grupo_enemigos.update()
    grupo_torretas.update()
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
