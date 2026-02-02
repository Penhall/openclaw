---
summary: "Reaction semantics shared across channels"
read_when:
  - Working on reactions in any channel
---

Ferramentas de reacção

Semantica de reação compartilhada entre canais:

- `emoji` é necessário quando se adiciona uma reacção.
- <<CODE1> remove a(s) reacção(ões) do bot quando suportado(s).
- <<CODE2> remove o emoji especificado quando suportado (requer `emoji`).

Notas do canal:

- **Discord/Slack**: vazio `emoji` remove todas as reações do bot na mensagem; <<CODE1> remove apenas esse emoji.
- ** Google Chat**: vazio `emoji` remove as reações do aplicativo na mensagem; `remove: true` remove apenas esse emoji.
- **Telegrama**: vazio `emoji` remove as reações do bot; <<CODE5> também remove reações, mas ainda requer um não vazio `emoji` para validação da ferramenta.
- ** WhatsApp**: vazio `emoji` remove a reação bot; `remove: true` mapas para emoji vazio (ainda requer `emoji`).
- **Signal**: as notificações de reacção de entrada emitem eventos do sistema quando `channels.signal.reactionNotifications` estiver activa.
