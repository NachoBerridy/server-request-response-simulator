# import numpy as np
# import pandas as pd
# from tabulate import tabulate
# import queue
# import threading
import matplotlib.pyplot as plt
import seaborn as sns


def graficador(df, NUM_SERVERS, LAMBDA, MU, CANTIDAD_CLIENTES):

    sns.set_theme(style='whitegrid')
    sns.color_palette('Set2')

    # Distribución de tiempo de llegada
    sns.histplot(
        df['Tiempos entre llegadas'], 
        kde=True, 
        bins=20,
        color='b'
    )
    plt.title('Histograma de tiempo entre llegadas')
    plt.xlabel('Tiempo entre llegadas (ms)')
    plt.ylabel('Frecuencia')
    # Añadir valores de lambda y valor promedio
    plt.axvline(x=1/LAMBDA, color='r', linestyle='--', label='1/λ')
    plt.axvline(
        x=df['Tiempos entre llegadas'].mean(),
        color='g', linestyle='--',
        label='Promedio')
    plt.legend()
    plt.show()

    # Distribución de tiempo de servicio
    service_time = df['Tiempo de servicio']
    sns.histplot(service_time, kde=True, bins=20, color='g')
    plt.title('Histograma de tiempo de servicio')
    plt.xlabel('Tiempo de servicio (ms)')
    plt.ylabel('Frecuencia')
    # Añadir etiqueta con el valor de mu y valor promedio
    plt.axvline(x=1/MU, color='r', linestyle='--', label='1/μ')
    plt.axvline(
        x=service_time.mean(),
        color='g',
        linestyle='--',
        label='Promedio')
    plt.legend()
    plt.show()

    # Distribución de tiempo de espera
    wait_time = df['Tiempo de espera']
    sns.histplot(wait_time, kde=True, bins=20, color='y')
    plt.title('Histograma de tiempo de espera')
    plt.xlabel('Tiempo de espera (ms)')
    plt.ylabel('Frecuencia')
    # Añadir valor promedio
    plt.axvline(
        x=wait_time.mean(),
        color='r',
        linestyle='--',
        label='Promedio')
    plt.legend()
    plt.show()

    # Tiempos de ocio por servidor
    sns.relplot(
        y='Tiempo de ocio',
        data=df,
        hue='Servidor',
        kind='scatter',
    )
    plt.title('Tiempos de ocio por servidor')
    plt.xlabel('Cliente')
    plt.ylabel('Tiempo de ocio (ms)')
    plt.show()
