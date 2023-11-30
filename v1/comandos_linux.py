import subprocess
import psutil


def cpu(pid):
    comando = f"ps -o psr --pid {pid} | tail -n 1"
    resultado = subprocess.run(comando, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return int(resultado.stdout)

def porcentaje_cpu(pid):
    comando = f"ps -o %cpu --pid {pid} | tail -n 1"
    resultado = subprocess.run(comando, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(resultado.stdout)

def pid():
    return psutil.Process().pid  

def update_info_cpu(pidd):
        
        n_cpu = cpu(pidd)
        per_cpu = porcentaje_cpu(pidd)

        return n_cpu, per_cpu

