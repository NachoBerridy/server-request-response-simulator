import scipy.stats as stats
import numpy as np
import math
import pandas as pd


class Streak:
    """
    Prueba de Rachas para verificar condición de
    independencia en la muestra recibida
    """

    def __init__(self):
        pass

    def test(self, secuencia):

        n = len(secuencia)
        if n < 2:
            raise ValueError('''La secuencia debe tener al menos dos elementos
                            para realizar la prueba de rachas.''')

        # Calcular la media de la secuencia
        media = np.mean(secuencia)
        # Crear una secuencia de signos (+ y -)
        signos = ['+' if x > media else '-' for x in secuencia]

        # Imprimir la secuencia de signos para depuración
        # print("Secuencia de signos:", signos)

        # Contar las rachas
        rachas = 1
        for i in range(1, n):
            if signos[i] != signos[i-1]:
                rachas += 1

        # Imprimir el número de rachas para depuración
        print(f"Número de rachas contadas: {rachas}")

        # Contar el número de elementos mayores que la media (+)
        n1 = signos.count('+')
        # Calcular el número de elementos menores o iguales que la media (-)
        n2 = n - n1

        # Imprimir n1 y n2 para depuración
        print(f"n1 (número de '+'): {n1}")
        print(f"n2 (número de '-'): {n2}")

        # Asegurarse de que n1 y n2 no sean cero para evitar división por cero
        if n1 == 0 or n2 == 0:
            raise ValueError('''La secuencia no tiene suficiente variabilidad
                            para realizar la prueba de rachas.''')

        # Calcular la media esperada de rachas \mu
        media_esperada = ((2 * n1 * n2) / n) + 0.5
        # Calcular la varianza de rachas \sigma^2
        varianza = (2 * n1 * n2 * (2 * n1 * n2 - n)) / (n**2 * (n - 1))
        desviacion_estandar = math.sqrt(varianza)

        # Calcular el valor Z para la prueba de rachas
        Z = (rachas - media_esperada) / desviacion_estandar

        # Determinar el valor crítico de Z para un nivel de significancia
        # de 0.05 (bilateral)
        # El nivel de significancia (denotado como α) es la probabilidad de
        # cometer un error tipo I al rechazar una hipótesis nula verdadera.
        # Dividimos 0.05 por 2 porque estamos interesados en la cola inferior
        # y superior de la distribución normal.
        Z_alpha = stats.norm.ppf(1 - 0.05 / 2)

        # Preparar el DataFrame para mostrar los resultados
        df_rachas = pd.DataFrame(
            columns=['Rachas', 'Media Esperada', 'Varianza', 'Z', 'Z_critico'])
        df_rachas.loc[0] = [rachas, media_esperada, varianza, Z, Z_alpha]

        # Imprimir los resultados de la prueba de rachas
        print('\n RESULTADOS TEST DE RACHAS\n')
        print(df_rachas)

        # Comparar el valor Z calculado con el valor crítico para decidir
        # si se acepta o rechaza la hipótesis nula
        if -Z_alpha < Z < Z_alpha:
            return True
        else:
            return False
