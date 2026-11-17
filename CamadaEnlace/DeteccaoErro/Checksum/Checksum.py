# Função auxiliar para soma de bits
def somar_bits(a : str, b : str, n_bits : int) -> str:
    soma = (int(a, 2) + int(b, 2)) & ((1 << n_bits) - 1)   # descarta o carry final
    return format(soma, f"0{n_bits}b")

# Função auxiliar para inverter bits
def inverter_bits(bits : str) -> str:
    return bits.translate(str.maketrans("01", "10"))

def checksum_TX(quadros : list[str]) -> str:
    """
    TX: divide cada quadro pela metade e calcula o checksum.
    Depois, adiciona o checksum ao final do quadro.
    """
    for i in range(0, len(quadros)):
        quadro = quadros[i]
        mid = len(quadro) // 2
        first = quadro[0:mid]
        second = quadro[mid:]
        checksum = inverter_bits(somar_bits(first, second, len(first)))
        quadros[i] += checksum
    
    return quadros

def checksum_RX(quadros : list[str]) -> list[str]:
    """
    RX: faz a soma das três partes (início + fim + checksum).
    Depois, inverte elas e ao fim, se resultado = 0, funcionou.
    Caso contrário, ocorreu erro na transmissão do quadro.
    """
    saida = []
    for quadro in quadros:
        n = len(quadro) // 3
        first, second, check = quadro[:n], quadro[n:2*n], quadro[2*n:]

        total = somar_bits(somar_bits(first, second, n), check, n)

        if inverter_bits(total) != "0" * n:
            raise ValueError("Erro no checksum.")
        
        saida.append(first + second)
        
    return saida