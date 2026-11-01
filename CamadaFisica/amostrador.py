def amostradorSinal(                    #essa funcao vai fazer a amostragem do nosso sinal
    sinal: list[float],
    amostragem_por_bit: int = 100,    
) -> list[float]:

    if amostragem_por_bit <= 0:
        raise ValueError("A amostragem deve ser positiva")
    
    if len(sinal) % amostragem_por_bit != 0:   #basicamente, temos que verificar se a qtd de sinal eh compativel com o nivel de amostras que fizemos para cada sinal
        raise ValueError("Quantidade de amostras invalida.")

    if not sinal:
        raise ValueError("O sinal nao pode estar vazio.")

    amostras = []
    for inicio in range(0, len(sinal), amostragem_por_bit):   #aqui eu escolho um valor que vai estar na amostra para ser decodificado
        centro = inicio + amostragem_por_bit // 2
        amostras.append(sinal[centro])

    return amostras
