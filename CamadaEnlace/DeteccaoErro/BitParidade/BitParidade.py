def bit_paridade_TX(fluxo : list[str]) -> list[str]:
    """
    TX: Recebe os quadros e calcula a paridade da quantidade de '1's presentes para cada quadro.
    """
    return [quadro + str(quadro.count("1") %2) for quadro in fluxo]


def bit_paridade_RX(fluxo : list[str]) -> list[str]:
    """RX: confere e remove o bit de paridade de cada quadro; lança erro se divergir."""
    quadros = []
    for quadro in fluxo:
        if not quadro:
            raise ValueError("Quadro vazio.")
        dados, bit_par = quadro[:-1], quadro[-1]
        if str(dados.count("1") % 2) != bit_par:
            raise ValueError("Erro no bit de paridade")
        quadros.append(dados)
    return quadros