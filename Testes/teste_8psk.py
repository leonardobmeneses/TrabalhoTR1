from CamadaFisica.ModulacaoPortadora.PSK8.PSK8 import modular8PSK, demodular8PSK
from MeioComunicacao.meio import adicionarRuido
import random


def main():
    bits = [1, 0, 1, 1, 0, 0, 1, 0]     #8 bits: nao eh multiplo de 3, entao testa o padding
    amplitude = 1.0
    frequencia = 2
    amostragem = 100

    # Teste 1 - sem ruido
    sinal = modular8PSK(bits, amplitude, frequencia, amostragem)
    bitsRecebidos = demodular8PSK(sinal, len(bits), frequencia, amostragem)

    print("Teste 8PSK sem ruido")
    print("Bits transmitidos:", bits)
    print("Quantidade de amostras:", len(sinal))
    print("Bits recebidos:", bitsRecebidos)

    if bits == bitsRecebidos:
        print("Teste 8PSK passou!")
    else:
        print("Erro na demodulacao!")

    # Teste 2 - com ruido AWGN
    random.seed(42)
    sinalComRuido = adicionarRuido(sinal, media=0.0, desvioPadrao=0.5)
    bitsComRuido = demodular8PSK(sinalComRuido, len(bits), frequencia, amostragem)

    print("\nTeste 8PSK com ruido")
    print("Bits transmitidos:", bits)
    print("Bits recebidos:", bitsComRuido)

    if bits == bitsComRuido:
        print("Transmissao 8PSK realizada com sucesso!")
    else:
        print("Houve erro na transmissao!")


if __name__ == "__main__":
    main()