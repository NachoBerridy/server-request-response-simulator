import matplotlib.pyplot as plt
import seaborn as sns


def graficador(df, NUM_SERVERS, LAMBDA, MU, CANTIDAD_CLIENTES):
    sns.set_theme(style='whitegrid')
    sns.color_palette('Set2')

    # Crear una figura con 2 filas y 2 columnas
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Distribución de tiempo de llegada
    sns.histplot(
        df['Tiempos entre llegadas'],
        kde=True,
        bins=20,
        color='b',
        ax=axes[0, 0]
    )
    axes[0, 0].set_title('Histograma de tiempo entre llegadas')
    axes[0, 0].set_xlabel('Tiempo entre llegadas (ms)')
    axes[0, 0].set_ylabel('Frecuencia')
    axes[0, 0].axvline(x=1/LAMBDA, color='r', linestyle='--', label='1/λ')
    axes[0, 0].axvline(
        x=df['Tiempos entre llegadas'].mean(),
        color='g',
        linestyle='--',
        label='Promedio'
    )
    axes[0, 0].legend()

    # Distribución de tiempo de servicio
    service_time = df['Tiempo de servicio']
    sns.histplot(service_time, kde=True, bins=20, color='g', ax=axes[0, 1])
    axes[0, 1].set_title('Histograma de tiempo de servicio')
    axes[0, 1].set_xlabel('Tiempo de servicio (ms)')
    axes[0, 1].set_ylabel('Frecuencia')
    axes[0, 1].axvline(x=1/MU, color='r', linestyle='--', label='1/μ')
    axes[0, 1].axvline(
        x=service_time.mean(),
        color='g', linestyle='--',
        label='Promedio'
    )
    axes[0, 1].legend()

    # Distribución de tiempo de espera
    wait_time = df['Tiempo de espera']
    sns.histplot(wait_time, kde=True, bins=20, color='y', ax=axes[1, 0])
    axes[1, 0].set_title('Histograma de tiempo de espera')
    axes[1, 0].set_xlabel('Tiempo de espera (ms)')
    axes[1, 0].set_ylabel('Frecuencia')
    axes[1, 0].axvline(
        x=wait_time.mean(),
        color='r',
        linestyle='--',
        label='Promedio'
    )
    axes[1, 0].legend()

    # Tiempos de ocio por servidor
    sns.histplot(
        df['Tiempo de ocio'],
        kde=True,
        bins=20,
        color='c',
        ax=axes[1, 1]
    )
    axes[1, 1].set_title('Tiempos de ocio por servidor')
    axes[1, 1].set_xlabel('Tiempo de ocio (ms)')
    axes[1, 1].set_ylabel('Frecuencia')
    axes[1, 1].axvline(
        x=df['Tiempo de ocio'].mean(),
        color='r',
        linestyle='--',
        label='Promedio'
    )
    axes[1, 1].legend()

    # Ajustar los espacios entre subplots para una mejor
    # visualización y añadir título
    fig.suptitle(
        f'''Simulación de un sistema de cola con {NUM_SERVERS} servidores
        1/λ = {round(1/LAMBDA, 2)} ms y 1/μ = {round(1/MU, 2)} ms''',
        fontsize=16
    )
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
