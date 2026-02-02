---
summary: "Configure Moonshot K2 vs Kimi Coding (separate providers + keys)"
read_when:
  - You want Moonshot K2 (Moonshot Open Platform) vs Kimi Coding setup
  - You need to understand separate endpoints, keys, and model refs
  - You want copy/paste config for either provider
---

# Moonshot AI (Kimi)

Moonshot fornece a API Kimi com terminais compatíveis com OpenAI. Configurar o
provedor e definir o modelo padrão para `moonshot/kimi-k2.5`, ou usar
Kimi Coding com `kimi-coding/k2p5`.

IDs atuais do modelo Kimi K2:
{/  Moonshot- kimi-k2-ids:start  /}

- <<CODE0>
- <<CODE1>
- <<CODE2>
- `kimi-k2-thinking`
- `kimi-k2-thinking-turbo`
{/  moonshot-kimi-k2-ids:end  /}

```bash
openclaw onboard --auth-choice moonshot-api-key
```

Codificação Kimi:

```bash
openclaw onboard --auth-choice kimi-code-api-key
```

Nota: Moonshot e Kimi Coding são fornecedores separados. As chaves não são intercambiáveis, os objetivos diferem e os refs do modelo diferem (usos de Moonshot `moonshot/...`, Kimi Coding usa `kimi-coding/...`).

## Config snippet (A API da Lua)

```json5
{
  env: { MOONSHOT_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "moonshot/kimi-k2.5" },
      models: {
        // moonshot-kimi-k2-aliases:start
        "moonshot/kimi-k2.5": { alias: "Kimi K2.5" },
        "moonshot/kimi-k2-0905-preview": { alias: "Kimi K2" },
        "moonshot/kimi-k2-turbo-preview": { alias: "Kimi K2 Turbo" },
        "moonshot/kimi-k2-thinking": { alias: "Kimi K2 Thinking" },
        "moonshot/kimi-k2-thinking-turbo": { alias: "Kimi K2 Thinking Turbo" },
        // moonshot-kimi-k2-aliases:end
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [
          // moonshot-kimi-k2-models:start
          {
            id: "kimi-k2.5",
            name: "Kimi K2.5",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          {
            id: "kimi-k2-0905-preview",
            name: "Kimi K2 0905 Preview",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          {
            id: "kimi-k2-turbo-preview",
            name: "Kimi K2 Turbo",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          {
            id: "kimi-k2-thinking",
            name: "Kimi K2 Thinking",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          {
            id: "kimi-k2-thinking-turbo",
            name: "Kimi K2 Thinking Turbo",
            reasoning: true,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
          // moonshot-kimi-k2-models:end
        ],
      },
    },
  },
}
```

# # Kimi Coding

```json5
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "kimi-coding/k2p5" },
      models: {
        "kimi-coding/k2p5": { alias: "Kimi K2.5" },
      },
    },
  },
}
```

# # Notas

- Os refs do modelo Moonshot usam `moonshot/<modelId>`. Kimi Coding modelo refs usar `kimi-coding/<modelId>`.
- Substituir preços e metadados de contexto em <<CODE2>, se necessário.
- Se Moonshot publicar diferentes limites de contexto para um modelo, ajustar
<<CODE3> em conformidade.
- Utilizar `https://api.moonshot.cn/v1` se necessitar do parâmetro final da China.
