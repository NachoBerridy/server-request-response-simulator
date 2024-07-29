import math

class GeneradorCongruencialMultiplicativo:
    """Generador congruencial multiplicativo"""
    def __init__(self, seed, a, m):
        # Inicializa los parámetros del generador
        self.seed = seed    # Valor inicial para generar la secuencia
        self.a = a          # Multiplicador
        self.b = 0          # Incremento
        self.m = m          # Módulo
        self.valorActualSemilla = seed # Valor actual, inicialmente igual a la semilla
    def generarNumPseudoaleatorio(self):
        """Genera un número pseudoaleatorio entre 0 y 1 usando generador congruencial lineal multiplicativo"""
        # Aplica la fórmula del método congruencial mixto
        self.valorActualSemilla = (self.a * self.valorActualSemilla + self.b) % self.m
        # Devuelve el valor normalizado entre 0 y 1
        return self.valorActualSemilla / self.m
    def exponencial(self, lam):
        """Genera un número con distribución exponencial"""
        # Genera un número aleatorio uniforme entre 0 y 1
        u = self.generarNumPseudoaleatorio()
        # F(x) = 1 - e^(-λx)
        # F(x) = u = 1 - e^(-λx)
        # 1 - u = e^(-λx)
        # ln(1 - u) = ln(e^(-λx))
        # ln(1 - u) = -λx ln(e)
        # ln(1 - u) = -λx
        # ln(1 - u) / -λ = x
        # x = -ln(1 - u) / λ
        return -math.log(1 - u) / lam