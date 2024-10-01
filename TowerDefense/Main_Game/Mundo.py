import random
from .Enemigos_Datos import Enemigo_Spwan
from . import Constantes as c

class World():
    def __init__(self, imagen_mapa):
        self.image = imagen_mapa
        self.nivel = 1
        self.vida_jugador = c.VIDA_JUGADOR
        self.dinero = c.DINERO
        self.lista_enemigos = []
        self.enemigos_spawneados = 0
        self.enemigos_asesinados = 0
        self.enemigos_perdidos = 0

    def draw(self, surface):
        surface.blit(self.image, (0,0)) 
    
    def procesar_enemigos(self):
        if self.nivel <= len(Enemigo_Spwan):
            enemigos = Enemigo_Spwan[self.nivel -1]
            for tipo in enemigos:
                enemigos_para_spawnear = enemigos[tipo]
                for enemigo in range(enemigos_para_spawnear):
                    self.lista_enemigos.append(tipo)
            random.shuffle(self.lista_enemigos)
    
    def check_nivel_completado(self):
        if (self.enemigos_asesinados + self.enemigos_perdidos) == len(self.lista_enemigos):
            return True
    
    def nivel_reseteado(self):
        self.lista_enemigos = []
        self.enemigos_spawneados = 0
        self.enemigos_asesinados = 0
        self.enemigos_perdidos = 0