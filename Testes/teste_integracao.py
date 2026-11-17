
from Simulador.simulador import transmitirMensagem

enquadramentos = [
    "Bit stuffing",
    "Byte stuffing",
    "Contagem"
]

tecnicas = [
    ("NRZPolar", "Nenhuma"),
    ("Manchester", "Nenhuma"),
    ("Bipolar", "Nenhuma"),
    ("NRZPolar", "ASK"),
    ("NRZPolar", "FSK"),
    ("NRZPolar", "8PSK"),
    ("NRZPolar", "32-QAM")
]

mensagens = [
    "oi",
    "TR1",
    "A~}B",
    "~~~~"
]

tamanhos = [1, 3]

aprovados = 0
total = 0

for enquadramento in enquadramentos:
    for modulacao, portadora in tecnicas:
        for mensagem in mensagens:
            for tamanho in tamanhos:

                total += 1

                try:
                    dados = transmitirMensagem(
                        mensagem,
                        modulacao,
                        portadora=portadora,
                        desvio_padrao=0.0,
                        detalhes=True,
                        enquadramento=enquadramento,
                        tam_max_quadro=tamanho
                    )

                    correto = (
                        dados["textoRX"] == mensagem
                        and dados["bitsTX"] == dados["bitsRX"]
                        and dados["quadroTX"] == dados["quadroRX"]
                    )

                    if correto:
                        aprovados += 1
                    else:
                        print(
                            f"[FALHA] {enquadramento} | "
                            f"{modulacao}/{portadora} | "
                            f"{mensagem} | tamanho={tamanho}"
                        )

                except Exception as erro:
                    print(
                        f"[ERRO] {enquadramento} | "
                        f"{modulacao}/{portadora} | "
                        f"{mensagem} | tamanho={tamanho}"
                    )
                    print(type(erro).__name__, erro)

    print(f"[FINALIZADO] {enquadramento}")

print("\n===== RESULTADO FINAL =====")
print(f"Testes executados: {total}")
print(f"Testes aprovados: {aprovados}")
print(f"Testes com falha: {total - aprovados}")
