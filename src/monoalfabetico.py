'''
Funciones para cifrar y descifrar con transformaciones afines (monoalfabéticos)
'''

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

# ------------------------------------------------------------------------------
# --                             FUNCIONES                                    --
# ------------------------------------------------------------------------------

def cifrar_texto(texto, coef_A, coef_B):
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
        nuevo_indice = transformacion_afin(indice_c, coef_A, coef_B)
        nueva_letra = alfabeto_inverso[nuevo_indice]
        criptograma += nueva_letra
    return criptograma

def descifrar_texto(texto, coef_a, coef_b):
    '''Descifra el texto, usando la función afín especificada. Se espera que los
    parámetros de entrada correspondan con la función inversa de la función
    afín de cifrado. Esta función no encuentra dichos valores. Se asume que el
    texto está libre de espacios y caracteres especiales (alfabeto de 26 letras).

    :param texto: el criptograma a descifrar.
    :coef_a: el parámetro A (salto) de la función inversa de la función afín.
    :coef_b: el parámetro B (desplazamiento) de la función inversa de la función
    afín.'''

    return cifrar_texto(texto, coef_a, coef_b).lower()

def descifrar_fuerza_bruta(texto, longitud):
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
            intento = cifrar_texto(extracto_texto, inv_a, inv_b).lower()
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

def transformacion_afin(x, a, b):
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
    
    por_quitar = '¿?¡!,.$() '
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

# Estas funciones ya no las usé. :(

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

def coeficientes_afin(cifrado_a, plano_2, cifrado_2):
    '''Despeja los coeficientes A y B de la transformación afín, dados los
    valores cifrados conocidos.

    :param cifrado_a: la letra que cifra a la letra 'a'.
    :param plano_2: una letra en texto plano del que se conozca su cifrado.
    :param cifrado_2: la letra que cifra la letra conocida plano_2.'''

    valor_B = alfabeto[cifrado_a]
    plano_val = alfabeto[plano_2]
    cifrado_val = alfabeto[cifrado_2]

    if maximo_comun_divisor(plano_val, 26) == 1:
        valor_A = congruente_mod26((cifrado_val - valor_B) * inverso(plano_val))
    else:
        raise Exception('No se puede encontrar: plano_2 no tiene inverso.')

    return (valor_A, valor_B)

# ------------------------------------------------------------------------------
# --                               EJEMPLOS                                   --
# ------------------------------------------------------------------------------

# Coeficientes de salto válidos para funciones afines.
coprimos_26 = [i for i in range(0, 26) if maximo_comun_divisor(i, 26) == 1]

#s = 'VHYBX FVNRB XFDEH UUBSQ HXFAE JQJAN CHZNA RUHXF AEJXF UNIFA\
#BACFV NSQHX FAEJN QHRUB NBAOH AXBSQ HAFZK UHZHA EFJAN CHZKH\
#CBCND ZJKHP JHEHP JHUUB NANCN VNZOH UEHKJ HZNKU HACBH ACFNS\
#UBACN UKFUQ NVJHU EHVHH AZHAN UFANX HQHSU NUQNO BCNHA QNZFQ\
#HCNCC HEJZX BJCNC HZNXF RBZEH VBZFQ HCNCA FZHXJ NAENZ OHXHZ\
#VHZNQ ONZEH ZBADF PJHUH UVHZN QONUW JDHUF AQFZC BFZHZ CHQXB\
#HQFVN ZSJQQ HQNOB CNHAE JZXNQ QHZDU HANXH QNMQF UHAEJ XNVKF\
#XFAFX HZQNK HANDH QCJHQ FDHAE JXFUN IFAWN DJASN BQHCF ACHCN\
#AINAC BNSQF ZDZNA EFZDD FVHHA NVFUH CHQNW JVBQC NCPJH NCFUA\
#NEJMU HAEHV HHARU NACHX BHAHQ FURJQ QFPJH EHVKQ NEJXN AEFVH\
#HVSFU UNXWH HAQNZ HCCHE JZNAR UHXNQ BHAEH VHUHX FAFXB HAHQU\
#HMQHG FCHQN MJHAE HCHEJ QQNAE FVNZZ BAVNZ VHCHZ KBCFV HYBXF\
#PJHUB CFWHU BCFCH ZNARU HDCHQ JINCF ACHOF DEHKH UZBRF DEHNA\
#FUFXF VFNJA NVBRF PJHHZ XFACH JANXJ ANHAZ JNENJ CZWNU BMMHU\
#ANACH I'

#s = 'XHTIO KSIVT RWNCG WDAXC UMBBT LZWFK JOZXB YXFVK GXHHZ KBYVI EAVJX LRLBY\
#IIIIY MNHFA YULJI QZKKI JKBSI OKIQU KYJLR RTBZA GUKCR GRRBH ZKVUW YCIVT YIIUN\
#ZBWRA HLNHT QBTYO VLRYV CWZNX EIJKB JBAFA FKVLV BBYTF VUNTX MHCRX XPVTN HTHCI\
#CULCT QBTWY CWFYN VDIEO GIJIY KFUEM FKGYC IGRTH KQPUE USWEW NYWCR XXUCQ MGWUT \
#WAKQC KWFOX HUWHT HXVTB YIOEB BYWYT QFOOI JXNXT FFOEG KFRDV IMIIQ NGECR LNKGY\
#CKBTY FZKGU UYCQP UXHJC NXMCT CYUEI JVHSX LFAPU FJLBN HEYJP NHEUS IQKEW FVPKI\
#NFLRG EAFZV ZFIPM KVHHZ IYGLV RARYW YJCZG JOZVN JXWRT PAEUI LRTHG ZVNJT FRUNW\
#NCEIH TBPVZ FGEFR KHGEU LVDAX HFARR EYXWN JBMVV NXFIJ BEGUU CICUL CSQYO WUULR\
#XXUCQ MGKPR ZVGLI GMEGV CFVRY VIETN SBMDI YUZCT IQKEW RTPAE IYCZG GIVVH TFYEW\
#EZBYD XBGIU IBVXW YTQRX MUJJN YXMVQ AYMLL KPOHH VAYGI OVAGG XHGZN IMCTI QKXMK\
#IZGJO ZVNLN YGWFO UFVKB TLOJB EGUUA WFVHM KMEOH LVAQA KUEBR RTMVO HTWUX CRXKU\
#DCAJB UCIAA GWZWR RVIEK RVMIU MUOIY IKBSI OKIPO HHHCR ZHGRJ NIHGF JNYXF RUNWN\
#CEIHT BPVZF GESRC TAKUS IHTTH LMIGF UHCVT TKLMC UWLZI EKTFZ HNXVU CKHRH MRTTU\
#KCKUV IHMTC LGLIC CPOHH EWRDB MKQRX TNIIO GCIVV PUGWV XGULW FUBRT MIMQK LXVKB\
#SIOKW NJXGR AQKVI EAGOM OZZYG LVRAR YWYCI EKWHV CEUGU CAHYB HMMFZ BARKV UGYJA\
#RKGZF KNXHH VVRRV UDXBJ XFRQA ZXFZO RTVCR IEZBZ ZKVGE WLGBI HHTMC ZHHRK VUWYJ\
#CZGGI GTNTM YRVQU LCCIF STKLQ AGLJL MQKGJ VVFGK IEWQK LUIZB REILV NVKOV JNIHH\
#CIDAX MVBEG MUSIQ KKYRN VXFUI TNKQC JBRTV CRLRR TCEBR RBAVV POTXV TNYFU HCVTT M'

#f = frecuencias(limpiar_texto(s))
#print('Tabla de frecuencias: ', f)
#print('')
#print('Letras ordenadas de mayor a menor frecuencia:')
#print(sorted(f, key = f.get, reverse = True))

#descifrar_fuerza_bruta(limpiar_texto(s))

#descifrar_fuerza_bruta(limpiar_texto(s1))

#descifrar_texto(limpiar_texto(s), 21, 13)

#print(maximo_comun_divisor(192, 270))
#print(inverso(5))
#print(coeficientes_afin('n', 'r', 'c'))
#print(coprimos_26)
#print(inversa_afin(15, 7))
#print(cifrar_texto('hola', 2, 0))

# Intentos de descifrado: esto va en la documentación.

# Observando la tabla de frecuencias y sabiendo que las dos letras más comunes
# son la 'e' y la 'a', suponemos que 'h' cifra a 'e' y que 'n' cifra a 'a'.
#
# Del valor de 'a', despejamos:
# T(x) = Ax + B mod 26
# T(a) = T(0)
#      = A(0) + B mod 26
#      = B mod 26
#      = 13 mod 26
# De donde, en particular, B = 13. Para despejar a A, debemos encontrar un
# valor que tenga inverso multiplicativo modulo 26. Si usamos la letra 'e',
# entonces encontraremos que el coeficiente de A será 4, el cual no tiene
# inverso módulo 26. La siguiente letra más común es la 'o', la cual supondremos
# que ha sido cifrada con 'a' (tercera letra más común en el criptograma).
# Así, tenemos que
# T(o) = T(15)
#      = A * 15 + B (mod 26)
#      = A * 15 + 13
#      = 0
# Tenemos la ecuación
# A * 15 + B = 0 (mod 26)
# A * 15 = 0-13 (mod 26)
# A * 15 = 13 (mod 26)
# A * 15 * 7 = 13 * 7 (mod 26)
# A = 13 (mod 26)
# Por lo que la expresión queda T(x) = 13x + 13 (mod 26). No salió xd
# Si hacemos prueba y error, vemos que el siguiente valor que hace que 'h' cifre
# a la 'e' es el A=5. Tampoco funciona. xd
# Como no funcionó, utilicé fuerza bruta.
