#modulos externos
import pygame as py
from os.path import dirname
from typing import Callable
#estructuras de datos
from Estructuras.Lineales import SingleLinkedList as SLL
from Estructuras.Otras import HashmapProbing as HP
from Estructuras.NoLineales import ArbolBinario as AB
#modulos tower defense
from TowerDefense.Main_Game.Enemigos import Enemigo
from TowerDefense.Main_Game import Constantes as c
from TowerDefense.Main_Game.Torreta import Torreta
from TowerDefense.Main_Game.Mundo import World
from TowerDefense.Main_Game.Botones import Boton
from TowerDefense.Main_Game.Enemigos_Datos import Enemigo_Spwan

py.init()
#para importar correctamente los archivos sin importar la posicion en conslola
path: str = dirname(__file__)
gana = 0 #-1 pierde, 1 gana
ultimo_enemigo_creado = py.time.get_ticks()
game_over = False 
colocar_torretas = False
inicio_nivel = False
torreta_seleccionada: Torreta|None = None
torreta_seleccionada_arbol = None
torreta_seleccionada_imagen_izquierda = None
torreta_seleccionada_imagen_derecha = None
boton_subir_nivel_camino_1 = None
boton_subir_nivel_camino_2 = None
botones_mejora_visibles = False
frecuencia = py.time.Clock()
ventana = py.display.set_mode((c.VENTANA_ANCHO + c.PANEL_CONTIGUO,c.VENTANA_ALTURA))
py.display.set_caption("Tower Defense")
texto_fuente = py.font.SysFont("Consolas",24,bold=True)
fuente_largo = py.font.SysFont("Consolas",36)

mapa_imagen: py.Surface                     = py.image.load(path+"\TowerDefense\Assets\Imagenes\Zona\Mapa1.png").convert_alpha()
torreta_cursor: py.Surface                  = py.image.load(path+"\TowerDefense\Assets\Imagenes\Torretas\Torreta_Cursor.png").convert_alpha()
boton_comprar_torreta_imagen:py.Surface     = py.image.load(path+"\TowerDefense\Assets\Imagenes\Botones\\buy_turret.png").convert_alpha()
boton_cancelar_imagen:py.Surface            = py.image.load(path+"\TowerDefense\Assets\Imagenes\Botones\cancel.png").convert_alpha() 
boton_subir_nivel_torreta_imagen:py.Surface = py.image.load(path+"\TowerDefense\Assets/Imagenes/Botones/upgrade_turret.png").convert_alpha()
boton_empezar_nivel_imagen:py.Surface       = py.image.load(path+"\TowerDefense\Assets/Imagenes/Botones/begin.png").convert_alpha()
boton_reiniciar_juego_imagen:py.Surface     = py.image.load(path+"\TowerDefense\Assets/Imagenes/Botones/restart.png").convert_alpha()
spritesheets_torretas = SLL()
primeros_spritesheets_torretas = []
for x in range(1,c.NIVELES_TORRETAS+1):
    torreta_spritesheet: py.Surface = py.image.load(path+f"\TowerDefense\Assets/Imagenes/Torretas/Animacion_Torreta_{x}.png").convert_alpha()
    spritesheets_torretas.push_back(torreta_spritesheet)
    primera_imagen = AB.obtener_primera_imagen(torreta_spritesheet)
    primeros_spritesheets_torretas.append(primera_imagen)
arbol_spritesheets_torreta = AB.construir_arbol_binario_completo(spritesheets_torretas)
AB.asignar_niveles_en_orden(arbol_spritesheets_torreta)
enemigos_imagenes = {
    "debil": py.image.load(path+"\TowerDefense\Assets/Imagenes/Enemigos/enemy_1.png").convert_alpha(),
    "medio": py.image.load(path+"\TowerDefense\Assets/Imagenes/Enemigos/enemy_2.png").convert_alpha(),
    "fuerte": py.image.load(path+"\TowerDefense\Assets/Imagenes/Enemigos/enemy_3.png").convert_alpha(),
    "elite": py.image.load(path+"\TowerDefense\Assets/Imagenes/Enemigos/enemy_4.png").convert_alpha()
}
mundo = World(mapa_imagen)

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

def dibujar_texto(texto,fuente,color,x,y):
    img = fuente.render(texto,True,color)
    ventana.blit(img, (x,y))

def grid_a_hash(columna: int, fila: int) -> int:
    return fila*c.COLUMNAS + columna

def crear_torreta(pos: tuple[int, int]) -> None:
    new_pos: py.Vector2 = py.Vector2(*pos)
    new_pos //= c.TAMAÑO_PIXEL
    int_hash: int = grid_a_hash(*new_pos)
    if not espacios_ocupados.search(int_hash):
        new_pos += py.Vector2(0.5, 0.5)
        new_pos *= c.TAMAÑO_PIXEL
        new_torreta: Torreta = Torreta(spritesheets_torretas, *new_pos)
        espacios_ocupados.insert(int_hash, new_torreta)
        grupo_torretas.add(new_torreta)

layer: py.Surface = py.Surface(ventana.get_size(), py.SRCALPHA)
boton_torreta = Boton(c.VENTANA_ANCHO+30,120,boton_comprar_torreta_imagen)
boton_cancelar = Boton(c.VENTANA_ANCHO+50,180,boton_cancelar_imagen)
boton_subir_nivel = Boton(c.VENTANA_ANCHO+5,180,boton_subir_nivel_torreta_imagen)
boton_empezar_nivel = Boton(c.VENTANA_ANCHO+20,300,boton_empezar_nivel_imagen)
boton_reiniciar = Boton(310,300,boton_reiniciar_juego_imagen)

run = True
while run:
    #limpia capa superior
    layer.fill((0,0,0,0))
    ventana.fill("grey100")
    #re-dibuja fondo
    mundo.draw(ventana)
    for caja in c.cajas_camino: #wireframe de cajas de collsion del camino
        py.draw.rect(ventana, "grey", caja, width= 1)
    # py.draw.lines(ventana,"grey0",False,c.vertices)
    # 
    if not game_over:
        if mundo.vida_jugador <= 0:
            game_over = True
            game = -1
        if mundo.nivel > len(Enemigo_Spwan):
            game_over = True
            game = 1
        if not torreta_seleccionada:
            if inicio_nivel and py.time.get_ticks() - ultimo_enemigo_creado > c.SPAWN_COOLDOWN:
                if mundo.enemigos_spawneados < len(mundo.lista_enemigos):
                    tipo_enemigo = mundo.lista_enemigos[mundo.enemigos_spawneados]
                    enemigo = Enemigo(tipo_enemigo,c.vertices, enemigos_imagenes, mundo)
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
    else:
        py.draw.rect(ventana,"dodgerblue",(200,200,400,200), border_radius= 30)
        if game == -1:
            dibujar_texto("Game Over", fuente_largo,"grey0", 310,230)
        elif game == 1:    
            dibujar_texto("You Win!!!", fuente_largo,"grey0", 315,230)
                
    #deteccion de eventos -------------------------------------------
    posicion_mouse = py.mouse.get_pos()
    if py.event.get(py.QUIT):
       run = False
    for event in py.event.get(py.MOUSEBUTTONDOWN):
        if event.button == 1: #click izquierdo
            if boton_cancelar.on_click(event, posicion_mouse): colocar_torretas = False
            if colocar_torretas:
                if (posicion_mouse[0] < c.VENTANA_ANCHO and
                    posicion_mouse[1] < c.VENTANA_ALTURA and #si esta dentro del area de juego
                    mundo.dinero >= c.COSTO_TORRETA):        #y se tiene el dinero
                    crear_torreta(posicion_mouse)
                    colocar_torretas = False
                    mundo.dinero -= c.COSTO_TORRETA
            elif torreta_seleccionada != None:
                if (boton_subir_nivel.on_click(event, posicion_mouse) and #si se presiono el boton
                    torreta_seleccionada.nivel < c.NIVELES_TORRETAS and   #y se puede mejorar
                    mundo.dinero >= c.MEJORAR_TORRETA):                   #y se tiene el dinero
                    # Inicio Botones para elegir camino
                    for i in range(len(spritesheets_torretas)):
                        array1 = surfarray.array3d(primeros_spritesheets_torretas[i])
                        array2 = surfarray.array3d(torreta_seleccionada.imagen_original)
                        igualdad = (array1 == array2).all()
                        if igualdad:
                            torreta_seleccionada_arbol = AB.encontrar_nodo(arbol_spritesheets_torreta,spritesheets_torretas[i])
                            torreta_seleccionada_imagen_izquierda = AB.obtener_primera_imagen(torreta_seleccionada_arbol.izquierda.valor)
                            torreta_seleccionada_imagen_derecha = AB.obtener_primera_imagen(torreta_seleccionada_arbol.derecha.valor)
                    if not botones_mejora_visibles:
                        boton_subir_nivel_camino_1 = Boton(c.VENTANA_ANCHO + 5, 400, torreta_seleccionada_imagen_izquierda)
                        boton_subir_nivel_camino_2 = Boton(c.VENTANA_ANCHO + 100, 400, torreta_seleccionada_imagen_derecha)
                        botones_mejora_visibles = True
            
                if botones_mejora_visibles:
                    click_camino_1 = boton_subir_nivel_camino_1.draw(ventana)
                    click_camino_2 = boton_subir_nivel_camino_2.draw(ventana)
                    if mundo.dinero >= c.MEJORAR_TORRETA:
                        if click_camino_1:
                            torreta_seleccionada.subir_nivel(torreta_seleccionada_arbol,torreta_seleccionada_arbol.izquierda)
                            mundo.dinero -= c.MEJORAR_TORRETA
                            botones_mejora_visibles = False
                            
                        if click_camino_2:
                            torreta_seleccionada.subir_nivel(torreta_seleccionada_arbol,torreta_seleccionada_arbol.derecha)
                            mundo.dinero -= c.MEJORAR_TORRETA
                            botones_mejora_visibles = False
                     # Final Botones para elegir camino
                    torreta_seleccionada.subir_nivel()
                    mundo.dinero -= c.MEJORAR_TORRETA
                else:
                    torreta_seleccionada.seleccionado = False
                    torreta_seleccionada = None
                    ocu_hash = grid_a_hash(*map(lambda x: x//c.TAMAÑO_PIXEL,posicion_mouse))
                    if isinstance(espacios_ocupados[ocu_hash], Torreta):
                        torreta_seleccionada = espacios_ocupados[ocu_hash]
                        torreta_seleccionada.seleccionado = True
            else: #selecciona la torreta
                ocu_hash = grid_a_hash(*map(lambda x: x//c.TAMAÑO_PIXEL,posicion_mouse))
                if isinstance(espacios_ocupados[ocu_hash], Torreta):
                    torreta_seleccionada = espacios_ocupados[ocu_hash]
                    torreta_seleccionada.seleccionado = True
            if game_over:
                if boton_reiniciar.on_click(event, posicion_mouse):
                    game_over = False
                    inicio_nivel = False
                    ultimo_enemigo_creado = py.time.get_ticks()
                    colocar_torretas = False
                    torreta_seleccionada = None
                    mundo = World(mapa_imagen)
                    mundo.procesar_enemigos()
                    grupo_enemigos.empty()
                    grupo_torretas.empty()
            else:
                if not inicio_nivel:
                    if boton_empezar_nivel.on_click(event, posicion_mouse):
                        inicio_nivel = True
            #el checkeo debe ser despues o si no pone la torreta de una vez
            if boton_torreta.on_click(event, posicion_mouse): colocar_torretas = True
    #update de entidades en el mapa
    grupo_enemigos.update()
    grupo_torretas.update(grupo_enemigos)
    #dibujar objetos ------------------------------------------------
    dibujar_texto(str(mundo.vida_jugador), texto_fuente, "grey100", 0, 0)
    dibujar_texto(str(mundo.dinero), texto_fuente, "grey100", 0, 30)
    dibujar_texto(str(mundo.nivel), texto_fuente, "grey100", 0, 60)
    boton_torreta.draw(ventana)
    if colocar_torretas:
        if posicion_mouse[0] <= c.VENTANA_ANCHO: # dibuja torreta a poner
            cursor_rect = torreta_cursor.get_rect()
            cursor_pos = py.Vector2(posicion_mouse)//c.TAMAÑO_PIXEL
            if not espacios_ocupados[grid_a_hash(*cursor_pos)]:
                cursor_rect.center = (cursor_pos+py.Vector2(0.5,0.5))*c.TAMAÑO_PIXEL
                ventana.blit(torreta_cursor,cursor_rect)
        boton_cancelar.draw(ventana)
    if torreta_seleccionada:
        if torreta_seleccionada.nivel < c.NIVELES_TORRETAS:
            boton_subir_nivel.draw(ventana)
    for enemigo in grupo_enemigos: enemigo.draw(ventana)
    for torreta in grupo_torretas: torreta.draw(ventana, layer)
    if not inicio_nivel: boton_empezar_nivel.draw(ventana)
    ventana.blit(layer, layer.get_rect())
    py.display.update()
    frecuencia.tick(c.FPS)

py.quit()
