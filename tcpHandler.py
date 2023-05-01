import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                pass

            except FileNotFoundError as err:
                pass


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ForkedTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass