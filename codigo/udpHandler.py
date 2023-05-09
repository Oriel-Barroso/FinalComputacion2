import socketserver
from busquedaBidThreading import BusquedaBidireccional

class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        socket = self.request[1]
        try:
            print(f'Cliente conectado desde la dirección {self.client_address[0]} en el proceso {self.client_address[1]}')
            tamaño = self.request[0].decode('ascii')
            socket.sendto((f'{BusquedaBidireccional(int(tamaño)).run()}').encode(), self.client_address)
        except Exception as e:
            socket.sendto(f'{e}'.encode())


class ThreadedUDPHandler(socketserver.ThreadingUDPServer, socketserver.UDPServer):
    pass


class ForkedUDPHandler(socketserver.ForkingMixIn, socketserver.UDPServer):
    pass
