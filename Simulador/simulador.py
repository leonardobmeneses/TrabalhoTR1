
from AplicacaoRede.Conversor import (textoParaBits, bitsParaTexto)
from Simulador.conversor import (stringParaLista, listaParaString)

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

from MeioComunicacao.meio import adicionarRuido


# Funcao auxiliar para visualizar os sinais banda-base
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
            # Uma amostra representativa de cada metade do bit
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


# Seleciona o modulador por portadora
def modularPortadora(
    bits: list[int],
    portadora: str,
    amplitude: float,
    amostragem: int
) -> list[float]:

    if portadora == "ASK":
        return modularASK(
            bits, amplitude, amostragem=amostragem
        )

    elif portadora == "FSK":
        return modularFSK(
            bits, amplitude, amostragem=amostragem
        )

    elif portadora == "8PSK":
        return modular8PSK(
            bits, amplitude, amostragem=amostragem
        )

    elif portadora == "32-QAM":
        return modular32QAM(
            bits, amplitude, amostragem=amostragem
        )

    else:
        raise ValueError("Modulacao por portadora desconhecida")


# Seleciona o demodulador por portadora
def demodularPortadora(
    sinal: list[float],
    portadora: str,
    quantidade_bits: int,
    amplitude: float,
    amostragem: int
) -> list[int]:

    if portadora == "ASK":
        return demodularASK(
            sinal, amplitude, amostragem=amostragem
        )

    elif portadora == "FSK":
        return demodularFSK(
            sinal, amostragem=amostragem
        )

    elif portadora == "8PSK":
        return demodular8PSK(
            sinal, quantidade_bits, amostragem=amostragem
        )

    elif portadora == "32-QAM":
        return demodular32QAM(
            sinal, quantidade_bits, amplitude,
            amostragem=amostragem
        )

    else:
        raise ValueError("Modulacao por portadora desconhecida")


# Funcao principal do simulador
def transmitirMensagem(
    mensagem: str,
    modulacao: str,
    portadora: str = "Nenhuma",
    media: float = 0.0,
    desvio_padrao: float = 0.0,
    detalhes: bool = False
) -> str | dict[str, str]:

    amplitude = 1.0
    amostragem = 100

    if not mensagem:
        raise ValueError("A mensagem nao pode estar vazia.")

    # Aplicacao de rede - transmissor
    bitsString = textoParaBits(mensagem)

    # Converte string de bits para lista de inteiros
    bitsLista = stringParaLista(bitsString)

    # Camada fisica - transmissor
    if portadora != "Nenhuma":

        sinal = modularPortadora(
            bitsLista, portadora, amplitude, amostragem
        )

    elif modulacao == "NRZPolar":

        sinal = codificarNRZPolar(
            bitsLista, amplitude, amostragem
        )

    elif modulacao == "Manchester":

        sinal = codificarManchester(
            bitsLista, amplitude, amostragem
        )

    elif modulacao == "Bipolar":

        sinal = codificarBipolar(
            bitsLista, amplitude, amostragem
        )

    else:
        raise ValueError("Codificacao desconhecida")

    # Meio de comunicacao - adiciona ruido AWGN
    sinalRecebido = adicionarRuido(
        sinal, media, desvio_padrao
    )

    # Camada fisica - receptor
    if portadora != "Nenhuma":

        bitsRecebidos = demodularPortadora(
            sinalRecebido,
            portadora,
            len(bitsLista),
            amplitude,
            amostragem
        )

    elif modulacao == "NRZPolar":

        amostras = amostradorSinal(
            sinalRecebido, amostragem
        )

        bitsRecebidos = decodificadorNRZPolar(amostras)

    elif modulacao == "Manchester":

        amostras = amostradorSinal(
            sinalRecebido, amostragem // 2
        )

        bitsRecebidos = decodificadorManchester(amostras)

    elif modulacao == "Bipolar":

        amostras = amostradorSinal(
            sinalRecebido, amostragem
        )

        bitsRecebidos = decodificadorBipolar(
            amostras, amplitude
        )

    # Converte a lista recebida para string de bits
    bitsRecebidosString = listaParaString(bitsRecebidos)

    # Aplicacao de rede - receptor
    mensagemRecebida = bitsParaTexto(bitsRecebidosString)

    # Retorna os detalhes para a interface GTK
    if detalhes:

        if portadora == "Nenhuma":
            # Exibe amostras representativas dos bits
            visualTX = resumirSinalBandaBase(
                sinal, modulacao, amostragem
            )

            visualRX = resumirSinalBandaBase(
                sinalRecebido, modulacao, amostragem
            )

        else:
            # dez amostras da onda por portadora
            visualTX = str([
                round(v, 2) for v in sinal[:10]
            ])

            visualRX = str([
                round(v, 2) for v in sinalRecebido[:10]
            ])

        return {
            "textoTX": mensagem,
            "bitsTX": bitsString,
            "textoRX": mensagemRecebida,
            "bitsRX": bitsRecebidosString,
            "sinalTX": visualTX,
            "sinalRX": visualRX
        }

    return mensagemRecebida
