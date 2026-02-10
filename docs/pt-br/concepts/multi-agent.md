---
summary: "Multi-agent routing: isolated agents, channel accounts, and bindings"
title: Multi-Agent Routing
read_when: "You want multiple isolated agents (workspaces + auth) in one gateway process."
status: active
---

Roteamento Multi-Agente

Objetivo: múltiplos agentes  isolados  (espaço de trabalho separado + sessões`agentDir`+), além de múltiplas contas de canais (por exemplo, dois WhatsApps) em um Gateway em execução. A entrada é encaminhada para um agente através de ligações.

## O que é “um agente”?

Um agente** é um cérebro com o seu próprio escopo:

- ** Espaço de trabalho** (arquivos, AGENTS.md/SOUL.md/USER.md, notas locais, regras de persona).
- ** Diretório de estado** `agentDir` para perfis de autenticação, registro de modelo e configuração por agente.
- **Store de sessão** (história do chat + estado de roteamento) sob`~/.openclaw/agents/<agentId>/sessions`.

Perfis de autenticação são ** por agente**. Cada agente lê o seu próprio:

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

As credenciais do agente principal são **não** compartilhadas automaticamente. Nunca reutilize`agentDir`entre agentes (causa colisões de autenticação/sessão). Se queres partilhar créditos,
cópia`auth-profiles.json`para o`agentDir`do outro agente.

Habilidades são per-agente através da pasta`skills/`de cada espaço de trabalho, com habilidades compartilhadas
Disponível no`~/.openclaw/skills`. Ver [Competências: por agente vs. partilhado] /tools/skills#per-agent-vs-shared-skills.

O Gateway pode hospedar ** um agente** (padrão) ou ** muitos agentes** lado a lado.

** Nota do espaço de trabalho:** o espaço de trabalho de cada agente é o **default cwd**, não um duro
Caixa de areia. Caminhos relativos resolvem-se dentro do espaço de trabalho, mas caminhos absolutos podem
chegar a outros locais da máquina a menos que o sandboxing esteja activo. Ver
/gateway/sandboxing.

## Caminhos (mapa rápido)

- Configuração:`~/.openclaw/openclaw.json`(ou`OPENCLAW_CONFIG_PATH`
- Direcção-Geral:`~/.openclaw`(ou`OPENCLAW_STATE_DIR`
- Espaço de trabalho:`~/.openclaw/workspace`(ou`~/.openclaw/workspace-<agentId>`
-`~/.openclaw/agents/<agentId>/agent`(ou`agents.list[].agentDir`
- Sessões:`~/.openclaw/agents/<agentId>/sessions`

## # Modo de agente único (padrão)

Se não fizer nada, o Openclaw gere um único agente:

-`agentId`defaults to **`main`**.
- As sessões são marcadas como`agent:main:<mainKey>`.
- Normas de espaço de trabalho para`~/.openclaw/workspace`(ou`~/.openclaw/workspace-<profile>`quando o`OPENCLAW_PROFILE`é definido).
- Defaults estatais para`~/.openclaw/agents/main/agent`.

## Agente ajudante

Use o assistente de agente para adicionar um novo agente isolado:

```bash
openclaw agents add work
```

Em seguida, adicione`bindings`(ou deixe o assistente fazê-lo) para rotear mensagens de entrada.

Verificar com:

```bash
openclaw agents list --bindings
```

## Vários agentes = várias pessoas, múltiplas personalidades

Com ** vários agentes**, cada`agentId`torna-se uma ** persona totalmente isolada**:

- **Diferentes números de telefone/contas** (por canal`accountId`.
- **Diferentes personalidades** (arquivos de espaço de trabalho por agente como`AGENTS.md`e`SOUL.md`.
- **Separar auth + sessões** (sem conversa cruzada, a menos que explicitamente habilitado).

Isso permite que **Multiplas pessoas** compartilhem um servidor Gateway mantendo seus “cérebros” de IA e dados isolados.

## Um número WhatsApp, várias pessoas (DM dividido)

Você pode encaminhar **diferentes DMs WhatsApp** para diferentes agentes enquanto estiver em **uma conta WhatsApp**. Coincidir no remetente E.164 (como`+15551234567` com`peer.kind: "dm"`. As respostas ainda vêm do mesmo número do WhatsApp (sem identidade do remetente do agente).

Detalhes importantes: chats diretos colapsam na chave de sessão principal do agente**, então o verdadeiro isolamento requer ** um agente por pessoa**.

Exemplo:

```json5
{
  agents: {
    list: [
      { id: "alex", workspace: "~/.openclaw/workspace-alex" },
      { id: "mia", workspace: "~/.openclaw/workspace-mia" },
    ],
  },
  bindings: [
    { agentId: "alex", match: { channel: "whatsapp", peer: { kind: "dm", id: "+15551230001" } } },
    { agentId: "mia", match: { channel: "whatsapp", peer: { kind: "dm", id: "+15551230002" } } },
  ],
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551230001", "+15551230002"],
    },
  },
}
```

Notas:

- Controle de acesso ao DM é **global por conta do WhatsApp** (pairing/allowlist), não por agente.
- Para grupos partilhados, ligue o grupo a um agente ou utilize [Grupos de radiodifusão] /broadcast-groups.

## Regras de roteamento (como as mensagens escolhem um agente)

As ligações são **determinadas** e ** vitórias mais específicas**:

1.`peer`corresponde (DMT/grupo/id do canal)
2.`guildId`(Discórdia)
3.`teamId`(Slack)
4.`accountId`corresponde a um canal
5. correspondência de nível de canal `accountId: "*"`
6. backback ao agente padrão `agents.list[].default`, outra entrada primeira lista, padrão:`main`

## Várias contas / números de telefone

Canais que suportam ** contas múltiplas** (por exemplo, WhatsApp) usam`accountId`para identificar
Cada login. Cada`accountId`pode ser encaminhado para um agente diferente, então um servidor pode hospedar
vários números de telefone sem misturar sessões.

## Conceitos

-`agentId`: um “cérebro” (espaço de trabalho, autenticação por agente, armazenamento de sessão por agente).
-`accountId`: uma instância de conta de canal (por exemplo, conta WhatsApp`"personal"`vs`"biz"`.
-`binding`: encaminha as mensagens de entrada para um`agentId`por`(channel, accountId, peer)`e, opcionalmente, guild/team ids.
- As conversas directas colapsam para`agent:<agentId>:<mainKey>`(por agente “main”;`session.mainKey`.

## Exemplo: dois WhatsApps → dois agentes

`~/.openclaw/openclaw.json`(JSON5):

```js
{
  agents: {
    list: [
      {
        id: "home",
        default: true,
        name: "Home",
        workspace: "~/.openclaw/workspace-home",
        agentDir: "~/.openclaw/agents/home/agent",
      },
      {
        id: "work",
        name: "Work",
        workspace: "~/.openclaw/workspace-work",
        agentDir: "~/.openclaw/agents/work/agent",
      },
    ],
  },

  // Deterministic routing: first match wins (most-specific first).
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },

    // Optional per-peer override (example: send a specific group to work agent).
    {
      agentId: "work",
      match: {
        channel: "whatsapp",
        accountId: "personal",
        peer: { kind: "group", id: "1203630...@g.us" },
      },
    },
  ],

  // Off by default: agent-to-agent messaging must be explicitly enabled + allowlisted.
  tools: {
    agentToAgent: {
      enabled: false,
      allow: ["home", "work"],
    },
  },

  channels: {
    whatsapp: {
      accounts: {
        personal: {
          // Optional override. Default: ~/.openclaw/credentials/whatsapp/personal
          // authDir: "~/.openclaw/credentials/whatsapp/personal",
        },
        biz: {
          // Optional override. Default: ~/.openclaw/credentials/whatsapp/biz
          // authDir: "~/.openclaw/credentials/whatsapp/biz",
        },
      },
    },
  },
}
```

### Exemplo: WhatsApp bate-papo diário + Telegram trabalho profundo

Dividir por canal: encaminhar WhatsApp para um agente diário rápido e Telegram para um agente Opus.

```json5
{
  agents: {
    list: [
      {
        id: "chat",
        name: "Everyday",
        workspace: "~/.openclaw/workspace-chat",
        model: "anthropic/claude-sonnet-4-5",
      },
      {
        id: "opus",
        name: "Deep Work",
        workspace: "~/.openclaw/workspace-opus",
        model: "anthropic/claude-opus-4-5",
      },
    ],
  },
  bindings: [
    { agentId: "chat", match: { channel: "whatsapp" } },
    { agentId: "opus", match: { channel: "telegram" } },
  ],
}
```

Notas:

- Se tiver várias contas para um canal, adicione`accountId`à ligação (por exemplo,`{ channel: "whatsapp", accountId: "personal" }`.
- Para encaminhar um único DM/grupo para o Opus enquanto mantém o resto no chat, adicione uma ligação`match.peer`para esse par; as correspondências entre pares sempre vencem as regras do canal.

## Exemplo: mesmo canal, um par para Opus

Mantenha WhatsApp no agente rápido, mas roteie um DM para Opus:

```json5
{
  agents: {
    list: [
      {
        id: "chat",
        name: "Everyday",
        workspace: "~/.openclaw/workspace-chat",
        model: "anthropic/claude-sonnet-4-5",
      },
      {
        id: "opus",
        name: "Deep Work",
        workspace: "~/.openclaw/workspace-opus",
        model: "anthropic/claude-opus-4-5",
      },
    ],
  },
  bindings: [
    { agentId: "opus", match: { channel: "whatsapp", peer: { kind: "dm", id: "+15551234567" } } },
    { agentId: "chat", match: { channel: "whatsapp" } },
  ],
}
```

As ligações dos pares ganham sempre, por isso mantém-nas acima da regra do canal.

## Agente familiar ligado a um grupo WhatsApp

Prenda um agente familiar dedicado a um único grupo WhatsApp, com a menção gating
e uma política de ferramentas mais rigorosa:

```json5
{
  agents: {
    list: [
      {
        id: "family",
        name: "Family",
        workspace: "~/.openclaw/workspace-family",
        identity: { name: "Family Bot" },
        groupChat: {
          mentionPatterns: ["@family", "@familybot", "@Family Bot"],
        },
        sandbox: {
          mode: "all",
          scope: "agent",
        },
        tools: {
          allow: [
            "exec",
            "read",
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
          ],
          deny: ["write", "edit", "apply_patch", "browser", "canvas", "nodes", "cron"],
        },
      },
    ],
  },
  bindings: [
    {
      agentId: "family",
      match: {
        channel: "whatsapp",
        peer: { kind: "group", id: "120363999999999999@g.us" },
      },
    },
  ],
}
```

Notas:

- Listas de ferramentas são **tools**, não habilidades. Se uma habilidade precisa executar um
binário, garantir`exec`é permitido e o binário existe na caixa de areia.
- Para gating mais rigoroso, definir`agents.list[].groupChat.mentionPatterns`e manter
listas de permissões de grupo habilitadas para o canal.

## Por-Agente Sandbox e Configuração de Ferramenta

A partir de v2026.1.6, cada agente pode ter sua própria caixa de areia e restrições de ferramentas:

```js
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: {
          mode: "off",  // No sandbox for personal agent
        },
        // No tool restrictions - all tools available
      },
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: {
          mode: "all",     // Always sandboxed
          scope: "agent",  // One container per agent
          docker: {
            // Optional one-time setup after container creation
            setupCommand: "apt-get update && apt-get install -y git curl",
          },
        },
        tools: {
          allow: ["read"],                    // Only read tool
          deny: ["exec", "write", "edit", "apply_patch"],    // Deny others
        },
      },
    ],
  },
}
```

Nota:`setupCommand`vive sob`sandbox.docker`e funciona uma vez na criação de containers.
As sobreposições`sandbox.docker.*`por agente são ignoradas quando o escopo resolvido é`"shared"`.

** Benefícios:**

- ** Isolamento de segurança**: Restrinja ferramentas para agentes não confiáveis
- **Controlo de recursos**: Agentes específicos da Sandbox enquanto mantém os outros na máquina
- ** Políticas flexíveis**: Permissões diferentes por agente

Nota:`tools.elevated`é **global** e baseado no remetente; não é configurável por agente.
Se você precisar de limites por agente, use`agents.list[].tools`para negar`exec`.
Para segmentação de grupo, use`agents.list[].groupChat.mentionPatterns`para que @mentions mapeie de forma limpa para o agente pretendido.

Veja [Multi-Agent Sandbox & Tools] /multi-agent-sandbox-tools para exemplos detalhados.
