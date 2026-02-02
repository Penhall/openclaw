---
summary: "Cron jobs + wakeups for the Gateway scheduler"
read_when:
  - Scheduling background jobs or wakeups
  - Wiring automation that should run with or alongside heartbeats
  - Deciding between heartbeat and cron for scheduled tasks
---

# Trabalhos de Cron (grampeador Gateway)

> **Cron vs Heartbeat?** Ver [Cron vs Heartbeat] /automation/cron-vs-heartbeat para orientação sobre quando usar cada.

Cron é o agendador embutido do Gateway. Continua a trabalhar, acorda o agente
o tempo certo, e pode opcionalmente entregar saída de volta para um chat.

Se você quiser   “corrir isso todas as manhãs”  ou   “falar com o agente em 20 minutos” ,
Cron é o mecanismo.

## TL;DR

- Cron corre ** dentro do Gateway** (não dentro do modelo).
- Os trabalhos persistem sob`~/.openclaw/cron/`para que reinicia não perca agendas.
- Dois estilos de execução:
- **Sessão principal**: enqueue um evento do sistema, em seguida, execute no próximo batimento cardíaco.
- ** Isolado**: executar uma volta de agente dedicado em`cron:<jobId>`, opcionalmente entregar saída.
- Acordes são de primeira classe: um trabalho pode solicitar "acordar agora" vs "próximo batimento cardíaco".

## Início rápido (acionável)

Crie um lembrete de um tiro, verifique se ele existe e execute-o imediatamente:

```bash
openclaw cron add \
  --name "Reminder" \
  --at "2026-02-01T16:00:00Z" \
  --session main \
  --system-event "Reminder: check the cron docs draft" \
  --wake now \
  --delete-after-run

openclaw cron list
openclaw cron run <job-id> --force
openclaw cron runs --id <job-id>
```

Agendar uma tarefa isolada recorrente com a entrega:

```bash
openclaw cron add \
  --name "Morning brief" \
  --cron "0 7 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Summarize overnight updates." \
  --deliver \
  --channel slack \
  --to "channel:C1234567890"
```

## Equivalentes de chamada de ferramentas (ferramenta de cron Gateway)

Para as formas e exemplos canônicos do JSON, veja [Esquema JSON para chamadas de ferramentas]/automation/cron-jobs#json-schema-for-tool-calls.

## Onde os trabalhos de cron são armazenados

Os trabalhos do Cron são persistidos no host do Gateway em`~/.openclaw/cron/jobs.json`por padrão.
O Gateway carrega o arquivo para a memória e o escreve de volta em alterações, então edita manualmente
Só estão seguros quando o portal for parado. Preferir`openclaw cron add/edit`ou o cron
ferramenta chamada API para alterações.

## Visão geral amigável de principiantes

Pense em um trabalho cron como: ** quando** para executar + ** o que** para fazer.

1. ** Escolha um horário**
- Lembrete de um tiro →`schedule.kind = "at"`(CLI:`--at`
- Repetição do trabalho →`schedule.kind = "every"`ou`schedule.kind = "cron"`- Se o seu timestamp ISO omite um fuso horário, é tratado como **UTC**.

2. ** Escolha onde corre **
-`sessionTarget: "main"`→ correr durante o próximo batimento cardíaco com contexto principal.
-`sessionTarget: "isolated"`→ executar uma volta de agente dedicado em`cron:<jobId>`.

3. ** Escolha a carga útil**
- Sessão principal →`payload.kind = "systemEvent"`- Sessão isolada →`payload.kind = "agentTurn"`

Opcional:`deleteAfterRun: true`remove trabalhos bem sucedidos de um tiro da loja.

## Conceitos

Empregos

Uma tarefa cron é um registro armazenado com:

- a ** horário** (quando deve ser executado),
- uma ** carga útil** (o que deve fazer),
- opcional **entrega** (onde a saída deve ser enviada).
- opcional ** vinculação de agentes** `agentId`: executar a tarefa sob um agente específico; se
faltando ou desconhecido, o gateway cai de volta para o agente padrão.

Os trabalhos são identificados por um`jobId`estável (utilizado por APIs CLI/Gateway).
Em chamadas de ferramenta de agente,`jobId`é canônico; legado`id`é aceito para compatibilidade.
Tarefas podem opcionalmente auto-deletar após uma execução bem sucedida de um tiro via`deleteAfterRun: true`.

Calendários

Cron suporta três tipos de programação:

-`at`: timestamp de um tiro (ms desde a época). Gateway aceita ISO 8601 e coerções para UTC.
-`every`: intervalo fixo (ms).
-`cron`: Expressão de cron de 5 campos com fuso horário opcional IANA.

As expressões Cron usam`croner`. Se um fuso- horário for omitido, a máquina Gateway
é utilizado o fuso horário local.

Execução principal vs execução isolada

## # # Trabalhos principais de sessão (eventos do sistema)

Trabalhos principais enqueam um evento do sistema e, opcionalmente, acordam o corredor do batimento cardíaco.
Devem utilizar`payload.kind = "systemEvent"`.

-`wakeMode: "next-heartbeat"`(padrão): evento espera pelo próximo batimento cardíaco programado.
-`wakeMode: "now"`: evento desencadeia um batimento cardíaco imediato.

Este é o melhor ajuste quando você quer o prompt cardíaco normal + contexto de sessão principal.
Ver [Heartbeat] /gateway/heartbeat.

Trabalhos isolados (sessões de crono dedicadas)

Trabalhos isolados executam uma vez agente dedicado na sessão`cron:<jobId>`.

Comportamentos-chave:

- Prompt é prefixado com`[cron:<jobId> <job name>]`para rastreabilidade.
- Cada execução inicia um novo ID de sessão** (sem conversação prévia).
- Um resumo é publicado na sessão principal (prefixo`Cron`, configurável).
-`wakeMode: "now"`provoca um batimento cardíaco imediato após postar o resumo.
- Se`payload.deliver: true`, a saída é entregue em um canal; caso contrário, ela permanece interna.

Use trabalhos isolados para tarefas ruidosas, frequentes ou "tarefas de fundo" que não devem ser spam
o seu histórico de chat principal.

Formas de carga útil (o que corre)

Dois tipos de carga são suportados:

-`systemEvent`: sessão principal apenas, encaminhada através do sinal cardíaco.
-`agentTurn`: sessão isolada apenas, corre uma vez agente dedicado.

Campos`agentTurn`comuns:

-`message`: pedido de texto.
-`model`/`thinking`: substituições opcionais (ver abaixo).
-`timeoutSeconds`: tempo limite opcional.
-`deliver`:`true`para enviar a saída para um alvo de canal.
-`channel`:`last`ou um canal específico.
-`to`: alvo específico do canal (telefone/chat/canal id).
-`bestEffortDeliver`: evitar falhas no trabalho se a entrega falhar.

Opções de isolamento (apenas para`session=isolated`:

-`postToMainPrefix`(CLI:`--post-prefix`: prefixo para o evento do sistema em geral.
-`postToMainMode`:`summary`(padrão) ou`full`.
-`postToMainMaxChars`: valores máximos quando`postToMainMode=full`(padrão 8000).

## Modelo e pensamento anula

Trabalhos isolados `agentTurn` podem substituir o modelo e o nível de pensamento:

-`model`: Providenciador/modelo (por exemplo,`anthropic/claude-sonnet-4-20250514` ou apelido (por exemplo,`opus`
-`thinking`: nível de reflexão `off`,`minimal`,`low`,`medium`,`high`,`xhigh`; GPT-5.2 + apenas modelos de codex)

Nota: Você pode definir`model`em trabalhos de sessão principal também, mas muda o principal compartilhado
modelo de sessão. Recomendamos sobreposições do modelo apenas para trabalhos isolados para evitar
mudanças de contexto inesperadas.

Prioridade da resolução:

1. Sobreposição da carga útil do trabalho (mais alta)
2. Defaults específicos do gancho (por exemplo,`hooks.gmail.model`
3. Padrão de configuração do agente

## # Entrega (canal + alvo)

Trabalhos isolados podem fornecer saída para um canal. A carga útil do trabalho pode especificar:

- PTUXCODE0: PTUXCODE1 / PTUXCODE2 / PTUXCODE3 / PTUXCODE4 / PTUXCODE5 (plugin) / PTUXCODE6 / PTUXCODE7 / PTUXCODE8
-`to`: alvo do destinatário específico do canal

Se o`channel`ou o`to`for omitido, o cron pode voltar à “última rota” da sessão principal
(o último lugar onde o agente respondeu).

Notas de entrega:

- Se o`to`estiver definido, o cron entrega automaticamente a saída final do agente, mesmo que o`deliver`seja omitido.
- Use`deliver: true`quando quiser entrega de última rota sem um`to`explícito.
- Use`deliver: false`para manter a saída interna mesmo se um`to`estiver presente.

Lembretes do formato de destino:

- Os alvos Slack/Discord/Mattermost (plugin) devem utilizar prefixos explícitos (por exemplo,`channel:<id>`,`user:<id>` para evitar ambiguidades.
- Os tópicos de telegrama devem utilizar o formulário`:topic:`(ver abaixo).

### # Alvos de entrega de telegrama (tópicos / tópicos do fórum)

Telegram suporta tópicos do fórum via`message_thread_id`. Para entrega de cron, você pode codificar
O tópico/fio no campo`to`:

-`-1001234567890`(apenas id de bate-papo)
-`-1001234567890:topic:123`(preferido: marcador tópico explícito)
-`-1001234567890:123`(shorthand: sufixo numérico)

São também aceites objectivos prefixados como`telegram:...`/`telegram:group:...`:

-`telegram:group:-1001234567890:topic:123`

## JSON esquema para chamadas de ferramentas

Use estas formas ao chamar ferramentas`cron.*`Gateway diretamente (chamadas de ferramenta de agente ou RPC).
As bandeiras CLI aceitam durações humanas como`20m`, mas as chamadas de ferramentas usam milissegundos de época para`atMs`e`everyMs`(os calendários ISO são aceites para o`at`vezes).

## cron.add params

Uma imagem, tarefa principal da sessão (evento do sistema):

```json
{
  "name": "Reminder",
  "schedule": { "kind": "at", "atMs": 1738262400000 },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": { "kind": "systemEvent", "text": "Reminder text" },
  "deleteAfterRun": true
}
```

Trabalho recorrente e isolado com entrega:

```json
{
  "name": "Morning brief",
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "America/Los_Angeles" },
  "sessionTarget": "isolated",
  "wakeMode": "next-heartbeat",
  "payload": {
    "kind": "agentTurn",
    "message": "Summarize overnight updates.",
    "deliver": true,
    "channel": "slack",
    "to": "channel:C1234567890",
    "bestEffortDeliver": true
  },
  "isolation": { "postToMainPrefix": "Cron", "postToMainMode": "summary" }
}
```

Notas:

-`schedule.kind`:`at``atMs`,`every``everyMs` ou`cron``expr`, opcional`tz`.
-`atMs`e`everyMs`são milissegundos de época.
-`at`0 deve ser`at`1 ou`at`2 e corresponder ao`at`3.
- Domínios facultativos:`at`4,`at`5,`at`6,`at`7,`at`8.
-`at`9 é omitido em`atMs`0.

cron.update params

```json
{
  "jobId": "job-123",
  "patch": {
    "enabled": false,
    "schedule": { "kind": "every", "everyMs": 3600000 }
  }
}
```

Notas:

-`jobId`é canónico;`id`é aceite para compatibilidade.
- Utilize`agentId: null`no sistema para limpar a ligação do agente.

cron.run e cron.remove params

```json
{ "jobId": "job-123", "mode": "force" }
```

```json
{ "jobId": "job-123" }
```

## Armazenamento & histórico

- Loja de emprego:`~/.openclaw/cron/jobs.json`(JSON gerido pelo portal).
- Histórico de execução:`~/.openclaw/cron/runs/<jobId>.jsonl`(JSONL, auto-pruned).
- Sobrescrever o caminho da loja:`cron.store`em configuração.

Configuração

```json5
{
  cron: {
    enabled: true, // default true
    store: "~/.openclaw/cron/jobs.json",
    maxConcurrentRuns: 1, // default 1
  },
}
```

Desactivar o cron inteiramente:

-`cron.enabled: false`(configuração)
-`OPENCLAW_SKIP_CRON=1`(env)

## CLI faststart

Lembrete de um tiro (UTC ISO, auto- delete após o sucesso):

```bash
openclaw cron add \
  --name "Send reminder" \
  --at "2026-01-12T18:00:00Z" \
  --session main \
  --system-event "Reminder: submit expense report." \
  --wake now \
  --delete-after-run
```

Lembrete de um tiro (sessão principal, acorde imediatamente):

```bash
openclaw cron add \
  --name "Calendar check" \
  --at "20m" \
  --session main \
  --system-event "Next heartbeat: check calendar." \
  --wake now
```

Trabalho isolado recorrente (entrega ao WhatsApp):

```bash
openclaw cron add \
  --name "Morning status" \
  --cron "0 7 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Summarize inbox + calendar for today." \
  --deliver \
  --channel whatsapp \
  --to "+15551234567"
```

Trabalho isolado recorrente (entrega para um tópico Telegram):

```bash
openclaw cron add \
  --name "Nightly summary (topic)" \
  --cron "0 22 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Summarize today; send to the nightly topic." \
  --deliver \
  --channel telegram \
  --to "-1001234567890:topic:123"
```

Trabalho isolado com modelo e sobreposição de pensamento:

```bash
openclaw cron add \
  --name "Deep analysis" \
  --cron "0 6 * * 1" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Weekly deep analysis of project progress." \
  --model "opus" \
  --thinking high \
  --deliver \
  --channel whatsapp \
  --to "+15551234567"
```

Seleção do agente (configurações multiagentes):

```bash
# Pin a job to agent "ops" (falls back to default if that agent is missing)
openclaw cron add --name "Ops sweep" --cron "0 6 * * *" --session isolated --message "Check ops queue" --agent ops

# Switch or clear the agent on an existing job
openclaw cron edit <jobId> --agent ops
openclaw cron edit <jobId> --clear-agent
```

Execução manual (depuração):

```bash
openclaw cron run <jobId> --force
```

Editar uma tarefa existente (campos de patch):

```bash
openclaw cron edit <jobId> \
  --message "Updated prompt" \
  --model "opus" \
  --thinking low
```

Histórico de execução:

```bash
openclaw cron runs --id <jobId> --limit 50
```

Evento imediato do sistema sem criar um trabalho:

```bash
openclaw system event --mode now --text "Next heartbeat: check battery."
```

## Superfície API Gateway

-`cron.list`,`cron.status`,`cron.add`,`cron.update`,`cron.remove`-`cron.run`(força ou vencimento),`cron.runs`Para eventos imediatos do sistema sem trabalho, use `openclaw system event` /cli/system.

## Resolução de problemas

## Nada corre #

- O código de controlo está activado:`cron.enabled`e`OPENCLAW_SKIP_CRON`.
- Verifique se o Gateway está funcionando continuamente (cron corre dentro do processo Gateway).
- Para os esquemas`cron`: confirmar o fuso horário `--tz` versus o fuso horário da máquina.

### Telegrama entrega no lugar errado

- Para tópicos de fórum, use`-100…:topic:<id>`para que seja explícito e inequívoco.
- Se você ver prefixos`telegram:...`em logs ou alvos armazenados “última rota”, isso é normal;
cron entrega aceita-los e ainda analisar IDs tópicos corretamente.
