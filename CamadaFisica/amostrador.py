def amostradorSinal(                    #essa funcao vai fazer a amostragem do nosso sinal
    sinal: list[float],
    amostragemPorBit: int = 100,    
) -> list[float]:

    if amostragemPorBit <= 0:
        raise ValueError("A amostragem deve ser positiva")
    
    if len(sinal) % amostragemPorBit != 0:   #basicamente, temos que verificar se a qtd de sinal eh compativel com o nivel de amostras que fizemos para cada sinal
        raise ValueError("Quantidade de amostras invalida.")

    if not sinal:
        raise ValueError("O sinal nao pode estar vazio.")

    amostras = []
    for inicio in range(0, len(sinal), amostragemPorBit):   #aqui eu escolho um valor que vai estar na amostra para ser decodificado
        centro = inicio + amostragemPorBit // 2
        amostras.append(sinal[centro])

    return amostras
