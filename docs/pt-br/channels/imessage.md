---
summary: "iMessage support via imsg (JSON-RPC over stdio), setup, and chat_id routing"
read_when:
  - Setting up iMessage support
  - Debugging iMessage send/receive
---

# iMessage (imsg)

Estado: integração CLI externa. Gateway gera`imsg rpc`(JSON-RPC sobre stdio).

## Montagem rápida (início)

1. Assegure-se de que as mensagens são assinadas neste Mac.
2. Instalar`imsg`:
-`brew install steipete/tap/imsg`3. Configure Openclaw com`channels.imessage.cliPath`e`channels.imessage.dbPath`.
4. Inicie o gateway e aprove todos os prompts do macOS (Automação + Acesso ao disco completo).

Configuração mínima:

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "/usr/local/bin/imsg",
      dbPath: "/Users/<you>/Library/Messages/chat.db",
    },
  },
}
```

## O que é

- canal iMessage apoiado pelo`imsg`no macOS.
- Roteamento determinístico: respostas sempre voltar para iMessage.
- Os DMs compartilham a sessão principal do agente; os grupos são isolados `agent:<agentId>:imessage:group:<chat_id>`.
- Se um fio multiparticipante chegar com`is_group=false`, poderá ainda isolá- lo através do`chat_id`utilizando o`channels.imessage.groups`(ver “linhas de grupo” abaixo).

## A configuração escreve

Por padrão, o iMessage pode escrever atualizações de configuração acionadas pelo`/config set|unset`(requer`commands.config: true`.

Desactivar com:

```json5
{
  channels: { imessage: { configWrites: false } },
}
```

## Requisitos

- MacOS com mensagens assinadas.
- Acesso completo ao disco para OpenClaw +`imsg`(Acesso DB de mensagens).
- Autorização de automatização ao enviar.
-`channels.imessage.cliPath`pode apontar para qualquer comando que proxies stdin/stdout (por exemplo, um script de embrulho que SSHes para outro Mac e executa`imsg rpc`.

## Configuração (caminho rápido)

1. Assegure-se de que as mensagens são assinadas neste Mac.
2. Configure iMessage e inicie o gateway.

## # Usuário dedicado do macOS (para identidade isolada)

Se você quiser que o bot envie de uma identidade **separada iMessage** (e mantenha suas Mensagens pessoais limpas), use um ID Apple dedicado + um usuário macOS dedicado.

1. Crie um ID Apple dedicado (exemplo:`my-cool-bot@icloud.com`.
- A Apple pode exigir um número de telefone para verificação / 2FA.
2. Crie um usuário macOS (exemplo:`openclawhome` e entre nele.
3. Abra Mensagens no usuário do macOS e entre no iMessage usando o bot Apple ID.
4. Habilite o login remoto (Configurações do sistema → Geral → Compartilhamento → Login remoto).
5. Instalar`imsg`:
-`brew install steipete/tap/imsg`6. Configurar SSH assim`ssh <bot-macos-user>@localhost true`funciona sem senha.
7. Ponto`channels.imessage.accounts.bot.cliPath`em um invólucro SSH que executa`imsg`como o usuário de bot.

Nota de primeira execução: o envio/receção pode exigir aprovações GUI (Automação + Acesso a Discos Completos) no  bot macOS user . Se`imsg rpc`parecer preso ou sair, faça logon nesse usuário (Screen Shareing ajuda), execute um`imsg chats --limit 1`/`imsg send ...`, aprove prompts, então tente novamente.

Embalagem de exemplo `chmod +x`. Substituir`<bot-macos-user>`pelo seu nome de utilizador macOS real:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Run an interactive SSH once first to accept host keys:
#   ssh <bot-macos-user>@localhost true
exec /usr/bin/ssh -o BatchMode=yes -o ConnectTimeout=5 -T <bot-macos-user>@localhost \
  "/usr/local/bin/imsg" "$@"
```

Configuração do exemplo:

```json5
{
  channels: {
    imessage: {
      enabled: true,
      accounts: {
        bot: {
          name: "Bot",
          enabled: true,
          cliPath: "/path/to/imsg-bot",
          dbPath: "/Users/<bot-macos-user>/Library/Messages/chat.db",
        },
      },
    },
  },
}
```

Para configurações de conta única, use opções planas `channels.imessage.cliPath`,`channels.imessage.dbPath` em vez do mapa`accounts`.

## # Variante remota/SSH (opcional)

Se você quiser o iMessage em outro Mac, configure o`channels.imessage.cliPath`para uma embalagem que executa o`imsg`no host remoto do macOS sobre o SSH. Openclaw só precisa de stdio.

Embalagem de exemplo:

```bash
#!/usr/bin/env bash
exec ssh -T gateway-host imsg "$@"
```

** Anexos remotos: ** Quando`cliPath`aponta para um host remoto via SSH, os caminhos de anexos nos arquivos de referência do banco de dados Mensagens na máquina remota. OpenClaw pode obter automaticamente estes sobre SCP, definindo`channels.imessage.remoteHost`:

```json5
{
  channels: {
    imessage: {
      cliPath: "~/imsg-ssh", // SSH wrapper to remote Mac
      remoteHost: "user@gateway-host", // for SCP file transfer
      includeAttachments: true,
    },
  },
}
```

Se`remoteHost`não estiver definido, o OpenClaw tenta detectá-lo automaticamente, processando o comando SSH em seu script de wrapper. A configuração explícita é recomendada para a confiabilidade.

### # Mac remoto via Tailscale (exemplo)

Se o Gateway é executado em um host/VM Linux mas iMessage deve ser executado em um Mac, Tailscale é a ponte mais simples: o Gateway fala com o Mac sobre a tailnet, corre`imsg`via SSH, e os anexos SCPs voltam.

Arquitetura:

```
┌──────────────────────────────┐          SSH (imsg rpc)          ┌──────────────────────────┐
│ Gateway host (Linux/VM)      │──────────────────────────────────▶│ Mac with Messages + imsg │
│ - openclaw gateway           │          SCP (attachments)        │ - Messages signed in     │
│ - channels.imessage.cliPath  │◀──────────────────────────────────│ - Remote Login enabled   │
└──────────────────────────────┘                                   └──────────────────────────┘
              ▲
              │ Tailscale tailnet (hostname or 100.x.y.z)
              ▼
        user@gateway-host
```

Exemplo de configuração de betão (nome da máquina em escala de caracteres):

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "~/.openclaw/scripts/imsg-ssh",
      remoteHost: "bot@mac-mini.tailnet-1234.ts.net",
      includeAttachments: true,
      dbPath: "/Users/bot/Library/Messages/chat.db",
    },
  },
}
```

Embalagem de exemplo `~/.openclaw/scripts/imsg-ssh`:

```bash
#!/usr/bin/env bash
exec ssh -T bot@mac-mini.tailnet-1234.ts.net imsg "$@"
```

Notas:

- Certifique-se de que o Mac está conectado às Mensagens e que o Login Remoto está ativado.
- Use chaves SSH para`ssh bot@mac-mini.tailnet-1234.ts.net`funciona sem prompts.
-`remoteHost`deve corresponder ao alvo SSH para que o SCP possa obter anexos.

Suporte multi-conta: use`channels.imessage.accounts`com configuração por conta e opcional`name`. Ver `gateway/configuration`/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts para o padrão partilhado. Não commit`~/.openclaw/openclaw.json`(com frequência contém tokens).

## Controle de acesso (DMs + grupos)

DM:

- Predefinição:`channels.imessage.dmPolicy = "pairing"`.
- Os remetentes desconhecidos recebem um código de pareamento; as mensagens são ignoradas até serem aprovadas (os códigos expiram após 1 hora).
- Aprovar via:
-`openclaw pairing list imessage`-`openclaw pairing approve imessage <CODE>`- Emparelhamento é a troca de token padrão para DMs iMessage. Detalhes: [Pairing] /start/pairing

Grupos:

-`channels.imessage.groupPolicy = open | allowlist | disabled`.
- Controlos`channels.imessage.groupAllowFrom`que podem desencadear em grupos quando o`allowlist`é definido.
- Mention gating usa`agents.list[].groupChat.mentionPatterns`(ou`messages.groupChat.mentionPatterns` porque iMessage não tem metadados nativos de menção.
- Substituição multi-agente: definir padrões por agente em`agents.list[].groupChat.mentionPatterns`.

## Como funciona (comportamento)

-`imsg`transmite eventos de mensagens; o gateway normaliza-os no envelope de canais compartilhados.
- Respostas sempre encaminhar de volta para o mesmo chat ID ou manusear.

## Linhas em grupo `is_group=false`

Alguns threads iMessage podem ter vários participantes, mas ainda chegam com`is_group=false`dependendo de como Mensagens armazenam o identificador de chat.

Se você configurar explicitamente um`chat_id`sob`channels.imessage.groups`, OpenClaw trata esse tópico como um “grupo” para:

- isolamento de sessão (chave de sessão separada`agent:<agentId>:imessage:group:<chat_id>`
- grupo allowlisting / mention gating behavior

Exemplo:

```json5
{
  channels: {
    imessage: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15555550123"],
      groups: {
        "42": { requireMention: false },
      },
    },
  },
}
```

Isso é útil quando você quer uma personalidade/modelo isolada para um thread específico (veja [Roteamento multi-agente]/concepts/multi-agent. Para isolamento do sistema de arquivos, veja [Sandboxing]/gateway/sandboxing.

## Mídia + limites

- Ingestão opcional de fixação via`channels.imessage.includeAttachments`.
- Tampa de mídia via`channels.imessage.mediaMaxMb`.

## Limites

- O texto de saída é cortado para`channels.imessage.textChunkLimit`(padrão 4000).
- Opcional nova linha de blocos: definir`channels.imessage.chunkMode="newline"`para dividir em linhas em branco (limites de parágrafo) antes do comprimento de blocos.
- Os uploads de mídia são tampados pelo`channels.imessage.mediaMaxMb`(padrão 16).

## Endereçamento / alvos de entrega

Preferir`chat_id`para roteamento estável:

-`chat_id:123`(preferido)
-`chat_guid:...`-`chat_identifier:...`- pegas directas:`imessage:+1555`/`sms:+1555`/`user@example.com`

Listar conversas:

```
imsg chats --limit 20
```

## Referência de configuração (iMessage)

Configuração completa: [Configuração]/gateway/configuration

Opções do fornecedor:

-`channels.imessage.enabled`: activar/desactivar a inicialização do canal.
-`channels.imessage.cliPath`: caminho para`imsg`.
- Mensagens DB caminho.
-`channels.imessage.remoteHost`: Servidor SSH para transferência de anexos SCP quando`cliPath`aponta para um Mac remoto (por exemplo,`user@gateway-host`. Auto-detectado a partir do invólucro SSH se não estiver definido.
-`channels.imessage.service`:`imessage | sms | auto`.
-`channels.imessage.region`: região SMS.
-`channels.imessage.cliPath`0:`channels.imessage.cliPath`1 (por omissão: emparelhamento).
-`channels.imessage.cliPath`2: DM allowlist (handles, emails, números E.164 ou`channels.imessage.cliPath`3).`channels.imessage.cliPath`4 exige`channels.imessage.cliPath`5. O iMessage não tem nomes de utilizador; use manipuladores ou alvos de chat.
-`channels.imessage.cliPath`6:`channels.imessage.cliPath`7 (default: allowlist).
-`channels.imessage.cliPath`8: lista de remetentes de grupo.
-`channels.imessage.cliPath`9 /`imsg`0: mensagens de grupo máximas para incluir como contexto (0 desabilita).
-`imsg`1: Limite de histórico de DM em turnos de usuário.`imsg`2.
-`imsg`3: padrões por grupo + allowlist (use`imsg`4 para padrões globais).
-`imsg`5: ingerir anexos no contexto.
-`imsg`6: capa de suporte de entrada/saída (MB).
-`imsg`7: tamanho do pedaço de saída (chars).
-`imsg`8:`imsg`9 (padrão) ou`channels.imessage.dbPath`0 para dividir em linhas em branco (limites de parágrafos) antes do corte do comprimento.

Opções globais relacionadas:

-`agents.list[].groupChat.mentionPatterns`(ou`messages.groupChat.mentionPatterns`.
-`messages.responsePrefix`.
