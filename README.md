# Simulador de Comunicação entre Dois Dispositivos

Trabalho final de **CIC0235 – Teleinformática e Redes 1 (T01)**, Universidade de Brasília.
Prof. Marcelo Antônio Marotta.

O simulador transmite uma mensagem de chat do **transmissor (TX)** para o **receptor (RX)** passando pelas camadas de **aplicação**, **enlace** e **física**, por um **meio de comunicação** com ruído gaussiano. Tudo pode ser configurado e acompanhado por uma interface gráfica em GTK.

| Integrante | Matrícula | Responsabilidade |
| --- | --- | --- |
| Leonardo Braga Meneses | 251024664 | Meio de comunicação, banda-base, interface e integração |
| Lucas Centurion Netto | 242003781 | Modulação por portadora, código de Hamming e integração da detecção de erros |
| Marcel Capistrano Almeida Rodrigues | 242035391 | Enquadramento e detecção de erros |

---

## O que foi implementado

| Camada | Protocolos |
| --- | --- |
| **Aplicação** | Chat de texto: texto ↔ bits (ASCII, 8 bits por caractere) |
| **Enlace – enquadramento** | Contagem de caracteres, entrelaçamento de bits, *byte stuffing*, *bit stuffing* |
| **Enlace – detecção de erros** | Bit de paridade par, checksum, CRC-32 (polinômio IEEE 802) |
| **Enlace – correção de erros** | Código de Hamming |
| **Física – banda-base** | NRZ-Polar, Manchester, Bipolar AMI |
| **Física – portadora** | ASK, FSK, 8PSK, 32-QAM |
| **Meio de comunicação** | Sinal em Volts + ruído AWGN com média e desvio padrão ajustáveis |

Todos os protocolos foram implementados à mão, usando apenas a biblioteca padrão do Python (`math` e `random`), sem bibliotecas prontas.

---

## Requisitos

- **Linux** (ou Ubuntu no **WSL**, no Windows)
- **Python 3.10** ou mais novo
- **GTK 3** com **PyGObject**, só para a interface gráfica

> Os testes rodam em qualquer sistema com Python 3.10+. Só a interface gráfica precisa de Linux, por causa do GTK.

### Instalação no Ubuntu / WSL

```bash
sudo apt update
sudo apt install -y python3 python3-gi gir1.2-gtk-3.0
```

### Usando o WSL no Windows

1. Instale o Ubuntu (no PowerShell como administrador) e reinicie se for pedido:
   ```bash
   wsl --install -d Ubuntu
   ```
2. Deixe o Ubuntu como padrão. Isso evita entrar no Linux do Docker, que não tem Python:
   ```bash
   wsl --set-default Ubuntu
   ```
3. No terminal do VS Code, na pasta do projeto, digite `wsl` para entrar no Ubuntu. Para voltar ao Windows, digite `exit`.

---

## Como executar

### Interface gráfica

Na pasta raiz do projeto, no Linux ou no WSL:

```bash
python3 main.py
```

### Testes

Os testes são executados como módulos, a partir da pasta raiz do projeto:

```bash
python3 -m Testes.teste_integracao
```

| Teste | O que verifica |
| --- | --- |
| `teste_nrz`, `teste_manchester`, `teste_bipolar` | Codificação banda-base |
| `teste_ask`, `teste_fsk`, `teste_8psk`, `teste_32qam` | Modulação por portadora, sem e com ruído |
| `teste_meio` | Meio de comunicação e amostrador |
| `teste_conversor`, `teste_conversorRede` | Conversões texto ↔ bits e string ↔ lista |
| `teste_enquadramento` | Métodos de enquadramento |
| `teste_hamming` | Código de Hamming: correção de todos os erros de 1 bit |
| `teste_deteccao` | Detecção e correção integradas ao simulador |
| `teste_simulador`, `teste_integracao`, `teste_integracaoF` | Simulador completo, com várias combinações |

> No Windows, sem WSL, use `python` no lugar de `python3`.

---

## Como usar a interface

Digite a mensagem, ajuste as opções em **Configuração geral** e clique em **Enviar**.

| Campo | Opções | Observação |
| --- | --- | --- |
| Mensagem | texto | Apenas caracteres ASCII (sem acentos nem ç) |
| Codificação banda-base | NRZPolar, Manchester, Bipolar | Travada em NRZPolar quando há portadora |
| Modulação por portadora | Nenhuma, ASK, FSK, 8PSK, 32-QAM | "Nenhuma" usa só a banda-base |
| Tipo de enquadramento | Nenhum, Bit stuffing, Byte stuffing, Contagem, Entrelaçamento | |
| Tamanho máximo da carga útil por quadro | 1 a 255 bytes | Bytes de dados por quadro, sem cabeçalho, flags nem EDC |
| Tipo de detecção ou correção | Nenhuma, Bit de paridade, Checksum, CRC-32, Hamming | Aplicado a cada quadro |
| Média do ruído AWGN | −1,0 a 1,0 V | Desloca o sinal inteiro |
| Desvio padrão do ruído AWGN | 0,0 a 3,0 V | Intensidade do ruído |

Os resultados aparecem por camada, com o transmissor à esquerda e o receptor à direita:

- **Aplicação de rede:** texto e bits enviados e recebidos.
- **Camada de enlace:** quadros transmitidos e recebidos e a verificação de cada quadro no receptor (`Q1: OK`, `Q4: bit 5 corrigido`, `Q2: erro detectado, descartado`).
- **Camada física:** em banda-base, uma amostra por bit (duas no Manchester); com portadora, as 10 primeiras amostras da onda, em Volts.

> Cada clique em **Enviar** sorteia um ruído novo. Para ver o efeito do ruído, envie a mesma mensagem algumas vezes.

### Testes rápidos pela interface

| Configuração | Resultado esperado |
| --- | --- |
| Qualquer combinação com desvio 0,0 | Mensagem sempre chega correta |
| Portadoras com desvio 0,8 V, sem enlace | ASK, FSK e 8PSK corretos; 32-QAM com erros |
| Média −1,0 V e desvio 0,1 V | Banda-base erra; as 4 portadoras acertam |
| Contagem + Hamming, 1 byte por quadro, desvio 0,5 V | Bits corrigidos e mensagem correta na maioria das vezes |
| Contagem + CRC-32, desvio 0,5 V | Quadros com erro descartados e sinalizados |

---

## Estrutura do projeto

```
TrabalhoTR1/
├── main.py                      # Ponto de entrada: abre a interface
├── AplicacaoRede/
│   └── Conversor.py             # Texto <-> bits (ASCII)
├── CamadaEnlace/
│   ├── Enquadramento/           # Contagem, Entrelacamento, ByteStuffing, BitStuffing
│   ├── DeteccaoErro/            # BitParidade, Checksum, CRC
│   └── CorrecaoErro/Hamming/    # Codigo de Hamming
├── CamadaFisica/
│   ├── ModulacaoDigital/        # NRZPolar, Manchester, Bipolar + amostrador
│   └── ModulacaoPortadora/      # ASK, FSK, PSK8 (8PSK), QAM32 (32-QAM)
├── MeioComunicacao/
│   └── meio.py                  # Ruido AWGN
├── Simulador/
│   ├── simulador.py             # Integra todas as camadas (TX -> meio -> RX)
│   └── conversor.py             # String de bits <-> lista de inteiros
├── Interface/
│   └── interface.py             # Interface grafica em GTK 3
└── Testes/                      # Testes de cada protocolo e de integracao
```

Cada protocolo tem uma função de **transmissão** e outra de **recepção** (por exemplo, `modularASK` / `demodularASK` e `crc_TX` / `crc_RX`).

---

## Funcionamento resumido

```
TX: texto → bits (ASCII) → enquadramento → EDC em cada quadro → banda-base ou portadora
                                                                        ↓
                                                    meio: Volts + ruído n(média, σ)
                                                                        ↓
RX: texto ← bits ← desenquadramento ← verificação/correção ← decodificação ou demodulação
```

- **Representação dos bits:** listas de inteiros na camada física e *strings* de `'0'` e `'1'` na camada de enlace.
- **Sinal físico:** 100 amostras de tensão por bit ou por símbolo.
- **Portadora:** recebe o sinal NRZ-Polar (ligação "NRZ" da Figura 1 do enunciado). A demodulação é feita por correlação com ondas de referência, o que torna as portadoras imunes à média do ruído.
- **Enlace:** o código de detecção ou correção é anexado a cada quadro, e cada quadro é transmitido separadamente pela camada física. No receptor, quadros com erro detectado são descartados e sinalizados, e o Hamming corrige até 1 bit por quadro.

---

## Observações

- Os nomes `PSK8` e `QAM32` foram usados porque nomes de módulos Python não podem começar com número.
- O 8PSK e o 32-QAM agrupam 3 e 5 bits por símbolo. Quando a mensagem não é múltipla desse tamanho, zeros de preenchimento são adicionados e removidos no receptor.
- O relatório completo, com a explicação de cada protocolo e as decisões de projeto, foi entregue em PDF junto com o código.
