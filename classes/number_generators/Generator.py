import math


class Generator:

    def __init__(self, seed, a, m, b=0):
        self.seed = seed  # Valor inicial para generar la secuencia
        self.a = a  # Multiplicador
        self.b = b  # Incremento
        self.m = m  # Módulo
        # Valor actual, inicialmente igual a la semilla
        self.current_seed_value = seed

    def generate_pseudo_random_number(self):
        '''
        Genera un número pseudoaleatorio entre 0 y 1 usando generador
        congruencial lineal multiplicativo
        '''

        self.current_seed_value = (self.a * self.current_seed_value) % self.m
        return self.current_seed_value / self.m

    def exponential(self, lam):
        '''
        Genera un número con distribución exponencial
        '''
        u = self.generate_pseudo_random_number()
        return -math.log(1 - u) / lam
