import matplotlib.pyplot as plt


def plotarNRZPolar(
    bits: list[int],
    sinalTransmitido: list[float],
    sinalRecebido: list[float],
    amostragemPorBit: int
):

    # Criando os gráficos
    figura, (grafico1, grafico2) = plt.subplots(
        2, 1, figsize=(12, 7), sharex=True
    )

    # Eixo horizontal: indice das amostras
    tempo = list(range(len(sinalTransmitido)))

    # Gráfico do sinal transmitido
    grafico1.plot(tempo, sinalTransmitido)
    grafico1.set_title("NRZ-Polar - Sinal Transmitido")
    grafico1.set_ylabel("Tensao (V)")
    grafico1.grid(True)

    # Gráfico do sinal recebido
    grafico2.plot(tempo, sinalRecebido)
    grafico2.set_title("NRZ-Polar - Sinal Recebido com AWGN")
    grafico2.set_ylabel("Tensao (V)")
    grafico2.set_xlabel("Indice da amostra")
    grafico2.grid(True)

    # Marcando os centros dos intervalos de bit
    for i in range(len(bits)):
        centro = i * amostragemPorBit + amostragemPorBit // 2

        grafico2.scatter(
            centro,
            sinalRecebido[centro],
            color="red"
        )

    plt.tight_layout()
    plt.show()