FILAS = 20
COLUMNAS = 20
TAMAÑO_PIXEL = 32
from pygame import Rect, Vector2
from Estructuras.Lineales import SingleLinkedList as SLL
vertices: SLL[Vector2] = SLL(
    Vector2(560,0),
    Vector2(560,112),
    Vector2(240,112),
    Vector2(240,48),
    Vector2(80,48),
    Vector2(80,336),
    Vector2(176,336),
    Vector2(176,272),
    Vector2(336,272),
    Vector2(336,304),
    Vector2(592,304),
    Vector2(592,560),
    Vector2(432,560),
    Vector2(432,432),
    Vector2(272,432),
    Vector2(272,560),
    Vector2(0,560)
)
cajas_camino: SLL[Rect] = SLL()
def calcular_cajas_camino():
    itr = iter(vertices)
    inicio = Vector2(next(itr))
    for i, fin in enumerate(itr):
        fin = Vector2(fin)
        direccion: Vector2 = fin - inicio
        if i == 0:
            direccion +=  direccion.normalize()*TAMAÑO_PIXEL
        elif i == len(vertices)-2:
            inicio += direccion.normalize()*TAMAÑO_PIXEL
            direccion -=  direccion.normalize()*TAMAÑO_PIXEL
        else:
            inicio += direccion.normalize()*TAMAÑO_PIXEL
            # direccion +=  direccion.normalize()*2*c.TAMAÑO_PIXEL
        caja = Rect(
            0,
            0,
            direccion.length() if direccion.x else TAMAÑO_PIXEL*2,
            direccion.length() if direccion.y else TAMAÑO_PIXEL*2
        )
        caja.center = inicio + direccion/2
        cajas_camino.push_back(caja)
        inicio = fin
calcular_cajas_camino()
PANEL_CONTIGUO = 200 
SPAWN_COOLDOWN = 400
VIDA_JUGADOR = 100
DINERO = 900
VENTANA_ALTURA = FILAS*TAMAÑO_PIXEL
VENTANA_ANCHO = COLUMNAS*TAMAÑO_PIXEL
FPS = 60
DELAY_ANIMACION = 15
NIVELES_TORRETAS = 7
SUBIR_TORRETA = 2
COSTO_TORRETA = 200
MEJORAR_TORRETA = 150
RECOMPENSA_NIVEL = 300
