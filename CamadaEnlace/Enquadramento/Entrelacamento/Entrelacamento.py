TAM_BYTE = 8


def entrelacamento_TX(cargaUtil: str, tam_max_quadro: int) -> list[str]:
    if tam_max_quadro < 1:
        raise ValueError("tam_max_quadro deve ser pelo menos 1 byte.")
    tam_linha = tam_max_quadro * TAM_BYTE
    matriz = [
        cargaUtil[i:i + tam_linha]
        for i in range(0, len(cargaUtil), tam_linha)
    ]
    paridade = ""

    for coluna in range(tam_linha):
        conta_uns = 0
        for linha in matriz:
            # Verifica se a coluna existe nesta linha
            if coluna < len(linha):
                if linha[coluna] == "1":
                    conta_uns += 1
        paridade += str(conta_uns % 2)
    matriz.append(paridade)
    return matriz

def entrelacamento_RX(fluxo: list[str]) -> str:
    if not fluxo:
        return ""
    # Nao modifica a lista original
    paridade_recebida = fluxo[-1]
    linhas_dados = fluxo[:-1]
    tam_linha = len(paridade_recebida)
    paridade_calculada = ""
    for coluna in range(tam_linha):
        conta_uns = 0
        for linha in linhas_dados:
            # Ignora colunas inexistentes
            if coluna < len(linha):
                if linha[coluna] == "1":
                    conta_uns += 1
        paridade_calculada += str(conta_uns % 2)
    if paridade_calculada != paridade_recebida:
        diff = 0
        for i in range(tam_linha):
            if paridade_recebida[i] != paridade_calculada[i]:
                diff += 1
        raise ValueError(
            f"Erro detectado. Os bits de paridade "
            f"divergem em {diff} colunas."
        )
    bits = ""
    for linha in linhas_dados:
        bits += linha
    return bits