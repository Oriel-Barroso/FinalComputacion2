import time
import random

class busquedaBidireccional:
    def __init__(self, largo):
        self.diccionario_anchuraInicial = {}
        self.diccionario_anchuraFinal = {}
        self.grafo = {}
        for i in range(0, largo):
            self.grafo[i] = list()

    def agregarNodo(self, clave, valor):
        for k,v in self.grafo.items():
            if clave == k:
                v.append(valor)

    def metodoSolucion(self, puzzleInicial, puzzleFinal):
        sentido = ['adelante', 'atras']
        self.diccionario_anchuraInicial = {0: puzzleInicial.copy()}
        self.diccionario_anchuraFinal = {0: puzzleFinal.copy()}
        tomarLista1 = 0
        contadorSoluciones1 = 0
        tomarLista2 = 0
        contadorSoluciones2 = 0
        while True:
            if sentido[0] == 'adelante':
                nodo1 = self.diccionario_anchuraInicial.get(tomarLista1).index(0) #Se fija en donde se encuentra el 0, y de aqui determinamos sus vecinos
                for neighbour in self.grafo[nodo1]:
                    listaAux = self.diccionario_anchuraInicial.get(tomarLista1).copy()
                    valorAux = listaAux[neighbour]
                    indCero = listaAux.index(0)
                    listaAux[neighbour] = 0
                    listaAux[indCero] = valorAux
                    if listaAux not in self.diccionario_anchuraInicial.values(): #no guardar valores que ya esten
                        contadorSoluciones1 += 1
                        self.diccionario_anchuraInicial[contadorSoluciones1] = listaAux
                tomarLista1 += 1
            if sentido[1] == 'atras':
                nodo2 = self.diccionario_anchuraFinal.get(tomarLista2).index(0)
                for neighbour in self.grafo[nodo2]:
                    listaAux = self.diccionario_anchuraFinal.get(tomarLista2).copy()
                    valorAux = listaAux[neighbour]
                    indCero = listaAux.index(0)
                    listaAux[neighbour] = 0
                    listaAux[indCero] = valorAux
                    if listaAux not in self.diccionario_anchuraFinal.values(): #no guardar valores que ya esten
                        contadorSoluciones2 +=1
                        self.diccionario_anchuraFinal[contadorSoluciones2] = listaAux
                tomarLista2 += 1
            s = self.check()
            if s is True:
                break

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

def main():
    busqueda = busquedaBidireccional(largo=9) #Defino el largo de la matriz
    busqueda.agregarNodo(0, 1)
    busqueda.agregarNodo(0, 3)
    busqueda.agregarNodo(1, 0)
    busqueda.agregarNodo(1, 2)
    busqueda.agregarNodo(1, 4)
    busqueda.agregarNodo(2, 1)
    busqueda.agregarNodo(2, 5)
    busqueda.agregarNodo(3, 0)
    busqueda.agregarNodo(3, 4)
    busqueda.agregarNodo(3, 6)
    busqueda.agregarNodo(4, 1)
    busqueda.agregarNodo(4, 3)
    busqueda.agregarNodo(4, 5)
    busqueda.agregarNodo(4, 7)
    busqueda.agregarNodo(5, 2)
    busqueda.agregarNodo(5, 4)
    busqueda.agregarNodo(5, 8)
    busqueda.agregarNodo(6, 3)
    busqueda.agregarNodo(6, 7)
    busqueda.agregarNodo(7, 4)
    busqueda.agregarNodo(7, 6)
    busqueda.agregarNodo(7, 8)
    busqueda.agregarNodo(8, 5)
    busqueda.agregarNodo(8, 7)
    puzzleInicial = [1,2,3,4,5,6,7,8,0]
    puzzleFinal = busqueda.crear_random(puzzleInicial)
    print(puzzleFinal)
    start = time.time()
    busqueda.metodoSolucion(puzzleInicial, puzzleFinal)
    end = time.time()
    print('El tiempo que demora: ',end - start)

if __name__ == '__main__':
    main()
