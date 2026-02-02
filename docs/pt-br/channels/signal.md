---
summary: "Signal support via signal-cli (JSON-RPC + SSE), setup, and number model"
read_when:
  - Setting up Signal support
  - Debugging Signal send/receive
---

# Sinal (sinal-cli)

Estado: integração CLI externa. Gateway fala com`signal-cli`sobre HTTP JSON-RPC + SSE.

## Montagem rápida (início)

1. Use um número de sinal ** separado para o bot (recomendado).
2. Instalar`signal-cli`(o que é necessário para o Java).
3. Link o dispositivo bot e iniciar o daemon:
-`signal-cli link -n "OpenClaw"`4. Configure OpenClaw e inicie o gateway.

Configuração mínima:

```json5
{
  channels: {
    signal: {
      enabled: true,
      account: "+15551234567",
      cliPath: "signal-cli",
      dmPolicy: "pairing",
      allowFrom: ["+15557654321"],
    },
  },
}
```

## O que é

- Canal de sinal via`signal-cli`(libsignal não incorporado).
- Roteamento determinístico: respostas sempre voltar para Signal.
- Os DMs compartilham a sessão principal do agente; os grupos são isolados `agent:<agentId>:signal:group:<groupId>`.

## A configuração escreve

Por padrão, Signal é permitido escrever atualizações de configuração acionadas pelo`/config set|unset`(requer`commands.config: true`.

Desactivar com:

```json5
{
  channels: { signal: { configWrites: false } },
}
```

## O modelo numérico (importante)

- O gateway se conecta a um dispositivo **Signal** (a conta`signal-cli`.
- Se você executar o bot em ** sua conta pessoal Signal**, ele irá ignorar suas próprias mensagens (proteção de loop).
- Para "Eu texto o bot e ele responde", use um ** número de bot separado**.

## Configuração (caminho rápido)

1. Instale o`signal-cli`(exigido o Java).
2. Vincular uma conta bot:
-`signal-cli link -n "OpenClaw"`e escaneie o QR em sinal.
3. Configurar o sinal e iniciar o gateway.

Exemplo:

```json5
{
  channels: {
    signal: {
      enabled: true,
      account: "+15551234567",
      cliPath: "signal-cli",
      dmPolicy: "pairing",
      allowFrom: ["+15557654321"],
    },
  },
}
```

Suporte multi-conta: use`channels.signal.accounts`com configuração por conta e opcional`name`. Ver `gateway/configuration`/gateway/configuration#telegramaccounts--discordaccounts--slackaccounts--signalaccounts--imessageaccounts para o padrão partilhado.

## Modo de servidor externo (httpUrl)

Se você quiser gerenciar o`signal-cli`você mesmo (iniciações lentas do JVM frias, entrada do recipiente ou CPUs compartilhadas), execute o daemon separadamente e aponte OpenClaw para ele:

```json5
{
  channels: {
    signal: {
      httpUrl: "http://127.0.0.1:8080",
      autoStart: false,
    },
  },
}
```

Isto salta automaticamente e a inicialização espera dentro do OpenClaw. Para inícios lentos quando auto-spawning, definir`channels.signal.startupTimeoutMs`.

## Controle de acesso (DMs + grupos)

DM:

- Predefinição:`channels.signal.dmPolicy = "pairing"`.
- Os remetentes desconhecidos recebem um código de pareamento; as mensagens são ignoradas até serem aprovadas (os códigos expiram após 1 hora).
- Aprovar via:
-`openclaw pairing list signal`-`openclaw pairing approve signal <CODE>`- Emparelhamento é a troca padrão do token para DMs de sinal. Detalhes: [Pairing] /start/pairing
- Os expedidores exclusivamente UUID (do`sourceUuid` são armazenados como`uuid:<id>`no`channels.signal.allowFrom`.

Grupos:

-`channels.signal.groupPolicy = open | allowlist | disabled`.
- Controlos`channels.signal.groupAllowFrom`que podem desencadear em grupos quando o`allowlist`é definido.

## Como funciona (comportamento)

-`signal-cli`é executado como um daemon; o gateway lê eventos via SSE.
- As mensagens de entrada são normalizadas no envelope do canal partilhado.
- Respostas sempre voltar para o mesmo número ou grupo.

## Mídia + limites

- O texto de saída é cortado para`channels.signal.textChunkLimit`(padrão 4000).
- Opcional nova linha de blocos: definir`channels.signal.chunkMode="newline"`para dividir em linhas em branco (limites de parágrafo) antes do comprimento de blocos.
- Anexos suportados (base64 obtidos do`signal-cli`.
- Cap de mídia padrão:`channels.signal.mediaMaxMb`(padrão 8).
- Use`channels.signal.ignoreAttachments`para pular mídia de download.
- O contexto histórico dos grupos utiliza o`channels.signal.historyLimit`(ou o`channels.signal.accounts.*.historyLimit`, que remonta ao`messages.groupChat.historyLimit`. Definir`0`para desabilitar (padrão 50).

## Datilografia + recibos de leitura

- ** Indicadores de tipagem**: OpenClaw envia sinais de digitação via`signal-cli sendTyping`e os atualiza enquanto uma resposta está sendo executada.
- **Ler recibos**: quando`channels.signal.sendReadReceipts`é verdadeiro, o OpenClaw encaminha recibos para DM permitidos.
- Signal-cli não expõe recibos de leitura para grupos.

## Reações (ferramenta de mensagem)

- Utilizar`message action=react`com`channel=signal`.
- Alvos: remetente E.164 ou UUID (use`uuid:<id>`da saída de emparelhamento; UUID nu também funciona).
-`messageId`é o sinal de hora para a mensagem que você está reagindo.
- As reacções de grupo exigem`targetAuthor`ou`targetAuthorUuid`.

Exemplos:

```
message action=react channel=signal target=uuid:123e4567-e89b-12d3-a456-426614174000 messageId=1737630212345 emoji=🔥
message action=react channel=signal target=+15551234567 messageId=1737630212345 emoji=🔥 remove=true
message action=react channel=signal target=signal:group:<groupId> targetAuthor=uuid:<sender-uuid> messageId=1737630212345 emoji=✅
```

Configuração:

-`channels.signal.actions.reactions`: activar/desactivar acções de reacção (padrão true).
-`channels.signal.reactionLevel`:`off | ack | minimal | extensive`.
-`off`/`ack`desactiva as reacções dos agentes (a ferramenta de mensagem`react`irá errar).
-`minimal`/`extensive`permite reacções do agente e define o nível de orientação.
- Por conta substitui:`channels.signal.accounts.<id>.actions.reactions`,`channels.signal.accounts.<id>.reactionLevel`.

## Alvos de entrega (CLI/cron)

- DM:`signal:+15551234567`(ou E.164).
- DM UUID:`uuid:<id>`(ou UUID nu).
- Grupos`signal:group:<groupId>`.
- Usuários:`username:<name>`(se suportado pela sua conta Signal).

## Referências de configuração (sinal)

Configuração completa: [Configuração]/gateway/configuration

Opções do fornecedor:

-`channels.signal.enabled`: activar/desactivar a inicialização do canal.
-`channels.signal.account`: E.164 para a conta bot.
-`channels.signal.cliPath`: trajecto para`signal-cli`.
-`channels.signal.httpUrl`: URL completo do servidor (sobrepõe a máquina/porta).
-`channels.signal.httpHost`,`channels.signal.httpPort`: ligação do daemon (padrão 127.0.0.1:8080).
-`channels.signal.autoStart`: daemon automático (padrão true se o`httpUrl`estiver desligado).
-`channels.signal.startupTimeoutMs`: tempo limite de espera de arranque em ms (cap 120000).
-`channels.signal.account`0:`channels.signal.account`1.
-`channels.signal.account`2: saltar downloads anexos.
-`channels.signal.account`3: Ignorar histórias do daemon.
-`channels.signal.account`4: recibos de leitura.
-`channels.signal.account`5:`channels.signal.account`6 (padrão: emparelhamento).
-`channels.signal.account`7: Lista de autorizações de DM (E.164 ou`channels.signal.account`8).`channels.signal.account`9 exige`channels.signal.cliPath`0. O sinal não tem nomes de utilizador; use IDs de telefone/UUID.
-`channels.signal.cliPath`1:`channels.signal.cliPath`2 (default: allowlist).
-`channels.signal.cliPath`3: lista de remetentes de grupo.
-`channels.signal.cliPath`4: mensagens de grupo máximas para incluir como contexto (0 desactiva).
-`channels.signal.cliPath`5: Limite de histórico de DM em turnos de usuário.`channels.signal.cliPath`6.
-`channels.signal.cliPath`7: tamanho do pedaço de saída (chars).
-`channels.signal.cliPath`8:`channels.signal.cliPath`9 (padrão) ou`signal-cli`0 para dividir em linhas em branco (limites de parágrafos) antes do corte do comprimento.
-`signal-cli`1: tampa de suporte de entrada/saída (MB).

Opções globais relacionadas:

-`agents.list[].groupChat.mentionPatterns`(sinal não suporta menções nativas).
-`messages.groupChat.mentionPatterns`(regresso global).
-`messages.responsePrefix`.
