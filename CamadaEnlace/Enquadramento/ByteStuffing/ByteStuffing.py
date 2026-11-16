TAM_BYTE = 8                    # 1 "caractere" = 1 byte = 8 bits
FLAG_BYTE = "01111110"          # 0x7E: delimitador do byte stuffing
ESC_BYTE = "01111101"           # 0x7D: byte de escape do byte stuffing


# Enquadramento: flags com inserção de bytes (byte stuffing)
def byte_stuffing_TX(cargaUtil : str, tam_max_quadro : int) -> list[str]:
    """
    TX: quadro = FLAG + dados + FLAG. Se um byte dos dados for igual à FLAG ou
    ao ESC, insere-se um ESC antes dele.
    """
    
    if tam_max_quadro < 1:
        raise ValueError("tam_max_quadro deve ser pelo menos 1 byte.")
    
    tam = tam_max_quadro * TAM_BYTE
    quadros = []
    for dados in [cargaUtil[i:i + tam] for i in range(0, len(cargaUtil), tam)]:
        recheado = ""
        for i in range(0, len(dados), TAM_BYTE):
            byte = dados[i:i + TAM_BYTE]
            if byte in (FLAG_BYTE, ESC_BYTE):
                recheado += ESC_BYTE                        # insere o escape
            recheado += byte
        quadros.append(FLAG_BYTE + recheado + FLAG_BYTE)
    return quadros


def byte_stuffing_RX(fluxo : list[str]) -> str:
    """
    RX: percorre o fluxo byte a byte. FLAG abre/fecha quadro; ESC faz o byte
    seguinte ser tratado como dado. Retorna a lista de payloads.
    """

    for quadro in range(0, len(fluxo)):
        if len(fluxo[quadro]) % TAM_BYTE != 0:
            raise ValueError("Cada quadro deve ter número de bits múltiplo de 8.")

    quadros = ""
    atual = None            # None = fora de um quadro
    escapado = False
    for quadro in range(0, len(fluxo)):
        for i in range(0, len(fluxo[quadro]), TAM_BYTE):
            byte = fluxo[quadro][i:i + TAM_BYTE]
            if escapado:
                atual += byte                                   # byte literal
                escapado = False
            elif byte == FLAG_BYTE:
                if atual is None:
                    atual = ""                                  # abre quadro
                else:
                    if atual:
                        quadros += atual                   # fecha quadro
                    atual = None
            elif byte == ESC_BYTE:
                if atual is None:
                    raise ValueError("Escape fora de quadro.")
                escapado = True
            else:
                if atual is None:
                    raise ValueError("Dados fora de quadro.")
                atual += byte
        if atual is not None or escapado:
            raise ValueError("Quadro sem flag final.")
    return quadros