
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
    bit_stuffing_RX
)
from CamadaEnlace.Enquadramento.ByteStuffing.ByteStuffing import (
    byte_stuffing_TX,
    byte_stuffing_RX
)
from CamadaEnlace.Enquadramento.Contagem.contagem import contagem_caracteres_TX, contagem_caracteres_RX
from CamadaEnlace.Enquadramento.Entrelacamento.Entrelacamento import entrelacamento_TX, entrelacamento_RX
from CamadaEnlace.DeteccaoErro.BitParidade.BitParidade import bit_paridade_TX, bit_paridade_RX
from CamadaEnlace.DeteccaoErro.Checksum.Checksum import checksum_TX, checksum_RX
from CamadaEnlace.DeteccaoErro.CRC.CRC import crc_TX, crc_RX
from CamadaEnlace.CorrecaoErro.Hamming.hamming import hamming_TX, hamming_RX


from MeioComunicacao.meio import adicionarRuido


# FUNCAO AUXILIAR PARA VISUALIZACAO DOS SINAIS BANDA-BASE
def resumirSinalBandaBase(
    sinal: list[float],
    modulacao: str,
    amostragem: int = 100,
    maxBits: int = 16
):

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
):

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
):

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
):

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

# ENLACE - ENQUADRAMENTO (TRANSMISSOR)
def enquadrarTX(
    bitsString: str,
    enquadramento: str,
    tam_max_quadro: int
):
    # Divide a carga util em quadros de acordo com o protocolo escolhido.
    # Sem enquadramento, a mensagem inteira e tratada como um unico quadro.
    if enquadramento == "Bit stuffing":
        return bit_stuffing_TX(bitsString, tam_max_quadro)

    elif enquadramento == "Byte stuffing":
        return byte_stuffing_TX(bitsString, tam_max_quadro)

    elif enquadramento == "Contagem":
        return contagem_caracteres_TX(bitsString, tam_max_quadro)

    elif enquadramento == "Entrelaçamento":
        return entrelacamento_TX(bitsString, tam_max_quadro)

    elif enquadramento == "Nenhum":
        return [bitsString]

    else:
        raise ValueError("Tipo de enquadramento desconhecido.")


# ENLACE - DESENQUADRAMENTO (RECEPTOR)
def desenquadrarRX(
    quadros: list[str | None],
    enquadramento: str
):
    # Remove o enquadramento e devolve (carga util, numeros dos quadros descartados).
    # Posicoes com None sao quadros que ja foram descartados pela deteccao de erros.
    validos = [quadro for quadro in quadros if quadro is not None]

    if not validos:
        return "", []

    if enquadramento == "Nenhum":
        return "".join(validos), []

    # No entrelacamento o bloco inteiro e conferido junto,
    # pois a ultima linha e a paridade de todas as outras
    if enquadramento == "Entrelaçamento":
        return entrelacamento_RX(validos), []

    funcoesRX = {
        "Bit stuffing": bit_stuffing_RX,
        "Byte stuffing": byte_stuffing_RX,
        "Contagem": contagem_caracteres_RX
    }

    if enquadramento not in funcoesRX:
        raise ValueError("Tipo de enquadramento desconhecido.")

    # Cada quadro e desenquadrado separadamente: um quadro corrompido
    # (flag ou contagem estragada pelo ruido) e descartado sem perder os outros
    cargaUtil = ""
    descartados = []

    for numero, quadro in enumerate(quadros, start=1):
        if quadro is None:
            continue
        try:
            dados = funcoesRX[enquadramento]([quadro])
            if len(dados) % 8 != 0:
                raise ValueError("Quadro sem numero inteiro de bytes.")
            cargaUtil += dados
        except ValueError:
            descartados.append(numero)

    return cargaUtil, descartados


# ENLACE - DETECCAO / CORRECAO DE ERROS (TRANSMISSOR)
def aplicarDeteccaoTX(
    quadros: list[str],
    deteccao: str
):
    # Anexa a cada quadro o codigo de deteccao (EDC) ou, no Hamming,
    # transforma o quadro em uma palavra de codigo com bits de paridade.
    if deteccao == "Bit de paridade":
        return bit_paridade_TX(quadros)

    elif deteccao == "Checksum":
        return checksum_TX(quadros)

    elif deteccao == "CRC-32":
        return crc_TX(quadros)

    elif deteccao == "Hamming":
        return [hamming_TX(quadro) for quadro in quadros]

    elif deteccao == "Nenhuma":
        return list(quadros)

    else:
        raise ValueError("Tipo de deteccao ou correcao desconhecido.")


# ENLACE - DETECCAO / CORRECAO DE ERROS (RECEPTOR)
def verificarDeteccaoRX(
    quadros: list[str],
    deteccao: str
):
    # Confere cada quadro recebido.
    # Quadro correto: o codigo e removido e o quadro segue para o desenquadramento.
    # Quadro com erro detectado: e descartado (vira None) e o descarte e sinalizado.
    # Hamming: corrige 1 bit por quadro e informa a posicao corrigida.
    # Retorna (quadros verificados, relatorio de cada quadro).
    if deteccao == "Nenhuma":
        return list(quadros), [f"Q{n}: sem verificacao" for n in range(1, len(quadros) + 1)]

    funcoesRX = {
        "Bit de paridade": bit_paridade_RX,
        "Checksum": checksum_RX,
        "CRC-32": crc_RX
    }

    if deteccao != "Hamming" and deteccao not in funcoesRX:
        raise ValueError("Tipo de deteccao ou correcao desconhecido.")

    verificados = []
    relatorio = []

    for numero, quadro in enumerate(quadros, start=1):
        try:
            if deteccao == "Hamming":
                dados, posicao = hamming_RX(quadro)

                if posicao == 0:
                    relatorio.append(f"Q{numero}: OK")
                else:
                    relatorio.append(
                        f"Q{numero}: bit {posicao} corrigido"
                    )
            else:
                dados = funcoesRX[deteccao]([quadro])[0]
                relatorio.append(f"Q{numero}: OK")

            verificados.append(dados)

        except ValueError:
            verificados.append(None)
            relatorio.append(f"Q{numero}: erro detectado, descartado")

    return verificados, relatorio


# FUNCAO PRINCIPAL DO SIMULADOR
def transmitirMensagem(
    mensagem: str,
    modulacao: str,
    portadora: str = "Nenhuma",
    media: float = 0.0,
    desvio_padrao: float = 0.0,
    detalhes: bool = False,
    enquadramento: str = "Nenhum",
    tam_max_quadro: int = 1,
    deteccao: str = "Nenhuma"
):

    amostragem = 100

    if not mensagem:
        raise ValueError("A mensagem nao pode estar vazia.")

    # APLICACAO - TRANSMISSOR
    bitsString = textoParaBits(mensagem)

    # ENLACE - TRANSMISSOR
    # 1) enquadramento  2) deteccao/correcao anexada a cada quadro
    quadrosEnquadrados = enquadrarTX(
        bitsString, enquadramento, tam_max_quadro
    )

    quadrosTX = aplicarDeteccaoTX(
        quadrosEnquadrados, deteccao
    )

    # CAMADA FISICA + CANAL AWGN
    # Cada quadro e transmitido separadamente, assim o receptor
    # sabe onde cada quadro comeca e termina
    quadrosRecebidos = []
    sinalTX = []
    sinalRX = []

    for quadro in quadrosTX:
        resultadoFisico = transmitirBits(
            stringParaLista(quadro),
            modulacao,
            portadora,
            media,
            desvio_padrao
        )

        quadrosRecebidos.append(
            listaParaString(resultadoFisico["bitsRecebidos"])
        )

        sinalTX += resultadoFisico["sinalTX"]
        sinalRX += resultadoFisico["sinalRX"]

    # ENLACE - RECEPTOR
    # 1) verifica/corrige cada quadro  2) desenquadramento
    quadrosVerificados, relatorio = verificarDeteccaoRX(
        quadrosRecebidos, deteccao
    )

    bitsRecebidosString, descartados = desenquadrarRX(
        quadrosVerificados, enquadramento
    )

    # Sinaliza os quadros descartados no desenquadramento
    for numero in descartados:
        relatorio[numero - 1] += ", quadro corrompido, descartado"

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
            "quadroRX": " | ".join(quadrosRecebidos),
            "verificacao": " | ".join(relatorio),
            "sinalTX": visualTX,
            "sinalRX": visualRX,
            "amostrasTX": sinalTX,
            "amostrasRX": sinalRX,
            "amostragem": amostragem
        }

    return mensagemRecebida
