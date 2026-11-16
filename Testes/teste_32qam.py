from CamadaFisica.ModulacaoPortadora.QAM32.QAM32 import modular32QAM, demodular32QAM
from MeioComunicacao.meio import adicionarRuido
import random


def main():
    bits = [1, 0, 1, 1, 0, 0, 1, 0]     #8 bits: nao eh multiplo de 5, entao testa o padding
    amplitude = 1.0
    frequencia = 2
    amostragem = 100

    # Teste 1 - sem ruido
    sinal = modular32QAM(bits, amplitude, frequencia, amostragem)
    bitsRecebidos = demodular32QAM(sinal, len(bits), amplitude, frequencia, amostragem)

    print("Teste 32-QAM sem ruido")
    print("Bits transmitidos:", bits)
    print("Quantidade de amostras:", len(sinal))
    print("Bits recebidos:", bitsRecebidos)

    if bits == bitsRecebidos:
        print("Teste 32-QAM passou!")
    else:
        print("Erro na demodulacao!")

    # Teste 2 - com ruido AWGN
    random.seed(42)
    sinalComRuido = adicionarRuido(sinal, media=0.0, desvioPadrao=0.5)
    bitsComRuido = demodular32QAM(sinalComRuido, len(bits), amplitude, frequencia, amostragem)

    print("\nTeste 32-QAM com ruido")
    print("Bits transmitidos:", bits)
    print("Bits recebidos:", bitsComRuido)

    if bits == bitsComRuido:
        print("Transmissao 32-QAM realizada com sucesso!")
    else:
        print("Houve erro na transmissao!")


if __name__ == "__main__":
    main()