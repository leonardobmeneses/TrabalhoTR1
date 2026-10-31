from MeioComunicacao.meio import adicionarRuido
from CamadaFisica.ModulacaoDigital.NRZPolar.NRZPolar import (codificarNRZPolar,decodificadorNRZPolar)
from CamadaFisica.ModulacaoDigital.NRZPolar.amostrador import amostradorSinal 
from visualizador import plotarNRZPolar
import random

sinal = [1.0, -1.0, 1.0, 1.0, -1.0]

    #Teste sem ruido
sinalSemruido = adicionarRuido(sinal, 0.0, 0.0)
print("Teste 1, canal teoricamente perfeito sem ruido")
print("Sinal transmitido eh: ", sinal)
print("sinal recebido foi: ", sinalSemruido)
if(sinal == sinalSemruido):
    print("O teste deu certo!")
else:
    print("O teste nao deu certo, corrija o codigo")

    #teste com ruido adicionado
random.seed(42)
sinalComRuido = adicionarRuido(sinal, 0.0, 0.1)
print("\nTeste 2, agora com ruido")
print("Sinal transmitido eh: ", sinal)
print("sinal recebido foi: ", sinalComRuido)
if(len(sinal) == len(sinalComRuido)):
    print("O teste deu certo!")
else:
    print("O teste nao deu certo, corrija o codigo")

    # Teste 3 - Ruído com média 0.5 e desvio zero
sinalTeste3 = adicionarRuido(sinal, 0.5, 0.0)
sinalEsperado = [1.5, -0.5, 1.5, 1.5, -0.5]
print("\nTeste 3, deslocamento constante")
print("Sinal recebido:", sinalTeste3)
if sinalTeste3 == sinalEsperado:
    print("O teste deu certo!")
else:
    print("O teste nao deu certo, corrija o codigo")

sinal = [1, 1, 1, -1, -1, -1, 1, 1, 1]

resultado = amostradorSinal(sinal, 3)

print("\nSinal original:", sinal)
print("Sinal amostrado:", resultado)    