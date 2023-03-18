#from queue import Queue
from threading import Barrier as barr
import threading
import random
COLA_INICIAL = {}
COLA_FINAL = {}


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

def crear_random(grafo, puzzle):
    tomarLista = 0
    contadorSoluciones = 0
    diccionarioAnchura = {0:puzzle.copy()}
    random_val = random.randint(0,100)
    while tomarLista != random_val:          
        nodo = diccionarioAnchura.get(tomarLista).index(0)
        for neighbour in grafo[nodo]:
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

def busquedaBid(cola, grafo, bar):
    tomarLista = 0
    contadorSoluciones = 0
    while True:
        while True:
            bar.wait()
            nodo1 = cola.get(tomarLista).index(0)
            for neighbour in grafo[nodo1]:
                listaAux = cola.get(tomarLista).copy()
                valorAux = listaAux[neighbour]
                indCero = listaAux.index(0)
                listaAux[neighbour] = 0
                listaAux[indCero] = valorAux
                if listaAux not in cola.values(): #no guardar valores que ya esten
                    contadorSoluciones+=1
                    cola[contadorSoluciones]=listaAux
            tomarLista += 1
            bar.wait()
            valCheck = check()
            if valCheck is True:
                break
        break
        

def check():
    global COLA_INICIAL, COLA_FINAL
    for k1,v1 in COLA_INICIAL.items():
        for k2,v2 in COLA_FINAL.items():
            if v1 == v2 and k1 != 0 and k2 != 0:
                print('Coinciden!')
                print('Valor: ', v1, ', Nodo de la lista inicial: ', k1, ', Nodo de la lista final: ', k2)
                return True

def main():
    global COLA_INICIAL, COLA_FINAL
    threadsList = []
    puzzleInicial = [1,2,3,4,5,6,7,8,0]
    grafo = crear_grafo(puzzleInicial)
    puzzleFinal = crear_random(grafo, puzzleInicial)
    COLA_INICIAL = {0:puzzleInicial}
    COLA_FINAL = {0:puzzleFinal}
    colas = [COLA_INICIAL, COLA_FINAL]
    bar = barr(2)
    for cola in colas:
        threads = threading.Thread(target=busquedaBid, args=(cola, grafo, bar))
        threadsList.append(threads)
    for thread in threadsList:
        if thread.is_alive() is False:
            thread.start()
        """bar.wait()
        for k1,v1 in cola_inicial.items():
            for k2,v2 in cola_final.items():
                if v1 == v2 and k1 != 0 and k2 != 0:
                    print('Coinciden!')
                    print('Valor: ', v1, ', Nodo de la lista inicial: ', k1, ', Nodo de la lista final: ', k2)
                    break
        bar.wait()
        break"""
    for thread in threadsList:
        thread.join()
    print('x')



if __name__ == '__main__':
    main()