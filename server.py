import socketserver
import threading
import multiprocessing
from tcpHandler import ForkedTCPServer, ThreadedTCPServer, MyTCPHandler
from udpHandler import ForkedUDPServer, ThreadedUDPServer, MyUDPHandle
import redis


def getValues():
    redisDB = redis.Redis(host='localhost', port=6379, db=0)
    values = redisDB.mget(['user', 'parametros'])
    value
    return values


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    socketserver.UDPServer.allow_reuse_address = True
    redisValues = getValues()
    protocolo, asincronia, puerto, direccion = redisValues[0], redisValues[1],\
                                               redisValues[2], redisValues[3]
    if protocolo == 'tcp':
        if asincronia == 'process':
            with ForkedTCPServer((direccion, puerto), MyTCPHandler) as server:
                print('hello world from processing')
                server_fork = multiprocessing.Process(target=server.
                                                      serve_forever())
                server_fork.daemon = True
                server_fork.start()
        if asincronia == 'thread':
            with ThreadedTCPServer((direccion, puerto), MyTCPHandler) as server:
                print('hello world from threading')
                server_thread = threading.Thread(target=server.serve_forever())
                server_thread.daemon = True
                server_thread.start()
    # UDP
    if asincronia == 'process':
        with ForkedUDPServer((direccion, puerto), MyUDPHandle) as server:
            print('hello world from processing')
            server_fork = multiprocessing.Process(target=server.serve_forever())
            server_fork.daemon = True
            server_fork.start()
    if asincronia == 'thread':
        with ThreadedUDPServer((direccion, puerto), MyUDPHandle) as server:
            print('hello world from threading')
            server_thread = threading.Thread(target=server.serve_forever())
            server_thread.daemon = True
            server_thread.start()
