---
summary: "Brave Search API setup for web_search"
read_when:
  - You want to use Brave Search for web_search
  - You need a BRAVE_API_KEY or plan details
---

API de pesquisa corajosa

OpenClaw usa a pesquisa corajosa como o provedor padrão para`web_search`.

## Obter uma chave API

1. Criar uma conta API de pesquisa corajosa em https://brave.com/search/api/
2. No painel, escolha o plano **Data for Search** e gere uma chave API.
3. Armazenar a chave na configuração (recomendada) ou definir`BRAVE_API_KEY`no ambiente Gateway.

## Exemplo de configuração

```json5
{
  tools: {
    web: {
      search: {
        provider: "brave",
        apiKey: "BRAVE_API_KEY_HERE",
        maxResults: 5,
        timeoutSeconds: 30,
      },
    },
  },
}
```

## Notas

- Os dados para o plano de IA não são ** compatíveis com`web_search`.
- Bravo fornece uma camada livre mais planos pagos; verifique o portal API Bravo para os limites atuais.

Veja [Ferramentas Web]/tools/web para a configuração completa da pesquisa na web.
