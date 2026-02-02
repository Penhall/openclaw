---
summary: "CLI reference for `openclaw status` (diagnostics, probes, usage snapshots)"
read_when:
  - You want a quick diagnosis of channel health + recent session recipients
  - You want a pasteable “all” status for debugging
---

#`openclaw status`

Diagnóstico para canais + sessões.

```bash
openclaw status
openclaw status --all
openclaw status --deep
openclaw status --usage
```

Notas:

-`--deep`executa sondas ao vivo (WhatsApp Web + Telegram + Discord + Google Chat + Slack + Signal).
- Saída inclui lojas de sessão por agente quando vários agentes são configurados.
- Visão geral inclui Gateway + serviço de host nó instalar / status de execução quando disponível.
- Visão geral inclui canal de atualização + git SHA (para checkouts de origem).
- Atualizar superfícies de informação na Visão Geral; se uma atualização estiver disponível, o status imprime uma dica para executar`openclaw update`(ver [Atualização]/install/updating.
