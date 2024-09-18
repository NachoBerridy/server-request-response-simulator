import pandas as pd


# Se busca extraer medidas de rendimiento de la simulación

# Porcentaje de uso de cada servidor

def server_usage(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the server usage percentage for each server.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the simulation data.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the server usage percentage for each server.
    """
    # Se obtiene el tiempo de ocio total de cada servidor
    ocio_total = data.groupby('Servidor')['Tiempo de ocio'].sum()
    # Se obtiene el tiempo total de la simulación
    tiempo_total = data['Tiempo de salida'].max()
    # Se calcula el tiempo de uso de cada servidor
    uso = tiempo_total - ocio_total
    # Se calcula el porcentaje de uso de cada servidor
    uso_porcentaje = 100 * uso / tiempo_total
    return uso_porcentaje

# Tiempo promedio de espera en la cola


def average_waiting_time(data: pd.DataFrame) -> float:
    """
    Calculate the average waiting time in the queue.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the simulation data.

    Returns
    -------
    float
        Average waiting time in the queue.
    """
    return data['Tiempo de espera'].mean()

# Tiempo promedio de servicio


def average_service_time(data: pd.DataFrame) -> float:
    """
    Calculate the average service time.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the simulation data.

    Returns
    -------
    float
        Average service time.
    """
    return data['Tiempo de servicio'].mean()


def analyze_simulation(data: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze the simulation data.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the simulation data.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the analysis results.
    """
    return pd.DataFrame({
        'Porcentaje de uso': server_usage(data),
        'Tiempo promedio de espera en la cola': average_waiting_time(data),
        'Tiempo promedio de servicio': average_service_time(data)
    })
