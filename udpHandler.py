import socketserver

class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        pass

class ThreadedUDPHandler(socketserver.ThreadingUDPServer, socketserver.UDPServer):
    pass

class ForkedUDPHandler(socketserver.ForkingMixIn, socketserver.UDPServer):
    pass