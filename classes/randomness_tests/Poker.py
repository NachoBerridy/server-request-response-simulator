from collections import Counter
import scipy.stats as stats
import pandas as pd


class Poker:
    """
    Realiza la prueba de póker para una secuencia de números.

    :param secuencia: Lista de números entre 0 y 1.
    :param num_digitos: Número de dígitos a considerar
    para cada número (default 5).
    :param alpha: Nivel de significancia para la prueba (default 0.05).
    :return: True si la prueba pasa, False en caso contrario.
    """
    # Cantidad de números en la secuencia
    
    def __init__(self, num_digitos=5, alpha=0.05):
        self.num_digitos = num_digitos
        self.alpha = alpha

    def test(self, secuencia):
        n = len(secuencia)
        # Convertir los números a strings de dígitos
        numeros_str = [f"{num:.{self.num_digitos}f}"[2:] for num in secuencia]

        # Contar las frecuencias de cada patrón
        frecuencias_observadas = Counter(numeros_str)

        # Calcular la frecuencia esperada
        k = 10 ** self.num_digitos
        frecuencia_esperada = n / k

        # Calcular el estadístico chi-cuadrado
        # Calcula la suma de Chi-cuadrado usando la fórmula:
        # sum((observado - esperado)^2 / esperado)
        chi_cuadrado = sum(
            (fo - frecuencia_esperada) ** 2 /
            frecuencia_esperada for fo in frecuencias_observadas.values())

        # Calcular los grados de libertad
        grados_libertad = k - 1

        # Obtener el valor crítico de chi-cuadrado
        chi_critico = stats.chi2.ppf(1 - self.alpha, grados_libertad)

        # Crear un DataFrame para presentar los resultados
        df_poker = pd.DataFrame(
            columns=['Chi-cuadrado', 'Chi-cuadrado_critico'])
        df_poker.loc[0] = [chi_cuadrado, chi_critico]

        print('\n RESULTADOS TEST DE POKER\n')

        # Comparar y devolver el resultado
        if chi_cuadrado <= chi_critico:
            return True
        else:
            return False
