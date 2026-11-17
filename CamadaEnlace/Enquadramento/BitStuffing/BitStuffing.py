TAM_BYTE = 8                    # 1 "caractere" = 1 byte = 8 bits
FLAG_BIT = "01111110"           # delimitador do bit stuffing

# Função auxiliar para validar o trem de bits
def _validar_payload(bits : str):
    """Garante que o payload é uma string de bits com tamanho múltiplo de 8."""
    if not isinstance(bits, str) or set(bits) - {"0", "1"}:
        raise ValueError("O trem de bits deve ser uma string de '0' e '1'.")
    if len(bits) % TAM_BYTE != 0:
        raise ValueError("O payload deve ter número de bits múltiplo de 8.")



# Enquadramento: flags com inserção de bits (bit stuffing)
def _inserir_bits(dados : str):
    """Insere um '0' depois de cada sequência de cinco '1' consecutivos."""
    saida = ""
    uns = 0
    for b in dados:
        saida += b
        if b == "1":
            uns += 1
            if uns == 5:
                saida += "0"
                uns = 0
        else:
            uns = 0
    return saida


def _remover_bits(dados : str):
    """Remove o '0' que segue cada sequência de cinco '1' consecutivos."""
    saida = ""
    uns = 0
    i = 0
    while i < len(dados):
        b = dados[i]
        saida += b
        if b == "1":
            uns += 1
            if uns == 5:
                if i + 1 >= len(dados) or dados[i + 1] != "0":
                    raise ValueError("Bit stuffing inválido: quadro corrompido.")
                i += 1                                      # pula o '0' inserido
                uns = 0
        else:
            uns = 0
        i += 1
    return saida


def bit_stuffing_TX(bits : str, tam_max_quadro : int):
    """TX: quadro = FLAG + dados com bit stuffing + FLAG."""
    _validar_payload(bits)

    if tam_max_quadro < 1:
            raise ValueError("tam_max_quadro deve ser pelo menos 1 byte.")
    
    tam = tam_max_quadro * TAM_BYTE

    return [FLAG_BIT + _inserir_bits(dados) + FLAG_BIT
            for dados in [bits[i:i + tam] for i in range(0, len(bits), tam)]]


def bit_stuffing_RX(fluxo : list[str]):
    """RX: valida as flags de cada quadro, remove-as e desfaz o bit stuffing."""
    if not fluxo:
        raise ValueError("Fluxo vazio.")

    tam_flag  = len(FLAG_BIT)
    cargaUtil = ""
    for quadro in fluxo:
        if (len(quadro)) < 2 * tam_flag or not quadro.startswith(FLAG_BIT) or not quadro.endswith(FLAG_BIT):
            raise ValueError("Quadro sem flags de início/fim: quadro corrompido.")

        recheado = quadro[tam_flag:-tam_flag]   # removendo as flags

        if FLAG_BIT in recheado:
            raise ValueError("Flag dentro dos dados: quadro corrompido.")

        cargaUtil += _remover_bits(recheado)

    return cargaUtil