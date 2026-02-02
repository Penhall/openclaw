---
summary: "CLI reference for `openclaw config` (get/set/unset config values)"
read_when:
  - You want to read or edit config non-interactively
---

#`openclaw config`

Ajudantes de configuração: obter/set/desset valores por caminho. Executar sem um subcomando para abrir
o assistente de configuração (mesmo que`openclaw configure`.

## Exemplos

```bash
openclaw config get browser.executablePath
openclaw config set browser.executablePath "/usr/bin/google-chrome"
openclaw config set agents.defaults.heartbeat.every "2h"
openclaw config set agents.list[0].tools.exec.node "node-id-or-name"
openclaw config unset tools.web.search.apiKey
```

## Caminhos

Os caminhos usam a notação do ponto ou do suporte:

```bash
openclaw config get agents.defaults.workspace
openclaw config get agents.list[0].id
```

Use o índice de lista de agentes para direcionar um agente específico:

```bash
openclaw config get agents.list
openclaw config set agents.list[1].tools.exec.node "node-id-or-name"
```

## Valores

Os valores são analisados como JSON5 quando possível; caso contrário, eles são tratados como strings.
Use`--json`para exigir análise JSON5.

```bash
openclaw config set agents.defaults.heartbeat.every "0m"
openclaw config set gateway.port 19001 --json
openclaw config set channels.whatsapp.groups '["*"]' --json
```

Reinicie o gateway após as edições.
