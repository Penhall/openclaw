---
summary: "CLI reference for `openclaw models` (status/list/set/scan, aliases, fallbacks, auth)"
read_when:
  - You want to change default models or view provider auth status
  - You want to scan available models/providers and debug auth profiles
---

#`openclaw models`

Modelo descoberta, digitalização e configuração (modelo padrão, fallbacks, perfis de autenticação).

Relacionados:

- Fornecedores + modelos: [Modelos] /providers/models
- Configuração da autenticação do fornecedor: [Iniciando] /start/getting-started

## Comandos comuns

```bash
openclaw models status
openclaw models list
openclaw models set <model-or-alias>
openclaw models scan
```

`openclaw models status`mostra o padrão/fallbacks resolvidos mais uma visão geral de autenticação.
Quando os instantâneos de uso do provedor estão disponíveis, a seção de status OAuth/token inclui
cabeçalhos de uso do provedor.
Adicione`--probe`para executar sondas de autenticação ao vivo contra cada perfil de provedor configurado.
As sondas são pedidos reais (podem consumir tokens e acionar limites de taxa).
Use`--agent <id>`para inspecionar o modelo/estado do agente configurado. Quando omitido,
o comando utiliza`OPENCLAW_AGENT_DIR`/`PI_CODING_AGENT_DIR`se definido, caso contrário o
agente padrão configurado.

Notas:

- O`models set <model-or-alias>`aceita o`provider/model`ou um alias.
- Os refs do modelo são analisados dividindo no **primeiro**`/`. Se o ID do modelo incluir`/`(estilo OpenRouter), inclua o prefixo do provedor (exemplo:`openrouter/moonshotai/kimi-k2`.
- Se você omitir o provedor, OpenClaw trata a entrada como um alias ou um modelo para o provedor **default** (apenas funciona quando não há`/`no ID do modelo).

## #`models status`

Opções:

-`--json`-`--plain`-`--check`(saída 1 = expirada/falta, 2 = expirada)
-`--probe`(sonda viva de perfis de autenticação configurados)
-`--probe-provider <name>`(sonda de um fornecedor)
-`--probe-profile <id>`(repetição ou identificação de perfil separada por vírgulas)
-`--probe-timeout <ms>`-`--probe-concurrency <n>`-`--probe-max-tokens <n>`-`--agent <id>`(id do agente configurado; substitui`--plain`0/`--plain`1)

## Apelidos + recuos

```bash
openclaw models aliases list
openclaw models fallbacks list
```

## Perfis de autenticação

```bash
openclaw models auth add
openclaw models auth login --provider <id>
openclaw models auth setup-token
openclaw models auth paste-token
```

`models auth login`executa o fluxo de autenticação de um plugin de provedor (chave OAuth/API). Utilização`openclaw plugins list`para ver quais fornecedores estão instalados.

Notas:

-`setup-token`pede um valor de configuração (gerar com`claude setup-token`em qualquer máquina).
-`paste-token`aceita uma string de token gerada em outro lugar ou da automação.
