import sys
import argparse
import redis
import socket
import socketserver
import time


def selectIPV(ip, protocolo):
    if ip == 'ipv6':
        return socket.socket(socket.AF_INET6, protocolo)
    return socket.socket(socket.AF_INET, protocolo)


def udp_protocol(ip, port, ipv):
    print('Conexion UDP')
    c_sock = selectIPV(ipv, socket.SOCK_DGRAM)
    print('Introduzca un tamaño de matriz mayor a 2')
    print('Especifique el tipo de ejecucion. El mismo debe ser procesos o hilos')
    while True:
        try:
            tamaño = 0
            ejc = ''
            while tamaño < 3:
                tamaño = int(input('Tamaño matriz: '))
            while ejc != 'hilos' and ejc != 'procesos':
                try:
                    ejc = str(input('Indique el tipo de ejecucion: '))
                except Exception as e:
                    print(f'Error: {e}')
            values = {'tamaño': tamaño, 'ejecucion': ejc}
            c_sock.sendto(str(values).encode(), (ip, port))
            rcv = str(c_sock.recv(1024), "utf-8")
            print("El resultado es: ", rcv)
        except EOFError as e:
            print(e)
            break
    c_sock.close()


def tcp_protocol(ip, port, ipv):
    print('Conexion TCP')
    c_sock = selectIPV(ipv, socket.SOCK_STREAM)
    c_sock.connect((ip, port))
    print('Introduzca un tamaño de matriz mayor a 2')
    print('Especifique el tipo de ejecucion. El mismo debe ser procesos o hilos')
    while True:
        try:
            tamaño = 0
            ejc = ''
            while tamaño < 3:
                tamaño = int(input('Tamaño matriz: '))
            while ejc != 'hilos' and ejc != 'procesos':
                try:
                    ejc = str(input('Indique el tipo de ejecucion: '))
                except Exception as e:
                    print(f'Error: {e}')
            values = {'tamaño': tamaño, 'ejecucion': ejc}
            c_sock.sendall(str(values).encode())
            res = str(c_sock.recv(5012), "utf-8")
            print('El resultado es: ', res)
        except EOFError as e:
            print(e)
            break


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


def main():
    socketserver.TCPServer.allow_reuse_address = True
    socketserver.UDPServer.allow_reuse_address = True
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', '--identificacion', help='Provee tu nombre'
                        ' de usuario', type=str, required=True)
    args = parser.parse_args()
    print('Procesando argumentos...')
    time.sleep(1)
    dictValues = getValues(args.identificacion)
    ip, puerto, protocolo, ipv = dictValues['host'], dictValues['puerto'], dictValues['protocolo'], dictValues['ip']
    print(ip)
    if protocolo.lower() == 'udp':
        udp_protocol(ip, puerto, ipv)
    elif protocolo.lower() == 'tcp':
        tcp_protocol(ip, puerto, ipv)
    else:
        print('Error')


if __name__ == '__main__':
    main()
