---
summary: "Slack setup for socket or HTTP webhook mode"
read_when: "Setting up Slack or debugging Slack socket/HTTP mode"
---

# Slack

## Modo de soquete (padrão)

Configuração rápida (início)

1. Crie um aplicativo Slack e habilite **Socket Mode**.
2. Crie um Token ** `xapp-...` e ** Bot Token ** `xoxb-...`.
3. Definir tokens para OpenClaw e iniciar o gateway.

Configuração mínima:

```json5
{
  channels: {
    slack: {
      enabled: true,
      appToken: "xapp-...",
      botToken: "xoxb-...",
    },
  },
}
```

Configuração

1. Criar um aplicativo Slack (Do zero) em https://api.slack.com/apps.
2. **Socket Mode** → alternância. Em seguida, vá para ** Informações Básicas** → ** Tokens de Nível de App** → ** Token e Scopes Generate** com escopo`connections:write`. Copie o **App Token** `xapp-...`.
3. **OAuth & Permissões** → adicionar escopos de token bot (use o manifesto abaixo). Clique em **Instalar para o Espaço de Trabalho**. Copie o **Bot User OAuth Token** `xoxb-...`.
4. Opcional: **OAuth & Permissões** → adicionar **User Token Scopes** (veja a lista somente de leitura abaixo). Reinstale o aplicativo e copie o **User OAuth Token** `xoxp-...`.
5. **As assinaturas de eventos** → permitem eventos e assinam:
-`message.*`(inclui edições/exclusões/transmissões de fio)
-`app_mention`-`reaction_added`,`reaction_removed`-`member_joined_channel`,`member_left_channel`-`xapp-...`0
-`xapp-...`1,`xapp-...`2
6. Convide o bot para canais que você quer que ele leia.
7. Comandos Slash → criar`xapp-...`3 se você usar`xapp-...`4. Se você habilitar comandos nativos, adicione um comando slash por comando embutido (os mesmos nomes que`xapp-...`5). O padrão nativo está desligado para o Slack a menos que você defina`xapp-...`6 (global`xapp-...`7 é`xapp-...`8 que deixa o Slack desligado).
8. App Home → habilite a aba **Mensagens** para que os usuários possam DM o bot.

Use o manifesto abaixo para que os escopos e eventos permaneçam em sincronia.

Suporte multi-conta: use`channels.slack.accounts`com fichas por conta e opcional`name`. Ver `gateway/configuration`/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts para o padrão partilhado.

### Configuração do OpenClaw (mínimo)

Definir os tokens via env vars (recomendado):

-`SLACK_APP_TOKEN=xapp-...`-`SLACK_BOT_TOKEN=xoxb-...`

Ou através da configuração:

```json5
{
  channels: {
    slack: {
      enabled: true,
      appToken: "xapp-...",
      botToken: "xoxb-...",
    },
  },
}
```

## # Token do usuário (opcional)

Openclaw pode usar um token de usuário Slack `xoxp-...` para operações de leitura (história,
pinos, reações, emoji, informação do membro). Por padrão, isto permanece somente leitura: lê
prefere o token do usuário quando presente, e escreve ainda usar o token do bot a menos que
Você opta explicitamente por entrar. Mesmo com`userTokenReadOnly: false`, o símbolo de bot permanece
preferido para escrever quando estiver disponível.

Os tokens do usuário estão configurados no arquivo de configuração (sem suporte ao env var). Para
multi-conta, definir`channels.slack.accounts.<id>.userToken`.

Exemplo com bot + app + tokens de usuário:

```json5
{
  channels: {
    slack: {
      enabled: true,
      appToken: "xapp-...",
      botToken: "xoxb-...",
      userToken: "xoxp-...",
    },
  },
}
```

Exemplo com userTokenReadSomente explicitamente definido (permitir que o usuário escreva):

```json5
{
  channels: {
    slack: {
      enabled: true,
      appToken: "xapp-...",
      botToken: "xoxb-...",
      userToken: "xoxp-...",
      userTokenReadOnly: false,
    },
  },
}
```

Uso do token

- Operações de leitura (história, lista de reações, lista de pinos, lista de emojis, informação de membro,
busca) prefere o token do usuário quando configurado, caso contrário o token do bot.
- Gravar operações (enviar/editar/eliminar mensagens, adicionar/remover reacções, pin/unpin,
uploads de arquivos) use o token bot por padrão. Se`userTokenReadOnly: false`e
nenhum token de bot está disponível, OpenClaw cai de volta para o token de usuário.

## # Contexto histórico

-`channels.slack.historyLimit`(ou`channels.slack.accounts.*.historyLimit` controla quantas mensagens recentes de canal/grupo estão envolvidas no prompt.
- Regressa ao`messages.groupChat.historyLimit`. Definir`0`para desabilitar (padrão 50).

## Modo HTTP (A API dos eventos)

Use o modo HTTP webhook quando seu Gateway for acessível por Slack sobre HTTPS (típico para implantações de servidores).
O modo HTTP usa a API Eventos + Interatividade + Comandos Slash com uma URL de solicitação compartilhada.

Configuração

1. Crie um aplicativo Slack e **desativar o modo Socket** (opcional se você só usar HTTP).
2. ** Informações básicas** → copiar o **Signing Secret**.
3. **OAuth & Permissões** → instale o aplicativo e copie o **Bot User OAuth Token** `xoxb-...`.
4. **As Assinaturas de eventos** → ativam os eventos e definem o URL de solicitação** para o seu caminho webhook gateway (padrão`/slack/events`.
5. **Interatividade & Atalhos** → activar e definir o mesmo ** Pedir URL**.
6. ** Comandos Slash** → definir o mesmo ** Pedir URL** para seus comandos.

URL de pedido de exemplo:`https://gateway-host/slack/events`

### Configuração do OpenClaw (mínimo)

```json5
{
  channels: {
    slack: {
      enabled: true,
      mode: "http",
      botToken: "xoxb-...",
      signingSecret: "your-signing-secret",
      webhookPath: "/slack/events",
    },
  },
}
```

Modo HTTP multi-conta: definir`channels.slack.accounts.<id>.mode = "http"`e fornecer um único`webhookPath`por conta para que cada aplicativo Slack possa apontar para sua própria URL.

Manifesto (opcional)

Use este manifesto de aplicativo Slack para criar o aplicativo rapidamente (ajustar o nome/comando se você quiser). Incluir o
escopos de usuário se você planeja configurar um token de usuário.

```json
{
  "display_information": {
    "name": "OpenClaw",
    "description": "Slack connector for OpenClaw"
  },
  "features": {
    "bot_user": {
      "display_name": "OpenClaw",
      "always_online": false
    },
    "app_home": {
      "messages_tab_enabled": true,
      "messages_tab_read_only_enabled": false
    },
    "slash_commands": [
      {
        "command": "/openclaw",
        "description": "Send a message to OpenClaw",
        "should_escape": false
      }
    ]
  },
  "oauth_config": {
    "scopes": {
      "bot": [
        "chat:write",
        "channels:history",
        "channels:read",
        "groups:history",
        "groups:read",
        "groups:write",
        "im:history",
        "im:read",
        "im:write",
        "mpim:history",
        "mpim:read",
        "mpim:write",
        "users:read",
        "app_mentions:read",
        "reactions:read",
        "reactions:write",
        "pins:read",
        "pins:write",
        "emoji:read",
        "commands",
        "files:read",
        "files:write"
      ],
      "user": [
        "channels:history",
        "channels:read",
        "groups:history",
        "groups:read",
        "im:history",
        "im:read",
        "mpim:history",
        "mpim:read",
        "users:read",
        "reactions:read",
        "pins:read",
        "emoji:read",
        "search:read"
      ]
    }
  },
  "settings": {
    "socket_mode_enabled": true,
    "event_subscriptions": {
      "bot_events": [
        "app_mention",
        "message.channels",
        "message.groups",
        "message.im",
        "message.mpim",
        "reaction_added",
        "reaction_removed",
        "member_joined_channel",
        "member_left_channel",
        "channel_rename",
        "pin_added",
        "pin_removed"
      ]
    }
  }
}
```

Se você habilitar comandos nativos, adicione uma entrada`slash_commands`por comando que deseja expor (conforme a lista`/help`. Substituir o`channels.slack.commands.native`.

## Escopo (atual vs opcional)

A API de Conversas do Slack é de tipo: você só precisa dos escopos para o
tipos de conversa que você realmente toca (canais, grupos, im, mpim). Ver
https://docs.slack.dev/apis/web-api/using-the-conversations-api/ para a visão geral.

### Escopo do símbolo Bot (obrigatório)

-`chat:write`(enviar/atualizar/excluir mensagens via`chat.postMessage`
https://docs.slack.dev/reference/methods/chat.postMessage
-`im:write`(DM abertos via`conversations.open`para os DM utilizadores)
https://docs.slack.dev/reference/methods/conversations.open
-`channels:history`,`groups:history`,`im:history`,`mpim:history`https://docs.slack.dev/reference/methods/conversations.history
-`channels:read`,`groups:read`,`chat.postMessage`0,`chat.postMessage`1
https://docs.slack.dev/reference/methods/conversations.info
-`chat.postMessage`2 (busca de utilizadores)
https://docs.slack.dev/reference/methods/users.info
-`chat.postMessage`3,`chat.postMessage`4 `chat.postMessage`5 /`chat.postMessage`6)
https://docs.slack.dev/reference/methods/reactions.get
https://docs.slack.dev/reference/methods/reactions.add
-`chat.postMessage`7,`chat.postMessage`8 `chat.postMessage`9 /`im:write`0 /`im:write`1)
https://docs.slack.dev/reference/scopes/pins.read
https://docs.slack.dev/reference/scopes/pins.write
-`im:write`2 `im:write`3)
https://docs.slack.dev/reference/scopes/emoji.read
-`im:write`4 (carregamentos via`im:write`5)
https://docs.slack.dev/mensaging/working- with-files/#upload

### escopos de token do usuário (opcional, somente leitura por padrão)

Adicione estes em **User Token Scopes** se você configurar`channels.slack.userToken`.

-`channels:history`,`groups:history`,`im:history`,`mpim:history`-`channels:read`,`groups:read`,`im:read`,`mpim:read`-`users:read`-`reactions:read`-`groups:history`0
-`groups:history`1
-`groups:history`2

### Não é necessário hoje (mas provável futuro)

-`mpim:write`(apenas se adicionarmos grupo-DM aberto/DM início via`conversations.open`
-`groups:write`(somente se adicionarmos gestão de canais privados: create/rename/invite/archive)
-`chat:write.public`(somente se quisermos postar nos canais em que o bot não está)
https://docs.slack.dev/reference/scopes/chat.write.public
-`users:read.email`(apenas se precisarmos de campos de e-mail de`users.info`
https://docs.slack.dev/changelog/2017-04-narrowing-email-access
-`files:read`(apenas se começarmos a listar/ler metadados de ficheiros)

Configuração

O Slack usa apenas o Modo Socket (sem servidor HTTP webhook). Fornecer ambos os símbolos:

```json
{
  "slack": {
    "enabled": true,
    "botToken": "xoxb-...",
    "appToken": "xapp-...",
    "groupPolicy": "allowlist",
    "dm": {
      "enabled": true,
      "policy": "pairing",
      "allowFrom": ["U123", "U456", "*"],
      "groupEnabled": false,
      "groupChannels": ["G123"],
      "replyToMode": "all"
    },
    "channels": {
      "C123": { "allow": true, "requireMention": true },
      "#general": {
        "allow": true,
        "requireMention": true,
        "users": ["U123"],
        "skills": ["search", "docs"],
        "systemPrompt": "Keep answers short."
      }
    },
    "reactionNotifications": "own",
    "reactionAllowlist": ["U123"],
    "replyToMode": "off",
    "actions": {
      "reactions": true,
      "messages": true,
      "pins": true,
      "memberInfo": true,
      "emojiList": true
    },
    "slashCommand": {
      "enabled": true,
      "name": "openclaw",
      "sessionPrefix": "slack:slash",
      "ephemeral": true
    },
    "textChunkLimit": 4000,
    "mediaMaxMb": 20
  }
}
```

Os tokens também podem ser fornecidos via env vars:

-`SLACK_BOT_TOKEN`-`SLACK_APP_TOKEN`

As reações de Ack são controladas globalmente via`messages.ackReaction`+`messages.ackReactionScope`. Use`messages.removeAckAfterReply`para limpar o
reacção após a resposta do bot.

## Limites

- O texto de saída é cortado para`channels.slack.textChunkLimit`(padrão 4000).
- Opcional nova linha de blocos: definir`channels.slack.chunkMode="newline"`para dividir em linhas em branco (limites de parágrafo) antes do comprimento de blocos.
- Os uploads de mídia são tampados pelo`channels.slack.mediaMaxMb`(padrão 20).

## Responder threading

Por padrão, o OpenClaw responde no canal principal. Use`channels.slack.replyToMode`para controlar roscamento automático:

Modo
------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*`off`Responder no canal principal. Apenas thread se a mensagem ativando já estiver em um thread. □
A primeira resposta vai para thread (sob a mensagem desencadeante), as respostas subsequentes vão para o canal principal. Útil para manter o contexto visível enquanto evita a confusão de threads.
Todas as respostas vão para o tópico. Mantém as conversas contidas, mas pode reduzir a visibilidade.

O modo aplica-se tanto às chamadas de auto-respostas como às chamadas de ferramentas de agentes `slack sendMessage`.

## Per-chat-tipo threading

Você pode configurar o comportamento de threading diferente por tipo de chat, definindo`channels.slack.replyToModeByChatType`:

```json5
{
  channels: {
    slack: {
      replyToMode: "off", // default for channels
      replyToModeByChatType: {
        direct: "all", // DMs always thread
        group: "first", // group DMs/MPIM thread first reply
      },
    },
  },
}
```

Tipos de conversa suportados:

-`direct`: 1:1 DM (Slack`im`
-`group`: DM do grupo / MPIM (Slack`mpim`
-`channel`: canais normalizados (públicos/privados)

Precedência:

1.`replyToModeByChatType.<chatType>`2.`replyToMode`3. Predefinição do provedor `off`

Legacy`channels.slack.dm.replyToMode`ainda é aceito como um recurso para`direct`quando nenhum cancelamento do tipo chat é definido.

Exemplos:

Apenas DM de thread:

```json5
{
  channels: {
    slack: {
      replyToMode: "off",
      replyToModeByChatType: { direct: "all" },
    },
  },
}
```

Grupo de thread DMs mas manter canais na raiz:

```json5
{
  channels: {
    slack: {
      replyToMode: "off",
      replyToModeByChatType: { group: "first" },
    },
  },
}
```

Faça o thread dos canais, mantenha os DMs na raiz:

```json5
{
  channels: {
    slack: {
      replyToMode: "first",
      replyToModeByChatType: { direct: "off", group: "off" },
    },
  },
}
```

Marcas manuais de threading

Para controle de granulação fina, use estas tags nas respostas do agente:

-`[[reply_to_current]]`— resposta à mensagem de desencadeamento (linha inicial/continuação).
-`[[reply_to:<id>]]`— resposta a uma mensagem específica id.

## Sessões + roteamento

- Os DM partilham a sessão`main`(como WhatsApp/Telegram).
- Mapa de canais para sessões`agent:<agentId>:slack:channel:<channelId>`.
- Os comandos Slash usam sessões`agent:<agentId>:slack:slash:<userId>`(prefixo configurável via`channels.slack.slashCommand.sessionPrefix`.
- Se Slack não fornecer`channel_type`, OpenClaw inferi-lo a partir do prefixo ID do canal `D`,`C`,`G` e defaults para`channel`para manter as chaves de sessão estáveis.
- Registro de comando nativo usa`commands.native`(global default`agent:<agentId>:slack:channel:<channelId>`0 → Slack off) e pode ser substituído por espaço de trabalho com`agent:<agentId>:slack:channel:<channelId>`1. Os comandos de texto requerem mensagens`agent:<agentId>:slack:channel:<channelId>`2 autônomas e podem ser desativados com`agent:<agentId>:slack:channel:<channelId>`3. Os comandos Slack slash são gerenciados no aplicativo Slack e não são removidos automaticamente. Use`agent:<agentId>:slack:channel:<channelId>`4 para ignorar as verificações de grupo de acesso para comandos.
- Lista completa de comandos + configuração: [Comandos Slash] /tools/slash-commands

## Segurança DM (paring)

- Padrão:`channels.slack.dm.policy="pairing"`— remetentes desconhecidos de DM obter um código de pareamento (expira após 1 hora).
- Aprovar via`openclaw pairing approve slack <code>`.
- Para permitir a qualquer um: definir`channels.slack.dm.policy="open"`e`channels.slack.dm.allowFrom=["*"]`.
-`channels.slack.dm.allowFrom`aceita IDs de usuário, @handles ou e-mails (resolvido na inicialização quando tokens permitem). O assistente aceita nomes de usuário e os resolve para IDs durante a configuração quando os tokens permitem.

## Política do grupo

-`channels.slack.groupPolicy`controla o manuseamento do canal `open|disabled|allowlist`.
-`allowlist`exige que os canais sejam enumerados no`channels.slack.channels`.
- Se apenas definir`SLACK_BOT_TOKEN`/`SLACK_APP_TOKEN`e nunca criar uma secção`channels.slack`,
o tempo de execução deteta`groupPolicy`para`open`. Adicionar`channels.slack.groupPolicy`,`open|disabled|allowlist`0, ou uma lista de canais para bloqueá-lo.
- O assistente de configuração aceita nomes`open|disabled|allowlist`1 e resolve-os para IDs quando possível
(público + privado); se existirem múltiplas correspondências, ele prefere o canal ativo.
- No arranque, o OpenClaw resolve os nomes dos canais/utilizadores em listas de permissões para IDs (quando os tokens permitem)
e registra o mapeamento; entradas não resolvidas são mantidas como digitadas.
- Para permitir ** nenhum canal**, defina`open|disabled|allowlist`2 (ou mantenha uma lista de permissões vazia).

Opções de canal `channels.slack.channels.<id>`ou`channels.slack.channels.<name>`:

-`allow`: permitir/negar o canal quando`groupPolicy="allowlist"`.
-`requireMention`: Mencione a ligação para o canal.
-`tools`: sobrepõe-se a política opcional por canal `allow`/`deny`/`alsoAllow`.
-`toolsBySender`: A política opcional de ferramentas por sender substitui-se dentro do canal (as chaves são ids remetentes/@handles/emails; suportadas pelo`"*"`.
-`allowBots`: permitir mensagens de autoria de bots neste canal (padrão: false).
-`groupPolicy="allowlist"`0: opcional por canal user allowlist.
-`groupPolicy="allowlist"`1: filtro de habilidade (omite = todas as habilidades, vazio = nenhum).
-`groupPolicy="allowlist"`2: prompt de sistema extra para o canal (combinado com tópico/propósito).
-`groupPolicy="allowlist"`3: definir`groupPolicy="allowlist"`4 para desativar o canal.

## Alvos de entrega

Use estes com cron/CLI envia:

-`user:<id>`para os DM
-`channel:<id>`para canais

## Acções da ferramenta

As ações da ferramenta Slack podem ser fechadas com`channels.slack.actions.*`:

O grupo de ação O padrão
-------------- --------- ------------
Reações ativadas Reagir + listar reações
As mensagens estão activadas
• pinos activados • Pin/unpin/list
MembroInfo activado Informação do membro
EmojiList ativado emoji

## Notas de segurança

- Grava padrão para o token bot para que as ações de mudança de estado permaneçam
permissões bot do aplicativo e identidade.
- A configuração`userTokenReadOnly: false`permite que o token do usuário seja usado para escrever
operações quando um token de bot está indisponível, o que significa que as ações
instalando o acesso do usuário. Trate o token do usuário como altamente privilegiado e mantenha
Portas de ação e listas de permissão apertadas.
- Se você habilitar o usuário-token escreve, certifique-se de que o token do usuário inclui a escrita`chat:write`,`reactions:write`,`pins:write`,`files:write` ou essas operações falharão.

## Notas

- a indicação é controlada através do`channels.slack.channels`(configuração do`requireMention`ao`true`; o`agents.list[].groupChat.mentionPatterns`(ou o`messages.groupChat.mentionPatterns` também conta como menção.
- Substituição multi-agente: definir padrões por agente em`agents.list[].groupChat.mentionPatterns`.
- As notificações de reacção seguem o`channels.slack.reactionNotifications`(utilizar o`reactionAllowlist`com o modo`allowlist`.
- Mensagens de autor de bots são ignoradas por padrão; habilitar via`channels.slack.allowBots`ou`requireMention`0.
- Aviso: Se você permitir respostas a outros bots `requireMention`1 ou`requireMention`2), evite lacetes de resposta bot-to-bot com`requireMention`3,`requireMention`4 allowlists, e/ou limpar guaritails em`requireMention`5 e`requireMention`6.
- Para a ferramenta Slack, a semântica de remoção de reação está em [/tools/reactions]/tools/reactions.
- Os anexos são baixados para a loja de mídia quando permitido e abaixo do limite de tamanho.
