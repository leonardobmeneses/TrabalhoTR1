
from AplicacaoRede.Conversor import (
    textoParaBits, bitsParaTexto
)
from Simulador.conversor import (
    stringParaLista, listaParaString
)

from CamadaFisica.ModulacaoDigital.NRZPolar.NRZPolar import (
    codificarNRZPolar, decodificadorNRZPolar
)
from CamadaFisica.ModulacaoDigital.Manchester.Manchester import (
    codificarManchester, decodificadorManchester
)
from CamadaFisica.ModulacaoDigital.Bipolar.Bipolar import (
    codificarBipolar, decodificadorBipolar
)
from CamadaFisica.ModulacaoDigital.amostrador import amostradorSinal

from CamadaFisica.ModulacaoPortadora.ASK.ASK import (
    modularASK, demodularASK
)
from CamadaFisica.ModulacaoPortadora.FSK.FSK import (
    modularFSK, demodularFSK
)
from CamadaFisica.ModulacaoPortadora.PSK8.PSK8 import (
    modular8PSK, demodular8PSK
)
from CamadaFisica.ModulacaoPortadora.QAM32.QAM32 import (
    modular32QAM, demodular32QAM
)
from CamadaEnlace.Enquadramento.BitStuffing.BitStuffing import (
    bit_stuffing_TX,
    bit_stuffing_RX,
    FLAG_BIT
)
from CamadaEnlace.Enquadramento.ByteStuffing.ByteStuffing import (
    byte_stuffing_TX,
    byte_stuffing_RX,
    FLAG_BYTE,
    ESC_BYTE
)
from CamadaEnlace.Enquadramento.Contagem.contagem import contagem_caracteres_TX, contagem_caracteres_RX
from CamadaEnlace.Enquadramento.Entrelacamento.Entrelacamento import entrelacamento_TX, entrelacamento_RX


from MeioComunicacao.meio import adicionarRuido


# FUNCAO AUXILIAR PARA VISUALIZACAO DOS SINAIS BANDA-BASE
def resumirSinalBandaBase(
    sinal: list[float],
    modulacao: str,
    amostragem: int = 100,
    maxBits: int = 16
) -> str:

    valores = []

    quantidadeBits = min(
        len(sinal) // amostragem,
        maxBits
    )

    for i in range(quantidadeBits):
        inicio = i * amostragem

        if modulacao == "Manchester":
            # Uma amostra representativa de cada metade
            primeira = sinal[inicio + amostragem // 4]
            segunda = sinal[inicio + 3 * amostragem // 4]

            valores.append(
                (round(primeira, 2), round(segunda, 2))
            )

        else:
            # Uma amostra representativa por bit
            valor = sinal[inicio + amostragem // 2]
            valores.append(round(valor, 2))

    return str(valores)

# MODULACAO POR PORTADORA - TRANSMISSOR
def modularPortadora(
    bits: list[int],
    portadora: str,
    amplitude: float,
    amostragem: int
) -> list[float]:

    if portadora == "ASK":
        return modularASK(
            bits,
            amplitude,
            amostragem=amostragem
        )

    elif portadora == "FSK":
        return modularFSK(
            bits,
            amplitude,
            amostragem=amostragem
        )

    elif portadora == "8PSK":
        return modular8PSK(
            bits,
            amplitude,
            amostragem=amostragem
        )

    elif portadora == "32-QAM":
        return modular32QAM(
            bits,
            amplitude,
            amostragem=amostragem
        )

    else:
        raise ValueError(
            "Modulacao por portadora desconhecida"
        )


# DEMODULACAO POR PORTADORA - RECEPTOR
def demodularPortadora(
    sinal: list[float],
    portadora: str,
    quantidade_bits: int,
    amplitude: float,
    amostragem: int
) -> list[int]:

    if portadora == "ASK":
        return demodularASK(
            sinal,
            amplitude,
            amostragem=amostragem
        )

    elif portadora == "FSK":
        return demodularFSK(
            sinal,
            amostragem=amostragem
        )

    elif portadora == "8PSK":
        return demodular8PSK(
            sinal,
            quantidade_bits,
            amostragem=amostragem
        )

    elif portadora == "32-QAM":
        return demodular32QAM(
            sinal,
            quantidade_bits,
            amplitude,
            amostragem=amostragem
        )

    else:
        raise ValueError(
            "Modulacao por portadora desconhecida"
        )

# CAMADA FISICA + MEIO DE COMUNICACAO
def transmitirBits(
    bits: list[int],
    modulacao: str,
    portadora: str = "Nenhuma",
    media: float = 0.0,
    desvio_padrao: float = 0.0
) -> dict:

    amplitude = 1.0
    amostragem = 100

    # Verifica se a entrada e uma lista valida de bits
    if (
        not isinstance(bits, list)
        or not bits
        or any(type(bit) is not int or bit not in (0, 1) for bit in bits)
    ):
        raise ValueError(
            "A entrada da camada fisica deve ser "
            "uma lista nao vazia de bits 0 e 1."
        )
    # CAMADA FISICA - TRANSMISSOR
    if portadora != "Nenhuma":
        sinal = modularPortadora(
            bits,
            portadora,
            amplitude,
            amostragem
        )

    elif modulacao == "NRZPolar":
        sinal = codificarNRZPolar(
            bits,
            amplitude,
            amostragem
        )
    elif modulacao == "Manchester":
        sinal = codificarManchester(
            bits,
            amplitude,
            amostragem
        )
    elif modulacao == "Bipolar":
        sinal = codificarBipolar(
            bits,
            amplitude,
            amostragem
        )

    else:
        raise ValueError("Codificacao desconhecida")
    
    # MEIO DE COMUNICACAO - CANAL AWGN
    sinalRecebido = adicionarRuido(
        sinal,
        media,
        desvio_padrao
    )

    # CAMADA FISICA - RECEPTOR
    if portadora != "Nenhuma":

        bitsRecebidos = demodularPortadora(
            sinalRecebido,
            portadora,
            len(bits),
            amplitude,
            amostragem
        )

    elif modulacao == "NRZPolar":

        amostras = amostradorSinal(
            sinalRecebido,
            amostragem
        )

        bitsRecebidos = decodificadorNRZPolar(
            amostras
        )

    elif modulacao == "Manchester":

        amostras = amostradorSinal(
            sinalRecebido,
            amostragem // 2
        )

        bitsRecebidos = decodificadorManchester(
            amostras
        )

    elif modulacao == "Bipolar":

        amostras = amostradorSinal(
            sinalRecebido,
            amostragem
        )

        bitsRecebidos = decodificadorBipolar(
            amostras,
            amplitude
        )

    # Retorna os bits recuperados e os sinais completos
    return {
        "bitsRecebidos": bitsRecebidos,
        "sinalTX": sinal,
        "sinalRX": sinalRecebido
    }


def separarQuadrosBitStuffing(fluxo: str) -> list[str]:
    # Identifica os quadros de um fluxo continuo usando as flags.
    if not fluxo.startswith(FLAG_BIT) or not fluxo.endswith(FLAG_BIT):
        raise ValueError("Fluxo recebido sem flags externas validas.")
    partes = fluxo.split(FLAG_BIT)
    quadros = [
        FLAG_BIT + dados + FLAG_BIT
        for dados in partes[1:-1]
        if dados
    ]
    if not quadros:
        raise ValueError("Nenhum quadro encontrado no fluxo recebido.")
    return quadros
# FUNCAO PRINCIPAL DO SIMULADOR


def separarQuadrosByteStuffing(fluxo: str) -> list[str]:
    """
    Recupera quadros de um fluxo continuo.
    Respeita o byte de escape para nao confundir dados com flags.
    """

    if not fluxo or len(fluxo) % 8 != 0:
        raise ValueError("Fluxo de bytes invalido.")

    quadros = []
    inicio = None
    escapado = False

    for pos in range(0, len(fluxo), 8):
        byte = fluxo[pos:pos + 8]

        if inicio is None:
            if byte != FLAG_BYTE:
                raise ValueError("Dados fora de quadro.")
            inicio = pos

        elif escapado:
            # O byte atual e dado, mesmo que seja uma flag
            escapado = False

        elif byte == ESC_BYTE:
            escapado = True

        elif byte == FLAG_BYTE:
            quadro = fluxo[inicio:pos + 8]

            if len(quadro) <= 16:
                raise ValueError("Quadro vazio ou invalido.")

            quadros.append(quadro)
            inicio = None

    if inicio is not None or escapado:
        raise ValueError("Quadro incompleto.")

    if not quadros:
        raise ValueError("Nenhum quadro encontrado.")

    return quadros


def separarQuadrosContagem(fluxo: str) -> list[str]:
    #Recupera quadros usando o primeiro byte como contagem
    #da quantidade de bytes da carga util.

    if not fluxo or len(fluxo) % 8 != 0:
        raise ValueError("Fluxo de bytes invalido.")

    quadros = []
    pos = 0

    while pos < len(fluxo):
        cabecalho = fluxo[pos:pos + 8]

        quantidade_bytes = int(cabecalho, 2)

        if quantidade_bytes == 0:
            raise ValueError("Contagem de caracteres invalida.")

        fim = pos + 8 + quantidade_bytes * 8

        if fim > len(fluxo):
            raise ValueError("Quadro incompleto.")

        quadros.append(fluxo[pos:fim])
        pos = fim

    return quadros


def transmitirMensagem(
    mensagem: str,
    modulacao: str,
    portadora: str = "Nenhuma",
    media: float = 0.0,
    desvio_padrao: float = 0.0,
    detalhes: bool = False,
    enquadramento: str = "Nenhum",
    tam_max_quadro: int = 1
) -> str | dict[str, str]:

    amostragem = 100

    if not mensagem:
        raise ValueError("A mensagem nao pode estar vazia.")
   
    # APLICACAO - TRANSMISSOR
    bitsString = textoParaBits(mensagem)

   
    # ENLACE - TRANSMISSOR

    if enquadramento == "Bit stuffing":
        quadrosTX = bit_stuffing_TX(
            bitsString, tam_max_quadro
        )

    elif enquadramento == "Byte stuffing":
        quadrosTX = byte_stuffing_TX(
            bitsString, tam_max_quadro
        )

    elif enquadramento == "Contagem":
        quadrosTX = contagem_caracteres_TX(
            bitsString, tam_max_quadro
        )

    elif enquadramento == "Nenhum":
        quadrosTX = []

    else:
        raise ValueError("Tipo de enquadramento desconhecido.")

    if enquadramento == "Nenhum":
        fluxoTX = bitsString
    else:
        fluxoTX = "".join(quadrosTX)

    # CAMADA FISICA + CANAL AWGN
    resultadoFisico = transmitirBits(
        stringParaLista(fluxoTX),
        modulacao,
        portadora,
        media,
        desvio_padrao
    )

    fluxoRX = listaParaString(
        resultadoFisico["bitsRecebidos"]
    )

    sinalTX = resultadoFisico["sinalTX"]
    sinalRX = resultadoFisico["sinalRX"]

    # ENLACE - RECEPTOR
    if enquadramento == "Bit stuffing":
        quadrosRX = separarQuadrosBitStuffing(fluxoRX)
        bitsRecebidosString = bit_stuffing_RX(
            quadrosRX
        )

    elif enquadramento == "Byte stuffing":
        quadrosRX = separarQuadrosByteStuffing(fluxoRX)
        bitsRecebidosString = byte_stuffing_RX(
            quadrosRX
        )
    elif enquadramento == "Contagem":
        quadrosRX = separarQuadrosContagem(fluxoRX)
        bitsRecebidosString = contagem_caracteres_RX(
            quadrosRX
        )
    else:
        quadrosRX = []
        bitsRecebidosString = fluxoRX

    # APLICACAO - RECEPTOR
    mensagemRecebida = bitsParaTexto(
        bitsRecebidosString
    )

    # DETALHES PARA A INTERFACE
    if detalhes:

        if portadora == "Nenhuma":

            visualTX = resumirSinalBandaBase(
                sinalTX, modulacao, amostragem
            )

            visualRX = resumirSinalBandaBase(
                sinalRX, modulacao, amostragem
            )

        else:

            visualTX = str([
                round(v, 2) for v in sinalTX[:10]
            ])

            visualRX = str([
                round(v, 2) for v in sinalRX[:10]
            ])

        return {
            "textoTX": mensagem,
            "bitsTX": bitsString,
            "textoRX": mensagemRecebida,
            "bitsRX": bitsRecebidosString,
            "quadroTX": " | ".join(quadrosTX),
            "quadroRX": " | ".join(quadrosRX),
            "sinalTX": visualTX,
            "sinalRX": visualRX
        }

    return mensagemRecebida