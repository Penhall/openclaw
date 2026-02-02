---
summary: "Firecrawl fallback for web_fetch (anti-bot + cached extraction)"
read_when:
  - You want Firecrawl-backed web extraction
  - You need a Firecrawl API key
  - You want anti-bot extraction for web_fetch
---

Firecrawl

OpenClaw pode usar **Firecrawl** como um extrator para `web_fetch`. É um hospedado
serviço de extração de conteúdo que suporta evasão de bot e cache, o que ajuda
com sites JS-pesados ou páginas que bloqueiam as buscas HTTP simples.

# # Obter uma chave API

1. Crie uma conta Firecrawl e gere uma chave API.
2. Armazená-lo em configuração ou conjunto `FIRECRAWL_API_KEY` no ambiente gateway.

## Configurar Firecrawl

```json5
{
  tools: {
    web: {
      fetch: {
        firecrawl: {
          apiKey: "FIRECRAWL_API_KEY_HERE",
          baseUrl: "https://api.firecrawl.dev",
          onlyMainContent: true,
          maxAgeMs: 172800000,
          timeoutSeconds: 60,
        },
      },
    },
  },
}
```

Notas:

- <<CODE0> o padrão é true quando uma chave API está presente.
- <<CODE1> controla a idade dos resultados em cache (ms). O padrão é de 2 dias.

# # A evasão furtiva / bot

Firecrawl expõe um parâmetro **proxy para evasão de bots (<`basic`, `stealth`, ou `auto`).
OpenClaw sempre usa `proxy: "auto"` mais `storeInCache: true` para pedidos Firecrawl.
Se proxy for omitido, Firecrawl defaults to `auto`. <<CODE6> repete com proxies furtivas se uma tentativa básica falhar, que pode usar mais créditos
que apenas raspagem básica.

Como <<CODE0> usa Firecrawl

Ordem de extracção <<CODE0>:

1. Readability (local)
2. Firecrawl (se configurado)
3. Limpeza básica em HTML (último recurso)

Veja [Ferramentas web](</tools/web) para a configuração completa da ferramenta web.
