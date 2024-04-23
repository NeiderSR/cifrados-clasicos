'''
Funciones para descifrar un cifrado polialfabético (Vigenère).
'''

from monoalfabetico import *

# ------------------------------------------------------------------------------
# --                             FUNCIONES                                    --
# ------------------------------------------------------------------------------

def cifrado_vigenere(texto, clave):
    '''Cifra un mensaje usando el cifrado de Vigenère, con la clave especificada.

    :param texto: el texto a cifrar.
    :param clave: la clave de cifrado.
    :returns: el texto cifrado.'''

    long_clave = len(clave)
    valores_clave = [alfabeto[c] for c in clave]
    text_grupos = ' '.join(texto[i:i + long_clave] for i in range(0, len(texto), long_clave))
    grupos = text_grupos.split()
    cifrado = ''
    for grupo in grupos:
        for i in range(len(grupo)):
            nueva_letra = evalua_afin(alfabeto[grupo[i]], 1, valores_clave[i])
            cifrado += alfabeto_inverso[nueva_letra].lower()
    return cifrado

def descifrado_vigenere(texto, clave):
    '''Descifra un mensaje cifrado con el cifrado de Vigenère, usando la
    clave especificada.

    :param texto: el texto cifrado.
    :param clave: la clave de cifrado.
    :returns: una cadena que representa el texto descifrado.'''

    valores_clave = [congruente_mod26(alfabeto[c] * (-1)) for c in clave]
    # clave_descifrado codifica los desplazamientos inversos a la clave original.
    clave_descifrado = ''
    for n in valores_clave:
        clave_descifrado += alfabeto_inverso[n]
    return cifrado_vigenere(texto, clave_descifrado.lower())

# ------------------------------------------------------------------------------
# --                               AUXILIARES                                 --
# ------------------------------------------------------------------------------

def subcadena_lista(cadena, lista):
    '''Verifica si la cadena es subcadena de alguna otra cadena en una lista.

    :param cadena: la cadena que se verificará si aparece en la lista.
    :param lista: una lista de cadenas.
    :returns: True si la cadena es subcadena de alguna otra cadena en la lista.
              False en otro caso.'''

    for s in lista:
        if cadena in s and cadena != s:
            return True
    return False

def encuentra_indices(texto, cadena):
    '''Encuentra todos los índices en los que una cadena aparece en el texto.

    :param texto: una cadena que representa el texto sobre el cual se buscarán
           coincidencias.
    :param cadena: la cadena a buscar en el texto.
    :returns: una lista de valores numéricos, que indican los índices en el texto
              en los que aparece la cadena.'''
    
    inicio = 0
    
    while True:
        inicio = texto.find(cadena, inicio)
        if inicio == -1:
            return
        yield inicio
        inicio += len(cadena)

def primos(val):
    '''Obtiene una lista de números primos, en el rango de 0 hasta el valor
    especificado.

    :param val: el valor máximo del rango sobre el que se obtendrán los números
           primos.
    :returns: la lista de primos en el rango de 0 hasta el valor.'''
    
    lista_primos = []
    for i in range(val):
        if i == 0 or i == 1:
            continue
        else:
            for j in range(2, int(i / 2) + 1):
                if i % j == 0:
                    break
            else:
                lista_primos.append(i)
    return lista_primos

def factores(num):
    '''Obtiene la lista de factores primos de un número.

    :param num: el valor numérico al que se le obtendrán sus factores primos.
    :returns: una lista de los factores primos del número.'''

    factores = []
    lista_primos = primos(num + 1)
    for p in lista_primos:
        if num == 1:
            break
        while num % p == 0:
            factores.append(p)
            num = num // p
    return factores

def diferencias(lista):
    '''Calcula la diferencia entre cada par contiguo de valores en la lista
    especificada.

    :param lista: una lista de valores numéricos.
    :returns: una lista de valores numéricos con las diferencias entre pares
              contiguos de la lista.'''

    return [lista[i] - lista[i - 1] for i in range(1, len(lista))]

# ------------------------------------------------------------------------------
# --                    AUXILIARES PARA CRIPTOANALISIS                        --
# ------------------------------------------------------------------------------

def indice_coincidencias(texto):
    '''Obtiene el índice de coincidencias del texto especificado. Se asume
    un texto sobre un alfabeto de 26 caracteres.

    :param texto: el texto sobre el que se calculará el índice de coincidencias.'''

    longitud = len(texto)
    f_texto = frecuencias(texto)
    ic = 0;
    for frec in f_texto.values():
        ic += (frec * (frec - 1)) / (longitud * (longitud - 1))
    return ic

# Las siguientes funciones se ejecutan una tras otra, en orde, para hallar la
# factorización de las distancias de cadenas repetidas.

def repetidas(texto):
    '''Encuentra todas las subcadenas repetidas de la cadena especificada,
    indicando además cuántas veces aparece. Este algoritmo toma tiempo O(n^3),
    por lo que no se recomienda para textos muy largos.

    :param texto: la cadena sobre la cual se van a buscar las repeticiones.
    :returns: un diccionario que asocia cada subcadena repetida con el número de
              veces que aparece en el texto.'''

    frecs = {}
    subcadenas = [texto[i:j] for i in range(len(texto)) for j in range(i + 1, len(texto) + 1)]
    for s in subcadenas:
        frecs[s] = texto.count(s)
    frecs = {k: v for k, v in frecs.items() if v >= 2 and len(k) >= 2}
    frecs = {k: v for k, v in frecs.items() if not subcadena_lista(k, frecs.keys())}
    return frecs

def repetidas_pos(texto, frecs):
    '''Asocia cada subcadena en frecs con los índices en los que aparece dentro
    del texto.

    :param texto: la cadena donde se hará la búsqueda.
    :param frecs: un diccionario (o lista) con las subcadenas a buscar en el
           texto.
    :returns: un diccionario que asocia cada subcadena en frecs con la lista
    de índices del texto en el que aparecen.'''

    return {cadena: list(encuentra_indices(texto, cadena)) for cadena in frecs.keys()}

def repetidas_difs(repetidas):
    '''Asocia cada cadena con las diferencias entre los índices de las apariciones
    en el texto.

    :param repetidas: un diccionario que contiene la asociación entre cadenas
           e índices de aparición.
    :returns: un diccionario que asocia cada cadena con las diferencias entre
              cada aparición de la cadena en un texto.'''

    return {cadena: diferencias(repetidas[cadena]) for cadena in repetidas.keys()}

def factores_difs(difs):
    '''Asocia cada cadena en difs con el listado de factores primos, de la
    distancia de aparición de subcadenas repetidas.

    :param difs: un diccionario que asocia cadenas con las diferencias de
           aparición.
    :returns: un diccionario que asocia cada cadena con los factores primos de
              las distancias entre apariciones de las cadenas en un texto.'''

    facts = {}
    for cadena in difs.keys():
        valores = difs[cadena]
        fac_dif = []
        for val in valores:
            fac_dif.append(factores(val))
        facts[cadena] = fac_dif
    return facts
