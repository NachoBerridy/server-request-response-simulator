import statistics
import scipy.stats as stats
import pandas as pd


class Chi_Square:
    """
    Prueba Chi-cuadrado para verificar la uniformidad de las frecuencias
    observadas.

    Parámetros:
    - frecuenciasObservadas: Lista de frecuencias observadas en cada categoría.
    - alpha: Nivel de significancia para la prueba
    (e.g., 0.05 para un 95% de confianza).
    - gradosLibertad: Grados de libertad para la distribución chi-cuadrado.

    Retorna:
    - True si la hipótesis nula se acepta, False en caso contrario.
    """

    def __init__(self, alpha, gradosLibertad):
        self.alpha = alpha
        self.gradosLibertad = gradosLibertad

    def test(self, frecuenciasObservadas):
        # Calcula la suma de Chi-cuadrado usando la fórmula:
        # sum((observado - esperado)^2 / esperado)
        # donde 'esperado' es la media de las frecuencias observadas.
        chi2_suma = sum(((fo - statistics.mean(frecuenciasObservadas)) ** 2) /
                        statistics.mean(frecuenciasObservadas)
                        for fo in frecuenciasObservadas)

        # Calcula el valor crítico de Chi-cuadrado para el nivel de
        # significancia 'alpha' y los grados de libertad especificados.
        chi2_critico = stats.chi2.ppf(1 - self.alpha, self.gradosLibertad)

        # Crea un DataFrame para presentar los resultados de la prueba.
        df_chi2 = pd.DataFrame(
            columns=['Chi-cuadrado', 'Chi-cuadrado_critico'])

        df_chi2.loc[0] = [chi2_suma, chi2_critico]

        # Compara el estadístico calculado con el valor crítico para
        # determinar si se acepta o rechaza la hipótesis nula.
        if chi2_suma < chi2_critico:
            # Si el estadístico es menor que el valor crítico:
            # la hipótesis nula se acepta.
            return True
        else:
            # Si el estadístico es mayor que el valor crítico:
            # la hipótesis nula se rechaza.
            return False
