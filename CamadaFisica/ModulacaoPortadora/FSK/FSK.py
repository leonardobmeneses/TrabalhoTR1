import math                         #biblioteca padrao do python, usada para o seno (sin) e o pi


def modularFSK(
    bits: list[int],
    amplitude: float = 1.0,         #altura da onda (no FSK ela eh sempre a mesma)
    frequencia0: int = 2,           #quantas ondas completas cabem em um bit quando o bit for 0 (onda devagar)
    frequencia1: int = 4,           #quantas ondas completas cabem em um bit quando o bit for 1 (onda rapida)
    amostragem: int = 100           #quantas amostras representam um bit
):

    if not bits:
        raise ValueError("A lista de bits nao pode estar vazia.")

    for bit in bits:
        if bit != 0 and bit != 1:
            raise ValueError("O bit deve ser 0 ou 1.")

    if amplitude <= 0:
        raise ValueError("A amplitude deve ser positiva.")

    if frequencia0 <= 0 or frequencia1 <= 0:
        raise ValueError("As frequencias devem ser positivas.")

    if frequencia0 == frequencia1:  #se as duas forem iguais o receptor nao consegue diferenciar 0 de 1
        raise ValueError("As frequencias do bit 0 e do bit 1 devem ser diferentes.")

    if amostragem <= 0:
        raise ValueError("A amostragem deve ser positiva.")

    sinal = []
    for bit in bits:
        if bit == 1:                    #bit 1: onda rapida
            frequencia = frequencia1
        else:                           #bit 0: onda devagar
            frequencia = frequencia0

        for k in range(amostragem):     #desenhamos um pedaco de senoide com "amostragem" pontos
            t = k / amostragem          #tempo dentro do bit, vai de 0 ate quase 1
            valor = amplitude * math.sin(2 * math.pi * frequencia * t)
            sinal.append(valor)

    return sinal


def demodularFSK(
    sinal: list[float],
    frequencia0: int = 2,
    frequencia1: int = 4,
    amostragem: int = 100
):

    if not sinal:
        raise ValueError("O sinal nao pode estar vazio.")

    if amostragem <= 0:
        raise ValueError("A amostragem deve ser positiva.")

    if len(sinal) % amostragem != 0:    #o sinal tem que ter um numero inteiro de bits
        raise ValueError("Quantidade de amostras invalida.")

    bits_recebidos = []
    for inicio in range(0, len(sinal), amostragem):     #andamos de bit em bit
        soma0 = 0.0                                     #o quanto o pedaco recebido parece com a onda devagar
        soma1 = 0.0                                     #o quanto o pedaco recebido parece com a onda rapida
        for k in range(amostragem):
            t = k / amostragem
            soma0 += sinal[inicio + k] * math.sin(2 * math.pi * frequencia0 * t)
            soma1 += sinal[inicio + k] * math.sin(2 * math.pi * frequencia1 * t)

        if soma1 >= soma0:              #parece mais com a onda rapida: bit 1
            bits_recebidos.append(1)
        else:                           #parece mais com a onda devagar: bit 0
            bits_recebidos.append(0)

    return bits_recebidos