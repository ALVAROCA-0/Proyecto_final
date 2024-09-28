# Proyecto final de Estructuras de Datos 2024-1
Juego tower defense creado por Nicolas Pajaro y Álvaro Romero
## Juego tower defense
El archivo ejecutable es `main.py`, este a traves de los modulos dentro de la carpeta TowerDefense se encarga de el juego en si.

### Carpeta TowerDefense:
Contiene la carpeta Assets con texturas para los objetos de juego. Y tambien esta la carpeta Main_Game donde estan los modulos que permiten la ejecucion del juego

## Paquete Estructuras:
Paquete que contiene todas las estructuras a ser usadas
Contiene los sub-paquetes:
* Lineales
* NoLineales
* Otras.

### Sub-Paquete Lineales:
Se encuentran los siguientes modulos:
* SingleLinkedList
* DoubleLinkedList
* ArrayList
* Queue
* Stack

Tambien se encuentra la carpeta Array que contiene:
* Array.c
* setup.py

Para compilar codigo usando Array se debe:
1. Compilar setup.py con: `python setup.py build_ext --inplace`
2. Al importar Array usar: `from {camino de paquetes hasta Array}.Array import Array`
3. El editor no encuentra el archivo, pero ya esta importada la clase Array

### Sub-Paquete NoLineales:
Se encuentras los siguientes modulos:
* ArbolBinario
* ArbolAVL

### Sub-Paquete Otros:
Se encuentras los siguientes modulos:
* HashmapProbing.py
* HashmapSeparateChaining.py