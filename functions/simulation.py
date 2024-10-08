import threading
import time
import pandas as pd
from classes.simulator.Server import Server  # Importa la clase Server
from classes.number_generators.Generator import Generator
from queue import Queue

# Variables globales
datos_clientes = []  # Lista para almacenar datos de los clientes
estadisticas = []  # Lista para almacenar estadísticas


def simulate(generator: Generator, LAMBDA, MU, CANTIDAD_CLIENTES, NUM_SERVERS):
    global datos_clientes, estadisticas

    # Crear una cola compartida para todos los servidores
    cola_clientes = Queue()

    # Crear instancias de la clase Server para cada servidor
    servidores =\
        [Server(f'Servidor {i}', cola_clientes) for i in range(NUM_SERVERS)]

    # Crear una lista de hilos para ejecutar el método server de cada servidor
    hilos_servidores =\
        [threading.Thread(target=servidor.server) for servidor in servidores]

    # Iniciar cada hilo de servidor
    for hilo in hilos_servidores:
        hilo.start()

    clientes_generados = 0
    tiempo_simulacion = 0

    # Generar clientes y ponerlos en la cola
    while clientes_generados < CANTIDAD_CLIENTES:
        # Genera un tiempo de demora exponencial
        tiempo_demora = generator.exponential(LAMBDA)
        # Genera un tiempo de servicio exponencial
        tiempo_servicio = generator.exponential(MU)

        time.sleep(tiempo_demora * 0.001)  # Retraso entre llegadas
        tiempo_simulacion += tiempo_demora  # Actualiza el tiempo de simulación
        llegada = tiempo_simulacion
        nombre_cliente = f'Cliente {clientes_generados}'

        # Agrega el cliente a la cola
        # compartida para que cualquier servidor lo atienda
        cola_clientes.put(
            (nombre_cliente, llegada, tiempo_servicio, tiempo_demora))
        clientes_generados += 1

    # Esperar a que todos los clientes sean atendidos
    cola_clientes.join()

    # Finalizar la simulación para cada servidor
    for _ in range(NUM_SERVERS):
        # Colocar un None en la cola para finalizar cada servidor
        cola_clientes.put(None)

    # Esperar que todos los hilos terminen
    for hilo in hilos_servidores:
        hilo.join()

    # Recopilar los datos de cada servidor
    for servidor in servidores:
        datos_clientes.extend(servidor.datos_clientes)
        estadisticas.extend(servidor.estadisticas)

    # Crear DataFrames con los datos recopilados
    df = pd.DataFrame(datos_clientes)\
        .sort_values(by="Tiempo de llegada")\
        .reset_index(drop=True)
    estadisticas_df = pd.DataFrame(estadisticas)\
        .sort_values(by="Tiempo de llegada")\
        .reset_index(drop=True)

    return df, estadisticas_df  # Retorna los DataFrames resultantes
