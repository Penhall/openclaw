---
summary: "Research notes: offline memory system for Clawd workspaces (Markdown source-of-truth + derived index)"
read_when:
  - Designing workspace memory (~/.openclaw/workspace) beyond daily Markdown logs
  - Deciding: standalone CLI vs deep OpenClaw integration
  - Adding offline recall + reflection (retain/recall/reflect)
---

# Memória do espaço de trabalho v2 (offline): notas de pesquisa

Alvo: Espaço de trabalho de estilo Clawd (<<<CODE0>>, padrão <<CODE1>>>) onde “memória” é armazenada como um arquivo Markdown por dia (<<CODE2>>) mais um pequeno conjunto de arquivos estáveis (por exemplo, <<CODE3>>, <<CODE4>>>).

Este documento propõe uma arquitetura de memória **offline-first** que mantém Markdown como fonte canônica, reviewable de verdade, mas acrescenta ** remember ** (pesquisa, resumos de entidade, atualizações de confiança) através de um índice derivado.

# # Por que mudar?

A configuração atual (um arquivo por dia) é excelente para:

- Revista “somente para apêndice”
- edição humana
- durabilidade git-backed + auditoria
- captura de baixa fricção (“apenas anote”)

É fraco para:

- recuperação de alta chamada (“o que decidimos sobre X?”, “última vez que tentamos Y?”)
- respostas centradas na entidade (“me conte sobre Alice / O Castelo / Warelay”) sem reler muitos arquivos
- estabilidade da opinião/preferência (e elementos comprovativos da sua alteração)
- restrições de tempo (“o que era verdade durante 2025?”) e resolução de conflitos

# # Objetivos de design

- **Offline**: funciona sem rede; pode ser executado no laptop/Castle; sem dependência de nuvem.
- **Explicável**: itens recuperados devem ser atribuíveis (arquivo + localização) e separáveis da inferência.
- **Cerimônia baixa**: diário de registro fica Markdown, nenhum trabalho de esquema pesado.
- **Incremental**: v1 é útil apenas com FTS; semântico/vetor e gráficos são atualizações opcionais.
- **Agent-friendly**: torna fácil “recall within token budgets” (retornar pequenos pacotes de fatos).

# # Modelo de estrela norte (Hindsight × Letta)

Duas peças para misturar:

1. ** Loop de controle estilo Letta/MemGPT

- manter um pequeno “núcleo” sempre no contexto (persona + fatos-chave do usuário)
- todo o resto está fora de contexto e recuperado através de ferramentas
- memory writes são chamadas explícitas de ferramentas (append/replace/inserir), persistiu, em seguida, reinjectou o próximo turno

2. ** Substrato de memória estilo Hindsight**

- separar o que é observado vs o que é acreditado vs o que é resumido
- retenção/recuperação/reflexão de apoio
- opiniões confiantes que podem evoluir com provas
- recuperação consciente da entidade + consultas temporais (mesmo sem gráficos completos de conhecimento)

# # Arquitectura proposta (Marcar fonte de verdade + índice derivado)

Loja canónica (amigável)

Manter <<CODE0>> como memória legível por humanos canónicos.

Disposição do espaço de trabalho sugerida:

```
~/.openclaw/workspace/
  memory.md                    # small: durable facts + preferences (core-ish)
  memory/
    YYYY-MM-DD.md              # daily log (append; narrative)
  bank/                        # “typed” memory pages (stable, reviewable)
    world.md                   # objective facts about the world
    experience.md              # what the agent did (first-person)
    opinions.md                # subjective prefs/judgments + confidence + evidence pointers
    entities/
      Peter.md
      The-Castle.md
      warelay.md
      ...
```

Notas:

- ** O diário de bordo permanece diário **. Não precisas de o transformar em JSON.
- Os arquivos <<CODE0>> são **curados**, produzidos por trabalhos de reflexão, e ainda podem ser editados à mão.
- <<CODE1> permanece “pequeno + núcleo-ish”: as coisas que você quer Clawd para ver cada sessão.

Loja de origem

Adicionar um índice derivado sob a área de trabalho (não necessariamente git rastreado):

```
~/.openclaw/workspace/.memory/index.sqlite
```

Volta com:

- esquema SQLite para fatos + links de entidade + metadados de opinião
- SQLite **FTS5** para recall lexical (rápido, minúsculo, offline)
- tabela de incorporação opcional para memória semântica (ainda offline)

O índice é sempre **reconstruível a partir de Markdown**.

# # Manter / Recordar / Refletir (lacete operacional)

## # Manter: normalizar registros diários em “fatos”

A visão chave de Hindsight que importa aqui: armazenar ** fatos narrativos, auto-contidos**, não pequenos trechos.

Regra prática para <<CODE0>>:

- no fim do dia (ou durante), adicionar uma secção <<CODE0>> com 2–5 balas que sejam:
- narrativa (contexto transversal preservado)
- auto-contido (standalone faz sentido mais tarde)
- etiquetados com menções de tipo + entidade

Exemplo:

```
## Retain
- W @Peter: Currently in Marrakech (Nov 27–Dec 1, 2025) for Andy’s birthday.
- B @warelay: I fixed the Baileys WS crash by wrapping connection.update handlers in try/catch (see memory/2025-11-27.md).
- O(c=0.95) @Peter: Prefers concise replies (&lt;1500 chars) on WhatsApp; long content goes into files.
```

Análise mínima:

- Prefixo de tipo: <<CODE0>> (mundo), <<CODE1> (experiência/biográfica), <<CODE2> (opinião), <<CODE3>> (observação/síntese; normalmente gerado)
- Entidades: <<CODE4>>, <<CODE5>>>, etc. (mapa para <<CODE6>>)
- Confiança no parecer: <<CODE7>> opcional

Se você não quer que os autores pensem sobre isso: o trabalho de reflexão pode inferir essas balas do resto do registro, mas ter uma seção explícita <<CODE0>> é a mais fácil “manga de qualidade”.

## # Lembre-se: consultas sobre o índice derivado

Recordar deve apoiar:

- **lexical**: “encontrar termos exatos / nomes / comandos” (FTS5)
- **entidade**: “me conte sobre X” (páginas de entidade + factos ligados)
- ** Temporal**: “o que aconteceu por volta de 27 de novembro” / “desde a semana passada”
- **opinião**: “o que prefere Pedro?” (com confiança + evidência)

O formato de devolução deve ser amigável ao agente e citar fontes:

- <<CODE0> (<<CODE1>>)
- <<CODE2>> (dia da fonte, ou intervalo de tempo extraído se presente)
- <<CODE3> (<<CODE4>>)
- <<CODE5>> (o facto narrativo)
- <<CODE6> (<<CODE7>> etc.)

## # Refletir: produzir páginas estáveis + atualizar crenças

Reflexão é uma tarefa programada (diária ou batimento cardíaco <<CODE0>>) que:

- actualizações <<CODE0>> de factos recentes (sínteses de entidades)
- actualizações <<CODE1>> confiança baseada no reforço/contradição
- opcionalmente propõe edições para <<CODE2>> (fatos duráveis “core-ish”)

Evolução do parecer (simples, explicável):

- cada parecer tem:
- declaração
- confiança <<CODE0>>
- última  atualização
- ligações de provas (apoiando + identidades de facto contraditórias)
- quando chegam novos factos:
- encontrar opiniões candidatas por sobreposição de entidade + similaridade (FTS primeiro, incorporações mais tarde)
- atualizar a confiança por pequenos deltas; grandes saltos requerem forte contradição + evidência repetida

# # Integração CLI: integração autônoma vs profunda

Recomendação: ** integração profunda no OpenClaw**, mas manter uma biblioteca de núcleo separável.

# # # # Por que integrar-se ao Openclaw?

- Openclaw já sabe:
- a localização do espaço de trabalho (<<<CODE0>>)
- o modelo de sessão + batimentos cardíacos
- registro + padrões de solução de problemas
Queres que o próprio agente chame as ferramentas:
- <<CODE1>>
- <<CODE2>>

Porque ainda dividiste uma biblioteca?

- manter a lógica de memória testável sem gateway/runtime
- reutilização de outros contextos (scripts locais, futuro aplicativo desktop, etc.)

Forma:
A ferramenta de memória destina-se a ser uma pequena camada de biblioteca CLI +, mas isso é apenas exploratório.

# # “S-Collide” / SuCo: quando usá-lo (pesquisa)

Se “S-Collide” refere-se a **SuCo (Subspace Collision)**: é uma abordagem de recuperação ANN que visa fortes tradeoffs de recall/latency usando colisões aprendidas/estruturadas em subespaços (papel: arXiv 2411.14754, 2024).

Tomada pragmática para <<CODE0>>:

- ** não comece com o SuCo.
- começar com SQLite FTS + (opcional) simples incorporações; você terá a maioria das vitórias UX imediatamente.
- considerar soluções da classe SuCo/HNSW/ScaNN apenas uma vez:
- corpus é grande (dez/centenas de milhares de pedaços)
- a busca embutida por força bruta torna-se muito lenta
- qualidade de memória é significativamente estrangulada pela busca lexical

Alternativas off-friendly (em complexidade crescente):

- Filtros SQLite FTS5 + metadados (zero ML)
- Embebidos + força bruta (funciona surpreendentemente longe se a contagem de pedaços é baixa)
- Índice HNSW (comum, robusto; precisa de uma ligação à biblioteca)
- SuCo (nível de pesquisa; atraente se houver uma implementação sólida que você pode incorporar)

Pergunta em aberto:

- qual é o melhor modelo de incorporação offline para "memória assistente pessoal" em suas máquinas (laptop + desktop)?
- se já tiver Ollama: embed com um modelo local; caso contrário, envie um pequeno modelo de incorporação na cadeia de ferramentas.

# # Pequeno piloto útil

Se você quiser uma versão mínima e ainda útil:

- Adicionar <<CODE0>> páginas de entidade e uma secção <<CODE1>> nos registos diários.
- Use SQLite FTS para lembrar com citações (caminho + números de linha).
- Adicione incorporações apenas se a qualidade ou escala de memória o exigir.

# # Referências

- Letta / MemGPT conceitos: “core memory blocks” + “archival memory” + auto-edição de ferramentas.
- Hindsight Technical Report: “reter/relembrar/refletir”, memória de quatro redes, extração de fatos narrativos, evolução da confiança da opinião.
- SuCo: arXiv 2411.14754 (2024): “Colisão subespacial” aproximada recuperação do vizinho mais próximo.
