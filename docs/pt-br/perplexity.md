---
summary: "Perplexity Sonar setup for web_search"
read_when:
  - You want to use Perplexity Sonar for web search
  - You need PERPLEXITY_API_KEY or OpenRouter setup
---

Sonar de Perplexidade

OpenClaw pode usar Sonar Perplexity para a ferramenta <<CODE0>>. Você pode conectar
através da API direta da Perplexity ou através do OpenRouter.

# # Opções da API

## # Perplexidade (direta)

- URL base: https://api.perplexity.ai
- Variável ambiente: <<CODE0>>

OpenRouter (alternativo)

- URL base: https://openrouter.ai/api/v1
- Variável ambiente: <<CODE0>>
- Suporta créditos pré-pagos/cripto.

# # Exemplo de configuração

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

# # Mudando de Bravo

```json5
{
  tools: {
    web: {
      search: {
        provider: "perplexity",
        perplexity: {
          apiKey: "pplx-...",
          baseUrl: "https://api.perplexity.ai",
        },
      },
    },
  },
}
```

Se forem definidos ambos <<CODE0>> e <<CODE1>>>, definir
<<CODE2>> (ou <<CODE3>>>)
para desambiguar.

Se nenhum URL base estiver definido, o OpenClaw escolhe um padrão baseado na fonte da chave da API:

- <<CODE0>> ou <<CODE1>> → Perplexidade directa (<<CODE2>>)
- <<CODE3>> ou <<CODE4>> → OpenRouter (<<CODE5>)
- Formatos de chave desconhecidos → OpenRouter (fallback seguro)

# # Modelos

- <<CODE0>> — perguntas e respostas rápidas com pesquisa na web
- <<CODE1> (padrão) — raciocínio multi-passo + pesquisa na web
- <<CODE2>> — investigação aprofundada

Veja [Ferramentas Web](<<<LINK0>>) para a configuração completa de web search.
