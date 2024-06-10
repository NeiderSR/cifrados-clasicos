class CurvaElipticaModular:
    '''Representa una curva elíptica definida sobre un número primo. Contiene
    además operaciones usadas en la criptografía de curva elíptica modular.'''

    p = None
    a = None
    b = None
    puntos = []

    def __init__(self, primo_p, const_a, const_b):
        '''Inicializa una curva elíptica con los valores especificados.

        :param const_a: el valor de la constante A en la definición de la curva.
        :param const_b: el valor de la constante B en la definición de la curva.
        :param primo_p: el valor del primo sobre el que se define la curva.
        :raises ValueError: si el número PRIMO_P no es primo, o si el
                determinante de la curva es cero.'''

        if not es_primo(primo_p):
            raise ValueError('El valor primo_p especificado no es primo.')
        
        #if CurvaElipticaModular.curva_discriminante(const_a, const_b, primo_p) == 0:
        #    raise ValueError('La curva no es válida: el discriminante de la curva no es cero.')
        
        self.p = primo_p
        self.a = const_a
        self.b = const_b
        self.puntos = CurvaElipticaModular.soluciones_curva(const_a, const_b, primo_p)

    def es_punto(self, punto):
        '''Determina si el punto especificado es parte de la curva elíptica.
        
        :param punto: el punto que se desea verificar si es parte de la curva.
        :returns: True si el punto es parte de la curva, False en otro caso.'''

        return es_punto(punto, self.a, self.b, self.p)

    def suma_puntos(self, punto1, punto2):
        '''Calcula la suma de los puntos especificados, que estan sobre esta
        curva eliptica.

        :param punto1: el primer punto a sumar.
        :param punto2: el segundo punto a sumar.
        :returns: el punto sobre la curva, resultante de sumar punto1 y
                  punto2.'''

        if punto1 not in self.puntos or punto2 not in self.puntos:
            raise ValueError('Los puntos especificados no forman parte de la curva.')

        if punto1.x == punto2.x and punto1.y != punto2.y:
            return Punto(float('inf'), float('inf'))    # Punto al infinito
        elif punto1.x == punto2.x and punto1.y == punto2.y and punto1.y == 0:
            return Punto(float('inf'), float('inf'))
        else:
            val_lambda = 0
            if punto1.x == punto2.x and punto1.y == punto2.y:
                val_lambda = ((3 * (punto1.x ** 2)) + self.a) * inverso(2 * punto1.y, self.p)
            else:
                val_lambda = (punto2.y - punto1.y) * inverso(punto2.x - punto1.x, self.p)
            x3 = cong_mod_M((val_lambda ** 2) - punto1.x - punto2.x, self.p)
            y3 = cong_mod_M((val_lambda * (punto1.x - x3)) - punto1.y, self.p)
            return Punto(x3, y3)

    def exp_puntos(self, punto, n):
        '''Realiza el producto/exponenciación del punto especificado, es decir,
        la suma del punto iterada sobre sí mismo N veces, en esta curva
        eliptica.

        :param punto: el punto que se desea operar.
        :param n: la cantidad de veces que se hará la iteración.
        :returns: el punto resultante de hacer la operación.'''

        if punto not in self.puntos:
            raise ValueError('El punto especificado no forma parte de la curva.')

        parcial = Punto(punto.x, punto.y)
        for i in range(1, n):
            parcial = self.suma_puntos(parcial, punto)
        return parcial

    def logaritmo(self, punto1, punto2):
        '''Calcula el logaritmo discreto para los puntos especificados usando
        fuerza bruta, es decir, el valor K tal que punto1 = K * punto2, en esta
        curva eliptica.

        :param punto1: el punto que se desea igualar.
        :param punto2: la base del logaritmo que se desea encontrar.
        :returns: el valor numérico del logaritmo discreto.'''

        if punto1 not in self.puntos or punto2 not in self.puntos:
            raise ValueError('Los puntos especificados no forman parte de la curva.')

        i = 1
        while(True):
            prueba = self.exp_puntos(punto2, i)
            if prueba == punto1:
                return i
            i += 1

    def orden(self, punto):
        '''Obtiene el orden del punto especificado, en esta curva elíptica.

        :param punto: el punto al que se desea obtener su orden
        :returns: el entero que representa el orden del punto.'''

        i = 1
        while True:
            prueba = self.exp_puntos(punto, i)
            if prueba.es_infinito():
                return i
            i += 1

    @staticmethod
    def curvas_validas(p):
        '''Obtiene un listado de las posibles combinaciones de valores A y B que
        definen curvas validas para el valor primo P especificado.

        :param p: el numero primo sobre el cual se define la curva.
        :returns: la lista de pares (A, B) que definen curvas elipticas sobre P
        (el discriminante no es 0).'''

        pares = []
        for i in range(0, p):
            for j in range(0, p):
                if CurvaElipticaModular.curva_discriminante(i, j, p) != 0:
                    pares.append((i, j))
        return pares

    @staticmethod
    def curvas_invalidas(p):
        '''Obtiene un listado de las posibles combinaciones de valores A y B que
        no producen curvas válidas para el valor primo P especificado.

        :param p: el numero primo sobre el cual se define la curva.
        :returns: la lista de pares (A, B) que definen curvas elipticas sobre P
        (el discriminante no es 0).'''

        pares = []
        for i in range(0, p):
            for j in range(0, p):
                if CurvaElipticaModular.curva_discriminante(i, j, p) == 0:
                    pares.append((i, j))
        return pares

    @staticmethod
    def curva_discriminante(a, b, p):
        '''Calcula el discriminante de la curva definida sobre P, dados los
        valores constantes de A y B.
    
        :param a: un entero que representa la constante A.
        :param b: un entero que representa la constante B.
        :param p: un entero que representa el primo P sobre el que se define la
                  curva.
        :returns: el valor del discriminante en la curva.'''

        return cong_mod_M((4 * (a ** 3)) + (27 * (b ** 2)), p)

    @staticmethod
    def soluciones_curva(a, b, p):
        '''Calcula las soluciones para la curva eliptica especificada.

        :param a: la constante A de la curva eliptica.
        :param b: la constante B de la curva eliptica.
        :param p: el primo sobre el cual se define la curva.
        :returns: la lista de puntos que son soluciones a la curva
        especificada.'''

        puntos = []
        for i in range(0, p):
            for j in range(0, p):
                punto_prueba = Punto(i, j)
                if CurvaElipticaModular.es_punto(punto_prueba, a, b, p):
                    puntos.append(Punto(i, j))
        return puntos

    @staticmethod
    def es_punto(punto, a, b, p):
        '''Determina si el punto especificado es parte de la curva eliptica.

        :param punto: el punto que se desea verificar si es parte de la curva.
        :param a: el valor numérico de la constante A de la curva.
        :param b: el valor numérico de la constante B de la curva.
        :param p: el número primo sobre el que se define la curva.
        :returns: True si el punto es parte de la curva, False en otro caso.'''

        lhs = pow(punto.y, 2, p)
        rhs = cong_mod_M((punto.x ** 3) + (a * punto.x) + b, p)
        return lhs == rhs

class Punto:
    '''Representa un punto en el plano, con coordenadas X y Y. Usado en las
    operaciones de curvas elípticas.'''
    
    x = None
    y = None

    def __init__(self, coord_x, coord_y):
        '''Inicializa un nuevo punto, con las coordenadas especificadas.

        :param coord_x: el valor numérico de la coordenada x.
        :param coord_y: el valor numérico de la coordenada y. '''
        
        self.x = coord_x
        self.y = coord_y

    def __str__(self):
        '''Representación en String de un punto.

        :returns: una cadena con la representación del punto.'''

        return f'({self.x}, {self.y})'

    def __eq__(self, punto):
        '''Verifica si dos puntos son iguales. Dos puntos son iguales si sus
        coordenadas con las mismas.'''

        return self.x == punto.x and self.y == punto.y

    def es_infinito(self):
        '''Verifica si el punto representa al punto al infinito, es decir, el
        neutro aditivo para los puntos en una curva elíptica.

        :returns: True si el punto es el punto al infinito, False en otro
        caso.'''

        return self.x == float('inf') and self.y == float('inf')

# ------------------------------------------------------------------------------
# --                     Funciones de aritmética modular                      --
# ------------------------------------------------------------------------------

def es_primo(n):
    '''Determina si N es primo o no.

    :param n: el numero que se desea ver si es primo.
    :returns: true si N es primo, false en otro caso.'''

    divs = 0
    for i in range(1, n + 1):
        if n % i == 0:
            divs += 1
    return divs == 2

def cong_mod_M(a, m):
    '''Obtiene el valor al que el numero especificado sea congruente, modulo M.

    :param a: un entero al que se obtendra su congruencia, modulo M.
    :param m: un entero que representa el modulo.
    :returns: el entero x que satisface la congruencia a = x (mod m). '''

    if 0 <= a and a < m:
        return a
    elif a >= m:
        return a % m
    else:
        val = a
        while val < 0:
            val += m
        return val

def inverso(a, p):
    '''Obtiene el inverso multiplicativo del valor especificado, modulo P. El
    valor especificado P debe ser primo y A debe cumplir 0 <= A < P.

    :param a: el valor para el que se busca el inverso multiplicativo.
    :param p: el numero primo sobre el que se define el modulo. P debe ser primo.
    :returns: el inverso multiplicativo de a, modulo M.'''

    if es_primo(p):
        for i in range(0, p):
            val = cong_mod_M(a * i, p)
            if val == 1:
                return i
        raise Exception('No se pudo encontrar el inverso. Si estas viendo esto, algo muy raro paso. D:')
    else:
         raise Exception('El valor P no es primo.')
