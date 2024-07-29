import math
import time
import numpy as np
from sympy import nextprime

from .congruential_mix_generator import GeneradorCongruencialMixto
from .congruential_generator import GeneradorCongruencialMultiplicativo
from .chi_cuadrado import prueba_chi2
from .kolgomorov_smirnov import prueba_ks
from .prueba_poker import prueba_poker
from .test_rachas import prueba_rachas


SEMILLA = 42

"""## Verificación del módulo

### Ejecución de pruebas de aleatoriedad y selección de parámetros
"""

# Pruebas básicas de aleatoriedad
def basic_random_tests(generador, num_samples=1000):
    '''
    La idea detrás de esta prueba es que, si el generador produce números verdaderamente aleatorios
    con una distribución uniforme entre 0 y 1, la media de una muestra grande de estos números debería
    estar cerca de 0.5. Por lo tanto, este método sirve como una primera verificación rápida de la calidad del generador.
    '''
    # Generar una lista de números pseudoaleatorios utilizando el generador dado
    num_generados = [generador.generarNumPseudoaleatorio() for _ in range(num_samples)]
    # Calcular la media de los números generados
    mean = np.mean(num_generados)
    # Calcular la varianza de los números generados
    #variance = np.var(num_generados)
    return mean

# Pruebas avanzadas de aleatoriedad
def advanced_random_tests(tipo_generador, num_samples=1000, a=None, b=None, m=None):
    """
    Realiza pruebas de aleatoriedad avanzadas utilizando un generador congruencial mixto o multiplicativo.

    Parámetros:
    - tipo_generador (str): El tipo de generador a utilizar. Puede ser 'mixto' o 'multiplicativo'.
    - num_samples (int): El número de muestras pseudoaleatorias a generar. Por defecto es 1000.
    - a (int): El multiplicador para el generador congruencial mixto. Por defecto es None.
    - b (int): El incremento para el generador congruencial mixto. Por defecto es None.
    - m (int): El módulo para el generador congruencial mixto o multiplicativo. Por defecto es None.

    Retorna:
    - bool: True si todas las pruebas de aleatoriedad son aprobadas, False en caso contrario.
    """

    # Crear una instancia del generador congruencial mixto o multiplicativo según el tipo especificado
    if tipo_generador == 'mixto':
        generador = GeneradorCongruencialMixto(SEMILLA, a, b, m)
    elif tipo_generador == 'multiplicativo':
        generador = GeneradorCongruencialMultiplicativo(SEMILLA, a, m)
    else:
        raise ValueError(f"Tipo de generador '{tipo_generador}' no reconocido.")

    # Generar una lista de números pseudoaleatorios utilizando el generador dado
    samples = [generador.generarNumPseudoaleatorio() for _ in range(num_samples)]

    # Convertir los números generados en frecuencias para la prueba chi-cuadrado
    frecuenciasObservadas, _ = np.histogram(samples, bins=10)
    # Realizar la prueba chi-cuadrado y obtener el resultado
    chi2_pass = prueba_chi2(frecuenciasObservadas, alpha=0.05, gradosLibertad=9)

    # Realizar la prueba KS y obtener el resultado
    ks_pass = prueba_ks(samples, D_estadistico=1.36 / math.sqrt(num_samples))

    # Realizar la prueba de rachas y obtener el resultado
    rachas_pass = prueba_rachas(samples)

    # Realizar la prueba de poker y obtener el resultado
    poker_pass = prueba_poker(samples, num_digitos=4, alpha=0.05)

    print('\nResultados de las pruebas de aleatoriedad:')
    print(f'Prueba Chi-cuadrado: {"Aprobada" if chi2_pass else "Rechazada"}')
    print(f'Prueba KS: {"Aprobada" if ks_pass else "Rechazada"}')
    print(f'Prueba Rachas: {"Aprobada" if rachas_pass else "Rechazada"}')
    print(f'Prueba Póker: {"Aprobada" if poker_pass else "Rechazada"}')

    # Devolver True si todas las pruebas son aprobadas, False en caso contrario
    return (chi2_pass and ks_pass and rachas_pass and poker_pass)


# Búsqueda de parámetros adecuados
def find_good_parameters(seed, tipo_generador, num_trials=1000, max_time=300):
    '''
    Parámetros:
    - seed: Semilla para el generador congruencial.
    - tipo_generador: Tipo de generador congruencial ('mixto' o 'multiplicativo').
    - num_trials: Número de intentos para encontrar los mejores parámetros (default 1000).
    - max_time: Tiempo máximo en segundos para realizar la búsqueda (default 300).
    '''

    best_params = None
    best_score = float('inf')   # Inicializa el mejor score con infinito
    start_time = time.time()   # Registra el tiempo de inicio

    for trial in range(num_trials):
        # Verificar si se ha alcanzado el tiempo máximo
        if time.time() - start_time > max_time:
            print(f"Tiempo máximo alcanzado ({max_time} segundos). Terminando búsqueda.")
            break

        try:
            # Generar parámetros aleatorios para el generador congruencial mixto
            if tipo_generador == 'mixto':
                a = np.random.randint(1, 2**30)
                b = np.random.randint(1, 2**30)
                m = nextprime(np.random.randint(max(a, b), 2**31))
                # Verificar que m, a y b sean coprimos
                if math.gcd(m, b) == 1 and math.gcd(m, a) == 1:
                    generador = GeneradorCongruencialMixto(seed, a, b, m)
                    # Realizar pruebas básicas de aleatoriedad y obtener la media
                    mean = basic_random_tests(generador)
                    # Calcular el score actual como la diferencia absoluta entre la media y 0.5
                    current_score = abs(mean - 0.5) #Verifica que la media sea cercana a 0.5. Si la muestra es uniforme,
                                                    # la media debería ser 0.5.

                    # Verificar si el score actual es mejor que el mejor score encontrado hasta ahora
                    if current_score < best_score:
                        # Realizar pruebas avanzadas de aleatoriedad y verificar si todas son aprobadas
                        if advanced_random_tests('mixto', a=a, b=b, m=m):
                            # Actualizar el mejor score y los mejores parámetros
                            best_score = current_score
                            best_params = (a, b, m)
                            print(f"Nuevos mejores parámetros encontrados en el intento {trial}: score = {best_score}")

            # Generar parámetros aleatorios para el generador congruencial multiplicativo
            elif tipo_generador == 'multiplicativo':
                a = np.random.randint(1, 2**30)
                b = 0  # En el generador multiplicativo b debe ser 0
                m = nextprime(np.random.randint(max(a, 2), 2**31))  # Se ajusta el rango para m

                # Verificar que m y a sean coprimos
                if math.gcd(m, a) == 1:
                    generador = GeneradorCongruencialMultiplicativo(seed, a, m)
                    # Realizar pruebas básicas de aleatoriedad y obtener la media
                    mean = basic_random_tests(generador)
                    # Calcular el score actual como la diferencia absoluta entre la media y 0.5
                    current_score = abs(mean - 0.5)

                    # Verificar si el score actual es mejor que el mejor score encontrado hasta ahora
                    if current_score < best_score:
                        # Realizar pruebas avanzadas de aleatoriedad y verificar si todas son aprobadas
                        if advanced_random_tests('multiplicativo', a=a, b=b, m=m):
                            # Actualizar el mejor score y los mejores parámetros
                            best_score = current_score
                            best_params = (a, m)
                            print(f"Nuevos mejores parámetros encontrados en el intento {trial}: score = {best_score}")

        except Exception as e:
            print(f"Error en el intento {trial}: {e}")

        # Imprimir el mejor score hasta el momento cada 100 intentos
        if trial % 100 == 0:
            print(f"Intento {trial}: Mejor puntuación hasta ahora = {best_score}")

    # Verificar si se encontraron buenos parámetros
    if best_params is None:
        raise ValueError("No se encontraron buenos parámetros después de múltiples intentos.")

    # Devolver los mejores parámetros encontrados
    return best_params