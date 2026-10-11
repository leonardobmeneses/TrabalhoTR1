import random                       #biblioteca para usar a distribuicao gaussiana

def adicionarRuido(
    sinal: list[float],             #lista de sinais fisicos transmitidos em volts
    media: float,                
    desvioPadrao: float
) -> list[float]:
    if desvioPadrao < 0:
        raise ValueError("o Desvio padrao nao pode ser negativo")

    sinal_recebido = []         
    for valor in sinal:
        ruido = random.gauss(media, desvioPadrao)
        valor_recebido = valor + ruido
        sinal_recebido.append(valor_recebido)
    return sinal_recebido