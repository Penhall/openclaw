---
summary: "How OpenClaw memory works (workspace files + automatic memory flush)"
read_when:
  - You want the memory file layout and workflow
  - You want to tune the automatic pre-compaction memory flush
---

Memória

A memória OpenClaw é **plain Markdown no espaço de trabalho do agente**. Os arquivos são o
fonte da verdade; o modelo só "lembra" o que é escrito no disco.

As ferramentas de busca de memória são fornecidas pelo plugin de memória ativa (padrão:`memory-core`. Desactivar plugins de memória com`plugins.slots.memory = "none"`.

## Arquivos de memória (Markdown)

A disposição padrão do espaço de trabalho usa duas camadas de memória:

-`memory/YYYY-MM-DD.md`- Diário de bordo.
- Leia hoje + ontem no início da sessão.
-`MEMORY.md`(facultativo)
- Memória de longo prazo.
- ** Só carregar na sessão principal, privada** (nunca em contextos de grupo).

Estes arquivos vivem sob a área de trabalho `agents.defaults.workspace`, padrão`~/.openclaw/workspace`. Ver [Espaço de trabalho do agente]/concepts/agent-workspace para o layout completo.

## Quando escrever a memória

- As decisões, preferências e factos duradouros vão para`MEMORY.md`.
- Notas do dia-a-dia e contexto de execução ir para`memory/YYYY-MM-DD.md`.
- Se alguém disser "lembre-se disto", escreva-o (não o guarde em RAM).
- Esta área continua a evoluir. Ajuda a lembrar o modelo para armazenar memórias; saberá o que fazer.
- Se queres algo para colar, pede ao robot para o escrever na memória.

## Automatic memória flush (pré-compaction ping)

Quando uma sessão é ** perto de auto-compaction**, OpenClaw desencadeia um **silent,
agentic turn** que lembra o modelo de escrever memória durável **antes
contexto é compactado. Os prompts padrão dizem explicitamente que o modelo  pode responder ,
mas geralmente`NO_REPLY`é a resposta correta para que o usuário nunca veja esta volta.

Isto é controlado pelo`agents.defaults.compaction.memoryFlush`:

```json5
{
  agents: {
    defaults: {
      compaction: {
        reserveTokensFloor: 20000,
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 4000,
          systemPrompt: "Session nearing compaction. Store durable memories now.",
          prompt: "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store.",
        },
      },
    },
  },
}
```

Detalhes:

- ** Limiar suave**: gatilhos de descarga quando a estimativa do token de sessão se cruza`contextWindow - reserveTokensFloor - softThresholdTokens`.
- **Silêncio** por padrão: prompts incluem`NO_REPLY`para que nada seja entregue.
- **Dois prompts**: um prompt do usuário mais um prompt do sistema anexem o lembrete.
- ** Um flush por ciclo de compactação** (tracked in`sessions.json`.
- ** O espaço de trabalho deve ser escrito**: se a sessão correr sandboxed com`workspaceAccess: "ro"`ou`"none"`, o flush é ignorado.

Para o ciclo de vida completo de compactação, ver
[Gestão de sessão + compactação] /reference/session-management-compaction.

## Pesquisa de memória vetorial

OpenClaw pode construir um pequeno índice vetorial sobre`MEMORY.md`e`memory/*.md`(mais
quaisquer diretórios extras ou arquivos que você optar) para que consultas semânticas possam encontrar relacionados
notas mesmo quando o texto difere.

Predefinição:

- Activado por omissão.
- Observa arquivos de memória para alterações (debunçado).
- Usa incorporações remotas por padrão. Se o`memorySearch.provider`não estiver definido, o OpenClaw seleciona automaticamente:
1.`local`se um`memorySearch.local.modelPath`estiver configurado e o arquivo existir.
2.`openai`se uma chave OpenAI puder ser resolvida.
3.`gemini`se uma chave Gemini pode ser resolvida.
4. Caso contrário, a pesquisa de memória permanece desactivada até ser configurada.
- O modo local utiliza o nó- llama-cpp e pode requerer`pnpm approve-builds`.
- Usa sqlite-vec (quando disponível) para acelerar a busca vetorial dentro do SQLite.

Embutições remotas **requer** uma chave API para o provedor incorporador. Openclaw
resolve chaves de perfis de autenticação,`models.providers.*.apiKey`ou ambiente
variáveis. O Codex OAuth só cobre chat/compleções e não satisfaz **
incorporações para pesquisa de memória. Para Gemini, utilizar`GEMINI_API_KEY`ou`models.providers.google.apiKey`. Ao utilizar um endpoint compatível com OpenAI personalizado,`memorySearch.remote.apiKey`(e opcional`memorySearch.remote.headers`.

Caminhos de memória adicionais

Se você deseja indexar arquivos Markdown fora da disposição padrão do espaço de trabalho, adicione
caminhos explícitos:

```json5
agents: {
  defaults: {
    memorySearch: {
      extraPaths: ["../team-docs", "/srv/shared-notes/overview.md"]
    }
  }
}
```

Notas:

- Os caminhos podem ser absolutos ou relacionados com o espaço de trabalho.
- Os diretórios são digitalizados recursivamente para arquivos`.md`.
- Só os ficheiros Markdown estão indexados.
- Symlinks são ignorados (arquivos ou diretórios).

### Gemini incorporações (nativo)

Defina o provedor para`gemini`para usar diretamente a API de incorporação Gemini:

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "gemini",
      model: "gemini-embedding-001",
      remote: {
        apiKey: "YOUR_GEMINI_API_KEY"
      }
    }
  }
}
```

Notas:

-`remote.baseUrl`é opcional (defaults to the Gemini API base URL).
-`remote.headers`permite adicionar cabeçalhos extras se necessário.
- Modelo padrão:`gemini-embedding-001`.

Se quiser utilizar um endpoint **compatível com OpenAI ** (OpenRouter, vLLM, ou um proxy),
você pode usar a configuração`remote`com o provedor OpenAI:

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "openai",
      model: "text-embedding-3-small",
      remote: {
        baseUrl: "https://api.example.com/v1/",
        apiKey: "YOUR_OPENAI_COMPAT_API_KEY",
        headers: { "X-Custom-Header": "value" }
      }
    }
  }
}
```

Se você não quiser definir uma chave API, use`memorySearch.provider = "local"`ou set`memorySearch.fallback = "none"`.

Regressos:

-`memorySearch.fallback`pode ser`openai`,`gemini`,`local`ou`none`.
- O provedor de retrocesso só é usado quando o provedor principal de incorporação falha.

Indexação em lote (OpenAI + Gemini):

- Habilitado por padrão para incorporação OpenAI e Gemini. Defina`agents.defaults.memorySearch.remote.batch.enabled = false`para desabilitar.
- O comportamento padrão espera pela conclusão do lote; ajuste`remote.batch.wait`,`remote.batch.pollIntervalMs`e`remote.batch.timeoutMinutes`se necessário.
- Defina`remote.batch.concurrency`para controlar quantos trabalhos em lote enviamos em paralelo (padrão: 2).
- O modo Lote se aplica quando`memorySearch.provider = "openai"`ou`"gemini"`e usa a chave API correspondente.
- Trabalhos em lote Gemini usam o endpoint de lote assync embeddings e requerem disponibilidade da API Gemini Batch.

Por que OpenAI lote é rápido + barato:

- Para grandes backfills, o OpenAI é normalmente a opção mais rápida que apoiamos porque podemos enviar muitos pedidos de incorporação em um único trabalho em lote e deixar o OpenAI processá-los assincronicamente.
- OpenAI oferece preços com desconto para cargas de trabalho da API Batch, então grandes corridas de indexação são geralmente mais baratas do que enviar os mesmos pedidos de forma sincronizada.
- Consulte os documentos da OpenAI Batch API e preços para detalhes:
- https://platform.openai.com/docs/api-reference/batch
- https://platform.openai.com/pricing

Exemplo de configuração:

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "openai",
      model: "text-embedding-3-small",
      fallback: "openai",
      remote: {
        batch: { enabled: true, concurrency: 2 }
      },
      sync: { watch: true }
    }
  }
}
```

Ferramentas:

-`memory_search`— retorna trechos com intervalos de arquivo + linha.
-`memory_get`— ler o conteúdo do arquivo de memória por caminho.

Modo local:

- Preparar`agents.defaults.memorySearch.provider = "local"`.
- Fornecer`agents.defaults.memorySearch.local.modelPath`(GGUF ou`hf:`URI).
- Opcional: definir`agents.defaults.memorySearch.fallback = "none"`para evitar retrocesso remoto.

Como funcionam as ferramentas de memória

-`memory_search`pesquisa semanticamente blocos Markdown (~400 token target, sobreposição de 80 token) de`MEMORY.md`+`memory/**/*.md`. Ele retorna texto de trecho (capped ~700 chars), caminho do arquivo, faixa de linha, pontuação, provedor/modelo, e se nós caímos de incorporados locais → remotos. Nenhuma carga completa do arquivo é devolvida.
-`memory_get`lê um arquivo Markdown de memória específica (relativo ao espaço de trabalho), opcionalmente a partir de uma linha de partida e para linhas N. Caminhos fora do`MEMORY.md`/`memory/`só são permitidos quando explicitamente enumerados no`memorySearch.extraPaths`.
- Ambas as ferramentas são habilitadas somente quando o`memorySearch.enabled`resolve true para o agente.

## O que é indexado (e quando)

- Tipo de ficheiro: apenas marcação `MEMORY.md`,`memory/**/*.md`, além de quaisquer ficheiros`.md`sob`memorySearch.extraPaths`.
- Armazenamento de índice: por agente SQLite em`~/.openclaw/memory/<agentId>.sqlite`(configurado via`agents.defaults.memorySearch.store.path`, suporta token`{agentId}`.
- Frescura: o observador em`MEMORY.md`,`memory/`e`memorySearch.extraPaths`marca o índice sujo (debounce 1.5s). A sincronização é agendada no início da sessão, na pesquisa ou em um intervalo e é executada assíncrona. As transcrições das sessões usam limiares delta para activar a sincronização de fundo.
- Reindex gatilhos: o índice armazena a incorporação **provider/model + impressão digital endpoint + params de blocos**. Se alguma dessas alterações, o OpenClaw reinicia automaticamente e reindexa toda a loja.

### Pesquisa híbrida (BM25 + vetor)

Quando habilitado, OpenClaw combina:

- ** Semelhança vetorial** (match semântico, frase pode diferir)
- **Relevância da palavra-chave BM25** (toques exactos como IDs, env vars, símbolos de código)

Se a pesquisa de texto completo não estiver disponível em sua plataforma, o OpenClaw retornará à busca somente por vetores.

Porquê híbrido?

Vector busca é grande em “isso significa a mesma coisa”:

- "Mac Studio gateway host" vs "a máquina que executa o gateway"
- “desbanhar atualizações de arquivos” vs “evitar indexação em cada gravação”

Mas pode ser fraco em fichas de alto sinal.

- BI `a828e60`,`b3b9895a…`
- símbolos de código `memorySearch.query.hybrid`
- strings de erro (“sqlite-vec indisponível”)

BM25 (texto completo) é o oposto: forte em fichas exatas, mais fraco em paráfrases.
Pesquisa híbrida é o meio-termo pragmático: **use ambos os sinais de recuperação** para que você obtenha
bons resultados para as consultas “linguagem natural” e “agulha em um palheiro”.

#### Como mesclamos os resultados (o design atual)

Esboço de implementação:

1. Recuperar um pool candidato de ambos os lados:

- **Vector**: topo`maxResults * candidateMultiplier`por semelhança cossena.
- **BM25**: topo`maxResults * candidateMultiplier`por FTS5 BM25 (inferior é melhor).

2. Converta a classificação BM25 em uma pontuação de 0.1-ish:

-`textScore = 1 / (1 + max(0, bm25Rank))`

3. Candidatos da União por block id e calcular uma pontuação ponderada:

-`finalScore = vectorWeight * vectorScore + textWeight * textScore`

Notas:

-`vectorWeight`+`textWeight`é normalizado para 1.0 em resolução de configuração, então os pesos se comportam como percentuais.
- Se as incorporações não estiverem disponíveis (ou o provedor devolver um vetor zero), ainda rodamos BM25 e retornamos correspondências de palavras-chave.
- Se FTS5 não pode ser criado, nós mantemos apenas a pesquisa vetorial (sem falha difícil).

Isto não é “IR-teoria perfeita”, mas é simples, rápido, e tende a melhorar a memória/precisão em notas reais.
Se queremos ficar mais fancier mais tarde, os próximos passos comuns são Reciprocal Rank Fusion (RRF) ou normalização de pontuação
(min/max ou escore z) antes da mistura.

Configuração:

```json5
agents: {
  defaults: {
    memorySearch: {
      query: {
        hybrid: {
          enabled: true,
          vectorWeight: 0.7,
          textWeight: 0.3,
          candidateMultiplier: 4
        }
      }
    }
  }
}
```

Embutindo cache

OpenClaw pode cache **chunk embeddings** no SQLite para reindexar e atualizações frequentes (especialmente transcrições de sessão) não reembed texto inalterado.

Configuração:

```json5
agents: {
  defaults: {
    memorySearch: {
      cache: {
        enabled: true,
        maxEntries: 50000
      }
    }
  }
}
```

## # Pesquisa de memória de sessão (experimental)

Você pode, opcionalmente, indexar ** transcripts de sessão** e superfirá-los via`memory_search`.
Isto está fechado atrás de uma bandeira experimental.

```json5
agents: {
  defaults: {
    memorySearch: {
      experimental: { sessionMemory: true },
      sources: ["memory", "sessions"]
    }
  }
}
```

Notas:

- A indexação da sessão é ** opt-in** (off por padrão).
- As actualizações da sessão são desbotadas e ** indexadas assíncrona** uma vez que cruzam os limiares delta (melhor esforço).
-`memory_search`nunca bloqueia a indexação; os resultados podem ser ligeiramente obsoletos até que a sincronização de fundo termine.
- Os resultados ainda incluem apenas trechos;`memory_get`permanece limitado a arquivos de memória.
- A indexação da sessão é isolada por agente (apenas os registros de sessão do agente são indexados).
- Registros de sessão ao vivo no disco `~/.openclaw/agents/<agentId>/sessions/*.jsonl`. Qualquer processo/usuário com acesso ao sistema de arquivos pode lê-los, então trate o acesso ao disco como o limite de confiança. Para um isolamento mais rigoroso, execute agentes sob usuários ou hosts separados do sistema operacional.

Limiares delta (padrão mostrado):

```json5
agents: {
  defaults: {
    memorySearch: {
      sync: {
        sessions: {
          deltaBytes: 100000,   // ~100 KB
          deltaMessages: 50     // JSONL lines
        }
      }
    }
  }
}
```

### Aceleração vetorial SQLite (sqlite-vec)

Quando a extensão sqlite-vec está disponível, as lojas OpenClaw
Tabela virtual SQLite `vec0` e executa consultas de distância vetorial na
base de dados. Isto mantém a pesquisa rapidamente sem carregar cada incorporação no JS.

Configuração (opcional):

```json5
agents: {
  defaults: {
    memorySearch: {
      store: {
        vector: {
          enabled: true,
          extensionPath: "/path/to/sqlite-vec"
        }
      }
    }
  }
}
```

Notas:

-`enabled`defaults to true; quando desactivado, a pesquisa volta para o processo
similaridade cossena sobre incorporações armazenadas.
- Se a extensão sqlite-vec estiver ausente ou não for carregada, o OpenClaw registra o
erro e continua com o retorno do JS (sem tabela vetorial).
-`extensionPath`substitui o caminho sqlite-vec empacotado (útil para construções personalizadas
ou locais de instalação não normalizados).

## # Local incorporando auto-download

- Modelo de incorporação local padrão:`hf:ggml-org/embeddinggemma-300M-GGUF/embeddinggemma-300M-Q8_0.gguf`(~0.6 GB).
- Quando o`memorySearch.provider = "local"`, o`node-llama-cpp`resolve o`modelPath`; se o GGUF não o encontrar **auto-downloads** para o cache (ou o`local.modelCacheDir`se estiver definido), então o carrega. Os downloads são retomados ao tentar novamente.
- Exigência de construção nativa: execute`pnpm approve-builds`, escolha`node-llama-cpp`, em seguida,`pnpm rebuild node-llama-cpp`.
- Fallback: se a configuração local falhar e`memorySearch.fallback = "openai"`, mudamos automaticamente para incorporações remotas `openai/text-embedding-3-small`a menos que sobreponha) e gravamos a razão.

## # Exemplo de terminal compatível com OpenAI personalizado

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "openai",
      model: "text-embedding-3-small",
      remote: {
        baseUrl: "https://api.example.com/v1/",
        apiKey: "YOUR_REMOTE_API_KEY",
        headers: {
          "X-Organization": "org-id",
          "X-Project": "project-id"
        }
      }
    }
  }
}
```

Notas:

- O`remote.*`tem precedência sobre o`models.providers.openai.*`.
-`remote.headers`funde-se com cabeçalhos OpenAI; vitórias remotas em conflitos de chaves. Omitir`remote.headers`para usar os padrões do OpenAI.
