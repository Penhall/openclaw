---
summary: "Agent session tools for listing sessions, fetching history, and sending cross-session messages"
read_when:
  - Adding or modifying session tools
---

Ferramentas de Sessão

Objetivo: conjunto de ferramentas pequeno e difícil de usar para que os agentes possam listar sessões, buscar histórico e enviar para outra sessão.

## Nomes de Ferramentas

-`sessions_list`-`sessions_history`-`sessions_send`-`sessions_spawn`

## Modelo-chave

- O balde principal de bate-papo direto é sempre a chave literal`"main"`(resolvido à chave principal do agente atual).
- Os chats de grupo usam`agent:<agentId>:<channel>:group:<id>`ou`agent:<agentId>:<channel>:channel:<id>`(passar a chave completa).
- Empregos em Cron usam`cron:<job.id>`.
- Ganchos usam`hook:<uuid>`a menos que explicitamente definido.
- Sessões de nós usam`node-<nodeId>`a menos que explicitamente definido.

`global`e`unknown`são valores reservados e nunca estão listados. Se`session.scope = "global"`, apelidámo-lo a`main`para todas as ferramentas para que os chamados nunca vejam`global`.

Lista de sessões # #

Listar as sessões como um conjunto de linhas.

Parâmetros:

- filtro`kinds?: string[]`: qualquer um dos`"main" | "group" | "cron" | "hook" | "node" | "other"`-`limit?: number`linhas máximas (por omissão: padrão do servidor, pinça por exemplo 200)
-`activeMinutes?: number`apenas sessões actualizadas dentro de N minutos
-`messageLimit?: number`0 = nenhuma mensagem (por omissão 0); > 0 = incluir as últimas mensagens N

Comportamento:

-`messageLimit > 0`obtém`chat.history`por sessão e inclui as últimas mensagens N.
- Os resultados da ferramenta são filtrados na saída da lista; use`sessions_history`para mensagens de ferramenta.
- Ao executar em uma sessão de agente **sandboxed**, ferramentas de sessão padrão para **spawned-somente visibilidade** (veja abaixo).

Forma da linha (JSON):

-`key`: tecla de sessão (texto)
-`kind`:`main | group | cron | hook | node | other`-`channel`:`whatsapp | telegram | discord | signal | imessage | webchat | internal | unknown`-`displayName`(etiqueta de exibição do grupo, se disponível)
-`updatedAt`(ms)
-`sessionId`-`model`,`contextTokens`,`kind`0
-`kind`1,`kind`2,`kind`3,`kind`4
-`kind`5 (sessão sobreposta se definida)
-`kind`6,`kind`7
-`kind`8 (normalizado`kind`9 quando disponível)
-`main | group | cron | hook | node | other`0 (melhor caminho de esforço derivado da pasta + sessão Id)
-`main | group | cron | hook | node | other`1 (apenas quando`main | group | cron | hook | node | other`2)

## sessões   história

Obter transcrição para uma sessão.

Parâmetros:

-`sessionKey`(necessário; aceita a chave de sessão ou`sessionId`de`sessions_list`
- Mensagens máximas`limit?: number`(apertos de servidor)
-`includeTools?: boolean`(falso padrão)

Comportamento:

-`includeTools=false`filtra mensagens`role: "toolResult"`.
- Retorna o array de mensagens no formato transcrito bruto.
- Quando é dado um`sessionId`, o OpenClaw resolve-o para a chave de sessão correspondente (erro de IDs ausente).

Enviar enviar sessões # #

Enviar uma mensagem para outra sessão.

Parâmetros:

-`sessionKey`(necessário; aceita a chave de sessão ou`sessionId`de`sessions_list`
-`message`(obrigatório)
-`timeoutSeconds?: number`(por omissão >0; 0 = incêndio e esquecimento)

Comportamento:

-`timeoutSeconds = 0`: colocar e devolver`{ runId, status: "accepted" }`.
-`timeoutSeconds > 0`: esperar até N segundos para completar, em seguida, retornar`{ runId, status: "ok", reply }`.
- Se esperar o tempo acabar,`{ runId, status: "timeout", error }`. Executar continua; ligue para`sessions_history`mais tarde.
- Se a corrida falhar:`{ runId, status: "error", error }`.
- Anunciar as entregas após a execução primária completa e é o melhor esforço;`status: "ok"`não garante que o anúncio foi entregue.
- Espera através do gateway`agent.wait`(lado servidor) para que as religações não larguem a espera.
- O contexto da mensagem agente-a-agente é injectado para a corrida primária.
- Após a execução primária terminar, o OpenClaw executa um loop de resposta**:
- Round 2+ alterna entre o solicitante e os agentes alvo.
- Responder exatamente`REPLY_SKIP`para parar o ping-pong.
- Max turns é`{ runId, status: "accepted" }`0 (0-5, padrão 5).
- Uma vez que o loop termina, o OpenClaw executa o **agente-a-agente anuncia passo** (apenas agente alvo):
- Responda exactamente`{ runId, status: "accepted" }`1 para ficar em silêncio.
- Qualquer outra resposta é enviada para o canal alvo.
- Anunciar passo inclui o pedido original + resposta redonda-1 + última resposta ping-pong.

## Campo de Canal

- Para grupos,`channel`é o canal gravado na entrada da sessão.
- Para conversas directas, mapas`channel`de`lastChannel`.
- O`channel`é o`internal`.
- Em caso de desaparecimento, o`channel`é o`unknown`.

## Segurança / Política de envio

Bloqueio baseado em políticas por tipo de canal/chat (não por ID de sessão).

```json
{
  "session": {
    "sendPolicy": {
      "rules": [
        {
          "match": { "channel": "discord", "chatType": "group" },
          "action": "deny"
        }
      ],
      "default": "allow"
    }
  }
}
```

Sobreposição do tempo de execução (por entrada de sessão):

-`sendPolicy: "allow" | "deny"`(não definido = herdar a configuração)
- Settable via`sessions.patch`ou apenas proprietário`/send on|off|inherit`(mensagem standalone).

Pontos de execução:

-`chat.send`/`agent`(porta)
- lógica de entrega de resposta automática

## sessões  lança

Espalhe um sub-agente em uma sessão isolada e anuncie o resultado de volta para o canal de chat do solicitante.

Parâmetros:

-`task`(obrigatório)
-`label?`(opcional; usado para logs/UI)
-`agentId?`(opcional; desova sob outro agente id se permitido)
-`model?`(opcional; substitui o modelo de sub- agente; erro de valores inválidos)
-`runTimeoutSeconds?`(padrão 0; quando definido, aborta o sub- agente executado após N segundos)
-`cleanup?``delete|keep`, OCTXCODE por defeito7)

Lista de permissões:

-`agents.list[].subagents.allowAgents`: lista dos ids de agentes autorizados através do`agentId``["*"]`. Padrão: somente o agente solicitante.

Descoberta:

- Use`agents_list`para descobrir quais IDs de agente são permitidos para`sessions_spawn`.

Comportamento:

- Inicia uma nova sessão`agent:<agentId>:subagent:<uuid>`com`deliver: false`.
- Sub-agentes padrão para o conjunto completo de ferramentas **minus session tools** (configurável via`tools.subagents.tools`.
- Os sub-agentes não podem chamar`sessions_spawn`(sem sub-agente → desova do sub-agente).
- Sempre sem bloqueio: devolve`{ status: "accepted", runId, childSessionKey }`imediatamente.
- Após a conclusão, o OpenClaw executa um sub-agente **announce step** e publica o resultado no canal de chat do solicitante.
- Responder exatamente`ANNOUNCE_SKIP`durante o anúncio passo para ficar em silêncio.
- As respostas anunciadas são normalizadas para`Status`/`Result`/`Notes`;`Status`provém de resultados em tempo de execução (não de texto modelo).
- As sessões de sub-agentes são auto-arquivadas após`deliver: false`0 (padrão: 60).
- As respostas anunciadas incluem uma linha de estatísticas (runtime, tokens, sessionKey/session ID, caminho da transcrição e custo opcional).

## Visibilidade da Sessão Sandbox

Sessões Sandboxed podem usar ferramentas de sessão, mas por padrão eles só veem sessões que geraram via`sessions_spawn`.

Configuração:

```json5
{
  agents: {
    defaults: {
      sandbox: {
        // default: "spawned"
        sessionToolsVisibility: "spawned", // or "all"
      },
    },
  },
}
```
