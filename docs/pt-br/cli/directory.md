---
summary: "CLI reference for `openclaw directory` (self, peers, groups)"
read_when:
  - You want to look up contacts/groups/self ids for a channel
  - You are developing a channel directory adapter
---

#`openclaw directory`

Pesquisa de diretórios para canais que o suportam (contatos/parceiros, grupos e “eu”).

## Bandeiras comuns

-`--channel <name>`: id/alias do canal (obrigatório quando vários canais são configurados; auto quando apenas um é configurado)
-`--account <id>`: conta id (padrão: canal padrão)
-`--json`: saída JSON

## Notas

-`directory`é destinado para ajudá-lo a encontrar IDs que você pode colar em outros comandos (especialmente`openclaw message send --target ...`.
- Para muitos canais, os resultados são confirmados (allowlists / grupos configurados) em vez de um diretório de provedores ao vivo.
- Saída padrão é`id`(e às vezes`name` separado por uma aba; use`--json`para scripting.

## Usando resultados com`message send`

```bash
openclaw directory peers list --channel slack --query "U0"
openclaw message send --channel slack --target user:U012ABCDEF --message "hello"
```

## Formatos de identificação (por canal)

- WhatsApp:`+15551234567`(DM),`1234567890-1234567890@g.us`(grupo)
- Telegram:`@username`ou ID de chat numérico; grupos são IDs numéricos
- Slack:`user:U…`e`channel:C…`- Discórdia:`user:<id>`e`channel:<id>`- Matriz (plugin):`user:@user:server`,`room:!roomId:server`, ou`#alias:server`- Equipas Microsoft (plugin):`1234567890-1234567890@g.us`0 e`1234567890-1234567890@g.us`1
- Zalo (plugin): ID do usuário (Bot API)
- Zalo Personal /`1234567890-1234567890@g.us`2 (plugin): thread id (DM/grupo) de`1234567890-1234567890@g.us`3 `1234567890-1234567890@g.us`4,`1234567890-1234567890@g.us`5,`1234567890-1234567890@g.us`6)

## Eu próprio (“eu”)

```bash
openclaw directory self --channel zalouser
```

## Parceiros (contactos/utilizadores)

```bash
openclaw directory peers list --channel zalouser
openclaw directory peers list --channel zalouser --query "name"
openclaw directory peers list --channel zalouser --limit 50
```

## Grupos

```bash
openclaw directory groups list --channel zalouser
openclaw directory groups list --channel zalouser --query "work"
openclaw directory groups members --channel zalouser --group-id <id>
```
