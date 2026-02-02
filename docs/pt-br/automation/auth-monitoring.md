---
summary: "Monitor OAuth expiry for model providers"
read_when:
  - Setting up auth expiry monitoring or alerts
  - Automating Claude Code / Codex OAuth refresh checks
---

Monitoramento de autenticação

OpenClaw expõe a saúde expirada de OAuth via`openclaw models status`. Use isso para
automação e alerta; scripts são extras opcionais para fluxos de trabalho do telefone.

## Preferido: Verificação CLI (portátil)

```bash
openclaw models status --check
```

Códigos de saída:

-`0`: OK
-`1`: credenciais expiradas ou em falta
-`2`: expira em breve (dentro das 24h)

Isso funciona em cron/systemd e não requer scripts extras.

## scripts opcionais (ops / fluxos de trabalho de telefone)

Estes vivem sob`scripts/`e são ** opcional**. Eles assumem acesso SSH ao
gateway host e são sintonizados para systemd + Termux.

-`scripts/claude-auth-status.sh`utiliza agora o`openclaw models status --json`fonte da verdade (regressando ao arquivo direto lê se o CLI não estiver disponível),
Assim, manter`openclaw`em`PATH`para timers.
-`scripts/auth-monitor.sh`: alvo de temporizador cron/systemd; envia alertas (ntfy ou telefone).
-`scripts/systemd/openclaw-auth-monitor.{service,timer}`: temporizador de usuário sistematizado.
-`scripts/claude-auth-status.sh`: Claude Code + OpenClaw auth checker (full/json/simples).
-`scripts/mobile-reauth.sh`: fluxo de reauth guiado sobre SSH.
-`scripts/termux-quick-auth.sh`: status de widget de uma tap + URL de autenticação aberta.
-`scripts/termux-auth-widget.sh`: fluxo de widgets guiados.
-`openclaw models status --json`0: sync Claude Code creds → OpenClaw.

Se você não precisa de automação de telefone ou timers systemd, pule esses scripts.
