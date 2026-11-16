from Simulador.simulador import transmitirMensagem


def main():
    dados = transmitirMensagem(
        "oi",
        "NRZPolar",
        desvio_padrao=0.1,
        detalhes=True
    )

    print("Sinal TX:", dados["sinalTX"])
    print("Sinal RX:", dados["sinalRX"])


if __name__ == "__main__":
    main()