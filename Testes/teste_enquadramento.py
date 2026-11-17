from CamadaEnlace.Enquadramento.BitStuffing.BitStuffing import bit_stuffing_TX, bit_stuffing_RX
from CamadaEnlace.Enquadramento.ByteStuffing.ByteStuffing import byte_stuffing_TX, byte_stuffing_RX
from CamadaEnlace.Enquadramento.Contagem.contagem import contagem_caracteres_TX, contagem_caracteres_RX
from CamadaEnlace.Enquadramento.Entrelacamento.Entrelacamento import entrelacamento_TX, entrelacamento_RX


# Casos de teste: nome, bits de entrada, tamanho maximo em bytes
casos = [
    ("Mensagem oi", "0110111101101001", 2),
    ("Byte de flag", "01111110", 1),
    ("Flag e escape", "0111111001111101", 2),
    ("Ultima parte incompleta", "011011110110100101111110", 2),
]

metodos = [
    ("Bit stuffing", bit_stuffing_TX, bit_stuffing_RX),
    ("Byte stuffing", byte_stuffing_TX, byte_stuffing_RX),
    ("Contagem", contagem_caracteres_TX, contagem_caracteres_RX),
    ("Entrelacamento", entrelacamento_TX, entrelacamento_RX),
]


def executar_teste(nome, tx, rx, bits, tamanho):
    try:
        quadros = tx(bits, tamanho)

        # Copia a lista porque alguns receptores podem modifica-la
        recuperado = rx(quadros.copy())

        if recuperado == bits:
            print(f"[OK] {nome}")
        else:
            print(f"[FALHA] {nome}")
            print(f"  Esperado:  {bits}")
            print(f"  Recebido: {recuperado}")

    except Exception as erro:
        print(f"[ERRO] {nome}")
        print(f"  {type(erro).__name__}: {erro}")


for nome_metodo, tx, rx in metodos:
    print(f"\n===== {nome_metodo} =====")

    for nome_caso, bits, tamanho in casos:
        executar_teste(
            nome_caso,
            tx,
            rx,
            bits,
            tamanho
        )


import random

gerador = random.Random(42)

tamanhos_mensagem = [
    1, 2, 3, 5, 8, 9, 16, 17,
    31, 32, 33, 64, 255, 256
]

tamanhos_quadro = [1, 2, 4, 8]

total = 0
sucessos = 0

print("\n===== TESTES ESTENDIDOS =====")

for nome_metodo, tx, rx in metodos:

    print(f"\nTestando {nome_metodo}...")

    for qtd_bytes in tamanhos_mensagem:

        # Cada byte possui 8 bits
        qtd_bits = qtd_bytes * 8

        # Gera uma sequencia aleatoria de zeros e uns
        bits = "".join(
            gerador.choice("01")
            for _ in range(qtd_bits)
        )

        for tamanho in tamanhos_quadro:

            total += 1

            try:
                quadros = tx(bits, tamanho)

                recuperados = rx(quadros.copy())

                if recuperados == bits:
                    sucessos += 1
                else:
                    print(
                        f"[FALHA] {nome_metodo} | "
                        f"Mensagem: {qtd_bytes} bytes | "
                        f"Quadro: {tamanho} bytes"
                    )

            except Exception as erro:
                print(
                    f"[ERRO] {nome_metodo} | "
                    f"Mensagem: {qtd_bytes} bytes | "
                    f"Quadro: {tamanho} bytes"
                )

                print(
                    f"  {type(erro).__name__}: {erro}"
                )

print("\n===== RESULTADO FINAL =====")
print(f"Testes executados: {total}")
print(f"Testes aprovados: {sucessos}")
print(f"Testes com falha: {total - sucessos}")

bits = "0110111101101001"

quadros = entrelacamento_TX(bits, 2)

# Cria uma copia para simular um erro na transmissao
quadros_corrompidos = quadros.copy()

# Inverte o primeiro bit da primeira linha
primeiro_bit = "1" if quadros_corrompidos[0][0] == "0" else "0"

quadros_corrompidos[0] = (
    primeiro_bit + quadros_corrompidos[0][1:]
)

try:
    recuperado = entrelacamento_RX(quadros_corrompidos)
    print("Erro nao detectado!")
except ValueError as erro:
    print("Erro detectado corretamente:", erro)


from Simulador.simulador import transmitirBits
from Simulador.conversor import stringParaLista, listaParaString

print("\n===== INTEGRACAO ENLACE + FISICA =====")

# Mensagem "oi" em ASCII
bits_originais = "0110111101101001"

# Primeiro: enquadramento
# Limite de 1 byte de carga util por quadro
quadros_TX = bit_stuffing_TX(bits_originais, 1)

quadros_RX = []

# Transmite cada quadro pela camada fisica
for quadro in quadros_TX:

    bits_quadro = stringParaLista(quadro)

    resultado = transmitirBits(
        bits_quadro,
        "NRZPolar",
        desvio_padrao=0.0
    )

    quadro_recebido = listaParaString(
        resultado["bitsRecebidos"]
    )

    quadros_RX.append(quadro_recebido)

# Desenquadramento
bits_recuperados = bit_stuffing_RX(quadros_RX)

print("Quadros TX:", quadros_TX)
print("Quadros RX:", quadros_RX)

print("Bits originais:  ", bits_originais)
print("Bits recuperados:", bits_recuperados)

assert bits_recuperados == bits_originais

print("[OK] Integracao enlace + fisica!")


print("\n===== INTEGRACAO COM FLUXO CONTINUO =====")

FLAG = "01111110"

# Mensagem "oi"
bits_originais = "0110111101101001"

# 1. Camada de Enlace TX
quadros_TX = bit_stuffing_TX(bits_originais, 1)

# Junta todos os quadros em uma unica sequencia
fluxo_TX = "".join(quadros_TX)

print("Fluxo TX:", fluxo_TX)

# 2. Camada Fisica + Meio de Comunicacao
resultado = transmitirBits(
    stringParaLista(fluxo_TX),
    "NRZPolar",
    desvio_padrao=0.0
)

fluxo_RX = listaParaString(
    resultado["bitsRecebidos"]
)

print("Fluxo RX:", fluxo_RX)

# 3. Camada de Enlace RX
# Identifica as flags no fluxo recebido
if not fluxo_RX.startswith(FLAG) or not fluxo_RX.endswith(FLAG):
    raise ValueError("Fluxo recebido sem flags externas validas.")

partes = fluxo_RX.split(FLAG)

# Reconstroi os quadros a partir dos delimitadores
quadros_RX = [
    FLAG + dados + FLAG
    for dados in partes[1:-1]
    if dados
]

if not quadros_RX:
    raise ValueError("Nenhum quadro encontrado.")

# 4. Desenquadramento
bits_recuperados = bit_stuffing_RX(quadros_RX)

print("Quadros recuperados:", quadros_RX)
print("Bits originais:   ", bits_originais)
print("Bits recuperados: ", bits_recuperados)

assert fluxo_RX == fluxo_TX
assert bits_recuperados == bits_originais

print("[OK] Transmissao continua com Bit Stuffing!")
