from multiprocessing import Process, Array, Value, Manager, Barrier, Queue
from time import sleep
from carrito import Carrito
from iu import IU
from fourier import Fourier
from time import sleep
if __name__ == '__main__':

    # Colas de comunicación
    medidas = Queue()
    recorrido = Queue()
    datos_para_fourier = Queue()
    fourier_a_iu = Queue()
    # Barreras de sincronización
    barrera_principal = Barrier(2)
    barrera_principal_fin = Barrier(2)

    barrera_fourier = Barrier(2)
    barrera_fourier_fin = Barrier(2)
    # Datos compartidos entre procesos
    recorrido_saltado = Array("i", (0, 0))
    # Posiciones en CPU
    posicion_cpu = Array("i", (0, 0, 0))

    # Posiciones en PID
    pids = Array("i", (0, 0, 0))
    
    # Posiciones en PID
    porcen_cpu = Array("d", (0, 0, 0))

    carrito = Carrito(recorrido_saltado, medidas, recorrido, datos_para_fourier, barrera_principal, barrera_principal_fin, barrera_fourier, barrera_fourier_fin, posicion_cpu, pids, porcen_cpu)
    proceso_carrito = Process(target=carrito.iniciar_sensor)
    proceso_carrito.start()

    fourier = Fourier(datos_para_fourier, fourier_a_iu, barrera_fourier, barrera_fourier_fin, posicion_cpu, pids, porcen_cpu)
    proceso_fourier = Process(target=fourier.iniciar)
    proceso_fourier.start()

    iu = IU(medidas, recorrido, fourier_a_iu, barrera_principal, barrera_principal_fin, recorrido_saltado, barrera_fourier_fin, posicion_cpu, pids, porcen_cpu)
    iu.iniciar_iu()

    proceso_carrito.join()
    proceso_iu.join()
    proceso_fourier.join()


