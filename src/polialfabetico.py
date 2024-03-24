'''
Funciones para descifrar un cifrado polialfabético (Vigenère).
'''

from monoalfabetico import *

def repetidas(texto):
    '''Encuentra todas las subcadenas repetidas de la cadena especificada,
    indicando además cuántas veces aparece.

    :param texto: la cadena sobre la cual se van a buscar las repeticiones.
    :returns: un diccionario que asocia cada subcadena repetida con el número de
              veces que aparece en el texto.'''

    frecs = {}
    subcadenas = [texto[i:j] for i in range(len(texto)) for j in range(i + 1, len(texto) + 1)]
    subcadenas = list(dict.fromkeys(subcadenas))
    for s in subcadenas:
        frecs[s] = texto.count(s)
    frecs = {k: v for k, v in frecs.items() if v >= 2 and len(k) >= 2}
    frecs = {k: v for k, v in frecs.items() if not subcadena_lista(k, frecs.keys())}
    return frecs

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
    '''Encuentra los índices en los que una cadena aparece en el texto.

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

def repetidas_pos(texto, frecs):
    '''Asocia cada subcadena en frecs con los índices en los que aparece dentro
    del texto.

    :param texto: la cadena donde se hará la búsqueda.
    :param frecs: un diccionario (o lista) con las subcadenas a buscar en el
           texto.
    :returns: un diccionario que asocia cada subcadena en frecs con la lista
    de índices del texto en el que aparecen.'''

    return {cadena: list(encuentra_indices(texto, cadena)) for cadena in frecs.keys()}

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
            nueva_letra = transformacion_afin(alfabeto[grupo[i]], 1, valores_clave[i])
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

s = 'XHTIO KSIVT RWNCG WDAXC UMBBT LZWFK JOZXB YXFVK GXHHZ KBYVI EAVJX LRLBY\
IIIIY MNHFA YULJI QZKKI JKBSI OKIQU KYJLR RTBZA GUKCR GRRBH ZKVUW YCIVT YIIUN\
ZBWRA HLNHT QBTYO VLRYV CWZNX EIJKB JBAFA FKVLV BBYTF VUNTX MHCRX XPVTN HTHCI\
CULCT QBTWY CWFYN VDIEO GIJIY KFUEM FKGYC IGRTH KQPUE USWEW NYWCR XXUCQ MGWUT\
WAKQC KWFOX HUWHT HXVTB YIOEB BYWYT QFOOI JXNXT FFOEG KFRDV IMIIQ NGECR LNKGY\
CKBTY FZKGU UYCQP UXHJC NXMCT CYUEI JVHSX LFAPU FJLBN HEYJP NHEUS IQKEW FVPKI\
NFLRG EAFZV ZFIPM KVHHZ IYGLV RARYW YJCZG JOZVN JXWRT PAEUI LRTHG ZVNJT FRUNW\
NCEIH TBPVZ FGEFR KHGEU LVDAX HFARR EYXWN JBMVV NXFIJ BEGUU CICUL CSQYO WUULR\
XXUCQ MGKPR ZVGLI GMEGV CFVRY VIETN SBMDI YUZCT IQKEW RTPAE IYCZG GIVVH TFYEW\
EZBYD XBGIU IBVXW YTQRX MUJJN YXMVQ AYMLL KPOHH VAYGI OVAGG XHGZN IMCTI QKXMK\
IZGJO ZVNLN YGWFO UFVKB TLOJB EGUUA WFVHM KMEOH LVAQA KUEBR RTMVO HTWUX CRXKU\
DCAJB UCIAA GWZWR RVIEK RVMIU MUOIY IKBSI OKIPO HHHCR ZHGRJ NIHGF JNYXF RUNWN\
CEIHT BPVZF GESRC TAKUS IHTTH LMIGF UHCVT TKLMC UWLZI EKTFZ HNXVU CKHRH MRTTU\
KCKUV IHMTC LGLIC CPOHH EWRDB MKQRX TNIIO GCIVV PUGWV XGULW FUBRT MIMQK LXVKB\
SIOKW NJXGR AQKVI EAGOM OZZYG LVRAR YWYCI EKWHV CEUGU CAHYB HMMFZ BARKV UGYJA\
RKGZF KNXHH VVRRV UDXBJ XFRQA ZXFZO RTVCR IEZBZ ZKVGE WLGBI HHTMC ZHHRK VUWYJ\
CZGGI GTNTM YRVQU LCCIF STKLQ AGLJL MQKGJ VVFGK IEWQK LUIZB REILV NVKOV JNIHH\
CIDAX MVBEG MUSIQ KKYRN VXFUI TNKQC JBRTV CRLRR TCEBR RBAVV POTXV TNYFU HCVTT M'.replace(' ', '')

d = repetidas(s)
pos = repetidas_pos(s, d)
difs = repetidas_difs(pos)
facts = factores_difs(difs)

# Ya sabemos que la clave es de tamaño 6

s = ' '.join(s[i:i + 6] for i in range(0, len(s), 6))
c1 = s[::7]
c2 = s[1::7]
c3 = s[2::7]
c4 = s[3::7]
c5 = s[4::7]
c6 = s[5::7]

f_c1 = frecuencias(c1)
f_c1_ord = sorted(f_c1, key = f_c1.get, reverse = True)
# La letra e se cifró con X o T, desplazamiento de 19, o 15. La letra es T, o P
# La letra 'e' o 'a' se cifran con X, un desplazamiento de 19 o 23. La letra es T, o X

f_c2 = frecuencias(c2)
f_c2_ord = sorted(f_c2, key = f_c2.get, reverse = True)
# La letra 'e' se cifró con U o I, desplazamiento de 16, o 4. La letra es Q, o E
# La letra 'e' o 'a' se cifran con U, un desplazamiento de 16 o 20. La letra es Q, o U

f_c3 = frecuencias(c3)
f_c3_ord = sorted(f_c3, key = f_c3.get, reverse = True)
# La letra 'e' se cifró con V o R, desplazamiento de 17, o 13. La letra es R, o N
# La letra 'e' o 'a' se cifran con V un desplazamiento de 17 o 21. La letra es R, o V

f_c4 = frecuencias(c4)
f_c4_ord = sorted(f_c4, key = f_c4.get, reverse = True)
# la letra 'e' se cifró con I o K, desplazamiento de 4, o 6. La letra es E, o G
# La letra 'e' o 'a' se cifra con I, un desplazamiento de 4 o 8. La letra es E, o I

f_c5 = frecuencias(c5)
f_c5_ord = sorted(f_c5, key = f_c5.get, reverse = True)
# la letra 'e' se cifró con N o R, desplazamiento de 9, o 13. La letra es B, o N
# La letra 'e' o 'a' se cifran con N, un desplazamiento de 9 o 13. La letra J, o N

f_c6 = frecuencias(c6)
f_c6_ord = sorted(f_c6, key = f_c6.get, reverse = True)
# la letra 'e' se cifró con G o K, desplazamiento de 2, o 6. La letra es C, o G
# La letra 'e' o 'a' se cifran con G, un desplazamiento de 2 o 6. La letra es C, o G

# T Q R E B C
# P E N G N G

# T Q R E J C
# X U V I N G

# T Q R E N G

# La clave es 'turing'
