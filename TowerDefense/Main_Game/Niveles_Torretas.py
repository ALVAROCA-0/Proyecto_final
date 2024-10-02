import pygame as py
from Estructuras.Lineales import SingleLinkedList as SLL
from Estructuras.NoLineales.ArbolBinario import ArbolBinario
from os.path import dirname

py.init()
path = dirname(__file__)
niveles_arbol: ArbolBinario[dict[str, int|py.Surface]] = ArbolBinario(SLL(
    {"rango":90, "cooldown":1500,"daño":5, "imagen":path+f"/../Assets/Imagenes/Torretas/Animacion_Torreta_1.png"},
    {"rango":100,"cooldown":1350,"daño":8, "imagen":path+f"/../Assets/Imagenes/Torretas/Animacion_Torreta_2.png"},
    {"rango":110,"cooldown":1500,"daño":9, "imagen":path+f"/../Assets/Imagenes/Torretas/Animacion_Torreta_3.png"},
    {"rango":140,"cooldown":1200,"daño":14,"imagen":path+f"/../Assets/Imagenes/Torretas/Animacion_Torreta_4.png"},
    {"rango":110,"cooldown":800, "daño":12,"imagen":path+f"/../Assets/Imagenes/Torretas/Animacion_Torreta_5.png"},
    {"rango":150,"cooldown":1400,"daño":15,"imagen":path+f"/../Assets/Imagenes/Torretas/Animacion_Torreta_6.png"},
    {"rango":200,"cooldown":1600, "daño":20,"imagen":path+f"/../Assets/Imagenes/Torretas/Animacion_Torreta_7.png"}
))
