import sys, argparse, socket, redis


def udp_protocol(ip, port):
    try:
        c_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            tamañoMatriz = int(input("Indica el tamaño de la matriz. El numero indicado "
                                    "dara como resultado una matriz nxn (no puede ser menor"
                                    "a 3): "))
            try:
                for line in sys.stdin:
                    print('linea escrita:', line)
                    c_sock.sendto(line.encode(), (ip, port))
                c_sock.sendto('EOFError'.encode(), (ip, port))
                print('Texto enviado')
                c_sock.close()
                break
            except KeyboardInterrupt:
                c_sock.sendto('KeyboardInterrupt'.encode(), (ip, port))
                c_sock.close()
                print('\nAdios')
                break
    except Exception:
        print('Error')
    


def tcp_protocol(ip, port):
    try:
        c_sock = socket.socket()
        c_sock.connect((ip, port))
        mezclas = int(input("Indica el tam: "))
        c_sock.recv()
        while True:
            print('Escribe')
            try:
                for line in sys.stdin:
                    c_sock.send(line.encode())
                c_sock.send('EOFError'.encode())
                c_sock.close()
                print('Texto enviado')
                break
            except KeyboardInterrupt:
                c_sock.send('KeyboardInterrupt'.encode())
                c_sock.close()
                print('\nAdios')
                break
    except Exception:
        print('Tremendo error hermano')


def main():
    parse = argparse.ArgumentParser('Cliente')
    parse.add_argument('-i', '--ipdirection', help='Indique la direccion IP', required=True,
                       type=str, action='store', default='localhost')
    parse.add_argument('-ps', '--port', help='Indique el puerto para comunicarte con el servidor',
                       required=True, type=int, action='store')
    parse.add_argument('-t', '--tprotocol', help='Indique el protocolo. process para procesos, y thread para hilo', required=True,
                       type=str, action='store')
    parse.add_argument('-thp', '--asincrony', help='Indique si quiere utilizar procesos para la generacion del server',
                       type=str, action='store')
    args = parse.parse_args()
    redisDB = redis.Redis(host='localhost', port=6379, db=0)
    redisDB.mset({'protocolo': args.tprocotol, 'asincronia': args.asincrony,
                  'puerto': args.port, 'direction': args.ipdirection})
    if args.tprotocol.lower() == 'udp':
        udp_protocol(args.aipdirection, args.port)
    elif args.tprotocol.lower() == 'tcp':
        tcp_protocol(args.aipdirection, args.port)
    else:
        print('Error')


if __name__ == '__main__':
    main()
