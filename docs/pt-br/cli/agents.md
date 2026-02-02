---
summary: "CLI reference for `openclaw agents` (list/add/delete/set identity)"
read_when:
  - You want multiple isolated agents (workspaces + routing + auth)
---

#`openclaw agents`

Gerenciar agentes isolados (espaços de trabalho + autenticação + roteamento).

Relacionados:

- Roteamento multiagentes: [Roteamento Multiagente] /concepts/multi-agent
- Área de trabalho do agente: [Espaço de trabalho do agente] /concepts/agent-workspace

## Exemplos

```bash
openclaw agents list
openclaw agents add work --workspace ~/.openclaw/workspace-work
openclaw agents set-identity --workspace ~/.openclaw/workspace --from-identity
openclaw agents set-identity --agent main --avatar avatars/openclaw.png
openclaw agents delete work
```

## Arquivos de identidade

Cada espaço de trabalho do agente pode incluir um`IDENTITY.md`na raiz do espaço de trabalho:

- Caminho do exemplo:`~/.openclaw/workspace/IDENTITY.md`-`set-identity --from-identity`lê-se da raiz do espaço de trabalho (ou de um`--identity-file`explícito)

Os caminhos do Avatar resolvem-se em relação à raiz do espaço de trabalho.

## Definir identidade

`set-identity`escreve campos em`agents.list[].identity`:

-`name`-`theme`-`emoji`-`avatar`(caminho relativo ao espaço de trabalho, URL( s) http( s) ou URI de dados)

Carga de`IDENTITY.md`:

```bash
openclaw agents set-identity --workspace ~/.openclaw/workspace --from-identity
```

Substituir explicitamente os campos:

```bash
openclaw agents set-identity --agent main --name "OpenClaw" --emoji "🦞" --avatar avatars/openclaw.png
```

Amostra de configuração:

```json5
{
  agents: {
    list: [
      {
        id: "main",
        identity: {
          name: "OpenClaw",
          theme: "space lobster",
          emoji: "🦞",
          avatar: "avatars/openclaw.png",
        },
      },
    ],
  },
}
```
