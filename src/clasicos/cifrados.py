'''
Criptografía y Seguridad 2024-2.
Tarea 1.

Equipo DinamitaBB. Integrantes:
- Flores Ayala Luis Edgar. 317251340
- Robles Huerta Rosa Maria. 317061521
- Sánchez Reza Neider. 317020931
- Sánchez Velasco Eduardo Leonel. 420004035
'''

import monoalfabetico
import polialfabetico

def imprime_diccionario(dic):
    '''Imprime un diccionario, con formato bonito.
    :param dic: el diccionario que se quiere imprimir.'''

    print('{' + '\n'.join('{!r}: {!r},'.format(k, v) for k, v in dic.items()) + '}')

# ------------------------------------------------------------------------------
# --                       CIFRADO MONOALFABETICO                             --
# ------------------------------------------------------------------------------

print('======================== CIFRADO MONOALFABETICO ========================\n')

with open('./../data/Texto1.txt', 'r') as archivo:
    noticia = archivo.read()

print('Un fragmento de la noticia:')
print(noticia[:255], '...\n')

# Verficamos que la noticia sí sea de la longitud especificada.
longitud_noticia = len(noticia)
print('La longitud de la noticia de entrada es de', longitud_noticia, 'caracteres.\n')

texto_plano1 = monoalfabetico.limpiar_texto(noticia)
cifrado_mono = monoalfabetico.cifrado_monoalfabetico(texto_plano1, 19, 2)

cripto_1 = ' '.join(cifrado_mono[i:i+5] for i in range(0, len(cifrado_mono), 5))
with open('./../data/Criptograma1.txt', 'w') as archivo:
    archivo.write(cripto_1)

print('Un fragmento del texto cifrado:')
print(cripto_1[:255], '\n')

frec_plano1 = monoalfabetico.frecuencias(texto_plano1)
print('Tabla de frecuencias del texto plano:')
imprime_diccionario(frec_plano1)
print('Ordenadas de mayor a menor frecuencia:\n', sorted(frec_plano1, key = frec_plano1.get, reverse = True), '\n')

frec_cript1 = monoalfabetico.frecuencias(cifrado_mono)
print('Tabla de frecuencias del texto cifrado:')
imprime_diccionario(frec_cript1)
print('Ordenadas de mayor a menor frecuencia:\n', sorted(frec_cript1, key = frec_cript1.get, reverse = True), '\n')

print('Índice de coincidencias texto plano: ', polialfabetico.indice_coincidencias(texto_plano1))
print('Índice de coincidencias texto cifrado (monoalfabetico): ', polialfabetico.indice_coincidencias(cifrado_mono))

# ------------------------------------------------------------------------------
# --                       CIFRADO POLIALFABETICO                             --
# ------------------------------------------------------------------------------

print('\n======================== CIFRADO POLIALFABETICO ========================\n')

with open('./../data/Texto2.txt', 'r') as archivo:
    noticia = archivo.read()

texto_plano2 = monoalfabetico.limpiar_texto(noticia)
cifrado_poli = polialfabetico.cifrado_vigenere(texto_plano2, 'dinamitabb')

cripto_2 = ' '.join(cifrado_poli[i:i+5] for i in range(0, len(cifrado_poli), 5)).upper()
with open('./../data/Criptograma2.txt', 'w') as archivo:
    archivo.write(cripto_2)

print('Un fragmento del texto cifrado:')
print(cripto_2[:255], '\n')

frec_plano2 = monoalfabetico.frecuencias(texto_plano2)
print('Tabla de frecuencias del texto plano:')
imprime_diccionario(frec_plano2)
print('Ordenadas de mayor a menor frecuencia:\n', sorted(frec_plano2, key = frec_plano2.get, reverse = True), '\n')

frec_cript2 = monoalfabetico.frecuencias(cifrado_poli)
print('Tabla de frecuencias del texto cifrado:')
imprime_diccionario(frec_cript2)
print('Ordenadas de mayor a menor frecuencia:\n', sorted(frec_cript2, key = frec_cript2.get, reverse = True), '\n')

print('Índice de coincidencias texto plano: ', polialfabetico.indice_coincidencias(texto_plano2))
print('Índice de coincidencias texto cifrado (polialfabetico): ', polialfabetico.indice_coincidencias(cifrado_poli), '\n')

# Se obtiene un extracto de los textos, debido a que los algoritmos para
# calcular los factores de las distancias toman mucho tiempo.
texto_plano_extracto = texto_plano2[0:1500]
texto_cifrado_extracto = cifrado_poli[0:1500]

reps_plano = polialfabetico.repetidas(texto_plano_extracto)
pos_plano = polialfabetico.repetidas_pos(texto_plano_extracto, reps_plano)
difs_plano = polialfabetico.repetidas_difs(pos_plano)
facts_plano = polialfabetico.factores_difs(difs_plano)
print('Los factores de las distancias en el texto plano son:')
imprime_diccionario(facts_plano)

reps_cript = polialfabetico.repetidas(texto_cifrado_extracto)
pos_cript = polialfabetico.repetidas_pos(texto_cifrado_extracto, reps_cript)
difs_cript = polialfabetico.repetidas_difs(pos_cript)
facts_cript = polialfabetico.factores_difs(difs_cript)
print('\nLos factores de las distancias en el texto cifrado son:')
imprime_diccionario(facts_cript)
