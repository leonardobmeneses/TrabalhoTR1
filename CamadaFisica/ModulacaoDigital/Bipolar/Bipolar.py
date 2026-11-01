def codificarBipolar(
    bits: list[int],
    amplitude: float = 1.0,
    amostragem: int = 100
)-> list[float]:

    if not bits:
        raise ValueError("Deve ser enviada uma lista de bits.")

    if amplitude <= 0:
        raise ValueError("A amplitude nao pode ser nula ou negativa.")

    if amostragem <= 0:
        raise ValueError("A amostragem deve ser positiva.")

    sinal = []
    flag = False
    for bit in bits:
        if bit != 0 and bit != 1:
            raise ValueError("O bit deve ser 1 ou 0.")
        elif bit == 0:
            nivel = 0.0
        elif bit == 1:
            if not flag:
                nivel = amplitude
                flag = True
            else:
                nivel = -amplitude
                flag = False
        for _ in range(amostragem):
            sinal.append(float(nivel))       

    return sinal

def decodificadorBipolar(
    amostras: list[float],
    amplitude: float = 1.0,
)-> list[int]:

    limite = amplitude / 2

    if not amostras:
        raise ValueError("Devem existir amostras.")

    bits_recebidos = []
    for amostra in amostras:
        amostra = abs(amostra)
        if amostra >= limite:
            bits_recebidos.append(1)
        else:
            bits_recebidos.append(0)

    return bits_recebidos    


