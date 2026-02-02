---
summary: "CLI reference for `openclaw logs` (tail gateway logs via RPC)"
read_when:
  - You need to tail Gateway logs remotely (without SSH)
  - You want JSON log lines for tooling
---

#`openclaw logs`

Caudal Gateway logs de arquivos sobre RPC (funciona em modo remoto).

Relacionados:

- Visão geral do registo: [Logging] /logging

## Exemplos

```bash
openclaw logs
openclaw logs --follow
openclaw logs --json
openclaw logs --limit 500
```
