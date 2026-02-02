---
summary: "CLI reference for `openclaw agent` (send one agent turn via the Gateway)"
read_when:
  - You want to run one agent turn from scripts (optionally deliver reply)
---

#`openclaw agent`

Executar uma volta de agente através do Gateway (use`--local`para incorporado).
Use`--agent <id>`para direcionar um agente configurado diretamente.

Relacionados:

- Ferramenta de envio do agente: [Agent send] /tools/agent-send

## Exemplos

```bash
openclaw agent --to +15555550123 --message "status update" --deliver
openclaw agent --agent ops --message "Summarize logs"
openclaw agent --session-id 1234 --message "Summarize inbox" --thinking medium
openclaw agent --agent ops --message "Generate report" --deliver --reply-channel slack --reply-to "#reports"
```
