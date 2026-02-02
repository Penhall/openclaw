---
summary: "How OpenClaw builds prompt context and reports token usage + costs"
read_when:
  - Explaining token usage, costs, or context windows
  - Debugging context growth or compaction behavior
---

# Uso do item & custos

Faixas OpenClaw **tokens**, não caracteres. Tokens são modelos específicos, mas a maioria
Modelos estilo OpenAI média ~4 caracteres por token para o texto em Inglês.

# # Como o sistema é construído

Openclaw monta seu próprio prompt de sistema em cada execução. Inclui:

- Lista de ferramentas + descrições curtas
- Lista de competências (apenas metadados; instruções são carregadas sob demanda com <<CODE0>>)
- Instruções de auto-atualização
- Espaço de trabalho + ficheiros de arranque (<<<<CODE1>>>, <<CODE2>>>, <<CODE3>>, <<CODE4>>, <<CODE5>>, <<CODE6>>, <<CODE7>> quando novo). Arquivos grandes são truncados por <<CODE8>> (padrão: 20000).
- Hora (UTC + fuso horário do utilizador)
- Responder tags + comportamento cardíaco
- Metadados em tempo de execução (host/OS/model/thinking)

Ver a desagregação completa em [System Prompt] (<<<LINK0>>).

# # O que conta na janela de contexto

Tudo o que o modelo recebe conta para o limite de contexto:

- Prompt de sistema (todas as seções listadas acima)
- Histórico de conversação (mensagens de usuário + assistente)
- Chamadas de ferramenta e resultados de ferramenta
- Anexos/transcripts (imagens, áudio, arquivos)
- Resumos de compactação e artefatos de poda
- Envelopes de provedor ou cabeçalhos de segurança (não visíveis, mas ainda contados)

Para uma quebra prática (por arquivo injetado, ferramentas, habilidades e tamanho do sistema), use <<CODE0>>> ou <<CODE1>>>. Ver [Contexto] (<<<LINK0>>>).

# # Como ver o uso atual do token

Use estes no chat:

- <<CODE0>> → ** carta de estado emoji-rich** com o modelo de sessão, utilização do contexto,
a última resposta input/output tokens, e ** custo estimado** (chave API apenas).
- <<CODE1> → adiciona um rodapé de utilização ** por resposta** a cada resposta.
- Persiste por sessão (armazenada como <<CODE2>>).
- OAuth auth **hides cost** (apenas fichas).
- <<CODE3> → mostra um resumo de custo local de registros de sessão OpenClaw.

Outras superfícies:

- ** TUI/Web TUI:** <<CODE0>> + <<CODE1>> são suportados.
- ** CLI:** <<CODE2>> e <<CODE3>>
janelas de quota do fornecedor (não custos por resposta).

# # Estimativa de custos (quando mostrado)

Os custos são estimados a partir do seu modelo de configuração de preços:

```
models.providers.<provider>.models[].cost
```

Estes são **USD por fichas de 1M** para <<CODE0>>, <<CODE1>>>, <<CODE2>>, e
<<CODE3>>>. Se o preço está faltando, OpenClaw mostra apenas tokens. Tokens OAuth
Nunca mostre o custo do dólar.

# # Cache TTL e impacto poda

O cache de prompt do provedor só se aplica dentro da janela de cache TTL. OpenClaw can
opcionalmente executar **cache-ttl poda**: ele poda a sessão uma vez que o cache TTL
expirou e, em seguida, redefine a janela de cache para que as requisições subsequentes possam reutilizar
contexto recentemente guardado em vez de re-catching o histórico completo. Isto mantém a 'cache'
escrever custos mais baixos quando uma sessão passa ocioso pelo TTL.

Configure- o em [Configuração do portal](<<<LINK0>>>) e veja o
detalhes do comportamento em [Poda de Sessão] (<<<LINK1>>>).

Heartbeat pode manter o cache ** quente** através de lacunas ociosas. Se seu cache de modelo TTL
é <<CODE0>>, definindo o intervalo cardíaco logo abaixo desse (p. ex., <<CODE1>>>>) pode evitar
re-caching o prompt completo, reduzindo os custos de gravação do cache.

Para preços de API antrópica, leituras de cache são significativamente mais baratos do que a entrada
tokens, enquanto o cache escreve são faturados em um multiplicador superior. Veja Antrópicos
preços de cache imediatos para as taxas mais recentes e multiplicadores TTL:
https://docs.anthropic.com/docs/build-with-claude/prompt-caching

## # Exemplo: manter o cache 1h quente com batimento cardíaco

```yaml
agents:
  defaults:
    model:
      primary: "anthropic/claude-opus-4-5"
    models:
      "anthropic/claude-opus-4-5":
        params:
          cacheControlTtl: "1h"
    heartbeat:
      every: "55m"
```

# # Dicas para reduzir a pressão do token

- Use <<CODE0>> para resumir sessões longas.
- Aparar grandes saídas de ferramentas em seus fluxos de trabalho.
- Mantenha descrições de habilidade curtas (lista de habilidades é injetada no prompt).
- Prefere modelos mais pequenos para trabalhos exploratórios.

Veja [Skills](<<<LINK0>>) para a fórmula exata da lista de habilidades.
