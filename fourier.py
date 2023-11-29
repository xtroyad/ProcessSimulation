import numpy as np
import matplotlib.pyplot as plt
from scipy import fft
from time import sleep
import math

from comandos_linux import *

class Fourier:
    def __init__(self, datos_para_calcular, fourier_a_iu , barrera_fourier, barrera_fourier_fin, posicion_cpu, pids, porcen_cpu):
        self.fourier_a_iu = fourier_a_iu
        self.ventana = [0]*100
        self.datos_para_calcular = datos_para_calcular

        self.porcen_cpu = porcen_cpu
        self.posicion_cpu = posicion_cpu
        self.pids = pids

        self.barrera_fourier = barrera_fourier
        self.barrera_fourier_fin = barrera_fourier_fin

    def update_info_cpu(self):
        self.pids[1] = pid()
        self.posicion_cpu[1] = cpu(self.pids[1])
        self.porcen_cpu[1] = porcentaje_cpu(self.pids[1])

    def iniciar(self):

        ventana = []
        while(True):
            self.barrera_fourier.wait()

            self.update_info_cpu()

            dato = self.datos_para_calcular.get()
            ventana.append(dato)
            if len(ventana) == 100:
              
                l_fourier = self.fourier(ventana)
                self.fourier_a_iu.put(l_fourier)
                ventana = []

            self.barrera_fourier_fin.wait()
    

    def fourier(self, y):
        n = len(y)
        Y = np.fft.fft(y) / n
        Y = Y[range(int(n/2))]
        return np.abs(Y)

       


   