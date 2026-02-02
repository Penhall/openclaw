---
summary: "Model providers (LLMs) supported by OpenClaw"
read_when:
  - You want to choose a model provider
  - You want quick setup examples for LLM auth + model selection
---

# Provedores de Modelo

Openclaw pode usar muitos provedores LLM. Escolha um, autentique, e depois defina o padrão
modelo como `provider/model`.

# # Destaque: Venius (Veneza AI)

Venius é nossa configuração de IA de Veneza recomendada para a primeira inferência de privacidade com uma opção de usar Opus para as tarefas mais difíceis.

- Padrão: `venice/llama-3.3-70b`
- Melhor global: `venice/claude-opus-45` (Opus permanece o mais forte)

Ver [AI de Veneza] (</providers/venice).

# # Início rápido (dois passos)

1. Autenticar com o provedor (geralmente via `openclaw onboard`).
2. Defina o modelo padrão:

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-5" } } },
}
```

# # Provedores suportados (set inicial)

- [OpenAI (API + Codex)] (</providers/openai)
- [Antrópico (API + Código CLI Claude)] (</providers/anthropic)
- [OpenRouter] (/providers/openrouter)
- [Vercel AI Gateway]
- [I.A. (Kimi + Kimi Coding)] (</providers/moonshot)
- [Sintético] (</providers/synthetic)
- [OpenCode Zen] (</providers/opencode)
- [Z.AI] (/providers/zai)
- [Modelos GLM] (</providers/glm)
- [MiniMax] (</providers/minimax)
- [Venius (Venice AI)] (/providers/venice)
- [Amazon Bedrock] (</bedrock)

Para o catálogo completo do fornecedor (xAI, Groq, Mistral, etc.) e configuração avançada,
ver [Fornecedores de modelos] (</concepts/model-providers).
