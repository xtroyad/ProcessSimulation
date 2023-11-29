from time import sleep
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
from multiprocessing import Process
from grafica import Grafica
from grafica_fourier import GraficaFourier
import psutil

from comandos_linux import *

class IU:
    def __init__(self, medidas, recorrido, fourier, barrera_principal, barrera_principal_fin, recorrido_saltado, barrera_fourier_fin, posicion_cpu, pids, porcen_cpu):
        self.barrera_principal = barrera_principal
        self.barrera_principal_fin = barrera_principal_fin

        self.porcen_cpu = porcen_cpu
        self.posicion_cpu = posicion_cpu
        self.pids = pids

        self.fourier_a_iu = fourier
        self.medidas = medidas
        self.recorrido = recorrido

        self.recorrido_saltado = recorrido_saltado

        #-------------------------------------------
        self.ventana = tk.Tk()
        self.ventana.title("Simulador")

        # Creamos los FRAMES principales
        frame_izquierdo = tk.Frame(self.ventana, bg="white", width=50, height=50)
        frame_derecho = tk.Frame(self.ventana, bg="white", width=50, height=50)
        frame_izquierdo.grid(row=0, column=0)
        frame_derecho.grid(row=0, column=1)

        # Crear sub-frames para los datos de los procesos
        self.frame_carrito = tk.Frame(frame_izquierdo, height=50, bg="white")
        self.frame_fourier = tk.Frame(frame_izquierdo, height=50, bg="red")
        self.frame_iu= tk.Frame(frame_izquierdo, height=50, bg="white")

        self.frame_carrito.pack(fill=tk.X)
        self.frame_fourier.pack(fill=tk.X)
        self.frame_iu.pack(fill=tk.X)

        # Agregar etiquetas a cada sub-frame
        self.label_carrito = tk.Label(self.frame_carrito, height=2, text="Datos del Carrito", bg="white")
        self.label_carrito.pack(fill=tk.X)
        self.label_carrito_cpu = tk.Label(self.frame_carrito, height=2, text="Nº CPU:", bg="white")
        self.label_carrito_cpu.pack(fill=tk.X)
        self.label_carrito_cpu_porcentaje = tk.Label(self.frame_carrito, height=2, text="% CPU:", bg="white")
        self.label_carrito_cpu_porcentaje.pack(fill=tk.X)
        self.label_carrito_pid = tk.Label(self.frame_carrito, height=2, text="PID:", bg="white")
        self.label_carrito_pid.pack(fill=tk.X)

        self.label_fourier = tk.Label(self.frame_fourier, height=2, text="Datos de Fourier", bg="orange")
        self.label_fourier.pack(fill=tk.X)
        self.label_fourier_cpu = tk.Label(self.frame_fourier, height=2, text="Nº CPU:", bg="orange")
        self.label_fourier_cpu.pack(fill=tk.X)
        self.label_fourier_cpu_porcentaje = tk.Label(self.frame_fourier, height=2, text="% CPU:", bg="orange")
        self.label_fourier_cpu_porcentaje.pack(fill=tk.X)
        self.label_fourier_pid = tk.Label(self.frame_fourier, height=2, text="PID:", bg="orange")
        self.label_fourier_pid.pack(fill=tk.X)

        self.label_iu = tk.Label(self.frame_iu, height=2, text="Datos de IU", bg="white")
        self.label_iu.pack(fill=tk.X)
        self.label_iu_cpu = tk.Label(self.frame_iu, height=2, text="Nº CPU:", bg="white")
        self.label_iu_cpu.pack(fill=tk.X)
        self.label_iu_cpu_porcentaje = tk.Label(self.frame_iu, height=2, text="% CPU:", bg="white")
        self.label_iu_cpu_porcentaje.pack(fill=tk.X)
        self.label_iu_pid = tk.Label(self.frame_iu, height=2, text="PID:", bg="white")
        self.label_iu_pid.pack(fill=tk.X)

        # Crear sub-frames para las gráficas
        self.frame_grafica_real = tk.Frame(frame_derecho, bg="white")
        self.frame_grafica_medidas = tk.Frame(frame_derecho, bg="white")
        self.frame_grafica_fourier = tk.Frame(frame_derecho, bg="white")

        self.frame_grafica_real.grid(row=0, column=0, sticky="nsew")
        self.frame_grafica_medidas.grid(row=1, column=0, sticky="nsew")
        self.frame_grafica_fourier.grid(row=2, column=0, sticky="nsew")

        # Crear instancias de las clases Grafica
        self.grafica_real = Grafica()
        self.grafica_medidas = Grafica()
        self.grafica_fourier = GraficaFourier()

        # Cambas
        self.ncanvas = [None, None, None]

        # Añadir la primera gráfica
        self.agregar_grafica(self.frame_grafica_real, self.grafica_real, 0)

        # Añadir la segunda gráfica
        self.agregar_grafica(self.frame_grafica_medidas, self.grafica_medidas, 1)

        # Añadir la tercera gráfica
        self.agregar_grafica(self.frame_grafica_fourier, self.grafica_fourier, 2)

    def cerrar_ventana(self):
        self.ventana.destroy()

    def iniciar_iu(self):

        hilo_iu = threading.Thread(target=self.actualizar)
        hilo_iu.start()
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        self.ventana.mainloop()
        hilo_iu.join()


    def agregar_grafica(self, frame, grafica, i):

        if self.ncanvas[i] is None:
            # Si no hay una gráfica en este índice, crea una nueva
            self.ncanvas[i] = FigureCanvasTkAgg(grafica.fig, master=frame)
            self.ncanvas[i].get_tk_widget().grid(row=0, column=0, sticky="nsew")
        else:
            # Si ya hay una gráfica, simplemente actualiza el Canvas
            self.ncanvas[i].draw()

    def update_info_cpu(self):
        self.pids[2] = pid()
        self.posicion_cpu[2] = cpu(self.pids[2])
        self.porcen_cpu[2] = porcentaje_cpu(self.pids[2])

    def update_label_cpu(self):

        self.label_carrito_cpu.config(text = f"Nº CPU: {self.posicion_cpu[0]}")
        self.label_carrito_cpu_porcentaje.config(text = f"% CPU: {self.porcen_cpu[0]}")
        self.label_carrito_pid.config(text = f"PID: {self.pids[0]}")

        self.label_fourier_cpu.config(text = f"Nº CPU: {self.posicion_cpu[1]}")
        self.label_fourier_cpu_porcentaje.config(text = f"% CPU: {self.porcen_cpu[1]}")
        self.label_fourier_pid.config(text = f"PID: {self.pids[1]}")

        self.label_iu_cpu.config(text = f"Nº CPU: {self.posicion_cpu[2]}")
        self.label_iu_cpu_porcentaje.config(text = f"% CPU: {self.porcen_cpu[2]}") 
        self.label_iu_pid.config(text = f"PID: {self.pids[2]}")


    def actualizar(self):
        
        while True:
            
            self.update_info_cpu()
            self.update_label_cpu()

            self.update_label_cpu()
            self.barrera_principal.wait()

            ini = self.recorrido_saltado[0]
            fin = self.recorrido_saltado[1]

            if ini == fin:
                real = self.recorrido.get()
                self.update_grafica(self.frame_grafica_real, self.grafica_real, real, 0)
            else:
                for i in range (ini,fin+1):
                    real = self.recorrido.get()
                    self.update_grafica(self.frame_grafica_real, self.grafica_real, real, 0)

            medida = self.medidas.get()
            self.update_grafica2(self.frame_grafica_medidas, self.grafica_medidas, medida, 1)

            if not self.fourier_a_iu.empty():
                valores_fourier = self.fourier_a_iu.get()
                self.update_grafica(self.frame_grafica_fourier, self.grafica_fourier, valores_fourier, 2)

            self.barrera_principal_fin.wait()
    def update_grafica2(self, frame, grafica, valor, i):
        grafica.update_plot2(valor[0], valor[1])
        self.agregar_grafica(frame, grafica, i)

    def update_grafica(self, frame, grafica, valor, i):
        grafica.update_plot(valor)
        self.agregar_grafica(frame, grafica, i)




