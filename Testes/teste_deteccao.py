from Simulador.simulador import (
    transmitirMensagem,
    enquadrarTX,
    aplicarDeteccaoTX,
    verificarDeteccaoRX
)

enquadramentos = [
    "Nenhum",
    "Bit stuffing",
    "Byte stuffing",
    "Contagem",
    "Entrelaçamento"
]

deteccoes = [
    "Nenhuma",
    "Bit de paridade",
    "Checksum",
    "CRC-32",
    "Hamming"
]


def inverterBit(bits: str, posicao: int) -> str:
    #inverte o bit da posicao informada (contando a partir de 1), simulando um erro do canal
    i = posicao - 1
    bitInvertido = "1" if bits[i] == "0" else "0"
    return bits[:i] + bitInvertido + bits[i + 1:]


def main():
    # Teste 1 - sem ruido, toda combinacao de enquadramento e deteccao entrega a mensagem
    total = 0
    aprovados = 0

    for enquadramento in enquadramentos:
        for deteccao in deteccoes:
            total += 1
            recebida = transmitirMensagem(
                "Ola mundo",
                "NRZPolar",
                desvio_padrao=0.0,
                enquadramento=enquadramento,
                tam_max_quadro=2,
                deteccao=deteccao
            )
            if recebida == "Ola mundo":
                aprovados += 1
            else:
                print("Falhou:", enquadramento, deteccao, recebida)

    print("Teste 1 - sem ruido")
    print("Combinacoes aprovadas:", aprovados, "de", total)

    # Teste 2 - um bit errado no primeiro quadro
    # deteccao: o quadro deve ser descartado | Hamming: o bit deve ser corrigido
    print("\nTeste 2 - erro de 1 bit no primeiro quadro")
    tudoCerto = True

    for enquadramento in enquadramentos:
        quadros = enquadrarTX("0100111101101100", enquadramento, 1)

        for deteccao in deteccoes[1:]:
            quadrosTX = aplicarDeteccaoTX(quadros, deteccao)
            quadrosTX[0] = inverterBit(quadrosTX[0], 3)

            _, relatorio = verificarDeteccaoRX(quadrosTX, deteccao)

            if deteccao == "Hamming":
                esperado = "bit 3 corrigido"
            else:
                esperado = "erro detectado"

            if esperado not in relatorio[0]:
                tudoCerto = False
                print("Falhou:", enquadramento, deteccao, relatorio[0])

    if tudoCerto:
        print("Erros detectados e corrigidos em todas as combinacoes!")
    else:
        print("Alguma combinacao nao detectou ou corrigiu o erro!")


if __name__ == "__main__":
    main()
