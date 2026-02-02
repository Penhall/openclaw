---
summary: "Group chat behavior across surfaces (WhatsApp/Telegram/Discord/Slack/Signal/iMessage/Microsoft Teams)"
read_when:
  - Changing group chat behavior or mention gating
---

Grupos

OpenClaw trata bate-papos de grupo de forma consistente em superfícies: WhatsApp, Telegram, Discord, Slack, Signal, iMessage, Microsoft Teams.

# # Iniciante introdução (2 minutos)

OpenClaw “vive” em suas próprias contas de mensagens. Não há nenhum usuário de bot WhatsApp separado.
Se **você** está em um grupo, OpenClaw pode ver esse grupo e responder lá.

Comportamento padrão:

- Os grupos são restritos (<<<CODE0>>>).
- Respostas exigem uma menção, a menos que você desactiva explicitamente a menção gating.

Tradução: remetentes autorizados podem ativar OpenClaw mencionando-o.

> TL;DR
>
> - **O acesso ao DM** é controlado por <<CODE0>>.
> - **O acesso do grupo** é controlado por <<CODE1>> + allowlists (<<CODE2>>, <<CODE3>>).
> - ** O desencadeamento da resposta** é controlado pela menção gating (<<<CODE4>>, <<CODE5>>).

Fluxo rápido (o que acontece com uma mensagem de grupo):

```
groupPolicy? disabled -> drop
groupPolicy? allowlist -> group allowed? no -> drop
requireMention? yes -> mentioned? no -> store for context only
otherwise -> reply
```

[Fluxo da mensagem do grupo] (<<<LINK0>>>)

Se quiseres...
Objetivo O que definir
----------------------
□ Permitir que todos os grupos, mas apenas resposta em @mentions <<CODE0>
Não desactivar todas as respostas do grupo
Apenas grupos específicos (sem <<CODE3>> chave)
Apenas você pode disparar em grupos .. <<<CODE4>>, <<CODE5>>

# # Chaves de sessão

- Sessões em grupo usam chaves de sessão <<CODE0>> (quartos/canais usam <<CODE1>>).
- Tópicos do fórum do Telegram adicionam <<CODE2>> ao ID do grupo para que cada tópico tenha sua própria sessão.
- Conversas diretas usam a sessão principal (ou por mensagem, se configurada).
- Os batimentos cardíacos são ignorados.

## Padrão: DM pessoais + grupos públicos (agente único)

Sim — isto funciona bem se o seu tráfego “pessoal” for **DMs** e o seu tráfego “público” for **groups**.

Por que: no modo monoagente, os DMs normalmente pousam na chave de sessão **main** (<<<CODE0>>), enquanto os grupos usam sempre as teclas de sessão **non-main** (<<CODE1>>>). Se você habilitar sandboxing com <<CODE2>>, essas sessões de grupo são executadas no Docker enquanto sua sessão principal de DM permanece no host.

Isso lhe dá um agente “cérebro” (espaço de trabalho compartilhado + memória), mas duas posturas de execução:

- **DMs**: ferramentas completas (host)
- **Grupos**: sandbox + ferramentas restritas (Docker)

> Se você precisar de espaços de trabalho/pessoas verdadeiramente separados (“pessoal” e “público” nunca deve misturar), use um segundo agente + vinculações. Ver [Roteamento Multi-Agente] (<<<LINK0>>>).

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

Quer “grupos só podem ver a pasta X” em vez de “sem acesso ao host”? Manter <<CODE0>> e montar apenas caminhos listados na área de areia:

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

- Chaves de configuração e predefinições: [Configuração do portal] (<<<LINK0>>)
- Depurando por que uma ferramenta é bloqueada: [Sandbox vs Tool Policy vs Elevated](<<LINK1>>>)
- Detalhes das montagens de ligação: [Sandboxing] (<<<LINK2>>)

# # Mostrar rótulos

- As etiquetas de UI utilizam <<CODE0> quando disponíveis, formatadas como <<CODE1>>>.
- <<CODE2> está reservado para salas/canais; chats em grupo <<CODE3> (em minúsculas, espaços -> <<CODE4>>, manter <<CODE5>>).

# # Política do grupo

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
* <<CODE0>> * Grupos de allowlists de bypass; ainda se aplica a listagem.
<<CODE1>> Bloquear todas as mensagens de grupo inteiramente.
<<CODE2>> Apenas permite grupos/quartos que correspondam à lista de permissões configurada. □

Notas:

- <<CODE0> é separado de mencione-gating (que requer @mentions).
- WhatsApp/Telegram/Signal/iMessage/Microsoft Teams: use <<CODE1>> (fallback: explícito <<CODE2>>).
- Discórdia: allowlist usa <<CODE3>>>>.
- Slack: allowlist utiliza <<CODE4>>>.
- Matrix: allowlist usa <<CODE5>> (Identificações de quarto, apelidos ou nomes). Use <<CODE6>> para restringir os remetentes; por sala <<CODE7> também são suportadas listas de permissões.
- Os DM do grupo são controlados separadamente (<<<<CODE8>>, <<CODE9>>>).
- Telegram allowlist pode combinar IDs de usuário (<<<CODE10>>>, <<CODE11>>, <<CODE12>>>) ou nomes de usuário (<<CODE13>> ou <<CODE14>>>>); prefixos são insensíveis a casos.
- O padrão é <<CODE15>>>; se sua lista de allowlist do grupo estiver vazia, as mensagens do grupo são bloqueadas.

Modelo mental rápido (ordem de avaliação para mensagens de grupo):

1. <<CODE0>> (aberto/desactivado/lista autorizada)
2. lista de autorizações de grupo (<<<CODE1>>, <<CODE2>>, lista de autorizações específicas de canal)
3. mencionar gating (<<<CODE3>>, <<CODE4>>)

# # Mencionar gating (padrão)

As mensagens de grupo requerem uma menção, a menos que seja anulada por grupo. Os padrões vivem por subsistema em <<CODE0>>>.

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

- <<CODE0> são regexes sensíveis ao caso.
- Superfícies que fornecem menções explícitas ainda passam; padrões são um recuo.
- Substituição por agente: <<CODE1>> (útil quando múltiplos agentes compartilham um grupo).
- Mention gating só é aplicado quando a detecção de menção é possível (menções nativas ou <<CODE2>> são configurados).
- Os padrões de discórdia vivem em <<CODE3>> (superável por guild/canal).
- O contexto do histórico do grupo é envolto uniformemente em todos os canais e é ** (mensagens ignoradas devido à menção gating); use <<CODE4>> para o padrão global e <<CODE5>> (ou <<CODE6>>>) para sobreposições. Definir <<CODE7>> para desativar.

# # Restrições de ferramentas de grupo/canal (opcional)

Alguns canais configuram suporte restringindo quais ferramentas estão disponíveis **dentro de um grupo específico / sala / canal**.

- <<CODE0>>: permitir/negar ferramentas para todo o grupo.
- <<CODE1>>: substituições por sender dentro do grupo (chaves são IDs remetentes/nomes de usuário/email/números de telefone dependendo do canal). Utilizar <<CODE2>> como uma carta.

Ordem de resolução (vencimentos mais específicos):

1. grupo/canal <<CODE0>> correspondência
2. grupo/canal <<CODE1>>>
3. padrão (<<<CODE2>>) <<CODE3>> correspondência
4. padrão (<<<CODE4>>>) <<CODE5>>

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
- Alguns canais usam ninhos diferentes para salas/canais (por exemplo, Discórdia <<CODE0>>, Slack <<CODE1>>, Equipes MS <<CODE2>>>).

# # Listas de licenças de grupo

Quando <<CODE0>>, <<CODE1>>, ou <<CODE2>> é configurado, as chaves atuam como uma lista de allowlists de grupo. Use <<CODE3> para permitir todos os grupos enquanto ainda define o comportamento padrão de menção.

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

# # Ativação (somente proprietário)

Os proprietários do grupo podem alternar a ativação por grupo:

- <<CODE0>>
- <<CODE1>>

O proprietário é determinado por <<CODE0>> (ou pelo próprio robô E.164 quando desligado). Envie o comando como uma mensagem independente. Outras superfícies ignoram atualmente <<CODE1>>>>.

# # Campos de contexto

Conjunto de cargas de entrada do grupo:

- <<CODE0>>
- <<CODE1>> (se conhecido)
- <<CODE2>> (se conhecido)
- <<CODE3>
- Os tópicos do fórum de telegramas também incluem <<CODE4>> e <<CODE5>>.

O prompt do sistema do agente inclui uma introdução do grupo na primeira volta de uma nova sessão do grupo. Ele lembra o modelo para responder como um humano, evitar tabelas Markdown, e evitar digitar sequências literais <<CODE0>>.

# # iMensagem específica

- Preferir <<CODE0>> quando roteamento ou allowlisting.
- Listar chats: <<CODE1>>>.
- Respostas de grupo sempre voltar para o mesmo <<CODE2>>.

# # WhatsApp especifica

Veja [Mensagens do grupo](<<<LINK0>>) para o comportamento somente do WhatsApp (injeção histórica, mencionar detalhes do manuseio).
