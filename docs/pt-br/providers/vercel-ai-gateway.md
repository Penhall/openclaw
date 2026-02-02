---
title: "Vercel AI Gateway"
summary: "Vercel AI Gateway setup (auth + model selection)"
read_when:
  - You want to use Vercel AI Gateway with OpenClaw
  - You need the API key env var or CLI auth choice
---

Vercel AI Gateway

O [Vercel AI Gateway] (<https://vercel.com/ai-gateway) fornece uma API unificada para acessar centenas de modelos através de um único endpoint.

- Fornecedor: `vercel-ai-gateway`
- Autorização: `AI_GATEWAY_API_KEY`
- API: Mensagens Antrópicas compatíveis

# # Começo rápido

1. Defina a chave API (recomendada: armazene-a para o Gateway):

```bash
openclaw onboard --auth-choice ai-gateway-api-key
```

2. Defina um modelo padrão:

```json5
{
  agents: {
    defaults: {
      model: { primary: "vercel-ai-gateway/anthropic/claude-opus-4.5" },
    },
  },
}
```

# # Exemplo não-interactivo

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice ai-gateway-api-key \
  --ai-gateway-api-key "$AI_GATEWAY_API_KEY"
```

# # Nota ambiental

Se o Gateway for executado como um daemon (lançado/systemd), certifique-se de <<CODE0>
está disponível para esse processo (por exemplo, em `~/.openclaw/.env` ou via
<<CODE2>).
