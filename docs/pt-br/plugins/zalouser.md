---
summary: "Zalo Personal plugin: QR login + messaging via zca-cli (plugin install + channel config + CLI + tool)"
read_when:
  - You want Zalo Personal (unofficial) support in OpenClaw
  - You are configuring or developing the zalouser plugin
---

# Zalo Personal (plugin)

Zalo Suporte pessoal para OpenClaw através de um plugin, usando `zca-cli` para automatizar uma conta normal do usuário Zalo.

> **Aviso: ** Automatização não oficial pode levar à suspensão da conta / proibição. Use por sua própria conta e risco.

# # Nomeação

O ID do canal é <<CODE0> para torná-lo explícito, isto automatiza uma conta de usuário **pessoal do Zalo** (não oficial). Mantemos <<CODE1> reservado para uma futura integração oficial da API Zalo.

# # Onde corre

Este plugin é executado ** dentro do processo Gateway**.

Se você usar um Gateway remoto, instale/configure-o na **máquina que executa o Gateway**, então reinicie o Gateway.

Instalar

Opção A: instalar a partir do npm

```bash
openclaw plugins install @openclaw/zalouser
```

Reinicie o portal depois.

# # # Opção B: instalar a partir de uma pasta local (dev)

```bash
openclaw plugins install ./extensions/zalouser
cd ./extensions/zalouser && pnpm install
```

Reinicie o portal depois.

# # Pré-requisito: zca-cli

A máquina Gateway deve ter `zca` em <<CODE1>:

```bash
zca --version
```

Configuração

A configuração do canal vive em `channels.zalouser` (não `plugins.entries.*`):

```json5
{
  channels: {
    zalouser: {
      enabled: true,
      dmPolicy: "pairing",
    },
  },
}
```

# # CLI

```bash
openclaw channels login --channel zalouser
openclaw channels logout --channel zalouser
openclaw channels status --probe
openclaw message send --channel zalouser --target <threadId> --message "Hello from OpenClaw"
openclaw directory peers list --channel zalouser --query "name"
```

# # Ferramenta de agente

Nome da ferramenta: `zalouser`

Ações: <<CODE0>, <<CODE1>, `link`, `friends`, <<CODE4>, `me`, <<CODE6>
