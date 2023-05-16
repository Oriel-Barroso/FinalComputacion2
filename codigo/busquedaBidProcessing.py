from multiprocessing import Lock, Process, Manager, Value
import random


class BusquedaBidireccionalProcess():
    def __init__(self, tamañoMatriz):
        self.tamañoMatriz = tamañoMatriz**2
        self.grafo = {}
        self.puzzleInicial = []
        self.puzzleFinal = []
        self.resultado = ''
        self.checkD = False
    
    def crearPuzzle(self):
        for i in range(0, self.tamañoMatriz-1):
            self.puzzleInicial.append(i+1)
        self.puzzleInicial.append(0)

    def crear_grafo(self):
        largo = len(self.puzzleInicial)
        for i in range(0, largo):
            self.grafo[i] = []
        filas, columnas = int(largo ** 0.5), int(largo ** 0.5)
        for i in range(filas):
            for j in range(columnas):
                indice = i * columnas + j
                if i > 0:
                    self.grafo[indice].append((i - 1) * columnas + j)
                if i < filas - 1:
                    self.grafo[indice].append((i + 1) * columnas + j)
                if j > 0:
                    self.grafo[indice].append(i * columnas + (j - 1))
                if j < columnas - 1:
                    self.grafo[indice].append(i * columnas + (j + 1))
                self.grafo[indice].sort()

    def crear_random(self):
        tomarLista = 0
        contadorSoluciones = 0
        diccionarioAnchura = {0: self.puzzleInicial.copy()}
        random_val = random.randint(5, 100)
        while tomarLista != random_val:
            nodo = diccionarioAnchura.get(tomarLista).index(0)
            for neighbour in self.grafo[nodo]:
                listaAux = diccionarioAnchura.get(tomarLista).copy()
                valorAux = listaAux[neighbour]
                indCero = listaAux.index(0)
                listaAux[neighbour] = 0
                listaAux[indCero] = valorAux
                if listaAux not in diccionarioAnchura.values():  # no guardar valores que ya esten
                    contadorSoluciones += 1
                    diccionarioAnchura[contadorSoluciones] = listaAux
            tomarLista += 1
        self.puzzleFinal = diccionarioAnchura.get(list(diccionarioAnchura.keys())[-1])

    def busquedaBid(self, cola, lock, resultado, check_flag):
        tomarLista = 0
        contadorSoluciones = 0
        while True:
            nodo1 = cola.get(tomarLista).index(0)
            for neighbour in self.grafo[nodo1]:
                listaAux = cola.get(tomarLista).copy()
                valorAux = listaAux[neighbour]
                indCero = listaAux.index(0)
                listaAux[neighbour] = 0
                listaAux[indCero] = valorAux
                if listaAux not in cola.values():  # no guardar valores que ya esten
                    contadorSoluciones += 1
                    cola[contadorSoluciones] = listaAux
            tomarLista += 1
            self.check(lock, resultado, check_flag)
            if check_flag.value:
                break

    def check(self, lock, resultado, check_flag):
        global COLA_INICIAL, COLA_FINAL
        with lock:
            if not check_flag.value:
                for k1, v1 in COLA_INICIAL.items():
                    for k2, v2 in COLA_FINAL.items():
                        if v1 == v2:
                            resultado.append(('Coinciden!, Valor: ', v1, 'Nodo de la lista inicial: ', k1, ', Nodo de la lista final: ', k2))
                            check_flag.value = 1
                            return

    def run(self):
        global COLA_INICIAL, COLA_FINAL
        manager = Manager()
        # self.puzzleInicial = [1,2,3,4,5,6,7,8,0]
        # self.puzzleFinal = [1,2,3,4,0,6,7,5,8]
        # self.crear_grafo()
        # print(self.grafo)
        self.crearPuzzle()
        self.crear_grafo()
        self.crear_random()
        COLA_INICIAL = manager.dict({0: self.puzzleInicial})
        COLA_FINAL = manager.dict({0: self.puzzleFinal})
        colas = [COLA_INICIAL, COLA_FINAL]
        lock = Lock()
        resultado = manager.list()
        check_flag = Value('i', 0)
        processes = []
        for cola in colas:
            process = Process(target=self.busquedaBid, args=(cola, lock,
                              resultado, check_flag))
            processes.append(process)
            processes[-1].start()
        for process in processes:
            process.join()
        return resultado

# if __name__ == "__main__":
#     s = BusquedaBidireccionalProcess(3)
#     print(s.run())