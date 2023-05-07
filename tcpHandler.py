import socketserver
from busquedaBidThreading import BusquedaBidireccional


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                self.data = self.request.recv(1024)
                num = self.data.decode('ascii')
                print(num)
                busq = BusquedaBidireccional(num)
                print(busq.__str__())
                print('asf')
                print(busq.run())
                print(9877897)
                return "Exito"
            except Exception:
                return "Error"


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ForkedTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass
