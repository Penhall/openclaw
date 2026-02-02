---
summary: "Write agent tools in a plugin (schemas, optional tools, allowlists)"
read_when:
  - You want to add a new agent tool in a plugin
  - You need to make a tool opt-in via allowlists
---

# Ferramentas de agente de plug-in

Plugins OpenClaw podem registrar ** ferramentas de agente** (funções JSON-schema) que são expostas
para o LLM durante as corridas de agentes. As ferramentas podem ser **necessárias** (sempre disponíveis) ou
** Opcional** (opt-in).

As ferramentas do agente são configuradas em `tools` na configuração principal, ou per-agent em
`agents.list[].tools`. A política de allowlist/denylist controla que ferramentas o agente
Posso ligar.

## Ferramenta básica

```ts
import { Type } from "@sinclair/typebox";

export default function (api) {
  api.registerTool({
    name: "my_tool",
    description: "Do a thing",
    parameters: Type.Object({
      input: Type.String(),
    }),
    async execute(_id, params) {
      return { content: [{ type: "text", text: params.input }] };
    },
  });
}
```

# # Ferramenta opcional (opt-in)

As ferramentas opcionais são **nunca** automáticas. Usuários devem adicioná-los a um agente
allowlist.

```ts
export default function (api) {
  api.registerTool(
    {
      name: "workflow_tool",
      description: "Run a local workflow",
      parameters: {
        type: "object",
        properties: {
          pipeline: { type: "string" },
        },
        required: ["pipeline"],
      },
      async execute(_id, params) {
        return { content: [{ type: "text", text: params.pipeline }] };
      },
    },
    { optional: true },
  );
}
```

Habilitar ferramentas opcionais em `agents.list[].tools.allow` (ou global `tools.allow`):

```json5
{
  agents: {
    list: [
      {
        id: "main",
        tools: {
          allow: [
            "workflow_tool", // specific tool name
            "workflow", // plugin id (enables all tools from that plugin)
            "group:plugins", // all plugin tools
          ],
        },
      },
    ],
  },
}
```

Outros botões de configuração que afetam a disponibilidade da ferramenta:

- Allowlists que apenas as ferramentas de nome plugin são tratados como plugin opt-ins; ferramentas principais permanecem
habilitado a menos que você também inclua ferramentas ou grupos principais na lista de permissões.
- <<CODE0> / `agents.list[].tools.profile` (lista de licenças de base)
- <<CODE2> / `agents.list[].tools.byProvider` (providencial-específico permitido/negativo)
- `tools.sandbox.tools.*` (policy da ferramenta da caixa de areia quando sandboxed)

# # Regras + dicas

- Nomes de ferramentas devem **not** colidir com nomes de ferramentas principais; ferramentas conflitantes são ignoradas.
- IDs de plug-in usados em allowlists não devem colidir com nomes de ferramentas principais.
- Preferir <<CODE0> para ferramentas que desencadeiam efeitos secundários ou requerem
binários/credenciais.
