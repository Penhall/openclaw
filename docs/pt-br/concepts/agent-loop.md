---
summary: "Agent loop lifecycle, streams, and wait semantics"
read_when:
  - You need an exact walkthrough of the agent loop or lifecycle events
---

# Agente Loop (OpenClaw)

Um loop agentic é a execução “real” completa de um agente: aporte → montagem de contexto → inferência do modelo →
execução da ferramenta → respostas de streaming → persistência. É o caminho autoritário que transforma uma mensagem
em ações e uma resposta final, mantendo o estado da sessão consistente.

No OpenClaw, um loop é uma única execução serializada por sessão que emite ciclo de vida e eventos de fluxo
como o modelo pensa, chama ferramentas, e fluxos de saída. Este documento explica como é esse loop autêntico
De ponta a ponta.

## Pontos de entrada

- Porta RCP:`agent`e`agent.wait`.
- Comando`agent`.

## Como funciona (alto nível)

1.`agent`RPC valida params, resolve sessão (sessionKey/sessionId), persiste metadados de sessão, retorna`{ runId, acceptedAt }`imediatamente.
2.`agentCommand`executa o agente:
- resolve o modelo + thinking/verbose defaults
- carrega instantâneo de habilidades
- chamadas`runEmbeddedPiAgent`(period time pi-agent-core)
- emite **fim/erro do ciclo de vida** se o laço incorporado não emitir um
3.`runEmbeddedPiAgent`:
- serializa execuções por sessão + filas globais
- resolve modelo + perfil de autenticação e constrói a sessão pi
- assina eventos pi e streams assistente / ferramenta deltas
- obriga tempo limite -> aborta execução se excedido
- retorna cargas úteis + metadados de uso
4.`subscribeEmbeddedPiSession`pontes pi-agent-core eventos para OpenClaw`agent`fluxo:
- eventos da ferramenta =>`stream: "tool"`- deltas assistentes =>`stream: "assistant"`- acontecimentos do ciclo de vida =>`stream: "lifecycle"``{ runId, acceptedAt }`0)
5.`{ runId, acceptedAt }`1 utiliza`{ runId, acceptedAt }`2:
- espera por ** fim/erro do ciclo de vida** para`{ runId, acceptedAt }`3
- devolve`{ runId, acceptedAt }`4

## Fila + concorrência

- As corridas são serializadas por chave de sessão (faixa de sessão) e opcionalmente através de uma faixa global.
- Isto evita corridas de ferramentas/sessões e mantém o histórico de sessões consistente.
- Os canais de mensagens podem escolher os modos de fila (colete/steer/followup) que alimentam este sistema de faixa.
Ver [Comando Fila] /concepts/queue.

## Sessão + preparação do espaço de trabalho

- O espaço de trabalho é resolvido e criado; as sequências sandbox podem redirecionar para uma raiz de espaço de trabalho sandbox.
- As habilidades são carregadas (ou reutilizadas a partir de um instantâneo) e injetadas em env e prompt.
- Bootstrap / arquivos de contexto são resolvidos e injetados no relatório de prompt do sistema.
- Um bloqueio de gravação de sessão é adquirido;`SessionManager`é aberto e preparado antes da transmissão.

## Montagem imediata + prompt do sistema

- O prompt de sistema é construído a partir do prompt de base da OpenClaw, prompt de habilidades, contexto bootstrap e sobreposições por execução.
- Limites específicos do modelo e fichas de reserva de compactação são aplicadas.
- Veja [Prompt do sistema]/concepts/system-prompt para o que o modelo vê.

## Pontos de gancho (onde você pode interceptar)

Openclaw tem dois sistemas de gancho:

- ** Ganchos internos** (Gateway hooks): scripts dirigidos a eventos para comandos e eventos de ciclo de vida.
- ** Ganchos de plugin**: pontos de extensão dentro do ciclo de vida do agente / ferramenta e gateway pipeline.

Ganchos internos

- **`agent:bootstrap`**: roda enquanto constrói arquivos bootstrap antes que o prompt do sistema seja finalizado.
Use isto para adicionar/remover arquivos de contexto bootstrap.
- ** Ganchos de comando**:`/new`,`/reset`,`/stop`e outros eventos de comando (ver Hooks doc).

Veja [Hooks]/hooks para configuração e exemplos.

## # Ganchos de plug-in (agente + ciclo de vida de gateway)

Estes rodam dentro do loop do agente ou gateway pipeline:

- **`before_agent_start`**: injetar o contexto ou sobrepor o prompt do sistema antes do início da execução.
- **`agent_end`**: inspecionar a lista de mensagens final e executar metadados após a conclusão.
- **`before_compaction`/`after_compaction`**: observar ou anotar ciclos de compactação.
- **`before_tool_call`/`after_tool_call`**: interceptar parâmetros/resultados.
- **`tool_result_persist`**: transformar síncronamente os resultados da ferramenta antes de serem escritos para a transcrição da sessão.
- **`message_received`/`message_sending`/`message_sent`**: ganchos de entrada + de saída.
- **`agent_end`0 /`agent_end`1**: limites do ciclo de vida da sessão.
- **`agent_end`2 /`agent_end`3**: eventos do ciclo de vida do portal.

Veja [Plugins]/plugin#plugin-hooks para os detalhes do hook API e registro.

## Streaming + respostas parciais

- Os deltas assistentes são transmitidos do pi-agent-core e emitidos como eventos`assistant`.
- A transmissão em bloco pode emitir respostas parciais quer no`text_end`quer no`message_end`.
- Raciocínio de transmissão pode ser emitido como um fluxo separado ou como respostas em bloco.
- Veja [Streaming] /concepts/streaming para o comportamento de blocking e resposta.

## Execução de ferramentas + ferramentas de mensagens

- Os eventos de arranque/atualização/fim da ferramenta são emitidos no fluxo`tool`.
- Os resultados da ferramenta são higienizados para o tamanho e as cargas de imagem antes do registro / saída.
- Os envios da ferramenta de mensagens são rastreados para suprimir as confirmações duplicadas do assistente.

## Responder moldando + supressão

- As cargas finais são montadas a partir de:
- texto assistente (e raciocínio opcional)
- resumos em linha da ferramenta (quando verbose + permitido)
- texto de erro assistente quando os erros do modelo
-`NO_REPLY`é tratado como um token silencioso e filtrado de cargas de saída.
- Mensagens duplicadas de ferramentas são removidas da lista de carga útil final.
- Se não restarem cargas úteis e uma ferramenta estiver errada, uma resposta de erro de ferramenta de retorno é emitida
(a menos que uma ferramenta de mensagens já tenha enviado uma resposta visível para o usuário).

## Compactação + repetições

- Auto-compactação emite eventos de fluxo`compaction`e pode desencadear uma repetição.
- Na repetição, buffers in-memory e resumos de ferramentas são reiniciados para evitar saída duplicada.
- Ver [Compactação] /concepts/compaction para o gasoduto de compactação.

## Fluxos de eventos (hoje)

-`lifecycle`: emitido pelo`subscribeEmbeddedPiSession`(e como recurso pelo`agentCommand`
-`assistant`: deltas fluidas de pi-agent-core
-`tool`: eventos de ferramentas transmitidas do pi-agent-core

## Manuseamento de canais de chat

- Os deltas assistentes são tamponados em mensagens`delta`.
- Uma conversa`final`é emitida em ** Fim/Erro do ciclo de vida**.

## Tempo limite

-`agent.wait`padrão: 30s (apenas a espera).`timeoutMs`param substitui.
- Tempo de execução do agente:`agents.defaults.timeoutSeconds`padrão 600s; forçado no`runEmbeddedPiAgent`abortar temporizador.

## Onde as coisas podem acabar cedo

- Tempo de agente (abortar)
- Abortar sinal (cancel)
- Desligamento de porta ou tempo limite RPC
- Tempo limite`agent.wait`(só espera, não pára o agente)
