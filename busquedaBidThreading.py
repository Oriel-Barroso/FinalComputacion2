from queue import Queue
from threading import Barrier as bar
import threading
import random

def crear_grafo(lista):
    largo = len(lista)
    grafo = {}
    for i in range(0, largo):
        grafo[i] = []
    filas, columnas = int(largo ** 0.5), int(largo ** 0.5)
    for i in range(filas):
        for j in range(columnas):
            indice = i * columnas + j
            if i > 0:
                grafo[indice].append((i - 1) * columnas + j)  # agrega el vecino de arriba
            if i < filas - 1:
                grafo[indice].append((i + 1) * columnas + j)  # agrega el vecino de abajo
            if j > 0:
                grafo[indice].append(i * columnas + (j - 1))  # agrega el vecino de la izquierda
            if j < columnas - 1:
                grafo[indice].append(i * columnas + (j + 1))  # agrega el vecino de la derecha
            grafo[indice].sort()  # ordena la lista de vecinos
    return grafo

def check(self):
    for k1,v1 in self.diccionario_anchuraInicial.items():
        for k2,v2 in self.diccionario_anchuraFinal.items():
            if v1 == v2 and k1 != 0 and k2 != 0:
                print('Coinciden!')
                print('Valor: ', v1, ', Nodo de la lista inicial: ', k1, ', Nodo de la lista final: ', k2)
                return True

def crear_random(self, puzzle):
    tomarLista = 0
    contadorSoluciones = 0
    diccionarioAnchura = {0:puzzle.copy()}
    random_val = random.randint(0,100)
    while tomarLista != random_val:          
        nodo = diccionarioAnchura.get(tomarLista).index(0)
        for neighbour in self.grafo[nodo]:
            listaAux = diccionarioAnchura.get(tomarLista).copy()
            valorAux = listaAux[neighbour]
            indCero = listaAux.index(0)
            listaAux[neighbour] = 0
            listaAux[indCero] = valorAux
            if listaAux not in diccionarioAnchura.values(): #no guardar valores que ya esten
                contadorSoluciones +=1
                diccionarioAnchura[contadorSoluciones] = listaAux
        tomarLista += 1
    return diccionarioAnchura.get(list(diccionarioAnchura.keys())[-1])

def busquedaBid(cola, grafo):
    tomarLista = 0
    contadorSoluciones1 = 0
    while True:
        nodo1 = cola.get()[tomarLista].index(0)
        for neighbour in grafo[nodo1]:
            listaAux = cola.get()[tomarLista].copy()
            valorAux = listaAux[neighbour]
            indCero = listaAux.index(0)
            listaAux[neighbour] = 0
            listaAux[indCero] = valorAux
            queueAux = cola.get()
            if listaAux not in queueAux.values(): #no guardar valores que ya esten
                queueAux[contadorSoluciones1+1]=listaAux
                cola.put(queueAux)
        tomarLista += 1

def main():
    threadsList = []
    puzzleInicial = [1,2,3,4,5,6,7,8,0]
    puzzleFinal = crear_random(puzzleInicial)
    cola_inicial = Queue()
    cola_inicial.put({0:puzzleInicial})
    cola_final = Queue()
    cola_final.put({0:puzzleFinal})
    grafo = crear_grafo(puzzleInicial)
    colas = [cola_inicial, cola_final]
    for cola in colas:
        threads = threading.Thread(target=busquedaBid, args=(colas[cola], grafo))
        threadsList.append(threads)
    while True:
        for thread in threadsList:
            if thread.is_alive() is False:
                thread.start()
        bar.wait()
        for k1,v1 in self.diccionario_anchuraInicial.items():
            for k2,v2 in self.diccionario_anchuraFinal.items():
                if v1 == v2 and k1 != 0 and k2 != 0:
                    print('Coinciden!')
                    print('Valor: ', v1, ', Nodo de la lista inicial: ', k1, ', Nodo de la lista final: ', k2)
                    return True
        break
    for thread in threadsList:
        thread.join()