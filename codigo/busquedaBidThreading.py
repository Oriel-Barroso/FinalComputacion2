# from queue import Queue
from threading import Lock, Barrier as barr
import threading
import random
COLA_INICIAL = {}
COLA_FINAL = {}
CHECK = False
lock = Lock()


class BusquedaBidireccional():
    def __init__(self, tamañoMatriz):
        self.tamañoMatriz = tamañoMatriz**2
        self.grafo = {}
        self.puzzleInicial = []
        self.puzzleFinal = []
        self.resultado = ''

    def __str__(self):
        print('El valor del tamaño de matriz es: ', self.tamañoMatriz)

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

    def busquedaBid(self, cola, bar):
        global CHECK
        tomarLista = 0
        contadorSoluciones = 0
        while True:
            bar.wait()
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
            bar.wait()
            self.check()
            if CHECK:
                break

    def check(self):
        global COLA_INICIAL, COLA_FINAL, CHECK
        with lock:
            if CHECK is False:
                for k1, v1 in COLA_INICIAL.items():
                    for k2, v2 in COLA_FINAL.items():
                        if v1 == v2:
                            self.resultado = 'Coinciden!, Valor: ', v1, 'Nodo de la lista inicial: ', k1, ', Nodo de la lista final: ', k2
                            CHECK = True
                            return

    def run(self):
        global COLA_INICIAL, COLA_FINAL, CHECK
        self.crearPuzzle()
        self.crear_grafo()
        self.crear_random()
        COLA_INICIAL = {0: self.puzzleInicial}
        COLA_FINAL = {0: self.puzzleFinal}
        colas = [COLA_INICIAL, COLA_FINAL]
        bar = barr(2)
        threadsList = []
        for cola in colas:
            threads = threading.Thread(target=self.busquedaBid, args=(cola,
                                                                      bar))
            threadsList.append(threads)
            threadsList[-1].start()
        for thread in threadsList:
            thread.join()
        return self.resultado
