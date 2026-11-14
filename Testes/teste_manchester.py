from CamadaFisica.ModulacaoDigital.Manchester.Manchester import codificarManchester, decodificadorManchester
from CamadaFisica.ModulacaoDigital.amostrador import amostradorSinal
import random
from MeioComunicacao.meio import adicionarRuido
def main():
    bits = [0, 1, 0]
    amplitude = 1.0
    amostragem = 20

    sinal = codificarManchester(
        bits, amplitude, amostragem
    )

    print("Bits transmitidos:", bits)
    print("Sinal codificado:", sinal)
    print("Quantidade de amostras:", len(sinal))

    if len(sinal) == len(bits) * amostragem:
        print("Teste passou!")
    else:
        print("Teste falhou!")

# Amostrando o sinal
    amostras = amostradorSinal(sinal, amostragem // 2)

# Decodificando
    bitsRecebidos = decodificadorManchester(amostras)

    print("Amostras selecionadas:", amostras)
    print("Bits recebidos:", bitsRecebidos)

    if bits == bitsRecebidos:
        print("Decodificacao realizada com sucesso!")
    else:
        print("Erro na decodificacao!")

        # Teste do Manchester com ruido AWGN

    random.seed(42)

    sinalComRuido = adicionarRuido(
        sinal,
        media=0.0,
        desvioPadrao=0.1
    )

    amostrasComRuido = amostradorSinal(
        sinalComRuido,
        amostragem // 2
    )

    bitsComRuido = decodificadorManchester(amostrasComRuido)

    print("\nTeste Manchester com ruido")
    print("Bits transmitidos:", bits)
    print("Amostras transmitidas:", len(sinal))
    print("Amostras selecionadas:", amostrasComRuido)
    print("Bits recebidos:", bitsComRuido)

    if bits == bitsComRuido:
        print("Transmissao realizada com sucesso!")
    else:
        print("Houve erro na transmissao!")

if __name__ == "__main__":
    main()