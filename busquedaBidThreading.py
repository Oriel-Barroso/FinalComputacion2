#from queue import Queue
import sys 
from threading import Barrier as barr, Lock
import threading
import random
COLA_INICIAL = {}
COLA_FINAL = {}
CHECK = False
lock = threading.Lock()


def crearPuzzle(tamañoMatriz):
    puzzleInicial = []
    for i in range(0, tamañoMatriz-1):
        puzzleInicial.append(i+1)
    puzzleInicial.append(0)
    return puzzleInicial

def crear_grafo(largo):
    grafo = {}
    for i in range(0, largo):
        grafo[i] = []
    filas, columnas = int(largo ** 0.5), int(largo ** 0.5)
    for i in range(filas):
        for j in range(columnas):
            indice = i * columnas + j
            if i > 0:
                grafo[indice].append((i - 1) * columnas + j)  
            if i < filas - 1:
                grafo[indice].append((i + 1) * columnas + j)  
            if j > 0:
                grafo[indice].append(i * columnas + (j - 1))  
            if j < columnas - 1:
                grafo[indice].append(i * columnas + (j + 1))  
            grafo[indice].sort() 
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
    global CHECK
    tomarLista = 0
    contadorSoluciones = 0
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
        check()
        if CHECK:
            break
        #check()
        
        
        
def check():
    global COLA_INICIAL, COLA_FINAL, CHECK
    with lock:
        for k1,v1 in COLA_INICIAL.items():
            for k2,v2 in COLA_FINAL.items():
                if v1 == v2 and k1 != 0 and k2 != 0 and CHECK is False:
                        print('Coinciden!')
                        print('Valor: ', v1, ', Nodo de la lista inicial: ', k1, ', Nodo de la lista final: ', k2)
                        CHECK = True
                        return

def main():
    global COLA_INICIAL, COLA_FINAL, CHECK
    threadsList = []
    tamañoMatriz = int(input('Indica tamaño de la matriz: '))**2
    puzzleInicial = crearPuzzle(tamañoMatriz)
    grafo = crear_grafo(len(puzzleInicial))
    puzzleFinal = crear_random(grafo, puzzleInicial)
    COLA_INICIAL = {0:puzzleInicial}
    COLA_FINAL = {0:puzzleFinal}
    colas = [COLA_INICIAL, COLA_FINAL]
    bar1 = barr(2)
    for cola in colas:
        threads = threading.Thread(target=busquedaBid, args=(cola, grafo, bar1))
        threadsList.append(threads)
        threadsList[-1].start()
    for thread in threadsList:
        thread.join()


if __name__ == '__main__':
    main()