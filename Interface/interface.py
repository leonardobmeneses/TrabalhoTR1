
import gi
from Simulador.simulador import transmitirMensagem

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def aoMudarPortadora(seletorPortadora, seletor, avisoPortadora):
    portadora = seletorPortadora.get_active_text()

    if portadora != "Nenhuma":
        # Mantem NRZ-Polar selecionado visualmente.
        # Atenção: o simulador atual ainda envia os bits
        # diretamente ao modulador por portadora.
        seletor.set_active(0)
        seletor.set_sensitive(False)

        avisoPortadora.set_text(
            "Portadora selecionada: NRZ-Polar fixado na interface. "
            "A integracao das duas etapas ainda esta pendente."
        )

    else:
        seletor.set_sensitive(True)
        avisoPortadora.set_text("")


def aoClicar(
    botao, entrada, seletor, seletorPortadora, controleRuido,
    resultado, textoTX, textoRX, bitsTX, bitsRX,
    sinalTX, sinalRX, descricaoSinal
):
    # Captura os valores escolhidos pelo usuario
    mensagem = entrada.get_text()
    modulacao = seletor.get_active_text()
    portadora = seletorPortadora.get_active_text()
    desvio_padrao = controleRuido.get_value()

    textoTX.set_text(mensagem)

    # Limpa os resultados anteriores
    textoRX.set_text("Aguardando recepcao...")
    bitsTX.set_text("")
    bitsRX.set_text("")
    sinalTX.set_text("")
    sinalRX.set_text("")
    resultado.set_text("Processando transmissao...")

    try:
        dados = transmitirMensagem(
            mensagem,
            modulacao,
            portadora,
            media=0.0,
            desvio_padrao=desvio_padrao,
            detalhes=True
        )

        # Aplicacao de rede
        textoTX.set_text(dados["textoTX"])
        textoRX.set_text(dados["textoRX"])

        bitsTX.set_text(dados["bitsTX"])
        bitsRX.set_text(dados["bitsRX"])

        # Identifica o tipo de sinal exibido
        if portadora == "Nenhuma":

            if modulacao == "Manchester":
                descricaoSinal.set_text(
                    "Banda-base: duas amostras representativas "
                    "por bit (V)"
                )

            else:
                descricaoSinal.set_text(
                    "Banda-base: uma amostra representativa "
                    "por bit (V)"
                )

        else:
            descricaoSinal.set_text(
                "Modulacao por portadora: primeiras "
                "10 amostras da onda (V)"
            )

        # Camada fisica
        sinalTX.set_text(dados["sinalTX"])
        sinalRX.set_text(dados["sinalRX"])

        # Resultado final
        resultado.set_text(
            "Mensagem recebida: " + dados["textoRX"]
        )

    except (ValueError, UnicodeError) as erro:
        textoRX.set_text("Falha na recepcao")
        bitsRX.set_text("Dados indisponiveis")

        sinalTX.set_text("Dados indisponiveis")
        sinalRX.set_text("Dados indisponiveis")

        descricaoSinal.set_text(
            "Nao foi possivel concluir a transmissao."
        )

        resultado.set_text("Erro: " + str(erro))


def iniciarInterface():
    # JANELA PRINCIPAL
    janela = Gtk.Window(title="Simulador TR1")
    janela.set_default_size(1500, 750)
    janela.connect("destroy", Gtk.main_quit)

    caixa = Gtk.Box(
        orientation=Gtk.Orientation.VERTICAL,
        spacing=10
    )

    caixa.set_border_width(15)
    janela.add(caixa)

    texto = Gtk.Label(
        label="Bem-vindo ao simulador de TR1!"
    )

    caixa.pack_start(texto, False, False, 0)

    # Entrada da mensagem
    entrada = Gtk.Entry()
    entrada.set_placeholder_text("Digite sua mensagem...")

    caixa.pack_start(entrada, False, False, 0)

    # CONFIGURACAO GERAL
    frameConfiguracoes = Gtk.Frame(
        label="Configuracao geral"
    )

    caixa.pack_start(
        frameConfiguracoes, False, False, 0
    )

    caixaConfiguracoes = Gtk.Box(
        orientation=Gtk.Orientation.VERTICAL,
        spacing=10
    )

    caixaConfiguracoes.set_border_width(10)
    frameConfiguracoes.add(caixaConfiguracoes)

    # Seletor da codificacao banda-base
    rotuloBandaBase = Gtk.Label(
        label="Codificacao banda-base:"
    )

    caixaConfiguracoes.pack_start(
        rotuloBandaBase, False, False, 0
    )

    seletor = Gtk.ComboBoxText()

    seletor.append_text("NRZPolar")
    seletor.append_text("Manchester")
    seletor.append_text("Bipolar")

    seletor.set_active(0)

    caixaConfiguracoes.pack_start(
        seletor, False, False, 0
    )

    # Seletor da modulacao por portadora
    rotuloPortadora = Gtk.Label(
        label="Modulacao por portadora (Nenhuma = so banda-base):"
    )

    caixaConfiguracoes.pack_start(
        rotuloPortadora, False, False, 0
    )

    seletorPortadora = Gtk.ComboBoxText()

    seletorPortadora.append_text("Nenhuma")
    seletorPortadora.append_text("ASK")
    seletorPortadora.append_text("FSK")
    seletorPortadora.append_text("8PSK")
    seletorPortadora.append_text("32-QAM")

    seletorPortadora.set_active(0)

    caixaConfiguracoes.pack_start(
        seletorPortadora, False, False, 0
    )

    # Aviso da configuracao da portadora
    avisoPortadora = Gtk.Label(label="")
    avisoPortadora.set_line_wrap(True)

    caixaConfiguracoes.pack_start(
        avisoPortadora, False, False, 0
    )

    # Controla o seletor de banda-base
    seletorPortadora.connect(
        "changed",
        aoMudarPortadora,
        seletor,
        avisoPortadora
    )

    # Configuracao do ruido AWGN
    rotuloRuido = Gtk.Label(
        label="Desvio padrao do ruido AWGN (V):"
    )

    caixaConfiguracoes.pack_start(
        rotuloRuido, False, False, 0
    )

    controleRuido = Gtk.SpinButton.new_with_range(
        0.0, 3.0, 0.1
    )

    controleRuido.set_value(0.1)

    caixaConfiguracoes.pack_start(
        controleRuido, False, False, 0
    )

    # APLICACAO DE REDE
    frameAplicacao = Gtk.Frame(
        label="Aplicacao de rede"
    )

    caixa.pack_start(
        frameAplicacao, False, False, 0
    )

    gridAplicacao = Gtk.Grid()

    gridAplicacao.set_column_spacing(20)
    gridAplicacao.set_row_spacing(10)
    gridAplicacao.set_border_width(10)
    gridAplicacao.set_column_homogeneous(True)
    gridAplicacao.set_hexpand(True)

    frameAplicacao.add(gridAplicacao)

    # Titulos
    tituloTX = Gtk.Label(label="Transmissor (TX)")
    tituloRX = Gtk.Label(label="Receptor (RX)")

    tituloTX.set_hexpand(True)
    tituloRX.set_hexpand(True)

    gridAplicacao.attach(tituloTX, 0, 0, 1, 1)
    gridAplicacao.attach(tituloRX, 1, 0, 1, 1)

    # Textos transmitido e recebido
    textoTX = Gtk.Label(
        label="Aguardando transmissao..."
    )

    textoRX = Gtk.Label(
        label="Aguardando recepcao..."
    )

    textoTX.set_line_wrap(True)
    textoRX.set_line_wrap(True)

    textoTX.set_selectable(True)
    textoRX.set_selectable(True)

    gridAplicacao.attach(textoTX, 0, 1, 1, 1)
    gridAplicacao.attach(textoRX, 1, 1, 1, 1)

    # Bits ASCII
    bitsTX = Gtk.Label(
        label="Aguardando bits TX..."
    )

    bitsRX = Gtk.Label(
        label="Aguardando bits RX..."
    )

    bitsTX.set_line_wrap(True)
    bitsRX.set_line_wrap(True)

    bitsTX.set_max_width_chars(55)
    bitsRX.set_max_width_chars(55)

    bitsTX.set_selectable(True)
    bitsRX.set_selectable(True)

    gridAplicacao.attach(bitsTX, 0, 2, 1, 1)
    gridAplicacao.attach(bitsRX, 1, 2, 1, 1)

    # CAMADA DE ENLACE
    frameEnlace = Gtk.Frame(
        label="Camada de Enlace"
    )

    caixa.pack_start(
        frameEnlace, False, False, 0
    )

    gridEnlace = Gtk.Grid()

    gridEnlace.set_column_spacing(20)
    gridEnlace.set_row_spacing(10)
    gridEnlace.set_border_width(10)
    gridEnlace.set_column_homogeneous(True)
    gridEnlace.set_hexpand(True)

    frameEnlace.add(gridEnlace)

    # Titulos
    tituloEnlaceTX = Gtk.Label(
        label="Transmissor (TX)"
    )

    tituloEnlaceRX = Gtk.Label(
        label="Receptor (RX)"
    )

    gridEnlace.attach(tituloEnlaceTX, 0, 0, 1, 1)
    gridEnlace.attach(tituloEnlaceRX, 1, 0, 1, 1)

    # Campos dos quadros
    quadroTX = Gtk.Label(
        label="Aguardando integracao do enlace..."
    )

    quadroRX = Gtk.Label(
        label="Aguardando integracao do enlace..."
    )

    quadroTX.set_line_wrap(True)
    quadroRX.set_line_wrap(True)

    quadroTX.set_max_width_chars(55)
    quadroRX.set_max_width_chars(55)

    quadroTX.set_selectable(True)
    quadroRX.set_selectable(True)

    gridEnlace.attach(quadroTX, 0, 1, 1, 1)
    gridEnlace.attach(quadroRX, 1, 1, 1, 1)

    # CAMADA FISICA
    frameFisica = Gtk.Frame(
        label="Camada Fisica"
    )

    caixa.pack_start(
        frameFisica, False, False, 0
    )

    gridFisica = Gtk.Grid()

    gridFisica.set_column_spacing(20)
    gridFisica.set_row_spacing(10)
    gridFisica.set_border_width(10)
    gridFisica.set_column_homogeneous(True)
    gridFisica.set_hexpand(True)

    frameFisica.add(gridFisica)

    # Titulos
    tituloFisicaTX = Gtk.Label(
        label="Transmissor (TX)"
    )

    tituloFisicaRX = Gtk.Label(
        label="Receptor (RX)"
    )

    gridFisica.attach(tituloFisicaTX, 0, 0, 1, 1)
    gridFisica.attach(tituloFisicaRX, 1, 0, 1, 1)

    # Explica os valores exibidos
    descricaoSinal = Gtk.Label(
        label="Aguardando dados da camada fisica..."
    )

    descricaoSinal.set_line_wrap(True)

    # Ocupa duas colunas na primeira linha
    gridFisica.attach(
        descricaoSinal, 0, 1, 2, 1
    )

    # Sinais eletricos
    sinalTX = Gtk.Label(
        label="Aguardando sinal TX..."
    )

    sinalRX = Gtk.Label(
        label="Aguardando sinal RX..."
    )

    sinalTX.set_line_wrap(True)
    sinalRX.set_line_wrap(True)

    sinalTX.set_max_width_chars(55)
    sinalRX.set_max_width_chars(55)

    sinalTX.set_selectable(True)
    sinalRX.set_selectable(True)

    gridFisica.attach(sinalTX, 0, 2, 1, 1)
    gridFisica.attach(sinalRX, 1, 2, 1, 1)


    # BOTAO E RESULTADO
    resultado = Gtk.Label(
        label="Aguardando mensagem..."
    )

    resultado.set_line_wrap(True)
    resultado.set_selectable(True)

    botao = Gtk.Button(label="Enviar")

    # Todos os componentes devem existir
    # antes de serem passados ao callback.
    botao.connect(
        "clicked",
        aoClicar,
        entrada,
        seletor,
        seletorPortadora,
        controleRuido,
        resultado,
        textoTX,
        textoRX,
        bitsTX,
        bitsRX,
        sinalTX,
        sinalRX,
        descricaoSinal
    )

    caixa.pack_start(botao, False, False, 0)
    caixa.pack_start(resultado, False, False, 0)

    # Exibe a interface
    janela.show_all()
    Gtk.main()

