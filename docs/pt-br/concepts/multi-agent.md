---
summary: "Multi-agent routing: isolated agents, channel accounts, and bindings"
title: Multi-Agent Routing
read_when: "You want multiple isolated agents (workspaces + auth) in one gateway process."
status: active
---

Roteamento Multi-Agente

Objetivo: múltiplos agentes  isolados  (separar espaço de trabalho + <<CODE0>>+sessões), mais várias contas de canais (por exemplo, dois WhatsApps) em um Gateway em execução. A entrada é encaminhada para um agente através de ligações.

# # O que é “um agente”?

Um agente** é um cérebro com o seu próprio escopo:

- ** Espaço de trabalho** (arquivos, AGENTS.md/SOUL.md/USER.md, notas locais, regras de persona).
- ** Diretório de estado** (<<<CODE0>>) para perfis de autenticação, registro de modelo e configuração por agente.
- ** Armazenagem de sessão** (história do chat + estado de roteamento) em <<CODE1>>>.

Perfis de autenticação são ** por agente**. Cada agente lê o seu próprio:

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

As credenciais do agente principal são **não** compartilhadas automaticamente. Nunca reutilize <<CODE0>>
entre agentes (causa colisões de autenticação/sessão). Se queres partilhar créditos,
cópia <<CODE1>> para o outro agente <<CODE2>>>.

Habilidades são per-agente através da pasta <<CODE0>> de cada espaço de trabalho, com habilidades compartilhadas
disponível em <<CODE1>>>>. Ver [Competências: por agente vs partilhado] (<<<LINK0>>>).

O Gateway pode hospedar ** um agente** (padrão) ou ** muitos agentes** lado a lado.

** Nota do espaço de trabalho:** o espaço de trabalho de cada agente é o **default cwd**, não um duro
Caixa de areia. Caminhos relativos resolvem-se dentro do espaço de trabalho, mas caminhos absolutos podem
chegar a outros locais da máquina a menos que o sandboxing esteja activo. Ver
[Sandboxing] (<<<LINK0>>>).

# # Caminhos (mapa rápido)

- Configuração: <<CODE0>> (ou <<CODE1>>)
- Dir Estado: <<CODE2>> (ou <<CODE3>>>)
- Espaço de trabalho: <<CODE4>> (ou <<CODE5>>)
- Dir agente: <<CODE6>> (ou <<CODE7>>>)
- Sessões: <<CODE8>>

## # Modo de agente único (padrão)

Se não fizer nada, o Openclaw gere um único agente:

- <<CODE0> por omissão para **<<CODE1>**.
- As sessões são definidas como <<CODE2>>>.
- Padrão do espaço de trabalho para <<CODE3>> (ou <<CODE4>> quando <<CODE5> é definido).
- O padrão do estado é <<CODE6>>>>.

# # Agente ajudante

Use o assistente de agente para adicionar um novo agente isolado:

```bash
openclaw agents add work
```

Em seguida, adicione <<CODE0>> (ou deixe o assistente fazê-lo) para rotear mensagens de entrada.

Verificar com:

```bash
openclaw agents list --bindings
```

# # Vários agentes = várias pessoas, múltiplas personalidades

Com ** vários agentes**, cada <<CODE0>> torna-se uma ** persona totalmente isolada**:

- **Diferentes números de telefone/contas** (por canal <<CODE0>>>).
- **Diferentes personalidades** (arquivos de espaço de trabalho por agente como <<CODE1>> e <<CODE2>>>).
- **Separar auth + sessões** (sem conversa cruzada, a menos que explicitamente habilitado).

Isso permite que **Multiplas pessoas** compartilhem um servidor Gateway mantendo seus “cérebros” de IA e dados isolados.

# # Um número WhatsApp, várias pessoas (DM dividido)

Você pode encaminhar **diferentes DMs WhatsApp** para diferentes agentes enquanto permanece em **uma conta WhatsApp**. Combine no remetente E.164 (como <<CODE0>>) com <<CODE1>>. As respostas ainda vêm do mesmo número do WhatsApp (sem identidade do remetente do agente).

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
- Para grupos partilhados, ligar o grupo a um agente ou utilizar [Grupos de radiodifusão](<<<LINK0>>>).

# # Regras de roteamento (como as mensagens escolhem um agente)

As ligações são **determinadas** e ** vitórias mais específicas**:

1. <<CODE0>> correspondência (DMT/grupo/id do canal)
2. <<CODE1>> (Discórdia)
3. <<CODE2>> (Slack)
4. <<CODE3> corresponde a um canal
5. correspondência de nível de canal (<<<CODE4>>)
6. retorno ao agente padrão (<<<CODE5>, outra primeira entrada na lista, padrão: <<CODE6>>)

# # Várias contas / números de telefone

Canais que suportam ** várias contas** (por exemplo, WhatsApp) usam <<CODE0>> para identificar
Cada login. Cada <<CODE1> pode ser encaminhado para um agente diferente, então um servidor pode hospedar
vários números de telefone sem misturar sessões.

# # Conceitos

- <<CODE0>>: um “cérebro” (espaço de trabalho, autenticação por agente, armazenamento de sessão por agente).
- <<CODE1>>: uma instância de conta de canal (por exemplo, conta WhatsApp <<CODE2>> vs <<CODE3>>).
- <<CODE4>>: encaminha mensagens de entrada para uma <<CODE5>> por <<CODE6>> e opcionalmente guild/team ids.
- Conversas directas colapsam para <<CODE7>> (por agente “principal”; <<CODE8>>).

# # Exemplo: dois WhatsApps → dois agentes

<<CODE0> (JSON5):

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

# # # Exemplo: WhatsApp bate-papo diário + Telegram trabalho profundo

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

- Se tiver várias contas para um canal, adicione <<CODE0>>> à ligação (por exemplo <<CODE1>>).
- Para encaminhar um único DM/grupo para o Opus enquanto mantém o resto no chat, adicione uma ligação <<CODE2>> para esse par; correspondências por pares sempre vencem regras de todo o canal.

# # Exemplo: mesmo canal, um par para Opus

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

# # Agente familiar ligado a um grupo WhatsApp

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
binário, garantir <<CODE0>> é permitido e o binário existe na caixa de areia.
- Para gating mais rigoroso, definir <<CODE1>>> e manter
listas de permissões de grupo habilitadas para o canal.

# # Por-Agente Sandbox e Configuração de Ferramenta

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

Nota: <<CODE0>> vive em <<CODE1>> e é executado uma vez na criação do recipiente.
As substituições por agente <<CODE2>> são ignoradas quando o escopo resolvido é <<CODE3>>>.

** Benefícios:**

- ** Isolamento de segurança**: Restrinja ferramentas para agentes não confiáveis
- **Controlo de recursos**: Agentes específicos da Sandbox enquanto mantém os outros na máquina
- ** Políticas flexíveis**: Permissões diferentes por agente

Nota: <<CODE0> é **global** e baseado no remetente; não é configurável por agente.
Se precisar de limites por agente, utilize <<CODE1>> para negar <<CODE2>>.
Para segmentação de grupo, use <<CODE3> assim @mementions mapeia limpa para o agente pretendido.

Veja [Multi-Agent Sandbox & Tools](<<<LINK0>>>) para exemplos detalhados.
