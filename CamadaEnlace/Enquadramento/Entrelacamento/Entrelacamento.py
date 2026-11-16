TAM_BYTE = 8                    # 1 "caractere" = 1 byte = 8 bits
TAM_MAX_PADRAO = 8              # bytes de dados por quadro (padrão)
TAM_CABECALHO_CONTAGEM = 1      # byte de contagem (conta o próprio cabeçalho)
TAM_CABECALHO_ENTRELACADO = 32  # bits que guardam o tamanho original do payload

FLAG_BYTE = "01111110"          # 0x7E: delimitador do byte stuffing
ESC_BYTE = "01111101"           # 0x7D: byte de escape do byte stuffing
FLAG_BIT = "01111110"           # delimitador do bit stuffing (padrão HDLC)

def textoParaBits(texto : str) -> str:
    dados = texto.encode("ascii")       #transformo o texto em bits conforme a tabela ASCII
    bits = ""
    for byte in dados:
        bits += format(byte, "08b")     #tranformo cada caractere em byte ou 8 bits
    return bits

def bitsParaTexto(bits : str) -> str:
    if len(bits) % 8 != 0:
        raise ValueError("Devem ser enviados bytes.")    
    texto = ""
    for i in range(0, len(bits), 8):    #vamos separando as sequencias de bits de 8 em 8
        byte = bits[i : i+8]
        binario = int(byte, 2)
        texto += chr(binario)
    return texto

# Funções auxiliares
def inteiro_para_bits(valor, n_bits=TAM_BYTE):
    """Converte um inteiro em string de n_bits bits (MSB primeiro)."""
    if valor < 0 or valor >= 2 ** n_bits:
        raise ValueError("Valor não cabe em {} bits.".format(n_bits))
    return format(valor, "0{}b".format(n_bits))

def bits_para_inteiro(bits):
    """Converte uma string de bits (MSB primeiro) em inteiro."""
    return int(bits, 2) if bits else 0

# 2. Enquadramento: entrelaçamento de bits
def entrelacamento_TX(cargaUtil : str, tam_max_quadro : int) -> list[str]:
    """
    TX: o payload é dividido em N linhas de tam_max_quadro bytes;
    é calculado o bit de paridade para cada coluna
    e ocorre a transmissão.
    """
    
    if tam_max_quadro < 1:
        raise ValueError("tam_max_quadro deve ser pelo menos 1 byte.")

    tam_linha = tam_max_quadro * TAM_BYTE
    matriz = [cargaUtil[i:i + tam_linha] for i in range(0, len(cargaUtil), tam_linha)]

    paridade = ""

    for colunas in range(tam_linha):
        conta_uns = 0
        
        for linhas in range(len(matriz)):
            if(matriz[linhas][colunas]=="1"): conta_uns+=1

        paridade += str(conta_uns%2)

    matriz.append(paridade)

    return matriz


def entrelacamento_RX(fluxo : list[str]) -> str:
    """
    RX: desfaz o entrelaçamento (lê por colunas, reconstrói as linhas) e
    verifica a paridade de cada coluna.
    """
    if not fluxo: return ""

    paridade_recebida = fluxo.pop()     # Removendo a linha de paridade do fluxo recebido
    tam_linha = len(paridade_recebida)

    paridade_calculada = ""
    
    for colunas in range(0, tam_linha):
        conta_uns = 0
        
        for linhas in range(len(fluxo)):
            if not fluxo[linhas][colunas]: continue
            if(fluxo[linhas][colunas]=="1"): conta_uns+=1

        paridade_calculada += str(conta_uns%2)


    if not paridade_calculada == paridade_recebida:
        diff=0
        for i in range(0,tam_linha):
            if paridade_recebida[i] != paridade_calculada[i]: diff+=1
        raise ValueError(f"Erro detectado. Os bits de paridade divergem em {diff} colunas.")

    bits = ""
    for linhas in fluxo:
        bits+=linhas

    return bits


if __name__ == "__main__":
    text = input("insira entrada:\n")
    manda = textoParaBits(text)
    encaminha = entrelacamento_TX(manda, 2)
    print(f"Encaminhado = {encaminha}\n")
    print(f"Entrada em bits = '{manda}'")
    print(f"Linhas da encaminhada = {len(encaminha)}")
    print("\n")
    recebe = entrelacamento_RX(encaminha)
    print(f"saida em bits =   '{recebe}'")
    print(f"Mandou {text} e recebeu {bitsParaTexto(recebe)}")
