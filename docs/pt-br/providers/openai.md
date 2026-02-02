---
summary: "Use OpenAI via API keys or Codex subscription in OpenClaw"
read_when:
  - You want to use OpenAI models in OpenClaw
  - You want Codex subscription auth instead of API keys
---

OpenAI

O OpenAI oferece APIs de desenvolvedores para modelos GPT. O Codex suporta **ChatGPT sign-in** para assinatura
acesso ou ** chave API** sinal de acesso baseado no uso. A nuvem de codex requer o login do ChatGPT.

# # Opção A: OpenAI API chave (OpenAI Platform)

**Melhor para:** acesso direto à API e faturamento baseado em uso.
Obtenha sua chave de API no painel OpenAI.

Configuração do CLI

```bash
openclaw onboard --auth-choice openai-api-key
# or non-interactive
openclaw onboard --openai-api-key "$OPENAI_API_KEY"
```

### Config snippet

```json5
{
  env: { OPENAI_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "openai/gpt-5.2" } } },
}
```

# # Opção B: Assinatura do Código OpenAI (Código)

**Melhor para:** usando o acesso de assinatura ChatGPT/Codex em vez de uma chave API.
A nuvem do Codex requer o login do ChatGPT, enquanto o CLI do Codex suporta o login do ChatGPT ou da chave da API.

Configuração do CLI

```bash
# Run Codex OAuth in the wizard
openclaw onboard --auth-choice openai-codex

# Or run OAuth directly
openclaw models auth login --provider openai-codex
```

### Config snippet

```json5
{
  agents: { defaults: { model: { primary: "openai-codex/gpt-5.2" } } },
}
```

# # Notas

- Os refs do modelo utilizam sempre `provider/model` (ver [/conceitos/modelos](/concepts/models)).
- Detalhes de autenticação + regras de reutilização estão em [/conceitos/outh] (</concepts/oauth).
