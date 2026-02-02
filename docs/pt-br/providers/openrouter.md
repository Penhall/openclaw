---
summary: "Use OpenRouter's unified API to access many models in OpenClaw"
read_when:
  - You want a single API key for many LLMs
  - You want to run models via OpenRouter in OpenClaw
---

OpenRouter

OpenRouter fornece uma API **unificada que encaminha pedidos para muitos modelos atrás de um único
Endpoint e chave API. É compatível com OpenAI, então a maioria dos SDKs do OpenAI funcionam mudando a URL base.

# # Configuração do CLI

```bash
openclaw onboard --auth-choice apiKey --token-provider openrouter --token "$OPENROUTER_API_KEY"
```

# # Config snippet

```json5
{
  env: { OPENROUTER_API_KEY: "sk-or-..." },
  agents: {
    defaults: {
      model: { primary: "openrouter/anthropic/claude-sonnet-4-5" },
    },
  },
}
```

# # Notas

- Os refs-modelo são `openrouter/<provider>/<model>`.
- Para mais opções de modelo/fornecedor, ver [/conceitos/fornecedores de modelo](/concepts/model-providers).
- OpenRouter usa um token Bearer com sua chave API sob o capô.
