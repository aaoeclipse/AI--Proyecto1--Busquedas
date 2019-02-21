import numpy as np

global DIMENSION
class Estado:
    def __init__(self, tablero):
        global DIMENSION
        self.tablero = tablero
        self.numerosDisponibles = [[]]
        self.goal = False
        self.f = self.fun()
        pass
    def fun(self):
        return self.heuristica() + self.peso()
    def getCelda(self, pos):
        return self.tablero[pos]
    def heuristica(self, debug=0):
        # Calcular la heuristica
        # Posibilidad de numeros
        h = 0
        for cell in self.tablero:
            if(cell == '.'):
                h = h + 1
            else:

                if (self.numeroEnFila(debug)):
                    h = -1
                    return h
                if (self.numeroEnColuma(debug)):
                    h = -1
                    return h
                if (self.numeroEnCuadro(debug)):
                    h = -1
                    return h
        return h
    def numeroEnFila(self, debug=0):
        global DIMENSION
        counter = 0
        tmp = '.'
        for idx,cell in enumerate(self.tablero):
            if (idx % DIMENSION == 0):
                linea =  []
                for i in range(1,DIMENSION+1):
                    linea.append(str(i))
            if cell != '.':
                if cell in linea:
                    linea.remove(cell)
                else:
                    if debug == 1:
                        print('fila valor: {}'.format(cell))
                    return True
        return False
    def numeroEnColuma(self, debug=0):
        global DIMENSION
        for index in range(DIMENSION):
            nuevaTabla = []
            # Hard Coded
            nuevaTabla.append(self.tablero[0  + index])
            if (self.tablero[4 + index] in nuevaTabla and self.tablero[4 + index] != '.'):
                if debug == 1:
                        print('columna: {} con valor {}'.format(index, self.tablero[4 + index]))
                return True
            nuevaTabla.append(self.tablero[4 + index])
            if (self.tablero[8 + index] in nuevaTabla and self.tablero[8 + index] != '.'):
                if debug == 1:
                        print('columna: {} con valor {}'.format(index, self.tablero[8 + index]))
                return True
            nuevaTabla.append(self.tablero[8 + index])
            if (self.tablero[12 + index] in nuevaTabla and self.tablero[12 + index] != '.'):
                if debug == 1:
                        print('columna: {} con valor {}'.format(index, self.tablero[12 + index]))
                return True
        return False
    def numeroEnCuadro(self, debug=0):
        global DIMENSION
        for x in range(DIMENSION):
            c1 = []
            c1.append(self.tablero[0 + (x*2)])
            if (self.tablero[0 + DIMENSION + (x*2)] in c1 and self.tablero[0 + DIMENSION + (x*2)] != '.'):
                if debug == 1:
                        print('cuadro: {}'.format(x))          
                return True
            c1.append(self.tablero[0 + DIMENSION + (x*2)])
            if (self.tablero[1 + (x*2)] in c1 and self.tablero[1 + (x*2)] != '.'):
                if debug == 1:
                        print('cuadro: {}'.format(x))                         
                return True
            c1.append(self.tablero[1 + (x*2)])
            if (self.tablero[1+DIMENSION + (x*2)] in c1 and self.tablero[4+ DIMENSION + (x*2)] != '.'):
                if debug == 1:
                        print('cuadro: {}'.format(x))                          
                return True
        return False   
    def peso(self):
        return 4
    def printTablero(self):
        global DIMENSION
        print("   ", end="")
        for idx, var in enumerate(self.tablero):
            if (idx % DIMENSION == 0 and idx != 0):
                print('\n   ', end="")
                print(var, end="")
            else:
                print(var, end="")
        print('')


class Solver:
    def __init__(self, tablero):
        global DIMENSION
        DIMENSION = self.dimensiones(tablero)
        self.estado = Estado(list(tablero))
        self.caminosTomados = []
        self.posibleNumbers = {}
        for x in range(1,DIMENSION+1):
            self.posibleNumbers[str(x)] = DIMENSION
        self.pos = 0
        self.solver()
        """  
            1. Check Goal return if true
            2. Sacar posibles estados
            2.1 eliminar estados que ya fueron explorados
            2.2 Si no hay posibles estado para tomar entonces retroceder
            3. escoger el menor score y guardarlo en array caminosTomados
            3.1 Guardar los datos
            """
    def solver(self):
        counter = 0
        counterSkip = 0
        goal = False
        currentCamino = 0
        while(not goal):
            # 1. Check Goal return if true, return if true
            if (self.estado.goal == True):
                print('Goal found!')
                return
            # 2. Sacar posibles estados
            if(self.estado.getCelda(self.pos) != '.'):
                counterSkip = counterSkip + 1
                if (counterSkip > 9):
                    goal = True
                self.pos = self.pos + 1
            else:
                posiblesEstados = self.actions(self.estado)
                print('posibles estados {}'.format(len(posiblesEstados)))
                # 2.1 Eliminar estados que ya fueron explorados
                for estadoExplorado in self.caminosTomados:
                    for estadosEvaluando in posiblesEstados:
                        if (estadoExplorado.tablero == estadosEvaluando.tablero):
                            estadosEvaluando.printTablero()
                            posiblesEstados.remove(estadosEvaluando)
                print('posibles estados despues de remove {}'.format(len(posiblesEstados)))                
                # 2.2 Si no hay posibles estado para tomar entonces retroceder (hay que sacar otra lista nueva para decir el camino viejo tomado)
                if (len(posiblesEstados) == 0):
                    if (len(self.caminosTomados) > 0):
                        nuevoEstado = Estado(self.estado.tablero[:])
                        self.caminosTomados.append(nuevoEstado)
                        self.estado.tablero[self.pos] = '.'
                        counter = counter + 1
                        self.estadoTemporal = self.caminosTomados[currentCamino-counter]
                        self.estado =  self.estadoTemporal
                        self.pos = self.pos - 1
                        self.estado.tablero[self.pos] = '.'
                        # self.pos = self.pos - 1
                    else:
                        # print(self.caminosTomados[currentCamino])
                        print('Imposible de Resolver')
                        break
                    # self.pos = self.pos - 1
                # 3. Escoger el menor score y guardarlo en array caminosTomados
                else:
                    tmpEstado = Estado(self.estado.tablero[:])
                    for estado in posiblesEstados:
                        if (tmpEstado.f >= estado.f):
                            tmpEstado = estado
                    # 3.1 Guardar nuevos datos
                    self.estado = tmpEstado
                    self.caminosTomados.append(self.estado)
                    self.pos = self.pos + 1
                    counter = 0
                    # tmpEstado.printTablero()
                    if (self.pos == 15):
                        self.estado.goal = True
                    print('----')
                    self.estado.printTablero()
                    """ print('aAAAAAAAAAAAA')
                    for asdf in self.caminosTomados:
                        asdf.printTablero()
                        print('------') """
                    
        pass
    def actions(self, estado):
        global DIMENSION
        nuevosEstados = []
        # self.estado.tablero[self.estado.posicion]
        for key, value, in self.posibleNumbers.items():
            tablaCurr = self.estado.tablero [:]
            tmpEstado = Estado(tablaCurr)
            if (value > 0):
                tmpEstado.tablero[self.pos] = key
                print("*******")
                tmpEstado.printTablero()
                print("*******")
                # print(tmpEstado.heuristica())
                if (tmpEstado.heuristica() >= 0):
                    nuevosEstados.append(tmpEstado)
        return nuevosEstados
    def dimensiones(self, tablero):
        dimensionesFloat = np.sqrt(len(tablero))
        dimensiones = dimensionesFloat.astype(int)
        if ((dimensionesFloat % dimensiones) == 0):
            return dimensiones
        return -1
class Nodo:
    def __init__(self, pos, value=0, numPosibles=[]):
        self.pos = pos
        self.value = value
        self.numPosibles = numPosibles

# tablero = '1...2..4....3...'
tablero =   '1.....2..1..4..3'
solv = Solver(tablero)
