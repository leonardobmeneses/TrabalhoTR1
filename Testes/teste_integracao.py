from Simulador.simulador import transmitirMensagem

mensagens = [
    "oi",
    "TR1",
    "Teste de comunicacao"
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

for mensagem in mensagens:
    for modulacao, portadora in tecnicas:

        dados = transmitirMensagem(
            mensagem,
            modulacao,
            portadora=portadora,
            media=0.0,
            desvio_padrao=0.0,
            detalhes=True
        )

        correto = dados["bitsTX"] == dados["bitsRX"]

        tecnica = portadora if portadora != "Nenhuma" else modulacao

        if correto:
            print(f"[OK] {tecnica} - {mensagem}")
        else:
            print(f"[FALHA] {tecnica} - {mensagem}")