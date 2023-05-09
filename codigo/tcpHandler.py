import socketserver
from busquedaBidThreading import BusquedaBidireccional
import time


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            host, port = self.request.getsockname()
            print(f'Cliente conectado desde la dirección {host} en el puerto {port}')
            self.data = self.request.recv(1024)
            num = int(self.data.decode('ascii'))
            print(num)
            self.request.sendall((f'{BusquedaBidireccional(int(num)).run()}').encode())
        except Exception as e:
            print(e)
            return "Error"


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ForkedTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass
