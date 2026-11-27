import queue
import threading

from MeioComunicacao.meio import Meio
from Simulador.simulador import executarTX, executarRX


class ChatSimulador:
    def __init__(self, aoTerminarTX, aoTerminarRX, aoErro):
        self.meio = Meio()
        self.filaTX = queue.Queue()      # interface -> thread TX
        self.aoTerminarTX = aoTerminarTX
        self.aoTerminarRX = aoTerminarRX
        self.aoErro = aoErro

    def iniciar(self):
        threading.Thread(target=self._threadTX, daemon=True).start()
        threading.Thread(target=self._threadRX, daemon=True).start()

    def enviar(self, mensagem, config):  # chamada pela interface; nao bloqueia
        self.filaTX.put((mensagem, config))

    def encerrar(self):
        self.filaTX.put(None)
        self.meio.encerrar()

    def _threadTX(self):
        while True:
            item = self.filaTX.get()
            if item is None:
                break
            mensagem, c = item
            try:
                dados = executarTX(mensagem, c["modulacao"], c["portadora"],
                                   c["enquadramento"], c["tam_max_quadro"], c["deteccao"])
                self.aoTerminarTX(dados)
                self.meio.transmitir({"config": c, "pacotes": dados["pacotes"]})
            except (ValueError, UnicodeError) as erro:
                self.aoErro("TX", erro)

    def _threadRX(self):
        while True:
            recebido = self.meio.receber()
            if recebido is None:
                break
            c = recebido["config"]
            try:
                dados = executarRX(recebido["pacotes"], c["modulacao"], c["portadora"],
                                   c["enquadramento"], c["deteccao"])
                self.aoTerminarRX(dados)
            except (ValueError, UnicodeError) as erro:
                self.aoErro("RX", erro)