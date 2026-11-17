from MeioComunicacao.meio import adicionarRuido
from CamadaFisica.ModulacaoDigital.NRZPolar.NRZPolar import (codificarNRZPolar,decodificadorNRZPolar)
from CamadaFisica.ModulacaoDigital.amostrador import amostradorSinal 
import random

#transmissor
bits = [1, 0, 1, 0, 0]
amplitude = 1.0
amostragem = 100
transmissor = codificarNRZPolar(bits, amplitude, amostragem)

#meioComunicacao
random.seed(40)
sinalRecebido = adicionarRuido(transmissor, 0.0, 0.9)

#receptor Amostrador
amostrasRecebidas = amostradorSinal(sinalRecebido)

#receptor Decodificador
bitsRecebidos = decodificadorNRZPolar(amostrasRecebidas)

#resultados
print("o sinal que quero transimitir tem bits: ", bits)
print("A quantidade de amostras enviadas foi: ", len(transmissor))
print("A quantidade de amostras recebidas foi: ", len(amostrasRecebidas))
print("Os bits que chegaram foi: ", bitsRecebidos)
