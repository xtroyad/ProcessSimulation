from comandos_linux import *
from fourier import Fourier
from iu import IU
from vehiculo import Vehiculo
from multiprocessing import Queue, Process, Array, Barrier, Event, Value

if __name__ == '__main__':

    # Colas
    cola_medidas = Queue()
    cola_medidas_iu = Queue()
    cola_datos_fourier = Queue()
    # Variables del sistema compartido
    pids = Array("i",(0, 0, 0, 0))
    velocidad = Value("i", 40)

    # Barrera de inicio
    inicio_iu = Barrier(4)

    # Evento finalizar 
    fin_procesos = Event()


    fourier = Fourier(cola_medidas, cola_datos_fourier, pids, inicio_iu, velocidad)
    proceso_fourier = Process(target=fourier.iniciar, args=(fin_procesos,))
    proceso_fourier.start()

    iu = IU(cola_datos_fourier, cola_medidas_iu, pids,inicio_iu)
    proceso_iu = Process(target=iu.iniciar_iu, args=(fin_procesos,))
    proceso_iu.start()

    pids[0] = pid()
    carro = Vehiculo(cola_medidas, cola_medidas_iu, pids, inicio_iu, fin_procesos, velocidad)
    
    carro.iniciar()

    proceso_fourier.join()
    proceso_iu.join()