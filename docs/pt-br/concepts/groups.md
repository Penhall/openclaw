---
summary: "Group chat behavior across surfaces (WhatsApp/Telegram/Discord/Slack/Signal/iMessage/Microsoft Teams)"
read_when:
  - Changing group chat behavior or mention gating
---

Grupos

OpenClaw trata bate-papos de grupo de forma consistente em superfícies: WhatsApp, Telegram, Discord, Slack, Signal, iMessage, Microsoft Teams.

## Iniciante introdução (2 minutos)

OpenClaw “vive” em suas próprias contas de mensagens. Não há nenhum usuário de bot WhatsApp separado.
Se **você** está em um grupo, OpenClaw pode ver esse grupo e responder lá.

Comportamento padrão:

- Os grupos são restritos `groupPolicy: "allowlist"`.
- Respostas exigem uma menção, a menos que você desactiva explicitamente a menção gating.

Tradução: remetentes autorizados podem ativar OpenClaw mencionando-o.

> TL;DR
>
> - **O acesso DM** é controlado pelo`*.allowFrom`.
> - **O acesso do grupo** é controlado por`*.groupPolicy`+ allowlists `*.groups`,`*.groupAllowFrom`.
> - ** O desencadeamento da resposta** é controlado pela menção gating `requireMention`,`/activation`.

Fluxo rápido (o que acontece com uma mensagem de grupo):

```
groupPolicy? disabled -> drop
groupPolicy? allowlist -> group allowed? no -> drop
requireMention? yes -> mentioned? no -> store for context only
otherwise -> reply
```

! [Fluxo da mensagem do grupo] /images/groups-flow.svg

Se quiseres...
Objetivo O que definir
----------------------
□ Permitir que todos os grupos, mas apenas resposta em @mentions
OUTXCODE1
OUTXCODE2 (sem chave`"*"`
Apenas você pode acionar em grupos`groupPolicy: "allowlist"`,`groupAllowFrom: ["+1555..."]`

## Chaves de sessão

- Sessões de grupo usam chaves de sessão`agent:<agentId>:<channel>:group:<id>`(quartos/canais usam`agent:<agentId>:<channel>:channel:<id>`.
- Os tópicos do fórum do Telegram adicionam`:topic:<threadId>`ao ID do grupo para que cada tópico tenha sua própria sessão.
- Conversas diretas usam a sessão principal (ou por mensagem, se configurada).
- Os batimentos cardíacos são ignorados.

## Padrão: DM pessoais + grupos públicos (agente único)

Sim — isto funciona bem se o seu tráfego “pessoal” for **DMs** e o seu tráfego “público” for **groups**.

Por que: no modo monoagente, os DMs normalmente aterram na chave de sessão **main** `agent:main:main`, enquanto os grupos sempre usam **non-main** session keys `agent:main:<channel>:group:<id>`. Se você habilitar sandboxing com`mode: "non-main"`, essas sessões de grupo são executadas no Docker enquanto sua sessão principal de DM permanece no host.

Isso lhe dá um agente “cérebro” (espaço de trabalho compartilhado + memória), mas duas posturas de execução:

- **DMs**: ferramentas completas (host)
- **Grupos**: sandbox + ferramentas restritas (Docker)

> Se você precisar de espaços de trabalho/pessoas verdadeiramente separados (“pessoal” e “público” nunca deve misturar), use um segundo agente + vinculações. Ver [Roteamento Multi-Agente] /concepts/multi-agent.

Exemplo (DMs no host, grupos sandboxed + ferramentas somente de mensagens):

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main", // groups/channels are non-main -> sandboxed
        scope: "session", // strongest isolation (one container per group/channel)
        workspaceAccess: "none",
      },
    },
  },
  tools: {
    sandbox: {
      tools: {
        // If allow is non-empty, everything else is blocked (deny still wins).
        allow: ["group:messaging", "group:sessions"],
        deny: ["group:runtime", "group:fs", "group:ui", "nodes", "cron", "gateway"],
      },
    },
  },
}
```

Quer “grupos só podem ver a pasta X” em vez de “sem acesso ao host”? Manter`workspaceAccess: "none"`e montar apenas caminhos listados na área de areia:

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        scope: "session",
        workspaceAccess: "none",
        docker: {
          binds: [
            // hostPath:containerPath:mode
            "~/FriendsShared:/data:ro",
          ],
        },
      },
    },
  },
}
```

Relacionados:

- Chaves de configuração e predefinições: [Configuração do portal] /gateway/configuration#agentsdefaultssandbox
- Depurando por que uma ferramenta é bloqueada: [Sandbox vs Tool Policy vs Elevated] /gateway/sandbox-vs-tool-policy-vs-elevated
- Detalhes das montagens da ligação: [Sandboxing] /gateway/sandboxing#custom-bind-mounts

## Mostrar rótulos

- As etiquetas UI usam`displayName`quando disponíveis, formatadas como`<channel>:<token>`.
-`#room`está reservado para salas/canais; chats de grupo usam`g-<slug>`(inferior, espaços ->`-`, manter`#@+._-`.

## Política do grupo

Controle como as mensagens de grupo/quarto são tratadas por canal:

```json5
{
  channels: {
    whatsapp: {
      groupPolicy: "disabled", // "open" | "disabled" | "allowlist"
      groupAllowFrom: ["+15551234567"],
    },
    telegram: {
      groupPolicy: "disabled",
      groupAllowFrom: ["123456789", "@username"],
    },
    signal: {
      groupPolicy: "disabled",
      groupAllowFrom: ["+15551234567"],
    },
    imessage: {
      groupPolicy: "disabled",
      groupAllowFrom: ["chat_id:123"],
    },
    msteams: {
      groupPolicy: "disabled",
      groupAllowFrom: ["user@org.com"],
    },
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        GUILD_ID: { channels: { help: { allow: true } } },
      },
    },
    slack: {
      groupPolicy: "allowlist",
      channels: { "#general": { allow: true } },
    },
    matrix: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["@owner:example.org"],
      groups: {
        "!roomId:example.org": { allow: true },
        "#alias:example.org": { allow: true },
      },
    },
  },
}
```

□ Política
-----------------------------------------------------------------------------------------------
*`"open"`* Groups bypass allowlists; mencionando- gating ainda se aplica.
Bloquear todas as mensagens de grupo inteiramente.
Apenas permitir grupos/quartos que correspondam à lista de permissões configurada. □

Notas:

-`groupPolicy`é separado da citação-gating (que requer @ menções).
- WhatsApp/Telegram/Sinal/iMessage/Microsoft Teams: use`groupAllowFrom`(fallback: explícito`allowFrom`.
- Discórdia: lista de permissão usa`channels.discord.guilds.<id>.channels`.
- Slack: a lista de licenças utiliza`channels.slack.channels`.
- Matrix: a lista de allowlist utiliza`channels.matrix.groups`(IDs de quarto, apelidos ou nomes). Use`channels.matrix.groupAllowFrom`para restringir os remetentes; por quarto`users`allowlists também são suportados.
- Os DM do grupo são controlados separadamente `channels.discord.dm.*`,`channels.slack.dm.*`.
- Telegram allowlist pode combinar IDs de usuário `groupAllowFrom`0,`groupAllowFrom`1,`groupAllowFrom`2) ou nomes de usuário `groupAllowFrom`3 ou`groupAllowFrom`4); prefixos são insensíveis a casos.
- O padrão é`groupAllowFrom`5; se sua lista de allowlist do grupo estiver vazia, as mensagens do grupo serão bloqueadas.

Modelo mental rápido (ordem de avaliação para mensagens de grupo):

1.`groupPolicy`(aberto/desactivado/lista autorizada)
2. Listas de licenças de grupo `*.groups`,`*.groupAllowFrom`, lista de autorizações específicas do canal)
3. Mencionar o jating `requireMention`,`/activation`

## Mencionar gating (padrão)

As mensagens de grupo requerem uma menção, a menos que seja anulada por grupo. As predefinições vivem por subsistema ao abrigo do`*.groups."*"`.

Responder a uma mensagem bot conta como uma menção implícita (quando o canal suporta metadados de resposta). Isso se aplica ao Telegram, WhatsApp, Slack, Discord e Microsoft Teams.

```json5
{
  channels: {
    whatsapp: {
      groups: {
        "*": { requireMention: true },
        "123@g.us": { requireMention: false },
      },
    },
    telegram: {
      groups: {
        "*": { requireMention: true },
        "123456789": { requireMention: false },
      },
    },
    imessage: {
      groups: {
        "*": { requireMention: true },
        "123": { requireMention: false },
      },
    },
  },
  agents: {
    list: [
      {
        id: "main",
        groupChat: {
          mentionPatterns: ["@openclaw", "openclaw", "\\+15555550123"],
          historyLimit: 50,
        },
      },
    ],
  },
}
```

Notas:

-`mentionPatterns`são regexes sensíveis a casos.
- Superfícies que fornecem menções explícitas ainda passam; padrões são um recuo.
- Substituição por agente:`agents.list[].groupChat.mentionPatterns`(útil quando vários agentes compartilham um grupo).
- Mention gating só é aplicado quando a detecção de menção é possível (menções nativas ou`mentionPatterns`são configurados).
- Discord defaults live in`channels.discord.guilds."*"`(superável por guild/canal).
- O contexto do histórico do grupo é envolto uniformemente em todos os canais e é ** somente para gastos** (mensagens ignoradas devido à menção gating); use`messages.groupChat.historyLimit`para o padrão global e`channels.<channel>.historyLimit`(ou`channels.<channel>.accounts.*.historyLimit` para sobreposições. Defina`0`para desabilitar.

## Restrições de ferramentas de grupo/canal (opcional)

Alguns canais configuram suporte restringindo quais ferramentas estão disponíveis **dentro de um grupo específico / sala / canal**.

-`tools`: permitir/negar ferramentas para todo o grupo.
-`toolsBySender`: substitui por sender dentro do grupo (chaves são IDs remetentes/nomes de usuário/e-mails/números de telefone dependendo do canal). Use`"*"`como um wildcard.

Ordem de resolução (vencimentos mais específicos):

1. grupo/canal`toolsBySender`2. Grupo/canal`tools`3. por omissão `"*"``toolsBySender`match
4. por omissão `"*"``tools`

Exemplo (Telegrama):

```json5
{
  channels: {
    telegram: {
      groups: {
        "*": { tools: { deny: ["exec"] } },
        "-1001234567890": {
          tools: { deny: ["exec", "read", "write"] },
          toolsBySender: {
            "123456789": { alsoAllow: ["exec"] },
          },
        },
      },
    },
  },
}
```

Notas:

- Restrições de ferramentas de grupo/canal são aplicadas além da política global/agente (deny ainda vence).
- Alguns canais usam ninhos diferentes para salas/canais (por exemplo, Discord`guilds.*.channels.*`, Slack`channels.*`, MS Teams`teams.*.channels.*`.

## Listas de licenças de grupo

Quando`channels.whatsapp.groups`,`channels.telegram.groups`ou`channels.imessage.groups`é configurado, as chaves agem como uma lista de allowlist de grupo. Use`"*"`para permitir todos os grupos enquanto ainda define o comportamento padrão de menção.

Intenções comuns (cópia/cola):

1. Desactivar todas as respostas do grupo

```json5
{
  channels: { whatsapp: { groupPolicy: "disabled" } },
}
```

2. Permitir apenas grupos específicos (WhatsApp)

```json5
{
  channels: {
    whatsapp: {
      groups: {
        "123@g.us": { requireMention: true },
        "456@g.us": { requireMention: false },
      },
    },
  },
}
```

3. Permitir todos os grupos, mas exigir menção (explicit)

```json5
{
  channels: {
    whatsapp: {
      groups: { "*": { requireMention: true } },
    },
  },
}
```

4. Somente o proprietário pode acionar em grupos (WhatsApp)

```json5
{
  channels: {
    whatsapp: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
      groups: { "*": { requireMention: true } },
    },
  },
}
```

## Ativação (somente proprietário)

Os proprietários do grupo podem alternar a ativação por grupo:

-`/activation mention`-`/activation always`

O proprietário é determinado pelo`channels.whatsapp.allowFrom`(ou pelo próprio robô E.164 quando desactivado). Envie o comando como uma mensagem independente. Outras superfícies atualmente ignoram`/activation`.

## Campos de contexto

Conjunto de cargas de entrada do grupo:

-`ChatType=group`-`GroupSubject`(se conhecido)
-`GroupMembers`(se conhecido)
-`WasMentioned`(resultado da medição)
- Os temas do fórum de telegramas incluem também`MessageThreadId`e`IsForum`.

O prompt do sistema do agente inclui uma introdução do grupo na primeira volta de uma nova sessão do grupo. Ele lembra o modelo para responder como um humano, evitar tabelas Markdown, e evitar digitar sequências`
`literal.

## iMensagem específica

- Preferir`chat_id:<id>`quando rotear ou permitir listar.
- Conversas de lista:`imsg chats --limit 20`.
- As respostas do grupo voltam sempre para o mesmo`chat_id`.

## WhatsApp especifica

Ver [Mensagens do grupo]/concepts/group-messages para o comportamento WhatsApp-only (injeção histórica, mencionar detalhes de manipulação).
