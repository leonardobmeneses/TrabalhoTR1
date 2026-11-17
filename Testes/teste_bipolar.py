from CamadaFisica.ModulacaoDigital.Bipolar.Bipolar import (
    codificarBipolar,
    decodificadorBipolar
)

from CamadaFisica.ModulacaoDigital.amostrador import amostradorSinal
import random
from MeioComunicacao.meio import adicionarRuido


def main():
    bits = [1, 1, 0, 1, 0, 0, 1]

    amplitude = 1.0
    amostragem = 10

    # Codificador
    sinal = codificarBipolar(bits, amplitude, amostragem)

    # Amostrador
    amostras = amostradorSinal(sinal, amostragem)

    # Decodificador
    bitsRecebidos = decodificadorBipolar(
        amostras,
        amplitude=amplitude
    )

    print("Bits transmitidos:", bits)
    print("Sinal amostrado:", amostras)
    print("Bits recebidos:", bitsRecebidos)

    if bits == bitsRecebidos:
        print("Teste Bipolar passou!")
    else:
        print("Erro na decodificacao!")

    # Teste Bipolar com ruido AWGN
    random.seed(42)
    sinalRecebido = adicionarRuido(
        sinal,
        media=0.0,
        desvioPadrao=0.1
    )

    amostrasRecebidas = amostradorSinal(
        sinalRecebido,
        amostragem
    )

    bitsRecebidos = decodificadorBipolar(
        amostrasRecebidas,
        amplitude=amplitude
    )

    print("\nTeste Bipolar com ruido")
    print("Bits transmitidos:", bits)
    print("Amostras recebidas:", amostrasRecebidas)
    print("Bits recebidos:", bitsRecebidos)

    if bits == bitsRecebidos:
        print("Transmissao Bipolar realizada com sucesso!")
    else:
        print("Houve erro na transmissao!")
if __name__ == "__main__":
    main()