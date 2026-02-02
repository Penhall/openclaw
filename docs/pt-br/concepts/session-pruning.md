---
summary: "Session pruning: tool-result trimming to reduce context bloat"
read_when:
  - You want to reduce LLM context growth from tool outputs
  - You are tuning agents.defaults.contextPruning
---

Poda de Sessão

Cortes de poda de sessão ** resultados antigos da ferramenta** do contexto na memória logo antes de cada chamada LLM. Faz **não** reescrever o histórico de sessão no disco (<<CODE0>>>).

# # Quando corre

- Quando <<CODE0>> estiver activada e a última chamada antrópica para a sessão for superior a <<CODE1>>.
- Só afecta as mensagens enviadas ao modelo para esse pedido.
- Apenas ativo para chamadas de API antrópicas (e modelos Antrópicos OpenRouter).
- Para melhores resultados, coincida <<CODE2>> com o seu modelo <<CODE3>>.
- Depois de uma ameixa, a janela TTL repõe para que as solicitações subsequentes mantenham o cache até <<CODE4>> expira novamente.

# # Predefinição inteligente (Antrópico)

- ** OAuth ou setup-token** perfis: activar <<CODE0>> poda e definir o batimento cardíaco para <<CODE1>>.
- ** Chave API** perfis: habilitar <<CODE2>> poda, definir batimento cardíaco para <<CODE3>>, e padrão <<CODE4>> para <<CODE5>> em modelos Antrópicos.
- Se você definir algum desses valores explicitamente, o OpenClaw não ** os sobrepõe.

# # O que isso melhora (custo + comportamento cache)

- ** Porquê ameixa:** O cache rápido antrópico só se aplica dentro do TTL. Se uma sessão passar o TTL, o próximo pedido re-caches o prompt completo, a menos que você apara-lo primeiro.
- ** O que fica mais barato:** poda reduz o tamanho **cacheWrite** para o primeiro pedido após o TTL expirar.
- **Por que o reset TTL importa:** uma vez que a poda é executada, a janela de cache é reiniciada, para que os pedidos de seguimento possam reutilizar o prompt recém-cacheado em vez de refazer o histórico completo novamente.
- ** O que não faz:** poda não adiciona tokens ou custos “duplos”; só altera o que fica em cache na primeira solicitação pós-TTL.

# # O que pode ser podado

- Apenas <<CODE0>> mensagens.
- As mensagens de usuário + assistente são **nunca** modificadas.
- As últimas mensagens de assistente <<CODE1>> estão protegidas; os resultados da ferramenta após esse corte não são podados.
- Se não houver mensagens de assistente suficientes para estabelecer o ponto de corte, a poda é ignorada.
- Os resultados da ferramenta contendo **blocos de imagem** são ignorados (nunca aparados/limpados).

# # Estimativa da janela de contexto

A poda utiliza uma janela de contexto estimada (cartas × 4). O tamanho da janela é resolvido nesta ordem:

1. Definição do modelo <<CODE0>> (do registro do modelo).
2. <<CODE1>> sobreposição.
3. <<CODE2>>.
4. Predefinição <<CODE3>> tokens.

# # Modo

## #cache-ttl

- A poda só é executada se a última chamada antrópica for mais antiga do que <<CODE0>> (padrão <<CODE1>>).
- Quando corre: o mesmo comportamento suave + claro como antes.

# # Macio vs poda dura

- **Soft-trim**: apenas para resultados de ferramentas de tamanho excessivo.
- Mantém a cabeça + cauda, insere <<CODE0>>, e adiciona uma nota com o tamanho original.
- Salta resultados com blocos de imagens.
- **Hard-clear**: substitui todo o resultado da ferramenta por <<CODE1>>.

# # Seleção de ferramentas

- <<CODE0>>/ <<CODE1>suporte <<CODE2>>
- Negar ganha.
- A correspondência é insensível.
- Lista de permissões vazia => todas as ferramentas permitidas.

# # Interacção com outros limites

- Ferramentas incorporadas já truncam sua própria saída; a poda de sessão é uma camada extra que impede que chats de longo prazo acumulem muito resultado de ferramenta no contexto do modelo.
- A compactação é separada: a compactação resume e persiste, a poda é transitória por solicitação. Ver [/conceitos/compactação](<<<LINK0>>>).

# # Por omissão (quando activado)

- <<CODE0>>: <<CODE1>>>
- <<CODE2>>: <<CODE3>>
- <<CODE4>>: <<CODE5>>
- <<CODE6>>: <<CODE7>>
- <<CODE8>>: <<CODE9>>>
- <<CODE10>>: <<CODE11>>
- <<CODE12>>: <<CODE13>>

# # Exemplos

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

Ver referência de configuração: [Configuração de Gateway](<<<LINK0>>)
