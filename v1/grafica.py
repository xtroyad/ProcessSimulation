from time import sleep
import numpy as np
import matplotlib.pyplot as plt

class Grafica:

    def __init__(self):
  
        self.fig, self.ax = plt.subplots(figsize=(10, 3), dpi=100)
        self.line, = self.ax.plot([], [])

        self.ax.set_xlim(0, 100)  # Inicializar con un límite de 200
        self.ax.set_ylim(-5, 5)

        self.x_values = []
        self.y_values = []


    # Función para actualizar la gráfica con un nuevo valor
    def update_plot(self, y):
        if len(self.line.get_xdata()) == 0:
            self.x_values = np.array([0])
        else:
            self.x_values = np.append(self.line.get_xdata(), self.line.get_xdata()[-1] + 1)
        
        self.y_values = np.append(self.line.get_ydata(), y)
        self.line.set_data( self.x_values, self.y_values)
        
        # Ajustar el límite del eje x para mantener un intervalo de 100
        if  self.x_values[-1] > 100:
            self.ax.set_xlim( self.x_values[-1] - 100,  self.x_values[-1])
        else:
            self.ax.set_xlim(0, 100)

    def update_plot2(self, x, y):
        # Agregar el nuevo punto (x, y)
        self.x_values = np.append(self.line.get_xdata(), x)
        self.y_values = np.append(self.line.get_ydata(), y)

        self.line.set_data(self.x_values, self.y_values)

        # Ajustar el límite del eje x para mantener un intervalo de 100
        if self.x_values[-1] > 100:
            self.ax.set_xlim(self.x_values[-1] - 100, self.x_values[-1])
        else:
            self.ax.set_xlim(0, 100)  

    def detener_grafica(self):
        # Detener la ejecución para ver la gráfica
        plt.ioff()
        plt.show()


    
