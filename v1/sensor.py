from multiprocessing import current_process
import random
import numpy as np
from time import sleep

from comandos_linux import *
class Sensor():
    def __init__(self, posicion, velocidad, cola_medidas, cola_medidas_iu, pids, inicio_iu):
        
        self.inicio_iu = inicio_iu
        self.pids = pids

        self.velocidad_carro = velocidad
        self.velocidad_sensor = 0

        self.cola_medidas = cola_medidas
        self.cola_medidas_iu = cola_medidas_iu
        self.posicion = posicion

    def iniciar(self, fin_procesos):
        self.pids[1] = pid()
        
        self.inicio_iu.wait()
        while(not fin_procesos.is_set()):
            
            #self.pids[1], self.n_cpu[1], self.per_cpu[1] = update_info_cpu()

            self.update_velocidad_sensor()
           
            sleep(self.velocidad_sensor)
            value = self.posicion.value

            muestra = self.calcular(value)
            
            self.cola_medidas_iu.put([value, muestra])

   

            self.cola_medidas.put(muestra)
            


    def calcular(self, x):
        aux = x % 50
        if 10 < aux < 40:
            ra = random.randint(3, 4)
            return np.sin(x*30) * 0.5
        else:
            ra = random.randint(3, 4)
            return np.sin(x/10) * 4
        
    def update_velocidad_sensor(self):
        if(self.velocidad_carro.value >= 70):
            self.velocidad_sensor = 3/70
        else:
            self.velocidad_sensor = (3/(10*self.velocidad_carro.value))
