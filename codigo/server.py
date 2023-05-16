import socketserver
import threading
import multiprocessing
from tcpHandler import MyTCPThreadV4Handler, MyTCPThreadV6Handler, MyForkedTCPV6Server, MyForkedTCPV4Server, MyTCPHandler
from udpHandler import MyForkedUDPV6Server, MyForkedUDPV4Server, MyUDPServerThreadV6Handler, MyUDPServerThreadV4Handler, MyUDPHandler
import argparse
import redis
import sys


def getValues(identificacion):
    try:
        redisDB = redis.Redis(host='localhost', port=6379, db=0)
        dictValues = {}
        for k, v in redisDB.hgetall(identificacion.capitalize()).items():
            try:
                dictValues[k.decode()] = int(v.decode())
            except:
                dictValues[k.decode()] = v.decode()
        if len(dictValues.keys()) != 0:
            return dictValues
        else:
            print(f"Error redis. Su usuario se encuentra registrado?")
            sys.exit()
    except Exception as error:
        print(f'Error: {error}')
        sys.exit()


def executeServer(ejecucion, server):
    if ejecucion == 'process':
        server = multiprocessing.Process(target=server.serve_forever())
    else:
        server = threading.Thread(target=server.serve_forever())
    server.daemon = True
    server.start()



if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument('-id', '--identificacion', help='Indique su'
                       ' nombre', type=str, action='store',
                       required=True)
    args = parse.parse_args()
    dictValues = getValues(args.identificacion)
    print('Procesando argumentos...')
    socketserver.TCPServer.allow_reuse_address = True
    socketserver.UDPServer.allow_reuse_address = True
    if dictValues['ip'] == 'ipv6' and dictValues['protocolo'].lower() == 'tcp' and dictValues['proceso'].lower() == 'thread':
        handlerClass = MyTCPThreadV6Handler
    elif dictValues['ip'] == 'ipv4' and dictValues['protocolo'].lower() == 'tcp' and dictValues['proceso'].lower() == 'thread':
        handlerClass = MyTCPThreadV4Handler
    elif dictValues['ip'] == 'ipv6' and dictValues['protocolo'].lower() == 'tcp' and dictValues['proceso'].lower() == 'process':
        handlerClass = MyForkedTCPV6Server
    elif dictValues['ip'] == 'ipv4' and dictValues['protocolo'].lower() == 'tcp' and dictValues['proceso'].lower() == 'process':
        handlerClass = MyForkedTCPV4Server
    elif dictValues['ip'] == 'ipv6' and dictValues['protocolo'].lower() == 'udp' and dictValues['proceso'].lower() == 'thread':
        handlerClass = MyUDPServerThreadV6Handler
    elif dictValues['ip'] == 'ipv4' and dictValues['protocolo'].lower() == 'udp' and dictValues['proceso'].lower() == 'thread':
        handlerClass = MyUDPServerThreadV4Handler
    elif dictValues['ip'] == 'ipv6' and dictValues['protocolo'].lower() == 'udp' and dictValues['proceso'].lower() == 'process':
        handlerClass = MyForkedUDPV6Server
    elif dictValues['ip'] == 'ipv4' and dictValues['protocolo'].lower() == 'udp' and dictValues['proceso'].lower() == 'process':
        handlerClass = MyForkedUDPV4Server
    print(handlerClass)
    if dictValues['protocolo'].lower() == 'tcp':
        if dictValues['proceso'].lower() == 'process':
            with handlerClass((dictValues['host'], dictValues['puerto']), MyTCPHandler) as server:
                print('hello world from processing')
                executeServer(dictValues['proceso'].lower(), server)
        if dictValues['proceso'] == 'thread':
            with handlerClass((dictValues['host'], dictValues['puerto']), MyTCPHandler) as server:
                print('hello world from threading')
                executeServer(dictValues['proceso'].lower(), server)
    elif dictValues['protocolo'].lower() == 'udp':
        if dictValues['proceso'].lower() == 'process':
            with handlerClass((dictValues['host'], dictValues['puerto']), MyUDPHandler) as server:
                print('hello world from processing')
                executeServer(dictValues['proceso'].lower(), server)
        if dictValues['proceso'].lower() == 'thread':
            with handlerClass((dictValues['host'], dictValues['puerto']), MyUDPHandler) as server:
                print('hello world from threading')
                executeServer(dictValues['proceso'].lower(), server)
