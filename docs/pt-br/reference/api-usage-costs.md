---
summary: "Audit what can spend money, which keys are used, and how to view usage"
read_when:
  - You want to understand which features may call paid APIs
  - You need to audit keys, costs, and usage visibility
  - You’re explaining /status or /usage cost reporting
---

# Uso da API & custos

Este documento lista ** recursos que podem invocar chaves API** e onde seus custos aparecem. Concentra-se em
Recursos OpenClaw que podem gerar uso de provedor ou chamadas de API pagas.

# # Onde os custos aparecem (chat + CLI)

** Instantâneo de custo por sessão**

- <<CODE0> mostra o modelo de sessão atual, o uso do contexto e os tokens de última resposta.
- Se o modelo utiliza **API-key auth**, <<CODE1> também mostra ** custo estimado** para a última resposta.

** Per-mensagem custo rodapé **

- `/usage full` adiciona um rodapé de utilização a cada resposta, incluindo ** custo estimado** (apenas API-chave).
- <<CODE1> mostra apenas fichas; Os fluxos de OAuth escondem o custo do dólar.

** Janelas de utilização de CLI (quotas de fornecedores) **

- `openclaw status --usage` e <<CODE1> mostram o fornecedor ** janelas de utilização **
(snapshotsquota, não custos por mensagem).

Ver [Token use & costs](</token-use) para detalhes e exemplos.

# # Como as chaves são descobertas

Openclaw pode pegar credenciais de:

- Perfis de autenticação** (por agente, armazenados em `auth-profiles.json`).
- ** Variáveis de ambiente** (por exemplo, `OPENAI_API_KEY`, `BRAVE_API_KEY`, `FIRECRAWL_API_KEY`).
- **Config** (`models.providers.*.apiKey`, <CODE5>>, `tools.web.fetch.firecrawl.*`,
`memorySearch.*`, `talk.apiKey`).
- ** Skills** (`skills.entries.<name>.apiKey`) que pode exportar chaves para o processo de habilidade env.

# # Características que podem gastar chaves

## # 1) Respostas do modelo principal (chat + ferramentas)

Cada resposta ou chamada de ferramenta usa o provedor **current model** (OpenAI, Anthropic, etc). Este é o
fonte primária de utilização e custo.

Ver [Modelos](</providers/models) para configuração de preços e [Token use & costs](/token-use) para exibição.

### 2) Compreensão de mídia (áudio/imagem/vídeo)

Os meios de entrada podem ser resumidos/transcritos antes da resposta ser executada. Isto usa APIs de modelo/fornecedor.

- Áudio: OpenAI / Groq / Deepgram (agora ** auto- habilitado** quando existem chaves).
- Imagem: OpenAI / Anthropic / Google.
- Vídeo: Google.

Ver [Compreensão da mídia] (</nodes/media-understanding).

## # 3) Incorporações de memória + pesquisa semântica

A pesquisa de memória semântica usa ** APIs incorporadas** quando configuradas para provedores remotos:

- <<CODE0> → Incorporações OpenAI
- <<CODE1> → Incorporações gemini
- Regresso opcional ao OpenAI se as incorporações locais falharem

Você pode mantê-lo local com `memorySearch.provider = "local"` (sem uso de API).

Ver [Memória] (</concepts/memory).

# # # 4) Ferramenta de pesquisa web (Bravo / Perplexidade via OpenRouter)

<<CODE0> usa chaves API e pode incorrer em taxas de uso:

- **Brave Search API**: `BRAVE_API_KEY` ou `tools.web.search.apiKey`
- **Perplexidade** (via OpenRouter): `PERPLEXITY_API_KEY` ou `OPENROUTER_API_KEY`

**Brave free layer (generioso): **

- **2.000 pedidos/mês**
- **1 pedido/segundo
- ** Cartão de crédito necessário** para verificação (sem custo, a menos que você atualizar)

Ver [Ferramentas Web] (</tools/web).

## # 5) Ferramenta de busca da Web (Firecrawl)

<<CODE0> pode chamar **Firecrawl** quando uma chave API está presente:

- <<CODE0> ou <<CODE1>

Se Firecrawl não estiver configurado, a ferramenta cai para buscar + legibilidade direta (sem API paga).

Ver [Ferramentas Web] (</tools/web).

## # 6) Instantâneos de uso do provedor (estado/saúde)

Alguns comandos de status chamam **provider use endpoints** para exibir janelas de cotas ou auth health.
Estas são tipicamente chamadas de baixo volume, mas ainda batem nas APIs do provedor:

- <<CODE0>
- <<CODE1>

Ver [Modelos CLI] (</cli/models).

# # # 7) Compactação resguarda resumo

A salvaguarda da compactação pode resumir o histórico de sessões usando o **modelo atual**, que
invoca APIs de provedor quando é executado.

Ver [Gestão de sessão + compactação] (</reference/session-management-compaction).

# # # 8) Modelo de varredura / sonda

<<CODE0> pode sondar modelos OpenRouter e usa `OPENROUTER_API_KEY` quando
A sondagem está activada.

Ver [Modelos CLI] (</cli/models).

### 9) Conversa

O modo de conversa pode invocar **ElevenLabs** quando configurado:

- <<CODE0> ou <<CODE1>

Veja [Modo de fala] (</nodes/talk).

### 10) Habilidades ( APIs de terceiros)

As habilidades podem armazenar `apiKey` em `skills.entries.<name>.apiKey`. Se uma habilidade usa essa chave para o exterior
APIs, pode incorrer custos de acordo com o provedor da habilidade.

Ver [Skills] (</tools/skills).
