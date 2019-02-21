# Importaciones
import numpy as np

# Variables Globales
global DIMENSION
""" Estado """
class Estado:
    """ El estado es la posicion del tablero [1:n, '.'] """
    def __init__(self, tablero):
        self.tablero = tablero
        self.goal = False
        self.g = self.getScore()
        
    def getScore(self):
        score = 0 
        # g = h + c
        score = self.heuristica() + self.costo()
        if (score == 1): # si el score es igual a 1 significa que la heuristica es 0
            self.goalReached()
            return -1 # aqui -1 se va a significar que termino el programa, llego a su meta
        return score

    def heuristica(self):
        # Manhattan (|x_f-x_i| + |y_f-y_i|) -> como solo es de 1 dimension (|xf - xi|)
        h = 0
        for idx, cuadro in enumerate(self.tablero):
            h = h + self.getManhattanOfSquare(cuadro,idx+1)
        return h

    def getManhattanOfSquare(self, cuadro, xi):
        score = 0
        if (cuadro == '.'):
            return score
        try:
            xf = int(cuadro)
            score = abs(xf - xi)
        except:
            try:
                xf = ord(cuadro) - 55 # 65 es A = 10, B tiene que ser 11 y es 66. Numero = x - 55
                score = abs(xf - xi)
            except:
                print('ERROR: No es un numero deseablo')
        return score

    def costo(self):
        # El costo de movimiento siempre va a ser 1
        return 1

    def goalReached(self):
        self.goal = True

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

""" Solver """
class Solver:
    def __init__(self, tableroInicial):
        # String -> Lista
        tablero = list(tableroInicial)
        # Dimensiones
        global DIMENSION
        DIMENSION = self.dimensiones(tableroInicial)
        if DIMENSION == -1:
            print("Tablero No Cuadrado")
            return
        # Variables de la clase
        self.instrucciones = []
        self.explorados = []
        self.estado = Estado(tablero)     
        self.estadoTemporal = Estado(tablero)
        # El Solver   
        self.solve()

    def solve(self):
        goal = False
        while (not goal):
            """  
            1. Check Goal return if true
            2. Sacar posibles estados
            2.1 eliminar estados que ya fueron explorados
            2.2 Si no hay posibles estado para tomar entonces retroceder
            3. escoger el menor score y guardarlo en array caminosTomados, si es -1, goal = true y salir. Si no, agregar a explorados
             """
            # 1. Check Goal return if true
            if self.estado.goal:
                print("Goal!")
                goal = True
                for i in range(len(self.instrucciones)):
                    print('{}. {}'.format(i+1,self.instrucciones[i]))
                    print('-----------')
                    self.explorados[i].printTablero()
                    print('')
                break
            # 2. Sacar posibles estados
            posiblesEstadosConInstrucciones = self.actions(self.estado.tablero) # (estado, instruccion)
            # 2.1 eliminar estados que ya fueron explorados
            for estadoExplorado in self.explorados:
                for estadosEvaluando in posiblesEstadosConInstrucciones:
                    if (estadoExplorado.tablero == estadosEvaluando[0].tablero or estadosEvaluando[0].tablero == self.estadoTemporal.tablero):
                        # print("Estado explorado!")
                        posiblesEstadosConInstrucciones.remove(estadosEvaluando)
            # 2.2 Si no hay posibles estado para tomar entonces retroceder
            if (len(posiblesEstadosConInstrucciones) == 0):
                if (len(self.estado.tablero) != 0):
                    self.estadoTemporal = self.explorados.pop()
                    self.estado = self.explorados[-1]
                    self.instrucciones.pop()
                else:
                    print('Imposible de Resolver!')
                # print(self.instrucciones.pop())
                # print('Imposible de Resolver!')
                # return self.instrucciones
            # 3. escoger el menor score y guardarlo en array caminosTomados, si es -1, goal = true y salir. Si no, agregar a explorados
            else:
                tmpEstado = self.estado
                tmpEstado.g = 10000 # necesitamos un alto score para que avance
                tmpInstruccion = 'None'
                for estado in posiblesEstadosConInstrucciones:
                    if (tmpEstado.g >= estado[0].g):
                        tmpEstado = estado[0]
                        tmpInstruccion = estado[1]
                # 4. Guardar nuevos datos
                self.estado = tmpEstado
                self.instrucciones.append(tmpInstruccion)
                self.explorados.append(self.estado)
                # 5. Debug
                # print(self.instrucciones[-1])
                # self.estado.printTablero()
        pass

    def actions(self, tablero):
        global DIMENSION
        estados = []
        # cuales son las posibles acciones
        # cada una de estas va a crear un child para comparar el costo y la heuristica con cada una
        switcher = {
            0 : 'Left',
            1 : 'Up',
            2 : 'Right',
            3 : 'Down'
        }
        posicionDel0 = self.posicionCero(tablero)
        if (posicionDel0 == 0):
            # 1 casilla
            del switcher[0]
            del switcher[1]
        elif (posicionDel0 % DIMENSION == 0):
            # primera casilla de la row
            del switcher[0]
        elif (posicionDel0 <= DIMENSION):
            # primer row
            del switcher[1]
        if (posicionDel0 == len(tablero)-1):
            # Ultima casilla
            del switcher[2]
            del switcher[3]
        elif (posicionDel0 >= DIMENSION*(DIMENSION-1)):
            # ultimo row
            del switcher[3]
        elif (posicionDel0 % DIMENSION == DIMENSION-1):
            # ultima casilla del row
            del switcher[2]
        for option in switcher:
            estados.append((self.swap(posicionDel0, option, tablero), switcher[option]))
        return estados
    
    def swap(self, pos0, option, tablero):
        global DIMENSION
        newTablero = tablero[:]
        # Swap dos cuadros
        if (option == 0): # left
            celdaRemplazar = pos0 - 1
            # print('left')
        elif (option == 1): # Up
            celdaRemplazar = pos0 - DIMENSION
            # print('Up')
        elif (option == 2): # Right
            celdaRemplazar = pos0+1
            # print('Right')
        elif (option == 3): # Down
            celdaRemplazar = pos0 + DIMENSION
            # print('Down')
        else:
            celdaRemplazar = pos0
            print('Error')
        # print('pos0:{}, Celda #{}, instruccion:{}'.format(pos0, celdaRemplazar, option))
        newTablero[pos0] = newTablero[celdaRemplazar]
        newTablero[celdaRemplazar] = '.'
        nuevoEstado = Estado(newTablero)
        return nuevoEstado
    
    def posicionCero(self, tablero):
        # Encontrar el 0 en la tabla
        return tablero.index('.')
        
    def dimensiones(self, tablero):
        dimensionesFloat = np.sqrt(len(tablero))
        dimensiones = dimensionesFloat.astype(int)
        if ((dimensionesFloat % dimensiones) == 0):
            return dimensiones
        return -1
# 15 puzzle
# test = '2.B3157496C8DAEF'     # Hard
# test = '51437928BD6CFE.A'   # Medium
# test= '123456789AE.BDFC'    # simple test
# 8 puzzle
test = '45618237.'
# test = '35214.867'
puzzle = Solver(test)