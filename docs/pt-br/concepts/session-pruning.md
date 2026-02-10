---
summary: "Session pruning: tool-result trimming to reduce context bloat"
read_when:
  - You want to reduce LLM context growth from tool outputs
  - You are tuning agents.defaults.contextPruning
---

Poda de Sessão

Cortes de poda de sessão ** resultados antigos da ferramenta** do contexto na memória logo antes de cada chamada LLM. Ele faz **not** reescrever o histórico de sessão no disco `*.jsonl`.

## Quando corre

- Quando o`mode: "cache-ttl"`está habilitado e o último convite Antrópico para a sessão é mais antigo que o`ttl`.
- Só afecta as mensagens enviadas ao modelo para esse pedido.
- Apenas ativo para chamadas de API antrópicas (e modelos Antrópicos OpenRouter).
- Para melhores resultados, coincida`ttl`com o seu modelo`cacheControlTtl`.
- Depois de uma ameixa, a janela TTL reinicia assim que as solicitações subsequentes manter cache até`ttl`expira novamente.

## Predefinição inteligente (Antrópico)

- **OAuth ou setup-token** perfis: habilitar a poda`cache-ttl`e definir o batimento cardíaco para`1h`.
- ** Chave API** perfis: habilitar poda`cache-ttl`, definir batimento cardíaco para`30m`, e padrão`cacheControlTtl`para`1h`em modelos antrópicos.
- Se você definir algum desses valores explicitamente, o OpenClaw não ** os sobrepõe.

## O que isso melhora (custo + comportamento cache)

- ** Porquê ameixa:** O cache rápido antrópico só se aplica dentro do TTL. Se uma sessão passar o TTL, o próximo pedido re-caches o prompt completo, a menos que você apara-lo primeiro.
- ** O que fica mais barato:** poda reduz o tamanho **cacheWrite** para o primeiro pedido após o TTL expirar.
- **Por que o reset TTL importa:** uma vez que a poda é executada, a janela de cache é reiniciada, para que os pedidos de seguimento possam reutilizar o prompt recém-cacheado em vez de refazer o histórico completo novamente.
- ** O que não faz:** poda não adiciona tokens ou custos “duplos”; só altera o que fica em cache na primeira solicitação pós-TTL.

## O que pode ser podado

- Apenas mensagens`toolResult`.
- As mensagens de usuário + assistente são **nunca** modificadas.
- As últimas mensagens de assistente`keepLastAssistants`estão protegidas; os resultados da ferramenta após esse corte não são podados.
- Se não houver mensagens de assistente suficientes para estabelecer o ponto de corte, a poda é ignorada.
- Os resultados da ferramenta contendo **blocos de imagem** são ignorados (nunca aparados/limpados).

## Estimativa da janela de contexto

A poda utiliza uma janela de contexto estimada (cartas × 4). O tamanho da janela é resolvido nesta ordem:

1. Definição do modelo`contextWindow`(do registro do modelo).
2.`models.providers.*.models[].contextWindow`sobrescrever.
3.`agents.defaults.contextTokens`.
4. Tokens padrão`200000`.

## Modo

## #cache-ttl

- A poda só é executada se a última chamada antrópica for mais antiga do que`ttl`(padrão`5m`.
- Quando corre: o mesmo comportamento suave + claro como antes.

## Macio vs poda dura

- **Soft-trim**: apenas para resultados de ferramentas de tamanho excessivo.
- Mantém cabeça + cauda, insere`...`, e adiciona uma nota com o tamanho original.
- Salta resultados com blocos de imagens.
- **Hard-clear**: substitui todo o resultado da ferramenta por`hardClear.placeholder`.

## Seleção de ferramentas

-`tools.allow`/`tools.deny`apoiar`*`- Negar ganha.
- A correspondência é insensível.
- Lista de permissões vazia => todas as ferramentas permitidas.

## Interacção com outros limites

- Ferramentas incorporadas já truncam sua própria saída; a poda de sessão é uma camada extra que impede que chats de longo prazo acumulem muito resultado de ferramenta no contexto do modelo.
- A compactação é separada: a compactação resume e persiste, a poda é transitória por solicitação. Ver [/conceitos/compactação] /concepts/compaction.

## Por omissão (quando activado)

-`ttl`:`"5m"`-`keepLastAssistants`:`3`-`softTrimRatio`:`0.3`-`hardClearRatio`:`0.5`-`minPrunableToolChars`:`50000`-`"5m"`0:`"5m"`1
-`"5m"`2:`"5m"`3

## Exemplos

Padrão (desligado):

```json5
{
  agent: {
    contextPruning: { mode: "off" },
  },
}
```

Activar a poda consciente de TTL:

```json5
{
  agent: {
    contextPruning: { mode: "cache-ttl", ttl: "5m" },
  },
}
```

Restrinja a poda a ferramentas específicas:

```json5
{
  agent: {
    contextPruning: {
      mode: "cache-ttl",
      tools: { allow: ["exec", "read"], deny: ["*image*"] },
    },
  },
}
```

Veja a referência de configuração: [Configuração de Gateway]/gateway/configuration
