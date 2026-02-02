---
summary: "Skills config schema and examples"
read_when:
  - Adding or modifying skills config
  - Adjusting bundled allowlist or install behavior
---

Configuração de Habilidades

Todas as configurações relacionadas às habilidades vivem em `skills` em <CODE1>>.

```json5
{
  skills: {
    allowBundled: ["gemini", "peekaboo"],
    load: {
      extraDirs: ["~/Projects/agent-scripts/skills", "~/Projects/oss/some-skill-pack/skills"],
      watch: true,
      watchDebounceMs: 250,
    },
    install: {
      preferBrew: true,
      nodeManager: "npm", // npm | pnpm | yarn | bun (Gateway runtime still Node; bun not recommended)
    },
    entries: {
      "nano-banana-pro": {
        enabled: true,
        apiKey: "GEMINI_KEY_HERE",
        env: {
          GEMINI_API_KEY: "GEMINI_KEY_HERE",
        },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

# # Campos

- <<CODE0>: lista facultativa de autorizações para **compilação** apenas de competências. Quando definido, apenas
as competências agrupadas na lista são elegíveis (competências geridas/espaço de trabalho não afectadas).
- <<CODE1>: diretórios de habilidade adicionais para escanear (mais baixa precedência).
- <<CODE2>: ver pastas de habilidades e atualizar o instantâneo de habilidades (padrão: true).
- `load.watchDebounceMs`: desapontamento para eventos de observação de habilidades em milissegundos (padrão: 250).
- <<CODE4>: preferir instaladores de cerveja quando disponíveis (padrão: true).
- `install.nodeManager`: preferência do instalador do nó (`npm`  . . `pnpm` . . `yarn` . . `bun`, por omissão: npm).
Isso só afeta **skill installs**; o tempo de execução do Gateway ainda deve ser Node
(Bun não recomendado para WhatsApp/Telegram).
- `entries.<skillKey>`: substituições por habilidade.

Domínios por qualificação:

- `enabled`: definir <<CODE1> para desativar uma habilidade, mesmo que seja empacotada/instalada.
- <<CODE2>: variáveis de ambiente injectadas para a execução do agente (apenas se não estiverem já definidas).
- <<CODE3>: conveniência opcional para as competências que declaram um env var primário.

# # Notas

- Chaves no mapa `entries` para o nome da habilidade por padrão. Se uma habilidade define
<<CODE1>, use essa chave.
- Mudanças nas habilidades são captadas na próxima volta do agente quando o observador estiver habilitado.

# # Habilidades de caixa de areia + env vars

Quando uma sessão é **sandboxed**, processos de habilidade são executados dentro do Docker. A caixa de areia
não ** herdar o hospedeiro `process.env`.

Utilizar um de:

- <<CODE0> (ou por agente `agents.list[].sandbox.docker.env`)
- assar o env em sua imagem personalizada sandbox

Global `env` e <<CODE1> aplicam-se apenas a **host** roda.
