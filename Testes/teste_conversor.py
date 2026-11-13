from Simulador.conversor import (
    stringParaLista,
    listaParaString
)

def main():
    bitsOriginais = "101100101"

    lista = stringParaLista(bitsOriginais)

    bitsRecuperados = listaParaString(lista)

    print("String original:", bitsOriginais)
    print("Lista convertida:", lista)
    print("String recuperada:", bitsRecuperados)

    assert bitsOriginais == bitsRecuperados

    print("Teste passou!")


if __name__ == "__main__":
    main()