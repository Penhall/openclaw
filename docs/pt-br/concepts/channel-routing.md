---
summary: "Routing rules per channel (WhatsApp, Telegram, Discord, Slack) and shared context"
read_when:
  - Changing channel routing or inbox behavior
---

# Canais e roteamento

O OpenClaw responde **volta ao canal de onde veio uma mensagem**. A
modelo não escolhe um canal; roteamento é determinístico e controlado pela
configuração da máquina.

## Termos-chave

- **Canal**:`whatsapp`,`telegram`,`discord`,`slack`,`signal`,`imessage`,`webchat`.
- **AccountId**: instância de conta por canal (quando suportado).
- **AgentId**: um espaço de trabalho isolado + sessão (“cérebro”).
- **SessionKey**: a chave de balde usada para armazenar contexto e controlar a concorrência.

### Formas da chave da sessão (exemplos)

Mensagens diretas colapsam na sessão **main** do agente:

-`agent:<agentId>:<mainKey>`(por omissão:`agent:main:main`

Grupos e canais permanecem isolados por canal:

- Grupos`agent:<agentId>:<channel>:group:<id>`- Canais/quartos:`agent:<agentId>:<channel>:channel:<id>`

Tópicos:

- Os threads Slack/Discord anexam`:thread:<threadId>`à chave base.
- Tópicos do fórum do Telegram incorporar`:topic:<topicId>`na chave do grupo.

Exemplos:

-`agent:main:telegram:group:-1001234567890:topic:42`-`agent:main:discord:channel:123456:thread:987654`

## Regras de roteamento (como um agente é escolhido)

Escolhas de rota ** um agente** para cada mensagem de entrada:

1. **Exact peer match** `bindings`com`peer.kind`+`peer.id`.
2. ** Guild match** (Discord) via`guildId`.
3. **Team match** (Slack) via`teamId`.
4. ** Count match** `accountId`no canal).
5. **Channel match** (qualquer conta nesse canal).
6. **Agente padrão** `agents.list[].default`, outra entrada da primeira lista, retorno para`main`.

O agente combinado determina qual espaço de trabalho e armazenamento de sessão são usados.

## Grupos de transmissão (executar múltiplos agentes)

Grupos de transmissão permitem que você execute **multiple agents** para o mesmo peer ** quando OpenClaw normalmente responderia ** (por exemplo: em grupos WhatsApp, após o gating de menção/ativação).

Configuração:

```json5
{
  broadcast: {
    strategy: "parallel",
    "120363403215116621@g.us": ["alfred", "baerbel"],
    "+15555550123": ["support", "logger"],
  },
}
```

Ver: [Grupos de radiodifusão] /broadcast-groups.

## Visão geral da configuração

-`agents.list`: definições denominadas de agente (espaço de trabalho, modelo, etc.).
-`bindings`: mapear canais/contas/parceiros de entrada para agentes.

Exemplo:

```json5
{
  agents: {
    list: [{ id: "support", name: "Support", workspace: "~/.openclaw/workspace-support" }],
  },
  bindings: [
    { match: { channel: "slack", teamId: "T123" }, agentId: "support" },
    { match: { channel: "telegram", peer: { kind: "group", id: "-100123" } }, agentId: "support" },
  ],
}
```

## Armazenamento de sessão

Sessões armazenam ao vivo sob o diretório de estado (padrão`~/.openclaw`:

-`~/.openclaw/agents/<agentId>/sessions/sessions.json`As transcrições do JSONL vivem ao lado da loja.

Você pode substituir o caminho da loja via`session.store`e`{agentId}`templating.

## Comportamento do WebChat

WebChat se liga ao ** agente selecionado** e defaults ao principal do agente
sessão. Por causa disso, WebChat permite que você veja o contexto entre canais para que
Agente num só lugar.

## Responder contexto

As respostas de entrada incluem:

-`ReplyToId`,`ReplyToBody`e`ReplyToSender`quando disponíveis.
- O contexto citado é anexado ao`Body`como um bloco`[Replying to ...]`.

Isto é consistente em todos os canais.
