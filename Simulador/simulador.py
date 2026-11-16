from AplicacaoRede.Conversor import(textoParaBits, bitsParaTexto)
from Simulador.conversor import(stringParaLista, listaParaString)
from CamadaFisica.ModulacaoDigital.NRZPolar.NRZPolar import (codificarNRZPolar, decodificadorNRZPolar)
from CamadaFisica.ModulacaoDigital.Manchester.Manchester import(codificarManchester, decodificadorManchester)
from CamadaFisica.ModulacaoDigital.Bipolar.Bipolar import(codificarBipolar, decodificadorBipolar)
from CamadaFisica.ModulacaoDigital.amostrador import amostradorSinal
from MeioComunicacao.meio import adicionarRuido

def transmitirMensagem(
    mensagem: str,
    modulacao: str,
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

    if modulacao == "NRZPolar":
        sinal = codificarNRZPolar(bitsLista, amplitude, amostragem)

    elif modulacao == "Manchester":
        sinal = codificarManchester(bitsLista, amplitude, amostragem)

    elif modulacao == "Bipolar":
        sinal = codificarBipolar(bitsLista, amplitude, amostragem)

    else:
        raise ValueError("Codificacao Desconhecida")

    #Meio de comunicacao
    sinalRecebido = adicionarRuido(sinal, media, desvio_padrao)

    #receptor
    if modulacao == "NRZPolar":
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