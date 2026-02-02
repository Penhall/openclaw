---
summary: "Use Venice AI privacy-focused models in OpenClaw"
read_when:
  - You want privacy-focused inference in OpenClaw
  - You want Venice AI setup guidance
---

# Venice AI (ponto alto da Veneza)

**Venice** é a nossa configuração de Veneza de destaque para a primeira inferência de privacidade com acesso anônimo opcional a modelos proprietários.

Venice AI fornece inferência de IA focada em privacidade com suporte para modelos sem censura e acesso a modelos proprietários principais através de seu proxy anônimo. Toda inferência é privada por padrão – sem treinamento em seus dados, sem registro.

# # Por que Veneza em OpenClaw

- **Inferência privada** para modelos de código aberto (sem registro).
- **Modelos sem censura** quando você precisa deles.
- ** Acesso anônimo** a modelos proprietários (Opus/GPT/Gemini) quando a qualidade importa.
- Objectivos compatíveis com o OpenAI `/v1`.

# # Modos de privacidade

Veneza oferece dois níveis de privacidade — entender isso é fundamental para escolher o seu modelo:

Modelos
----------------- ---- -------------------------------------------------------------------------------------------------------------------------------------------------------------------- -----------
* Privada** Totalmente privada. Os prompts/respostas são ** nunca armazenados ou registrados **. Ephemeral.
* Anonymized** * Proxied através de Veneza com metadados despojados. O provedor subjacente (OpenAI, Anthropic) vê pedidos anônimos. Claude, GPT, Gemini, Grok, Kimi, MiniMax

# # Características

- ** Focado na privacidade**: Escolha entre os modos "private" (fully private) e "anonymized" (proxied)
- **Modelos sem censura**: Acesso a modelos sem restrições de conteúdo
- **Acesso ao modelo principal**: Use Claude, GPT-5.2, Gemini, Grok via proxy anônimo de Veneza
- ** API compatível com o OpenAI**: Endpoints padrão <<CODE0> para fácil integração
- **Streaming **: , Suportado em todos os modelos
- ** Chamada de funções**: □ Suportado em modelos selecionados (verificar capacidades do modelo)
- **Visão**:
- **Sem limites de taxa dura**: O estrangulamento de uso justo pode ser aplicado para uso extremo

Configuração

## # 1. Obter chave API

1. Inscreva-se em [venice.ai] (<https://venice.ai)
2. Vá para **Configurações → API Keys → Criar nova chave**
3. Copie sua chave API (formato: `vapi_xxxxxxxxxxxx`)

## # 2. Configurar OpenClaw

**Opção A: Variável de Ambiente**

```bash
export VENICE_API_KEY="vapi_xxxxxxxxxxxx"
```

**Opção B: Configuração Interactiva (Recomendada)**

```bash
openclaw onboard --auth-choice venice-api-key
```

Isto será:

1. Peça para sua chave API (ou use existente `VENICE_API_KEY`)
2. Mostrar todos os modelos de Veneza disponíveis
3. Deixar você escolher seu modelo padrão
4. Configurar o provedor automaticamente

**Opção C: Não-interactiva

```bash
openclaw onboard --non-interactive \
  --auth-choice venice-api-key \
  --venice-api-key "vapi_xxxxxxxxxxxx"
```

## 3. Verificar configuração

```bash
openclaw chat --model venice/llama-3.3-70b "Hello, are you working?"
```

# # Seleção do modelo

Após a configuração, OpenClaw mostra todos os modelos de Veneza disponíveis. Escolha com base em suas necessidades:

- **Padrão (nossa escolha)**: <<CODE0> para desempenho privado e equilibrado.
- **Melhor qualidade global**: `venice/claude-opus-45` para trabalhos duros (Opus continua a ser o mais forte).
- **Privacidade**: Escolha modelos "privados" para inferência totalmente privada.
- ** Capacidade**: Escolha modelos "anônimos" para acessar Claude, GPT, Gemini via proxy de Veneza.

Altere seu modelo padrão a qualquer momento:

```bash
openclaw models set venice/claude-opus-45
openclaw models set venice/llama-3.3-70b
```

Listar todos os modelos disponíveis:

```bash
openclaw models list | grep venice
```

## Configurar via `openclaw configure`

1. Executar <<CODE0>
2. Selecione **Modelo/auth**
3. Escolha **Veneza IA**

# # Que modelo devo usar?

Caso de uso , modelo recomendado , por que
------------------- (---------------------------------------------------------------- --------------------------------------------------------
Conversa geral Bom all-around, totalmente privado
Melhor qualidade global** <<CODE1> Opus permanece o mais forte para tarefas difíceis
Privacidade + qualidade Claude** Qualidade `claude-opus-45` Melhor raciocínio via proxy anônimo
* Codificação** `qwen3-coder-480b-a35b-instruct`
. . . . . . . . . . . . . . . . Melhor modelo de visão privada
* Sem censura * * `venice-uncensored` Sem restrições de conteúdo
Mais rápido + barato** `qwen3-4b`
Raciocínio complexo** Raciocínio forte, privado

# # Modelos Disponíveis (25 Total)

## # Modelos privados (15) — Totalmente privado, sem registro

□ ID do modelo : Nome : Contexto (tokens)
□------------------------------------------------ ------------------------------------------------------------------------ ------------------------
* <<CODE0> * Llama 3.3 70B * 131k * Geral *
* <<CODE1> * Llama 3.2 3B * 131k * Rápido, leve *
* <<CODE2> * Hermes 3 Llama 3.1 405B * 131k * Tarefas complexas *
* `qwen3-235b-a22b-thinking-2507` * Qwen3 235B Pensar em 131k
Instrução geral
Código 480B
* `qwen3-next-80b` * Qwen3 Next 80B * 262k * Geral
Visão
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
* `deepseek-v3.2` * DeepSeek V3.2 * 163k
* <<CODE10>* Veneza sem censura *
• `mistral-31-24b` • Venice Medium (Mistral)
Gemma 3 27B Instrução 202k Visão
* < < < CÓDIGO13>>
* `zai-org-glm-4.7` * GLM 4.7 * 202k

Modelos anônimos (10) — Via Venice Proxy

* ID do modelo * Contexto original * Características *
-----------------------------------------
* <<CODE0> * Claude Opus 4.5 * 202k * Raciocínio, visão
* <<CODE1> * Claude Sonnet 4.5 * 202k * Raciocínio, visão *
* <<CODE2> > .
* < < < CÓDIGO3>> * Códice GPT-5.2 *
* <<CODE4> * Gemini 3 Pro * 202k * Raciocínio, visão *
* <<CODE5> * Gemini 3 Flash *
* <<CODE6> * Grok 4.1 Rápido * 262k * Raciocínio, visão *
Código Grok
* Kimi K2 Thinking * 262k * Raciocínio *
□ `minimax-m21`

# # Descoberta do Modelo

OpenClaw automaticamente descobre modelos da API de Veneza quando <<CODE0> é definido. Se a API é inacessível, ela cai de volta para um catálogo estático.

O endpoint `/models` é público (sem autorização necessária para listagem), mas a inferência requer uma chave API válida.

# # Streaming & Suporte da ferramenta

Característica Suporte
------------------------------------ ----------------------------------------------------------------------
Todos os modelos
A maioria dos modelos (verifique `supportsFunctionCalling` na API)
Modelos marcados com o recurso "Vision"
O modo JSON** O modo JSON**

# # Preços

Veneza usa um sistema baseado em crédito. Verificar [venice.ai/pricing](<https://venice.ai/pricing) para as taxas correntes:

- ** Modelos privados**: Custo geralmente mais baixo
- ** Modelos anônimos**: Semelhante ao preço direto da API + pequena taxa de Veneza

# # Comparação: Veneza vs API direta

• Aspectos de Veneza (anônimo)
-------------- ---------------------------------------------------------------------
Privacidade** Metadata despojado, anonimizado
. . ** Latência** . . + 10-50ms (proxy) . .
Caracteristicas** A maioria dos recursos suportados
Tradução e Legendagem:

# # Exemplos de uso

```bash
# Use default private model
openclaw chat --model venice/llama-3.3-70b

# Use Claude via Venice (anonymized)
openclaw chat --model venice/claude-opus-45

# Use uncensored model
openclaw chat --model venice/venice-uncensored

# Use vision model with image
openclaw chat --model venice/qwen3-vl-235b-a22b

# Use coding model
openclaw chat --model venice/qwen3-coder-480b-a35b-instruct
```

# # Resolução de problemas

Tecla API não reconhecida

```bash
echo $VENICE_API_KEY
openclaw models list | grep venice
```

Certifique-se de que a chave começa com `vapi_`.

# # # Modelo não disponível

O catálogo modelo de Veneza atualiza dinamicamente. Executar <<CODE0> para ver os modelos atualmente disponíveis. Alguns modelos podem estar temporariamente offline.

Problemas de ligação

A API de Veneza está em `https://api.venice.ai/api/v1`. Certifique-se de que sua rede permite conexões HTTPS.

# # Exemplo de arquivo de configuração

```json5
{
  env: { VENICE_API_KEY: "vapi_..." },
  agents: { defaults: { model: { primary: "venice/llama-3.3-70b" } } },
  models: {
    mode: "merge",
    providers: {
      venice: {
        baseUrl: "https://api.venice.ai/api/v1",
        apiKey: "${VENICE_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "llama-3.3-70b",
            name: "Llama 3.3 70B",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 131072,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

# # Links

- [AI de Veneza] (<https://venice.ai)
- [Documentação API] (<https://docs.venice.ai)
- [Pricing] (<https://venice.ai/pricing)
- [Status] (<https://status.venice.ai)
