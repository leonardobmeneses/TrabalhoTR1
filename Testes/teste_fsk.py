from CamadaFisica.ModulacaoPortadora.FSK.FSK import modularFSK, demodularFSK
from MeioComunicacao.meio import adicionarRuido
import random


def main():
    bits = [1, 0, 1, 1, 0, 0, 1, 0]
    amplitude = 1.0
    frequencia0 = 2
    frequencia1 = 4
    amostragem = 100

    # Teste 1 - sem ruido
    sinal = modularFSK(bits, amplitude, frequencia0, frequencia1, amostragem)
    bitsRecebidos = demodularFSK(sinal, frequencia0, frequencia1, amostragem)

    print("Teste FSK sem ruido")
    print("Bits transmitidos:", bits)
    print("Quantidade de amostras:", len(sinal))
    print("Bits recebidos:", bitsRecebidos)

    if bits == bitsRecebidos:
        print("Teste FSK passou!")
    else:
        print("Erro na demodulacao!")

    # Teste 2 - com ruido AWGN
    random.seed(42)
    sinalComRuido = adicionarRuido(sinal, media=0.0, desvioPadrao=0.5)
    bitsComRuido = demodularFSK(sinalComRuido, frequencia0, frequencia1, amostragem)

    print("\nTeste FSK com ruido")
    print("Bits transmitidos:", bits)
    print("Bits recebidos:", bitsComRuido)

    if bits == bitsComRuido:
        print("Transmissao FSK realizada com sucesso!")
    else:
        print("Houve erro na transmissao!")


if __name__ == "__main__":
    main()