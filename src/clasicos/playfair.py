from monoalfabetico import *
from hill import *

def cifrado_playfair(cuadro, texto):
    '''Cifra el texto usando el cuadro de Playfair especificado.

    :param cuadro: el cuadro de Playfair.
    :param texto: el texto a cifrar.
    :returns: el texto cifrado usando el cuadro de Playfair.'''

    digramas = separa_grafias(texto.lower(), 2)
    cifrado = ''
    for d in digramas:
        x1, y1 = busca_letra(cuadro, d[0])
        x2, y2 = busca_letra(cuadro, d[1])
        if x1 == x2:
            cifrado += cuadro[x1][(y1 + 1) % 5] + cuadro[x1][(y2 + 1) % 5]
        elif y1 == y2:
            cifrado += cuadro[(x1 + 1) % 5][y1] + cuadro[(x2 + 1) % 5][y1]
        else:
            cifrado += cuadro[x1][y2] + cuadro[x2][y1]
    return cifrado.upper()

def descifrado_playfair(cuadro, texto):
    '''Aplica las reglas inversas para descifrar con el cuadro de Playfair
    especificado.

    :param cuadro: el cuadro de Playfair usado para cifrar.
    :param texto: el texto cifrado con el CUADRO de Playfair.
    :returns: el texto descifrado usando el cuadro de Playfair'''

    digramas = separa_grafias(texto.lower(), 2)
    cifrado = ''
    for d in digramas:
        x1, y1 = busca_letra(cuadro, d[0])
        x2, y2 = busca_letra(cuadro, d[1])
        if x1 == x2:
            cifrado += cuadro[x1][(y1 - 1) % 5] + cuadro[x1][(y2 - 1) % 5]
        elif y1 == y2:
            cifrado += cuadro[(x1 - 1) % 5][y1] + cuadro[(x2 - 1) % 5][y1]
        else:
            cifrado += cuadro[x1][y2] + cuadro[x2][y1]
    return cifrado

def construye_cuadro(clave):
    '''Obtiene el cuadro de Playfair a partir de la clave especificada.

    :param clave: la clave que se utilizará para el cifrado.
    :returns: un arreglo de caracteres que representa el cuadro de Playfair.'''

    clave_limpia = clave.lower().replace(' ', '')
    unicos = ''.join(dict.fromkeys(clave_limpia))
    alfabeto = ''.join([x for x in 'abcdefghijklmnopqrstuvwxyz' if x not in unicos])
    cuadro = [[], [], [], [], []]
    i = 0
    j = 0
    for c in unicos:
        if j == 5:
            break
        cuadro[j].append(c)
        i += 1
        if i == 5:
            j += 1
            i = 0
            
    for a in alfabeto:
        if j == 5:
            break
        cuadro[j].append(a)
        i += 1
        if i == 5:
            j += 1
            i = 0
    return cuadro

def busca_letra(cuadro, letra):
    '''Busca la posicion de la letra en el cuadro de Playfair especificado.

    :param cuadro: el cuadro de Playfair.
    :param letra: la letra que sera buscada.
    :returns: una tupla (x, y) indicando la posicion de la letra en el cuadro
              de Playfair'''

    letra = letra.lower().strip()
    for i in range(0, 5):
        for j in range(0, 5):
            if cuadro[i][j] == letra:
                return (i, j)
    return (4, 4)    # La letra que falta se coloca en la ultima posicion.

cripto4 = 'YFGZRXFGBELFOJZLRNPHAFOBYFOHFGNPFPRXFNMYGNPQCVPEIZLEZNLFOKNTYDNTETBEMXNPRVNPLZGRLFOKRAOBOFECDKNVRANPPGPOEVFSFOOEOFMYPLRNNFYFPDASCEOFGNXRCENPRAONFCHOCPPNNGRNGBHMVNZQNFAFOBVNYNCEQAGEYFOHRGHJJZIGARBACPRALZOBRAOKTFOFIGKNFNCBARPNTMNTPNASFGEVYNHPFGFVASNPBEGIVINRDZASEVJZGZRXFGBEGKFNBPVFPKGBASNPPGAIOHRGHJJZIGRTVHLFZVASNPBEBOVEEBVSGZLZGBPDECPAMVFONPHPZAKEFNMVNPGBPDNPAPNPBEEVTMFRFSLPOVXQNFNPTENFPHOHIBAIGZRXFGBEPNNFTENFPLPKPFQEDPAPNPMXFOXFFAPAOBTNECTPFOFNNTGZPHLZBUOFIGMXNPNOEJRVRAMZGNPQGPRADBHMDKBOKERNEIRNGEIDNFPFETAPNORAIGMNFXPGMCAIZLOVXQNFDXRABGDPBPVHRNNTIVEBZEPDMKNGRNYFQAZLEIFNRTVFHZAOCEDINZFGKPDYPKCENPMZPAMXFOFNNTGBAKBPVFPNBNOVPCRXAIZLOVXQNFZYVCGBAKBPVFBNAVGNOFGRIBOFAIGZAIOHRGIGIVYKBPVFAIGZRXFGBERNRGBCCVOHIBMXAIVIFNNOLENPMZIVFCEVGLNFPGIVEBAIGZRXFGBEPNNRLETENFMYGNIEPAIEXJVFIGMXFIRGLEPNQDNFOBRNFAAFCBTKIADBGZVIBGFGAINGCPNOLFVNHGLEGJGETENROKGENRGBOANQVMFNPAIVEBECRAGBASEBRARTVFKGFTIETFTSVFGZMKBINTFTFNJHGZKSTFNBIJLZKSAIGZRXFGBERAGNQDOEPNMVPCNGEZFNSKNGDPYDIDKYRGCPHMUKRNPDPCQCVFECNPLZPVUTFINTAZAFOBOHIBAIOHRGIGIVEBRAFGAIFAPAECPAZETNDXAJFNOFPHPFMXFOFNNOCEIGMXNONRYGFGRORLBOAIZLOVXQNFZSYDCEIGOFRAOKTFHMXCOVFCRFDYRNOBOHIBAIGZRXFGBEJZIADBGZVIBGFGAINTOVQDNFVNJZGZRXFGBERAHZAZFBNPFPRXFNGPNFPVYARGCPPNQDEBQALOEVGLEJDBTFFMEBVNJZGZRXFGBEUMRFMYGNPQCVIGPNDBFNNTOFKTVFIGSNZFFCEPKEEVHGLEGJCEEVYNCEQADPNTMXRNNTQABICPUCAIFNRGLEMXAIFOOEPNPLEBOFGNORTZIEFXESNROKIOOKGEPKPNRAAZAFZGNTVGXQNFMCJKEVJZGZRXFGBEEJRAOBPNSKAIIAPEAIQALOCVAIPAPCEBOFHGLEGJBV'
