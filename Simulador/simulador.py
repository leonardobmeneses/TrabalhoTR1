from AplicacaoRede.Conversor import(textoParaBits, bitsParaTexto)
from Simulador.conversor import(stringParaLista, listaParaString)
from CamadaFisica.ModulacaoDigital.NRZPolar.NRZPolar import (codificarNRZPolar, decodificadorNRZPolar)
from CamadaFisica.ModulacaoDigital.Manchester.Manchester import(codificarManchester, decodificadorManchester)
from CamadaFisica.ModulacaoDigital.Bipolar.Bipolar import(codificarBipolar, decodificadorBipolar)
from CamadaFisica.ModulacaoDigital.amostrador import amostradorSinal
from CamadaFisica.ModulacaoPortadora.ASK.ASK import (modularASK, demodularASK)
from CamadaFisica.ModulacaoPortadora.FSK.FSK import (modularFSK, demodularFSK)
from CamadaFisica.ModulacaoPortadora.PSK8.PSK8 import (modular8PSK, demodular8PSK)
from CamadaFisica.ModulacaoPortadora.QAM32.QAM32 import (modular32QAM, demodular32QAM)
from MeioComunicacao.meio import adicionarRuido


def modularPortadora(
    bits: list[int],
    portadora: str,
    amplitude: float,
    amostragem: int
) -> list[float]:
    #escolhe o modulador por portadora de acordo com o que foi selecionado na interface
    if portadora == "ASK":
        return modularASK(bits, amplitude, amostragem=amostragem)
    elif portadora == "FSK":
        return modularFSK(bits, amplitude, amostragem=amostragem)
    elif portadora == "8PSK":
        return modular8PSK(bits, amplitude, amostragem=amostragem)
    elif portadora == "32-QAM":
        return modular32QAM(bits, amplitude, amostragem=amostragem)
    else:
        raise ValueError("Modulacao por portadora desconhecida")


def demodularPortadora(
    sinal: list[float],
    portadora: str,
    quantidade_bits: int,
    amplitude: float,
    amostragem: int
) -> list[int]:
    #escolhe o demodulador por portadora correspondente ao modulador usado no transmissor
    if portadora == "ASK":
        return demodularASK(sinal, amplitude, amostragem=amostragem)
    elif portadora == "FSK":
        return demodularFSK(sinal, amostragem=amostragem)
    elif portadora == "8PSK":
        return demodular8PSK(sinal, quantidade_bits, amostragem=amostragem)
    elif portadora == "32-QAM":
        return demodular32QAM(sinal, quantidade_bits, amplitude, amostragem=amostragem)
    else:
        raise ValueError("Modulacao por portadora desconhecida")


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

    #Aplicacao de rede - transmissor
    bitsString = textoParaBits(mensagem)

    #Conversao para lista de inteiros
    bitsLista = stringParaLista(bitsString)

    #Camada fisica - transmissor
    if portadora != "Nenhuma":
        #modulacao por portadora: os bits viram uma onda senoidal
        sinal = modularPortadora(bitsLista, portadora, amplitude, amostragem)

    elif modulacao == "NRZPolar":
        sinal = codificarNRZPolar(bitsLista, amplitude, amostragem)

    elif modulacao == "Manchester":
        sinal = codificarManchester(bitsLista, amplitude, amostragem)

    elif modulacao == "Bipolar":
        sinal = codificarBipolar(bitsLista, amplitude, amostragem)

    else:
        raise ValueError("Codificacao Desconhecida")

    #Meio de comunicacao
    sinalRecebido = adicionarRuido(sinal, media, desvio_padrao)

    #Camada fisica - receptor
    if portadora != "Nenhuma":
        bitsRecebidos = demodularPortadora(
            sinalRecebido, portadora, len(bitsLista), amplitude, amostragem
        )

    elif modulacao == "NRZPolar":
        amostras = amostradorSinal(sinalRecebido, amostragem)
        bitsRecebidos = decodificadorNRZPolar(amostras)

    elif modulacao == "Manchester":
        amostras = amostradorSinal(sinalRecebido, amostragem // 2)
        bitsRecebidos = decodificadorManchester(amostras)

    elif modulacao == "Bipolar":
        amostras = amostradorSinal(sinalRecebido, amostragem)
        bitsRecebidos = decodificadorBipolar(amostras, amplitude)

    #Conversao para string de bits
    bitsRecebidosString = listaParaString(bitsRecebidos)

    #Aplicacao de rede - receptor
    mensagemRecebida = bitsParaTexto(bitsRecebidosString)

    if detalhes:
        return {
            "textoTX": mensagem,
            "bitsTX": bitsString,
            "textoRX": mensagemRecebida,
            "bitsRX": bitsRecebidosString,
            "sinalTX": str([round(v, 2) for v in sinal[:10]]),
            "sinalRX": str([round(v, 2) for v in sinalRecebido[:10]])
        }

    return mensagemRecebida