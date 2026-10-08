from MeioComunicacao.meio import adicionarRuido

sinalTransmitido = [1.0, 1,0, -1.0, 1.0, 2.0]
media = 0.0
desvio = 0.1

sinalRecebido = adicionarRuido(sinalTransmitido, media, desvio)

print("Sinal Transmitido: ", sinalTransmitido)
print("Sinal que Recebeu: ", sinalRecebido)