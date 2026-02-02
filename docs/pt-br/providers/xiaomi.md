---
summary: "Use Xiaomi MiMo (mimo-v2-flash) with OpenClaw"
read_when:
  - You want Xiaomi MiMo models in OpenClaw
  - You need XIAOMI_API_KEY setup
---

Xiaomi MiMo

Xiaomi MiMo é a plataforma API para modelos **MiMo**. Ele fornece APIs REST compatíveis com
Formatos OpenAI e Anthropic e usa chaves API para autenticação. Criar sua chave de API em
a consola [Xiaomi MiMo] (<https://platform.xiaomimimo.com/#/console/api-keys). Usos do Openclaw
o provedor <<CODE0> com uma chave de API Xiaomi MiMo.

# # Vista geral do modelo

- **mimo-v2-flash**: janela de contexto 262144-token, compatível com API Mensagens Antrópicas.
- URL base: `https://api.xiaomimimo.com/anthropic`
- Autorização: `Bearer $XIAOMI_API_KEY`

# # Configuração do CLI

```bash
openclaw onboard --auth-choice xiaomi-api-key
# or non-interactive
openclaw onboard --auth-choice xiaomi-api-key --xiaomi-api-key "$XIAOMI_API_KEY"
```

# # Config snippet

```json5
{
  env: { XIAOMI_API_KEY: "your-key" },
  agents: { defaults: { model: { primary: "xiaomi/mimo-v2-flash" } } },
  models: {
    mode: "merge",
    providers: {
      xiaomi: {
        baseUrl: "https://api.xiaomimimo.com/anthropic",
        api: "anthropic-messages",
        apiKey: "XIAOMI_API_KEY",
        models: [
          {
            id: "mimo-v2-flash",
            name: "Xiaomi MiMo V2 Flash",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 262144,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

# # Notas

- Modelo ref: `xiaomi/mimo-v2-flash`.
- O fornecedor é injectado automaticamente quando <<CODE1> é definido (ou existe um perfil de autenticação).
- Ver [/conceitos/modelo-fornecedores](/concepts/model-providers) para as regras do prestador.
