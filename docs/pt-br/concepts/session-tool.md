---
summary: "Agent session tools for listing sessions, fetching history, and sending cross-session messages"
read_when:
  - Adding or modifying session tools
---

Ferramentas de Sessão

Objetivo: conjunto de ferramentas pequeno e difícil de usar para que os agentes possam listar sessões, buscar histórico e enviar para outra sessão.

# # Nomes de Ferramentas

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>
- <<CODE3>>

# # Modelo-chave

- O balde principal de chat direto é sempre a chave literal <<CODE0>> (resolvido à chave principal do agente atual).
- Os chats em grupo utilizam <<CODE1>> ou <<CODE2>> (passar a chave completa).
- Os trabalhos de Cron usam <<CODE3>>>.
- Ganchos usar <<CODE4>> a menos que explicitamente definido.
- Sessões de nós usam <<CODE5> a menos que explicitamente definidas.

<<CODE0>> e <<CODE1>> são valores reservados e nunca estão listados. Se <<CODE2>>, apelidamo-lo de <<CODE3>> para todas as ferramentas para que as chamadas nunca vejam <<CODE4>>.

Lista de sessões # #

Listar as sessões como um conjunto de linhas.

Parâmetros:

- <<CODE0> filtro: qualquer um dos <<CODE1>>
- <<CODE2>> linhas máximas (padrão: padrão do servidor, pinça, por exemplo, 200)
- <<CODE3> apenas sessões actualizadas em minutos N
- <<CODE4>> 0 = sem mensagens (padrão 0); > 0 = incluir as últimas mensagens N

Comportamento:

- <<CODE0> > obtém <<CODE1>> por sessão e inclui as últimas mensagens N.
- Os resultados da ferramenta são filtrados na saída da lista; use <<CODE2>> para mensagens de ferramenta.
- Ao executar em uma sessão de agente **sandboxed**, ferramentas de sessão padrão para **spawned-somente visibilidade** (veja abaixo).

Forma da linha (JSON):

- <<CODE0>>: tecla de sessão (texto)
- <<CODE1>: <<CODE2>>
- <<CODE3>>: <<CODE4>>
- <<CODE5>> (Rótulo de exibição do grupo, se disponível)
- <<CODE6> (ms)
- <<CODE7>>
- <<CODE8>>, <<CODE9>>, <<CODE10>>
- <<CODE11>>, <<CODE12>>, <<CODE13>>, <<CODE14>>
- <<CODE15>> (substituir a sessão se estiver definida)
- <<CODE16>>, <<CODE17>>
- <<CODE18> (normalizado <<CODE19>> quando disponível)
- <<CODE20>> (melhor caminho do esforço derivado da pasta de armazenamento + sessão Id)
- <<CODE21>> (apenas quando <<CODE22>>)

# # sessões   história

Obter transcrição para uma sessão.

Parâmetros:

- <<CODE0>> (obrigatório; aceita a chave de sessão ou <<CODE1>> de <<CODE2>>)
- <<CODE3>> mensagens máximas (apertos de serviço)
- <<CODE4>> (falso padrão)

Comportamento:

- <<CODE0>> filtros <<CODE1>> mensagens.
- Retorna o array de mensagens no formato transcrito bruto.
- Quando é dado um <<CODE2>>, o OpenClaw resolve-o para a tecla de sessão correspondente (erro de IDs em falta).

Enviar enviar sessões # #

Enviar uma mensagem para outra sessão.

Parâmetros:

- <<CODE0>> (obrigatório; aceita a chave de sessão ou <<CODE1>> de <<CODE2>>)
- <<CODE3> (necessário)
- <<CODE4>> (padrão >0; 0 = fogo e esquecimento)

Comportamento:

- <<CODE0>>: enquear e voltar <<CODE1>>.
- <<CODE2>: esperar até N segundos para completar, depois regressar <<CODE3>>>.
- Se esperar tempo: <<CODE4>>>>. Executar continua; chamada <<CODE5>> mais tarde.
- Se a execução falhar: <<CODE6>>>>.
- Anunciar as operações de entrega após a execução primária completa e é o melhor esforço; <<CODE7> não garante que o anúncio foi entregue.
- Waits via gateway <<CODE8> (lado servidor) para que as religações não larguem a espera.
- O contexto da mensagem agente-a-agente é injectado para a corrida primária.
- Após a execução primária terminar, o OpenClaw executa um loop de resposta**:
- Round 2+ alterna entre o solicitante e os agentes alvo.
- Responder exatamente <<CODE9>> para parar o ping-pong.
- Max Turns é <<CODE10>> (0–5, padrão 5).
- Uma vez que o loop termina, o OpenClaw executa o **agente-a-agente anuncia passo** (apenas agente alvo):
- Responder exatamente <<CODE11>> para ficar em silêncio.
- Qualquer outra resposta é enviada para o canal alvo.
- Anunciar passo inclui o pedido original + resposta redonda-1 + última resposta ping-pong.

# # Campo de Canal

- Para grupos, <<CODE0>> é o canal gravado na entrada da sessão.
- Para conversas diretas, <<CODE1>> mapas de <<CODE2>>.
- Para cron/hook/node, <<CODE3>> é <<CODE4>>>.
- Em caso de falta, <<CODE5>> é <<CODE6>>>.

# # Segurança / Política de envio

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

- <<CODE0> (não definido = herdar a configuração)
- Settable via <<CODE1> ou somente proprietário <<CODE2>> (mensagem individual).

Pontos de execução:

- <<CODE0>> / <<CODE1>> (porta)
- lógica de entrega de resposta automática

# # sessões  lança

Espalhe um sub-agente em uma sessão isolada e anuncie o resultado de volta para o canal de chat do solicitante.

Parâmetros:

- <<CODE0> (necessário)
- <<CODE1>> (facultativo; utilizado para registos/UI)
- <<CODE2>> (facultativo; desova sob outro ID de agente, se permitido)
- <<CODE3>> (opcional; substitui o modelo do sub- agente; erro de valores inválidos)
- <<CODE4>> (padrão 0; quando definido, aborta a execução do sub- agente após N segundos)
- <<CODE5> (<<CODE6>>>, por omissão <<CODE7>>)

Lista de permissões:

- <<CODE0>>: lista de ids de agentes autorizados via <<CODE1>> (<<CODE2>> para permitir qualquer). Padrão: somente o agente solicitante.

Descoberta:

- Use <<CODE0>> para descobrir quais IDs de agente são permitidos para <<CODE1>>>.

Comportamento:

- Inicia uma nova sessão <<CODE0>> com <<CODE1>>.
- Subagentes padrão para o conjunto completo de ferramentas **minus session tools** (configurável via <<CODE2>>).
- Os sub-agentes não estão autorizados a chamar <<CODE3>> (sem sub-agente → desova do sub-agente).
- Sempre sem bloqueio: retorna <<CODE4>> imediatamente.
- Após a conclusão, o OpenClaw executa um sub-agente **announce step** e publica o resultado no canal de chat do solicitante.
- Responder exatamente <<CODE5>> durante o passo de anúncio para permanecer em silêncio.
- Respostas anunciadas são normalizadas para <<CODE6>>/<<CODE7>/<<CODE8>>; <<CODE9>> vem do resultado da execução (não do texto do modelo).
- As sessões de subagentes são auto-arquivadas após <<CODE10>> (padrão: 60).
- As respostas anunciadas incluem uma linha de estatísticas (runtime, tokens, sessionKey/session ID, caminho da transcrição e custo opcional).

# # Visibilidade da Sessão Sandbox

Sessões Sandbox podem usar ferramentas de sessão, mas por padrão eles só veem sessões que geraram via <<CODE0>>>.

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
