TAM_BYTE = 8
# Funções auxiliares
def inteiro_para_bits(valor : int, n_bits=TAM_BYTE) -> str:
    """Converte um inteiro em string de n_bits bits (MSB primeiro)."""
    if valor < 0 or valor >= 2 ** n_bits:
        raise ValueError("Valor não cabe em {} bits.".format(n_bits))
    return format(valor, "0{}b".format(n_bits))

def bits_para_inteiro(bits : str) -> int:
    """Converte uma string de bits (MSB primeiro) em inteiro."""
    return int(bits, 2) if bits else 0

# Enquadramento - contagem de caracteres
def contagem_caracteres_TX(cargaUtil : str, tam_max_quadro : int) -> list[str]:
    """
    contagem_caracteres_TX: [contagem (1byte)] + dados
    contagem não inclui o próprio cabeçalho (decisão de projeto)
    por isso tam_max_quadro varia de 1 a 255 bytes.
    Retorna uma lista de quadros (strings de bits)
    """

    if tam_max_quadro < 1:
        raise ValueError("tam_max_quadro deve ser pelo menos 1 byte.")
    elif tam_max_quadro > 255:
        raise ValueError("Na contagem de caracteres, tam_max_quadro <= 255.")

    tam = tam_max_quadro * TAM_BYTE

    quadros = []
    for i in range(0, len(cargaUtil), tam):
        dados = cargaUtil[i:i+tam]
        contagem = len(dados) // TAM_BYTE
        quadros.append(inteiro_para_bits(contagem) + dados)
    return quadros

def contagem_caracteres_RX(fluxo : list[str]) -> str:
    """
    contagem_caracteres_RX: Recebe os quadros e remove o cabeçalho.
    Retorna a cargaUtil. Lança ValueError se contagem for inválida.
    """

    quadros = ""
    for i in range (0, len(fluxo)):
        pos = 0
        while pos < len(fluxo[i]):

            if pos + TAM_BYTE > len(fluxo[i]):
                raise ValueError("Cabeçalho de contagem incompleto.")
            
            contagem = bits_para_inteiro(fluxo[i][pos:pos + TAM_BYTE])
            fim = pos + TAM_BYTE + contagem * TAM_BYTE

            if contagem < 1 or fim > len(fluxo[i]):
                raise ValueError("Contagem inválida: quadro corrompido.")
            
            quadros += fluxo[i][pos + TAM_BYTE:fim]
            pos = fim
    return quadros
