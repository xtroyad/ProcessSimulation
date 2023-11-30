from fourier import Fourier
from sensor import Sensor
from multiprocessing import Process, Value
from time import sleep
from comandos_linux import *

from multiprocessing import current_process

class Vehiculo:
    def __init__(self, colas_medidas, cola_medidas_iu, pids, inicio_iu, fin_procesos):
        self.fin_procesos = fin_procesos
        self.inicio_iu = inicio_iu
        self.pids = pids

        self.velocidad = Value("i", 10000) # cm/s
        self.posicion = Value("d", 0)
        self.sensor = Sensor(self.posicion, self.velocidad, colas_medidas, cola_medidas_iu, pids, inicio_iu)
 
    def iniciar(self): 
        proceso_sensor = Process(target= self.sensor.iniciar, args=(self.fin_procesos,))
        proceso_sensor.start()

        self.mover()

        proceso_sensor.join()

    def mover(self):
        i = 0
        
        self.inicio_iu.wait()
        while(not self.fin_procesos.is_set()):
            
            sleep(2/(self.velocidad.value))
            self.posicion.value = i
            i = i + 1
            
      

