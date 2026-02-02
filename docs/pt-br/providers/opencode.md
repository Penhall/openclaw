---
summary: "Use OpenCode Zen (curated models) with OpenClaw"
read_when:
  - You want OpenCode Zen for model access
  - You want a curated list of coding-friendly models
---

# OpenCode Zen

OpenCode Zen é uma lista **curada de modelos** recomendada pela equipe OpenCode para agentes de codificação.
É um caminho de acesso opcional de modelo hospedado que usa uma chave API e o provedor `opencode`.
Zen está atualmente em beta.

# # Configuração do CLI

```bash
openclaw onboard --auth-choice opencode-zen
# or non-interactive
openclaw onboard --opencode-zen-api-key "$OPENCODE_API_KEY"
```

# # Config snippet

```json5
{
  env: { OPENCODE_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "opencode/claude-opus-4-5" } } },
}
```

# # Notas

- <<CODE0> é também suportado.
- Você entra no Zen, adiciona detalhes de faturamento e copia sua chave API.
- Notas do OpenCode Zen por pedido; verifique o painel do OpenCode para obter detalhes.
