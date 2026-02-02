---
summary: "Slash commands: text vs native, config, and supported commands"
read_when:
  - Using or configuring chat commands
  - Debugging command routing or permissions
---

Comandos Slash

Os comandos são tratados pelo portal. A maioria dos comandos deve ser enviada como uma ** mensagem standalone** que começa com `/`.
O comando host-only bash chat usa `! <cmd>` (com `/bash <cmd>` como um alias).

Existem dois sistemas relacionados:

- **Comandos**: mensagens independentes `/...`.
- ** Directivas**: `/think`, `/verbose`, `/reasoning`, `/elevated`, `/exec`, <<CODE6>, `/queue`.
- As directivas são retiradas da mensagem antes de o modelo a ver.
- Nas mensagens de chat normais (não apenas diretivas), elas são tratadas como “inline hints” e não ** persistir configurações de sessão.
- Nas mensagens de directiva (a mensagem contém apenas directivas), elas persistem na sessão e respondem com um reconhecimento.
- As directivas só são aplicáveis aos ** remetentes autorizados** (listas de canais/pares mais `commands.useAccessGroups`).
Os remetentes não autorizados vêem diretivas tratadas como texto simples.

Existem também alguns atalhos em linha** (apenas remetentes autorizados): `/help`, `/commands`, `/status`, `/whoami` (`/id`).
Eles correm imediatamente, são despojados antes que o modelo veja a mensagem, e o texto restante continua através do fluxo normal.

Configuração

```json5
{
  commands: {
    native: "auto",
    nativeSkills: "auto",
    text: true,
    bash: false,
    bashForegroundMs: 2000,
    config: false,
    debug: false,
    restart: false,
    useAccessGroups: true,
  },
}
```

- `commands.text` (padrão `true`) permite a análise `/...` nas mensagens de chat.
- Em superfícies sem comandos nativos (WhatsApp/WebChat/Sinal/iMessage/Google Chat/MS Teams), comandos de texto ainda funcionam mesmo se você definir isso para `false`.
- `commands.native` (padrão `"auto"`) registra comandos nativos.
- Auto: on for Discord/Telegram; off for Slack (até adicionar comandos de barra); ignorado para provedores sem suporte nativo.
- Definir `channels.discord.commands.native`, `channels.telegram.commands.native`, ou `channels.slack.commands.native` para substituir por fornecedor (bool ou `"auto"`).
- `false` limpa comandos previamente registrados em Discord/Telegram na inicialização. Os comandos Slack são gerenciados no aplicativo Slack e não são removidos automaticamente.
- `commands.nativeSkills` (padrão `"auto"`) registra comandos **skill** nativamente quando suportados.
- Auto: on for Discord/Telegram; off for Slack (Slack requer criar um comando slash por habilidade).
- Definir `channels.discord.commands.nativeSkills`, `channels.telegram.commands.nativeSkills`, ou `channels.slack.commands.nativeSkills` para substituir por provedor (bool ou `"auto"`).
- `commands.bash` (padrão `false`) permite `! <cmd>` executar comandos de shell (`/bash <cmd>` é um alias; requer `tools.elevated` allowlists).
- `commands.bashForegroundMs` (padrão `2000`) controla quanto tempo o bash espera antes de mudar para o modo de fundo (<<CODE24>) imediatamente.
- `commands.config` (padrão `false`) permite `/config` (leituras/escritas `openclaw.json`).
- `commands.debug` (por omissão `false`) permite `/debug` (somente sobreposições de execução).
- `commands.useAccessGroups` (default `true`) impõe listas/políticas de comandos.

# # Lista de comandos

Texto + nativo (quando habilitado):

- <<CODE0>
- <<CODE1>
- <<CODE2> (corrir uma habilidade pelo nome)
- `/status` (mostrar o estado atual; inclui o uso/quota do provedor do modelo atual quando disponível)
- <<CODE4> (lista/add/remove allowlist entradas)
- <<CODE5> (promessas de aprovação executiva)
- `/context [list|detail|json]` (explicar “contexto”; `detail` mostra por ficheiro + por ferramenta + por habilidade + tamanho do sistema)
- `/whoami` (mostrar o seu id remetente; alias: `/id`)
- `/subagents list|stop|log|info|send` (inspeccionar, parar, registar ou executar sub- agente de mensagens para a sessão actual)
- <<CODE11> (persistir configuração para o disco, somente proprietário; requer `commands.config: true`)
- `/debug show|set|unset|reset` (somente para execução; requer `commands.debug: true`)
- `/usage off|tokens|full|cost` (per- resposta de utilização do rodapé ou resumo dos custos locais)
- `/tts off|always|inbound|tagged|status|provider|limit|summary|audio` (TTS de controlo; ver [/tts](/tts)]
- Discórdia: comando nativo é `/voice` (reservas de discórdia `/tts`); texto `/tts` ainda funciona.
- <<CODE20>
- <<CODE21>
- <<CODE22> (também conhecido por `/dock_telegram`) (comutação de respostas ao Telegram)
- <<CODE24> (também conhecido por `/dock_discord`) (comutação de respostas à Discórdia)
- <<CODE26> (também conhecido por `/dock_slack`) (respostas de mudança para Slack)
- `/activation mention|always` (apenas grupos)
- <<CODE29> (apenas proprietário)
- <<CODE30> ou <<CODE31> (Dica do modelo opcional; o restante é passado através)
- `/think <off|minimal|low|medium|high|xhigh>` (escolhas dinâmicas por modelo/fornecedor; apelidos: `/thinking`, `/t`)
- <<CODE35> (também conhecido por `/v`)
- `/reasoning on|off|stream` (também conhecido por: `/reason`; quando ligado, envia uma mensagem separada prefixada `Reasoning:`; `stream` = apenas projecto de telegrama)
- `/elevated on|off|ask|full` (também conhecido por: `/elev`; `full` salta aprovações executivas)
- `/exec host=<sandbox|gateway|node> security=<deny|allowlist|full> ask=<off|on-miss|always> node=<id>` (enviar `/exec` para mostrar a corrente)
- `/model <name>` (também conhecido por: `/models`; ou `/<alias>` de `agents.defaults.models.*.alias`)
- <<CODE50> (mais opções como `debounce:2s cap:25 drop:summarize`; envie `/queue` para ver as configurações atuais)
- <<CODE53> (somente para hospedeiros; alias para `! <command>`; requer `commands.bash: true` + <CODE56> listas de autorizações)

Apenas texto:

- `/compact [instructions]` (ver [/conceitos/compactação] (</concepts/compaction)]
- <<CODE1> (apenas para acolhimento; um de cada vez; utilização `!poll` + `!stop` para trabalhos de longa duração)
- `!poll` (verificar saída / status; aceita opcional `sessionId`; `/bash poll` também funciona)
- `!stop` (parar a tarefa de execução bash; aceita opcional `sessionId`; `/bash stop` também funciona)

Notas:

- Os comandos aceitam um opcional `:` entre o comando e os args (por exemplo, `/think: high`, `/send: on`, `/help:`).
- <<CODE4> aceita um alias de modelo, `provider/model`, ou um nome de provedor (fuzzy match); se não corresponder, o texto é tratado como o corpo da mensagem.
- Para avaria total da utilização do prestador, utilizar `openclaw status --usage`.
- <<CODE7> requer `commands.config=true` e honra o canal `configWrites`.
- <<CODE10> controla o rodapé de utilização por resposta; <<CODE11> imprime um resumo de custo local de registros de sessão OpenClaw.
- `/restart` está desativado por padrão; definido `commands.restart: true` para habilitá-lo.
- <<CODE14> é destinado para depuração e visibilidade extra; mantenha-o desligado** em uso normal.
- `/reasoning` (e `/verbose`) são arriscados em configurações de grupo: eles podem revelar raciocínio interno ou saída de ferramenta que você não pretendia expor. Prefere deixá-los fora, especialmente em bate-papo em grupo.
- ** Caminho rápido:** Mensagens somente de comandos de remetentes listados são tratadas imediatamente (ficha bypass + modelo).
- **Mensagem do grupo gating:**mensagens somente de comandos de remetentes listados para a listagem de pedidos de menção bypass.
- **Atalhos em linha (apenas remetentes listados):** alguns comandos também funcionam quando incorporados em uma mensagem normal e são despojados antes que o modelo veja o texto restante.
- Exemplo: `hey /status` desencadeia uma resposta de status, e o texto restante continua através do fluxo normal.
- Actualmente: `/help`, `/commands`, `/status`, `/whoami` (`/id`).
- As mensagens de comando não autorizadas são silenciosamente ignoradas, e os tokens em linha `/...` são tratados como texto simples.
- ** Comandos de habilidade:** `user-invocable` habilidades são expostas como comandos de barra. Nomes são higienizados para `a-z0-9_` (máximo de 32 caracteres); colisões recebem sufixos numéricos (por exemplo, `_2`).
- `/skill <name> [input]` executa uma habilidade pelo nome (útil quando os limites de comandos nativos impedem comandos por habilidade).
- Por padrão, os comandos de habilidade são encaminhados para o modelo como uma solicitação normal.
- Habilidades podem declarar opcionalmente `command-dispatch: tool` para encaminhar o comando diretamente para uma ferramenta (determinística, sem modelo).
- Exemplo: `/prose` (plugin OpenProse) — veja [OpenProse](/prose).
- ** Argumentos de comandos nativos:** Discórdia usa autocompleto para opções dinâmicas (e menus de botões quando você omite args necessários). Telegram e Slack mostram um menu de botões quando um comando suporta escolhas e você omite o arg.

# # Superfícies de uso (o que mostra onde)

- **Uso do fornecedor/quota** (exemplo: “Claude 80% à esquerda”) aparece em `/status` para o provedor atual do modelo quando o rastreamento do uso é ativado.
- **Os tokens/custos por resposta** são controlados por `/usage off|tokens|full` (aplicados às respostas normais).
- <<CODE2> é sobre **models/auth/endpoints**, não uso.

# # Seleção do modelo (`/model`)

`/model` é implementado como diretiva.

Exemplos:

```
/model
/model list
/model 3
/model openai/gpt-5.2
/model opus@anthropic:default
/model status
```

Notas:

- <<CODE0> e <<CODE1> mostrar um seletor compacto e numerado (família modelo + fornecedores disponíveis).
- <<CODE2> seleciona a partir desse coletor (e prefere o provedor atual quando possível).
- <<CODE3> mostra a visão detalhada, incluindo o endpoint do provedor configurado (`baseUrl`) e o modo API (`api`) quando disponível.

# # Depurar substitui

`/debug` permite que você configure **runtime-only** config sobreposições (memória, não disco). Só para proprietários. Desactivado por omissão; activar com `commands.debug: true`.

Exemplos:

```
/debug show
/debug set messages.responsePrefix="[openclaw]"
/debug set channels.whatsapp.allowFrom=["+1555","+4477"]
/debug unset messages.responsePrefix
/debug reset
```

Notas:

- Sobrescritos se aplicam imediatamente a novas leituras de configuração, mas não ** escreva para `openclaw.json`.
- Use <<CODE1> para limpar todos os comandos e retornar à configuração on-disk.

# # Atualizações de configuração

`/config` escreve para a sua configuração no disco (`openclaw.json`). Só para proprietários. Desactivado por omissão; activar com `commands.config: true`.

Exemplos:

```
/config show
/config show messages.responsePrefix
/config get messages.responsePrefix
/config set messages.responsePrefix="[openclaw]"
/config unset messages.responsePrefix
```

Notas:

- Config é validado antes de escrever; alterações inválidas são rejeitadas.
- <<CODE0> as actualizações persistem durante os reinícios.

# # Notas de superfície

- **Comandos de texto** executados na sessão de chat normal (DMs share `main`, grupos têm sua própria sessão).
- ** Comandos nativos** usam sessões isoladas:
- Discórdia: `agent:<agentId>:discord:slash:<userId>`
- Slack: `agent:<agentId>:slack:slash:<userId>` (prefixo configurável via `channels.slack.slashCommand.sessionPrefix`)
- Telegrama: `telegram:slash:<userId>` (segmenta a sessão de chat via `CommandTargetSessionKey`)
- **`/stop`** atinge a sessão de chat ativa para que possa interromper a execução atual.
- ** Slack:** `channels.slack.slashCommand` ainda é suportado para um comando de estilo <<CODE8>. Se você habilitar `commands.native`, você deve criar um comando Slack slash por comando embutido (os mesmos nomes que `/help`). Os menus de argumentos de comandos para o Slack são entregues como botões efêmeros do Block Kit.
