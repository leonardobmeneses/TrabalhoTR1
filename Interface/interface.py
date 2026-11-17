
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from Simulador.simulador import transmitirMensagem
from Interface.grafico import criarGrafico, limparGrafico, atualizarGrafico

# FUNCOES AUXILIARES DA INTERFACE
def criarRotulo(texto, largura=55):
    """
    Cria um rotulo que permite selecionar e copiar
    os valores exibidos.
    """
    rotulo = Gtk.Label(label=texto)

    rotulo.set_line_wrap(True)
    rotulo.set_max_width_chars(largura)
    rotulo.set_selectable(True)
    rotulo.set_xalign(0.0)
    rotulo.set_hexpand(True)

    return rotulo


def criarGridTXRX():
    """
    Cria uma grade com duas colunas:
    transmissor e receptor.
    """
    grid = Gtk.Grid()

    grid.set_column_spacing(20)
    grid.set_row_spacing(10)
    grid.set_border_width(10)
    grid.set_column_homogeneous(True)
    grid.set_hexpand(True)

    tituloTX = Gtk.Label(label="Transmissor (TX)")
    tituloRX = Gtk.Label(label="Receptor (RX)")

    grid.attach(tituloTX, 0, 0, 1, 1)
    grid.attach(tituloRX, 1, 0, 1, 1)

    return grid

# ALTERACAO DA MODULACAO POR PORTADORA
def aoMudarPortadora(
    seletorPortadora,
    seletor,
    avisoPortadora
):
    portadora = seletorPortadora.get_active_text()

    if portadora != "Nenhuma":

        # Mantem NRZ-Polar selecionado
        seletor.set_active(0)
        seletor.set_sensitive(False)

        # A integracao efetiva entre NRZ e portadora
        # ainda sera implementada no simulador.
        avisoPortadora.set_text(
            "Com portadora, NRZ-Polar fica selecionado. "
            "A integracao das duas etapas ainda esta pendente."
        )

    else:

        # Libera a escolha entre as tres codificacoes
        seletor.set_sensitive(True)
        avisoPortadora.set_text("")


# EVENTO DO BOTAO ENVIAR
def aoClicar(
    botao,
    entrada,
    seletor,
    seletorPortadora,
    seletorEnquadramento,
    controleQuadro,
    seletorDeteccao,
    controleMedia,
    controleRuido,
    resultado,
    textoTX,
    textoRX,
    bitsTX,
    bitsRX,
    quadroTX,
    quadroRX,
    verificacao,
    sinalTX,
    sinalRX,
    descricaoSinal,
    grafico
):

    # Recupera as configuracoes selecionadas
    mensagem = entrada.get_text()

    modulacao = seletor.get_active_text()
    portadora = seletorPortadora.get_active_text()

    enquadramento = seletorEnquadramento.get_active_text()
    tam_max_quadro = controleQuadro.get_value_as_int()

    deteccao = seletorDeteccao.get_active_text()

    media = controleMedia.get_value()
    desvio_padrao = controleRuido.get_value()

    # Limpa os resultados anteriores
    textoTX.set_text(mensagem)
    textoRX.set_text("Aguardando recepcao...")

    bitsTX.set_text("")
    bitsRX.set_text("")

    quadroTX.set_text("")
    quadroRX.set_text("")
    verificacao.set_text("")

    sinalTX.set_text("")
    sinalRX.set_text("")

    descricaoSinal.set_text("")
    resultado.set_text("Processando transmissao...")
    limparGrafico(grafico)

    try:

        # Executa o simulador completo
        dados = transmitirMensagem(
            mensagem,
            modulacao,
            portadora,
            media=media,
            desvio_padrao=desvio_padrao,
            detalhes=True,
            enquadramento=enquadramento,
            tam_max_quadro=tam_max_quadro,
            deteccao=deteccao
        )

        # APLICACAO DE REDE
        textoTX.set_text(dados["textoTX"])
        textoRX.set_text(dados["textoRX"])
        atualizarGrafico(
            grafico,
            dados["amostrasTX"],
            dados["amostrasRX"],
            dados["amostragem"],
            portadora
            )
        bitsTX.set_text(dados["bitsTX"])
        bitsRX.set_text(dados["bitsRX"])

        # CAMADA DE ENLACE
        if enquadramento == "Nenhum" and deteccao == "Nenhuma":

            quadroTX.set_text("Sem enquadramento")
            quadroRX.set_text("Sem enquadramento")

        else:

            quadroTX.set_text(dados["quadroTX"])
            quadroRX.set_text(dados["quadroRX"])

        verificacao.set_text(
            "Verificacao no receptor (" + deteccao + "): "
            + dados["verificacao"]
        )

        # CAMADA FISICA
        if portadora == "Nenhuma":

            if modulacao == "Manchester":

                descricaoSinal.set_text(
                    "Banda-base: duas amostras "
                    "representativas por bit (V)"
                )

            else:

                descricaoSinal.set_text(
                    "Banda-base: uma amostra "
                    "representativa por bit (V)"
                )

        else:

            descricaoSinal.set_text(
                "Modulacao por portadora: "
                "primeiras 10 amostras da onda (V)"
            )

        sinalTX.set_text(dados["sinalTX"])
        sinalRX.set_text(dados["sinalRX"])

        # RESULTADO FINAL
        resultado.set_text(
            "Mensagem recebida: " + dados["textoRX"]
        )

    except (ValueError, UnicodeError) as erro:

        textoRX.set_text("Falha na recepcao")
        bitsRX.set_text("Dados indisponiveis")

        quadroTX.set_text("Transmissao nao concluida")
        quadroRX.set_text("Recepcao nao concluida")
        verificacao.set_text("Verificacao nao concluida")

        sinalTX.set_text("Dados indisponiveis")
        sinalRX.set_text("Dados indisponiveis")

        descricaoSinal.set_text(
            "Nao foi possivel concluir a transmissao."
        )

        resultado.set_text("Erro: " + str(erro))


# INICIALIZACAO DA INTERFACE
def iniciarInterface():

    # JANELA PRINCIPAL
    janela = Gtk.Window(title="Simulador TR1")

    janela.set_default_size(1500, 750)
    janela.connect("destroy", Gtk.main_quit)

    # Permite rolar a janela caso existam muitos campos
    rolagem = Gtk.ScrolledWindow()

    rolagem.set_policy(
        Gtk.PolicyType.AUTOMATIC,
        Gtk.PolicyType.AUTOMATIC
    )

    janela.add(rolagem)

    caixa = Gtk.Box(
        orientation=Gtk.Orientation.VERTICAL,
        spacing=10
    )

    caixa.set_border_width(15)
    rolagem.add(caixa)

    # Titulo principal
    titulo = Gtk.Label(
        label="Bem-vindo ao simulador de TR1!"
    )

    caixa.pack_start(titulo, False, False, 0)

    # Entrada da mensagem
    entrada = Gtk.Entry()

    entrada.set_placeholder_text(
        "Digite sua mensagem..."
    )

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

    # CODIFICACAO BANDA-BASE
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

    # MODULACAO POR PORTADORA
    rotuloPortadora = Gtk.Label(
        label="Modulacao por portadora:"
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

    # Aviso exibido quando uma portadora e escolhida
    avisoPortadora = Gtk.Label(label="")
    avisoPortadora.set_line_wrap(True)

    caixaConfiguracoes.pack_start(
        avisoPortadora, False, False, 0
    )

    seletorPortadora.connect(
        "changed",
        aoMudarPortadora,
        seletor,
        avisoPortadora
    )


    # ENQUADRAMENTO
    rotuloEnquadramento = Gtk.Label(
        label="Tipo de enquadramento:"
    )

    caixaConfiguracoes.pack_start(
        rotuloEnquadramento, False, False, 0
    )

    seletorEnquadramento = Gtk.ComboBoxText()

    seletorEnquadramento.append_text("Nenhum")
    seletorEnquadramento.append_text("Bit stuffing")
    seletorEnquadramento.append_text("Byte stuffing")
    seletorEnquadramento.append_text("Contagem")
    seletorEnquadramento.append_text("Entrelaçamento")

    seletorEnquadramento.set_active(0)

    caixaConfiguracoes.pack_start(
        seletorEnquadramento, False, False, 0
    )

    # TAMANHO MAXIMO DA CARGA UTIL
    rotuloQuadro = Gtk.Label(
        label="Tamanho maximo da carga util por quadro (bytes):"
    )

    caixaConfiguracoes.pack_start(
        rotuloQuadro, False, False, 0
    )

    controleQuadro = Gtk.SpinButton.new_with_range(
        1, 255, 1
    )

    controleQuadro.set_value(1)

    caixaConfiguracoes.pack_start(
        controleQuadro, False, False, 0
    )

    # DETECCAO OU CORRECAO DE ERROS
    rotuloDeteccao = Gtk.Label(
        label="Tipo de deteccao ou correcao de erros:"
    )

    caixaConfiguracoes.pack_start(
        rotuloDeteccao, False, False, 0
    )

    seletorDeteccao = Gtk.ComboBoxText()

    seletorDeteccao.append_text("Nenhuma")
    seletorDeteccao.append_text("Bit de paridade")
    seletorDeteccao.append_text("Checksum")
    seletorDeteccao.append_text("CRC-32")
    seletorDeteccao.append_text("Hamming")

    seletorDeteccao.set_active(0)

    caixaConfiguracoes.pack_start(
        seletorDeteccao, False, False, 0
    )


    # RUIDO AWGN: media (x) e desvio padrao (sigma)
    rotuloMedia = Gtk.Label(
        label="Media do ruido AWGN (V):"
    )

    caixaConfiguracoes.pack_start(
        rotuloMedia, False, False, 0
    )

    controleMedia = Gtk.SpinButton.new_with_range(
        -1.0, 1.0, 0.1
    )

    controleMedia.set_value(0.0)

    caixaConfiguracoes.pack_start(
        controleMedia, False, False, 0
    )

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

    gridAplicacao = criarGridTXRX()

    frameAplicacao.add(gridAplicacao)

    # Textos
    textoTX = criarRotulo(
        "Aguardando transmissao..."
    )

    textoRX = criarRotulo(
        "Aguardando recepcao..."
    )

    gridAplicacao.attach(textoTX, 0, 1, 1, 1)
    gridAplicacao.attach(textoRX, 1, 1, 1, 1)

    # Bits ASCII
    bitsTX = criarRotulo(
        "Aguardando bits TX..."
    )

    bitsRX = criarRotulo(
        "Aguardando bits RX..."
    )

    gridAplicacao.attach(bitsTX, 0, 2, 1, 1)
    gridAplicacao.attach(bitsRX, 1, 2, 1, 1)


    # CAMADA DE ENLACE
    frameEnlace = Gtk.Frame(
        label="Camada de Enlace"
    )

    caixa.pack_start(
        frameEnlace, False, False, 0
    )

    gridEnlace = criarGridTXRX()

    frameEnlace.add(gridEnlace)

    # Quadros transmitidos e recebidos
    quadroTX = criarRotulo(
        "Aguardando quadros TX..."
    )

    quadroRX = criarRotulo(
        "Aguardando quadros RX..."
    )

    gridEnlace.attach(quadroTX, 0, 1, 1, 1)
    gridEnlace.attach(quadroRX, 1, 1, 1, 1)

    # Resultado da deteccao/correcao de cada quadro no receptor
    verificacao = criarRotulo(
        "Aguardando verificacao dos quadros...", 120
    )

    gridEnlace.attach(verificacao, 0, 2, 2, 1)

    # CAMADA FISICA
    frameFisica = Gtk.Frame(
        label="Camada Fisica"
    )

    caixa.pack_start(
        frameFisica, False, False, 0
    )

    gridFisica = criarGridTXRX()

    frameFisica.add(gridFisica)

    # Descricao dos sinais
    descricaoSinal = Gtk.Label(
        label="Aguardando dados da camada fisica..."
    )

    descricaoSinal.set_line_wrap(True)

    gridFisica.attach(
        descricaoSinal, 0, 1, 2, 1
    )

    # Sinais eletricos
    sinalTX = criarRotulo(
        "Aguardando sinal TX..."
    )

    sinalRX = criarRotulo(
        "Aguardando sinal RX..."
    )

    gridFisica.attach(sinalTX, 0, 2, 1, 1)
    gridFisica.attach(sinalRX, 1, 2, 1, 1)
    grafico = criarGrafico()
    gridFisica.attach(grafico[0], 0, 3, 2, 1)


    # BOTAO DE ENVIO E RESULTADO
    resultado = criarRotulo(
        "Aguardando mensagem..."
    )

    botao = Gtk.Button(label="Enviar")

    botao.connect(
        "clicked",
        aoClicar,
        entrada,
        seletor,
        seletorPortadora,
        seletorEnquadramento,
        controleQuadro,
        seletorDeteccao,
        controleMedia,
        controleRuido,
        resultado,
        textoTX,
        textoRX,
        bitsTX,
        bitsRX,
        quadroTX,
        quadroRX,
        verificacao,
        sinalTX,
        sinalRX,
        descricaoSinal,
        grafico
    )

    caixa.pack_start(
        botao, False, False, 0
    )

    caixa.pack_start(
        resultado, False, False, 0
    )

    # EXIBIR INTERFACE
    janela.show_all()
    Gtk.main()
