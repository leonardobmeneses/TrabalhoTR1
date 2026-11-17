GERADOR = "100000100110000010001110110110111"   # x^32 + x^26 + ... + 1 (0x104C11DB7)
TAM_CRC = 32

def _resto_crc(bits : str) -> str:
    """
    Divide (bits + 32 zeros) pelo gerador, módulo 2, e devolve o resto de 32 bits.
    """
    dividendo = list(bits + "0" * TAM_CRC)
    for i in range(len(bits)):
        if dividendo[i] == "1":                       # só divide onde há '1' à frente
            for j in range(len(GERADOR)):
                dividendo[i + j] = str(int(dividendo[i + j]) ^ int(GERADOR[j]))   # XOR
    return "".join(dividendo[-TAM_CRC:])

def crc_TX(quadros : list[str]) -> list[str]:
    """TX: calcula o CRC-32 de cada quadro e o anexa ao final."""
    saida = []
    for quadro in quadros:
        if not quadro:
            raise ValueError("Quadro vazio.")
        saida.append(quadro + _resto_crc(quadro))
    return saida


def crc_RX(quadros : list[str]) -> list[str]:
    """
    RX: separa o CRC, recalcula sobre os dados e compara; devolve os quadros sem o CRC.
    """
    saida = []
    for quadro in quadros:
        if len(quadro) <= TAM_CRC:
            raise ValueError("Quadro curto demais para conter dados + CRC.")
        dados, crc = quadro[:-TAM_CRC], quadro[-TAM_CRC:]
        if _resto_crc(dados) != crc:
            raise ValueError("Erro detectado pelo CRC-32.")
        saida.append(dados)
    return saida