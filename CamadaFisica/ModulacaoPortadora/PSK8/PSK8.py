import math                         #biblioteca padrao do python, usada para o seno (sin) e o pi

BITS_POR_SIMBOLO = 3                #no 8PSK cada pedaco de onda carrega 3 bits (2^3 = 8 fases)

#tabela de Gray: a posicao na lista eh o numero da fase (0 a 7) e o valor sao os 3 bits daquela fase
#fase numero i fica em i * 45 graus. Fases vizinhas diferem em apenas 1 bit
TABELA_8PSK = [
    (0, 0, 0),                      #fase 0 ->   0 graus
    (0, 0, 1),                      #fase 1 ->  45 graus
    (0, 1, 1),                      #fase 2 ->  90 graus
    (0, 1, 0),                      #fase 3 -> 135 graus
    (1, 1, 0),                      #fase 4 -> 180 graus
    (1, 1, 1),                      #fase 5 -> 225 graus
    (1, 0, 1),                      #fase 6 -> 270 graus
    (1, 0, 0),                      #fase 7 -> 315 graus
]


def modular8PSK(
    bits: list[int],
    amplitude: float = 1.0,         #altura da onda (no PSK ela eh sempre a mesma)
    frequencia: int = 2,            #quantas ondas completas cabem em um simbolo (sempre a mesma)
    amostragem: int = 100           #quantas amostras representam um simbolo (3 bits)
) -> list[float]:

    if not bits:
        raise ValueError("A lista de bits nao pode estar vazia.")

    for bit in bits:
        if bit != 0 and bit != 1:
            raise ValueError("O bit deve ser 0 ou 1.")

    if amplitude <= 0:
        raise ValueError("A amplitude deve ser positiva.")

    if frequencia <= 0:
        raise ValueError("A frequencia deve ser positiva.")

    if amostragem <= 0:
        raise ValueError("A amostragem deve ser positiva.")

    #se a quantidade de bits nao for multiplo de 3, completamos com zeros no final (padding)
    bits_completos = list(bits)
    while len(bits_completos) % BITS_POR_SIMBOLO != 0:
        bits_completos.append(0)

    sinal = []
    for inicio in range(0, len(bits_completos), BITS_POR_SIMBOLO):     #andamos de 3 em 3 bits
        grupo = tuple(bits_completos[inicio:inicio + BITS_POR_SIMBOLO])
        numero_fase = TABELA_8PSK.index(grupo)                          #procura em qual fase esta esse grupo
        fase = numero_fase * 2 * math.pi / 8                            #converte para radianos (cada fase anda 45 graus)

        for k in range(amostragem):     #desenhamos um pedaco de senoide comecando na fase escolhida
            t = k / amostragem
            valor = amplitude * math.sin(2 * math.pi * frequencia * t + fase)
            sinal.append(valor)

    return sinal


def demodular8PSK(
    sinal: list[float],
    quantidade_bits: int,           #quantos bits foram enviados de verdade (para descartar o padding)
    frequencia: int = 2,
    amostragem: int = 100
) -> list[int]:

    if not sinal:
        raise ValueError("O sinal nao pode estar vazio.")

    if amostragem <= 0:
        raise ValueError("A amostragem deve ser positiva.")

    if len(sinal) % amostragem != 0:    #o sinal tem que ter um numero inteiro de simbolos
        raise ValueError("Quantidade de amostras invalida.")

    if quantidade_bits <= 0 or quantidade_bits > (len(sinal) // amostragem) * BITS_POR_SIMBOLO:
        raise ValueError("Quantidade de bits invalida para esse sinal.")

    bits_recebidos = []
    for inicio in range(0, len(sinal), amostragem):     #andamos de simbolo em simbolo
        melhor_fase = 0
        maior_soma = None
        for numero_fase in range(8):                    #comparamos o pedaco recebido com as 8 ondas modelo
            fase = numero_fase * 2 * math.pi / 8
            soma = 0.0
            for k in range(amostragem):                 #correlacao com a onda modelo dessa fase
                t = k / amostragem
                soma += sinal[inicio + k] * math.sin(2 * math.pi * frequencia * t + fase)

            if maior_soma is None or soma > maior_soma: #guardamos a fase que mais combinou ate agora
                maior_soma = soma
                melhor_fase = numero_fase

        bits_recebidos.extend(TABELA_8PSK[melhor_fase]) #a fase vencedora vira os seus 3 bits

    return bits_recebidos[:quantidade_bits]             #jogamos fora os zeros de padding