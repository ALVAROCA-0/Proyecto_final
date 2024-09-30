FILAS = 20
COLUMNAS = 20
TAMAÑO_PIXEL = 32
#import Main_Game.Estructuras.SingleLinkedList as SLL
vertices = [
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
mapa_matriz = [22, 68, 69, 70, 70, 70, 70, 70, 71, 22, 22, 22, 22, 22, 22, 22, 114, 162, 117, 22,
        22, 114, 115, 116, 116, 116, 116, 115, 163, 22, 22, 22, 22, 22, 22, 22, 114, 162, 117, 22,
        22, 114, 115, 886, 207, 207, 889, 161, 1024, 69, 69, 70, 70, 70, 70, 70, 1027, 162, 117, 22,
        22, 114, 115, 117, 22, 22, 160, 161, 161, 161, 161, 161, 161, 116, 116, 116, 116, 162, 117, 22,
        22, 114, 115, 117, 22, 22, 206, 207, 207, 207, 207, 207, 207, 207, 208, 208, 208, 208, 209, 22,
        22, 114, 115, 117, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
        22, 114, 115, 117, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
        22, 114, 115, 117, 68, 69, 69, 69, 69, 69, 69, 71, 22, 22, 22, 22, 22, 22, 22, 22,
        22, 114, 115, 117, 160, 115, 115, 115, 115, 115, 115, 1024, 69, 69, 69, 69, 69, 69, 69, 71,
        22, 114, 115, 1024, 1027, 162, 886, 207, 207, 889, 115, 115, 115, 115, 115, 115, 115, 115, 115, 117,
        22, 114, 115, 162, 162, 162, 163, 22, 22, 206, 207, 207, 207, 207, 207, 207, 207, 889, 162, 117,
        22, 206, 207, 207, 207, 207, 209, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 160, 162, 117,
        22, 22, 22, 22, 22, 22, 22, 68, 70, 70, 70, 70, 70, 70, 71, 22, 22, 160, 162, 117,
        22, 22, 22, 22, 22, 22, 22, 160, 162, 162, 162, 162, 162, 162, 163, 22, 22, 160, 162, 117,
        22, 22, 22, 22, 22, 22, 22, 160, 162, 886, 207, 207, 889, 162, 163, 22, 22, 160, 162, 117,
        22, 22, 22, 22, 22, 22, 22, 160, 162, 163, 22, 22, 160, 162, 163, 22, 22, 160, 162, 117,
        69, 69, 69, 69, 69, 69, 69, 1027, 162, 163, 22, 22, 160, 162, 1024, 69, 69, 1027, 162, 117,
        162, 162, 162, 162, 162, 162, 162, 162, 162, 163, 22, 22, 160, 162, 162, 162, 162, 162, 162, 163,
        207, 207, 207, 207, 207, 207, 207, 207, 208, 209, 22, 22, 206, 208, 208, 208, 208, 208, 208, 209,
        22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22]
PANEL_CONTIGUO = 200 
SPAWN_COOLDOWN = 400
VIDA_JUGADOR = 100
DINERO = 900
VENTANA_ALTURA = FILAS*TAMAÑO_PIXEL
VENTANA_ANCHO = COLUMNAS*TAMAÑO_PIXEL
FPS = 60
ANIMACION_TORRETAS = 8
DELAY_ANIMACION = 15
NIVELES_TORRETAS = 4
COSTO_TORRETA = 200
MEJORAR_TORRETA = 150
RECOMPENSA_NIVEL = 300