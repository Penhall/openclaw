---
summary: "Where OpenClaw loads environment variables and the precedence order"
read_when:
  - You need to know which env vars are loaded, and in what order
  - You are debugging missing API keys in the Gateway
  - You are documenting provider auth or deployment environments
---

# Variáveis de ambiente

OpenClaw puxa variáveis de ambiente de várias fontes. A regra é **nunca sobrepor valores existentes**.

# # Precedência (mais alta → mais baixa)

1. ** Ambiente de processo** (o que o processo Gateway já tem da shell-mãe/daemon).
2. **<<<CODE0>> no diretório de trabalho atual** (dotenv padrão; não substitui).
3. **Global <<CODE1>** em <<CODE2>>> (também conhecido por <<CODE3>>; não substitui).
4. **Config <<CODE4>>bloqueio** em <<CODE5>>> (aplicado apenas se faltar).
5. ** Importação opcional de cartuchos de login** (<<<CODE6>> ou <<CODE7>>>>>), aplicada apenas para chaves em falta.

Se o ficheiro de configuração estiver completamente ausente, o passo 4 é ignorado; a importação do shell ainda é executada se estiver activo.

Configuração <<CODE0>> block

Duas formas equivalentes de definir env vars em linha (ambos não são imperiosos):

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: {
      GROQ_API_KEY: "gsk-...",
    },
  },
}
```

# # Shell env import

<<CODE0> roda sua shell de login e importa apenas **falso** chaves esperadas:

```json5
{
  env: {
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}
```

Env var equivalentes:

- <<CODE0>>
- <<CODE1>>

# # Substituição do Env var na configuração

Você pode referenciar env vars diretamente em valores de string config usando sintaxe <<CODE0>>:

```json5
{
  models: {
    providers: {
      "vercel-gateway": {
        apiKey: "${VERCEL_GATEWAY_API_KEY}",
      },
    },
  },
}
```

Ver [Configuração: substituição do Env var] (<<<LINK0>>>) para detalhes completos.

# # Relacionado

- [Configuração do portal] (<<<LINK0>>>)
- [FAQ: env vars and .env loading] (<<<<LINK1>>>>)
- [Observação dos modelos] (<<<LINK2>>>)
