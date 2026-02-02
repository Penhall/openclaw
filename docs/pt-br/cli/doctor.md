---
summary: "CLI reference for `openclaw doctor` (health checks + guided repairs)"
read_when:
  - You have connectivity/auth issues and want guided fixes
  - You updated and want a sanity check
---

#`openclaw doctor`

Verificações de saúde + correções rápidas para o gateway e canais.

Relacionados:

- Resolução de problemas:
- Auditoria de segurança: [Segurança] /gateway/security

## Exemplos

```bash
openclaw doctor
openclaw doctor --repair
openclaw doctor --deep
```

Notas:

- Os prompts interativos (como as correções de chaveiro/OAuth) só são executados quando o stdin é um TTY e o`--non-interactive`é **not set. Executar sem cabeça (cron, Telegram, nenhum terminal) irá pular prompts.
-`--fix`(também conhecido por`--repair` escreve um backup para`~/.openclaw/openclaw.json.bak`e solta chaves de configuração desconhecidas, listando cada remoção.

## macOS:`launchctl`env substitui

Se você executou anteriormente`launchctl setenv OPENCLAW_GATEWAY_TOKEN ...`(ou`...PASSWORD`, esse valor substitui seu arquivo de configuração e pode causar erros persistentes “não autorizados”.

```bash
launchctl getenv OPENCLAW_GATEWAY_TOKEN
launchctl getenv OPENCLAW_GATEWAY_PASSWORD

launchctl unsetenv OPENCLAW_GATEWAY_TOKEN
launchctl unsetenv OPENCLAW_GATEWAY_PASSWORD
```
