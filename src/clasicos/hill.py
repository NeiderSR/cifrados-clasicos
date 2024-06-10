from monoalfabetico import *
from polialfabetico import *

def separa_grafias(s, n):
    '''Separa el texto especificado S en grafias de longitud N. Se asume
    un texto de entrada sin espacios.

    :param s: el texto que va a ser separado en grafias.
    :param n: la longitud que tendra cada grafia.
    :returns: una lista con las grafias del texto.'''

    return [s[i:i+n] for i in range(0, len(s), n)]

def cifrado_hill(a, b, c, d, s):
    '''Cifra el texto especificado, usando la matriz de cifrado especificada
    a traves de sus valores. La matriz de cifrado debe ser de 2x2.

    :param a: la entrada (1, 1) de la matriz de cifrado.
    :param b: la entrada (1, 2) de la matriz de cifrado.
    :param c: la entrada (2, 1) de la matriz de cifrado.
    :param d: la entrada (2, 2) de la matriz de cifrado.
    :param s: el texto a cifrar con la matriz de cifrado.
    :returns: el texto cifrado con el sistema de Hill.'''

    grafias = separa_grafias(s.replace(' ', '').lower(), 2)
    cifradas = []
    for graf in grafias:
        if graf[0] in alfabeto and graf[1] in alfabeto:
            val_a = alfabeto[graf[0]]
            val_b = alfabeto[graf[1]]
            coord_1 = congruente_mod26((a * val_a) + (b * val_b))
            coord_2 = congruente_mod26((c * val_a) + (d * val_b))
            cifradas.append(alfabeto_inverso[coord_1]
                            + alfabeto_inverso[coord_2])
    return ''.join(cifradas)

def descifrado_hill(a, b, c, d, s):
    '''Descifra el texto especificado, a partir de la matriz de cifrado
    original.

    :param a: la entrada (1, 1) de la matriz de cifrado.
    :param b: la entrada (1, 2) de la matriz de cifrado.
    :param c: la entrada (2, 1) de la matriz de cifrado.
    :param d: la entrada (2, 2) de la matriz de cifrado.
    :param s: el texto a descifrar, cifrado con la matriz de cifrado
              especificada.
    :returns: el texto descifrado en claro.'''

    a_inv, b_inv, c_inv, d_inv = matriz_inversa(a, b, c, d)
    return cifrado_hill(a_inv, b_inv, c_inv, d_inv, s)

def matriz_inversa(a, b, c, d):
    '''Obtiene la matriz inversa de la matriz especificada si exsite, en los
    enteros modulo 26. La matriz se ingresa a traves de sus entradas, de modo
    que:
    
    | a b |
    | c d |

    corresponde con la tupla (a, b, c, d).

    :param a: la entrada (1, 1) de la matriz
    :param b: la entrada (1, 2) de la matriz
    :param c: la entrada (2, 1) de la matriz
    :param d: la entrada (2, 2) de la matriz
    :returns: una tupla que corresponde con las entradas de la matriz inversa,
              si existe.'''

    det = (a * d) - (b * c)
    inv_det = inverso(congruente_mod26(det))    # Puede lanzar una excepcion.
    return (congruente_mod26(inv_det * d),
            congruente_mod26(inv_det * (-b)),
            congruente_mod26(inv_det * (-c)),
            congruente_mod26(inv_det * a))

def descifrado_hill_fuerza_bruta(s):
    '''Prueba todas las combinaciones de matrices de cifrado para intentar
    descifrar el texto especificado S. Luego de probar todas las
    combinaciones, obtiene el indice de coincidencias (IC), de modo que
    textos descifrados cuyo valor de IC sean mas cercanos al IC del espannol,
    seran mas probablemente el texto descifrado. El resultado se escribe en
    un archivo de texto para su posterior analisis.

    :param s: el texto cifrado con el sistema de Hill.'''

    extracto = s.replace(' ', '')
    contador = 0                     # Contador de intentos totales.
    textos = []                      # Almacena los intentos.
    
    # Las combinaciones se representan como la matriz:
    #
    # | i j |
    # | k m |
    #
    for i in range(0, 26):
      for j in range(0, 26):
        for k in range(0, 26):
          for m in range(0, 26):
            det = congruente_mod26((i * m) - (j * k))
            if det in coprimos_26:                    # Si el inverso existe.
              intento = descifrado_hill(i, j, k, m, extracto).lower()
              lista_frec = frecuencias(intento)
              lista_frec = sorted(lista_frec, key=lista_frec.get, reverse=True)
              idx_c = indice_coincidencias(intento)
              if lista_frec[0] == 'e' or lista_frec[0] == 'a' or lista_frec[0] == 'o':
                contador += 1
                matriz = str(i) + ' ' + str(j) + ' ' + str(k) + ' ' + str(m)
                textos.append((idx_c,
                               contador,
                               matriz,
                               intento[:100])
                              )
              
    textos.sort(reverse=True)    # Se ordenan segun el IC.
    with open('hill.txt', 'a') as f:
      for ic, i, m, t in textos:
        f.write(str(i) + '; ' + str(ic) + '; ' + m + '; ' + t + '\n')

s = 'RX WW YD AD ME ZC SF BI FH QD ZC OQ DB HK AE SW ZY TJ JO ER SW ZY TJ JO CX SA RG AN VZ AV RL AI JP JL XQ XE LU BF MR PV ZC TX MR W— RA EO NU MO KB KX RX SW AJ KI YV DD XI AD JM —L UP CY NR AE NM LD UH HB BI I— CU FB VO WH MR W— ER AL JZ MU MU H— OQ KC OR AV Q— MR W— SA OW OI H— LJ ME GO UZ DE JI DR MR BF HS AE I— SA SA O— AJ AV AL AL RA JP JL QL G— TX H— MR PV ZC MU AI CU SA QL BF AD NM AE I— MU IL MR W— SA HG RA BF HS NM ZC ZL QM —C TU H— OW UB BF DR SA OQ UH NM ZC SF OE H— RA OR FH MU BF ND XZ GT II FB LU JP SW BI WH SA AN OW WW GO QL VX AL —H DR MU ZL BF OQ OP VX H— DV NE MH G— OM AJ RX JL XQ II FB LU JP IC NR S— CD MH RG AN VZ VX UC YB OQ AV RL CJ DF NZ OR ZF JI KX NM MQ VX WW ZC OR MX CY GO NZ AD AV Q— MR W— SA AE SW —H AJ HF GN KG MU QL SA WM SA MN MV ZC XY DR NU G— OM AJ RX JL RI XI AD JM —L UP CY NR XZ DV IL PV AZ HJ KX ME QL JF ZC MU WT ND BF TU DD JZ UU BF AN MQ DW JG PG HG BF GT KG SF KW CX S— TD SA VO Q— QM W— UA MQ NU AV UC OL ZL HV SA RX WW YD AD ME ZC H— BF QL IJ BI RB NU VD SX KX AI AI CU SA BI AJ JF H— QL NU II EO XQ TD DR JI EO OQ ZD ND BI MN JF AI MR MU IS FB RA WW BW IL H— XY DR NU HS SW ZM ND TU HS AJ AV NZ OR AM MR KX NU HG CP MV CY HH BF BM PJ RA TU OM AJ VX I— VO BI IC UH SS OR HS WP JP SW OE EE TC MU P— EW VX I— RA O— CD FB LJ RA CU BF CY NR DR SA MV AJ —P OQ EE CH MV GT KU KX AE YD HB AR VZ IJ TE CY HB JL —T YD HB NM ZC RA G— GY OQ CX NO EE ME OP AI QL SA RG AN I— PV SW QL G— OM AJ RX GO DA XQ II FB LU JP SW JL P— H— OQ YV NU KC AZ PV ZC AI QL RA EW VX BI ZC LU JP LT EE FB DR XQ OP QL AV VZ QL UC FV DK VX NU DR IA —L I— AJ CY NR NU RG AN JL P— SF VG GN ME TD KX AE KW OQ WW NR H— SW HK GT QM KX O— AJ O— GT DA RI XI OJ DE LU RO AZ SA —T ZC OR MX FK EO MV KU JP BI MN AD JM —L UP CY NR TE WW MV NU AV JL CU SA ER SW KS RA WR RA SF I— SA MV KU JP PQ OQ LC HB AR AJ SW SW VK WO QP RA AI XQ DX YV EE DE LU JP AZ AI CU SA KC OR MQ UC XL QL SA G— OM AJ RX JL XQ II FB LU JP SW I— VO Z— ZD ND FH MR MR SA YV NU KC AZ BF CY —M EE FB DR QL SA RG AN PQ DZ VD GO MN —C I— DR QL SA RG AN FW ND CH BF SF SS OR AM MR OJ JG NU HG CP MV CY NR H— NU BZ H— ME HO OR HS ZO RG AE ZC AJ AV Q— MR W— SA NU MN AV ZO MV CG BA TU AE ZC AJ AV XT WT ND QM IA BF AN NZ OR FQ SA NU LX OR NZ OR AM MR KX NU HG CP MV CY NR MN VX G— H— BF ME CY NR AV ZO MV CG BA TU NU AV RG AN BI HF FB MR W— —M VX GN BF HS NM ZC SF JZ CJ OW WW HF ME MN CY NR H— MR AI XY ZD ND BI GJ VX JM BW ND XZ GT II FB LU JP SW UC BI GG IJ TE MV QC KX —C GQ KX BI GJ VX JM XI WW RZ KF SA MV YD SA BF AV XT DZ EE DE SA AV ZO AE VZ BI DV XQ BW ND XZ XT QL LU JP SW BI ZC VX AV WW HS BU NU RG AN BI ZX I— BF HS Z— IG ND OW I— VO ZC NR HK BI AJ VD JA OQ RA OP UH NU GO KI HV QL H— BI OW DE EO TF AD RX GO DW WW ZF JI BF HS BF VD JA OQ RA OP UH NU DE H— —L S— HB VZ KX EE CJ H— HV MR BF HS H— GY DW CD EO HS OP SF I— SA MV KU JP BI QC OJ GR EO CK LU JP QC OM FB DR QL SA RG AN PQ YV DE MU ZR MV HF YV HS SW ZM ND MI YB OQ VO I— QM W— TD SA G— OM AJ RX JL XQ II FB LU JP WL ND MQ H— ME AZ MH IL ME NM ZC OQ QL LU JP XI GO Q— NR ZD ND FH SA O— AJ AV AM RA H— HS CH DW NU YV NU KC AZ BF CY TU NO EE ME NU AV JL CU SA OP IL AD VX NZ NR NU LU RO LP IR OQ G— OM AJ RX NU HG CP MV CY NR NU BZ NU H— ME DA H— —C IC LJ DR DR QL RA EW VX BI ZC LU JP QC OM FB GJ AV GL OE QL SA RG AN FH NO '
