---
summary: "CLI reference for `openclaw health` (gateway health endpoint via RPC)"
read_when:
  - You want to quickly check the running Gateway’s health
---

#`openclaw health`

Vai buscar saúde ao portal.

```bash
openclaw health
openclaw health --json
openclaw health --verbose
```

Notas:

-`--verbose`executa sondas ao vivo e imprime timings por conta quando várias contas são configuradas.
- Saída inclui lojas de sessão por agente quando vários agentes são configurados.
