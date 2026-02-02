---
summary: "Model providers (LLMs) supported by OpenClaw"
read_when:
  - You want to choose a model provider
  - You need a quick overview of supported LLM backends
---

# Provedores de Modelo

Openclaw pode usar muitos provedores LLM. Escolha um provedor, autentique-se e defina o
modelo padrão como `provider/model`.

À procura de documentos de canais de conversação (WhatsApp/Telegram/Discord/Slack/Mattermost (plugin)/etc.)? Ver [Canais] (</channels).

# # Destaque: Venius (Veneza AI)

Venius é nossa configuração de IA de Veneza recomendada para a primeira inferência de privacidade com uma opção de usar Opus para tarefas difíceis.

- Padrão: `venice/llama-3.3-70b`
- Melhor global: `venice/claude-opus-45` (Opus permanece o mais forte)

Ver [AI de Veneza] (</providers/venice).

# # Começo rápido

1. Autenticar com o provedor (geralmente via `openclaw onboard`).
2. Defina o modelo padrão:

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-5" } } },
}
```

# # Docs provedor

- [OpenAI (API + Codex)] (</providers/openai)
- [Antrópico (API + Código CLI Claude)] (</providers/anthropic)
- [Qwen (OAuth)] (</providers/qwen)
- [OpenRouter] (</providers/openrouter)
- [Vercel AI Gateway] (</providers/vercel-ai-gateway)
- [I.A. (Kimi + Kimi Coding)] (</providers/moonshot)
- [OpenCode Zen] (</providers/opencode)
- [Amazon Bedrock] (</bedrock)
- [Z.AI] (</providers/zai)
- [Xiaomi] (</providers/xiaomi)
- [Modelos GLM] (</providers/glm)
- [MiniMax] (</providers/minimax)
- [Venius (Venice AI, centrada na privacidade)] (</providers/venice)
- [Ollama (modelos locais)] (</providers/ollama)

# # Prestadores de transcrição

- [Deepgram (transcrição de áudio)] (</providers/deepgram)

# # Ferramentas comunitárias

- [Claude Max API Proxy] (</providers/claude-max-api-proxy) - Use a assinatura Claude Max/Pro como um endpoint API compatível com OpenAI

Para o catálogo completo do fornecedor (xAI, Groq, Mistral, etc.) e configuração avançada,
ver [Fornecedores de modelos] (</concepts/model-providers).
