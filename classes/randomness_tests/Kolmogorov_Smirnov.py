import pandas as pd


class Kolmogorov_Smirnov:
    """
    Realiza la prueba de Kolmogorov-Smirnov para verificar si una secuencia de
    números pseudoaleatorios cumple condición de uniformidad.

    Parámetros:
    - secuencia: Lista de números (secuencia de datos) a evaluar.
    - D_estadistico: Valor del estadístico D para comparar contra
    el valor máximo encontrado en la prueba.
    """

    def __init__(self, D_estadistico):
        self.D_estadistico = D_estadistico

    def test(self, secuencia):

        # Ordena la secuencia de números en orden ascendente
        # para realizar la prueba.
        # No borrar la linea porque causa que se ordene la variable samples.
        secuencia2 = [0] * len(secuencia)
        for i in range(len(secuencia)):
            secuencia2[i] = secuencia[i]

        secuencia2.sort()

        # Obtiene la cantidad total de elementos en la secuencia.
        cantidad = len(secuencia2)

        # Calcula la Función de Distribución Acumulativa Esperada (FDAE)
        # para cada elemento de la secuencia.
        FDAE = [(i + 1) / cantidad for i in range(cantidad)]

        # Encuentra el valor máximo de la diferencia absoluta
        # entre la secuencia y la FDAE.
        maximoValor = max(
            abs(secuencia2[i] - FDAE[i]) for i in range(cantidad))

        # Crea un DataFrame para presentar los resultados de la prueba,
        # incluyendo el valor máximo encontrado y el D estadístico.
        df_ks = pd.DataFrame(columns=['Maximo valor', 'D_estadistico'])
        df_ks.loc[0] = [maximoValor, self.D_estadistico]

        # Imprime los resultados de la prueba de Kolmogorov-Smirnov.
        print('\n RESULTADOS TEST KOLMOGOROV-SMIRNOV\n')

        # Compara el valor máximo encontrado con el D estadístico para
        # determinar si se acepta o rechaza la hipótesis.
        if maximoValor < self.D_estadistico:
            # Si el valor máximo es menor que el D estadístico:
            # la hipótesis se acepta.
            return True
        else:
            # Si el valor máximo es mayor o igual que el D estadístico:
            # la hipótesis se rechaza.
            return False
