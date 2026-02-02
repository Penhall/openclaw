---
summary: "Context window + compaction: how OpenClaw keeps sessions under model limits"
read_when:
  - You want to understand auto-compaction and /compact
  - You are debugging long sessions hitting context limits
---

# Janela de contexto e compactação

Cada modelo tem uma ** janela de contexto** (máx. tokens que pode ver). Chats de longa duração acumulam mensagens e resultados de ferramentas; uma vez que a janela é apertada, OpenClaw **compacts** o histórico mais antigo para ficar dentro dos limites.

## O que é compactação

Compactação ** resume conversas antigas** em uma entrada compacta e mantém as mensagens recentes intactas. O resumo é armazenado no histórico de sessão, então futuras solicitações usam:

- Resumo da compactação
- Mensagens recentes após o ponto de compactação

Compactação **persistas** na história da sessão JSONL.

Configuração

Veja [Configuração e modos de computação]/concepts/compaction para as configurações`agents.defaults.compaction`.

## Auto-compactação (por omissão)

Quando uma sessão se aproxima ou excede a janela de contexto do modelo, o OpenClaw aciona a autocompactação e pode tentar novamente a solicitação original usando o contexto compactado.

Você verá:

-`🧹 Auto-compaction complete`em modo verbose
-`/status`que apresenta o`🧹 Compactions: <count>`

Antes da compactação, o OpenClaw pode executar um **silent memory flush** turn to store
notas duráveis ao disco. Veja [Memory]/concepts/memory para detalhes e configuração.

## Compactação manual

Utilizar`/compact`(opcionalmente com instruções) para forçar uma passagem de compactação:

```
/compact Focus on decisions and open questions
```

## Fonte da janela de contexto

A janela de contexto é específica do modelo. O OpenClaw usa a definição do modelo do catálogo de provedores configurados para determinar limites.

## Compactação vs poda

- **Compaction**: resumos e **persists** em JSONL.
- ** Session pounding**: apara resultados antigos ** tool** apenas, ** in-memory**, por pedido.

Ver [/conceitos/sessão-pruning] /concepts/session-pruning para detalhes de poda.

Dicas

- Use`/compact`quando as sessões se sentirem estagnadas ou o contexto estiver inchado.
- Grandes saídas de ferramentas já estão truncadas; poda pode reduzir ainda mais o acúmulo de resultados de ferramentas.
- Se você precisar de uma nova ardósia,`/new`ou`/reset`inicia um novo ID de sessão.
