---
summary: "Use Synthetic's Anthropic-compatible API in OpenClaw"
read_when:
  - You want to use Synthetic as a model provider
  - You need a Synthetic API key or base URL setup
---

Sintético

O sintético expõe os objetivos compatíveis com o antrópico. Openclaw registra-o como o
`synthetic` provedor e usa a API Mensagens Antrópicas.

# # Montagem rápida

1. Definir `SYNTHETIC_API_KEY` (ou executar o assistente abaixo).
2. Executar a bordo:

```bash
openclaw onboard --auth-choice synthetic-api-key
```

O modelo padrão está definido como:

```
synthetic/hf:MiniMaxAI/MiniMax-M2.1
```

# # Exemplo de configuração

```json5
{
  env: { SYNTHETIC_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.1" },
      models: { "synthetic/hf:MiniMaxAI/MiniMax-M2.1": { alias: "MiniMax M2.1" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      synthetic: {
        baseUrl: "https://api.synthetic.new/anthropic",
        apiKey: "${SYNTHETIC_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "hf:MiniMaxAI/MiniMax-M2.1",
            name: "MiniMax M2.1",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 192000,
            maxTokens: 65536,
          },
        ],
      },
    },
  },
}
```

Nota: Cliente Antrópico do OpenClaw adiciona `/v1` ao URL base, então use
<<CODE1> (não `/anthropic/v1`). Se alterações sintéticas
sua URL base, sobreponha `models.providers.synthetic.baseUrl`.

# # Catálogo modelo

Todos os modelos abaixo do custo de uso `0` (input/output/cache).

□ ID do modelo □ Janela de contexto
---------------------------------------------
* <<CODE0> > 192000 * 65536 * texto falso *
* `hf:moonshotai/Kimi-K2-Thinking` * 256000 * 8192 * texto verdadeiro *
* <<CODE2> > 198000 * 128000 * texto falso *
* `hf:deepseek-ai/DeepSeek-R1-0528` * 128000 * 8192 * texto falso *
* `hf:deepseek-ai/DeepSeek-V3-0324` * 128000 * 8192 * texto falso *
* `hf:deepseek-ai/DeepSeek-V3.1` * 128000 * 8192 * texto falso *
* `hf:deepseek-ai/DeepSeek-V3.1-Terminus` * 128000 * 8192 * texto falso *
* `hf:deepseek-ai/DeepSeek-V3.2` * 159000 * 8192 * texto falso *
* `hf:meta-llama/Llama-3.3-70B-Instruct` * 128000 * 8192 * texto falso *
* `hf:meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` * 524000 * 8192 * texto falso *
* `hf:moonshotai/Kimi-K2-Instruct-0905` * 256000 * 8192 * texto falso *
* `hf:openai/gpt-oss-120b` * 128000 * 8192 * texto falso *
* `hf:Qwen/Qwen3-235B-A22B-Instruct-2507` * 256000 * 8192 * texto falso *
* `hf:Qwen/Qwen3-Coder-480B-A35B-Instruct` * 256000 * 8192 * texto falso *
* `hf:Qwen/Qwen3-VL-235B-A22B-Instruct` * 250000 * 8192 * falso * texto + imagem *
* `hf:zai-org/GLM-4.5` * 128000 * 128000 * texto falso *
* `hf:zai-org/GLM-4.6` * 198000 * 128000 * texto falso *
* `hf:deepseek-ai/DeepSeek-V3` * 128000 * 8192 * texto falso *
* `hf:Qwen/Qwen3-235B-A22B-Thinking-2507` * 256000 * 8192 * texto verdadeiro *

# # Notas

- Modelo de refs use `synthetic/<modelId>`.
- Se activar uma lista de permissões de modelos (<`agents.defaults.models`), adicione cada modelo que
plano de utilização.
- Ver [Fornecedores de modelos] (</concepts/model-providers) para as regras do fornecedor.
