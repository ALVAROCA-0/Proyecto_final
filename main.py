import pygame as py
from TowerDefense.Main_Game.Enemigos import Enemigo
from TowerDefense.Main_Game import Constantes as c
from Estructuras.Lineales import SingleLinkedList as SLL, ArrayList
from Estructuras.Otras import HashmapProbing as HP
from TowerDefense.Main_Game.Torreta import Torreta
from TowerDefense.Main_Game.Mundo import World
from typing import Callable
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

espacios_ocupados: HP[int, bool | Torreta] = HP(c.COLUMNAS*c.FILAS)

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

def grid_a_hash(columna: int, fila: int) -> int:
    return fila*c.COLUMNAS + columna

def crear_torreta1(pos: tuple[int, int]) -> None:
    new_pos: py.Vector2 = py.Vector2(*pos)
    new_pos //= c.TAMAÑO_PIXEL
    int_hash: int = grid_a_hash(*new_pos)
    if not espacios_ocupados.search(int_hash):
        new_pos += py.Vector2(0.5, 0.5)
        new_pos *= c.TAMAÑO_PIXEL
        new_torreta: Torreta = Torreta(torreta_imagen, *new_pos, 100)
        espacios_ocupados.insert(int_hash, new_torreta)
        grupo_torretas.add(new_torreta)

proc_torretas: ArrayList[Callable[[tuple[int,int]],None]] = ArrayList(
    crear_torreta1
)

placing: bool = True
selected: Torreta | None = None

layer: py.Surface = py.Surface(ventana.get_size(), py.SRCALPHA)
enemigo = Enemigo(c.vertices, enemigo_imagen, 100)
grupo_enemigos.add(enemigo)
mundo = World(mapa_imagen)
run = True
while run:
    layer.fill((0,0,0,0))
    ventana.fill("grey100")
    mundo.draw(ventana)
    # for caja in c.cajas_camino: #wireframe de cajas de collsion del camino
    #     py.draw.rect(ventana, "grey", caja, width= 1)
    # py.draw.lines(ventana,"grey0",False,c.vertices)
    grupo_enemigos.update()
    grupo_torretas.update(grupo_enemigos)
    grupo_enemigos.draw(ventana)
    
    for torreta in grupo_torretas: torreta.draw(ventana, layer)
    ventana.blit(layer, layer.get_rect())
    if py.event.get(py.QUIT):
       run = False
    for event in py.event.get(py.MOUSEBUTTONDOWN):
        if event.button == 1:
            posicion_mouse = py.mouse.get_pos()
            if placing: 
                if posicion_mouse[0] < c.VENTANA_ANCHO and posicion_mouse[1] < c.VENTANA_ALTURA:
                    crear_torreta1(posicion_mouse)
            else:
                ocu_hash = grid_a_hash(*map(lambda x: x//c.TAMAÑO_PIXEL,posicion_mouse))
                if selected: selected.selected = False
                if isinstance(espacios_ocupados[ocu_hash], Torreta):
                    selected = espacios_ocupados[ocu_hash]
                    selected.selected = True     
        elif event.button == 3:
            placing = not placing     
    # for event in py.event.get(py.MOUSEMOTION):
    py.display.update()
    frecuencia.tick(c.FPS)

py.quit()
