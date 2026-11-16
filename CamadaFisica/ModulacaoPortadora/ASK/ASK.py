import math                         #biblioteca padrao do python, usada para o seno (sin) e o pi


def modularASK(
    bits: list[int],
    amplitude: float = 1.0,         #altura da onda quando o bit for 1
    frequencia: int = 2,            #quantas ondas completas cabem dentro de um bit
    amostragem: int = 100           #quantas amostras representam um bit
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

    sinal = []
    for bit in bits:
        if bit == 1:                    #bit 1: a onda balanca com altura cheia
            altura = amplitude
        else:                           #bit 0: a onda fica desligada (altura zero)
            altura = 0.0

        for k in range(amostragem):     #desenhamos um pedaco de senoide com "amostragem" pontos
            t = k / amostragem          #tempo dentro do bit, vai de 0 ate quase 1
            valor = altura * math.sin(2 * math.pi * frequencia * t)
            sinal.append(valor)

    return sinal


def demodularASK(
    sinal: list[float],
    amplitude: float = 1.0,
    frequencia: int = 2,
    amostragem: int = 100
) -> list[int]:

    if not sinal:
        raise ValueError("O sinal nao pode estar vazio.")

    if amostragem <= 0:
        raise ValueError("A amostragem deve ser positiva.")

    if len(sinal) % amostragem != 0:    #o sinal tem que ter um numero inteiro de bits
        raise ValueError("Quantidade de amostras invalida.")

    limite = amplitude / 2              #meio do caminho entre altura 0 (bit 0) e altura cheia (bit 1)

    bits_recebidos = []
    for inicio in range(0, len(sinal), amostragem):     #andamos de bit em bit
        soma = 0.0
        for k in range(amostragem):                     #correlacao: multiplica o recebido pela onda modelo e soma
            t = k / amostragem
            soma += sinal[inicio + k] * math.sin(2 * math.pi * frequencia * t)

        altura_estimada = 2 * soma / amostragem         #essa conta transforma a soma na altura da onda recebida

        if altura_estimada >= limite:
            bits_recebidos.append(1)
        else:
            bits_recebidos.append(0)

    return bits_recebidos