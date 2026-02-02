---
summary: "CLI reference for `openclaw nodes` (list/status/approve/invoke, camera/canvas/screen)"
read_when:
  - You’re managing paired nodes (cameras, screen, canvas)
  - You need to approve requests or invoke node commands
---

#`openclaw nodes`

Gerencie nós emparelhados (dispositivos) e invoque capacidades de nó.

Relacionados:

- Visão geral dos nós: [nós]/nodes
- Câmara: [nós da câmara] /nodes/camera
- Imagens: [nós de imagem] /nodes/images

Opções comuns:

-`--url`,`--token`,`--timeout`,`--json`

## Comandos comuns

```bash
openclaw nodes list
openclaw nodes list --connected
openclaw nodes list --last-connected 24h
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes status
openclaw nodes status --connected
openclaw nodes status --last-connected 24h
```

`nodes list`imprime mesas pendentes/pareadas. As linhas emparelhadas incluem a idade de ligação mais recente (Última Ligação).
Use`--connected`para mostrar apenas nós conectados atualmente. Usar`--last-connected <duration>`para
filtrar os nós que se ligam dentro de uma duração (por exemplo,`24h`,`7d`.

## Invocar / correr

```bash
openclaw nodes invoke --node <id|name|ip> --command <command> --params <json>
openclaw nodes run --node <id|name|ip> <command...>
openclaw nodes run --raw "git status"
openclaw nodes run --agent main --node <id|name|ip> --raw "git status"
```

Marcas de facturação:

-`--params <json>`: string de objeto JSON (padrão`{}`.
-`--invoke-timeout <ms>`: Node invoy timeout (padrão`15000`.
-`--idempotency-key <key>`: chave opcional de idempotência.

## # Defaults estilo Exec

`nodes run`reflete o comportamento executivo do modelo (padrão + aprovações):

- Lê-se`tools.exec.*`(mais`agents.list[].tools.exec.*`substitui).
- Utiliza aprovações executivas `exec.approval.request` antes de invocar o`system.run`.
-`--node`pode ser omitido quando o`tools.exec.node`é definido.
- Requer um nó que anuncia`system.run`(macOS app ou host de nó sem cabeça).

Bandeiras:

-`--cwd <path>`: directório de trabalho.
-`--env <key=val>`: sobreposição do Env (repetível).
- Tempo limite de comando.
-`--invoke-timeout <ms>`: tempo limite de invocação de nó (padrão`30000`.
-`--needs-screen-recording`: requer permissão de gravação de tela.
-`--raw <command>`: executar uma cadeia de conchas `/bin/sh -lc`ou`cmd.exe /c`.
-`--agent <id>`: aprovações/listas permitidas por agentes (defaults to configurated agent).
-`--env <key=val>`0,`--env <key=val>`1: substituições.
