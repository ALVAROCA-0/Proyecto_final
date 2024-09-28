FILAS = 20
COLUMNAS = 20
TAMAÑO_PIXEL = 32
from Estructuras.Lineales import SingleLinkedList as SLL
vertices = SLL[
    (560,0),
    (560,112),
    (240,112),
    (240,48),
    (80,48),
    (80,336),
    (176,336),
    (176,272),
    (336,272),
    (336,304),
    (592,304),
    (592,560),
    (432,560),
    (432,432),
    (272,432),
    (272,560),
    (0,560)
]
VENTANA_ALTURA = FILAS*TAMAÑO_PIXEL
VENTANA_ANCHO = COLUMNAS*TAMAÑO_PIXEL
FPS = 60
