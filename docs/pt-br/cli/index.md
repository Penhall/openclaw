---
summary: "OpenClaw CLI reference for `openclaw` commands, subcommands, and options"
read_when:
  - Adding or modifying CLI commands or options
  - Documenting new command surfaces
---

Referência CLI

Esta página descreve o comportamento CLI atual. Se os comandos mudarem, atualize este documento.

## Páginas de comando

- `setup` /cli/setup
- `onboard` /cli/onboard
- `configure` /cli/configure
- `config` /cli/config
- `doctor` /cli/doctor
- `dashboard` /cli/dashboard
- `reset` /cli/reset
- `uninstall`/cli/uninstall
- `update` /cli/update
- `message` /cli/message
- `onboard`0] /cli/onboard0)
- `onboard`1] /cli/onboard1)
- `onboard`2] /cli/onboard2)
- `onboard`3] /cli/onboard3)
- `onboard`4]/cli/onboard4)
- `onboard`5] /cli/onboard5)
- `onboard`6] /cli/onboard6)
- `onboard`7]/cli/onboard7)
- `onboard`8] /cli/onboard8)
- `onboard`9] /cli/onboard9)
- `configure`0] /cli/configure0)
- `configure`1] /cli/configure1)
- `configure`2] /cli/configure2)
- `configure`3] /cli/configure3)
- `configure`4] /cli/configure4)
- `configure`5] /cli/configure5)
- `configure`6] /cli/configure6)
- `configure`7] /cli/configure7)
`configure`8] /cli/configure8)
- `configure`9] /cli/configure9)
- `config`0] /cli/config0)
- `config`1] /cli/config1)
- `config`2] /cli/config2)
- `config`3] /cli/config3)
- `config`4] /cli/config4) (comandos de plug-in)
- `config`5] /cli/config5)
- `config`6] /cli/config6)
- `config`7] /cli/config7)
- `config`8] /cli/config8) (plugin; se instalado)

## Bandeiras globais

-`--dev`: estado isolado sob`~/.openclaw-dev`e portas padrão de deslocamento.
-`--profile <name>`: estado isolado no âmbito do`~/.openclaw-<name>`.
-`--no-color`: Desactivar as cores ANSI.
-`--update`: abreviatura para`openclaw update`(apenas instalações de origem).
-`-V`,`--version`,`-v`, versão impressa e saída.

## Estilo de saída

- ANSI cores e indicadores de progresso apenas renderizar em sessões TTY.
- Os hiperlinks OSC-8 renderizam como links clicáveis em terminais suportados; caso contrário, voltamos para URLs simples.
-`--json`(e`--plain`onde suportado) desabilita o estilo para saída limpa.
-`--no-color`desabilita o estilo ANSI;`NO_COLOR=1`também é respeitado.
- Os comandos de longo prazo mostram um indicador de progresso (OSC 9;4 quando suportado).

## Paleta de cores

Openclaw usa uma paleta de lagosta para a saída CLI.

-`accent`(#FF5A2D): cabeçalhos, rótulos, destaques primários.
-`accentBright`(#FF7A3D): nomes de comandos, ênfase.
-`accentDim`(#D14A22): texto de destaque secundário.
-`info`(#FF8A5B): valores informativos.
-`success`(#2FBF71): estados de sucesso.
-`warn`(#FFB020): avisos, recuos, atenção.
-`error`(#E23D2D): erros, falhas.
-`muted`(# 8B7F77): de-ênfase, metadados.

Fonte palette da verdade:`src/terminal/palette.ts`(também conhecido por “fundição lobster”).

## Árvore de comando

```
openclaw [--dev] [--profile <name>] <command>
  setup
  onboard
  configure
  config
    get
    set
    unset
  doctor
  security
    audit
  reset
  uninstall
  update
  channels
    list
    status
    logs
    add
    remove
    login
    logout
  skills
    list
    info
    check
  plugins
    list
    info
    install
    enable
    disable
    doctor
  memory
    status
    index
    search
  message
  agent
  agents
    list
    add
    delete
  acp
  status
  health
  sessions
  gateway
    call
    health
    status
    probe
    discover
    install
    uninstall
    start
    stop
    restart
    run
  logs
  system
    event
    heartbeat last|enable|disable
    presence
  models
    list
    status
    set
    set-image
    aliases list|add|remove
    fallbacks list|add|remove|clear
    image-fallbacks list|add|remove|clear
    scan
    auth add|setup-token|paste-token
    auth order get|set|clear
  sandbox
    list
    recreate
    explain
  cron
    status
    list
    add
    edit
    rm
    enable
    disable
    runs
    run
  nodes
  devices
  node
    run
    status
    install
    uninstall
    start
    stop
    restart
  approvals
    get
    set
    allowlist add|remove
  browser
    status
    start
    stop
    reset-profile
    tabs
    open
    focus
    close
    profiles
    create-profile
    delete-profile
    screenshot
    snapshot
    navigate
    resize
    click
    type
    press
    hover
    drag
    select
    upload
    fill
    dialog
    wait
    evaluate
    console
    pdf
  hooks
    list
    info
    check
    enable
    disable
    install
    update
  webhooks
    gmail setup|run
  pairing
    list
    approve
  docs
  dns
    setup
  tui
```

Nota: os plugins podem adicionar comandos de topo adicionais (por exemplo,`openclaw voicecall`.

## Segurança

-`openclaw security audit`— configuração de auditoria + estado local para armas de segurança comuns.
-`openclaw security audit --deep`— sonda de melhor esforço ao vivo.
-`openclaw security audit --fix`- apertar padrões seguros e estado chmod/config.

## Plugins

Gerenciar extensões e sua configuração:

-`openclaw plugins list`- descobrir plugins (use`--json`para a saída da máquina).
-`openclaw plugins info <id>`— mostrar detalhes para um plugin.
-`openclaw plugins install <path|.tgz|npm-spec>`— instale um plugin (ou adicione um caminho para o`plugins.load.paths`.
-`openclaw plugins enable <id>`/`disable <id>`— Comutar o`plugins.entries.<id>.enabled`.
-`openclaw plugins doctor`— relatar erros de carga de plugin.

A maioria das alterações de plug-ins requer um reinício do gateway. Ver [/plugin] /plugin.

## Memória

Pesquisa de vetores sobre`MEMORY.md`+`memory/*.md`:

-`openclaw memory status`— apresentar estatísticas do índice.
-`openclaw memory index`— reindexar arquivos de memória.
-`openclaw memory search "<query>"`— pesquisa semântica sobre memória.

## Comandos de barra de conversa

Mensagens de chat suportam comandos`/...`(texto e nativos). Ver [/tools/slash-commands] /tools/slash-commands.

Destaques:

-`/status`para diagnósticos rápidos.
-`/config`para alterações de configuração persistentes.
-`/debug`para sobreposições de configuração somente de execução (memória, não disco; requer`commands.debug: true`.

## Configuração + integração

## #`setup`

Inicializar configuração + espaço de trabalho.

Opções:

-`--workspace <dir>`: rota do espaço de trabalho do agente (padrão`~/.openclaw/workspace`.
-`--wizard`: execute o assistente de bordo.
-`--non-interactive`: execute o assistente sem avisos.
- Modo assistente.
-`--remote-url <url>`: URL do portal remoto.
-`--remote-token <token>`: símbolo remoto da porta.

O assistente executa automaticamente quando estão presentes quaisquer bandeiras de assistente `--non-interactive`,`--mode`,`--remote-url`,`--remote-token`.

## #`onboard`

Assistente interativo para configurar gateway, espaço de trabalho e habilidades.

Opções:

-`--workspace <dir>`-`--reset`(reset config + credenciais + sessões + espaço de trabalho antes do assistente)
-`--non-interactive`-`--mode <local|remote>`-`--flow <quickstart|advanced|manual>`(manual é um apelido para avançado)
-`--auth-choice <setup-token|token|chutes|openai-codex|openai-api-key|openrouter-api-key|ai-gateway-api-key|moonshot-api-key|kimi-code-api-key|synthetic-api-key|venice-api-key|gemini-api-key|zai-api-key|apiKey|minimax-api|minimax-api-lightning|opencode-zen|skip>`-`--token-provider <id>`(não interactivo; utilizado com`--auth-choice token`
-`--token <token>`(não-interactivo; utilizado com`--auth-choice token`
-`--reset`0 (não-interactivo; por omissão:`--reset`1)
-`--reset`2 (não-interactivo, por exemplo,`--reset`3,`--reset`4)
-`--reset`5
-`--reset`6
-`--reset`7
-`--reset`8
-`--reset`9
-`--non-interactive`0
-`--non-interactive`1
-`--non-interactive`2
-`--non-interactive`3
-`--non-interactive`4
-`--non-interactive`5
-`--non-interactive`6
-`--non-interactive`7
-`--non-interactive`8
-`--non-interactive`9
-`--mode <local|remote>`0
-`--mode <local|remote>`1
-`--mode <local|remote>`2
-`--mode <local|remote>`3
-`--mode <local|remote>`4
-`--mode <local|remote>`5 (também conhecido por:`--mode <local|remote>`6)
-`--mode <local|remote>`7
-`--mode <local|remote>`8
-`--mode <local|remote>`9
-`--flow <quickstart|advanced|manual>`0
-`--flow <quickstart|advanced|manual>`1
-`--flow <quickstart|advanced|manual>`2 (pnpm recomendado; pão não recomendado para o tempo de execução Gateway)
-`--flow <quickstart|advanced|manual>`3

## #`configure`

Assistente de configuração interativa (modelos, canais, habilidades, gateway).

## #`config`

Ajudantes de configuração não- interativos (get/set/unset). Executar`openclaw config`sem
subcomando lança o assistente.

Subcomandos:

-`config get <path>`: imprime um valor de configuração (ponto/caminho).
-`config set <path> <value>`: defina um valor (JSON5 ou string cru).
-`config unset <path>`: remover um valor.

## #`doctor`

Verificações de saúde + correções rápidas (config + gateway + serviços legados).

Opções:

-`--no-workspace-suggestions`: desabilitar dicas de memória de espaço de trabalho.
-`--yes`: aceitar predefinições sem alertar (sem cabeça).
-`--non-interactive`: pule prompts; aplique migrações seguras apenas.
-`--deep`: serviços de sistema de varredura para instalações de gateway extra.

## Ajudantes de canal

## #`channels`

Gerenciar contas de canais de chat (WhatsApp/Telegram/Discord/Google Chat/Slack/Mattermost (plugin)/Sinal/iMessage/MS Teams).

Subcomandos:

-`channels list`: mostrar canais configurados e perfis de autenticação.
-`channels status`: verificar a acessibilidade do portal e a saúde do canal `--probe`executa verificações extras; use`openclaw health`ou`openclaw status --deep`para sondas de saúde do portal).
- Dica:`channels status`imprime avisos com correções sugeridas quando pode detectar erros comuns (então aponta para`openclaw doctor`.
-`channels logs`: mostrar os registros de canais recentes do arquivo de registro de gateway.
-`channels add`: configuração em estilo de assistente quando nenhuma bandeira é passada; bandeiras mudam para o modo não-interativo.
-`channels remove`: desabilitar por padrão; passar`channels status`0 para remover entradas de configuração sem prompts.
-`channels status`1: login de canal interativo (somente WhatsApp Web).
-`channels status`2: sair de uma sessão de canal (se for suportado).

Opções comuns:

-`--channel <name>`:`whatsapp|telegram|discord|googlechat|slack|mattermost|signal|imessage|msteams`-`--account <id>`: ID da conta de canal (padrão`default`
-`--name <label>`: nome de exibição para a conta

`channels login`opções:

-`--channel <channel>`(padrão`whatsapp`; apoia`whatsapp`/`web`
-`--account <id>`-`--verbose`

`channels logout`opções:

-`--channel <channel>`(padrão`whatsapp`
-`--account <id>`

`channels list`opções:

-`--no-usage`: skip model provider use/quota snapshots (OAuth/API-backed only).
-`--json`: saída JSON (inclui o uso a menos que o`--no-usage`esteja definido).

`channels logs`opções:

-`--channel <name|all>`(padrão`all`
-`--lines <n>`(padrão`200`
-`--json`

Mais detalhes: [/conceitos/outh]/concepts/oauth

Exemplos:

```bash
openclaw channels add --channel telegram --account alerts --name "Alerts Bot" --token $TELEGRAM_BOT_TOKEN
openclaw channels add --channel discord --account work --name "Work Bot" --token $DISCORD_BOT_TOKEN
openclaw channels remove --channel discord --account work --delete
openclaw channels status --probe
openclaw status --deep
```

## #`skills`

Listar e inspecionar as habilidades disponíveis mais informações de prontidão.

Subcomandos:

-`skills list`: listar as habilidades (padrão quando não há subcomando).
-`skills info <name>`: mostrar detalhes para uma habilidade.
-`skills check`: resumo dos requisitos prontos versus em falta.

Opções:

-`--eligible`: mostrar apenas habilidades prontas.
-`--json`: saída JSON (sem estilo).
-`-v`,`--verbose`: incluir os requisitos em falta.

Dica: use`npx clawhub`para pesquisar, instalar e sincronizar habilidades.

## #`pairing`

Aprovar pedidos de emparelhamento DM entre canais.

Subcomandos:

-`pairing list <channel> [--json]`-`pairing approve <channel> <code> [--notify]`

## #`webhooks gmail`

Gmail Pub/Sub gancho configuração + corredor. Ver [/automatização/gmail-pubsub]/automation/gmail-pubsub.

Subcomandos:

-`webhooks gmail setup`(exige`--account <email>`; apoia`--project`,`--topic`,`--subscription`,`--label`,`--hook-url`,`--hook-token`,`--push-token`,`--bind`,`--account <email>`0,`--account <email>`1,`--account <email>`2,`--account <email>`3,`--account <email>`4,`--account <email>`5,`--account <email>`6,`--account <email>`7,`--account <email>`8,`--account <email>`9)
-`--project`0 (sobreposição de tempo de execução para as mesmas bandeiras)

## #`dns setup`

Ampla área de descoberta DNS helper (CoreDNS + Tailscale). Ver [/porta/descoberta] /gateway/discovery.

Opções:

-`--apply`: instalar/atualizar a configuração do CoreDNS (exige sudo; macOS somente).

## Mensagens + agente

## #`message`

Mensagens de saída unificadas + ações de canal.

Ver: [/cli/mensagem]/cli/message

Subcomandos:

-`message send|poll|react|reactions|read|edit|delete|pin|unpin|pins|permissions|search|timeout|kick|ban`-`message thread <create|list|reply>`-`message emoji <list|upload>`-`message sticker <send|upload>`-`message role <info|add|remove>`-`message channel <info|list>`-`message member info`-`message voice status`-`message event <list|create>`

Exemplos:

-`openclaw message send --target +15555550123 --message "Hi"`-`openclaw message poll --channel discord --target channel:123 --poll-question "Snack?" --poll-option Pizza --poll-option Sushi`

## #`agent`

Executar uma volta de agente através do Gateway (ou`--local`incorporado).

Necessário:

-`--message <text>`

Opções:

-`--to <dest>`(para chave de sessão e entrega opcional)
-`--session-id <id>`-`--thinking <off|minimal|low|medium|high|xhigh>`(apenas modelos GPT-5.2 + Codex)
-`--verbose <on|full|off>`-`--channel <whatsapp|telegram|discord|slack|mattermost|signal|imessage|msteams>`-`--local`-`--deliver`-`--json`-`--timeout <seconds>`

## #`agents`

Gerenciar agentes isolados (espaços de trabalho + autenticação + roteamento).

###`agents list`

Listar os agentes configurados.

Opções:

-`--json`-`--bindings`

###`agents add [name]`

Adicione um novo agente isolado. Executa o assistente guiado a menos que as bandeiras (ou`--non-interactive` sejam passadas;`--workspace`é necessário em modo não-interativo.

Opções:

-`--workspace <dir>`-`--model <id>`-`--agent-dir <dir>`-`--bind <channel[:accountId]>`(repetível)
-`--non-interactive`-`--json`

Especificações de ligação usam`channel[:accountId]`. Quando o`accountId`é omitido para o WhatsApp, o id da conta padrão é usado.

###`agents delete <id>`

Excluir um agente e podar seu espaço de trabalho + estado.

Opções:

-`--force`-`--json`

## #`acp`

Execute a ponte ACP que conecta IDEs ao Gateway.

Ver `acp`/cli/acp para opções e exemplos completos.

## #`status`

Mostrar a saúde da sessão ligada e os destinatários recentes.

Opções:

-`--json`-`--all`(diagnóstico completo; somente leitura, pastável)
-`--deep`(canais de sondagem)
-`--usage`(mostrar a utilização/quota do fornecedor do modelo)
-`--timeout <ms>`-`--verbose`-`--debug`(também conhecido por`--verbose`

Notas:

- Visão geral inclui Gateway + nó host status de serviço quando disponível.

### Rastreio de uso

OpenClaw pode usar / quota de superfície do provedor quando os créditos OAuth / API estão disponíveis.

Superfícies:

-`/status`(adiciona uma linha de uso curta do provedor quando disponível)
-`openclaw status --usage`(impressão completa do fornecedor)
- barra de menu do macOS (Seção de Uso em Contexto)

Notas:

- Os dados provêm directamente dos objectivos de utilização do prestador (sem estimativas).
- Providers: Anthropic, GitHub Copilot, OpenAI Codex OAuth, plus Gemini CLI/Antigravity quando esses plugins de provedores estão habilitados.
- Se não existirem credenciais correspondentes, o uso está oculto.
- Detalhes: ver /concepts/usage-tracking.

## #`health`

Vai buscar saúde ao portal.

Opções:

-`--json`-`--timeout <ms>`-`--verbose`

## #`sessions`

Listar as sessões de conversação armazenadas.

Opções:

-`--json`-`--verbose`-`--store <path>`-`--active <minutes>`

## Reiniciar / Desinstalar

## #`reset`

Repor a configuração/estado local (mantém o CLI instalado).

Opções:

-`--scope <config|config+creds+sessions|full>`-`--yes`-`--non-interactive`-`--dry-run`

Notas:

- O`--non-interactive`exige o`--scope`e o`--yes`.

## #`uninstall`

Desinstale o serviço de gateway + dados locais (o CLI permanece).

Opções:

-`--service`-`--state`-`--workspace`-`--app`-`--all`-`--yes`-`--non-interactive`-`--dry-run`

Notas:

-`--non-interactive`exige`--yes`e âmbitos explícitos (ou`--all`.

## Gateway

## #`gateway`

Passa o portal WebSocket.

Opções:

-`--port <port>`-`--bind <loopback|tailnet|lan|auto|custom>`-`--token <token>`-`--auth <token|password>`-`--password <password>`-`--tailscale <off|serve|funnel>`-`--tailscale-reset-on-exit`-`--allow-unconfigured`-`--dev`-`--reset`(reset dev config + credenciais + sessões + espaço de trabalho)
-`--bind <loopback|tailnet|lan|auto|custom>`0 (ouvinte já morto no porto)
-`--bind <loopback|tailnet|lan|auto|custom>`1
-`--bind <loopback|tailnet|lan|auto|custom>`2
-`--bind <loopback|tailnet|lan|auto|custom>`3
-`--bind <loopback|tailnet|lan|auto|custom>`4 (também conhecido por`--bind <loopback|tailnet|lan|auto|custom>`5)
-`--bind <loopback|tailnet|lan|auto|custom>`6
-`--bind <loopback|tailnet|lan|auto|custom>`7

## #`gateway service`

Gerenciar o serviço Gateway (lançado/systemd/schtasks).

Subcomandos:

-`gateway status`(procura o RPC de Gateway por padrão)
-`gateway install`(instalação de serviço)
-`gateway uninstall`-`gateway start`-`gateway stop`-`gateway restart`

Notas:

-`gateway status`sonda o PCR Gateway por padrão usando a porta/configuração resolvida do serviço (sobreposta com o`--url/--token/--password`.
- O`gateway status`apoia o`--no-probe`, o`--deep`e o`--json`para a escrita.
-`gateway status`também apresenta serviços legados ou extra gateway quando pode detectá-los `--deep`adiciona scans de nível de sistema). Serviços OpenClaw com nome de perfil são tratados como de primeira classe e não são marcados como "extra".
-`gateway status`imprime o caminho de configuração que o CLI usa vs o qual configura o serviço que provavelmente usa (service env), além do URL alvo resolvido.
-`gateway install|uninstall|start|stop|restart`suporta`--url/--token/--password`0 para scripting (a saída padrão permanece amigável ao homem).
-`--url/--token/--password`1 defaults to Node runtime; bun is ** not recomendado** (WhatsApp/Telegram bugs).
-`--url/--token/--password`2 opções:`--url/--token/--password`3,`--url/--token/--password`4,`--url/--token/--password`5,`--url/--token/--password`6,`--url/--token/--password`7.

## #`logs`

Registros de arquivos do Gateway de cauda via RPC.

Notas:

- As sessões de TTY renderizam uma visão colorida e estruturada; não-TTTY volta ao texto simples.
-`--json`emite JSON delimitado por linha (um evento de log por linha).

Exemplos:

```bash
openclaw logs --follow
openclaw logs --limit 200
openclaw logs --plain
openclaw logs --json
openclaw logs --no-color
```

## #`gateway <subcommand>`

Ajudantes de CLI (utilizar`--url`,`--token`,`--password`,`--timeout`,`--expect-final`para subcomandos RCP).

Subcomandos:

-`gateway call <method> [--params <json>]`-`gateway health`-`gateway status`-`gateway probe`-`gateway discover`-`gateway install|uninstall|start|stop|restart`-`gateway run`

RCP comuns:

-`config.apply`(validar + gravar configuração + reiniciar + despertar)
-`config.patch`(merge uma atualização parcial + reiniciar + despertar)
-`update.run`(atualização de execução + reiniciar + despertar)

Dica: ao chamar diretamente`config.set`/`config.apply`/`config.patch`, passe`baseHash`de`config.get`se já existe uma configuração.

## Modelos

Ver [/conceitos/modelos]/concepts/models para comportamento de retrocesso e estratégia de digitalização.

Autenticação antrópica preferida (setup-token):

```bash
claude setup-token
openclaw models auth setup-token --provider anthropic
openclaw models status
```

## #`models`(raiz)

`openclaw models`é um apelido para`models status`.

Opções raiz:

-`--status-json`(também conhecido por`models status --json`
-`--status-plain`(também conhecido por`models status --plain`

## #`models list`

Opções:

-`--all`-`--local`-`--provider <name>`-`--json`-`--plain`

## #`models status`

Opções:

-`--json`-`--plain`-`--check`(saída 1 = expirada/falta, 2 = expirada)
-`--probe`(sonda viva de perfis de autenticação configurados)
-`--probe-provider <name>`-`--probe-profile <id>`(repetição ou separação vírgula)
-`--probe-timeout <ms>`-`--probe-concurrency <n>`-`--probe-max-tokens <n>`

Sempre inclui a visão geral da autenticação e o estado de expiração do OAuth para perfis no armazenamento de autenticação.`--probe`executa solicitações ao vivo (pode consumir tokens e ativar limites de taxa).

## #`models set <model>`

Preparar`agents.defaults.model.primary`.

## #`models set-image <model>`

Preparar`agents.defaults.imageModel.primary`.

## #`models aliases list|add|remove`

Opções:

-`list`:`--json`,`--plain`-`add <alias> <model>`-`remove <alias>`

## #`models fallbacks list|add|remove|clear`

Opções:

-`list`:`--json`,`--plain`-`add <model>`-`remove <model>`-`clear`

## #`models image-fallbacks list|add|remove|clear`

Opções:

-`list`:`--json`,`--plain`-`add <model>`-`remove <model>`-`clear`

## #`models scan`

Opções:

-`--min-params <b>`-`--max-age-days <days>`-`--provider <name>`-`--max-candidates <n>`-`--timeout <ms>`-`--concurrency <n>`-`--no-probe`-`--yes`-`--no-input`-`--set-default`-`--max-age-days <days>`0
-`--max-age-days <days>`1

## #`models auth add|setup-token|paste-token`

Opções:

-`add`: Auth helper interativo
- CÓDIGO OCTX1: CÓDIGO OCTX2 (por omissão CÓDIGO OCTX3), CÓDIGO OCTX4
-`paste-token`:`--provider <name>`,`--profile-id <id>`,`--expires-in <duration>`

## #`models auth order get|set|clear`

Opções:

-`get`:`--provider <name>`,`--agent <id>`,`--json`-`set`:`--provider <name>`,`--agent <id>`,`<profileIds...>`-`clear`:`--provider <name>`,`--provider <name>`0

## Sistema

## #`system event`

Coloque um evento do sistema e, opcionalmente, ative um batimento cardíaco (RPC de Gateway).

Necessário:

-`--text <text>`

Opções:

-`--mode <now|next-heartbeat>`-`--json`-`--url`,`--token`,`--timeout`,`--expect-final`

## #`system heartbeat last|enable|disable`

Controles de batimento cardíaco (RPC de Gateway).

Opções:

-`--json`-`--url`,`--token`,`--timeout`,`--expect-final`

## #`system presence`

Listar entradas de presença do sistema (RPC de Gateway).

Opções:

-`--json`-`--url`,`--token`,`--timeout`,`--expect-final`

## Cron

Gerenciar trabalhos agendados (RPC do Gateway). Ver [/automação/crono-jobs] /automation/cron-jobs.

Subcomandos:

-`cron status [--json]`-`cron list [--all] [--json]`(produto de mesa por padrão; use`--json`em bruto)
-`cron add`(também conhecido por:`create`; requer`--name`e exactamente um dos`--at`;`--every`;
-`cron list [--all] [--json]`1 (campos de correspondência)
-`cron list [--all] [--json]`2 (também conhecido por:`cron list [--all] [--json]`3,`cron list [--all] [--json]`4)
-`cron list [--all] [--json]`5
-`cron list [--all] [--json]`6
-`cron list [--all] [--json]`7
-`cron list [--all] [--json]`8

Todos os comandos`cron`aceitam`--url`,`--token`,`--timeout`,`--expect-final`.

## Node host

`node`executa um host de nó ** sem cabeça** ou gerencia-o como um serviço de fundo. Ver
`openclaw node` /cli/node.

Subcomandos:

-`node run --host <gateway-host> --port 18789`-`node status`-`node install [--host <gateway-host>] [--port <port>] [--tls] [--tls-fingerprint <sha256>] [--node-id <id>] [--display-name <name>] [--runtime <node|bun>] [--force]`-`node uninstall`-`node stop`-`node restart`

## Nós

`nodes`fala com o Gateway e alvos de nós emparelhados. Ver [/nós]/nodes.

Opções comuns:

-`--url`,`--token`,`--timeout`,`--json`

Subcomandos:

-`nodes status [--connected] [--last-connected <duration>]`-`nodes describe --node <id|name|ip>`-`nodes list [--connected] [--last-connected <duration>]`-`nodes pending`-`nodes approve <requestId>`-`nodes reject <requestId>`-`nodes rename --node <id|name|ip> --name <displayName>`-`nodes invoke --node <id|name|ip> --command <command> [--params <json>] [--invoke-timeout <ms>] [--idempotency-key <key>]`-`nodes run --node <id|name|ip> [--cwd <path>] [--env KEY=VAL] [--command-timeout <ms>] [--needs-screen-recording] [--invoke-timeout <ms>] <command...>`(nodo central ou host de nó sem cabeça)
-`nodes notify --node <id|name|ip> [--title <text>] [--body <text>] [--sound <name>] [--priority <passive|active|timeSensitive>] [--delivery <system|overlay|auto>] [--invoke-timeout <ms>]`(somente mac)

Câmera:

-`nodes camera list --node <id|name|ip>`-`nodes camera snap --node <id|name|ip> [--facing front|back|both] [--device-id <id>] [--max-width <px>] [--quality <0-1>] [--delay-ms <ms>] [--invoke-timeout <ms>]`-`nodes camera clip --node <id|name|ip> [--facing front|back] [--device-id <id>] [--duration <ms|10s|1m>] [--no-audio] [--invoke-timeout <ms>]`

Tela + tela:

-`nodes canvas snapshot --node <id|name|ip> [--format png|jpg|jpeg] [--max-width <px>] [--quality <0-1>] [--invoke-timeout <ms>]`-`nodes canvas present --node <id|name|ip> [--target <urlOrPath>] [--x <px>] [--y <px>] [--width <px>] [--height <px>] [--invoke-timeout <ms>]`-`nodes canvas hide --node <id|name|ip> [--invoke-timeout <ms>]`-`nodes canvas navigate <url> --node <id|name|ip> [--invoke-timeout <ms>]`-`nodes canvas eval [<js>] --node <id|name|ip> [--js <code>] [--invoke-timeout <ms>]`-`nodes canvas a2ui push --node <id|name|ip> (--jsonl <path> | --text <text>) [--invoke-timeout <ms>]`-`nodes canvas a2ui reset --node <id|name|ip> [--invoke-timeout <ms>]`-`nodes screen record --node <id|name|ip> [--screen <index>] [--duration <ms|10s>] [--fps <n>] [--no-audio] [--out <path>] [--invoke-timeout <ms>]`

Localização:

-`nodes location get --node <id|name|ip> [--max-age <ms>] [--accuracy <coarse|balanced|precise>] [--location-timeout <ms>] [--invoke-timeout <ms>]`

## Navegador

Controle do navegador CLI (dedicado Chrome/Brave/Edge/Chromium). Ver `openclaw browser`/cli/browser e a ferramenta [Browser]/tools/browser.

Opções comuns:

-`--url`,`--token`,`--timeout`,`--json`-`--browser-profile <name>`

Gerenciar:

-`browser status`-`browser start`-`browser stop`-`browser reset-profile`-`browser tabs`-`browser open <url>`-`browser focus <targetId>`-`browser close [targetId]`-`browser profiles`-`browser create-profile --name <name> [--color <hex>] [--cdp-url <url>]`-`browser start`0

Inspecionar:

-`browser screenshot [targetId] [--full-page] [--ref <ref>] [--element <selector>] [--type png|jpeg]`-`browser snapshot [--format aria|ai] [--target-id <id>] [--limit <n>] [--interactive] [--compact] [--depth <n>] [--selector <sel>] [--out <path>]`

Acções:

-`browser navigate <url> [--target-id <id>]`-`browser resize <width> <height> [--target-id <id>]`-`browser click <ref> [--double] [--button <left|right|middle>] [--modifiers <csv>] [--target-id <id>]`-`browser type <ref> <text> [--submit] [--slowly] [--target-id <id>]`-`browser press <key> [--target-id <id>]`-`browser hover <ref> [--target-id <id>]`-`browser drag <startRef> <endRef> [--target-id <id>]`-`browser select <ref> <values...> [--target-id <id>]`-`browser upload <paths...> [--ref <ref>] [--input-ref <ref>] [--element <selector>] [--target-id <id>] [--timeout-ms <ms>]`-`browser fill [--fields <json>] [--fields-file <path>] [--target-id <id>]`-`browser resize <width> <height> [--target-id <id>]`0
-`browser resize <width> <height> [--target-id <id>]`1
-`browser resize <width> <height> [--target-id <id>]`2
-`browser resize <width> <height> [--target-id <id>]`3
-`browser resize <width> <height> [--target-id <id>]`4

## Busca de médicos

## #`docs [query...]`

Pesquisa o índice de documentos ao vivo.

## TUI

## #`tui`

Abra a interface de terminal conectada ao Gateway.

Opções:

-`--url <url>`-`--token <token>`-`--password <password>`-`--session <key>`-`--deliver`-`--thinking <level>`-`--message <text>`-`--timeout-ms <ms>`(defaults to`agents.defaults.timeoutSeconds`
-`--history-limit <n>`
