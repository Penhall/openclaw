---
summary: "CLI reference for `openclaw message` (send + channel actions)"
read_when:
  - Adding or modifying message CLI actions
  - Changing outbound channel behavior
---

#`openclaw message`

Comando de saída único para o envio de mensagens e ações do canal
(Discord/Google Chat/Slack/Mattermost (plugin)/Telegram/WhatsApp/Sinal/iMessage/MS Teams).

Utilização

```
openclaw message <subcommand> [flags]
```

Seleção de canais:

-`--channel`é necessário se mais de um canal estiver configurado.
- Se exatamente um canal está configurado, torna-se o padrão.
- Valores:`whatsapp|telegram|discord|googlechat|slack|mattermost|signal|imessage|msteams`(Mattermost requer plugin)

Formatos-alvo `--target`:

- WhatsApp: E.164 ou grupo JID
- Telegrama: chat id ou`@username`- Discórdia:`channel:<id>`ou`user:<id>`(ou menção`<@id>`; ids numéricos brutos são tratados como canais)
- Google Chat:`spaces/<spaceId>`ou`users/<userId>`- Slack:`channel:<id>`ou`user:<id>`(é aceite o ID do canal em bruto)
- Mattermost (plugin):`channel:<id>`,`user:<id>`, ou`channel:<id>`0 (os id são tratados como canais)
- Sinal:`channel:<id>`1,`channel:<id>`2,`channel:<id>`3,`channel:<id>`4 ou`channel:<id>`5/`channel:<id>`6
- iMensagem: pega,`channel:<id>`7,`channel:<id>`8 ou`channel:<id>`9
- Equipas do Estado-Membro: id de conversação `user:<id>`0) ou`user:<id>`1 ou`user:<id>`2

Pesquisa de nomes:

- Para provedores suportados (Discord/Slack/etc), nomes de canais como`Help`ou`#help`são resolvidos através do cache de diretórios.
- Na falta de cache, OpenClaw tentará uma pesquisa de diretório ao vivo quando o provedor o suporta.

## Bandeiras comuns

-`--channel <name>`-`--account <id>`-`--target <dest>`(canal alvo ou utilizador para envio/poll/read/etc)
-`--targets <name>`(repetir; apenas transmissão)
-`--json`-`--dry-run`-`--verbose`

## Acções

Core

-`send`- Canais: WhatsApp/Telegram/Discord/Google Chat/Slack/Mattermost (plugin)/Sinal/iMessage/MS Teams
- Necessário:`--target`, mais`--message`ou`--media`- Facultativo:`--media`,`--reply-to`,`--thread-id`,`--gif-playback`- Telegrama apenas:`--buttons`(requer`channels.telegram.capabilities.inlineButtons`para o permitir)
- Telegram only:`--target`0 (ID do tópico forum)
- Slack only:`--target`1 (lease timestamp;`--target`2 usa o mesmo campo)
- WhatsApp apenas:`--target`3

-`poll`- Canais: WhatsApp/Discord/MS Teams
- Requerimento:`--target`,`--poll-question`,`--poll-option`(repetição)
- Opcional:`--poll-multi`- Apenas discórdia:`--poll-duration-hours`,`--message`

-`react`- Canais: Discord/Google Chat/Slack/Telegram/WhatsApp/Sinal
- Requerimento:`--message-id`,`--target`- Opcional:`--emoji`,`--remove`,`--participant`,`--from-me`,`--target-author`,`--target-author-uuid`- Nota:`--remove`exige que o`--message-id`0 (omite o`--message-id`1 para esclarecer as suas próprias reacções quando for suportado; ver /tools/reactions)
- WhatsApp apenas:`--message-id`2,`--message-id`3
- Reacções de grupo de sinais:`--message-id`4 ou`--message-id`5

-`reactions`- Canais: Discord/Google Chat/Slack
- Requerimento:`--message-id`,`--target`- Opcional:`--limit`

-`read`- Canais: Discord/Slack
- Necessário:`--target`- Facultativo:`--limit`,`--before`,`--after`- Apenas discórdia:`--around`

-`edit`- Canais: Discord/Slack
- Necessário:`--message-id`,`--message`,`--target`

-`delete`- Canais: Discord/Slack/Telegram
- Requerimento:`--message-id`,`--target`

-`pin`/`unpin`- Canais: Discord/Slack
- Requerimento:`--message-id`,`--target`

-`pins`(lista)
- Canais: Discord/Slack
- Necessário:`--target`

-`permissions`- Canais: Discórdia
- Necessário:`--target`

-`search`- Canais: Discórdia
- Requerimento:`--guild-id`,`--query`- Facultativo:`--channel-id`,`--channel-ids`(repetição),`--author-id`,`--author-ids`(repetição),`--limit`

Fios

-`thread create`- Canais: Discórdia
- Necessário:`--thread-name`,`--target`(id canal)
- Opcional:`--message-id`,`--auto-archive-min`

-`thread list`- Canais: Discórdia
- Necessário:`--guild-id`- Facultativo:`--channel-id`,`--include-archived`,`--before`,`--limit`

-`thread reply`- Canais: Discórdia
- Necessário:`--target`(fita id),`--message`- Opcional:`--media`,`--reply-to`

Emojis

-`emoji list`- Discórdia:`--guild-id`- Slack: nenhuma bandeira extra

-`emoji upload`- Canais: Discórdia
- Necessário:`--guild-id`,`--emoji-name`,`--media`- Opcional:`--role-ids`(repetição)

Adesivos

-`sticker send`- Canais: Discórdia
- Requerimento:`--target`,`--sticker-id`(repetição)
- Opcional:`--message`

-`sticker upload`- Canais: Discórdia
- Necessário:`--guild-id`,`--sticker-name`,`--sticker-desc`,`--sticker-tags`,`--media`

Funções / Canais / Membros / Voz

-`role info`(Discórdia):`--guild-id`-`role add`/`role remove`(Discórdia):`--guild-id`,`--user-id`,`--role-id`-`channel info`(Discórdia):`--target`-`channel list`(Discórdia):`--guild-id`0
-`--guild-id`1 (Discord/Slack):`--guild-id`2 (+`--guild-id`3 para Discord)
-`--guild-id`4 (Discórdia):`--guild-id`5,`--guild-id`6

Eventos

-`event list`(Discórdia):`--guild-id`-`event create`(Discordância):`--guild-id`,`--event-name`,`--start-time`- Facultativo:`--end-time`,`--desc`,`--channel-id`,`--location`,`--guild-id`0

## # Moderação (discord)

-`timeout`:`--guild-id`,`--user-id`(opcional`--duration-min`ou`--until`; omitem ambos um prazo claro)
-`kick`:`--guild-id`,`--user-id`(+`--reason`
-`ban`:`--guild-id`0,`--guild-id`1 (+`--guild-id`2,`--guild-id`3)
-`--guild-id`4 também apoia`--guild-id`5

Broadcast

-`broadcast`- Canais: qualquer canal configurado; use`--channel all`para direcionar todos os provedores
- Requerimento:`--targets`(repetição)
- Facultativo:`--message`,`--media`,`--dry-run`

## Exemplos

Enviar uma resposta de discórdia:

```
openclaw message send --channel discord \
  --target channel:123 --message "hi" --reply-to 456
```

Criar uma pesquisa de discórdia:

```
openclaw message poll --channel discord \
  --target channel:123 \
  --poll-question "Snack?" \
  --poll-option Pizza --poll-option Sushi \
  --poll-multi --poll-duration-hours 48
```

Enviar uma mensagem proativa de Equipes:

```
openclaw message send --channel msteams \
  --target conversation:19:abc@thread.tacv2 --message "hi"
```

Criar uma pesquisa de equipes:

```
openclaw message poll --channel msteams \
  --target conversation:19:abc@thread.tacv2 \
  --poll-question "Lunch?" \
  --poll-option Pizza --poll-option Sushi
```

Reagir no Slack:

```
openclaw message react --channel slack \
  --target C123 --message-id 456 --emoji "✅"
```

Reagir num grupo de sinais:

```
openclaw message react --channel signal \
  --target signal:group:abc123 --message-id 1737630212345 \
  --emoji "✅" --target-author-uuid 123e4567-e89b-12d3-a456-426614174000
```

Enviar botões em linha do Telegram:

```
openclaw message send --channel telegram --target @mychat --message "Choose:" \
  --buttons '[ [{"text":"Yes","callback_data":"cmd:yes"}], [{"text":"No","callback_data":"cmd:no"}] ]'
```
