# Importaciones estándar para funcionalidades básicas y análisis estadístico
import threading          # Soporte para hilos en Python
import queue              # Implementación de colas
import pandas as pd       # Análisis y manipulación de datos tabulares

from functions.parameters import find_good_parameters
# from functions.graficador import graficador
from functions.graficador_dos import graficador

from functions.simulation import simulate
from classes.number_generators.Generator import Generator

#Definición de los parámetros del sistema
SEMILLA = 42 #Valor semilla
LAMBDA = 75/100 #Tasa de llegada de clientes (clientes por unidad de tiempo)
MU = 30/100 #Tasa de servicio (clientes por unidad de tiempo)
CANTIDAD_CLIENTES = 1000  # Total de clientes
#TIEMPO_ENTRE_LLEGADAS = 15  # Tiempo promedio entre llegadas (1/λ)
#TIEMPO_SERVICIO = 20  # Tiempo promedio de servicio (1/μ)
NUM_SERVERS = 3   # Número de servidores
UNIDAD_TIEMPO = 'milisegundos'  # Unidad de tiempo (segundos)
CLIENTES_MAX_EN_SIMULTANEO = 3

#Variables globales
cola_clientes = queue.Queue()  # Cola para los clientes
datos_clientes = []  # Lista para almacenar datos de los clientes
tiempo_simulacion = 0  # Contador de tiempo simulado
estadisticas = []  # Lista para almacenar estadísticas
servidor_tiempos = {}  # Diccionario para almacenar los tiempos de los servidores
semaforo_cola = threading.Semaphore()  # Semáforo para manejar la cola de clientes


def main():
    print("\nSimulación de sistema de colas M/M/3 con generador congruencial")
    print("\nIntegrantes del grupo:")
    print("\n- Berridy Ignacio")
    print("\n- Olcoz Ignacio")
    print("\n- Rosales Cristian")

    # Selección del generador
    while True:
        print("\nMenú de selección de generador:")
        print("1. Generador Congruencial Mixto")
        print("2. Generador Congruencial Multiplicativo")
        print("0. Salir")

        try:
            eleccion_generador = int(input("Ingrese su selección (0-2): "))
            if 0 <= eleccion_generador <= 2:
                break
            print("Opción inválida. Intente nuevamente.")
        except ValueError:
            print("Entrada no válida. Ingrese un número entero (0-2).")

    if eleccion_generador == 0:
        print("Saliendo del programa...")
        return

    if eleccion_generador in [1, 2]:
        tipo_generador = 'mixto' if eleccion_generador == 1 else 'multiplicativo'
        try:
            print("Buscando parámetros adecuados...")
            if tipo_generador == 'mixto':
                a, b, m = find_good_parameters(SEMILLA, tipo_generador)
                df_parameters = pd.DataFrame({'a': [a], 'b': [b], 'm': [m]})
                generator = Generator(seed=SEMILLA, a=a, b=b, m=m)
            else:
                a, m = find_good_parameters(SEMILLA, tipo_generador)
                df_parameters = pd.DataFrame({'a': [a], 'm': [m]})
                generator = Generator(seed=SEMILLA, a=a, b=0, m=m)
            print('\nParámetros seleccionados:')
            print(df_parameters)
        except ValueError as e:
            print(e)
            return

    else:
        print("\nError.")
        return

    print('\nIniciando simulación...')
    resultado_df, estadisticas =\
        simulate(generator, LAMBDA, MU, CANTIDAD_CLIENTES, NUM_SERVERS)
    print("\nResumen de los datos de los clientes:")
    # print(resultado_df.describe())
    print(resultado_df)

    graficador(resultado_df, estadisticas, NUM_SERVERS, LAMBDA, MU, CANTIDAD_CLIENTES)

    print('\nFin de programa')



if __name__ == "__main__":
  main()