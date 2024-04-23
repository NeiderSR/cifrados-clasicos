'''
Funciones para cifrar y descifrar con transformaciones afines (monoalfabéticos)
'''

# ------------------------------------------------------------------------------
# --                             FUNCIONES                                    --
# ------------------------------------------------------------------------------

def cifrado_monoalfabetico(texto, coef_A, coef_B):
    '''Cifra el texto con la función afín indicada a través de sus parámetros.
    Se asume un texto sin espacios y sin caracteres especiales (alfabeto de 26
    letras).

    :param texto: el texto a cifrar.
    :param coef_A: el coeficiente A (salto) de la función afín para cifrar.
    :param coef_B: el coeficiente B (desplazamiento) de la función afín para
           cifrar.
    :returns: un texto cifrado usando la función afín especificada.'''

    criptograma = ''
    for c in texto:
        indice_c = alfabeto[c]
        nuevo_indice = evalua_afin(indice_c, coef_A, coef_B)
        nueva_letra = alfabeto_inverso[nuevo_indice]
        criptograma += nueva_letra
    return criptograma

def descifrado_monoalfabetico(texto, coef_a, coef_b):
    '''Descifra el texto usando la función afín especificada. Los parámetros de
    la función afín corresponden con los parámetros de la función usada para
    cifrar. Se asume que el texto está libre de espacios y caracteres especiales
    (alfabeto de 26 letras).

    :param texto: el criptograma a descifrar.
    :coef_a: el parámetro A (salto) de la función afín usada para cifrar.
    :coef_b: el parámetro B (desplazamiento) de la función afín usada para
             cifrar.'''

    cript_limpio = texto.lower().replace(' ', '')
    inv_a, inv_b = inversa_afin(coef_a, coef_b)

    return cifrado_monoalfabetico(cript_limpio, inv_a, inv_b).lower()

def descifrado_fuerza_bruta(texto, longitud):
    '''Muestra todas las combinaciones de funciones afines para intentar
    descifrar un texto. No descifra el texto en su totalidad, sólo muestra las
    combinaciones de funciones inversas y los posibles resultados, a través de
    los primeros caracteres especificados del texto descifrado.

    :param texto: el texto a descifrar.
    :param longitud: la cantidad de caracteres máxima a tomar del texto. Se
           sugiere una cantidad limitada, suficientemente grande para determinar
           si un texto es coherente o no.
    :returns: los valores A y B de la función afín usada para cifrar.'''

    extracto_texto = texto[:longitud]
    
    for i in coprimos_26:
        for j in range(0, 26):
            inv_a, inv_b = inversa_afin(i, j)
            intento = cifrado_monoalfabetico(extracto_texto, inv_a, inv_b).lower()
            print('Salto: ', inv_a)
            print('Desplazamiento: ', inv_b)
            print('El texto descifrado es: ', intento)
            print('')

# ------------------------------------------------------------------------------
# --                               AUXILIARES                                 --
# ------------------------------------------------------------------------------

def congruente_mod26(a):
    '''Obtiene el valor al que el número especificado sea congruente, modulo
    26.

    :param a: un entero al que se obtendrá su congruencia, módulo 26.
    :returns: el entero x que satisface la congruencia a = x (mod 26). '''

    if 0 <= a and a < 26:
        return a
    elif a >= 26:
        return a - (26 * (a // 26))
    else:
        val = a
        while val < 0:
            val += 26
        return val

def maximo_comun_divisor(a, b):
    '''Devuelve el máximo común divisor de los valores especificados usando el
    algoritmo de Euclides de manera recursiva.

    :param a: el primer valor para calcular el MCD.
    :param a: el segundo valor para calcular el MCD.
    :returns: el MCD entre a y b.'''

    if a == 0:
        return b
    elif b == 0:
        return a
    elif b > a:
        return maximo_comun_divisor(b, a)
    else:
        return maximo_comun_divisor(b, a - (b * (a // b)))

def inverso(a):
    '''Obtiene el inverso multiplicativo del valor especificado, módulo 26.

    :param a: el valor para el que se busca el inverso multiplicativo.
    :returns: el inverso multiplicativo de a, módulo 26.'''

    if maximo_comun_divisor(a, 26) == 1:
        for i in range(0, 26):
            val = congruente_mod26(a * i)
            if val == 1:
                return i
        raise Exception('No se pudo encontrar el inverso. Si estás viendo esto, algo muy raro pasó. D:')
    else:
         raise Exception('El valor no tiene inverso módulo 26.')

def evalua_afin(x, a, b):
    '''Evalúa la función afín especificada a través de sus parámetros, en el
    valor especificado.

    :param x: el valor numérico (entre 0 y 25, inclusivo) a evaluar en la
              función.
    :param a: el ceoficiente A (salto) de la función afín para cifrar.
    :param b: el coeficiente B (desplazamiento) de la función afín para cifrar.'''

    return congruente_mod26(a * x + b)
            
def inversa_afin(coef_A, coef_B):
    '''Devuelve los coeficientes de la función afín inversa, dados los
    coeficientes de la función original.

    :param coef_A: el valor del coeficiente A.
    :param coef_B: el valor del coeficiente B.
    :returns: una tupla que contiene los coeficientes A y B de la función
              inversa.'''

    if maximo_comun_divisor(coef_A, 26) == 1:
        inv_A = inverso(coef_A)
        return (inv_A, congruente_mod26((-coef_B) * inv_A))
    else:
        raise Exception('No se puede calcular función inversa: coef_A no tiene inverso.')
            
def limpiar_texto(texto):
    '''Eliminar espacios y caracteres especiales del texto dado. Además,
    convierte el texto a sólo minúsculas.

    :param texto: el texto sobre el cual se va a hacer la limpieza.
    :returns: un texto en minúsculas sin espacios ni caracteres especiales.'''

    nuevo_texto = texto.lower()

    # Cualquier implementación que se me ocurrió tiene complejidad O(n*m), con
    # n la longitud del texto y m la cantidad de caracteres a remover.

    nuevo_texto = nuevo_texto.replace('\n', ' ')

    por_quitar = ' :.,«»()-'
    for simbolo in por_quitar:
        nuevo_texto = nuevo_texto.replace(simbolo, '')
        
    nuevo_texto = nuevo_texto.replace('á', 'a')
    nuevo_texto = nuevo_texto.replace('é', 'e')
    nuevo_texto = nuevo_texto.replace('í', 'i')
    nuevo_texto = nuevo_texto.replace('ó', 'o')
    nuevo_texto = nuevo_texto.replace('ú', 'u')
    nuevo_texto = nuevo_texto.replace('ñ', 'nn')

    return nuevo_texto

# ------------------------------------------------------------------------------
# --                    AUXILIARES PARA CRIPTOANALISIS                        --
# ------------------------------------------------------------------------------

def frecuencias(texto):
    '''Devuelve las apariciones de cada letra en el texto dado. Se asume un
    texto sin números, sin caracteres especiales ni la letra ñ (alfabeto de 26
    letras).
    
    :param texto: el texto sobre el cual se va a hacer el conteo de letras.
    :returns: un diccionario que asocia cada letra del abecedario con la
              cantidad de apariciones en el texto.'''

    tabla_frec = {}
    for c in texto:
        if c not in tabla_frec:
            tabla_frec[c] = 1
        else:
            tabla_frec[c] += 1
    return tabla_frec

# ------------------------------------------------------------------------------
# --                            CONSTANTES                                    --
# ------------------------------------------------------------------------------

alfabeto = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7,
    'i': 8,
    'j': 9,
    'k': 10,
    'l': 11,
    'm': 12,
    'n': 13,
    'o': 14,
    'p': 15,
    'q': 16,
    'r': 17,
    's': 18,
    't': 19,
    'u': 20,
    'v': 21,
    'w': 22,
    'x': 23,
    'y': 24,
    'z': 25
}

# Usado para cifrar.
alfabeto_inverso = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H',
    8: 'I',
    9: 'J',
    10: 'K',
    11: 'L',
    12: 'M',
    13: 'N',
    14: 'O',
    15: 'P',
    16: 'Q',
    17: 'R',
    18: 'S',
    19: 'T',
    20: 'U',
    21: 'V',
    22: 'W',
    23: 'X',
    24: 'Y',
    25: 'Z'
}

# Coeficientes de salto válidos para funciones afines.
coprimos_26 = [i for i in range(0, 26) if maximo_comun_divisor(i, 26) == 1]
