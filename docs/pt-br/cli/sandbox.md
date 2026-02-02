---
title: Sandbox CLI
summary: "Manage sandbox containers and inspect effective sandbox policy"
read_when: "You are managing sandbox containers or debugging sandbox/tool-policy behavior."
status: active
---

Caixa de areia CLI

Gerencie recipientes sandbox baseados em Docker para execução de agentes isolados.

## Visão geral

OpenClaw pode executar agentes em recipientes Docker isolados para segurança. Os comandos`sandbox`ajudam você a gerenciar esses recipientes, especialmente após atualizações ou alterações de configuração.

## Comandos

## #`openclaw sandbox explain`

Inspecione o **effective** sandbox mode/scope/workspace access, sandbox tool policy, and highed gates (with fix-it config key roads).

```bash
openclaw sandbox explain
openclaw sandbox explain --session agent:main:main
openclaw sandbox explain --agent work
openclaw sandbox explain --json
```

## #`openclaw sandbox list`

Listar todos os recipientes sandbox com o seu estado e configuração.

```bash
openclaw sandbox list
openclaw sandbox list --browser  # List only browser containers
openclaw sandbox list --json     # JSON output
```

** A saída inclui:**

- Nome e status do recipiente (correndo/parado)
- Imagem do Docker e se corresponde à configuração
- Idade (tempo desde a criação)
- Tempo inactivo (tempo desde a última utilização)
- Sessão associada/agente

## #`openclaw sandbox recreate`

Remover recipientes sandbox para forçar a recreação com imagens/configuração atualizadas.

```bash
openclaw sandbox recreate --all                # Recreate all containers
openclaw sandbox recreate --session main       # Specific session
openclaw sandbox recreate --agent mybot        # Specific agent
openclaw sandbox recreate --browser            # Only browser containers
openclaw sandbox recreate --all --force        # Skip confirmation
```

**Opções:**

-`--all`: Recriar todos os recipientes de areia
-`--session <key>`: Recriar recipiente para sessão específica
-`--agent <id>`: Recriar recipientes para agentes específicos
-`--browser`: Só recriar recipientes de navegador
-`--force`: Saltar o prompt de confirmação

**Importante:** Os recipientes são automaticamente recriados quando o agente é usado a seguir.

## Casos de uso

## # Depois de atualizar as imagens do Docker

```bash
# Pull new image
docker pull openclaw-sandbox:latest
docker tag openclaw-sandbox:latest openclaw-sandbox:bookworm-slim

# Update config to use new image
# Edit config: agents.defaults.sandbox.docker.image (or agents.list[].sandbox.docker.image)

# Recreate containers
openclaw sandbox recreate --all
```

## # Depois de mudar a configuração da caixa de areia

```bash
# Edit config: agents.defaults.sandbox.* (or agents.list[].sandbox.*)

# Recreate to apply new config
openclaw sandbox recreate --all
```

## Depois de mudar de configuraçãoCommand

```bash
openclaw sandbox recreate --all
# or just one agent:
openclaw sandbox recreate --agent family
```

## Para um agente específico apenas

```bash
# Update only one agent's containers
openclaw sandbox recreate --agent alfred
```

## Por que isso é necessário?

** Problema: ** Quando você atualiza imagens ou configuração da área sandbox:

- Contêineres existentes continuam rodando com configurações antigas
- Os recipientes só são podados após 24h de inatividade
- Os agentes utilizados regularmente mantêm contentores velhos a funcionar indefinidamente

**Solução:** Use`openclaw sandbox recreate`para forçar a remoção de recipientes antigos. Eles serão recriados automaticamente com as configurações atuais quando necessário.

Dica: prefira`openclaw sandbox recreate`em vez de manual`docker rm`. Utiliza o
O recipiente do Gateway nomeia e evita desigualdades quando as teclas de escopo/sessão mudam.

Configuração

Configurações da caixa de areia ao vivo em`~/.openclaw/openclaw.json`sob`agents.defaults.sandbox`(por-agente substitui ir em`agents.list[].sandbox`:

```jsonc
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "all", // off, non-main, all
        "scope": "agent", // session, agent, shared
        "docker": {
          "image": "openclaw-sandbox:bookworm-slim",
          "containerPrefix": "openclaw-sbx-",
          // ... more Docker options
        },
        "prune": {
          "idleHours": 24, // Auto-prune after 24h idle
          "maxAgeDays": 7, // Auto-prune after 7 days
        },
      },
    },
  },
}
```

## Veja também

- [Documentação da caixa de areia] /gateway/sandboxing
- [Configuração do agente] /concepts/agent-workspace
Verifica a configuração da caixa de areia.
