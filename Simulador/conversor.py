def stringParaLista(bits: str):
    lista = []                          
    for bit in bits:
        if bit != '0' and bit != '1':
            raise ValueError("A string deve conter apenas 0 ou 1.")
        lista.append(int(bit))
    return lista

def listaParaString(bits: list[int]):
    for bit in bits:
        if bit != 0 and bit != 1:
            raise ValueError("A lista deve conter apenas 0 ou 1.")
    return ''.join(str(bit) for bit in bits)