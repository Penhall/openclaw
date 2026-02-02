---
summary: "GLM model family overview + how to use it in OpenClaw"
read_when:
  - You want GLM models in OpenClaw
  - You need the model naming convention and setup
---

# Modelos GLM

GLM é uma família de modelos** (não uma empresa) disponível através da plataforma Z.AI. Em Openclaw, GLM
modelos são acessados através do provedor `zai` e IDs de modelo como `zai/glm-4.7`.

# # Configuração do CLI

```bash
openclaw onboard --auth-choice zai-api-key
```

# # Config snippet

```json5
{
  env: { ZAI_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "zai/glm-4.7" } } },
}
```

# # Notas

- As versões e disponibilidade do GLM podem ser alteradas; verifique os documentos do Z.AI para mais recentes.
- Os identificadores de modelo de exemplo incluem `glm-4.7` e `glm-4.6`.
- Para mais informações sobre o fornecedor, ver [/fornecedores/zai] (</providers/zai).
