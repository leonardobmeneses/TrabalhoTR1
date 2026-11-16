TAM_BYTE = 8                    # 1 "caractere" = 1 byte = 8 bits

# Enquadramento: entrelaçamento de bits
def entrelacamento_TX(cargaUtil : str, tam_max_quadro : int) -> list[str]:
    """
    TX: o payload é dividido em N linhas de tam_max_quadro bytes;
    é calculado o bit de paridade para cada coluna
    e ocorre a transmissão.
    """
    
    if tam_max_quadro < 1:
        raise ValueError("tam_max_quadro deve ser pelo menos 1 byte.")

    tam_linha = tam_max_quadro * TAM_BYTE
    matriz = [cargaUtil[i:i + tam_linha] for i in range(0, len(cargaUtil), tam_linha)]

    paridade = ""

    for colunas in range(tam_linha):
        conta_uns = 0
        
        for linhas in range(len(matriz)):
            if(matriz[linhas][colunas]=="1"): conta_uns+=1

        paridade += str(conta_uns%2)

    matriz.append(paridade)

    return matriz


def entrelacamento_RX(fluxo : list[str]) -> str:
    """
    RX: desfaz o entrelaçamento (lê por colunas, reconstrói as linhas) e
    verifica a paridade de cada coluna.
    """
    if not fluxo: return ""

    paridade_recebida = fluxo.pop()     # Removendo a linha de paridade do fluxo recebido
    tam_linha = len(paridade_recebida)

    paridade_calculada = ""
    
    for colunas in range(0, tam_linha):
        conta_uns = 0
        
        for linhas in range(len(fluxo)):
            if not fluxo[linhas][colunas]: continue
            if(fluxo[linhas][colunas]=="1"): conta_uns+=1

        paridade_calculada += str(conta_uns%2)


    if not paridade_calculada == paridade_recebida:
        diff=0
        for i in range(0,tam_linha):
            if paridade_recebida[i] != paridade_calculada[i]: diff+=1
        raise ValueError(f"Erro detectado. Os bits de paridade divergem em {diff} colunas.")

    bits = ""
    for linhas in fluxo:
        bits+=linhas

    return bits