---
summary: "CLI reference for `openclaw channels` (accounts, status, login/logout, logs)"
read_when:
  - You want to add/remove channel accounts (WhatsApp/Telegram/Discord/Google Chat/Slack/Mattermost (plugin)/Signal/iMessage)
  - You want to check channel status or tail channel logs
---

#`openclaw channels`

Gerencie contas de canais de chat e seu status de execução no Gateway.

Documentos relacionados:

- Guias de canais: [Canais] /channels/index
- Configuração do portal: [Configuração] /gateway/configuration

## Comandos comuns

```bash
openclaw channels list
openclaw channels status
openclaw channels capabilities
openclaw channels capabilities --channel discord --target channel:123
openclaw channels resolve --channel slack "#general" "@jane"
openclaw channels logs --channel all
```

## Adicionar / remover contas

```bash
openclaw channels add --channel telegram --token <bot-token>
openclaw channels remove --channel telegram --delete
```

Dica:`openclaw channels add --help`mostra bandeiras por canal (token, token app, signal-cli paths, etc).

## Login / logout (interactivo)

```bash
openclaw channels login --channel whatsapp
openclaw channels logout --channel whatsapp
```

## Resolução de problemas

- Execute`openclaw status --deep`para uma sonda ampla.
- Use`openclaw doctor`para correções guiadas.
-`openclaw channels list`imprime`Claude: HTTP 403 ... user:profile`→ instantâneo de uso precisa do escopo`user:profile`. Use`--no-usage`, ou forneça uma chave de sessão claude.ai `CLAUDE_WEB_SESSION_KEY`/`CLAUDE_WEB_COOKIE`, ou reaite via Claude Code CLI.

## Sonda de capacidades

Obter dicas de capacidade do provedor (intenções/escopos onde disponíveis) mais suporte de recursos estáticos:

```bash
openclaw channels capabilities
openclaw channels capabilities --channel discord --target channel:123
```

Notas:

-`--channel`é opcional; omiti-lo para listar todos os canais (incluindo extensões).
-`--target`aceita`channel:<id>`ou um id de canal numérico bruto e só se aplica à Discórdia.
- Sondas são específicas do provedor: intenção de discórdia + permissões de canal opcionais; bot Slack + escopos do usuário; sinalizadores de bots de Telegram + webhook; daemon de sinal versão; token de aplicativo de MS Teams + papéis/escopos de gráfico (anotados onde conhecido). Canais sem sondas informam`Probe: unavailable`.

## Resolver nomes para IDs

Resolver nomes de canal/usuário para IDs usando o diretório do provedor:

```bash
openclaw channels resolve --channel slack "#general" "@jane"
openclaw channels resolve --channel discord "My Server/#support" "@someone"
openclaw channels resolve --channel matrix "Project Room"
```

Notas:

- Use`--kind user|group|auto`para forçar o tipo alvo.
- Resolução prefere jogos ativos quando vários itens compartilham o mesmo nome.
