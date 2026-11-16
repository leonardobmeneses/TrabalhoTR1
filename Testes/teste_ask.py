from CamadaFisica.ModulacaoPortadora.ASK.ASK import modularASK, demodularASK
from MeioComunicacao.meio import adicionarRuido
import random


def main():
    bits = [1, 0, 1, 1, 0, 0, 1, 0]
    amplitude = 1.0
    frequencia = 2
    amostragem = 100

    # Teste 1 - sem ruido
    sinal = modularASK(bits, amplitude, frequencia, amostragem)
    bitsRecebidos = demodularASK(sinal, amplitude, frequencia, amostragem)

    print("Teste ASK sem ruido")
    print("Bits transmitidos:", bits)
    print("Quantidade de amostras:", len(sinal))
    print("Bits recebidos:", bitsRecebidos)

    if bits == bitsRecebidos:
        print("Teste ASK passou!")
    else:
        print("Erro na demodulacao!")

    # Teste 2 - com ruido AWGN
    random.seed(42)
    sinalComRuido = adicionarRuido(sinal, media=0.0, desvioPadrao=0.5)
    bitsComRuido = demodularASK(sinalComRuido, amplitude, frequencia, amostragem)

    print("\nTeste ASK com ruido")
    print("Bits transmitidos:", bits)
    print("Bits recebidos:", bitsComRuido)

    if bits == bitsComRuido:
        print("Transmissao ASK realizada com sucesso!")
    else:
        print("Houve erro na transmissao!")


if __name__ == "__main__":
    main()