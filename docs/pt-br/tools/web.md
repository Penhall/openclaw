---
summary: "Web search + fetch tools (Brave Search API, Perplexity direct/OpenRouter)"
read_when:
  - You want to enable web_search or web_fetch
  - You need Brave Search API key setup
  - You want to use Perplexity Sonar for web search
---

Ferramentas Web

OpenClaw envia duas ferramentas web leves:

- `web_search` — Pesquise na web através de Brave Search API (padrão) ou Perplexity Sonar (direto ou via OpenRouter).
- `web_fetch` — HTTP fetch + extração legível (HTML → markdown/text).

Estes são ** não** automação do navegador. Para sites JS-pesados ou logins, use o
[Ferramenta do navegador] (/tools/browser).

# # Como funciona

- <<CODE0> chama seu provedor configurado e retorna resultados.
- **Brave** (padrão): retorna resultados estruturados (título, URL, trecho).
- **Perplexidade**: retorna respostas sintetizadas por IA com citações da pesquisa web em tempo real.
- Os resultados são guardados em cache por consulta por 15 minutos (configurável).
- <<CODE1> faz um HTTP GET simples e extrai conteúdo legível
(HTML → markdown/text). Ele faz **not** executar JavaScript.
- <<CODE2> é ativado por padrão (a menos que explicitamente desabilitado).

# # Escolhendo um provedor de pesquisa

Pros Prós Contras API Key
------------------------ ---------------------------------------------------------------------------------------------------------------------------------
Resultados rápidos e estruturados, níveis livres
Perplexidade** Respostas sintetizadas por IA, citações, em tempo real.

Veja [Configuração de pesquisa corajosa](</brave-search) e [Sonar de Perplexidade](/perplexity) para detalhes específicos do provedor.

Definir o provedor na configuração:

```json5
{
  tools: {
    web: {
      search: {
        provider: "brave", // or "perplexity"
      },
    },
  },
}
```

Exemplo: mudar para o Sonar de Perplexidade ( API direta):

```json5
{
  tools: {
    web: {
      search: {
        provider: "perplexity",
        perplexity: {
          apiKey: "pplx-...",
          baseUrl: "https://api.perplexity.ai",
          model: "perplexity/sonar-pro",
        },
      },
    },
  },
}
```

# # Obtendo uma chave de API corajosa

1. Criar uma conta API de pesquisa corajosa em https://brave.com/search/api/
2. No painel, escolha o plano **Data for Search** (não “Data for AI”) e gere uma chave API.
3. Executar `openclaw configure --section web` para armazenar a chave na configuração (recomendada), ou definir `BRAVE_API_KEY` em seu ambiente.

Bravo fornece uma camada livre mais planos pagos; verifique o portal API Bravo para o
Os limites actuais e os preços.

## # Onde definir a chave (recomendado)

**Recomendado:** executar `openclaw configure --section web`. Armazena a chave em
<<CODE1> em `tools.web.search.apiKey`.

** Alternativa do ambiente:** definido <<CODE0> no processo Gateway
ambiente. Para uma instalação de gateway, coloque em <<CODE1> (ou a sua
ambiente de serviço). Ver [Env vars] (</help/faq#how-does-openclaw-load-environment-variables).

# # Usando Perplexidade (direta ou via OpenRouter)

Perplexidade Os modelos Sonar têm recursos de busca na web incorporados e retornam o sintetizador de IA
respostas com citações. Você pode usá-los via OpenRouter (sem cartão de crédito necessário - suportes
cripto/pré-pago).

A obter uma chave de API OpenRouter

1. Criar uma conta em https://openrouter.ai/
2. Adicione créditos (suporta criptografia, pré-pago, ou cartão de crédito)
3. Gerar uma chave API em suas configurações de conta

A configurar a busca por Perplexidade

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        provider: "perplexity",
        perplexity: {
          // API key (optional if OPENROUTER_API_KEY or PERPLEXITY_API_KEY is set)
          apiKey: "sk-or-v1-...",
          // Base URL (key-aware default if omitted)
          baseUrl: "https://openrouter.ai/api/v1",
          // Model (defaults to perplexity/sonar-pro)
          model: "perplexity/sonar-pro",
        },
      },
    },
  },
}
```

** Alternativa do ambiente:** definida `OPENROUTER_API_KEY` ou `PERPLEXITY_API_KEY` na Gateway
ambiente. Para uma instalação de gateway, coloque-a em `~/.openclaw/.env`.

Se nenhum URL base estiver definido, o OpenClaw escolhe um padrão baseado na fonte da chave da API:

- <<CODE0> ou `pplx-...` → `https://api.perplexity.ai`
- <<CODE3> ou `sk-or-...` → `https://openrouter.ai/api/v1`
- Formatos de chave desconhecidos → OpenRouter (fallback seguro)

# # # Modelos de Perplexidade disponíveis

Descrição do modelo
□------------------------------------------------ --------------------------------------------------------------------
• Perguntas e respostas rápidas com pesquisa na web
(padrão) (Raciocínio multi-step com pesquisa na web)
Análise da cadeia de pensamento

Pesquisa na Web

Pesquise na web usando seu provedor configurado.

# # # Requisitos

- `tools.web.search.enabled` não deve ser `false` (padrão: activado)
- Chave API para o provedor escolhido:
- ** Bravo**: `BRAVE_API_KEY` ou `tools.web.search.apiKey`
- **Perplexidade**: `OPENROUTER_API_KEY`, `PERPLEXITY_API_KEY`, ou `tools.web.search.perplexity.apiKey`

Config

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        apiKey: "BRAVE_API_KEY_HERE", // optional if BRAVE_API_KEY is set
        maxResults: 5,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
      },
    },
  },
}
```

## # Parâmetros da ferramenta

- <<CODE0> (obrigatório)
- <<CODE1> (1-10; padrão da configuração)
- `country` (opcional): código de país de duas letras para os resultados específicos da região (por exemplo, "DE", "US", "ALL"). Se omitido, Brave escolhe sua região padrão.
- `search_lang` (opcional): Código ISO para os resultados da pesquisa (por exemplo, "de", "en", "fr")
- `ui_lang` (facultativo): Código ISO para elementos UI
- `freshness` (opcional, Bravo apenas): filtro pelo tempo de descoberta (`pd`, `pw`, `pm`, `py`, ou `YYYY-MM-DDtoYYYY-MM-DD`)

**Exemplos:**

```javascript
// German-specific search
await web_search({
  query: "TV online schauen",
  count: 10,
  country: "DE",
  search_lang: "de",
});

// French search with French UI
await web_search({
  query: "actualités",
  country: "FR",
  search_lang: "fr",
  ui_lang: "fr",
});

// Recent results (past week)
await web_search({
  query: "TMBG interview",
  freshness: "pw",
});
```

## Web fetch

Obter um URL e extrair conteúdo legível.

# # # Requisitos

- `tools.web.fetch.enabled` não deve ser `false` (padrão: activado)
- Retrocesso opcional do Firecrawl: definido `tools.web.fetch.firecrawl.apiKey` ou `FIRECRAWL_API_KEY`.

Config

```json5
{
  tools: {
    web: {
      fetch: {
        enabled: true,
        maxChars: 50000,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
        maxRedirects: 3,
        userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        readability: true,
        firecrawl: {
          enabled: true,
          apiKey: "FIRECRAWL_API_KEY_HERE", // optional if FIRECRAWL_API_KEY is set
          baseUrl: "https://api.firecrawl.dev",
          onlyMainContent: true,
          maxAgeMs: 86400000, // ms (1 day)
          timeoutSeconds: 60,
        },
      },
    },
  },
}
```

## # Parâmetros da ferramenta

- `url` (exigido apenas em http/https)
- <<CODE1> (`markdown` `text`)
- <<CODE4> (páginas longas)

Notas:

- <<CODE0> usa Readability (extracção de conteúdo principal) primeiro, depois Firecrawl (se configurado). Se ambos falharem, a ferramenta retorna um erro.
- Requisições Firecrawl usam o modo de evasão de bots e resultados de cache por padrão.
- <<CODE1> envia um agente de usuário tipo Chrome e `Accept-Language` por padrão; sobreposição `userAgent` se necessário.
- <<CODE4> bloqueia os nomes de host privados/internos e verifica de novo os redirecionamentos (limite com `maxRedirects`).
- <<CODE6> é a melhor extração de esforço; alguns sites vão precisar da ferramenta do navegador.
- Veja [Firecrawl](/tools/firecrawl) para detalhes de configuração e serviço de chave.
- As respostas são em cache (padrão 15 minutos) para reduzir as buscas repetidas.
- Se utilizar perfis de ferramentas/listas de licenças, adicione <<CODE7>/`web_fetch` ou `group:web`.
- Se faltar a chave corajosa, <<CODE10> retorna uma dica de configuração curta com um link de documentos.
