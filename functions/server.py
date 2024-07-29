import threading 
import queue  
import time

#Variables globales
cola_clientes = queue.Queue()  # Cola para los clientes
datos_clientes = []  # Lista para almacenar datos de los clientes
tiempo_simulacion = 0  # Contador de tiempo simulado
estadisticas = []  # Lista para almacenar estadísticas
servidor_tiempos = {}  # Diccionario para almacenar los tiempos de los servidores
semaforo_cola = threading.Semaphore()  # Semáforo para manejar la cola de clientes

def servidor(nombre_servidor):
    global tiempo_simulacion, servidor_tiempos
    ultimo_tiempo_salida = 0
    print("hola ", nombre_servidor)
    while True:
        cliente = cola_clientes.get()  # Obtiene un cliente de la cola
        if cliente is None:  # Si el cliente es None, significa que es el final de la simulación
            print("Fin ", cliente)
            cola_clientes.task_done()
            break
        nombre_cliente, llegada, tiempo_servicio, tiempo_demora = cliente  # Desempaqueta los datos del cliente
        print("datos ", nombre_cliente, tiempo_servicio, llegada, tiempo_demora)

        with semaforo_cola:
            print("entro de nuevo, ")
            tiempo_inicio = max(llegada, ultimo_tiempo_salida)  # Calcula el tiempo de inicio del servicio
            espera = max(0, tiempo_inicio - llegada)  # Calcula el tiempo de espera

        tiempo_ocio = max(0, tiempo_inicio - ultimo_tiempo_salida)  # Calcula el tiempo de ocio del servidor
        tiempo_llegada = llegada
        inicio = tiempo_inicio
        print(f'{nombre_cliente} llegó a la cola a las {tiempo_llegada:.2f}')  # Imprime el momento de llegada del cliente
        print(f'{nombre_cliente} empezó el servicio en {nombre_servidor} a las {inicio:.2f} (esperó {espera:.2f})')  # Imprime el inicio del servicio y el tiempo de espera
        print(f'{nombre_servidor} estuvo ocioso por {tiempo_ocio:.2f} antes de este servicio')  # Imprime el tiempo de ocio del servidor

        # Imprimir la cola justo antes de que el cliente comience a ser atendido
        clientes_en_cola = [c[0] for c in list(cola_clientes.queue)]
        print(f"\nClientes en cola antes de que {nombre_cliente} inicie servicio: {clientes_en_cola}\n")

        time.sleep(tiempo_servicio*0.001)  # Simula el tiempo de servicio
        duracion_servicio = tiempo_servicio
        tiempo_salida = tiempo_inicio + duracion_servicio
        print(f'{nombre_cliente} terminó el servicio en {nombre_servidor} a las {tiempo_salida:.2f} (duración del servicio {duracion_servicio:.2f})')  # Imprime el fin del servicio y la duración del mismo
        servidor_tiempos[nombre_servidor] = tiempo_inicio + duracion_servicio
        ultimo_tiempo_salida = tiempo_inicio + duracion_servicio  # Actualiza el tiempo de salida del último cliente atendido


        with semaforo_cola:
            datos_clientes.append({  # Agrega los datos del cliente a la lista de datos_clientes
                "Cliente": nombre_cliente,
                "Servidor": nombre_servidor,
                "Tiempo de llegada": tiempo_llegada,
                "Tiempo de inicio": inicio,
                "Tiempo de salida": tiempo_salida,
                "Tiempo de espera": espera,
                "Tiempo de servicio": duracion_servicio,
                "Tiempo de ocio": tiempo_ocio
            })
            estadisticas.append({  # Agrega los datos del cliente a la lista de estadisticas
                "Tiempo de llegada": tiempo_demora
            })
        cola_clientes.task_done()
