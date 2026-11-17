from Simulador.simulador import transmitirBits

bits = [0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1]

resultado = transmitirBits(
    bits,
    "Manchester",
    desvio_padrao=0.0
)

print("TX:", bits)
print("RX:", resultado["bitsRecebidos"])

assert resultado["bitsRecebidos"] == bits

print("Teste aprovado!")