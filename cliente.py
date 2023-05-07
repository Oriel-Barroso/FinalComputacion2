import sys
import argparse
import redis
import socket
import socketserver
import time
import ast


def udp_protocol(ip, port, tamaño):
    print('Conexion UDP')
    c_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    c_sock.sendto(str(tamaño).encode(), (ip, port))
    print('Texto enviado')
    rcv = str(c_sock.recv(1024), "utf-8")
    print("El resultado es: ", rcv)
    c_sock.close()


def tcp_protocol(ip, port, tamaño):
    c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(type(ip), type(port))
    c_sock.connect((ip, port))
    c_sock.send(str(tamaño).encode())
    res = str(c_sock.recv(1024), "utf-8")
    print('El resultado es: ', res)
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
    parser.add_argument('-tam', '--tamaño', help='Indique el tamaño de la'
                        ' matriz: 3,4,5... . (default 3x3)', type=int,
                        action='store')
    args = parser.parse_args()
    print('Procesando argumentos...')
    time.sleep(1)
    redisValues = getValues(args.identificacion)
    ip, puerto, protocolo = redisValues[0], redisValues[1], redisValues[2]
    if protocolo.lower() == 'udp':
        udp_protocol(ip, puerto, args.tamaño)
    elif protocolo.lower() == 'tcp':
        tcp_protocol(ip, puerto, args.tamaño)
    else:
        print('Error')


if __name__ == '__main__':
    main()
