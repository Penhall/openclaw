---
title: Lobster
summary: "Typed workflow runtime for OpenClaw with resumable approval gates."
description: Typed workflow runtime for OpenClaw — composable pipelines with approval gates.
read_when:
  - You want deterministic multi-step workflows with explicit approvals
  - You need to resume a workflow without re-running earlier steps
---

Lagosta

A lagosta é uma shell de fluxo de trabalho que permite ao OpenClaw executar sequências de ferramentas multi-step como uma única operação determinística com checkpoints de aprovação explícitos.

# # Gancho

Seu assistente pode construir as ferramentas que se gerenciam. Peça um fluxo de trabalho, e 30 minutos depois você tem um CLI mais tubulações que funcionam como uma chamada. A lagosta é a peça que falta: oleodutos determinísticos, aprovações explícitas e estado resumível.

# # Porque

Hoje, fluxos de trabalho complexos exigem muitas chamadas de ferramentas. Cada chamada custa fichas, e a LLM tem que orquestrar cada passo. A lagosta move essa orquestração para um tempo de execução digitado:

- Uma chamada em vez de muitos. Openclaw executa uma chamada de ferramenta de lagosta e obtém um resultado estruturado.
- **Aprovações incorporadas em**: Efeitos colaterais (enviar e-mail, post comment) param o fluxo de trabalho até ser explicitamente aprovado.
- ** Resumível**: Fluxos de trabalho parados retornam um token; aprovam e retomam sem repetir tudo.

# # Por que um DSL em vez de programas simples?

A lagosta é intencionalmente pequena. O objetivo não é "uma nova linguagem", é uma especificação de pipeline previsível, amiga de IA, com aprovações de primeira classe e fichas de currículo.

- **Aprovar/resumo é construído em **: Um programa normal pode alertar um humano, mas não pode  pausar e retomar  com um token durável sem que você mesmo invente esse tempo de execução.
- **Determinismo + auditoria**: Pipelines são dados, então eles são fáceis de registrar, diff, replay e revisão.
- **Superfície confinada para IA**: Uma minúscula gramática + encanamento JSON reduz caminhos de código “criativos” e torna a validação realista.
- **A política de segurança criada em**: Tempo limite, caps de saída, verificações sandbox e allowlists são aplicadas pelo tempo de execução, não cada script.
- ** Ainda programável**: Cada passo pode chamar qualquer CLI ou script. Se você quiser JS/TS, gere arquivos `.lobster` de código.

# # Como funciona

OpenClaw lança o CLI local <<CODE0> em **tool mode** e analisa um envelope JSON do stdout.
Se o oleoduto pausa para aprovação, a ferramenta retorna um `resumeToken` para que você possa continuar mais tarde.

# # # Padrão: CLI pequeno + tubos JSON + aprovações

Construa comandos minúsculos que falam JSON, em seguida, acorrente-os em uma única chamada de lagosta. (Exemplo de nomes de comandos abaixo — swap no seu próprio.)

```bash
inbox list --json
inbox categorize --json
inbox apply --json
```

```json
{
  "action": "run",
  "pipeline": "exec --json --shell 'inbox list --json' | exec --stdin json --shell 'inbox categorize --json' | exec --stdin json --shell 'inbox apply --json' | approve --preview-from-stdin --limit 5 --prompt 'Apply changes?'",
  "timeoutMs": 30000
}
```

Se o gasoduto solicitar a aprovação, retomar com o símbolo:

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

A IA ativa o fluxo de trabalho; A lagosta executa as etapas. As portas de aprovação mantêm os efeitos secundários explícitos e auditáveis.

Exemplo: mapear itens de entrada em chamadas de ferramentas:

```bash
gog.gmail.search --query 'newer_than:1d' \
  | openclaw.invoke --tool message --action send --each --item-key message --args-json '{"provider":"telegram","to":"..."}'
```

# # Passos LLM apenas para JSON (llm-task)

Para fluxos de trabalho que precisam de uma etapa LLM ** estruturada, habilite o opcional
`llm-task` ferramenta de plugin e chamá-lo de Lagosta. Isto mantém o fluxo de trabalho
determinístico enquanto ainda permite classificar/síntese/draft com um modelo.

Activar a ferramenta:

```json
{
  "plugins": {
    "entries": {
      "llm-task": { "enabled": true }
    }
  },
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": { "allow": ["llm-task"] }
      }
    ]
  }
}
```

Use-o num oleoduto:

```lobster
openclaw.invoke --tool llm-task --action json --args-json '{
  "prompt": "Given the input email, return intent and draft.",
  "input": { "subject": "Hello", "body": "Can you help?" },
  "schema": {
    "type": "object",
    "properties": {
      "intent": { "type": "string" },
      "draft": { "type": "string" }
    },
    "required": ["intent", "draft"],
    "additionalProperties": false
  }
}'
```

Veja [LLM Task](/tools/llm-task) para detalhes e opções de configuração.

## Arquivos de fluxo de trabalho (.lobster)

A lagosta pode executar arquivos de fluxo de trabalho YAML/JSON com campos `name`, `args`, `steps`, `env`, `condition` e `approval`. Em chamadas de ferramenta OpenClaw, defina `pipeline` para o caminho do arquivo.

```yaml
name: inbox-triage
args:
  tag:
    default: "family"
steps:
  - id: collect
    command: inbox list --json
  - id: categorize
    command: inbox categorize --json
    stdin: $collect.stdout
  - id: approve
    command: inbox apply --approve
    stdin: $categorize.stdout
    approval: required
  - id: execute
    command: inbox apply --execute
    stdin: $categorize.stdout
    condition: $approve.approved
```

Notas:

- `stdin: $step.stdout` e <<CODE1> passar uma saída de etapa anterior.
- <<CODE2> (ou `when`) podem dar passos em `$step.approved`.

# # Instalar lagosta

Instale o CLI de Lagosta no mesmo host** que executa o OpenClaw Gateway (veja o [Lobster repo](<https://github.com/openclaw/lobster)), e garanta que `lobster` esteja em `PATH`.
Se você quiser usar uma localização binária personalizada, passe uma **absoluta** <<CODE2> na chamada de ferramenta.

# # Habilitar a ferramenta

Lagosta é uma ferramenta de plugin ** opcional (não habilitada por padrão).

Recomendado (aditivo, seguro):

```json
{
  "tools": {
    "alsoAllow": ["lobster"]
  }
}
```

Ou por agente:

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": {
          "alsoAllow": ["lobster"]
        }
      }
    ]
  }
}
```

Evite usar `tools.allow: ["lobster"]` a menos que pretenda correr em modo allowlist restritivo.

Nota: allowlists são opt-in para plugins opcionais. Se a sua lista de permissões apenas nomes
ferramentas de plugin (como `lobster`), OpenClaw mantém as ferramentas principais habilitadas. Para restringir o núcleo
ferramentas, inclua as ferramentas principais ou grupos que você quer na lista de permissões também.

# # Exemplo: Triagem por e-mail

Sem lagosta:

```
User: "Check my email and draft replies"
→ openclaw calls gmail.list
→ LLM summarizes
→ User: "draft replies to #2 and #5"
→ LLM drafts
→ User: "send #2"
→ openclaw calls gmail.send
(repeat daily, no memory of what was triaged)
```

Com lagosta:

```json
{
  "action": "run",
  "pipeline": "email.triage --limit 20",
  "timeoutMs": 30000
}
```

Devolve um envelope JSON (truncado):

```json
{
  "ok": true,
  "status": "needs_approval",
  "output": [{ "summary": "5 need replies, 2 need action" }],
  "requiresApproval": {
    "type": "approval_request",
    "prompt": "Send 2 draft replies?",
    "items": [],
    "resumeToken": "..."
  }
}
```

O usuário aprova → retomar:

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

Um fluxo de trabalho. Determinista. Seguro.

# # Parâmetros da ferramenta

## # <<CODE0>

Execute um pipeline no modo ferramenta.

```json
{
  "action": "run",
  "pipeline": "gog.gmail.search --query 'newer_than:1d' | email.triage",
  "cwd": "/path/to/workspace",
  "timeoutMs": 30000,
  "maxStdoutBytes": 512000
}
```

Execute um arquivo de fluxo de trabalho com args:

```json
{
  "action": "run",
  "pipeline": "/path/to/inbox-triage.lobster",
  "argsJson": "{\"tag\":\"family\"}"
}
```

## # <<CODE0>

Continue um fluxo de trabalho interrompido após a aprovação.

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

# # Entradas opcionais

- <<CODE0>: Caminho absoluto para o binário de Lagosta (omite para usar `PATH`).
- <<CODE2>: Directório de trabalho para o gasoduto (por omissão para o directório de trabalho do processo actual).
- <<CODE3>: Matar o subprocesso se exceder esta duração (por omissão: 20000).
- <<CODE4>: Matar o subprocesso se o stdout exceder este tamanho (por omissão: 512000).
- <<CODE5>: string JSON passou para `lobster run --args-json` (apenas arquivos de fluxo de trabalho).

# # Envelope de saída

A lagosta devolve um envelope JSON com um dos três status:

- <<CODE0> → terminado com sucesso
- <<CODE1> → pausado; `requiresApproval.resumeToken` é necessário retomar
- `cancelled` → explicitamente negado ou cancelado

A ferramenta apresenta o envelope em ambos `content` (pretty JSON) e `details` (objeto cru).

# # Aprovações

Se <<CODE0> estiver presente, inspecione o prompt e decida:

- <<CODE0> → retomar e continuar os efeitos secundários
- <<CODE1> → cancelar e finalizar o fluxo de trabalho

Use `approve --preview-from-stdin --limit N` para anexar uma pré-visualização do JSON às solicitações de aprovação sem cola personalizada jq/heredoc. Retomar tokens são agora compactos: Lagosta armazena fluxo de trabalho retomar o estado sob sua dir estado e devolve uma pequena chave token.

# # OpenProse

OpenProse pares bem com lagosta: use `/prose` para orquestrar preparação multi-agente, em seguida, executar um gasoduto de lagosta para aprovações determinísticas. Se um programa Prose precisar de lagosta, permita a ferramenta `lobster` para subagentes via `tools.subagents.tools`. Veja [OpenProse](/prose).

# # Segurança

- ** Apenas subprocesso local** — nenhuma chamada de rede do próprio plugin.
- **Sem segredos** — Lagosta não gerencia OAuth; ele chama ferramentas OpenClaw que fazem.
- **Sandbox-aware** — desabilitado quando o contexto da ferramenta é sandboxed.
- **Hardened** — `lobsterPath` deve ser absoluto se especificado; timeouts e limites de saída aplicados.

# # Resolução de problemas

- **<<CODE0>** → aumento `timeoutMs`, ou divisão de um gasoduto longo.
- **<<CODE2>** → aumentar `maxStdoutBytes` ou reduzir o tamanho da saída.
- **<<CODE4>** → garantir que o gasoduto funciona em modo de ferramenta e imprime apenas JSON.
- **<<CODE5>** → executar o mesmo gasoduto em um terminal para inspecionar stderr.

# # Saiba mais

- [Plugins] (/plugin)
- [O autor da ferramenta de Plugins] (</plugins/agent-tools)

# # Estudo de caso: fluxos de trabalho comunitários

Um exemplo público: um “segundo cérebro” CLI + gasodutos de lagosta que gerenciam três cofres Markdown (pessoal, parceiro, compartilhado). O CLI emite JSON para estatísticas, listas de entrada e escaneamentos obsoletos; Lobster prende esses comandos em fluxos de trabalho como `weekly-review`, `inbox-triage`, `memory-consolidation` e `shared-task-sync`, cada um com portões de aprovação. A IA lida com julgamento (categorização) quando disponível e volta para regras determinísticas quando não.

- Tópico: https://x.com/plattenschieber/status/2014508656335770033
- Repo: https://github.com/bloomedai/brain-cli
