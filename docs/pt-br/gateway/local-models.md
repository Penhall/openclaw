---
summary: "Run OpenClaw on local LLMs (LM Studio, vLLM, LiteLLM, custom OpenAI endpoints)"
read_when:
  - You want to serve models from your own GPU box
  - You are wiring LM Studio or an OpenAI-compatible proxy
  - You need the safest local model guidance
---

Modelos locais

Local é viável, mas OpenClaw espera grande contexto + defesas fortes contra injeção rápida. Pequenos cartões truncam o contexto e fugas de segurança. Mirar alto: **2 Maxed-out Mac Studios ou equivalente GPU rig (~$30k+)**. Uma única **24 GB** GPU funciona apenas para prompts mais leves com maior latência. Use a ** maior / variante do modelo full-size que você pode executar**; quantizados agressivamente ou “pequenos” checkpoints aumentam o risco de injeção rápida (ver [Segurança](<<<LINK0>>)).

# # Recomendado: LM Studio + MiniMax M2.1 (Responses API, tamanho completo)

Melhor pilha local atual. Carregar MiniMax M2.1 no LM Studio, habilitar o servidor local (padrão <<CODE0>>), e usar a API Responses para manter o raciocínio separado do texto final.

```json5
{
  agents: {
    defaults: {
      model: { primary: "lmstudio/minimax-m2.1-gs32" },
      models: {
        "anthropic/claude-opus-4-5": { alias: "Opus" },
        "lmstudio/minimax-m2.1-gs32": { alias: "Minimax" },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      lmstudio: {
        baseUrl: "http://127.0.0.1:1234/v1",
        apiKey: "lmstudio",
        api: "openai-responses",
        models: [
          {
            id: "minimax-m2.1-gs32",
            name: "MiniMax M2.1 GS32",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 196608,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

** Lista de verificação de configuração **

- Instalar o LM Studio: https://lmstudio.ai
- No LM Studio, faça o download da **maior compilação MiniMax M2.1 disponível** (evitar “pequenas”/variantes quantizadas pesadas), inicie o servidor, confirme <<CODE0>> lista-o.
- Mantenha o modelo carregado; carga fria adiciona latência de inicialização.
- Ajustar <<CODE1>/<<CODE2> se a sua compilação LM Studio difere.
- Para WhatsApp, atenha-se à API Responses para que apenas o texto final seja enviado.

Mantenha os modelos hospedados configurados mesmo quando estiver rodando local; use <<CODE0> para que os fallbacks fiquem disponíveis.

### Configuração híbrida: acolhimento primário, recurso local

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["lmstudio/minimax-m2.1-gs32", "anthropic/claude-opus-4-5"],
      },
      models: {
        "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
        "lmstudio/minimax-m2.1-gs32": { alias: "MiniMax Local" },
        "anthropic/claude-opus-4-5": { alias: "Opus" },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      lmstudio: {
        baseUrl: "http://127.0.0.1:1234/v1",
        apiKey: "lmstudio",
        api: "openai-responses",
        models: [
          {
            id: "minimax-m2.1-gs32",
            name: "MiniMax M2.1 GS32",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 196608,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## # Local-primeiro com rede de segurança hospedada

Mude a ordem primária e de retorno; mantenha os mesmos provedores bloqueados e <<CODE0> para que você possa voltar para Sonnet ou Opus quando a caixa local estiver para baixo.

## # Hospedagem regional / roteamento de dados

- As variantes MiniMax/Kimi/GLM hospedadas também existem no OpenRouter com endpoints baseados em regiões (por exemplo, hospedados nos EUA). Escolha a variante regional lá para manter o tráfego em sua jurisdição escolhida, enquanto ainda usando <<CODE0>> para retrocessos Antrópicos/OpenAI.
- Somente local permanece o caminho de privacidade mais forte; roteamento regional hospedado é o meio-termo quando você precisa de recursos do provedor, mas quer controle sobre o fluxo de dados.

# # Outras proxies locais compatíveis com OpenAI

vLLM, LiteLLM, OAI-proxy, ou gateways personalizados funcionam se eles expõem um OpenAI-estilo <<CODE0> endpoint. Substitua o bloco do provedor acima por seu endpoint e ID do modelo:

```json5
{
  models: {
    mode: "merge",
    providers: {
      local: {
        baseUrl: "http://127.0.0.1:8000/v1",
        apiKey: "sk-local",
        api: "openai-responses",
        models: [
          {
            id: "my-local-model",
            name: "Local Model",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 120000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

Mantenha <<CODE0> para que os modelos hospedados permaneçam disponíveis.

# # Resolução de problemas

- A Gateway consegue contactar o procurador? <<CODE0>>.
- O modelo LM Studio está descarregado? Recarregar; início frio é uma causa comum de “pendura”.
- Erros de contexto? Abaixe <<CODE1>> ou aumente o limite do servidor.
- Segurança: os modelos locais ignoram os filtros do lado do fornecedor; mantêm os agentes estreitos e compactados para limitar o raio de explosão da injecção rápida.
