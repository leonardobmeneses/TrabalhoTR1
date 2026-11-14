from AplicacaoRede.Conversor import (textoParaBits, bitsParaTexto)

def main():
    mensagem = "oi"
    bits = textoParaBits(mensagem)
    mensagemRecebida = bitsParaTexto(bits)
    print("essa eh a mensagem:", mensagem)
    print("essa eh a mensagem em bits:", bits)
    print("essa eh a mensagem de bits de volta para o normal:",mensagemRecebida)
if __name__ == "__main__":
    main()