import sys, argparse, socket, redis, time


def udp_protocol(ip, port):
    c_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('linea escrita:', line)
    c_sock.sendto(line.encode(), (ip, port))
    print('Texto enviado')
    c_sock.close()


def tcp_protocol(ip, port, tamaño):
    c_sock = socket.socket()
    c_sock.connect((ip, port))
    c_sock.send(tamaño.encode(str(tamaño)))
    res = c_sock.recv(1024).decode()
    print('El resultado es: ', res)
    c_sock.close()


def convetirLista(args):
    return [args.ipdirection, args.port, args.tprotocol, args.asincrony]


def agregarUsuario(db, usuario):
    usuarios = [usuarioInlista.decode() for usuarioInlista in
                list(db.smembers('Usuarios'))]  # Ver si el usuario ya existe
    if usuario not in usuarios:
        db.sadd("Usuarios", usuario)
        return True
    return False


def main():
    redisDB = redis.Redis(host='localhost', port=6379, db=0)
    parse = argparse.ArgumentParser('Cliente')
    parse.add_argument('-id', '--identificacion', help='Indique su'
                       ' nombre', type=str, action='store',
                       required=True)
    parse.add_argument('-i', '--ipdirection', help='Indique la direccion IP',
                       required=True, type=str, action='store',
                       default='localhost')
    parse.add_argument('-ps', '--port', help='Indique el puerto para comunicarte con el servidor',
                       required=True, type=int, action='store')
    parse.add_argument('-t', '--tprotocol', help='Indique el protocolo. process para procesos, y thread para hilo', required=True,
                       type=str, action='store')
    parse.add_argument('-thp', '--asincrony', help='Indique si quiere utilizar procesos para la generacion del server',
                       type=str, action='store')
    parse.add_argument('-tam', '--tamaño', help='Indique el tamaño de la matriz: 3,4,5... . (default 3x3)',
                       type=int, action='store')
    args = parse.parse_args()
    print('Procesando argumentos...')
    time.sleep(1)
    if agregarUsuario(redisDB, args.identificacion) is False:
        print('El usuario ya existe, abortando...')
        sys.exit()
    listaArgs = convetirLista(args)
    redisDB.set('parametros', listaArgs)
    if args.tprotocol.lower() == 'udp':
        udp_protocol(args.aipdirection, args.port, args.tamaño)
    elif args.tprotocol.lower() == 'tcp':
        tcp_protocol(args.aipdirection, args.port, args.tamaño)
    else:
        print('Error')


if __name__ == '__main__':
    main()
