---
summary: "Model provider overview with example configs + CLI flows"
read_when:
  - You need a provider-by-provider model setup reference
  - You want example configs or CLI onboarding commands for model providers
---

# Provedores de modelos

Esta página cobre **LLM/modelo provedores** (não canais de chat como WhatsApp/Telegram).
Para regras de seleção de modelos, ver [/conceitos/modelos]/concepts/models.

## Regras rápidas

- Os árbitros-modelo utilizam`provider/model`(exemplo:`opencode/claude-opus-4-5`.
- Se você definir`agents.defaults.models`, torna-se a lista de permissão.
- Ajudantes de CLI:`openclaw onboard`,`openclaw models list`,`openclaw models set <provider/model>`.

## Provedores incorporados (catálogo pi-ai)

Naves OpenClaw com o catálogo pi-ai. Estes prestadores exigem **não**`models.providers`config; basta definir auth + escolher um modelo.

## OpenAI

- Provedor:`openai`- Auth:`OPENAI_API_KEY`- Modelo de exemplo:`openai/gpt-5.2`- CLI:`openclaw onboard --auth-choice openai-api-key`

```json5
{
  agents: { defaults: { model: { primary: "openai/gpt-5.2" } } },
}
```

Antrópico

- Provedor:`anthropic`- Autorização:`ANTHROPIC_API_KEY`ou`claude setup-token`- Modelo de exemplo:`anthropic/claude-opus-4-5`- CLI:`openclaw onboard --auth-choice token`(ficha de montagem em pasta) ou`openclaw models auth paste-token --provider anthropic`

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-5" } } },
}
```

## # Código OpenAI (Código)

- Provedor:`openai-codex`- Auth: Oauth (ChatGPT)
- Modelo de exemplo:`openai-codex/gpt-5.2`- CLI:`openclaw onboard --auth-choice openai-codex`ou`openclaw models auth login --provider openai-codex`

```json5
{
  agents: { defaults: { model: { primary: "openai-codex/gpt-5.2" } } },
}
```

## OpenCode Zen

- Provedor:`opencode`- Autorização:`OPENCODE_API_KEY`(ou`OPENCODE_ZEN_API_KEY`
- Modelo de exemplo:`opencode/claude-opus-4-5`- CLI:`openclaw onboard --auth-choice opencode-zen`

```json5
{
  agents: { defaults: { model: { primary: "opencode/claude-opus-4-5" } } },
}
```

Google Gemini (chave API)

- Provedor:`google`- Auth:`GEMINI_API_KEY`- Modelo de exemplo:`google/gemini-3-pro-preview`- CLI:`openclaw onboard --auth-choice gemini-api-key`

Google Vertex / Antigravidade / Gemini CLI

- Prestadores:`google-vertex`,`google-antigravity`,`google-gemini-cli`- Auth: Vertex usa gcloud ADC; Antigravity/Gemini CLI usa seus respectivos fluxos de autenticação
- Antigravity OAuth é enviado como um plugin empacotado `google-antigravity-auth`, desativado por padrão).
- Activar:`openclaw plugins enable google-antigravity-auth`- Login:`openclaw models auth login --provider google-antigravity --set-default`- Gemini CLI OAuth é enviado como um plugin empacotado `google-gemini-cli-auth`, desativado por padrão).
- Activar:`openclaw plugins enable google-gemini-cli-auth`- Login:`openclaw models auth login --provider google-gemini-cli --set-default`- Nota: você não ** colar um ID do cliente ou segredo em`openclaw.json`. As lojas de fluxo de login CLI
tokens em perfis de autenticação na máquina de gateway.

Z.AI (GLM)

- Provedor:`zai`- Auth:`ZAI_API_KEY`- Modelo de exemplo:`zai/glm-4.7`- CLI:`openclaw onboard --auth-choice zai-api-key`- Outros nomes:`z.ai/*`e`z-ai/*`normalizam para`zai/*`

Vercel AI Gateway

- Provedor:`vercel-ai-gateway`- Auth:`AI_GATEWAY_API_KEY`- Modelo de exemplo:`vercel-ai-gateway/anthropic/claude-opus-4.5`- CLI:`openclaw onboard --auth-choice ai-gateway-api-key`

### Outros fornecedores integrados

- OpenRouter:`openrouter``OPENROUTER_API_KEY`
- Modelo de exemplo:`openrouter/anthropic/claude-sonnet-4-5`- xAI:`xai``XAI_API_KEY`
- Groq:`groq``GROQ_API_KEY`
- Cerebras:`cerebras``CEREBRAS_API_KEY`
- Os modelos GLM em Cerebras usam IDs`zai-glm-4.7`e`OPENROUTER_API_KEY`0.
- URL base compatível com OpenAI:`OPENROUTER_API_KEY`1.
- Mistral:`OPENROUTER_API_KEY`2 `OPENROUTER_API_KEY`3)
- Copiloto GitHub:`OPENROUTER_API_KEY`4 `OPENROUTER_API_KEY`5 /`OPENROUTER_API_KEY`6 /`OPENROUTER_API_KEY`7)

## Provedores via`models.providers`( URL custom/base)

Utilizar`models.providers`(ou`models.json` para adicionar ** fornecedores personalizados** ou
OpenAI/Proxies compatíveis com antrópicos.

AI Moonshot (Kimi)

Moonshot usa terminais compatíveis com OpenAI, então configure-o como um provedor personalizado:

- Provedor:`moonshot`- Auth:`MOONSHOT_API_KEY`- Modelo de exemplo:`moonshot/kimi-k2.5`- Kimi K2 modelo IDs:
{/  moonshot- kimi- k2- model- refs:start  /}
-`moonshot/kimi-k2.5`-`moonshot/kimi-k2-0905-preview`-`moonshot/kimi-k2-turbo-preview`-`moonshot/kimi-k2-thinking`-`moonshot/kimi-k2-thinking-turbo`{/  moonshot- kimi-k2- model-refs:end  /}

```json5
{
  agents: {
    defaults: { model: { primary: "moonshot/kimi-k2.5" } },
  },
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [{ id: "kimi-k2.5", name: "Kimi K2.5" }],
      },
    },
  },
}
```

Kimi Coding

A codificação de Kimi usa o ponto final compatível com antrópicos da IA de Moonshot:

- Provedor:`kimi-coding`- Auth:`KIMI_API_KEY`- Modelo de exemplo:`kimi-coding/k2p5`

```json5
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: { model: { primary: "kimi-coding/k2p5" } },
  },
}
```

## Qwen OAuth (camada livre)

Qwen fornece acesso OAuth ao Qwen Coder + Vision através de um fluxo de código de dispositivo.
Activar o 'plugin' empacotado e, em seguida, iniciar sessão:

```bash
openclaw plugins enable qwen-portal-auth
openclaw models auth login --provider qwen-portal --set-default
```

Modelo refs:

-`qwen-portal/coder-model`-`qwen-portal/vision-model`

Ver [/fornecedores/qwen]/providers/qwen para detalhes e notas de configuração.

Sintético

O sintético fornece modelos compatíveis com Antrópicos por trás do provedor`synthetic`:

- Provedor:`synthetic`- Auth:`SYNTHETIC_API_KEY`- Modelo de exemplo:`synthetic/hf:MiniMaxAI/MiniMax-M2.1`- CLI:`openclaw onboard --auth-choice synthetic-api-key`

```json5
{
  agents: {
    defaults: { model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.1" } },
  },
  models: {
    mode: "merge",
    providers: {
      synthetic: {
        baseUrl: "https://api.synthetic.new/anthropic",
        apiKey: "${SYNTHETIC_API_KEY}",
        api: "anthropic-messages",
        models: [{ id: "hf:MiniMaxAI/MiniMax-M2.1", name: "MiniMax M2.1" }],
      },
    },
  },
}
```

### MiniMax

MiniMax é configurado via`models.providers`porque usa endpoints personalizados:

- MiniMax (compatível com antrópicos):`--auth-choice minimax-api`- Auth:`MINIMAX_API_KEY`

Veja [/fornecedores/minimax]/providers/minimax para detalhes de configuração, opções de modelo e trechos de configuração.

Ollama

Ollama é um runtime LLM local que fornece uma API compatível com OpenAI:

- Provedor:`ollama`- Auth: Nenhum necessário (servidor local)
- Modelo de exemplo:`ollama/llama3.3`- Instalação: https://olama.ai

```bash
# Install Ollama, then pull a model:
ollama pull llama3.3
```

```json5
{
  agents: {
    defaults: { model: { primary: "ollama/llama3.3" } },
  },
}
```

O Ollama é detectado automaticamente ao correr localmente em`http://127.0.0.1:11434/v1`. Ver [/fornecedores/ollama]/providers/ollama para recomendações de modelos e configuração personalizada.

## # Proxies locais (LM Studio, vLLM, LiteLLM, etc.)

Exemplo (OpenAI-compatível):

```json5
{
  agents: {
    defaults: {
      model: { primary: "lmstudio/minimax-m2.1-gs32" },
      models: { "lmstudio/minimax-m2.1-gs32": { alias: "Minimax" } },
    },
  },
  models: {
    providers: {
      lmstudio: {
        baseUrl: "http://localhost:1234/v1",
        apiKey: "LMSTUDIO_KEY",
        api: "openai-completions",
        models: [
          {
            id: "minimax-m2.1-gs32",
            name: "MiniMax M2.1",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

Notas:

- Os prestadores de serviços aduaneiros,`reasoning`,`input`,`cost`,`contextWindow`e`maxTokens`são facultativos.
Quando omitido, o OpenClaw é padrão para:
-`reasoning: false`-`input: ["text"]`-`cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 }`-`contextWindow: 200000`-`maxTokens: 8192`- Recomendado: definir valores explícitos que correspondam aos limites do seu proxy/modelo.

## Exemplos de CLI

```bash
openclaw onboard --auth-choice opencode-zen
openclaw models set opencode/claude-opus-4-5
openclaw models list
```

Veja também: [/gateway/configuration]/gateway/configuration para exemplos completos de configuração.
