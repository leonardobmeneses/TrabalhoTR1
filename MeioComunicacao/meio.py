import random                       #biblioteca para usar a distribuicao gaussiana
import queue

def adicionarRuido(
    sinal: list[float],             #lista de sinais fisicos transmitidos em volts
    media: float,                
    desvioPadrao: float
):

    sinal_recebido = []         
    for valor in sinal:
        ruido = random.gauss(media, desvioPadrao)
        valor_recebido = valor + ruido
        sinal_recebido.append(valor_recebido)
    return sinal_recebido


class Meio:
    """Canal entre TX e RX: soma ruido ao sinal e entrega por uma fila."""
    def __init__(self):
        self.fila = queue.Queue()

    def transmitir(self, mensagem):
        cfg = mensagem["config"]
        pacotesRuidosos = [
            {"sinal": adicionarRuido(p["sinal"], cfg["media"], cfg["desvio_padrao"]),
             "nBits": p["nBits"]}
            for p in mensagem["pacotes"]
        ]
        self.fila.put({"config": cfg, "pacotes": pacotesRuidosos})

    def receber(self):
        return self.fila.get()      # bloqueia ate chegar algo

    def encerrar(self):
        self.fila.put(None)