---
summary: "CLI reference for `openclaw cron` (schedule and run background jobs)"
read_when:
  - You want scheduled jobs and wakeups
  - You’re debugging cron execution and logs
---

#`openclaw cron`

Gerencie trabalhos de cron para o programador Gateway.

Relacionados:

- Trabalhos de Cron: [Trabalhos de Cron] /automation/cron-jobs

Dica: execute`openclaw cron --help`para a superfície de comando completa.

## Edições comuns

Atualizar as configurações de entrega sem alterar a mensagem:

```bash
openclaw cron edit <job-id> --deliver --channel telegram --to "123456789"
```

Desactivar a entrega para uma tarefa isolada:

```bash
openclaw cron edit <job-id> --no-deliver
```
