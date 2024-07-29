import pygame
import time
import random
import threading
import pandas as pd

class Client:
    def __init__(self, client_id, arrival_time, server, service_start_time, departure_time):
        self.client_id = client_id
        self.arrival_time = arrival_time
        self.server = server
        self.service_start_time = service_start_time
        self.departure_time = departure_time

class QueueSystem:
    def __init__(self, clients):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Sistema de Filas de Espera")
        self.clock = pygame.time.Clock()

        self.clients = clients
        self.client_representations = {}
        self.waiting_queue = []

        self.server_positions = {1: (600, 100), 2: (600, 300), 3: (600, 500)}

        self.current_time = 0
        self.clients_served = 0

        self.font = pygame.font.Font(None, 36)

        self.running = True
        self.start_simulation()

    def start_simulation(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((255, 255, 255))
            self.draw_servers()
            self.update_clients()
            self.update_labels()

            pygame.display.flip()
            self.clock.tick(30)  # Actualizar 30 veces por segundo
            self.current_time += 1 / 30

        pygame.quit()
        self.write_to_excel()

    def draw_servers(self):
        for server_id, position in self.server_positions.items():
            pygame.draw.rect(self.screen, (128, 128, 128), (position[0] - 80, position[1] - 80, 130, 130))
            text = self.font.render(f"S {server_id}", True, (0, 0, 0))
            self.screen.blit(text, (position[0] - 40, position[1] - 10))

    def update_clients(self):
        # Agregar clientes a la cola de espera
        for client in self.clients:
            if client.arrival_time <= self.current_time and client.client_id not in self.client_representations:
                color = [random.randint(0, 255) for _ in range(3)]
                self.client_representations[client.client_id] = {
                    "rect": [50, 100 + len(self.waiting_queue) * 30, 20, 20],
                    "color": color,
                    "id": client.client_id,
                    "in_queue": True
                }
                self.waiting_queue.append(client)
                threading.Thread(target=self.wait_in_queue, args=(client,)).start()

        # Dibujar los clientes
        for client_id, client_data in self.client_representations.items():
            pygame.draw.ellipse(self.screen, client_data["color"], client_data["rect"])
            text = self.font.render(str(client_data["id"]), True, (255, 255, 255))
            self.screen.blit(text, (client_data["rect"][0], client_data["rect"][1]))

    def wait_in_queue(self, client):
        while self.current_time < client.service_start_time:
            time.sleep(0.01)

        # Mover al cliente al servidor
        client_rep = self.client_representations[client.client_id]["rect"]
        server_pos = self.server_positions[client.server]

        self.client_representations[client.client_id]["in_queue"] = False

        while client_rep[0] < server_pos[0] - 50 or client_rep[1] < server_pos[1] - 50:
            if client_rep[0] < server_pos[0] - 50:
                client_rep[0] += 1
            if client_rep[1] < server_pos[1] - 50:
                client_rep[1] += 1
            time.sleep(0.01)

        # Esperar durante el tiempo de servicio
        time.sleep(client.departure_time - client.service_start_time)

        # Mover al cliente fuera del servidor
        while client_rep[0] < 800 and client_rep[1] < 600:
            client_rep[0] += 1
            client_rep[1] += 1
            time.sleep(0.01)

        del self.client_representations[client.client_id]
        self.clients_served += 1

        # Reordenar la cola de espera visualmente
        self.reorder_waiting_queue()

    def reorder_waiting_queue(self):
        y_offset = 100
        for client in self.waiting_queue:
            if self.client_representations[client.client_id]["in_queue"]:
                self.client_representations[client.client_id]["rect"][1] = y_offset
                y_offset += 30

    def update_labels(self):
        time_text = self.font.render(f"Tiempo: {int(self.current_time)}", True, (0, 0, 0))
        self.screen.blit(time_text, (10, 10))
        clients_text = self.font.render(f"Clientes atendidos: {self.clients_served}", True, (0, 0, 0))
        self.screen.blit(clients_text, (10, 50))

    def write_to_excel(self):
        data = {
            "Client ID": [client.client_id for client in self.clients],
            "Arrival Time": [client.arrival_time for client in self.clients],
            "Server": [client.server for client in self.clients],
            "Service Start Time": [client.service_start_time for client in self.clients],
            "Departure Time": [client.departure_time for client in self.clients],
        }
        df = pd.DataFrame(data)
        df.to_excel("clients_data.xlsx", index=False)
        print("Datos de los clientes guardados en 'clients_data.xlsx'")
