from Simulador.simulador import transmitirMensagem


def main():
    mensagem = "TR1 e uma materia de redes"

    for modulacao in ["NRZPolar", "Manchester", "Bipolar"]:
        mensagemRecebida = transmitirMensagem(
            mensagem,
            modulacao,
            desvio_padrao=0.1
    )
        print("\nModulacao:", modulacao)
        print("Mensagem enviada:", mensagem)
        print("Mensagem recebida:", mensagemRecebida)
        print("Teste passou?", mensagem == mensagemRecebida)
if __name__ == "__main__":
    main()