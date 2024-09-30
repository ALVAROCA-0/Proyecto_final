import pygame as py
from Enemigos import Enemigo
import Constantes as c
from Constantes import vertices, mapa_matriz
#import Main_Game.Estructuras.SingleLinkedList as SLL
from Torreta import Torreta
from Mundo import World
from Botones import Boton
from Enemigos_Datos import Enemigo_Spwan

py.init()
game_over = False
game = 0 # -1 pierde, 1 gana
ultimo_enemigo_creado = py.time.get_ticks()
colocar_torretas = False
torreta_seleccionada = None
inicio_nivel = False
fuente = py.font.Font(None, 36)
frecuencia = py.time.Clock()

ventana = py.display.set_mode((c.VENTANA_ANCHO + c.PANEL_CONTIGUO,c.VENTANA_ALTURA))
py.display  .set_caption("Tower Defense")

texto_fuente = py.font.SysFont("Consolas",24,bold=True)
fuente_largo = py.font.SysFont("Consolas",36)

def dibujar_texto(texto,fuente,color,x,y):
    img = fuente.render(texto,True,color)
    ventana.blit(img, (x,y))
     

def crear_torreta(posicion_mouse):
    torreta_colocada = False
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
            torreta_colocada = True
            mundo.dinero -= c.COSTO_TORRETA
    return torreta_colocada

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
enemigos_imagenes = {
    "debil": py.image.load("Assets/Imagenes/Enemigos/enemy_1.png").convert_alpha(),
    "medio": py.image.load("Assets/Imagenes/Enemigos/enemy_2.png").convert_alpha(),
    "fuerte": py.image.load("Assets/Imagenes/Enemigos/enemy_3.png").convert_alpha(),
    "elite": py.image.load("Assets/Imagenes/Enemigos/enemy_4.png").convert_alpha()
}
boton_comprar_torreta_imagen:py.Surface = py.image.load("Assets/Imagenes/Botones/buy_turret.png").convert_alpha()
boton_cancelar_imagen:py.Surface = py.image.load("Assets/Imagenes/Botones/cancel.png").convert_alpha() 
boton_subir_nivel_torreta_imagen:py.Surface = py.image.load("Assets/Imagenes/Botones/upgrade_turret.png").convert_alpha()
boton_empezar_nivel_imagen:py.Surface = py.image.load("Assets/Imagenes/Botones/begin.png").convert_alpha()
boton_reiniciar_juego_imagen:py.Surface = py.image.load("Assets/Imagenes/Botones/restart.png").convert_alpha()

grupo_enemigos = py.sprite.Group()
grupo_torretas = py.sprite.Group()

mundo = World(mapa_imagen)
mundo.procesar_enemigos()

boton_torreta = Boton(c.VENTANA_ANCHO+30,120,boton_comprar_torreta_imagen)
boton_cancelar = Boton(c.VENTANA_ANCHO+50,180,boton_cancelar_imagen)
boton_subir_nivel = Boton(c.VENTANA_ANCHO+5,180,boton_subir_nivel_torreta_imagen)
boton_empezar_nivel = Boton(c.VENTANA_ANCHO+20,300,boton_empezar_nivel_imagen)
boton_reiniciar = Boton(310,300,boton_reiniciar_juego_imagen)

run = True
while run:
    
    ventana.fill("grey100")
    py.draw.lines(ventana,"grey0",False,vertices)
    mundo.draw(ventana)
    
    if game_over == False:
        if mundo.vida_jugador <= 0:
            game_over = True
            game = -1
        if mundo.nivel > len(Enemigo_Spwan):
            game_over = True
            game = 1
        grupo_enemigos.update(mundo)
        grupo_torretas.update(grupo_enemigos)
        if torreta_seleccionada:
                torreta_seleccionada.selected = True
    
    grupo_enemigos.draw(ventana)
    for torreta in grupo_torretas:
        torreta.draw(ventana)
        
    dibujar_texto(str(mundo.vida_jugador), texto_fuente, "grey100", 0, 0)
    dibujar_texto(str(mundo.dinero), texto_fuente, "grey100", 0, 30)
    dibujar_texto(str(mundo.nivel), texto_fuente, "grey100", 0, 60)
    
    if game_over == False:
        if inicio_nivel == False:
            if boton_empezar_nivel.draw(ventana):
                inicio_nivel = True
        else:
            if py.time.get_ticks() - ultimo_enemigo_creado > c.SPAWN_COOLDOWN:
                if mundo.enemigos_spawneados < len(mundo.lista_enemigos):
                    tipo_enemigo = mundo.lista_enemigos[mundo.enemigos_spawneados]
                    enemigo = Enemigo(tipo_enemigo,vertices, enemigos_imagenes)
                    grupo_enemigos.add(enemigo)
                    mundo.enemigos_spawneados += 1
                    ultimo_enemigo_creado = py.time.get_ticks()
                
        if mundo.check_nivel_completado():
            mundo.nivel += 1
            mundo.dinero += c.RECOMPENSA_NIVEL
            inicio_nivel = False
            ultimo_enemigo_creado = py.time.get_ticks()
            mundo.nivel_reseteado()
            mundo.procesar_enemigos()
            
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
                    if mundo.dinero >= c.MEJORAR_TORRETA:
                        torreta_seleccionada.subir_nivel()
                        mundo.dinero -= c.MEJORAR_TORRETA
    else:
        py.draw.rect(ventana,"dodgerblue",(200,200,400,200), border_radius= 30)
        if game == -1:
            dibujar_texto("Game Over", fuente_largo,"grey0", 310,230)
        elif game == 1:    
            dibujar_texto("You Win!!!", fuente_largo,"grey0", 315,230)
        if boton_reiniciar.draw(ventana):
            game_over = False
            inicio_nivel = False
            ultimo_enemigo_creado = py.time.get_ticks()
            colocar_torretas = False
            torreta_seleccionada = None
            mundo = World(mapa_imagen)
            mundo.procesar_enemigos()
            grupo_enemigos.empty()
            grupo_torretas.empty()
    
                
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            posicion_mouse = py.mouse.get_pos()
            if posicion_mouse[0] < c.VENTANA_ANCHO and posicion_mouse[1] < c.VENTANA_ALTURA:
                if colocar_torretas:
                    if mundo.dinero >= c.COSTO_TORRETA:
                        if crear_torreta(posicion_mouse):
                            colocar_torretas = False
                else:
                    torreta_seleccionada = seleccionar_torreta(posicion_mouse)
    py.display.update()
    frecuencia.tick(c.FPS)

py.quit()
py.quit()