import random
import psutil
import numpy as np
from time import sleep
from grafica import Grafica
from comandos_linux import *

class Carrito:
    def __init__(self, recorrido_saltado, medidas, recorrido, datos_fourier, barrera_principal, barrera_principal_fin, barrera_fourier, barrera_fourier_fin, posicion_cpu, pids, porcen_cpu):
        
        self.barrera_fourier_fin = barrera_fourier_fin

        self.porcen_cpu = porcen_cpu
        self.posicion_cpu = posicion_cpu
        self.pids = pids
        
        self.velocidad = 1 #cm/s
        self.distancia = -1

        self.barrera_principal = barrera_principal
        self.barrera_principal_fin = barrera_principal_fin

        self.barrera_fourier = barrera_fourier
        self.barrera_fourier_fin = barrera_fourier_fin

        self.recorrido_saltado = recorrido_saltado
        self.recorrido_saltado[0] = self.distancia
        self.recorrido_saltado[1] = self.distancia

        self.medidas = medidas
        self.recorrido  = recorrido
        self.datos_para_fourier = datos_fourier

    def update_posicion(self):
        self.recorrido_saltado[0] = self.distancia + 1
        self.distancia = self.distancia + self.velocidad
        self.recorrido_saltado[1] = self.distancia
        
        
    def update_info_cpu(self):
        self.pids[0] = pid()
        self.posicion_cpu[0] = cpu(self.pids[0])
        self.porcen_cpu[0] = porcentaje_cpu(self.pids[0])
        
    def iniciar_sensor(self):
        cont = 0 
        while(True):
            print(self.velocidad)
            cont = cont + 1
            if cont == 50:
                cont = 0
                if self.porcen_cpu[2] > 80.0:
                    self.update_velocidad(self.velocidad-1)
                else:
                    self.update_velocidad(self.velocidad+1)


            self.update_posicion()
            self.update_info_cpu()

            self.barrera_principal.wait()
            sleep(1/(self.velocidad*100))
         
            ini = self.recorrido_saltado[0] 
            fin = self.recorrido_saltado[1] 

            real = 0
            if ini == fin:
                real = self.tomar_medida(self.distancia)
                self.recorrido.put(real)
            else:
                # Para visualizar recorrido hecho
                for i in range(ini, fin+1):
                    real = self.tomar_medida(i)
                    self.recorrido.put(real)
                    
            # Para visualizar los datos que se han podido conseguir

            self.medidas.put([self.distancia, real])

  
            # Para calcular Fourier
            self.barrera_fourier.wait()
            self.datos_para_fourier.put(real)
            self.barrera_fourier_fin.wait()

            self.barrera_principal_fin.wait()

    def tomar_medida(self, x):
        aux = x % 50
        if 10 < aux < 40:
            return 0
        else:
            ra = random.randint(3, 4)
            return np.sin(x/6) * ra

    def update_velocidad(self, velocidad):
        if velocidad > 0:
            self.velocidad = velocidad
