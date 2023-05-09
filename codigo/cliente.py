import sys
import argparse
import redis
import socket
import socketserver
import time
import ast


def udp_protocol(ip, port):
    print('Conexion UDP')
    c_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Introduzca un tamaño de matriz mayor a 2')
    while True:
        try:
            tamaño = 0
            while tamaño < 3:
                tamaño = int(input('Tamaño matriz: '))
            c_sock.sendto(str(tamaño).encode(), (ip, port))
            print('Texto enviado')
            rcv = str(c_sock.recv(1024), "utf-8")
            print("El resultado es: ", rcv)
        except EOFError as e:
            print(e)
            break
    c_sock.close()


def tcp_protocol(ip, port):
    print('Conexion TCP')
    c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_sock.connect((ip, port))
    print('Introduzca un tamaño de matriz mayor a 2')
    while True:
        try:
            tamaño = 0
            while tamaño < 3:
                tamaño = int(input('Tamaño matriz: '))
            c_sock.send(str(tamaño).encode())
            res = str(c_sock.recv(1024), "utf-8")
            print('El resultado es: ', res)
        except EOFError as e:
            print(e)
            break
    c_sock.close()


def getValues(identificacion):
    redisDB = redis.Redis(host='localhost', port=6379, db=0)
    try:
        return ast.literal_eval(redisDB.get(identificacion).decode())
    except Exception:
        print("Error redis. Su usuario se encuentra registrado?")
        sys.exit()


def main():
    socketserver.TCPServer.allow_reuse_address = True
    socketserver.UDPServer.allow_reuse_address = True
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', '--identificacion', help='Provee tu nombre'
                        ' de usuario', type=str, required=True)
    args = parser.parse_args()
    print('Procesando argumentos...')
    time.sleep(1)
    redisValues = getValues(args.identificacion)
    ip, puerto, protocolo = redisValues[0], redisValues[1], redisValues[2]
    if protocolo.lower() == 'udp':
        udp_protocol(ip, puerto)
    elif protocolo.lower() == 'tcp':
        tcp_protocol(ip, puerto)
    else:
        print('Error')


if __name__ == '__main__':
    main()
