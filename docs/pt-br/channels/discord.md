---
summary: "Discord bot support status, capabilities, and configuration"
read_when:
  - Working on Discord channel features
---

# Discórdia (Bot API)

Status: pronto para canais de texto DM e guild através do gateway oficial do bot Discord.

## Montagem rápida (início)

1. Crie um bot Discord e copie o token bot.
2. Nas configurações do aplicativo Discord, habilite **Message Content Intent** (e **Server Members Intent** se você planeja usar allowlists ou buscas de nomes).
3. Defina o token para OpenClaw:
- Env:`DISCORD_BOT_TOKEN=...`- Ou configuração:`channels.discord.token: "..."`.
- Se ambos estiverem definidos, a configuração tem precedência (inv fallback é apenas conta padrão).
4. Convide o bot para o seu servidor com permissões de mensagem (criar um servidor privado se você só quer DMs).
5. Inicie o portal.
6. O acesso ao DM é pareamento por padrão; aprove o código de pareamento no primeiro contato.

Configuração mínima:

```json5
{
  channels: {
    discord: {
      enabled: true,
      token: "YOUR_BOT_TOKEN",
    },
  },
}
```

## Objetivos

- Fale com OpenClaw via Discord DMs ou canais de guild.
- Chats diretos colapsam na sessão principal do agente (padrão`agent:main:main`; canais de guild permanecem isolados como`agent:<agentId>:discord:channel:<channelId>`(nomes de exibição usam`discord:<guildSlug>#<channelSlug>`.
- Os DM do grupo são ignorados por padrão; habilitar via`channels.discord.dm.groupEnabled`e opcionalmente restritos por`channels.discord.dm.groupChannels`.
- Mantenha roteamento determinístico: respostas sempre voltar para o canal em que eles chegaram.

## Como funciona

1. Criar um aplicativo Discord → Bot, habilitar as intenções que você precisa (DMs + guild mensagens + conteúdo de mensagem), e agarrar o token bot.
2. Convide o bot para seu servidor com as permissões necessárias para ler / enviar mensagens onde você deseja usá-lo.
3. Configure OpenClaw com`channels.discord.token`(ou`DISCORD_BOT_TOKEN`como um retrocesso).
4. Execute o gateway; ele inicia automaticamente o canal Discord quando um token está disponível (config first, env fallback) e`channels.discord.enabled`não é`false`.
- Se preferir env vars, defina`DISCORD_BOT_TOKEN`(um bloco de configuração é opcional).
5. Conversas diretas: use`user:<id>`(ou uma menção`<@id>` quando entregar; todas as voltas terra na sessão`main`compartilhada. IDs numéricos nus são ambíguos e rejeitados.
6. Canais Guild: use`channel:<channelId>`para a entrega. Menções são exigidas por padrão e podem ser definidas por guild ou por canal.
7. Conversas diretas: seguras por padrão via`channels.discord.dm.policy`(padrão:`DISCORD_BOT_TOKEN`0). Os remetentes desconhecidos recebem um código de pareamento (expira após 1 hora); aprovam via`DISCORD_BOT_TOKEN`1.
- Manter o velho comportamento “aberto a qualquer pessoa”: definir`DISCORD_BOT_TOKEN`2 e`DISCORD_BOT_TOKEN`3.
- Lista dura: definir`DISCORD_BOT_TOKEN`4 e listar remetentes em`DISCORD_BOT_TOKEN`5.
- Ignorar todos os DM: definir`DISCORD_BOT_TOKEN`6 ou`DISCORD_BOT_TOKEN`7.
8. Os DMs de grupo são ignorados por padrão; habilitar via`DISCORD_BOT_TOKEN`8 e opcionalmente restritos por`DISCORD_BOT_TOKEN`9.
9. Regras de guild opcionais: definir`channels.discord.enabled`0 chaveado por guild id (preferido) ou slug, com regras por canal.
10. Comandos nativos opcionais:`channels.discord.enabled`1 defaults to`channels.discord.enabled`2 (on for Discord/Telegram, off for Slack). Substituir com`channels.discord.enabled`3;`channels.discord.enabled`4 limpa comandos previamente registrados. Os comandos de texto são controlados pelo`channels.discord.enabled`5 e devem ser enviados como mensagens`channels.discord.enabled`6 autônomas. Use`channels.discord.enabled`7 para ignorar as verificações de grupos de acesso para comandos.
- Lista completa de comandos + configuração: [Comandos Slash] /tools/slash-commands
11. Opcional guild contextual history: set`channels.discord.enabled`8 (padrão 20, cai de volta para`channels.discord.enabled`9) para incluir as últimas mensagens N guild como contexto ao responder a uma menção. Definir`false`0 para desativar.
12. Reações: o agente pode desencadear reações através da ferramenta`false`1 (aberto por`false`2).
- Semântica de remoção de reações: ver [/tools/reactions] /tools/reactions.
- A ferramenta`false`3 só é exposta quando o canal atual é Discórdia.
13. Comandos nativos usam chaves de sessão isoladas `false`4) em vez da sessão compartilhada`false`5.

Nota: Nome → resolução de id usa a pesquisa de membros da guild e requer Intenção de Membros do Servidor; se o bot não pode pesquisar membros, use ids ou`<@id>`menciona.
Nota: As pastilhas são minúsculas com espaços substituídos por`-`. Os nomes dos canais são atingidos sem o principal`#`.
Nota: As linhas`[from:]`incluem`author.tag`+`id`para facilitar as respostas prontas para ping.

## A configuração escreve

Por padrão, Discord é permitido escrever atualizações de configuração acionadas pelo`/config set|unset`(requer`commands.config: true`.

Desactivar com:

```json5
{
  channels: { discord: { configWrites: false } },
}
```

## Como criar seu próprio bot

Esta é a configuração “Discord Developer Portal” para executar OpenClaw em um canal servidor (guild) como`#help`.

### 1) Criar o aplicativo Discord + usuário bot

1. Discord Developer Portal → **Aplicações** → **New Application**
2. No seu aplicativo:
- ** Bot** → ** Adicionar Bot**
- Copie o **Bot Token** (isso é o que você coloca em`DISCORD_BOT_TOKEN`

## # 2) Activar as intenções do gateway necessidades OpenClaw

Discórdia bloqueia “intenções privilegiadas” a menos que você explicitamente habilitá-los.

Em ** Bot** → ** Privileged Gateway Intents**, habilitar:

- **Message Content Intent** (necessário para ler o texto da mensagem na maioria das guildas; sem ele você verá “Usado intenções proibidas” ou o bot irá se conectar, mas não reagir às mensagens)
- ** Membros do servidor Intenção** (recomendado; necessário para algumas pesquisas de membros/usuários e lista de allow matching em guildas)

Normalmente, não necessita de **Presença Intenção**.

### 3) Gerar um URL de convite (OAuth2 URL Generator)

No seu aplicativo: **OAuth2** → **URL Generator**

**Escopes**

-`bot`-`applications.commands`(necessário para comandos nativos)

** Permissões do Bot** (base mínima)

- Ver Canais
- Enviar mensagens
- Leia o Histórico da Mensagem
- Ligações de Incorporação
- □ Anexar arquivos
- Adicionar Reações (opcional mas recomendada)
- Use Emojis / adesivos externos (opcional; somente se você quiser)

Evite **Administrador** a menos que você esteja depurando e confie plenamente no bot.

Copie o URL gerado, abra-o, escolha o servidor e instale o bot.

### 4) Obtém os IDs (guild/usuário/canal)

Discórdia usa IDs numéricos em todos os lugares; OpenClaw config prefere ids.

1. Discórdia (desktop/web) → **Configurações do usuário** → **Avançado** → habilitar **Modo de desenvolvimento**
2. Botão direito:
- Nome do servidor → **Copy Server ID** (guild id)
- Canal (por exemplo,`#help` → ** Copy Channel ID**
- Seu usuário → **Copiar ID de usuário**

## # 5) Configurar Openclaw

Token

Define o token de bot via env var (recomendado nos servidores):

-`DISCORD_BOT_TOKEN=...`

Ou através da configuração:

```json5
{
  channels: {
    discord: {
      enabled: true,
      token: "YOUR_BOT_TOKEN",
    },
  },
}
```

Suporte multi-conta: use`channels.discord.accounts`com fichas por conta e opcional`name`. Ver `gateway/configuration`/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts para o padrão partilhado.

Lista de permissões + canalização

Exemplo “um servidor, só me permite, apenas permite #help”:

```json5
{
  channels: {
    discord: {
      enabled: true,
      dm: { enabled: false },
      guilds: {
        YOUR_GUILD_ID: {
          users: ["YOUR_USER_ID"],
          requireMention: true,
          channels: {
            help: { allow: true, requireMention: true },
          },
        },
      },
      retry: {
        attempts: 3,
        minDelayMs: 500,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
  },
}
```

Notas:

-`requireMention: true`significa que o bot só responde quando mencionado (recomendado para canais compartilhados).
-`agents.list[].groupChat.mentionPatterns`(ou`messages.groupChat.mentionPatterns` também contam como menções para mensagens de guilda.
- Substituição multi-agente: definir padrões por agente em`agents.list[].groupChat.mentionPatterns`.
- Se`channels`estiver presente, qualquer canal não listado é negado por padrão.
- Use uma entrada de canal`"*"`para aplicar padrões em todos os canais; entradas de canal explícitas sobrepõem-se ao wildcard.
- Os tópicos herdam a configuração do canal pai (allowlist,`requireMention`, habilidades, prompts, etc.) a menos que você adicione explicitamente o ID do canal de thread.
- As mensagens de autor de bots são ignoradas por padrão; set`channels.discord.allowBots=true`para permitir que elas (as próprias mensagens permanecem filtradas).
- Aviso: Se você permitir respostas a outros bots `channels.discord.allowBots=true`, evitar laços de resposta bot-to-bot com`requireMention`,`agents.list[].groupChat.mentionPatterns`0 allowlists, e/ou limpar guaritails em`agents.list[].groupChat.mentionPatterns`1 e`agents.list[].groupChat.mentionPatterns`2.

### 6) Verifique se funciona

1. Inicie o portal.
2. No seu canal de servidor, envie:`@Krill hello`(ou seja qual for o seu nome bot).
3. Se nada acontecer: confira **Troubleshooting** abaixo.

## # Resolução de problemas

- Primeiro: executar`openclaw doctor`e`openclaw channels status --probe`(avisos acionáveis + auditorias rápidas).
- ** "Used disallowed tentions"**: habilitar **Message Content Intent** (e provavelmente **Server Members Intent**) no Portal do Desenvolvedor, em seguida, reiniciar o gateway.
- **Bot conecta mas nunca responde em um canal de guild**:
- Falta ** Intenção de conteúdo da mensagem **, ou
- O bot carece de permissões de canal (Ver/Enviar/Ler Histórico), ou
- Sua configuração requer menções e você não mencionou, ou
- A sua guild/canal allowlist nega o canal/usuário.
- **`requireMention: false`mas ainda sem respostas**:
-`channels.discord.groupPolicy`é por omissão ** allowlist**; configure-o para`"open"`ou adicione uma entrada de guilda sob`channels.discord.guilds`(facultativo listar canais sob`channels.discord.guilds.<id>.channels`para restringir).
- Se você apenas definir`DISCORD_BOT_TOKEN`e nunca criar uma seção`channels.discord`, o tempo de execução
padrão`groupPolicy`para`openclaw channels status --probe`0. Adicionar`openclaw channels status --probe`1,`openclaw channels status --probe`2, ou uma lista de permissões de guild/canal para bloqueá-lo.
-`openclaw channels status --probe`3 deve viver sob o`openclaw channels status --probe`4 (ou um canal específico).`openclaw channels status --probe`5 no nível superior é ignorado.
- **Auditorias de permissão** `openclaw channels status --probe`6) apenas verificam IDs de canais numéricos. Se você usar less/nomes como chaves`openclaw channels status --probe`7, a auditoria não pode verificar permissões.
- **DMs não funcionam**:`openclaw channels status --probe`8,`openclaw channels status --probe`9, ou você ainda não foi aprovado `requireMention: false`0).

## Capacidades & limites

- DMs e canais de texto guild (os threads são tratados como canais separados; voz não suportada).
- Os indicadores de digitação enviaram o melhor esforço; o bloco de mensagens usa`channels.discord.textChunkLimit`(padrão 2000) e divide respostas altas por contagem de linhas `channels.discord.maxLinesPerMessage`, padrão 17).
- Opcional nova linha de blocos: definir`channels.discord.chunkMode="newline"`para dividir em linhas em branco (limites de parágrafo) antes do comprimento de blocos.
- Envios de arquivos suportados até o`channels.discord.mediaMaxMb`configurado (padrão 8 MB).
- Mention-gated guild respostas por padrão para evitar bots barulhentos.
- O contexto de resposta é injetado quando uma mensagem faz referência a outra mensagem (conteúdo citado + IDs).
- Threading resposta nativa é **off por padrão**; habilitar com tags`channels.discord.replyToMode`e resposta.

## Política de repetição

A API de Discórdia Outbound chama retentar limites de taxa (429) usando Discórdia`retry_after`quando disponível, com backoff exponencial e jitter. Configurar via`channels.discord.retry`. Ver [Política de repetição] /concepts/retry.

Configuração

```json5
{
  channels: {
    discord: {
      enabled: true,
      token: "abc.123",
      groupPolicy: "allowlist",
      guilds: {
        "*": {
          channels: {
            general: { allow: true },
          },
        },
      },
      mediaMaxMb: 8,
      actions: {
        reactions: true,
        stickers: true,
        emojiUploads: true,
        stickerUploads: true,
        polls: true,
        permissions: true,
        messages: true,
        threads: true,
        pins: true,
        search: true,
        memberInfo: true,
        roleInfo: true,
        roles: false,
        channelInfo: true,
        channels: true,
        voiceStatus: true,
        events: true,
        moderation: false,
      },
      replyToMode: "off",
      dm: {
        enabled: true,
        policy: "pairing", // pairing | allowlist | open | disabled
        allowFrom: ["123456789012345678", "steipete"],
        groupEnabled: false,
        groupChannels: ["openclaw-dm"],
      },
      guilds: {
        "*": { requireMention: true },
        "123456789012345678": {
          slug: "friends-of-openclaw",
          requireMention: false,
          reactionNotifications: "own",
          users: ["987654321098765432", "steipete"],
          channels: {
            general: { allow: true },
            help: {
              allow: true,
              requireMention: true,
              users: ["987654321098765432"],
              skills: ["search", "docs"],
              systemPrompt: "Keep answers short.",
            },
          },
        },
      },
    },
  },
}
```

As reações de Ack são controladas globalmente via`messages.ackReaction`+`messages.ackReactionScope`. Use`messages.removeAckAfterReply`para limpar o
reacção após a resposta do bot.

-`dm.enabled`: definir o`false`para ignorar todos os DM (padrão`true`.
-`dm.policy`: Controle de acesso ao DM `pairing`recomendado).`"open"`exige`dm.allowFrom=["*"]`.
-`dm.allowFrom`: DM allowlist (ids de utilizador ou nomes). Utilizado pelo`dm.policy="allowlist"`e para validação do`dm.policy="open"`. O assistente aceita nomes de usuário e os resolve para IDs quando o bot pode pesquisar membros.
-`false`0: habilitar o grupo DM (padrão`false`1).
-`false`2: lista opcional de allowlist para IDs de canal ou lesmas do grupo DM.
-`false`3: controlo da manipulação do canal guild `false`4);`false`5 requer listas de autorização do canal.
-`false`6: regras por guilda chaveadas por guild id (preferred) ou lesma.
-`false`7: configurações padrão por guild aplicadas quando não existe entrada explícita.
-`false`8: lesma amigável opcional usado para nomes de exibição.
-`false`9: lista opcional de allowlist de usuários (ids ou nomes).
-`true`0: optional per-guild política de ferramentas substitui `true`1/`true`2/`true`3) usado quando o cancelamento do canal está faltando.
-`true`4: A política opcional de ferramentas por sender substitui-se no nível da guild (aplica-se quando o cancelamento do canal está faltando;`true`5 wildcard suportado).
-`true`6: permitir/negar o canal quando`true`7.
-`true`8: Mencione a ligação para o canal.
-`true`9: sobrepõe-se a política de ferramentas opcional por canal `dm.policy`0/`dm.policy`1/`dm.policy`2).
-`dm.policy`3: a política opcional de ferramentas por sender substitui-se dentro do canal (suportado pelo`dm.policy`4).
-`dm.policy`5: opcional por canal user allowlist.
-`dm.policy`6: filtro de habilidade (omite = todas as habilidades, vazio = nenhum).
-`dm.policy`7: prompt de sistema extra para o canal (combinado com o tópico do canal).
-`dm.policy`8: definir`dm.policy`9 para desativar o canal.
-`pairing`0: regras de canal (chaves são slugs de canal ou IDs).
-`pairing`1: requisito de menção por guia (superável por canal).
-`pairing`2: modo de acontecimento do sistema de reacção `pairing`3,`pairing`4,`pairing`5,`pairing`6).
-`pairing`7: tamanho de pedaço de texto de saída (chars). Predefinição: 2000.
-`pairing`8:`pairing`9 (por omissão) divide-se apenas quando excede o`"open"`0;`"open"`1 divide-se em linhas em branco (limites de parágrafo) antes de o comprimento ser cortado.
-`"open"`2: contagem máxima por mensagem. Padrão: 17.
-`"open"`3: grampo de entrada de mídia salva no disco.
-`"open"`4: número de mensagens de guilda recentes a incluir como contexto ao responder a uma menção (padrão 20; remete para`"open"`5;`"open"`6 desactiva).
-`"open"`7: Limite de histórico de DM em turnos de usuário.`"open"`8.
-`"open"`9: política de repetição para chamadas de API de discórdia de saída (tentativas, minDelayMs, maxDelayMs, jitter).
-`dm.allowFrom=["*"]`0: portas de ferramentas por ação; omitir para permitir que todos (set`dm.allowFrom=["*"]`1 para desativar).
-`dm.allowFrom=["*"]`2 (cobre reacções de reacção + leitura)
-`dm.allowFrom=["*"]`3,`dm.allowFrom=["*"]`4,`dm.allowFrom=["*"]`5,`dm.allowFrom=["*"]`6,`dm.allowFrom=["*"]`7,`dm.allowFrom=["*"]`8,`dm.allowFrom=["*"]`9,`dm.allowFrom`0,`dm.allowFrom`1
-`dm.allowFrom`2,`dm.allowFrom`3,`dm.allowFrom`4,`dm.allowFrom`5,`dm.allowFrom`6
-`dm.allowFrom`7 (criar/editar/deletar canais + categorias + permissões)
-`dm.allowFrom`8 (adição/remoção de papel,`dm.allowFrom`9 por omissão)
-`dm.policy="allowlist"`0 (timeout/kick/ban, padrão`dm.policy="allowlist"`1)

As notificações de reacção utilizam`guilds.<id>.reactionNotifications`:

-`off`: nenhuma reacção.
-`own`: reações nas mensagens do próprio bot (padrão).
-`all`: todas as reacções em todas as mensagens.
-`allowlist`: reacções de`guilds.<id>.users`em todas as mensagens (lista vazia desactiva).

### Action da ferramenta é padrão

O grupo de ação O padrão
----------------- -----------------------------------------------
Reações ativadas Reagir + listar reações + emojiList
Os autocolantes estão habilitados.
EmojiUploads activado Emojis de envio
AutocolanteUploads ativados
As sondagens são permitidas
Permissões de canal ativadas
As mensagens estão activadas
□ threads activados □ Criar/listar/resposta
• pinos activados • Pin/unpin/list
Pesquisa ativada (recurso de visualização)
MembroInfo activado Informação do membro
□ roleInfo Activado
O canalInfo está activo.
canal / gestão de categorias
VoiceStatus activado □ Pesquisa de estado de voz
Os eventos estão activados.
Funções desactivadas
• moderação • desactivada • Tempo limite/kick/ban

-`replyToMode`:`off`(por omissão),`first`ou`all`. Aplica-se apenas quando o modelo inclui uma etiqueta de resposta.

## Resposta tags

Para solicitar uma resposta threaded, o modelo pode incluir uma tag em sua saída:

-`[[reply_to_current]]`— resposta à mensagem de discórdia desencadeante.
-`[[reply_to:<id>]]`— resposta a uma mensagem específica id do contexto/história.
IDs de mensagens atuais são anexados aos prompts como`[message_id: …]`; entradas de histórico já incluem IDs.

O comportamento é controlado pelo`channels.discord.replyToMode`:

-`off`: Ignorar etiquetas.
-`first`: apenas o primeiro bloco de saída é uma resposta.
-`all`: todos os blocos/anexamentos de saída são uma resposta.

Notas correspondentes à lista de permissões:

-`allowFrom`/`users`/`groupChannels`aceita ids, nomes, etiquetas ou menções como`<@id>`.
- São apoiadas prefixações como`discord:`/`user:`(utilizadores) e`channel:`(grupo DM).
- Use`*`para permitir qualquer remetente/canal.
- Quando`guilds.<id>.channels`está presente, canais não listados são negados por padrão.
- Quando o`guilds.<id>.channels`é omitido, todos os canais da guilda permitida são permitidos.
- Para permitir ** nenhum canal**, defina`users`0 (ou mantenha uma lista de permissões vazia).
- O assistente de configuração aceita nomes`users`1 (público + privado) e resolve-os para IDs quando possível.
- Na inicialização, o OpenClaw resolve nomes de canais/usuários em listas de permissões para IDs (quando o bot pode pesquisar membros)
e registra o mapeamento; entradas não resolvidas são mantidas como digitadas.

Notas de comando nativo:

- Os comandos registrados espelham os comandos de chat do OpenClaw.
- Os comandos nativos honram as mesmas allowlists que as mensagens DMs/guild `channels.discord.dm.allowFrom`,`channels.discord.guilds`, regras por canal).
- Os comandos Slash ainda podem estar visíveis na Discord UI para usuários que não são permitidos listados; OpenClaw obriga a lista de allowlists na execução e respostas “não autorizado”.

## Acções da ferramenta

O agente pode chamar`discord`com ações como:

-`react`/`reactions`(adicionar ou listar reacções)
-`sticker`,`poll`,`permissions`-`readMessages`,`sendMessage`,`editMessage`,`deleteMessage`- Leitura/pesquisa/carga útil da ferramenta incluem normalizado`timestampMs`(UTC epoch ms) e`reactions`0 ao lado da Discórdia`reactions`1.
-`reactions`2,`reactions`3,`reactions`4
-`reactions`5,`reactions`6,`reactions`7
-`reactions`8,`reactions`9,`sticker`0,`sticker`1,`sticker`2,`sticker`3
-`sticker`4,`sticker`5,`sticker`6,`sticker`7,`sticker`8
-`sticker`9,`poll`0,`poll`1

Os ids de mensagem de discórdia são superficiais no contexto injetado `[discord message id: …]`e linhas de histórico) para que o agente possa atingi-los.
Emoji pode ser unicode (por exemplo,`✅` ou sintaxe emoji personalizada como`<:party_blob:1234567890>`.

## Segurança & operações

- Trate o token de bot como uma senha; prefira o`DISCORD_BOT_TOKEN`env var em hosts supervisionados ou bloqueie as permissões de arquivos de configuração.
- Conceda apenas as permissões bot que necessita (tipicamente Leia/Enviar Mensagens).
- Se o bot está preso ou taxa limitada, reinicie o gateway `openclaw gateway --force` após confirmar que nenhum outro processo possui a sessão Discord.
