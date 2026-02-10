---
summary: "Where OpenClaw loads environment variables and the precedence order"
read_when:
  - You need to know which env vars are loaded, and in what order
  - You are debugging missing API keys in the Gateway
  - You are documenting provider auth or deployment environments
---

# Variáveis de ambiente

OpenClaw puxa variáveis de ambiente de várias fontes. A regra é **nunca sobrepor valores existentes**.

## Precedência (mais alta → mais baixa)

1. ** Ambiente de processo** (o que o processo Gateway já tem da shell-mãe/daemon).
2. **`.env`no diretório de trabalho atual** (dotenv default; não substitui).
3. ** Global`.env`** em`~/.openclaw/.env`(também conhecido por`$OPENCLAW_STATE_DIR/.env`; não substitui).
4. **Config`env`block** in`~/.openclaw/openclaw.json`(aplicado apenas se faltar).
5. ** Importação opcional de shell de login** `env.shellEnv.enabled`ou`OPENCLAW_LOAD_SHELL_ENV=1`, aplicada apenas para chaves esperadas em falta.

Se o ficheiro de configuração estiver completamente ausente, o passo 4 é ignorado; a importação do shell ainda é executada se estiver activo.

## Bloco`env`de configuração

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

## Shell env import

`env.shellEnv`executa sua shell de login e importa apenas ** faltando** chaves esperadas:

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

-`OPENCLAW_LOAD_SHELL_ENV=1`-`OPENCLAW_SHELL_ENV_TIMEOUT_MS=15000`

## Substituição do Env var na configuração

Você pode referenciar env vars diretamente em valores de string de configuração usando a sintaxe`${VAR_NAME}`:

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

Ver [Configuração: substituição do Env var] /gateway/configuration#env-var-substitution-in-config para detalhes completos.

## Relacionado

- [Configuração do portal] /gateway/configuration
- [FAQ: env vars e .env loading] /help/faq#env-vars-and-env-loading
/concepts/models
