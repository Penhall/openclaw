---
summary: "Sub-agents: spawning isolated agent runs that announce results back to the requester chat"
read_when:
  - You want background/parallel work via the agent
  - You are changing sessions_spawn or sub-agent tool policy
---

Subagentes

Os sub-agentes são agentes de fundo que são executados a partir de um agente existente. Eles rodam em sua própria sessão (`agent:<agentId>:subagent:<uuid>`) e, quando terminado, **anunciar** seu resultado de volta para o canal de chat do solicitante.

# # Comando Slash

Use `/subagents` para inspecionar ou controlar as operações de subagentes para a sessão atual**:

- <<CODE0>
- <<CODE1>
- <<CODE2>
- `/subagents info <id|#>`
- `/subagents send <id|#> <message>`

`/subagents info` mostra metadados de execução (status, timestamps, session id, transcript path, cleanup).

Objectivos primários:

- Paralelizar o trabalho “pesquisa / tarefa longa / ferramenta lenta” sem bloquear a execução principal.
- Mantenha os subagentes isolados por padrão (separação de sessão + sandboxing opcional).
- Mantenha a superfície da ferramenta difícil de usar: subagentes não ** obter ferramentas de sessão por padrão.
- Evite aninhados fã-out: sub-agentes não podem gerar sub-agentes.

Nota de custo: cada sub-agente tem seu **on** contexto e uso de token. Para pesados ou repetitivos
tarefas, definir um modelo mais barato para subagentes e manter seu agente principal em um modelo de maior qualidade.
Você pode configurar isso via substituições `agents.defaults.subagents.model` ou por agente.

Ferramenta

Utilização <<CODE0>:

- Inicia uma corrida de sub- agente (`deliver: false`, faixa global: `subagent`)
- Em seguida, executa um anúncio passo e posta a resposta anunciar para o canal de chat solicitante
- Modelo padrão: herda o chamador a menos que você defina `agents.defaults.subagents.model` (ou por agente `agents.list[].subagents.model`); um explícito `sessions_spawn.model` ainda vence.

Parâmetros da ferramenta:

- <<CODE0> (obrigatório)
- <<CODE1> (facultativo)
- <<CODE2> (facultativo; desova sob outro ID de agente, se permitido)
- `model?` (opcional; substitui o modelo do sub- agente; os valores inválidos são ignorados e o sub- agente é executado no modelo padrão com um aviso no resultado da ferramenta)
- <<CODE4> (opcional; substitui o nível de pensamento para a execução do sub- agente)
- `runTimeoutSeconds?` (padrão `0`; quando definido, a execução do sub- agente é interrompida após N segundos)
- <<CODE7> (`delete|keep`, por omissão `keep`)

Lista de permissões:

- `agents.list[].subagents.allowAgents`: lista de ids de agentes que podem ser visados via `agentId` (`["*"]` para permitir qualquer). Padrão: somente o agente solicitante.

Descoberta:

- Utilizar `agents_list` para ver que IDs de agente são actualmente permitidos para `sessions_spawn`.

Arquivo automático:

- As sessões de subagentes são automaticamente arquivadas após `agents.defaults.subagents.archiveAfterMinutes` (padrão: 60).
- Archive usa `sessions.delete` e renomeia a transcrição para `*.deleted.<timestamp>` (mesma pasta).
- <<CODE3> arquivos imediatamente após anunciar (ainda mantém a transcrição via renomear).
- Arquivo automático é o melhor esforço; timers pendentes são perdidos se o gateway reiniciar.
- <<CODE4> faz **não** auto-arquivo; só pára a execução. A sessão permanece até ao auto-arquivo.

# # Autenticação

A autenticação do sub- agente é resolvida por ** agent id**, não por tipo de sessão:

- A tecla de sub-agente da sessão é `agent:<agentId>:subagent:<uuid>`.
- O armazém de autenticação é carregado a partir do `agentDir` desse agente.
- Os perfis de autenticação do agente principal são mesclados como um **fallback**; perfis de agente sobrepõem os perfis principais em conflitos.

Nota: a mesclagem é aditiva, então os perfis principais estão sempre disponíveis como fallbacks. A autenticação totalmente isolada por agente ainda não é suportada.

Anunciar

Os subagentes reportam de volta através de um passo de anúncio:

- O passo anunciado é executado dentro da sessão de subagentes (não na sessão de solicitantes).
- Se o sub- agente responder exactamente `ANNOUNCE_SKIP`, nada é publicado.
- Caso contrário, a resposta anunciada é postada no canal de chat do solicitante através de uma chamada de seguimento `agent` (`deliver=true`).
- Anunciar respostas preservar thread / roteamento tópico quando disponível (linhas de linha, tópicos de Telegram, tópicos Matrix).
- Anunciar mensagens são normalizadas para um modelo estável:
- `Status:` derivado do resultado da corrida (`success`, `error`, `timeout`, ou `unknown`).
- `Result:` o conteúdo sumário da etapa de anúncio (ou `(not available)` se faltar).
- `Notes:` detalhes de erro e outro contexto útil.
- <<CODE11> não é inferida a partir da saída do modelo; vem de sinais de resultado em tempo de execução.

Anunciar as cargas úteis incluem uma linha de estatísticas no final (mesmo quando embrulhada):

- Tempo de execução (por exemplo, `runtime 5m12s`)
- Utilização do token (input/output/total)
- Custo estimado quando o preço do modelo está configurado (`models.providers.*.models[].cost`)
- `sessionKey`, `sessionId`, e caminho da transcrição (de modo que o agente principal pode obter o histórico via `sessions_history` ou inspecionar o arquivo no disco)

# # Política de ferramentas (ferramentas subagentes)

Por padrão, os subagentes recebem **todas as ferramentas, exceto ferramentas de sessão**:

- <<CODE0>
- <<CODE1>
- <<CODE2>
- `sessions_spawn`

Substituir através da configuração:

```json5
{
  agents: {
    defaults: {
      subagents: {
        maxConcurrent: 1,
      },
    },
  },
  tools: {
    subagents: {
      tools: {
        // deny wins
        deny: ["gateway", "cron"],
        // if allow is set, it becomes allow-only (deny still wins)
        // allow: ["read", "exec", "process"]
      },
    },
  },
}
```

# # Concorrencial

Os subagentes usam uma faixa de fila dedicada em processo:

- Nome da via: `subagent`
- Concurrência: `agents.defaults.subagents.maxConcurrent` (padrão `8`)

# # Parando

- Enviando `/stop` no chat do solicitante aborta a sessão do solicitante e para qualquer sub-agente ativo corre gerado a partir dele.

# # Limitações

- O anúncio do Sub-Agente é o melhor. Se o gateway reiniciar, o trabalho pendente de "anunciar de volta" é perdido.
- Subagentes ainda compartilham os mesmos recursos do processo de gateway; tratam `maxConcurrent` como uma válvula de segurança.
- <<CODE1> é sempre não bloqueado: retorna <<CODE2> imediatamente.
- Contexto sub- agente apenas injecta `AGENTS.md` + `TOOLS.md` (não `SOUL.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, ou `BOOTSTRAP.md`).
