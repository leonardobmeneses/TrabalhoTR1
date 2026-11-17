# Função auxiliar para soma de bits
def somar_bits(a : str, b : str, n_bits : int) -> str:
    soma = (int(a, 2) + int(b, 2)) & ((1 << n_bits) - 1)   # descarta o carry final
    return format(soma, f"0{n_bits}b")

# Função auxiliar para inverter bits
def inverter_bits(bits : str) -> str:
    return bits.translate(str.maketrans("01", "10"))

# Função auxiliar para dividir o quadro em duas metades de mesmo tamanho
def _dividir_em_metades(quadro : str) -> tuple[str, str]:
    """
    Divide o quadro em duas metades de n bits, com n = metade arredondada para cima.
    Se o quadro tiver tamanho ímpar, a segunda metade é completada com um '0'
    apenas para a conta (esse '0' não é transmitido).
    """
    n = (len(quadro) + 1) // 2
    return quadro[:n], quadro[n:].ljust(n, "0")

def checksum_TX(quadros : list[str]) -> list[str]:
    """
    TX: divide cada quadro pela metade e calcula o checksum.
    Depois, adiciona o checksum ao final do quadro.
    """
    saida = []
    for quadro in quadros:
        if not quadro:
            raise ValueError("Quadro vazio.")
        first, second = _dividir_em_metades(quadro)
        checksum = inverter_bits(somar_bits(first, second, len(first)))
        saida.append(quadro + checksum)

    return saida

def checksum_RX(quadros : list[str]) -> list[str]:
    """
    RX: faz a soma das três partes (início + fim + checksum).
    Depois, inverte elas e ao fim, se resultado = 0, funcionou.
    Caso contrário, ocorreu erro na transmissão do quadro.
    O checksum tem n bits, com n = metade do quadro arredondada para cima,
    então n = (tamanho recebido + 2) // 3.
    """
    saida = []
    for quadro in quadros:
        if len(quadro) < 2:
            raise ValueError("Quadro curto demais para conter dados + checksum.")
        n = (len(quadro) + 2) // 3
        dados, check = quadro[:-n], quadro[-n:]
        first, second = _dividir_em_metades(dados)

        total = somar_bits(somar_bits(first, second, n), check, n)

        if inverter_bits(total) != "0" * n:
            raise ValueError("Erro no checksum.")

        saida.append(dados)

    return saida
