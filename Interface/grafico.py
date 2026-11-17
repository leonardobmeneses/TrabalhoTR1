from matplotlib.figure import Figure
from matplotlib.collections import LineCollection


def criarGrafico():
    """Cria o componente GTK e os dois eixos que serao atualizados a cada envio."""
    from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg

    figura = Figure(figsize=(10, 4), tight_layout=True)
    eixos = figura.subplots(2, 1, sharex=True, sharey=True)
    canvas = FigureCanvasGTK3Agg(figura)
    canvas.set_size_request(-1, 360)
    canvas.set_hexpand(True)

    grafico = (canvas, eixos)
    limparGrafico(grafico)
    return grafico


def limparGrafico(grafico):
    """Apaga o envio anterior, inclusive quando a nova transmissao falha."""
    canvas, eixos = grafico

    for eixo, titulo in zip(eixos, ["Transmitido — TX", "Recebido — RX"]):
        eixo.clear()
        eixo.set_title(titulo)
        eixo.set_ylabel("Tensão (V)")
        eixo.grid(True, alpha=0.3)

    eixos[1].set_xlabel("Índice da amostra")
    canvas.draw_idle()


def atualizarGrafico(
    grafico,
    sinalTX: list[float],
    sinalRX: list[float],
    amostragem: int,
    portadora: str,
):
    """Mostra todas as amostras da transmissao, sem limitar bits ou simbolos."""
    limparGrafico(grafico)
    canvas, eixos = grafico

    for eixo, sinal, cor in zip(eixos, [sinalTX, sinalRX], ["tab:blue", "tab:orange"]):
        indices = range(len(sinal))
        if portadora == "Nenhuma":
            eixo.step(indices, sinal, where="post", color=cor)
        else:
            eixo.plot(indices, sinal, color=cor)

        # Uma unica colecao marca os intervalos, mesmo em mensagens longas.
        marcadores = LineCollection(
            [((inicio, 0), (inicio, 1)) for inicio in range(0, len(sinal), amostragem)],
            transform=eixo.get_xaxis_transform(),
            colors="gray",
            linestyles="--",
            alpha=0.3,
        )
        eixo.add_collection(marcadores, autolim=False)

    unidade = "símbolo" if portadora in ("8PSK", "32-QAM") else "bit"
    eixos[0].set_title("Transmitido — TX (sinal completo)")
    eixos[1].set_title("Recebido — RX (sinal completo)")
    eixos[1].set_xlabel(
        f"Índice da amostra ({amostragem} amostras por {unidade})"
    )
    canvas.draw_idle()
