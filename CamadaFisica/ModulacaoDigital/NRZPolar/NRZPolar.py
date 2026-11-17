def codificarNRZPolar(
    bits : list[int],
    amplitude : float = 1.0,            #se o valor nao for passado, vai ser 1
    amostragem : int = 100,             #se o valor nao for passado, vai ser 100
):

    if not bits:
        raise ValueError("O campo nao pode estar vazio.")

    for bit in bits:
        if(bit != 1 and bit != 0):
            raise ValueError("O bit deve ser 1 ou 0.")

    if amplitude <= 0:
        raise ValueError("A amplitude nao pode ser menor ou igual a zero.")
    
    if amostragem <= 0:
        raise ValueError("O numero de amostras deve ser positivo.")

    sinal = []
    for bit in bits:
        if bit == 0:
            nivel = - amplitude
        else:
            nivel = amplitude
        for _ in range(amostragem):         #vamos repetir o valor pedido na amostragem
            sinal.append(float(nivel))
            
    return sinal

def decodificadorNRZPolar(
    amostras : list[float],
    limite : float = 0.0   
):

    if not amostras:
        raise ValueError("Devem existir amostras.")

    bits_recebidos = []
    for amostra in amostras:
        if amostra >= limite:                   #se sinal for maior que 0 vamos entender que eh o bit 1
            bits_recebidos.append(1)
        else:
            bits_recebidos.append(0)

    return bits_recebidos