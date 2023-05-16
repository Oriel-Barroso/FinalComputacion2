import socketserver, socket
from busquedaBidThreading import BusquedaBidireccionalThread
from busquedaBidProcessing import BusquedaBidireccionalProcess
import time
import ast


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(self.request.getsockname())
        while True:
            self.data = self.request.recv(1024)
            values = ast.literal_eval(self.data.decode())
            inicio = time.time()
            print(values)
            busq = self.busquedaBid(values['tamaño'], values['ejecucion'])
            fin = time.time()
            tiempo_transcurrido = fin - inicio
            self.request.sendall((f"{busq}.\n El tiempo en ejecutarse con {values['ejecucion']} fue de: {tiempo_transcurrido}").encode())

    def busquedaBid(self, num, proc):
        if proc == 'procesos':
            busq = BusquedaBidireccionalProcess(num)
            return busq.run()
        busq = BusquedaBidireccionalThread(num)
        return busq.run()


class MyForkedTCPV6Server(socketserver.ForkingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET6


class MyForkedTCPV4Server(socketserver.ForkingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET


class MyTCPThreadV6Handler(socketserver.ThreadingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET6


class MyTCPThreadV4Handler(socketserver.TCPServer, socketserver.ThreadingMixIn):
    address_family = socket.AF_INET
