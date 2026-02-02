---
summary: "Run multiple OpenClaw Gateways on one host (isolation, ports, and profiles)"
read_when:
  - Running more than one Gateway on the same machine
  - You need isolated config/state/ports per Gateway
---

# Várias Gateways (mesma máquina)

A maioria das configurações deve usar um Gateway porque um único Gateway pode lidar com várias conexões de mensagens e agentes. Se você precisar de isolamento ou redundância mais forte (por exemplo, um bot de resgate), execute Gateways separados com perfis/portos isolados.

# # Lista de verificação de isolamento (obrigatório)

- <<CODE0>> — ficheiro de configuração por instance
- <<CODE1>> — sessões por instance, credos, caches
- <<CODE2>> — raiz do espaço de trabalho por instance
- <<CODE3> (ou <<CODE4>>) — exclusiva por exemplo
- As portas derivadas (browser/canvas) não devem sobrepor-se

Se estes forem compartilhados, você irá clicar em corridas de configuração e conflitos de portas.

# # Recomendado: perfis (<<CODE0>>)

Auto-scópio de perfis <<CODE0>> + <<CODE1>>> e nomes de serviços sufixos.

```bash
# main
openclaw --profile main setup
openclaw --profile main gateway --port 18789

# rescue
openclaw --profile rescue setup
openclaw --profile rescue gateway --port 19001
```

Serviços por perfil:

```bash
openclaw --profile main gateway install
openclaw --profile rescue gateway install
```

# # Guia do robô de resgate

Executar um segundo Gateway no mesmo host com o seu próprio:

- perfil/config
- dir estado
- espaço de trabalho
- porto base (portas mais derivadas)

Isso mantém o bot de resgate isolado do bot principal para que ele possa depurar ou aplicar alterações de configuração se o bot primário estiver para baixo.

Espaçamento de portas: deixar pelo menos 20 portas entre portas de base para que as portas derivadas navegador/canvas/CDP nunca colidem.

## # Como instalar (robô de resgate)

```bash
# Main bot (existing or fresh, without --profile param)
# Runs on port 18789 + Chrome CDC/Canvas/... Ports
openclaw onboard
openclaw gateway install

# Rescue bot (isolated profile + ports)
openclaw --profile rescue onboard
# Notes:
# - workspace name will be postfixed with -rescue per default
# - Port should be at least 18789 + 20 Ports,
#   better choose completely different base port, like 19789,
# - rest of the onboarding is the same as normal

# To install the service (if not happened automatically during onboarding)
openclaw --profile rescue gateway install
```

# # Mapa da porta (derivado)

Porta base = <<CODE0>> (ou <<CODE1>>/ <HTML2>>>>).

- porta de serviço de controle do navegador = base + 2 (apenas loopback)
- <<CODE0>>
- Perfil de navegador Portas CDP auto- alocar de <<CODE1>>

Se você substituir qualquer um destes em config ou env, você deve mantê-los únicos por instância.

# # Notas do navegador/CDP (arma comum)

- Não ** pin <<CODE0>>> para os mesmos valores em várias instâncias.
- Cada instância precisa de sua própria porta de controle do navegador e faixa CDP (derivada de sua porta de gateway).
- Se você precisar de portas CDP explícitas, definir <<CODE1>> por instância.
- Remote Chrome: use <<CODE2>> (por perfil, por instância).

# # Exemplo manual

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/main.json \
OPENCLAW_STATE_DIR=~/.openclaw-main \
openclaw gateway --port 18789

OPENCLAW_CONFIG_PATH=~/.openclaw/rescue.json \
OPENCLAW_STATE_DIR=~/.openclaw-rescue \
openclaw gateway --port 19001
```

# # Verificação rápida

```bash
openclaw --profile main status
openclaw --profile rescue status
openclaw --profile rescue browser status
```
