---
summary: "JSON-only LLM tasks for workflows (optional plugin tool)"
read_when:
  - You want a JSON-only LLM step inside workflows
  - You need schema-validated LLM output for automation
---

Tarefa LLM

`llm-task` é uma ferramenta de plugin opcional** que executa uma tarefa LLM somente JSON e
retorna saída estruturada (opcionalmente validada contra o esquema JSON).

Isto é ideal para motores de fluxo de trabalho como a lagosta: você pode adicionar um único passo LLM
sem escrever código OpenClaw personalizado para cada fluxo de trabalho.

# # Habilitar o plugin

1. Active o plugin:

```json
{
  "plugins": {
    "entries": {
      "llm-task": { "enabled": true }
    }
  }
}
```

2. Allowlist a ferramenta (é registrada com `optional: true`):

```json
{
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

# # Configuração (opcional)

```json
{
  "plugins": {
    "entries": {
      "llm-task": {
        "enabled": true,
        "config": {
          "defaultProvider": "openai-codex",
          "defaultModel": "gpt-5.2",
          "defaultAuthProfileId": "main",
          "allowedModels": ["openai-codex/gpt-5.2"],
          "maxTokens": 800,
          "timeoutMs": 30000
        }
      }
    }
  }
}
```

<<CODE0> é uma lista permitida de <<CODE1> strings. Se definido, qualquer pedido
fora da lista é rejeitada.

# # Parâmetros da ferramenta

- <<CODE0> (cadeia necessária)
- <<CODE1> (qualquer, opcional)
- <<CODE2> (objecto, esquema opcional JSON)
- `provider` (cadeia, opcional)
- <<CODE4> (cadeia, opcional)
- <<CODE5> (texto, opcional)
- `temperature` (número, opcional)
- `maxTokens` (número, opcional)
- `timeoutMs` (número, opcional)

# # Saída

Retorna `details.json` contendo o JSON analisado (e valida contra
<<CODE1> quando fornecido).

# # Exemplo: Passo de fluxo de trabalho de lagosta

```lobster
openclaw.invoke --tool llm-task --action json --args-json '{
  "prompt": "Given the input email, return intent and draft.",
  "input": {
    "subject": "Hello",
    "body": "Can you help?"
  },
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

# # Notas de segurança

- A ferramenta é **JSON-only** e instrui o modelo para produzir apenas JSON (não
código cercas, sem comentários).
- Não há ferramentas expostas ao modelo para esta execução.
- Tratar saída como não confiável, a menos que você valide com `schema`.
- Colocar aprovações antes de qualquer etapa de efeito colateral (enviar, pós, exec).
