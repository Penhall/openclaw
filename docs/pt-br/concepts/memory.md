---
summary: "How OpenClaw memory works (workspace files + automatic memory flush)"
read_when:
  - You want the memory file layout and workflow
  - You want to tune the automatic pre-compaction memory flush
---

Memória

A memória OpenClaw é **plain Markdown no espaço de trabalho do agente**. Os arquivos são o
fonte da verdade; o modelo só "lembra" o que é escrito no disco.

As ferramentas de busca de memória são fornecidas pelo plugin de memória ativa (padrão:
<<CODE0>>). Desabilitar plugins de memória com <<CODE1>>>.

## Arquivos de memória (Markdown)

A disposição padrão do espaço de trabalho usa duas camadas de memória:

- <<CODE0>>
- Diário de bordo.
- Leia hoje + ontem no início da sessão.
- <<CODE1> (opcional)
- Memória de longo prazo.
- ** Só carregar na sessão principal, privada** (nunca em contextos de grupo).

Estes arquivos vivem sob a área de trabalho (<<<CODE0>>, padrão
<<CODE1>>). Ver [Espaço de trabalho do agente](<<<LINK0>>>) para o layout completo.

# # Quando escrever a memória

- As decisões, preferências e fatos duráveis vão para <<CODE0>>.
- Notas do dia-a-dia e contexto em execução ir para <<CODE1>>.
- Se alguém disser "lembre-se disto", escreva-o (não o guarde em RAM).
- Esta área continua a evoluir. Ajuda a lembrar o modelo para armazenar memórias; saberá o que fazer.
- Se queres algo para colar, pede ao robot para o escrever na memória.

# # Automatic memória flush (pré-compaction ping)

Quando uma sessão é ** perto de auto-compaction**, OpenClaw desencadeia um **silent,
agentic turn** que lembra o modelo de escrever memória durável **antes
contexto é compactado. Os prompts padrão dizem explicitamente que o modelo  pode responder ,
mas geralmente <<CODE0>> é a resposta correta para que o usuário nunca veja esta volta.

Isto é controlado por <<CODE0>>:

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

- ** Limiar suave**: gatilhos de descarga quando a estimativa do token de sessão se cruza
<<CODE0>>.
- **Silêncio** por padrão: prompts incluem <<CODE1> assim nada é entregue.
- **Dois prompts**: um prompt do usuário mais um prompt do sistema anexem o lembrete.
- ** Um flush por ciclo de compactação** (traçado em <<CODE2>>>).
- ** O espaço de trabalho deve ser escrito**: se a sessão correr sandboxed com
<<CODE3>> ou <<CODE4>>, o flush é ignorado.

Para o ciclo de vida completo de compactação, ver
[Gestão de sessão + compactação] (<<<LINK0>>>).

# # Pesquisa de memória vetorial

OpenClaw pode construir um pequeno índice vetorial sobre <<CODE0>> e <<CODE1>>> (mais
quaisquer diretórios extras ou arquivos que você optar) para que consultas semânticas possam encontrar relacionados
notas mesmo quando o texto difere.

Predefinição:

- Activado por omissão.
- Observa arquivos de memória para alterações (debunçado).
- Usa incorporações remotas por padrão. Se <<CODE0> não estiver definido, o OpenClaw seleciona automaticamente:
1. <<CODE1> se um <<CODE2> estiver configurado e o arquivo existir.
2. <<CODE3> se uma tecla OpenAI puder ser resolvida.
3. <<CODE4> se uma chave Gemini pode ser resolvida.
4. Caso contrário, a pesquisa de memória permanece desactivada até ser configurada.
- O modo local utiliza o nó- llama- cpp e pode requerer <<CODE5>>.
- Usa sqlite-vec (quando disponível) para acelerar a busca vetorial dentro do SQLite.

Embutições remotas **requer** uma chave API para o provedor incorporador. Openclaw
resolve chaves a partir de perfis de autenticação, <<CODE0>>, ou ambiente
variáveis. O Codex OAuth só cobre chat/compleções e não satisfaz **
incorporações para pesquisa de memória. Para Gemini, utilizar <<CODE1>>> ou
<<CODE2>>>. Ao utilizar um endpoint compatível com OpenAI personalizado,
definido <<CODE3>> (e opcional <<CODE4>>>).

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
- Os diretórios são digitalizados recursivamente para <<CODE0>> arquivos.
- Só os ficheiros Markdown estão indexados.
- Symlinks são ignorados (arquivos ou diretórios).

### Gemini incorporações (nativo)

Defina o provedor para <<CODE0>> para usar a API de incorporação Gemini diretamente:

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

- <<CODE0> é opcional (defaults to the Gemini API base URL).
- <<CODE1> permite adicionar cabeçalhos extras, se necessário.
- Modelo padrão: <<CODE2>>>>.

Se quiser utilizar um endpoint **compatível com OpenAI ** (OpenRouter, vLLM, ou um proxy),
pode utilizar o <<CODE0>> configuração com o fornecedor OpenAI:

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

Se você não quiser definir uma chave API, use <<CODE0>> ou set
<<CODE1>>>.

Regressos:

- <<CODE0>> pode ser <<CODE1>>, <<CODE2>>, <<CODE3>>, ou <<CODE4>>.
- O provedor de retrocesso só é usado quando o provedor principal de incorporação falha.

Indexação em lote (OpenAI + Gemini):

- Habilitado por padrão para incorporação OpenAI e Gemini. Definir <<CODE0>> para desativar.
- O comportamento padrão espera pela conclusão do lote; sintonize <<CODE1>>, <<CODE2>>>, e <<CODE3> se necessário.
- Definir <<CODE4>> para controlar quantos trabalhos em lote enviamos em paralelo (padrão: 2).
- O modo Lote aplica-se quando <<CODE5> ou <<CODE6> e utiliza a chave API correspondente.
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

- <<CODE0>> — retorna trechos com intervalos de arquivo + linha.
- <<CODE1>> — ler o conteúdo do arquivo de memória por caminho.

Modo local:

- Definir <<CODE0>>>.
- Fornecer <<CODE1>> (GGUF ou <HTML2>>URI).
- Opcional: definir <<CODE3> para evitar recuos remotos.

Como funcionam as ferramentas de memória

- <<CODE0> pesquisa semanticamente blocos Markdown (~400 token target, sobreposição de 80 token) de <<CODE1>> + <<CODE2>. Ele retorna texto de trecho (capped ~700 chars), caminho do arquivo, faixa de linha, pontuação, provedor/modelo, e se nós caímos de incorporados locais → remotos. Nenhuma carga completa do arquivo é devolvida.
- <<CODE3> lê um ficheiro de memória específica (relativo ao espaço de trabalho), opcionalmente a partir de uma linha de partida e para linhas N. Caminhos fora <<CODE4>> / <<CODE5>> só são permitidos quando explicitamente listados em <<CODE6>>.
- Ambas as ferramentas estão habilitadas apenas quando <<CODE7> resolve true para o agente.

# # O que é indexado (e quando)

- Tipo de ficheiro: Apenas Markdown (<<<CODE0>>, <<CODE1>>, mais quaisquer <<CODE2> ficheiros em <<CODE3>).
- Armazenamento de índice: por agente SQLite em <<CODE4>> (configurado via <<CODE5>>, suporta <<CODE6> token).
- Frescura: o observador em <<CODE7>>>, <<CODE8>>>, e <<CODE9>> marca o índice sujo (debate 1,5s). A sincronização é agendada no início da sessão, na pesquisa ou em um intervalo e é executada assíncrona. As transcrições das sessões usam limiares delta para activar a sincronização de fundo.
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

- IDs (<<<CODE0>>, <<CODE1>>)
- símbolos de código (<<<CODE2>>)
- strings de erro (“sqlite-vec indisponível”)

BM25 (texto completo) é o oposto: forte em fichas exatas, mais fraco em paráfrases.
Pesquisa híbrida é o meio-termo pragmático: **use ambos os sinais de recuperação** para que você obtenha
bons resultados para as consultas “linguagem natural” e “agulha em um palheiro”.

#### Como mesclamos os resultados (o design atual)

Esboço de implementação:

1. Recuperar um pool candidato de ambos os lados:

- ** Vector**: topo <<CODE0>> por semelhança cossena.
- ** BM25**: topo <<CODE1>> por FTS5 BM25 rank (inferior é melhor).

2. Converta a classificação BM25 em uma pontuação de 0.1-ish:

- <<CODE0>>

3. Candidatos da União por block id e calcular uma pontuação ponderada:

- <<CODE0>>

Notas:

- <<CODE0>> + <<CODE1>> é normalizada para 1,0 em resolução de configuração, de modo que os pesos se comportam como percentuais.
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

Você pode, opcionalmente, indexar ** transcripts de sessão** e superfirá-los via <<CODE0>>.
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
- <<CODE0> nunca bloqueia a indexação; os resultados podem ser ligeiramente obsoletos até que a sincronização de fundo termine.
- Os resultados ainda incluem apenas trechos; <<CODE1> permanece limitado a arquivos de memória.
- A indexação da sessão é isolada por agente (apenas os registros de sessão do agente são indexados).
- Registros de sessão ao vivo no disco (<<CODE2>>>). Qualquer processo/usuário com acesso ao sistema de arquivos pode lê-los, então trate o acesso ao disco como o limite de confiança. Para um isolamento mais rigoroso, execute agentes sob usuários ou hosts separados do sistema operacional.

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
SQLite tabela virtual (<<<CODE0>>) e executa consultas de distância vetorial na
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

- <<CODE0> o valor padrão é true; quando desabilitado, a pesquisa retorna ao processo
similaridade cossena sobre incorporações armazenadas.
- Se a extensão sqlite-vec estiver ausente ou não for carregada, o OpenClaw registra o
erro e continua com o retorno do JS (sem tabela vetorial).
- <<CODE1> > substitui o caminho do pacote sqlite-vec (útil para construções personalizadas
ou locais de instalação não normalizados).

## # Local incorporando auto-download

- Modelo de incorporação local padrão: <<CODE0>> (~0.6 GB).
- Quando <<CODE1>>, <<CODE2> resolve <<CODE3>>; se o GGUF está faltando ele **auto-downloads** para o cache (ou <<CODE4>> se definido), então carrega-o. Os downloads são retomados ao tentar novamente.
- Necessidade de construção nativa: executar <<CODE5>>, escolher <<CODE6>>>, em seguida, <<CODE7>>>.
- Fallback: se a configuração local falhar e <<CODE8>>, mudamos automaticamente para incorporações remotas (<<CODE9>> a menos que seja anulada) e gravamos a razão.

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

- <<CODE0> tem precedência sobre <<CODE1>>.
- <<CODE2>> mesclar com os cabeçalhos do OpenAI; vitórias remotas em conflitos de chaves. Omitir <<CODE3>> para usar os padrões OpenAI.
