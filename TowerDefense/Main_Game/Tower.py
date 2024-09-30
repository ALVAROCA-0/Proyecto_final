import pygame as py
from Enemigos import Enemigo
import Constantes as c
from Constantes import vertices, mapa_matriz
#import Main_Game.Estructuras.SingleLinkedList as SLL
from Torreta import Torreta
from Mundo import World
from Botones import Boton

py.init()
colocar_torretas = False
torreta_seleccionada = None
fuente = py.font.Font(None, 36)
frecuencia = py.time.Clock()
ventana = py.display.set_mode((c.VENTANA_ANCHO + c.PANEL_CONTIGUO,c.VENTANA_ALTURA))
py.display  .set_caption("Tower Defense")

def crear_torreta(posicion_mouse):
    mouse_tile_x = posicion_mouse[0] // c.TAMAÑO_PIXEL
    mouse_tile_y = posicion_mouse[1] // c.TAMAÑO_PIXEL
    mouse_tile_num = (mouse_tile_y * c.COLUMNAS) + mouse_tile_x
    if mapa_matriz[mouse_tile_num] == 22:
        espacio_libre = True
        for torreta in grupo_torretas:
            if (mouse_tile_x, mouse_tile_y) == (torreta.pos_x, torreta.pos_y):
                espacio_libre = False
        if espacio_libre:
            nueva_torreta = Torreta(spritesheets_torretas,mouse_tile_x,mouse_tile_y)
            grupo_torretas.add(nueva_torreta)

def seleccionar_torreta(posicion_mouse):
    mouse_tile_x = posicion_mouse[0] // c.TAMAÑO_PIXEL
    mouse_tile_y = posicion_mouse[1] // c.TAMAÑO_PIXEL
    for torreta in grupo_torretas:
            if (mouse_tile_x, mouse_tile_y) == (torreta.pos_x, torreta.pos_y):
                return torreta

mapa_imagen: py.Surface = py.image.load("Assets/Imagenes/Zona/Mapa1.png").convert_alpha()
spritesheets_torretas = []
for x in range(1,c.NIVELES_TORRETAS+1):
    torreta_spritesheet: py.Surface = py.image.load(f"Assets/Imagenes/Torretas/Animacion_Torreta_{x}.png").convert_alpha()
    spritesheets_torretas.append(torreta_spritesheet)
torreta_cursor: py.Surface = py.image.load("Assets/Imagenes/Torretas/Torreta_Cursor.png").convert_alpha()
enemigo_imagen: py.Surface = py.image.load("Assets/Imagenes/Enemigos/enemy_2.png").convert_alpha()
boton_comprar_torreta_imagen:py.Surface = py.image.load("Assets/Imagenes/Botones/buy_turret.png").convert_alpha()
boton_cancelar_imagen:py.Surface = py.image.load("Assets/Imagenes/Botones/cancel.png").convert_alpha() 
boton_subir_nive_torreta_imagen:py.Surface = py.image.load("Assets/Imagenes/Botones/upgrade_turret.png").convert_alpha() 
 
grupo_enemigos = py.sprite.Group()
grupo_torretas = py.sprite.Group()
enemigo = Enemigo(vertices, enemigo_imagen)
mundo = World(mapa_imagen)
grupo_enemigos.add(enemigo)

boton_torreta = Boton(c.VENTANA_ANCHO+30,120,boton_comprar_torreta_imagen)
boton_cancelar = Boton(c.VENTANA_ANCHO+50,180,boton_cancelar_imagen)
boton_subir_nivel = Boton(c.VENTANA_ANCHO+5,180,boton_subir_nive_torreta_imagen)

run = True
while run:
    
    ventana.fill("grey100")
    py.draw.lines(ventana,"grey0",False,vertices)
    mundo.draw(ventana)
    #py.draw.lines(ventana,"grey0",False,vertices)
    grupo_enemigos.update()
    grupo_torretas.update(grupo_enemigos)
    if torreta_seleccionada:
        torreta_seleccionada.selected = True
        
    grupo_enemigos.draw(ventana)
    for torreta in grupo_torretas:
        torreta.draw(ventana)
    
    if boton_torreta.draw(ventana):
        colocar_torretas = True
    if colocar_torretas:
        cursor_rect = torreta_cursor.get_rect()
        cursor_pos = py.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] <= c.VENTANA_ANCHO:
            ventana.blit(torreta_cursor,cursor_rect)
        if boton_cancelar.draw(ventana):
            colocar_torretas = False
    if torreta_seleccionada:
        if torreta_seleccionada.nivel < c.NIVELES_TORRETAS:
            if boton_subir_nivel.draw(ventana):
                torreta_seleccionada.subir_nivel()
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            posicion_mouse = py.mouse.get_pos()
            if posicion_mouse[0] < c.VENTANA_ANCHO and posicion_mouse[1] < c.VENTANA_ALTURA:
                if colocar_torretas:
                    crear_torreta(posicion_mouse)
                    colocar_torretas = False
                else:
                    torreta_seleccionada = seleccionar_torreta(posicion_mouse)
    py.display.update()
    frecuencia.tick(c.FPS)

py.quit()
py.quit()