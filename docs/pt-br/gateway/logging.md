---
summary: "Logging surfaces, file logs, WS log styles, and console formatting"
read_when:
  - Changing logging output or formats
  - Debugging CLI or gateway output
---

# Logging

Para uma visão geral do usuário (CLI + Control UI + config), veja [/logging](<<LINK0>>>).

Openclaw tem dois log “superfícies”:

- **Console output** (o que você vê no terminal / Debug UI).
- ** Registros de arquivos** (linhas JSON) escritos pelo registrador de gateway.

# # Logger baseado em arquivos

- O ficheiro de registo de rolos por omissão está em <<CODE0>> (um ficheiro por dia): <<CODE1>>
- A data usa o fuso horário local da máquina.
- O caminho e o nível do arquivo de log podem ser configurados via <<CODE2>>:
- <<CODE3>>
- <<CODE4>>

O formato de arquivo é um objeto JSON por linha.

A aba Control UI Logs segue este arquivo através do gateway (<<CODE0>>).
CLI pode fazer o mesmo:

```bash
openclaw logs --follow
```

**Verbose vs. níveis de log**

- ** Os registos de ficheiros** são controlados exclusivamente por <<CODE0>>>.
- <<CODE1> só afeta ** verbosidade de consola** (e estilo de registo WS); não afeta ****
aumentar o nível do registo do ficheiro.
- Para capturar os detalhes somente de verbose nos registros de arquivos, defina <<CODE2>> para <<CODE3>> ou
<<CODE4>>>.

# # Captura de Consola

O CLI captura <<CODE0>> e escreve-os em logs de arquivos,
enquanto ainda imprimia em stdout/stderr.

Você pode sintonizar a verbosidade do console de forma independente via:

- <<CODE0>> (padrão <<CODE1>>)
- < <<CODE2> (<<CODE3>>> <<CODE4>>> <<CODE5>)

# # Redação do resumo da ferramenta

Resumos verbosos de ferramentas (por exemplo, <<CODE0>>>) podem mascarar tokens sensíveis antes de atingirem o
fluxo de console. Isto é **tools-only** e não altera os logs de arquivos.

- < <<CODE0>>: <<CODE1>>>
- <<CODE4>>: array of regex strings (sobrepõe padrões)
- Use strings regex (auto <<CODE5>>>), ou <<CODE6>>> se você precisar de bandeiras personalizadas.
- Os fósforos são mascarados mantendo os primeiros 6 + últimos 4 caracteres (comprimento >= 18), caso contrário <<CODE7>>.
- Os padrões cobrem atribuições de chaves comuns, bandeiras CLI, campos JSON, cabeçalhos ao portador, blocos PEM e prefixos de token populares.

# # Gateway WebSocket logs

O gateway imprime registros de protocolo WebSocket em dois modos:

- **Modo normal (não <<CODE0>>)**: apenas são impressos os resultados de RPC “interessantes”:
- erros (<<<CODE1>>)
- chamadas lentas (limiar padrão: <<CODE2>>>)
- erros de análise
- ** Modo Verbose (<<CODE3>>)**: imprime todo o tráfego de solicitação/resposta WS.

# # # WS log style

<<CODE0> suporta um interruptor de estilo per-gateway:

- <<CODE0> (padrão): modo normal é otimizado; modo verbose usa saída compacta
- <<CODE1>>: saída compacta (pedido/resposta pareado) quando verbose
- <<CODE2>>: saída completa por quadro quando verbose
- <<CODE3>>: alias para <<CODE4>

Exemplos:

```bash
# optimized (only errors/slow)
openclaw gateway

# show all WS traffic (paired)
openclaw gateway --verbose --ws-log compact

# show all WS traffic (full meta)
openclaw gateway --verbose --ws-log full
```

# # Formatação da consola (registro do sub- sistema)

O formato do console é **TTY-saware** e imprime linhas consistentes e prefixadas.
Os registradores do subsistema mantêm a saída agrupada e digitalizável.

Comportamento:

- **Prefixos do subsistema** em cada linha (por exemplo, <<CODE0>>>, <<CODE1>>, <<CODE2>>>)
- ** Cores do subsistema** (estável por subsistema) mais coloração de nível
- ** Cor quando a saída é um TTY ou o ambiente parece um terminal rico** (<<<CODE3>>/<<CODE4>>/<<CODE5>>), respeita <<CODE6>>>
- **Prefixos de subsistema curtos**: gotas que conduzem <<CODE7>> + <<CODE8>>>, mantêm os últimos 2 segmentos (por exemplo, <<CODE9>>>>)
- ** Subloggers by sub-system** (prefixo automático + campo estruturado <<CODE10>>)
- **<<<CODE11>** para saída QR/UX (sem prefixo, sem formatação)
- ** Estilos de consola** (por exemplo, <<CODE12>>)
- ** Nível de registo da consola** separado do nível de registo do ficheiro (o ficheiro mantém todos os detalhes quando <<CODE13>> é definido como <<CODE14>>/<<CODE15>>)
- ** Os corpos de mensagens WhatsApp** estão registados em <<CODE16>> (use <<CODE17>>> para os ver)

Isso mantém os registros de arquivos existentes estáveis enquanto torna a saída interativa digitalizável.
