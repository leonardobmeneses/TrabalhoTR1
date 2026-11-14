import gi
from Simulador.simulador import transmitirMensagem

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def aoClicar(botao, entrada, seletor, controleRuido, resultado):
    mensagem = entrada.get_text()
    modulacao = seletor.get_active_text()
    desvio_padrao = controleRuido.get_value()
    try:
        mensagemRecebida = transmitirMensagem(
            mensagem,
            modulacao,
            media=0.0,
            desvio_padrao=desvio_padrao
        )
        resultado.set_text(
            "Mensagem recebida: " + mensagemRecebida
        )
    except (ValueError, UnicodeError) as erro:
        resultado.set_text("Erro: " + str(erro))

def iniciarInterface():
    janela = Gtk.Window(title="Simulador TR1")
    janela.set_default_size(1500, 750)
    janela.connect("destroy", Gtk.main_quit)

    caixa = Gtk.Box(
        orientation=Gtk.Orientation.VERTICAL,
        spacing=10
    )

    caixa.set_border_width(15)
    janela.add(caixa)

    texto = Gtk.Label(label="Bem-vindo ao simulador de TR1!")
    caixa.pack_start(texto, False, False, 0)

    # Entrada da mensagem
    entrada = Gtk.Entry()
    entrada.set_placeholder_text("Digite sua mensagem...")
    caixa.pack_start(entrada, False, False, 0)

    # Selecao da codificacao
    seletor = Gtk.ComboBoxText()

    seletor.append_text("NRZPolar")
    seletor.append_text("Manchester")
    seletor.append_text("Bipolar")

    seletor.set_active(0)

    caixa.pack_start(seletor, False, False, 0)

    # Configuracao do ruido
    rotuloRuido = Gtk.Label(
        label="Desvio padrao do ruido AWGN (V):"
    )

    caixa.pack_start(rotuloRuido, False, False, 0)

    controleRuido = Gtk.SpinButton.new_with_range(
        0.0, 3.0, 0.1
    )

    controleRuido.set_value(0.1)

    # Adiciona o controle de ruido na janela
    caixa.pack_start(controleRuido, False, False, 0)

    # Area para mostrar a mensagem recebida
    resultado = Gtk.Label(label="Aguardando mensagem...")
    resultado.set_line_wrap(True)
    resultado.set_selectable(True)

    # Botao de envio
    botao = Gtk.Button(label="Enviar")

    botao.connect(
        "clicked",
        aoClicar,
        entrada,
        seletor,
        controleRuido,
        resultado
    )

    caixa.pack_start(botao, False, False, 0)
    caixa.pack_start(resultado, False, False, 0)

    janela.show_all()
    Gtk.main()