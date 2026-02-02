---
summary: "CLI reference for `openclaw onboard` (interactive onboarding wizard)"
read_when:
  - You want guided setup for gateway, workspace, auth, channels, and skills
---

#`openclaw onboard`

Assistente de bordo interativo (configuração local ou remota do Gateway).

Relacionados:

- Guia do assistente: [A bordo] /start/onboarding

## Exemplos

```bash
openclaw onboard
openclaw onboard --flow quickstart
openclaw onboard --flow manual
openclaw onboard --mode remote --remote-url ws://gateway-host:18789
```

Notas de fluxo:

-`quickstart`: prompts mínimos, gera automaticamente um token de gateway.
-`manual`: alertas completos para o porto/liga/auth (também conhecido por`advanced`.
- Primeira conversa mais rápida:`openclaw dashboard`(Control UI, sem configuração do canal).
