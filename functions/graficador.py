import numpy as np
import pandas as pd
from tabulate import tabulate
import queue
import threading
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats



def graficador(df, estadisticas, NUM_SERVERS, LAMBDA, MU, CANTIDAD_CLIENTES):
    # Crear array con los tiempos de espera ordenados
    tiempos_espera = np.sort(df["Tiempo de espera"].values)

    # Crear un array con el tiempo de servicio ordenado
    tiempos_servicio = np.sort(df["Tiempo de servicio"].values)

    # Crear un DataFrame nuevo por cada servidor
    df_servidores = [df[df["Servidor"] == f"Servidor {i}"].copy() for i in range(NUM_SERVERS)]

    # Calcular el tiempo total de simulación
    tiempo_total = df["Tiempo de salida"].max()
    # Calcular el tiempo de espera promedio
    tiempo_Espera_promedio = df["Tiempo de espera"].mean()
    # Calcular el tiempo de servicio promedio
    tiempo_Servicio_promedio = df["Tiempo de servicio"].mean()
    # Calcular el tiempo de ocio promedio
    tiempo_Ocio_promedio = df["Tiempo de ocio"].mean()

    # Calcular el tiempo de espera máximo
    tiempo_Espera_maximo = df["Tiempo de espera"].max()
    # Calcular el tiempo de servicio máximo
    tiempo_Servicio_maximo = df["Tiempo de servicio"].max()
    # Calcular el tiempo de ocio máximo
    tiempo_Ocio_maximo = df["Tiempo de ocio"].max()

    # Calcular el tiempo de espera mínimo
    tiempo_Espera_minimo = df["Tiempo de espera"].min()
    # Calcular el tiempo de servicio mínimo
    tiempo_Servicio_minimo = df["Tiempo de servicio"].min()
    # Calcular el tiempo de ocio mínimo
    tiempo_Ocio_minimo = df["Tiempo de ocio"].min()

    # Crear un diccionario con los datos de la simulación
    datos_simulacion = {
        "Tiempo total": tiempo_total,
        "Tiempo de espera promedio": tiempo_Espera_promedio,
        "Tiempo de servicio promedio": tiempo_Servicio_promedio,
        "Tiempo de ocio promedio": tiempo_Ocio_promedio,
        "Tiempo de espera máximo": tiempo_Espera_maximo,
        "Tiempo de servicio máximo": tiempo_Servicio_maximo,
        "Tiempo de ocio máximo": tiempo_Ocio_maximo,
        "Tiempo de espera mínimo": tiempo_Espera_minimo,
        "Tiempo de servicio mínimo": tiempo_Servicio_minimo,
        "Tiempo de ocio mínimo": tiempo_Ocio_minimo,
    }

    # Convertir el diccionario en un DataFrame
    df_simulacion = pd.DataFrame(datos_simulacion, index=[0])

    # Declarar la variable espera_servidores
    espera_servidores = [0] * NUM_SERVERS  # Inicializar con ceros

    # Para cada DataFrame de servidor, agregar una columna que calcula el tiempo en espera
    for i in range(NUM_SERVERS):
        df_servidores[i] = df_servidores[i].assign(
            Servidor_en_espera=(df_servidores[i]['Tiempo de inicio'].shift(-1) - df_servidores[i]['Tiempo de salida'])
            .fillna(0)
            .apply(lambda x: max(0, x))
        )

        # Calcular el tiempo total de espera del servidor
        espera_servidores[i] = df_servidores[i]['Servidor_en_espera'].sum()

    # Calcular el tiempo total de cada servidor (incluyendo tiempo de ocio)
    tiempo_total_servidores = [df_servidores[i]['Tiempo de salida'].max() for i in range(NUM_SERVERS)]

    # Ajustar el tiempo total del servidor si es menor que el tiempo total de la simulación
    tiempo_total_simulacion = df["Tiempo de salida"].max()
    for i in range(NUM_SERVERS):
        # Agregar tiempo de ocio inicial del servidor
        tiempo_total_servidores[i] = tiempo_total_servidores[i] - df_servidores[i].iloc[0]['Tiempo de ocio']

        # Agregar tiempo de ocio al final de la simulación si el servidor no está ocupado
        if tiempo_total_servidores[i] < tiempo_total_simulacion:
            tiempo_total_servidores[i] = tiempo_total_simulacion

    # Calcular el porcentaje de espera de cada servidor
    porcentaje_espera_servidores = [espera_servidores[i] / tiempo_total_servidores[i] * 100 for i in range(NUM_SERVERS)]

    # Calcular el porcentaje de uso de cada servidor
    porcentaje_uso_servidores = [100 - porcentaje_espera_servidores[i] for i in range(NUM_SERVERS)]


    # Calcular el tiempo de ocio total de cada servidor
    tiempo_ocio_servidores = [df_servidores[i]["Tiempo de ocio"].sum() for i in range(NUM_SERVERS)]

    # Crear un diccionario con los datos de los servidores
    data_servidores = {
        "Servidor": [f"Servidor {i+1}" for i in range(NUM_SERVERS)],
        "Tiempo en espera": [float("{:.2f}".format(espera_servidores[i])) for i in range(NUM_SERVERS)],
        "Porcentaje de espera": [float("{:.2f}".format(porcentaje_espera_servidores[i])) for i in range(NUM_SERVERS)],
        "Porcentaje de uso": [float("{:.2f}".format(porcentaje_uso_servidores[i])) for i in range(NUM_SERVERS)],
        "Tiempo de ocio": [float("{:.2f}".format(tiempo_ocio_servidores[i])) for i in range(NUM_SERVERS)],
        "Cantidad de clientes atendidos": [df_servidores[i]["Cliente"].count() for i in range(NUM_SERVERS)],
    }

    # Convertir el diccionario en un DataFrame
    df_data_servidores = pd.DataFrame(data_servidores)
    # Imprimir los datos de los servidores
    print("\nMétricas de los servidores:")
    print(tabulate(df_data_servidores, headers="keys", tablefmt="pretty"))

    # Crear un DataFrame con los parámetros del sistema
    df_parametros = pd.DataFrame(columns=['Cantidad de clientes generados', 'Cantidad de servidores', '1/μ', '1/λ'])
    df_parametros.loc[0] = [CANTIDAD_CLIENTES, NUM_SERVERS, 1/MU, 1/LAMBDA]

    # Guardar todos los DataFrames en un archivo Excel, cada uno en una hoja diferente
    name = f'Resultados-({LAMBDA}-{MU}).xlsx'
    with pd.ExcelWriter(name, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Clientes', index=False)
        for i in range(NUM_SERVERS):
            df_servidores[i].to_excel(writer, sheet_name=f'Servidor {i+1}', index=False)
        df_simulacion.to_excel(writer, sheet_name='Datos de la simulación', index=False)
        df_data_servidores.to_excel(writer, sheet_name='Datos de los servidores', index=False)
        df_parametros.to_excel(writer, sheet_name='Parámetros del sistema', index=False)

    # ---- Gráfica de los tiempos de servicio en comparación con la exponencial teórica ----#
    tiempos_de_servicio = df["Tiempo de servicio"]

    plt.figure(figsize=(12, 6))
    plt.hist(tiempos_de_servicio, bins=30, density=True, alpha=0.6, color='g', label='Datos observados')
    if np.mean(tiempos_de_servicio) != 0:
        lambda_estimada = 1 / np.mean(tiempos_de_servicio)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.expon.pdf(x, scale=1 / lambda_estimada)
        plt.plot(x, p, 'k', linewidth=2, label=f'Distribución exponencial teórica\n($\\lambda$={lambda_estimada:.2f})')
    plt.xlabel("Tiempo de servicio")
    plt.ylabel("Densidad")
    plt.title("Distribución de los tiempos de servicio con envolvente exponencial")
    plt.legend()
    plt.show()

    # ---- Gráfica de los tiempos de llegada en comparación con la exponencial teórica ----#
    tiempos_de_llegada = estadisticas["Tiempo de llegada"]

    plt.figure(figsize=(12, 6))
    plt.hist(tiempos_de_llegada, bins=30, density=True, alpha=0.6, color='g', label='Datos observados')

    lambda_estimada = 1 / np.mean(tiempos_de_llegada)

    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.expon.pdf(x, scale=1 / lambda_estimada)
    plt.plot(x, p, 'k', linewidth=2, label=f'Distribución exponencial teórica\n($\\lambda$={lambda_estimada:.2f})')

    plt.xlabel("Tiempo de llegada")
    plt.ylabel("Densidad")
    plt.title("Distribución de los tiempos de llegada con envolvente exponencial")
    plt.legend()
    plt.show()

    # ---- Gráfica de Tiempos de Espera ----#
    plt.figure(figsize=(12, 6))
    plt.hist(tiempos_espera, bins=30, density=True, alpha=0.6, color='b')
    plt.axvline(tiempo_Espera_promedio, color='r', linestyle='dashed', linewidth=2)
    plt.xlabel("Tiempo de espera")
    plt.ylabel("Densidad")
    plt.title("Distribución de los tiempos de espera")
    plt.legend(["Tiempo de espera promedio", "Datos observados"])
    plt.show()

    # ---- Gráfica de Tiempo de Ocio por Servidor ----#
    # plt.figure(figsize=(12, 6))
    # for i in range(NUM_SERVERS):
    #     sns.kdeplot(df_servidores[i]["Tiempo de ocio"], label=f"Servidor {i+1}")
    # plt.xlabel("Tiempo de ocio")
    # plt.ylabel("Densidad")
    # plt.title("Distribución de los tiempos de ocio por servidor")
    # plt.legend()
    # plt.show()
    

    # ---- Gráfica de Porcentaje de Uso de Servidor ----#
    plt.figure(figsize=(12, 6))
    sns.barplot(x="Servidor", y="Porcentaje de uso", data=df_data_servidores)
    plt.xlabel("Servidor")
    plt.ylabel("Porcentaje de uso")
    plt.title("Porcentaje de uso por servidor")
    plt.show()

    # ---- Gráfica de Distribución de Clientes Atendidos por Servidor ----#
    plt.figure(figsize=(12, 6))
    sns.barplot(x="Servidor", y="Cantidad de clientes atendidos", data=df_data_servidores)
    plt.xlabel("Servidor")
    plt.ylabel("Cantidad de clientes atendidos")
    plt.title("Cantidad de clientes atendidos por servidor")
    plt.show()
