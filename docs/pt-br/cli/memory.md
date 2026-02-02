---
summary: "CLI reference for `openclaw memory` (status/index/search)"
read_when:
  - You want to index or search semantic memory
  - You’re debugging memory availability or indexing
---

#`openclaw memory`

Gerencie indexação e pesquisa de memória semântica.
Fornecido pelo plugin de memória ativa (padrão:`memory-core`; defina`plugins.slots.memory = "none"`para desabilitar).

Relacionados:

- Conceito de memória: [Memória] /concepts/memory
- Plugins: [Plugins] /plugins

## Exemplos

```bash
openclaw memory status
openclaw memory status --deep
openclaw memory status --deep --index
openclaw memory status --deep --index --verbose
openclaw memory index
openclaw memory index --verbose
openclaw memory search "release checklist"
openclaw memory status --agent main
openclaw memory index --agent main --verbose
```

## Opções

Frequentes:

-`--agent <id>`: escopo para um único agente (padrão: todos os agentes configurados).
-`--verbose`: emite registos detalhados durante sondas e indexação.

Notas:

- Vetor de sondas`memory status --deep`+ disponibilidade incorporada.
-`memory status --deep --index`executa um reindex se a loja estiver suja.
-`memory index --verbose`imprime detalhes por fase (fornecedor, modelo, fontes, atividade em lote).
-`memory status`inclui quaisquer caminhos adicionais configurados via`memorySearch.extraPaths`.
