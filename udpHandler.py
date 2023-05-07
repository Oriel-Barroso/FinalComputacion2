import socketserver


class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            pass
        except Exception:
            pass


class ThreadedUDPHandler(socketserver.ThreadingUDPServer, socketserver.UDPServer):
    pass


class ForkedUDPHandler(socketserver.ForkingMixIn, socketserver.UDPServer):
    pass
