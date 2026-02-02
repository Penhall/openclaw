---
summary: "Telegram bot support status, capabilities, and configuration"
read_when:
  - Working on Telegram features or webhooks
---

# Telegram (Bot API)

Status: produção-pronto para bot DM + grupos via gramamY. Polação longa por padrão; webhook opcional.

## Montagem rápida (início)

1. Crie um bot com **@BotPai** e copie o token.
2. Defina o símbolo:
- Env:`TELEGRAM_BOT_TOKEN=...`- Ou configuração:`channels.telegram.botToken: "..."`.
- Se ambos estiverem definidos, a configuração tem precedência (inv fallback é apenas conta padrão).
3. Inicie o portal.
4. O acesso ao DM é pareamento por padrão; aprove o código de pareamento no primeiro contato.

Configuração mínima:

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing",
    },
  },
}
```

## O que é

- Um canal de API do Telegram Bot da Gateway.
- Roteamento determinístico: respostas voltar ao Telegram; o modelo nunca escolhe canais.
- Os DMs compartilham a sessão principal do agente; os grupos permanecem isolados `agent:<agentId>:telegram:group:<chatId>`.

## Configuração (caminho rápido)

### 1) Criar um símbolo de bot (BotPai)

1. Abra o Telegram e converse com **@BotPather**.
2. Executar`/newbot`, em seguida, siga as instruções (nome + nome de usuário terminando em`bot`.
3. Copie o token e armazene-o com segurança.

Configurações opcionais do BotPai:

-`/setjoingroups`— permitir/negar a adição do bot aos grupos.
-`/setprivacy`— controlar se o bot vê todas as mensagens de grupo.

### 2) Configurar o token (env ou configuração)

Exemplo:

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing",
      groups: { "*": { requireMention: true } },
    },
  },
}
```

Opção Env:`TELEGRAM_BOT_TOKEN=...`(funciona para a conta padrão).
Se tanto env quanto config estiverem configurados, a configuração terá precedência.

Suporte multi-conta: use`channels.telegram.accounts`com fichas por conta e opcional`name`. Ver `gateway/configuration`/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts para o padrão partilhado.

3. Inicie o portal. O Telegram começa quando um token é resolvido (config first, env fallback).
4. padrão de acesso DM para emparelhamento. Aprovar o código quando o bot é contatado pela primeira vez.
5. Para grupos: adicionar o bot, decidir o comportamento de privacidade / administração (abaixo), em seguida, definir`channels.telegram.groups`para controlar a menção gating + allowlists.

## Token + privacidade + permissões (lado do telegrama)

## # Criação do Token (BotPai)

-`/newbot`cria o bot e retorna o token (mantenha-o em segredo).
- Se um token vaza, revogue/regenere-o via @BotPai e atualize sua configuração.

## # Visibilidade da mensagem em grupo (Modo de Privacidade)

Os bots do Telegram são padrão para ** Modo de Privacidade**, que limita as mensagens de grupo que recebem.
Se seu bot deve ver  all  mensagens de grupo, você tem duas opções:

- Desactivar o modo de privacidade com`/setprivacy`**ou **
- Adicione o bot como um grupo **admin** (os bots de administração recebem todas as mensagens).

**Nota:** Quando você alterna o modo de privacidade, o Telegram requer remover + re-adicionar o bot
a cada grupo para que a mudança produza efeito.

## # Permissões de grupo (direitos de administração)

O estado de administração está definido dentro do grupo (Telegram UI). Os bots de administração sempre recebem todos
mensagens de grupo, então use o administrador se você precisar de visibilidade total.

## Como funciona (comportamento)

- Mensagens de entrada são normalizadas para o envelope de canal compartilhado com contexto de resposta e espaços de mídia.
- Respostas de grupo exigem uma menção por padrão (native @mention ou`agents.list[].groupChat.mentionPatterns`/`messages.groupChat.mentionPatterns`.
- Substituição multiagente: definir padrões por agente em`agents.list[].groupChat.mentionPatterns`.
- As respostas voltam sempre ao mesmo chat do Telegram.
- Long-polling usa corredor de gramamY com sequenciamento per-chat; a concorrência global é capotada pelo`agents.defaults.maxConcurrent`.
- Telegram Bot API não suporta recibos de leitura; não há opção`sendReadReceipts`.

## Rascunho de transmissão

OpenClaw pode transmitir respostas parciais em DMs de Telegram usando`sendMessageDraft`.

Requisitos:

- Modo Threaded ativado para o bot em @BotPather (modo de tópico forum).
- Apenas tópicos de bate-papo privados (telegrama inclui`message_thread_id`em mensagens de entrada).
-`channels.telegram.streamMode`não definido para`"off"`(por omissão:`"partial"`,`"block"`permite a actualização dos projectos).

O rascunho de streaming é somente para DM; Telegram não o suporta em grupos ou canais.

## Formatação (Telegrama HTML)

- O texto do Telegrama Outbound usa`parse_mode: "HTML"`(subconjunto de tag suportado pelo Telegram).
- Markdown-ish input é renderizado em **Telegram-safe HTML** (bold/italic/strike/code/links); elementos de bloco são achatados para texto com novas linhas/bullets.
- O HTML bruto dos modelos é escapado para evitar erros de processamento do Telegram.
- Se o Telegram rejeitar a carga útil HTML, o OpenClaw repete a mesma mensagem que o texto simples.

## Comandos (nativo + personalizado)

OpenClaw registra comandos nativos (como`/status`,`/reset`,`/model` com o menu bot do Telegram na inicialização.
Você pode adicionar comandos personalizados ao menu via configuração:

```json5
{
  channels: {
    telegram: {
      customCommands: [
        { command: "backup", description: "Git backup" },
        { command: "generate", description: "Create an image" },
      ],
    },
  },
}
```

## Resolução de problemas

-`setMyCommands failed`em logs geralmente significa saída HTTPS/DNS é bloqueado para`api.telegram.org`.
- Se você vir falhas`sendMessage`ou`sendChatAction`, verifique roteamento IPv6 e DNS.

Mais ajuda: [Solução de problemas do canal] /channels/troubleshooting.

Notas:

- Comandos personalizados são **menu somente entradas**; O Openclaw não os implementa, a menos que os trate noutro lugar.
- Nomes de comando são normalizados (leadering`/`despojado, minúscula) e devem corresponder`a-z`,`0-9`,`_`(1–32 caracteres).
- Comandos personalizados ** não podem substituir comandos nativos**. Os conflitos são ignorados e registados.
- Se`commands.native`estiver desativado, apenas comandos personalizados são registrados (ou limpos se nenhum).

## Limites

- O texto de saída é cortado para`channels.telegram.textChunkLimit`(padrão 4000).
- Opcional nova linha de blocos: definir`channels.telegram.chunkMode="newline"`para dividir em linhas em branco (limites de parágrafo) antes do comprimento de blocos.
- Os downloads/carga de mídia são tampados pelo`channels.telegram.mediaMaxMb`(padrão 5).
- Telegram Bot API solicita tempo fora após`channels.telegram.timeoutSeconds`(padrão 500 via gramamY). Defina mais baixo para evitar enforcamentos longos.
- O contexto histórico dos grupos utiliza o`channels.telegram.historyLimit`(ou o`channels.telegram.accounts.*.historyLimit`, que remonta ao`messages.groupChat.historyLimit`. Definir`0`para desabilitar (padrão 50).
- O historial do DM pode ser limitado com`channels.telegram.dmHistoryLimit`(turnos do utilizador).`channels.telegram.dms["<user_id>"].historyLimit`.

## Modos de ativação do grupo

Por padrão, o bot só responde a menções em grupos `@botname`ou padrões em`agents.list[].groupChat.mentionPatterns`. Para alterar este comportamento:

## # Via config (recomendado)

```json5
{
  channels: {
    telegram: {
      groups: {
        "-1001234567890": { requireMention: false }, // always respond in this group
      },
    },
  },
}
```

**Importante:** A configuração do`channels.telegram.groups`cria uma ** lista ** - apenas grupos listados (ou`"*"` serão aceitos.
Tópicos do fórum herdam sua configuração do grupo pai (allowFrom, requireMention, skills, prompts) a menos que você adicione sobreposições por tópico sob`channels.telegram.groups.<groupId>.topics.<topicId>`.

Para permitir que todos os grupos com sempre responder:

```json5
{
  channels: {
    telegram: {
      groups: {
        "*": { requireMention: false }, // all groups, always respond
      },
    },
  },
}
```

Para manter a menção apenas para todos os grupos (comportamento padrão):

```json5
{
  channels: {
    telegram: {
      groups: {
        "*": { requireMention: true }, // or omit groups entirely
      },
    },
  },
}
```

## # Através do comando (nível de sessão)

Enviar no grupo:

-`/activation always`- responder a todas as mensagens
-`/activation mention`- exigir menções (por omissão)

**Nota:** Somente o estado da sessão de atualização de comandos. Para o comportamento persistente entre reinícios, use a configuração.

## Obtendo o ID de chat do grupo

Enviar qualquer mensagem do grupo para`@userinfobot`ou`@getidsbot`no Telegram para ver o ID do chat (número negativo como`-1001234567890`.

**Dica: ** Para o seu próprio ID de usuário, DM o bot e ele irá responder com o seu ID de usuário (mensagem paring), ou usar`/whoami`uma vez que os comandos estão habilitados.

** Nota de privacidade:**`@userinfobot`é um bot de terceiros. Se preferir, adicione o bot ao grupo, envie uma mensagem e use`openclaw logs --follow`para ler`chat.id`, ou use o Bot API`getUpdates`.

## A configuração escreve

Por padrão, o Telegram pode escrever atualizações de configuração acionadas por eventos de canal ou`/config set|unset`.

Isto acontece quando:

- Um grupo é atualizado para um supergrupo e o Telegram emite`migrate_to_chat_id`(alterações no ID de bate-papo). OpenClaw pode migrar`channels.telegram.groups`automaticamente.
- Você executa`/config set`ou`/config unset`em um chat de Telegram (requer`commands.config: true`.

Desactivar com:

```json5
{
  channels: { telegram: { configWrites: false } },
}
```

## Tópicos (supergrupos de fórum)

Os tópicos do fórum do Telegram incluem um`message_thread_id`por mensagem. Openclaw:

- Adiciona`:topic:<threadId>`à tecla de sessão de grupo Telegram para que cada tópico seja isolado.
- Envia indicadores de digitação e respostas com`message_thread_id`para que as respostas permaneçam no tópico.
- O tópico geral (thread id`1` é especial: mensagem envia`message_thread_id`(Telegram rejeita), mas os indicadores de digitação ainda incluem.
- Expo`MessageThreadId`+`IsForum`no contexto do modelo para roteamento/templação.
- A configuração específica do tópico está disponível sob`channels.telegram.groups.<chatId>.topics.<threadId>`(competências, allowlists, resposta automática, prompts do sistema, desabilitação).
- As configurações do tópico herdam as configurações do grupo (requer menção, allowlists, habilidades, prompts, habilitadas) a menos que sobreponham por tópico.

Os chats privados podem incluir`message_thread_id`em alguns casos de borda. O OpenClaw mantém a tecla de sessão DM inalterada, mas ainda usa o id de thread para respostas/difusão de draft quando está presente.

## Botões Inline

O Telegram suporta teclados em linha com botões de retorno.

```json5
{
  channels: {
    telegram: {
      capabilities: {
        inlineButtons: "allowlist",
      },
    },
  },
}
```

Para configuração por conta:

```json5
{
  channels: {
    telegram: {
      accounts: {
        main: {
          capabilities: {
            inlineButtons: "allowlist",
          },
        },
      },
    },
  },
}
```

Âmbito de aplicação:

-`off`— botões inline desactivados
-`dm`— apenas DM (objectivos de grupo bloqueados)
-`group`— apenas grupos (objectivos DM bloqueados)
-`all`— DM + grupos
-`allowlist`— DM + grupos, mas apenas remetentes autorizados pelo`allowFrom`/`groupAllowFrom`(mesmas regras como comandos de controlo)

Predefinição:`allowlist`.
Legado:`capabilities: ["inlineButtons"]`=`inlineButtons: "all"`.

A enviar botões

Use a ferramenta de mensagem com o parâmetro`buttons`:

```json5
{
  action: "send",
  channel: "telegram",
  to: "123456789",
  message: "Choose an option:",
  buttons: [
    [
      { text: "Yes", callback_data: "yes" },
      { text: "No", callback_data: "no" },
    ],
    [{ text: "Cancel", callback_data: "cancel" }],
  ],
}
```

Quando um usuário clica em um botão, os dados de retorno de chamada são enviados de volta para o agente como uma mensagem com o formato:`callback_data: value`

## # Opções de configuração

Os recursos do Telegram podem ser configurados em dois níveis (formulário objeto mostrado acima; arrays de string legados ainda suportados):

-`channels.telegram.capabilities`: Configuração global de capacidade padrão aplicada a todas as contas do Telegram, a menos que seja anulada.
-`channels.telegram.accounts.<account>.capabilities`: Capacidades por conta que sobrepõem os padrões globais para essa conta específica.

Use a configuração global quando todos os bots/contas do Telegram devem se comportar da mesma forma. Use a configuração por conta quando diferentes bots precisam de comportamentos diferentes (por exemplo, uma conta só lida com DMs enquanto outra é permitida em grupos).

## Controle de acesso (DMs + grupos)

## # Acesso DM

- Predefinição:`channels.telegram.dmPolicy = "pairing"`. Os remetentes desconhecidos recebem um código de pareamento; as mensagens são ignoradas até serem aprovadas (os códigos expiram após 1 hora).
- Aprovar via:
-`openclaw pairing list telegram`-`openclaw pairing approve telegram <CODE>`- Emparelhamento é a troca padrão de token usada para DMs de Telegram. Detalhes: [Pairing] /start/pairing
-`channels.telegram.allowFrom`aceita IDs numéricos de utilizadores (recomendados) ou entradas`@username`. É **not** o nome de usuário do bot; use o ID do remetente humano. O assistente aceita`@username`e resolve-o para o ID numérico quando possível.

Encontrar o seu ID de utilizador do Telegram

Mais seguro (sem bot de terceiros):

1. Inicie o gateway e DM seu bot.
2. Execute`openclaw logs --follow`e procure`from.id`.

Alternativo (a API oficial do Bot):

1. DM seu bot.
2. Busque atualizações com seu token bot e leia`message.from.id`:
   ```bash
   curl "https://api.telegram.org/bot<bot_token>/getUpdates"
   ```

Terceiros (menos privados):

- DM`@userinfobot`ou`@getidsbot`e use o ID de usuário retornado.

## # Acesso em grupo

Dois controlos independentes:

**1. Quais grupos são permitidos** (grupo allowlist via`channels.telegram.groups`:

- Não é permitida a configuração`groups`= todos os grupos
- Com configuração`groups`= apenas grupos listados ou`"*"`são permitidos
- Exemplo:`"groups": { "-1001234567890": {}, "*": {} }`permite que todos os grupos

**2. Que remetentes são permitidos** (enviar filtragem via`channels.telegram.groupPolicy`:

-`"open"`= todos os remetentes em grupos permitidos podem mensagem
-`"allowlist"`= apenas os remetentes no`channels.telegram.groupAllowFrom`podem enviar uma mensagem
-`"disabled"`= nenhuma mensagem de grupo aceite
O padrão é`groupPolicy: "allowlist"`(bloqueado a menos que você adicione`groupAllowFrom`.

A maioria dos usuários quer:`groupPolicy: "allowlist"`+`groupAllowFrom`+ grupos específicos listados em`channels.telegram.groups`

## Long-polling vs webhook

- Padrão: longo polling (sem URL pública necessária).
- Modo de hook web: conjunto`channels.telegram.webhookUrl`(opcionalmente`channels.telegram.webhookSecret`+`channels.telegram.webhookPath`.
- O ouvinte local liga-se ao`0.0.0.0:8787`e serve o`POST /telegram-webhook`por padrão.
- Se sua URL pública é diferente, use um proxy reverso e ponto`channels.telegram.webhookUrl`no endpoint público.

## Responder threading

O Telegram suporta respostas opcionais enroscadas através de tags:

-`[[reply_to_current]]`-- responda à mensagem desencadeante.
-`[[reply_to:<id>]]`-- responda a uma mensagem específica id.

Controlado por`channels.telegram.replyToMode`:

-`first`(padrão),`all`,`off`.

## Mensagens de áudio (voz vs arquivo)

Telegram distingue ** notas de voz** (bolha redonda) de ** arquivos de áudio** (cartão de metadados).
O OpenClaw é padrão para arquivos de áudio para compatibilidade backward.

Para forçar uma bolha de nota de voz nas respostas do agente, inclua esta tag em qualquer lugar na resposta:

-`[[audio_as_voice]]`– envie áudio como uma nota de voz em vez de um arquivo.

A etiqueta é retirada do texto entregue. Outros canais ignoram esta etiqueta.

Para enviar mensagens, defina`asVoice: true`com um áudio compatível com voz URL`media``message`é opcional quando a mídia está presente):

```json5
{
  action: "send",
  channel: "telegram",
  to: "123456789",
  media: "https://example.com/voice.ogg",
  asVoice: true,
}
```

Fixadores

O OpenClaw suporta receber e enviar adesivos Telegram com cache inteligente.

## Recebendo adesivos

Quando um usuário envia um adesivo, o OpenClaw o manipula com base no tipo de adesivo:

- ** Autocolantes Estáticos (WBP): ** Transferido e processado através da visão. O autocolante aparece como um substituto`<media:sticker>`no conteúdo da mensagem.
- ** Autocolantes animados (TGS):** Saltado (formato Lottie não suportado para processamento).
- **Vídeo adesivos (WEBM):** Saltado (formato de vídeo não suportado para processamento).

Campo de contexto do modelo disponível ao receber adesivos:

-`Sticker`— objecto com:
-`emoji`— emoji associado à etiqueta
-`setName`— nome do conjunto de autocolantes
-`fileId`— ID do ficheiro Telegram (enviar o mesmo autocolante de volta)
-`fileUniqueId`— ID estável para pesquisa de cache
-`cachedDescription`— descrição da visão em cache quando disponível

Cache de adesivos

Os adesivos são processados através das capacidades de visão da IA para gerar descrições. Como os mesmos adesivos são frequentemente enviados repetidamente, o OpenClaw caches essas descrições para evitar chamadas de API redundantes.

** Como funciona:**

1. ** Primeiro encontro:** A imagem autocolante é enviada para a IA para análise de visão. A IA gera uma descrição (por exemplo, "Um gato de desenho animado acenando com entusiasmo").
2. ** Armazenamento de cache: ** A descrição é salva junto com o arquivo ID do adesivo, emoji, e definir o nome.
3. ** Encontros posteriores: ** Quando o mesmo adesivo é visto novamente, a descrição em cache é usada diretamente. A imagem não é enviada para a IA.

**Cache location:**`~/.openclaw/telegram/sticker-cache.json`

**Formato de entrada do cache:**

```json
{
  "fileId": "CAACAgIAAxkBAAI...",
  "fileUniqueId": "AgADBAADb6cxG2Y",
  "emoji": "👋",
  "setName": "CoolCats",
  "description": "A cartoon cat waving enthusiastically",
  "cachedAt": "2026-01-15T10:30:00.000Z"
}
```

** Benefícios:**

- Reduz os custos de API, evitando repetidas chamadas de visão para o mesmo adesivo
- Tempos de resposta mais rápidos para adesivos em cache (sem atraso de processamento de visão)
- Permite a funcionalidade de busca de adesivos com base em descrições em cache

O cache é preenchido automaticamente como adesivos são recebidos. Não há necessidade de gerenciamento manual de cache.

Enviando adesivos

O agente pode enviar e pesquisar adesivos usando as ações`sticker`e`sticker-search`. Estes estão desactivados por omissão e devem estar activados na configuração:

```json5
{
  channels: {
    telegram: {
      actions: {
        sticker: true,
      },
    },
  },
}
```

Enviar um autocolante:

```json5
{
  action: "sticker",
  channel: "telegram",
  to: "123456789",
  fileId: "CAACAgIAAxkBAAI...",
}
```

Parâmetros:

-`fileId`(necessário) — identificação do ficheiro de telegrama da etiqueta. Obter isso de`Sticker.fileId`ao receber um adesivo, ou de um resultado`sticker-search`.
-`replyTo`(opcional) — ID da mensagem para responder.
-`threadId`(opcional) — ID da mensagem para tópicos do fórum.

** Procurar adesivos: **

O agente pode pesquisar adesivos em cache por descrição, emoji, ou definir o nome:

```json5
{
  action: "sticker-search",
  channel: "telegram",
  query: "cat waving",
  limit: 5,
}
```

Retorna adesivos correspondentes da cache:

```json5
{
  ok: true,
  count: 2,
  stickers: [
    {
      fileId: "CAACAgIAAxkBAAI...",
      emoji: "👋",
      description: "A cartoon cat waving enthusiastically",
      setName: "CoolCats",
    },
  ],
}
```

A pesquisa usa correspondência fuzzy entre texto de descrição, caracteres emoji e nomes de conjuntos.

**Exemplo com threading:**

```json5
{
  action: "sticker",
  channel: "telegram",
  to: "-1001234567890",
  fileId: "CAACAgIAAxkBAAI...",
  replyTo: 42,
  threadId: 123,
}
```

## Streaming (drafts)

Telegram pode transmitir **bolhas de draft** enquanto o agente está gerando uma resposta.
OpenClaw usa o Bot API`sendMessageDraft`(não mensagens reais) e então envia o
resposta final como uma mensagem normal.

Requisitos (Telegram Bot API 9.3+):

- **Conversas particulares com tópicos habilitados** (modo de fórum tópico para o bot).
- As mensagens recebidas devem incluir`message_thread_id`(telefone privado).
- O streaming é ignorado para grupos/supergrupos/canais.

Configuração:

-`channels.telegram.streamMode: "off" | "partial" | "block"`(por omissão:`partial`
-`partial`: atualizar a bolha de rascunho com o texto de streaming mais recente.
-`block`: atualizar a bolha de rascunho em blocos maiores (enchidos).
-`off`: desactivar a transmissão do projecto.
- Opcional (apenas para`streamMode: "block"`:
-`channels.telegram.draftChunk: { minChars?, maxChars?, breakPreference? }`- incumprimentos:`minChars: 200`,`maxChars: 800`,`breakPreference: "paragraph"`(apertado em`partial`0).

Observação: o rascunho de streaming é separado de **block streaming** (mensagens de canal).
O streaming em bloco está desligado por padrão e requer`channels.telegram.blockStreaming: true`se você deseja mensagens de Telegram antecipadas em vez de redigir atualizações.

Raciocínio do fluxo (apenas no Telegrama):

-`/reasoning stream`raciocina no rascunho da bolha enquanto a resposta é
gerando, então envia a resposta final sem raciocínio.
- Se`channels.telegram.streamMode`for`off`, o fluxo de raciocínio é desativado.
Mais contexto: [Streaming + blocking] /concepts/streaming.

## Política de repetição

A API do Telegram Outbound chama novamente erros de rede transiente/429 com backoff exponencial e jitter. Configurar via`channels.telegram.retry`. Ver [Política de repetição] /concepts/retry.

## Ferramenta de agente (mensagens + reações)

- Ferramenta:`telegram`com acção`sendMessage``to`,`content`, opcional`mediaUrl`,`replyToMessageId`,`messageThreadId`.
- Ferramenta:`telegram`com acção`react``chatId`,`sendMessage`0,`sendMessage`1).
- Ferramenta:`sendMessage`2 com acção`sendMessage`3 `sendMessage`4,`sendMessage`5).
- Semântica de remoção de reações: ver [/tools/reactions] /tools/reactions.
- Classificação das ferramentas:`sendMessage`6,`sendMessage`7,`sendMessage`8 (por omissão: activado) e`sendMessage`9 (por omissão: deficiente).

## notificações de reação

** Como funcionam as reacções:
As reações de telegrama chegam como **separar eventos`message_reaction`**, não como propriedades em cargas de mensagens. Quando um usuário adiciona uma reação, OpenClaw:

1. Recebe a atualização`message_reaction`da API do Telegram
2. Converte-o para um evento do sistema** com formato:`"Telegram reaction added: {emoji} by {user} on msg {id}"`3. Encaminha o evento do sistema usando a mesma chave de sessão** como mensagens regulares
4. Quando a próxima mensagem chega nessa conversa, os eventos do sistema são drenados e precedidos ao contexto do agente

O agente vê reações como ** notificações do sistema** no histórico de conversas, não como metadados de mensagens.

**Configuração:**

-`channels.telegram.reactionNotifications`: Controlos das reacções que desencadeiam as notificações
-`"off"`— ignorar todas as reacções
-`"own"`— notificar quando os utilizadores reagirem às mensagens bot (melhor esforço; in-memory) (padrão)
-`"all"`— Notificação de todas as reacções

-`channels.telegram.reactionLevel`: Capacidade de reacção do agente de controlo
-`"off"`— O agente não pode reagir às mensagens
-`"ack"`— bot envia reações de reconhecimento (em processamento) (padrão)
-`"minimal"`— o agente pode reagir com moderação (orientação: 1 por 5-10 intercâmbios)
-`"extensive"`— O agente pode reagir liberalmente quando adequado

** Grupos do Fórum:** As reações em grupos de fóruns incluem`message_thread_id`e usam chaves de sessão como`agent:main:telegram:group:{chatId}:topic:{threadId}`. Isso garante que as reações e mensagens no mesmo tópico permaneçam juntas.

** Configuração do exemplo: **

```json5
{
  channels: {
    telegram: {
      reactionNotifications: "all", // See all reactions
      reactionLevel: "minimal", // Agent can react sparingly
    },
  },
}
```

**Requisitos:**

- Os bots de telegrama devem solicitar explicitamente`message_reaction`em`allowed_updates`(configurado automaticamente pelo OpenClaw)
- Para o modo webhook, as reações estão incluídas no webhook`allowed_updates`- Para o modo de votação, as reacções estão incluídas no`getUpdates``allowed_updates`

## Alvos de entrega (CLI/cron)

- Use um chat id `123456789` ou um nome de usuário `@name` como alvo.
- Exemplo:`openclaw message send --channel telegram --target 123456789 --message "hi"`.

## Resolução de problemas

**Bot não responde às mensagens de não-menção em um grupo:**

- Se você definir`channels.telegram.groups.*.requireMention=false`, a API Bot do Telegram **privacy mode** deve ser desabilitada.
- BotPather:`/setprivacy`→ **Desactivar** (em seguida, remover + adicionar o bot ao grupo)
-`openclaw channels status`mostra um aviso quando a configuração espera mensagens de grupo não mencionadas.
-`openclaw channels status --probe`pode verificar adicionalmente os membros para identificar grupos numéricos explícitos (não pode auditar regras`"*"`.
- Teste rápido:`/activation always`(somente sessão; use a configuração para persistência)

** Não ver mensagens de grupo: **

- Se o`channels.telegram.groups`for definido, o grupo deve ser incluído na lista ou utilizar o`"*"`- Verifique as configurações de privacidade em @BotPai → "Privacidade do grupo" deve ser **OFF**
- Verificar bot é realmente um membro (não apenas um administrador sem acesso de leitura)
- Verifique os logs de gateway:`openclaw logs --follow`(procure por "mensagem de grupo de salto")

**Bot responde a menções, mas não`/activation always`:**

- O comando`/activation`atualiza o estado da sessão mas não persiste na configuração
- Para comportamento persistente, adicione grupo ao`channels.telegram.groups`com`requireMention: false`

**Comandos como`/status`não funcionam:**

- Certifique-se de que seu ID de usuário do Telegram está autorizado (via pareamento ou`channels.telegram.allowFrom`
- Os comandos requerem autorização mesmo em grupos com`groupPolicy: "open"`

** Long-polling aborta imediatamente em Node 22+ (muitas vezes com proxies/custom fetch):**

- Node 22+ é mais rigoroso sobre instâncias`AbortSignal`; sinais estrangeiros podem abortar chamadas`fetch`imediatamente.
- Atualizar para uma compilação OpenClaw que normaliza sinais de abortar, ou executar o gateway no Node 20 até que você possa atualizar.

** Bot começa, em seguida, silenciosamente pára de responder (ou logs`HttpError: Network request ... failed`:**

- Alguns anfitriões resolvem primeiro`api.telegram.org`para IPv6. Se seu servidor não tiver saída IPv6 funcionando, o grammY pode ficar preso apenas em pedidos IPv6.
- Corrigir habilitando IPv6 egress **ou** forçando resolução IPv4 para`api.telegram.org`(por exemplo, adicione uma entrada`/etc/hosts`usando o registro IPv4 A, ou prefira IPv4 em sua pilha de DNS do SO), em seguida, reinicie o gateway.
- Verificação rápida:`dig +short api.telegram.org A`e`dig +short api.telegram.org AAAA`para confirmar o que o DNS retorna.

## Referência de configuração (Telegrama)

Configuração completa: [Configuração]/gateway/configuration

Opções do fornecedor:

-`channels.telegram.enabled`: activar/desactivar a inicialização do canal.
-`channels.telegram.botToken`: bot token (BotPai).
-`channels.telegram.tokenFile`: ler token do caminho do arquivo.
-`channels.telegram.dmPolicy`:`pairing | allowlist | open | disabled`(padrão: emparelhamento).
-`channels.telegram.allowFrom`: Lista de autorizações de DM (ids/nomes de utilizador).`open`exige`"*"`.
-`channels.telegram.groupPolicy`:`open | allowlist | disabled`(default: allowlist).
-`channels.telegram.botToken`0: lista de permissões de envio de grupo (ids/nomes de utilizador).
-`channels.telegram.botToken`1: por grupo predefinições + allowlist (use`channels.telegram.botToken`2 para padrões globais).
-`channels.telegram.botToken`3: Mencione o padrão.
-`channels.telegram.botToken`4: filtro de habilidade (omite = todas as habilidades, vazio = nenhum).
-`channels.telegram.botToken`5: substituição por lista de remetentes por grupo.
-`channels.telegram.botToken`6: prompt de sistema extra para o grupo.
-`channels.telegram.botToken`7: desativar o grupo quando`channels.telegram.botToken`8.
-`channels.telegram.botToken`9: substituições por tópico (os mesmos campos do grupo).
-`channels.telegram.tokenFile`0: sobreposição por tópico.
-`channels.telegram.tokenFile`1:`channels.telegram.tokenFile`2 (default: allowlist).
-`channels.telegram.tokenFile`3: substituição por conta.
-`channels.telegram.tokenFile`4:`channels.telegram.tokenFile`5 (por omissão:`channels.telegram.tokenFile`6).
-`channels.telegram.tokenFile`7: tamanho do pedaço de saída (chars).
-`channels.telegram.tokenFile`8:`channels.telegram.tokenFile`9 (padrão) ou`channels.telegram.dmPolicy`0 para dividir em linhas em branco (limites de parágrafos) antes do corte do comprimento.
-`channels.telegram.dmPolicy`1: comutar as antevisões de ligações para mensagens de saída (por omissão: true).
-`channels.telegram.dmPolicy`2:`channels.telegram.dmPolicy`3 (transmissão do projecto).
-`channels.telegram.dmPolicy`4: capa de suporte de entrada/saída (MB).
-`channels.telegram.dmPolicy`5: política de repetição para chamadas de API de Telegram de saída (tentativas, minDelayMs, maxDelayMs, jitter).
-`channels.telegram.dmPolicy`6: sobrepor Node AutoSelectFamily (verdadeiro=enable, false=desable). O padrão é desabilitado no Node 22 para evitar tempo limite Happy Eyeballs.
-`channels.telegram.dmPolicy`7: URL proxy para chamadas de API Bot (SOCKS/HTTP).
-`channels.telegram.dmPolicy`8: ativar o modo webhook.
-`channels.telegram.dmPolicy`9: webhook secret (opcional).
-`pairing | allowlist | open | disabled`0: local webhook path (padrão`pairing | allowlist | open | disabled`1).
-`pairing | allowlist | open | disabled`2: Gate Telegram ferramenta reações.
-`pairing | allowlist | open | disabled`3: mensagem de ferramenta do portal Telegram envia.
-`pairing | allowlist | open | disabled`4: A mensagem da ferramenta do portal Telegram apaga.
-`pairing | allowlist | open | disabled`5: ações de etiqueta do portal Telegram - enviar e pesquisar (padrão: falso).
-`pairing | allowlist | open | disabled`6:`pairing | allowlist | open | disabled`7 — controlo das reacções que desencadeiam os acontecimentos do sistema (por omissão:`pairing | allowlist | open | disabled`8 quando não está definido).
-`pairing | allowlist | open | disabled`9:`channels.telegram.allowFrom`0 — capacidade de reacção do agente de controlo (por omissão:`channels.telegram.allowFrom`1 quando não está definido).

Opções globais relacionadas:

-`agents.list[].groupChat.mentionPatterns`(padrões de medição).
-`messages.groupChat.mentionPatterns`(regresso global).
-`commands.native`(defaults to`"auto"`→ on for Telegram/Discord, off for Slack),`commands.text`,`commands.useAccessGroups`(comportamento de comando). Substituir pelo`channels.telegram.commands.native`.
-`messages.responsePrefix`,`messages.ackReaction`,`messages.ackReactionScope`,`messages.groupChat.mentionPatterns`0.
