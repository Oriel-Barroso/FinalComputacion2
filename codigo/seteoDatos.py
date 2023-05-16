import redis
import argparse


class SetDataRedis():
    def __init__(self, identificacion='', host='', puerto='', protocolo='',
                 proceso='', ip=''):
        self.identificacion = identificacion
        self.host = host
        self.puerto = str(puerto)
        self.protocolo = protocolo
        self.proceso = proceso
        self.ip = ip

    def initRedis(self):
        return redis.Redis(host='localhost', port=6379, db=0)

    def setDatos(self):
        redis = self.initRedis()
        redis.hset(self.identificacion.capitalize(), mapping={
            "usuario": self.identificacion,
            "ip": self.ip,
            "host": self.host,
            "puerto": self.puerto,
            "protocolo": self.protocolo,
            "proceso": self.proceso
        })


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('-id', '--identificacion', help='Indique su'
                       ' nombre', type=str, action='store',
                       required=True)
    parse.add_argument('-ip', '--ipProtocol', help='Indique si usa ipv6 '
                       'o ipv4', type=str, action='store', default="ipv4")
    parse.add_argument('-i', '--ipdireccion', help='Indique la direccion IP',
                       type=str, action='store', default="localhost")
    parse.add_argument('-ps', '--puerto', help='Indique el puerto para'
                       'comunicarte con el servidor',
                       required=True, type=int, action='store')
    parse.add_argument('-t', '--protocolo', help='Indique el protocolo.'
                       'process para procesos, y thread para hilo',
                       required=True, type=str, action='store')
    parse.add_argument('-thp', '--procesamiento', help='Indique si quiere'
                       'utilizar procesos o hilos para la generacion del server',
                       type=str, action='store')
    args = parse.parse_args()
    setValues = SetDataRedis(args.identificacion, args.ipdireccion,
                             args.puerto, args.protocolo, args.procesamiento,
                             args.ipProtocol)
    setValues.setDatos()
    print('Datos ingresados correctamente!. Ahora puede utilizarlos en el '
          'servidor y el cliente')
