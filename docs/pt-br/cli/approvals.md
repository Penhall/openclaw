---
summary: "CLI reference for `openclaw approvals` (exec approvals for gateway or node hosts)"
read_when:
  - You want to edit exec approvals from the CLI
  - You need to manage allowlists on gateway or node hosts
---

#`openclaw approvals`

Gerencie aprovações executivas para o host ** local**, ** gateway host**, ou um host **node**.
Por padrão, os comandos visam o arquivo de aprovações locais no disco. Use`--gateway`para direcionar o gateway, ou`--node`para direcionar um nó específico.

Relacionados:

- aprovações exec: [aprovações exec] /tools/exec-approvals
- Nós: [nós] /nodes

## Comandos comuns

```bash
openclaw approvals get
openclaw approvals get --node <id|name|ip>
openclaw approvals get --gateway
```

## Substituir aprovações de um arquivo

```bash
openclaw approvals set --file ./exec-approvals.json
openclaw approvals set --node <id|name|ip> --file ./exec-approvals.json
openclaw approvals set --gateway --file ./exec-approvals.json
```

## Ajudantes do Allowlist

```bash
openclaw approvals allowlist add "~/Projects/**/bin/rg"
openclaw approvals allowlist add --agent main --node <id|name|ip> "/usr/bin/uptime"
openclaw approvals allowlist add --agent "*" "/usr/bin/uname"

openclaw approvals allowlist remove "~/Projects/**/bin/rg"
```

## Notas

-`--node`usa o mesmo resolvedor que`openclaw nodes`(ID, nome, ip ou prefixo de id).
-`--agent`defaults to`"*"`, que se aplica a todos os agentes.
- O host de nó deve anunciar`system.execApprovals.get/set`(aplicativo macOS ou host de nó sem cabeça).
- Os ficheiros de aprovação são armazenados por host no`~/.openclaw/exec-approvals.json`.
