---
summary: "Use MiniMax M2.1 in OpenClaw"
read_when:
  - You want MiniMax models in OpenClaw
  - You need MiniMax setup guidance
---

MiniMax

MiniMax é uma empresa de IA que constrói a família de modelos ** M2/M2.1**. A atual
A versão focada em codificação é **MiniMax M2.1** (23 de dezembro de 2025), construída para
tarefas complexas do mundo real.

Fonte: [MiniMax M2.1 release note](https://www.minimax.io/news/minimax-m21)

# # Visão geral do modelo (M2.1)

MiniMax destaca estas melhorias em M2.1:

- Mais forte **codificação multi-linguagem** (Rust, Java, Go, C++, Kotlin, Objective-C, TS/JS).
- Melhor desenvolvimento web/app** e qualidade de saída estética (incluindo celular nativo).
- Melhoria da instrução **composite** manipulação para fluxos de trabalho de escritório,
pensamento interleaved e execução de restrição integrada.
- **Respostas mais concisas** com o uso de token mais baixo e loops de iteração mais rápidos.
- mais forte **tool/agent framework** compatibilidade e gestão de contexto (Claude Code,
Droid / Fábrica IA, Cline, Kilo Código, Roo Código, BlackBox).
- Alta qualidade **diálogo e escrita técnica** saídas.

# # MiniMax M2.1 vs MiniMax M2.1 Raios

- ** Velocidade:** Lightning é a variante “rápido” nos documentos de preços da MiniMax.
- ** Custo:** Os preços mostram o mesmo custo de entrada, mas Lightning tem maior custo de saída.
- **Roteamento do plano de codificação:** A infra-estrutura Lightning não está diretamente disponível no MiniMax
Plano de codificação. MiniMax auto-rotas a maioria dos pedidos para Lightning, mas cai de volta para o
back-end M2.1 regular durante picos de tráfego.

# # Escolha uma configuração

## # MiniMax OAuth (Plano de Codificação) – recomendado

**Melhor para:** configuração rápida com MiniMax Coding Plan via OAuth, nenhuma chave API necessária.

Activar o 'plugin' OAuth embalado e autenticar:

```bash
moltbot plugins enable minimax-portal-auth  # skip if already loaded.
moltbot gateway restart  # restart if gateway is already running
moltbot onboard --auth-choice minimax-portal
```

Você será solicitado a selecionar um endpoint:

- **Global** - Utilizadores internacionais (<`api.minimax.io`)
- **CN** - Utilizadores na China (<`api.minimaxi.com`)

Veja [MiniMax OAuth plugin README](<https://github.com/moltbot/moltbot/tree/main/extensions/minimax-portal-auth) para detalhes.

## # MiniMax M2.1 (chave API)

**Melhor para:** MiniMax hospedado com API compatível com Anthropic.

Configurar via CLI:

- Executar <<CODE0>
- Selecione **Modelo/auth**
- Escolha **MiniMax M2.1**

```json5
{
  env: { MINIMAX_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "minimax/MiniMax-M2.1" } } },
  models: {
    mode: "merge",
    providers: {
      minimax: {
        baseUrl: "https://api.minimax.io/anthropic",
        apiKey: "${MINIMAX_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "MiniMax-M2.1",
            name: "MiniMax M2.1",
            reasoning: false,
            input: ["text"],
            cost: { input: 15, output: 60, cacheRead: 2, cacheWrite: 10 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## # MiniMax M2.1 como backback (Opus primário)

**Melhor para:** manter Opus 4.5 como primário, falhar para MiniMax M2.1.

```json5
{
  env: { MINIMAX_API_KEY: "sk-..." },
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-5": { alias: "opus" },
        "minimax/MiniMax-M2.1": { alias: "minimax" },
      },
      model: {
        primary: "anthropic/claude-opus-4-5",
        fallbacks: ["minimax/MiniMax-M2.1"],
      },
    },
  },
}
```

# # # Opcional: Local via LM Studio (manual)

**Melhor para:** inferência local com LM Studio.
Nós vimos resultados fortes com MiniMax M2.1 em hardware poderoso (por exemplo, um
desktop/servidor) usando o servidor local do LM Studio.

Configurar manualmente via <<CODE0>:

```json5
{
  agents: {
    defaults: {
      model: { primary: "lmstudio/minimax-m2.1-gs32" },
      models: { "lmstudio/minimax-m2.1-gs32": { alias: "Minimax" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      lmstudio: {
        baseUrl: "http://127.0.0.1:1234/v1",
        apiKey: "lmstudio",
        api: "openai-responses",
        models: [
          {
            id: "minimax-m2.1-gs32",
            name: "MiniMax M2.1 GS32",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 196608,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## Configurar via `openclaw configure`

Use o assistente de configuração interativo para definir MiniMax sem editar JSON:

1. Executar `openclaw configure`.
2. Selecione **Modelo/auth**.
3. Escolha **MiniMax M2.1**.
4. Escolha o seu modelo padrão quando solicitado.

# # Opções de configuração

- <<CODE0>: preferir <<CODE1> (Compatível com antrópicos); <<CODE2> é opcional para cargas disponíveis compatíveis com OpenAI.
- `models.providers.minimax.api`: preferir `anthropic-messages`; `openai-completions` é opcional para as cargas disponíveis compatíveis com o OpenAI.
- `models.providers.minimax.apiKey`: Tecla API MiniMax (`MINIMAX_API_KEY`).
- `models.providers.minimax.models`: definir `id`, `name`, `reasoning`, `contextWindow`, <<CODE13>, `cost`.
- `agents.defaults.models`: alias models que você deseja na lista de permissões.
- `models.mode`: manter `merge` se você quiser adicionar MiniMax ao lado built-ins.

# # Notas

- Os refs-modelo são `minimax/<model>`.
- API de uso do plano de codificação: `https://api.minimaxi.com/v1/api/openplatform/coding_plan/remains` (necessita de uma chave de plano de codificação).
- Atualizar valores de preços em `models.json` se você precisar de monitoramento exato de custos.
- Ligação de referência para o plano de codificação MiniMax (10% de desconto): https://platform.minimax.io/subscribe/coding-plan?code=DbXJTRClnb&source=link
- Ver [/conceitos/modelo-fornecedores](/concepts/model-providers) para as regras do prestador.
- Utilizar `openclaw models list` e `openclaw models set minimax/MiniMax-M2.1` para alternar.

# # Resolução de problemas

## # “Modelo desconhecido: minimax/MiniMax-M2.1”

Isso geralmente significa que o provedor **MiniMax não está configurado** (nenhuma entrada do provedor
e nenhuma chave miniMax auth profile/env encontrada). Uma correção para esta detecção está em
**2026.1.12** (não lançado no momento da escrita). Corrigir por:

- Atualizando para **2026.1.12** (ou executando a partir de fonte `main`), então reiniciando o gateway.
- Execução <<CODE1> e selecção **MiniMax M2.1**, ou
- Adicionar o bloco <<CODE2> manualmente, ou
- Definir `MINIMAX_API_KEY` (ou um perfil de autenticação MiniMax) para que o fornecedor possa ser injectado.

Certifique-se de que o ID do modelo é **caso- sensível**:

- <<CODE0>
- <<CODE1>

Em seguida, verifique novamente com:

```bash
openclaw models list
```
