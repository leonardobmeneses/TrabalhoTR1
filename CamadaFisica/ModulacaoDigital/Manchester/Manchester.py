def codificarManchester(
    bits: list[int],
    amplitude: float = 1.0,
    amostragem: int = 100
):

    if not bits:
        raise ValueError("A lista de bits nao pode estar vazia.")

    for bit in bits:
        if bit != 0 and bit != 1:
            raise ValueError("O bit deve ser 0 ou 1.")

    if amplitude <= 0:
        raise ValueError("A amplitude deve ser positiva.")

    if amostragem <= 0 or amostragem % 2 != 0:
        raise ValueError("A amostragem deve ser positiva e par.")

    sinal = []
    metade = amostragem // 2                

    for bit in bits:
        if bit == 0:                            #se 0 o manchester vai fazer 01
            primeiro_nivel = -amplitude
            segundo_nivel = amplitude
        else:                                   #se 1 o manchester vai fazer 10
            primeiro_nivel = amplitude
            segundo_nivel = -amplitude

        for _ in range(metade):
            sinal.append(float(primeiro_nivel))
        for _ in range(metade):
            sinal.append(float(segundo_nivel))

    return sinal

def decodificadorManchester(
    amostras: list[float],
    limite: float = 0.0
):

    if not amostras:
        raise ValueError("A lista de amostras nao pode estar vazia.")

    if len(amostras) % 2 != 0:
        raise ValueError("A quantidade de amostras deve ser par.")

    bits_recebidos = []

    for i in range(0, len(amostras), 2):       #como teremos duas amostras para uma so mensagem entao vamos de dois em dois
        primeira = amostras[i]                 #vejo o primeiro bit e o segundo e analiso os sinais
        segunda = amostras[i + 1]

        if primeira >= limite and segunda < limite:
            bits_recebidos.append(1)
        elif primeira < limite and segunda >= limite:
            bits_recebidos.append(0)
        else:
            raise ValueError("Transicao Manchester invalida.")

    return bits_recebidos