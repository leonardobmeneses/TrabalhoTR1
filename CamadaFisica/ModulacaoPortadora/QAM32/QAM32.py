import math                         #biblioteca padrao do python, usada para o seno, o cosseno e o pi

BITS_POR_SIMBOLO = 5                #no 32-QAM cada pedaco de onda carrega 5 bits (2^5 = 32 pontos)
NIVEIS = [-5, -3, -1, 1, 3, 5]      #valores possiveis de I e de Q (uma grade 6 x 6)
NIVEL_MAXIMO = 5


def montarConstelacao():
    #monta os 32 pontos (I, Q): uma grade 6 x 6 = 36 pontos, tirando os 4 cantos = 32 pontos
    #a posicao do ponto na lista (0 a 31) eh o numero que os 5 bits representam
    pontos = []
    for i in NIVEIS:
        for q in NIVEIS:
            if abs(i) == NIVEL_MAXIMO and abs(q) == NIVEL_MAXIMO:  #pula os 4 cantos
                continue
            pontos.append((i, q))
    return pontos


CONSTELACAO_32QAM = montarConstelacao()


def bitsParaNumero(grupo: list[int]):
    #converte uma lista de bits em numero, ex.: [0, 1, 0, 1, 1] -> 11
    numero = 0
    for bit in grupo:
        numero = numero * 2 + bit
    return numero


def numeroParaBits(numero: int, quantidade: int):
    #converte um numero em uma lista de bits com tamanho fixo, ex.: (11, 5) -> [0, 1, 0, 1, 1]
    grupo = []
    for _ in range(quantidade):
        grupo.insert(0, numero % 2)     #pega o ultimo bit e coloca na frente
        numero = numero // 2
    return grupo


def modular32QAM(
    bits: list[int],
    amplitude: float = 1.0,         #tensao do nivel mais alto da grade (I ou Q igual a 5)
    frequencia: int = 2,            #quantas ondas completas cabem em um simbolo
    amostragem: int = 100           #quantas amostras representam um simbolo (5 bits)
):

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

    escala = amplitude / NIVEL_MAXIMO   #transforma os niveis da grade (-5 a 5) em volts

    #se a quantidade de bits nao for multiplo de 5, completamos com zeros no final (padding)
    bits_completos = list(bits)
    while len(bits_completos) % BITS_POR_SIMBOLO != 0:
        bits_completos.append(0)

    sinal = []
    for inicio in range(0, len(bits_completos), BITS_POR_SIMBOLO):     #andamos de 5 em 5 bits
        grupo = bits_completos[inicio:inicio + BITS_POR_SIMBOLO]
        i, q = CONSTELACAO_32QAM[bitsParaNumero(grupo)]                 #os 5 bits escolhem um ponto (I, Q)

        for k in range(amostragem):
            t = k / amostragem
            #a onda eh a soma de uma onda seno com altura I e uma onda cosseno com altura Q
            valor = escala * (i * math.sin(2 * math.pi * frequencia * t)
                              + q * math.cos(2 * math.pi * frequencia * t))
            sinal.append(valor)

    return sinal


def demodular32QAM(
    sinal: list[float],
    quantidade_bits: int,           #quantos bits foram enviados de verdade (para descartar o padding)
    amplitude: float = 1.0,
    frequencia: int = 2,
    amostragem: int = 100
):

    if not sinal:
        raise ValueError("O sinal nao pode estar vazio.")

    if amplitude <= 0:
        raise ValueError("A amplitude deve ser positiva.")

    if amostragem <= 0:
        raise ValueError("A amostragem deve ser positiva.")

    if len(sinal) % amostragem != 0:    #o sinal tem que ter um numero inteiro de simbolos
        raise ValueError("Quantidade de amostras invalida.")

    if quantidade_bits <= 0 or quantidade_bits > (len(sinal) // amostragem) * BITS_POR_SIMBOLO:
        raise ValueError("Quantidade de bits invalida para esse sinal.")

    escala = amplitude / NIVEL_MAXIMO

    bits_recebidos = []
    for inicio in range(0, len(sinal), amostragem):     #andamos de simbolo em simbolo
        soma_seno = 0.0
        soma_cosseno = 0.0
        for k in range(amostragem):                     #correlacao com a onda seno e com a onda cosseno
            t = k / amostragem
            soma_seno += sinal[inicio + k] * math.sin(2 * math.pi * frequencia * t)
            soma_cosseno += sinal[inicio + k] * math.cos(2 * math.pi * frequencia * t)

        #igual ao ASK: 2 * soma / amostragem da a altura; dividindo pela escala voltamos para a grade
        i_estimado = 2 * soma_seno / amostragem / escala
        q_estimado = 2 * soma_cosseno / amostragem / escala

        #procuramos o ponto da constelacao mais perto do ponto (I, Q) que chegou
        melhor_numero = 0
        menor_distancia = None
        for numero, (i, q) in enumerate(CONSTELACAO_32QAM):
            distancia = (i - i_estimado) ** 2 + (q - q_estimado) ** 2
            if menor_distancia is None or distancia < menor_distancia:
                menor_distancia = distancia
                melhor_numero = numero

        bits_recebidos.extend(numeroParaBits(melhor_numero, BITS_POR_SIMBOLO))

    return bits_recebidos[:quantidade_bits]             #jogamos fora os zeros de padding