def textoParaBits(texto : str):
    dados = texto.encode("ascii")       #transformo o texto em bits conforme a tabela ASCII
    bits = ""
    for byte in dados:
        bits += format(byte, "08b")     #tranformo cada caractere em byte ou 8 bits
    return bits

def bitsParaTexto(bits : str):
    if len(bits) % 8 != 0:
        raise ValueError("Devem ser enviados bytes.")    
    texto = ""
    for i in range(0, len(bits), 8):    #vamos separando as sequencias de bits de 8 em 8
        byte = bits[i : i+8]
        binario = int(byte, 2)
        texto += chr(binario)
    return texto    