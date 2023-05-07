import socketserver
import threading
import multiprocessing
from tcpHandler import ForkedTCPServer, ThreadedTCPServer, MyTCPHandler
from udpHandler import ForkedUDPHandler, ThreadedUDPHandler, MyUDPHandler
import redis
import argparse
import time


def convetirLista(args):
    return [args.ipdireccion, args.puerto, args.protocolo]


def agregarUsuario(db, usuario):
    usuarios = [usuarioInlista.decode() for usuarioInlista in
                list(db.smembers('Usuarios'))]
    if usuario not in usuarios:  # Ver si el usuario ya existe
        db.sadd("Usuarios", usuario)


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    redisDB = redis.Redis(host='localhost', port=6379, db=0)
    parse.add_argument('-id', '--identificacion', help='Indique su'
                       ' nombre', type=str, action='store',
                       required=True)
    parse.add_argument('-i', '--ipdireccion', help='Indique la direccion IP',
                       type=str, action='store', default="localhost")
    parse.add_argument('-ps', '--puerto', help='Indique el puerto para'
                       'comunicarte con el servidor',
                       required=True, type=int, action='store')
    parse.add_argument('-t', '--protocolo', help='Indique el protocolo.'
                       'process para procesos, y thread para hilo',
                       required=True, type=str, action='store')
    parse.add_argument('-thp', '--procesamiento', help='Indique si quiere utilizar'
                       ' procesos para la generacion del server',
                       type=str, action='store')
    args = parse.parse_args()
    print('Procesando argumentos...')
    time.sleep(1)
    agregarUsuario(redisDB, args.identificacion)
    listaArgs = convetirLista(args)
    redisDB.set(args.identificacion, str(listaArgs))
    socketserver.TCPServer.allow_reuse_address = True
    socketserver.UDPServer.allow_reuse_address = True
    if args.protocolo == 'tcp':
        if args.procesamiento == 'process':
            with ForkedTCPServer((args.ipdireccion, args.puerto), MyTCPHandler) as server:
                print('hello world from processing')
                server_fork = multiprocessing.Process(target=server.
                                                      serve_forever())
                server_fork.daemon = True
                server_fork.start()
        if args.procesamiento == 'thread':
            with ThreadedTCPServer((args.ipdireccion, args.puerto), MyTCPHandler) as server:
                print('hello world from threading')
                server_thread = threading.Thread(target=server.serve_forever())
                server_thread.daemon = True
                server_thread.start()
    # UDP
    if args.procesamiento == 'process':
        with ForkedUDPHandler((args.ipdireccion, args.puerto), MyUDPHandler) as server:
            print('hello world from processing')
            server_fork = multiprocessing.Process(target=server.serve_forever())
            server_fork.daemon = True
            server_fork.start()
    if args.procesamiento == 'thread':
        with ThreadedUDPHandler((args.ipdireccion, args.puerto), MyUDPHandle) as server:
            print('hello world from threading')
            server_thread = threading.Thread(target=server.serve_forever())
            server_thread.daemon = True
            server_thread.start()
