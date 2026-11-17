from CamadaEnlace.CorrecaoErro.Hamming.hamming import hamming_TX, hamming_RX


def inverterBit(bits: str, posicao: int) -> str:
    #inverte o bit da posicao informada (contando a partir de 1), simulando um erro do canal
    i = posicao - 1
    bitInvertido = "1" if bits[i] == "0" else "0"
    return bits[:i] + bitInvertido + bits[i + 1:]


def main():
    # Teste 1 - exemplo classico: 4 bits de dados viram 7 bits
    dados = "1011"
    codigo = hamming_TX(dados)

    print("Teste 1 - exemplo classico")
    print("Dados:", dados)
    print("Palavra de codigo:", codigo)

    if codigo == "0110011":
        print("Codificacao correta!")
    else:
        print("Erro na codificacao!")

    # Teste 2 - sem erro no canal
    dadosRecebidos, posicao = hamming_RX(codigo)

    print("\nTeste 2 - sem erro")
    print("Dados recebidos:", dadosRecebidos, "| posicao corrigida:", posicao)

    if dadosRecebidos == dados and posicao == 0:
        print("Teste sem erro passou!")
    else:
        print("Erro na decodificacao!")

    # Teste 3 - um bit errado na posicao 5
    codigoComErro = inverterBit(codigo, 5)
    dadosRecebidos, posicao = hamming_RX(codigoComErro)

    print("\nTeste 3 - erro na posicao 5")
    print("Palavra recebida:", codigoComErro)
    print("Dados recebidos:", dadosRecebidos, "| posicao corrigida:", posicao)

    if dadosRecebidos == dados and posicao == 5:
        print("Erro corrigido com sucesso!")
    else:
        print("A correcao falhou!")

    # Teste 4 - um byte de mensagem ('O' = 01001111) com erro em cada posicao possivel
    dados = "01001111"
    codigo = hamming_TX(dados)
    todosCorrigidos = True

    for posicao in range(1, len(codigo) + 1):
        dadosRecebidos, corrigida = hamming_RX(inverterBit(codigo, posicao))
        if dadosRecebidos != dados or corrigida != posicao:
            todosCorrigidos = False

    print("\nTeste 4 - 'O' com erro em cada uma das", len(codigo), "posicoes")
    print("Palavra de codigo:", codigo)

    if todosCorrigidos:
        print("Todos os erros de 1 bit foram corrigidos!")
    else:
        print("Algum erro nao foi corrigido!")


if __name__ == "__main__":
    main()