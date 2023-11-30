from multiprocessing import current_process
import numpy as np
import matplotlib.pyplot as plt
from scipy import fft
from time import sleep
import math
from scipy.signal import argrelextrema

from comandos_linux import *

class Fourier:
    def __init__(self, cola_medidas, cola_datos_fourier, pids, inicio_iu, velocidad):
        
        self.velocidad = velocidad

        self.inicio_iu = inicio_iu

        self.pids = pids

        self.cola_medidas = cola_medidas
        self.cola_datos_fourier = cola_datos_fourier

    def iniciar(self, fin_proceso):

        ventana = []
        self.pids[2] = pid()
        
        self.inicio_iu.wait()
        val = 0
        while(True):
            
            #self.pids[2], self.n_cpu[2], self.per_cpu[2] = update_info_cpu()
            if not self.cola_medidas.empty():

                medida = self.cola_medidas.get()
                if len(ventana) > 0 and medida == ventana[-1]:
                    pass
                else:
                    ventana.append(medida)

                    if len(ventana) == 100:
                        l_fourier = self.fourier(ventana)
                        self.cola_datos_fourier.put(l_fourier)
                        ventana = []


            val = val +1

    

    def fourier(self, y):
        n = len(y)
        Y = np.fft.fft(y) / n
        Y = Y[range(int(n/2))]
        result = np.abs(Y)
        self.modificar_velocidad(result)

        return result

    def modificar_velocidad(self, y):

        indices_maximos = argrelextrema(y, np.greater)[0]
        puntos_maximos = y[indices_maximos]

        # Imprime o devuelve los resultados
        print("Índices de puntos máximos:", indices_maximos)
        print("Valores de puntos máximos:", puntos_maximos)

        reducido = False
        for (i, j) in zip(indices_maximos, puntos_maximos):
           
            if(j<0.2 and i > 20):
                self.velocidad.value = self.velocidad.value - 5
                reducido = True
                
                break

        if not reducido:
            self.velocidad.value = self.velocidad.value + 5


        