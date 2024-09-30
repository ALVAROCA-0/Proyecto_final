from PIL import Image
import pygame as py
import Constantes as c
# Cargar la imagen
imagen = Image.open("Assets/Imagenes/Torretas/Animacion_Torreta_2.png")

# Obtener el tamaño de la imagen (ancho, alto)
ancho, alto = imagen.size
py.init()
ventana = py.display.set_mode((ancho, alto))  # Reemplaza ancho y alto con tus dimensiones
print(f"Ancho: {ancho} píxeles")
print(f"Alto: {alto} píxeles")
sprite_sheet: py.Surface = py.image.load("Assets/Imagenes/Torretas/Animacion_Torreta_2.png").convert_alpha()

tamaño_sprite = sprite_sheet.get_height()  # Esto debería ser 128
print(tamaño_sprite)
if sprite_sheet.get_width() != 1024 or tamaño_sprite != 128:
    print(f"Error: El tamaño de la hoja de sprites no es el esperado. Ancho: {sprite_sheet.get_width()}, Alto: {tamaño_sprite}")
print(f"Error: El tamaño de la hoja de sprites no es el esperado. Ancho: {sprite_sheet.get_width()}, Alto: {tamaño_sprite}")

lista_animacion = []

for x in range(c.ANIMACION_TORRETAS):
    if x * tamaño_sprite + tamaño_sprite > sprite_sheet.get_width():
        print(f"Error: Subsurface fuera del área en el índice {x}")
        break  # Sal del bucle si intentas acceder fuera de la imagen

    imagen_temporal = sprite_sheet.subsurface(x * tamaño_sprite, 0, tamaño_sprite, tamaño_sprite)
    lista_animacion.append(imagen_temporal)

print(lista_animacion)

run = True
while run:
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
py.quit()        
# import pygame as py

# # Inicializa Pygame
# py.init()

# # Configuraciones de la ventana
# ANCHO_VENTANA = 800
# ALTURA_VENTANA = 600
# ventana = py.display.set_mode((ANCHO_VENTANA, ALTURA_VENTANA))
# py.display.set_caption("Contador de Dinero")

# # Cargar fuente
# fuente = py.font.Font(None, 36)  # Fuente por defecto, tamaño 36

# # Variables de dinero
# dinero = 100  # Cantidad inicial de dinero

# def mostrar_dinero():
#     texto_dinero = f'Dinero: ${dinero}'
#     superficie_texto = fuente.render(texto_dinero, True, (255, 255, 255))  # Texto blanco
#     ventana.blit(superficie_texto, (20, 20))  # Posición del texto

# def sumar_dinero(cantidad):
#     global dinero
#     dinero += cantidad

# def restar_dinero(cantidad):
#     global dinero
#     dinero -= cantidad

# # Bucle principal
# run = True
# while run:
#     for event in py.event.get():
#         if event.type == py.QUIT:
#             run = False
        
#         # Ejemplo de sumar o restar dinero con teclas
#         if event.type == py.KEYDOWN:
#             if event.key == py.K_UP:  # Sumar $10
#                 sumar_dinero(10)
#             if event.key == py.K_DOWN:  # Restar $10
#                 restar_dinero(10)

#     ventana.fill((0, 0, 0))  # Fondo negro
#     mostrar_dinero()  # Mostrar el dinero en la ventana
#     py.display.update()  # Actualiza la ventana

# # Cierra Pygame
# py.quit()
