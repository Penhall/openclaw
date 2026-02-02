---
summary: "CLI reference for `openclaw security` (audit and fix common security footguns)"
read_when:
  - You want to run a quick security audit on config/state
  - You want to apply safe “fix” suggestions (chmod, tighten defaults)
---

#`openclaw security`

Ferramentas de segurança (auditoria + correções opcionais).

Relacionados:

- Guia de segurança: [Segurança] /gateway/security

## Audição

```bash
openclaw security audit
openclaw security audit --deep
openclaw security audit --fix
```

A auditoria avisa quando vários remetentes de DM compartilham a sessão principal e recomenda`session.dmScope="per-channel-peer"`(ou`per-account-channel-peer`para canais multi-conta) para caixas de entrada compartilhadas.
Também avisa quando pequenos modelos `<=300B` são usados sem sandboxing e com ferramentas web/browser habilitadas.
