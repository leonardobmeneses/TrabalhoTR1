import random                       #biblioteca para usar a distribuicao gaussiana

def adicionarRuido(
    sinal: list[float],             #lista de sinais fisicos transmitidos em volts
    media: float,                
    desvioPadrao: float
) -> list[float]:

    sinal_recebido = []         
    for valor in sinal:
        ruido = random.gauss(media, desvioPadrao)
        valor_recebido = valor + ruido
        sinal_recebido.append(valor_recebido)
    return sinal_recebido