def codificarManchester(
    bits: list[int],
    amplitude: float = 1.0,
    amostragem: int = 100
) -> list[float]:

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
            primeiroNivel = -amplitude
            segundoNivel = amplitude
        else:                                   #se 1 o manchester vai fazer 10
            primeiroNivel = amplitude
            segundoNivel = -amplitude

        for _ in range(metade):
            sinal.append(float(primeiroNivel))
        for _ in range(metade):
            sinal.append(float(segundoNivel))

    return sinal

def decodificadorManchester(
    amostras: list[float],
    limite: float = 0.0
) -> list[int]:

    if not amostras:
        raise ValueError("A lista de amostras nao pode estar vazia.")

    if len(amostras) % 2 != 0:
        raise ValueError("A quantidade de amostras deve ser par.")

    bitsRecebidos = []

    for i in range(0, len(amostras), 2):    
        primeira = amostras[i]          #como te
        segunda = amostras[i + 1]

        if primeira >= limite and segunda < limite:
            bitsRecebidos.append(1)
        elif primeira < limite and segunda >= limite:
            bitsRecebidos.append(0)
        else:
            raise ValueError("Transicao Manchester invalida.")

    return bitsRecebidos