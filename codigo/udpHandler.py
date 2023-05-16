import socketserver
import socket
from busquedaBidThreading import BusquedaBidireccionalThread
from busquedaBidProcessing import BusquedaBidireccionalProcess
import ast
import time


class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        socket = self.request[1]
        try:
            print(f'Cliente conectado desde la dirección {self.client_address[0]} en el proceso {self.client_address[1]}')
            values = ast.literal_eval(self.request[0].decode())
            inicio = time.time()
            busq = self.busquedaBid(values['tamaño'], values['ejecucion'])
            fin = time.time()
            tiempo_transcurrido = fin - inicio
            socket.sendto((f"{busq}.\n El tiempo en ejecutarse con {values['ejecucion']} fue de: {tiempo_transcurrido}").encode(), self.client_address)
        except Exception as e:
            socket.sendto(f'{e}'.encode(), self.client_address)

    def busquedaBid(self, num, proc):
        if proc == 'procesos':
            busq = BusquedaBidireccionalProcess(num)
            return busq.run()
        busq = BusquedaBidireccionalThread(num)
        return busq.run()


class MyForkedUDPV6Server(socketserver.ForkingMixIn, socketserver.UDPServer):
    address_family = socket.AF_INET6


class MyForkedUDPV4Server(socketserver.ForkingMixIn, socketserver.UDPServer):
    address_family = socket.AF_INET


class MyUDPServerThreadV6Handler(socketserver.ThreadingMixIn, socketserver.UDPServer):
    address_family = socket.AF_INET6


class MyUDPServerThreadV4Handler(socketserver.UDPServer, socketserver.ThreadingMixIn):
    address_family = socket.AF_INET
