# Correcao de erros - Codigo de Hamming
# Os bits de paridade ficam nas posicoes que sao potencia de 2 (1, 2, 4, 8, ...),
# contando as posicoes a partir de 1. Os bits de dados ocupam as outras posicoes.
# Cada bit de paridade usa paridade par sobre as posicoes que ele "vigia".


# Funcoes auxiliares
def _validar_bits(bits : str):
    """Garante que a entrada eh uma string nao vazia de '0' e '1'."""
    if not isinstance(bits, str) or not bits or set(bits) - {"0", "1"}:
        raise ValueError("A entrada deve ser uma string nao vazia de '0' e '1'.")

def _eh_potencia_de_2(numero : int) -> bool:
    """Retorna True se o numero for 1, 2, 4, 8, 16, ..."""
    potencia = 1
    while potencia < numero:
        potencia *= 2
    return potencia == numero

def _quantidade_bits_paridade(m : int):
    """Menor r tal que 2^r >= m + r + 1 (m = quantidade de bits de dados)."""
    r = 0
    while 2 ** r < m + r + 1:
        r += 1
    return r

def _paridade_do_grupo(palavra : list[str], p : int):
    """
    Soma (em paridade) os bits das posicoes vigiadas pelo bit de paridade p.
    A posicao 'pos' eh vigiada por p quando, em binario, 'pos' tem o bit p ligado
    (por exemplo, p = 2 vigia 2, 3, 6, 7, 10, 11, ...).
    Retorna 0 se a quantidade de 1s for par e 1 se for impar.
    """
    paridade = 0
    for pos in range(1, len(palavra)):
        if pos & p:
            paridade ^= int(palavra[pos])
    return paridade


# Codigo de Hamming - transmissor
def hamming_TX(dados : str) -> str:
    """
    hamming_TX: recebe os bits de dados e devolve a palavra de codigo,
    com os bits de paridade inseridos nas posicoes potencia de 2.
    Ex.: '1011' (4 bits de dados) -> 7 bits (3 de paridade).
    """
    _validar_bits(dados)

    m = len(dados)
    r = _quantidade_bits_paridade(m)
    n = m + r

    # Lista com uma posicao extra no inicio para contar as posicoes a partir de 1
    palavra = ["0"] * (n + 1)

    # 1) Coloca os bits de dados nas posicoes que NAO sao potencia de 2
    j = 0
    for pos in range(1, n + 1):
        if not _eh_potencia_de_2(pos):
            palavra[pos] = dados[j]
            j += 1

    # 2) Calcula cada bit de paridade (posicoes 1, 2, 4, 8, ...)
    #    Como a posicao p ainda vale '0', a conta considera so os outros bits do grupo
    p = 1
    while p <= n:
        palavra[p] = str(_paridade_do_grupo(palavra, p))
        p *= 2

    return "".join(palavra[1:])


# Codigo de Hamming - receptor
def hamming_RX(codigo : str):
    """
    hamming_RX: recebe a palavra de codigo, corrige ate 1 bit errado
    e devolve (dados, posicao_corrigida).
    posicao_corrigida = 0 significa que nenhum erro foi encontrado.
    Lanca ValueError se a sindrome apontar para fora da palavra
    (sinal de que houve mais de um erro).
    """
    _validar_bits(codigo)

    n = len(codigo)
    palavra = ["0"] + list(codigo)      # posicoes contadas a partir de 1

    # 1) Recalcula cada grupo. Grupo com paridade impar soma sua posicao na sindrome
    sindrome = 0
    p = 1
    while p <= n:
        if _paridade_do_grupo(palavra, p) == 1:
            sindrome += p
        p *= 2

    # 2) A sindrome eh a posicao do bit errado: inverte esse bit
    if sindrome > n:
        raise ValueError("Mais de um erro detectado: nao eh possivel corrigir.")
    if sindrome != 0:
        palavra[sindrome] = "1" if palavra[sindrome] == "0" else "0"

    # 3) Retira os bits de paridade e devolve so os dados
    dados = ""
    for pos in range(1, n + 1):
        if not _eh_potencia_de_2(pos):
            dados += palavra[pos]

    return dados, sindrome