---
summary: "Model provider overview with example configs + CLI flows"
read_when:
  - You need a provider-by-provider model setup reference
  - You want example configs or CLI onboarding commands for model providers
---

# Provedores de modelos

Esta página cobre **LLM/modelo provedores** (não canais de chat como WhatsApp/Telegram).
Para regras de seleção de modelos, ver [/conceitos/modelos](<<<LINK0>>).

# # Regras rápidas

- Modelo de refs use <<CODE0>> (exemplo: <<CODE1>>>).
- Se você definir <<CODE2>>, torna-se a lista de permissões.
- Ajudantes de CLI: <<CODE3>>, <HTML4>>>, <<CODE5>>.

# # Provedores incorporados (catálogo pi-ai)

Naves OpenClaw com o catálogo pi-ai. Estes prestadores exigem **não**
<<CODE0>> config; basta definir auth + escolher um modelo.

# # OpenAI

- Fornecedor: <<CODE0>>
- Autêntico: <<CODE1>>
- Modelo de exemplo: <<CODE2>>>
- CLI: <<CODE3>>

```json5
{
  agents: { defaults: { model: { primary: "openai/gpt-5.2" } } },
}
```

Antrópico

- Fornecedor: <<CODE0>>
- Autorização: <<CODE1>> ou <<CODE2>>>
- Modelo de exemplo: <<CODE3>>>
- CLI: <<CODE4>> (paste setup- token) ou <<CODE5>>

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-5" } } },
}
```

## # Código OpenAI (Código)

- Fornecedor: <<CODE0>>
- Auth: Oauth (ChatGPT)
- Modelo de exemplo: <<CODE1>>
- CLI: <<CODE2>> ou <<CODE3>>>

```json5
{
  agents: { defaults: { model: { primary: "openai-codex/gpt-5.2" } } },
}
```

# # OpenCode Zen

- Fornecedor: <<CODE0>>
- Autorização: <<CODE1>> (ou <<CODE2>>>)
- Modelo de exemplo: <<CODE3>>>
- CLI: <<CODE4>>

```json5
{
  agents: { defaults: { model: { primary: "opencode/claude-opus-4-5" } } },
}
```

Google Gemini (chave API)

- Fornecedor: <<CODE0>>
- Autêntico: <<CODE1>>
- Modelo de exemplo: <<CODE2>>>
- CLI: <<CODE3>>

Google Vertex / Antigravidade / Gemini CLI

- Prestadores: <<CODE0>>, <<CODE1>>, <<CODE2>>
- Auth: Vertex usa gcloud ADC; Antigravity/Gemini CLI usa seus respectivos fluxos de autenticação
- Antigravity OAuth é enviado como um plugin empacotado (<<<CODE3>>, desativado por padrão).
- Activar: <<CODE4>>>
- Login: <<CODE5>>
- Gemini CLI OAuth é enviado como um plugin empacotado (<<<CODE6>>, desativado por padrão).
- Activar: <<CODE7>>>
- Login: <<CODE8>>>
- Nota: você não ** colar um ID do cliente ou segredo em <<CODE9>>. As lojas de fluxo de login CLI
tokens em perfis de autenticação na máquina de gateway.

Z.AI (GLM)

- Fornecedor: <<CODE0>>
- Autêntico: <<CODE1>>
- Modelo de exemplo: <<CODE2>>>
- CLI: <<CODE3>>
- Apelidos: <<CODE4>> e <<CODE5> normalizar para <<CODE6>

Vercel AI Gateway

- Fornecedor: <<CODE0>>
- Autêntico: <<CODE1>>
- Modelo de exemplo: <<CODE2>>>
- CLI: <<CODE3>>

# # # Outros fornecedores integrados

- OpenRouter: <<CODE0>> (<<CODE1>>)
- Modelo de exemplo: <<CODE2>>>
- xAI: <<CODE3>> (<<CODE4>>>)
- Groq: <<CODE5> (<<CODE6>>)
- Cerebras: <<CODE7>> (<<CODE8>>)
- Os modelos GLM em Cerebras usam ids <<CODE9>> e <<CODE10>>>.
- URL base compatível com OpenAI: <<CODE11>>.
- Mistral: <<CODE12>> (<HTML13>>>)
- Co-piloto GitHub: <<CODE14>> (<<CODE15>>/ <<CODE16>>/ <<CODE17>>)

# # Provedores via <<CODE0>> (URL custom/base)

Utilizar <<CODE0>> (ou <<CODE1>>>>) para adicionar ** fornecedores personalizados** ou
OpenAI/Proxies compatíveis com antrópicos.

AI Moonshot (Kimi)

Moonshot usa terminais compatíveis com OpenAI, então configure-o como um provedor personalizado:

- Fornecedor: <<CODE0>>
- Autêntico: <<CODE1>>
- Modelo de exemplo: <<CODE2>>>
- Kimi K2 modelo IDs:
{/  moonshot- kimi- k2- model- refs:start  /}
- <<CODE3>>
- <<CODE4>>
- <<CODE5>>
- <<CODE6>>
- <<CODE7>>
{/  moonshot- kimi-k2- model-refs:end  /}

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

- Fornecedor: <<CODE0>>
- Autêntico: <<CODE1>>
- Modelo de exemplo: <<CODE2>>>

```json5
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: { model: { primary: "kimi-coding/k2p5" } },
  },
}
```

# # Qwen OAuth (camada livre)

Qwen fornece acesso OAuth ao Qwen Coder + Vision através de um fluxo de código de dispositivo.
Activar o 'plugin' empacotado e, em seguida, iniciar sessão:

```bash
openclaw plugins enable qwen-portal-auth
openclaw models auth login --provider qwen-portal --set-default
```

Modelo refs:

- <<CODE0>>
- <<CODE1>>

Ver [/fornecedores/qwen](<<<LINK0>>>) para detalhes e notas de configuração.

Sintético

O sintético fornece modelos compatíveis com Antrópicos por trás do provedor <<CODE0>>:

- Fornecedor: <<CODE0>>
- Autêntico: <<CODE1>>
- Modelo de exemplo: <<CODE2>>>
- CLI: <<CODE3>>

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

# # # MiniMax

MiniMax é configurado via <<CODE0>> porque usa endpoints personalizados:

- MiniMax (compatível com antrópicos): <<CODE0>>
- Autêntico: <<CODE1>>

Veja [/fornecedores/minimax](<<<LINK0>>) para detalhes de configuração, opções de modelo e trechos de configuração.

Ollama

Ollama é um runtime LLM local que fornece uma API compatível com OpenAI:

- Fornecedor: <<CODE0>>
- Auth: Nenhum necessário (servidor local)
- Modelo de exemplo: <<CODE1>>
- Instalação: https://olama.ai

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

O Ollama é detectado automaticamente quando roda localmente em <<CODE0>>>. Ver [/fornecedores/ollama](<<<LINK0>>) para recomendações de modelo e configuração personalizada.

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

- Para os prestadores personalizados, <<CODE0>>, <<CODE1>>, <<CODE2>>, <<CODE3>>, e <<CODE4>> são facultativas.
Quando omitido, o OpenClaw é padrão para:
- <<CODE5>>
- <<CODE6>>
- <<CODE7>>
- <<CODE8>>
- <<CODE9>>
- Recomendado: definir valores explícitos que correspondam aos limites do seu proxy/modelo.

# # Exemplos de CLI

```bash
openclaw onboard --auth-choice opencode-zen
openclaw models set opencode/claude-opus-4-5
openclaw models list
```

Veja também: [/gateway/configuration](<<<LINK0>>) para exemplos completos de configuração.
