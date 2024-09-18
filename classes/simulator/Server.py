import threading
import time


class Server:
    def __init__(self, nombre_servidor, cola_clientes):
        self.nombre_servidor = nombre_servidor
        self.ultimo_tiempo_salida = 0
        self.tiempo_simulacion = 0
        self.servidor_tiempos = {}
        self.cola_clientes = cola_clientes  # Usa la cola global
        self.datos_clientes = []
        self.estadisticas = []
        self.semaforo_cola = threading.Semaphore()
        self.servidor_tiempos = {}

    def server(self):
        while True:
            print("Servidor ", self.nombre_servidor)
            cliente = self.cola_clientes.get()
            print("Cliente ", cliente)
            if cliente is None:
                print("Fin ", cliente)
                self.cola_clientes.task_done()
                break
            nombre_cliente, llegada, tiempo_servicio, tiempo_demora = cliente

            with self.semaforo_cola:
                tiempo_inicio = max(llegada, self.ultimo_tiempo_salida)
                espera = max(0, tiempo_inicio - llegada)

            tiempo_ocio = max(0, tiempo_inicio - self.ultimo_tiempo_salida)
            tiempo_llegada = llegada
            inicio = tiempo_inicio

            # clientes_en_cola = [c[0] for c in list(self.cola_clientes.queue)]
            time.sleep(tiempo_servicio * 0.001)
            duracion_servicio = tiempo_servicio
            tiempo_salida = tiempo_inicio + duracion_servicio
            self.servidor_tiempos[self.nombre_servidor] =\
                tiempo_inicio + duracion_servicio
            self.ultimo_tiempo_salida = tiempo_inicio + duracion_servicio

            with self.semaforo_cola:
                self.datos_clientes.append({
                    "Cliente": nombre_cliente,
                    "Servidor": self.nombre_servidor,
                    "Tiempo de llegada": tiempo_llegada,
                    "Tiempo de inicio": inicio,
                    "Tiempo de salida": tiempo_salida,
                    "Tiempo de espera": espera,
                    "Tiempo de servicio": duracion_servicio,
                    "Tiempo de ocio": tiempo_ocio
                })
                self.estadisticas.append({
                    "Tiempo de llegada": tiempo_demora
                })
            self.cola_clientes.task_done()
