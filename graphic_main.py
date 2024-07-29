import tkinter as tk
from tkinter import ttk, messagebox
import threading

# from functions.simulate import ejecutar_simulacion
from functions.simulate_graphic import ejecutar_simulacion
from functions.parameters_selector import find_good_parameters
from functions.congruential_generator import GeneradorCongruencialMultiplicativo
from functions.congruential_mix_generator import GeneradorCongruencialMixto
from functions.graficador import graficador
from functions.graphic_simulator import QueueSystem, Client

class ColaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Sistema de Colas M/M/3")

        self.mainframe = ttk.Frame(self.root, padding="10 10 10 10")
        self.mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.mainframe, text="Tasa de Llegada (λ):").grid(row=0, column=0, sticky=tk.W)
        self.lambda_entry = ttk.Entry(self.mainframe)
        self.lambda_entry.grid(row=0, column=1)

        ttk.Label(self.mainframe, text="Tasa de Servicio (μ):").grid(row=1, column=0, sticky=tk.W)
        self.mu_entry = ttk.Entry(self.mainframe)
        self.mu_entry.grid(row=1, column=1)

        ttk.Label(self.mainframe, text="Cantidad de Clientes:").grid(row=2, column=0, sticky=tk.W)
        self.clientes_entry = ttk.Entry(self.mainframe)
        self.clientes_entry.grid(row=2, column=1)

        ttk.Label(self.mainframe, text="Número de Servidores:").grid(row=3, column=0, sticky=tk.W)
        self.servers_entry = ttk.Entry(self.mainframe)
        self.servers_entry.grid(row=3, column=1)

        ttk.Label(self.mainframe, text="Semilla:").grid(row=4, column=0, sticky=tk.W)
        self.seed_entry = ttk.Entry(self.mainframe)
        self.seed_entry.grid(row=4, column=1)

        self.generador_var = tk.StringVar()
        ttk.Label(self.mainframe, text="Tipo de Generador:").grid(row=5, column=0, sticky=tk.W)
        ttk.Radiobutton(self.mainframe, text="Mixto", variable=self.generador_var, value='mixto').grid(row=5, column=1, sticky=tk.W)
        ttk.Radiobutton(self.mainframe, text="Multiplicativo", variable=self.generador_var, value='multiplicativo').grid(row=6, column=1, sticky=tk.W)

        start_button = ttk.Button(self.mainframe, text="Iniciar Simulación", command=self.on_start_button_click)
        start_button.grid(row=7, column=0, columnspan=2)

        # Añadir widgets para la cola y los servidores
        self.cola_label = ttk.Label(self.mainframe, text="Cola de Clientes:")
        self.cola_label.grid(row=8, column=0, columnspan=2, sticky=tk.W)

        self.cola_listbox = tk.Listbox(self.mainframe)
        self.cola_listbox.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.servidores_label = ttk.Label(self.mainframe, text="Servidores:")
        self.servidores_label.grid(row=10, column=0, columnspan=2, sticky=tk.W)

        self.servidores_listbox = tk.Listbox(self.mainframe)
        self.servidores_listbox.grid(row=11, column=0, columnspan=2, sticky=(tk.W, tk.E))

    def on_start_button_click(self):
        try:
            lambda_value = float(self.lambda_entry.get())
            mu_value = float(self.mu_entry.get())
            cantidad_clientes = int(self.clientes_entry.get())
            num_servers = int(self.servers_entry.get())
            semilla = int(self.seed_entry.get())

            generador_tipo = self.generador_var.get()

            if generador_tipo == 'mixto':
                a, b, m = find_good_parameters(semilla, 'mixto')
                generador = GeneradorCongruencialMixto(semilla, a, b, m)
            elif generador_tipo == 'multiplicativo':
                a, m = find_good_parameters(semilla, 'multiplicativo')
                generador = GeneradorCongruencialMultiplicativo(semilla, a, m)
            else:
                messagebox.showerror("Error", "Seleccione un tipo de generador.")
                return

            threading.Thread(target=self.iniciar_simulacion, args=(generador, lambda_value, mu_value, cantidad_clientes, num_servers)).start()

        except ValueError as e:
            messagebox.showerror("Error", f"Entrada no válida: {e}")

    def iniciar_simulacion(self, generador, lambda_value, mu_value, cantidad_clientes, num_servers):
        print('\nIniciando simulación...')
        resultado_df, estadisticas = ejecutar_simulacion(generador, lambda_value, mu_value, cantidad_clientes, num_servers, self)
        print("\nResumen de los datos de los clientes:")
        print(resultado_df)

        # Lista para almacenar las instancias de Client
        clientss = []

        # Iterar sobre las filas del DataFrame
        for index, row in resultado_df.iterrows():
            client_id = int(row["Cliente"].split()[1]) 
            arrival_time = row["Tiempo de llegada"]
            # Extraer el número del servidor
            server = int(row["Servidor"].split()[1]) + 1
            service_start_time = row["Tiempo de inicio"]
            departure_time = row["Tiempo de salida"]

            # Crear una instancia de Client
            client = Client(client_id, arrival_time, server, service_start_time, departure_time)
            # Añadir a la lista de clientes
            clientss.append(client)

        QueueSystem(clientss)
        graficador(resultado_df, estadisticas, num_servers, lambda_value, mu_value, cantidad_clientes)

        print('\nFin de programa')

    def actualizar_cola(self, clientes_en_cola):
        self.cola_listbox.delete(0, tk.END)
        for cliente in clientes_en_cola:
            self.cola_listbox.insert(tk.END, cliente)

    def actualizar_servidores(self, servidor, cliente, estado):
        self.servidores_listbox.insert(tk.END, f"{servidor} - {cliente} - {estado}")

def main():
    root = tk.Tk()
    app = ColaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
