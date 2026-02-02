---
summary: "Deep dive: session store + transcripts, lifecycle, and (auto)compaction internals"
read_when:
  - You need to debug session ids, transcript JSONL, or sessions.json fields
  - You are changing auto-compaction behavior or adding “pre-compaction” housekeeping
  - You want to implement memory flushes or silent system turns
---

# Gestão e compactação de sessões (Deep Dive)

Este documento explica como o OpenClaw gerencia sessões de ponta a ponta:

- ** Roteamento de sessões** (como as mensagens de entrada mapeiam para um `sessionKey`)
- ** Loja de sessões** (<`sessions.json`) e o que rastreia
- ** Persistência transcrita** (<`*.jsonl`) e sua estrutura
- ** Higiene transcrita** (ajuste específico do fornecedor antes das corridas)
- ** Limites de contexto** (janela de contexto vs tokens rastreados)
- **Compaction** (manual + auto-compaction) e onde ligar o trabalho pré-compaction
- ** Limpeza silenciosa** (por exemplo, a memória escreve que não deve produzir saída visível pelo usuário)

Se você quiser uma visão geral de nível superior primeiro, comece com:

- [/conceitos/sessão] (</concepts/session)
- [/conceitos/compactação] (</concepts/compaction)
- [/conceitos/sessões] (/concepts/session-pruning)
- [/referência/higiene transcrito] (/reference/transcript-hygiene)

---

# # Fonte da verdade: o Portal

Openclaw é projetado em torno de um único processo **Gateway** que possui estado de sessão.

- UIS (macOS app, web Control UI, TUI) devem consultar o Gateway para listas de sessões e contagem de tokens.
- No modo remoto, os arquivos de sessão estão no host remoto; "verificar seus arquivos Mac locais" não vai refletir o que o Gateway está usando.

---

# # Duas camadas de persistência

Openclaw persiste sessões em duas camadas:

1. ** Armazenagem de sementes (<`sessions.json`) **
- Mapa chave/valor: `sessionKey -> SessionEntry`
- Pequeno, mutável, seguro para editar (ou apagar entradas)
- Rastreia metadados de sessão (ID da sessão atual, última atividade, comutadores, contadores de tokens, etc.)

2. **Transcrito (`<sessionId>.jsonl`)**
- Transcrição apenas para apêndices com estrutura em árvore (entries têm `id` + `parentId`)
- Armazena a conversa atual + chamadas de ferramenta + resumos de compactação
- Usado para reconstruir o contexto do modelo para futuras voltas

---

# # Locais no disco

Por agente, no anfitrião da Gateway:

- Conservar: <<CODE0>
- Transcrições: `~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl`
- Sessões temáticas de telegrama: `.../<sessionId>-topic-<threadId>.jsonl`

Openclaw resolve estes via `src/config/sessions.ts`.

---

# # Teclas de sessão (`sessionKey`)

A <<CODE0> identifica  qual conversação bucket  você está em (roteamento + isolamento).

Padrões comuns:

- Conversa principal/direta (por agente): `agent:<agentId>:<mainKey>` (padrão `main`)
- Grupo: `agent:<agentId>:<channel>:group:<id>`
- Sala/canal (Discord/Slack): `agent:<agentId>:<channel>:channel:<id>` ou `...:room:<id>`
- Cron: <<CODE5>
- Webhook: <<CODE6>

As regras canônicas estão documentadas em [/conceitos/sessão](</concepts/session).

---

# # IDs de sessão (`sessionId`)

Cada ponto <<CODE0> numa corrente <<CODE1> (o arquivo de transcrição que continua a conversa).

Regras do polegar:

- **Reset** (<`/new`, `/reset`) cria um novo `sessionId` para esse `sessionKey`.
- **Reset diário** (padrão 4:00 hora local no host gateway) cria um novo `sessionId` na próxima mensagem após o limite de reset.
- **Expiração ociosa** (<`session.reset.idleMinutes` ou legado `session.idleMinutes`) cria uma nova `sessionId` quando uma mensagem chega após a janela ociosa. Quando diariamente + ocioso são configurados, o que expira primeiro ganha.

Detalhes da implementação: a decisão ocorre em `initSessionState()` em <CODE1>>.

---

# # Esquema da loja da sessão (`sessions.json`)

O tipo de valor da loja é `SessionEntry` em <CODE1>>.

Campos-chave (não exaustivos):

- `sessionId`: id da transcrição atual (o nome do arquivo é derivado disto, exceto se `sessionFile` for definido)
- <<CODE2>: última hora de atividade
- <<CODE3>: sobreposição opcional do caminho explícito da transcrição
- `chatType`: <<CODE5> (ajuda as UI e envia a política)
- `provider`, `subject`, `room`, `space`, `displayName`: metadados para a rotulagem do grupo/canal
- Alterna:
- `thinkingLevel`, `verboseLevel`, `reasoningLevel`, `elevatedLevel`
- `sendPolicy` (sobreposição por sessão)
- Seleção do modelo:
- `providerOverride`, `modelOverride`, `authProfileOverride`
- Contadores de token (melhor esforço / provedor dependente):
- `inputTokens`, `outputTokens`, `totalTokens`, `contextTokens`
- <<CODE23>: com que frequência a autocompactação foi concluída para esta chave de sessão
- <<CODE24>: data- limite para o último flush de memória pré- compactação
- <<CODE25>: contagem de compactação quando a última descarga

A loja é segura para editar, mas o Gateway é a autoridade: pode reescrever ou re-hidratar entradas como sessões executadas.

---

# # Estrutura transcrita (`*.jsonl`)

Os transcritos são gerenciados por `@mariozechner/pi-coding-agent` `SessionManager`.

O arquivo é JSONL:

- Primeira linha: cabeçalho da sessão (`type: "session"`, inclui `id`, `cwd`, `timestamp`, opcional `parentSession`)
- Em seguida: entradas de sessão com `id` + `parentId` (árvore)

Tipos de entrada notáveis:

- `message`: utilizador/assistente/ferramentaMensagens de resultado
- <<CODE1>: mensagens de extensão que  do  introduzem o contexto do modelo (podem ser ocultadas da UI)
- <<CODE2>: estado de extensão que  not  enter model context
- <<CODE3>: resumo de compactação persistente com `firstKeptEntryId` e `tokensBefore`
- <<CODE6>: resumo persistente ao navegar por um ramo de árvore

OpenClaw intencionalmente faz **not** "fix up" transcrições; o Gateway usa `SessionManager` para lê-los / escrevê-los.

---

# # Janelas de contexto vs fichas rastreadas

Dois conceitos diferentes importam:

1. **Modelo janela de contexto**: capa dura por modelo (tokens visíveis para o modelo)
2. **Contadores de lojas de sessões**: estatísticas de rolamento escritas em `sessions.json` (utilizadas para /status e painéis)

Se você está afinando limites:

- A janela de contexto vem do catálogo do modelo (e pode ser substituída via config).
- `contextTokens` na loja é uma estimativa em tempo de execução/valor de notificação; não a trate como uma garantia estrita.

Para mais informações, ver [/token-use] (</token-use).

---

# # Compactação: o que é

A compactação resume a conversa mais antiga em uma entrada persistente `compaction` na transcrição e mantém as mensagens recentes intactas.

Após a compactação, o futuro vira ver:

- Resumo da compactação
- Mensagens após `firstKeptEntryId`

A compactação é **persistente** (poda de sessão diferente). Ver [/conceitos/sessão-pruning](/concepts/session-pruning).

---

# # Quando a auto-compactação acontece (Pi Runtime)

No agente Pi incorporado, gatilhos de auto-compactação em dois casos:

1. **Overflow recuperação**: o modelo retorna um erro de sobrecarga de contexto → compact → retry.
2. ** Manutenção do limiar**: após uma volta bem sucedida, quando:

<<CODE0>

Em que:

- <<CODE0> é a janela de contexto do modelo
- <<CODE1> é headroom reservado para prompts + a próxima saída do modelo

Estas são semânticas de execução Pi (OpenClaw consome os eventos, mas Pi decide quando compactar).

---

# # Configurações de compactação (`reserveTokens`, `keepRecentTokens`)

As configurações de compactação Pi ao vivo nas configurações Pi:

```json5
{
  compaction: {
    enabled: true,
    reserveTokens: 16384,
    keepRecentTokens: 20000,
  },
}
```

OpenClaw também impõe um piso de segurança para corridas incorporadas:

- Se <<CODE0>, OpenClaw bate-lhe.
- O piso padrão é `20000` tokens.
- Definir `agents.defaults.compaction.reserveTokensFloor: 0` para desativar o piso.
- Se já está mais alto, o Openclaw deixa-o em paz.

Por que: deixar suficiente headroom para multi-turno “a manutenção da casa” (como a memória escreve) antes de compactação torna-se inevitável.

Implementação: <<CODE0> em <<CODE1>
(chamado de `src/agents/pi-embedded-runner.ts`).

---

# # Superfícies visíveis pelo usuário

Você pode observar a compactação e o estado da sessão via:

- <<CODE0> (em qualquer sessão de chat)
- <<CODE1> (CLI)
- <<CODE2>/ <<CODE3>
- Modo verboso: `🧹 Auto-compaction complete` + contagem de compactação

---

# # Serviço de limpeza silencioso (`NO_REPLY`)

OpenClaw suporta "silent" gira para tarefas de fundo onde o usuário não deve ver saída intermediária.

Convenção:

- O assistente inicia sua saída com `NO_REPLY` para indicar “não entregar uma resposta ao usuário”.
- OpenClaw tira/suprime isto na camada de entrega.

A partir de `2026.1.10`, OpenClaw também suprime **draft/tipagem streaming** quando um pedaço parcial começa com <<CODE1>, para que as operações silenciosas não vazem saída parcial no meio da volta.

---

# # Pré-compactação “memory flush” (implementado)

Objetivo: antes que a auto-compactação aconteça, execute um giro agente silencioso que escreva durável
estado para o disco (por exemplo, `memory/YYYY-MM-DD.md` no espaço de trabalho do agente) para que a compactação não possa
apagar o contexto crítico.

OpenClaw usa a abordagem **pre-threshold flush**:

1. Monitore o uso do contexto da sessão.
2. Quando cruza um “limiar suave” (abaixo do limiar de compactação de Pi), executar um silencioso
“escrever memória agora” diretiva para o agente.
3. Use <<CODE0> para que o usuário não veja nada.

Configuração (<`agents.defaults.compaction.memoryFlush`):

- <<CODE0> (por omissão: `true`)
- <<CODE2> (por omissão: `4000`)
- <<CODE4> (mensagem do utilizador para o turno do flush)
- <<CODE5> (prompt de sistema adicional anexado para a volta do flush)

Notas:

- O prompt padrão/prompt do sistema inclui uma dica `NO_REPLY` para suprimir a entrega.
- O flush é executado uma vez por ciclo de compactação (tracked in `sessions.json`).
- O flush é executado apenas para sessões de Pi incorporadas (os backends CLI ignoram).
- O flush é ignorado quando a área de trabalho da sessão é apenas leitura (`workspaceAccess: "ro"` ou `"none"`).
- Veja [Memory](</concepts/memory) para o layout do arquivo de espaço de trabalho e padrões de escrita.

Pi também expõe um gancho `session_before_compact` na API de extensão, mas OpenClaw
A lógica da descarga vive no lado do portal hoje.

---

# # Verificação de problemas

- A chave da sessão está errada? Comece com [/conceitos/sessão] (</concepts/session) e confirme o `sessionKey` em `/status`.
- Descompatibilidade entre a loja e a transcrição? Confirme o host Gateway e o caminho da loja de `openclaw status`.
- Spam de compactação? Verificar:
- janela de contexto do modelo (muito pequena)
- configurações de compactação (`reserveTokens` muito alto para a janela do modelo pode causar compactação anterior)
- bloat de resultado- ferramenta: poda de sessão ativa/desativa
- Viras silenciosas a vazar? Confirme que a resposta começa com `NO_REPLY` (toque exato) e você está em uma compilação que inclui a correção de supressão de streaming.
