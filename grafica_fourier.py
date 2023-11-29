from time import sleep
import numpy as np
import matplotlib.pyplot as plt

class GraficaFourier:
    
    def __init__(self):
        
        self.fig, self.ax = plt.subplots(figsize=(10, 3), dpi=100)
        self.line, = self.ax.plot([], [])

        self.ax.set_xlim(0, 50) 
        self.ax.set_ylim(0, 1)

        self.x_values = []
        self.y_values = []

        self.ventana = [0]*100
    

    

    def update_plot(self, y):

        if len(self.line.get_xdata()) == 0:
            self.x_values = np.arange(50)

        self.y_values = y
        self.line.set_data(self.x_values, self.y_values)

  


    
