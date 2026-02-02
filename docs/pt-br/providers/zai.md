---
summary: "Use Z.AI (GLM models) with OpenClaw"
read_when:
  - You want Z.AI / GLM models in OpenClaw
  - You need a simple ZAI_API_KEY setup
---

# Z.AI

Z.AI é a plataforma API para ** GLM** modelos. Ele fornece APIs REST para GLM e usa chaves API
para autenticação. Crie sua chave API no console Z.AI. OpenClaw usa o provedor `zai`
com uma chave de API Z.AI.

# # Configuração do CLI

```bash
openclaw onboard --auth-choice zai-api-key
# or non-interactive
openclaw onboard --zai-api-key "$ZAI_API_KEY"
```

# # Config snippet

```json5
{
  env: { ZAI_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "zai/glm-4.7" } } },
}
```

# # Notas

- Os modelos GLM estão disponíveis em `zai/<model>` (exemplo: `zai/glm-4.7`).
- Ver [/fornecedores/glm] (</providers/glm) para a visão geral da família do modelo.
- Z.AI usa a autenticação Bearer com sua chave API.
