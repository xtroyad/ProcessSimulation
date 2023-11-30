from multiprocessing import current_process
import numpy as np
import matplotlib.pyplot as plt
from scipy import fft
from time import sleep
import math

from comandos_linux import *

class Fourier:
    def __init__(self, cola_medidas, cola_datos_fourier, pids, inicio_iu):
        
        self.inicio_iu = inicio_iu

        self.pids = pids

        self.cola_medidas = cola_medidas
        self.cola_datos_fourier = cola_datos_fourier

    def iniciar(self, fin_proceso):

        ventana = []
        self.pids[2] = pid()
        
        self.inicio_iu.wait()

        while(not fin_proceso.is_set()):
            
            #self.pids[2], self.n_cpu[2], self.per_cpu[2] = update_info_cpu()
            if not self.cola_medidas.empty():

                medida = self.cola_medidas.get()
                if len(ventana) > 0 and medida == ventana[-1]:
                    pass
                else:
                    ventana.append(medida)

                    if len(ventana) == 200:
                        l_fourier = self.fourier(ventana)
                        self.cola_datos_fourier.put(l_fourier)
                        ventana = []

        print("Proceso Fourier OFF")
    def fourier(self, y):
        n = len(y)
        Y = np.fft.fft(y) / n
        Y = Y[range(int(n/2))]
        return np.abs(Y)

       


   