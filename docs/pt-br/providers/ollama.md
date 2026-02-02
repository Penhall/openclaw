---
summary: "Run OpenClaw with Ollama (local LLM runtime)"
read_when:
  - You want to run OpenClaw with local models via Ollama
  - You need Ollama setup and configuration guidance
---

# Ollama

Ollama é um tempo de execução LLM local que facilita a execução de modelos de código aberto na sua máquina. OpenClaw integra-se com a API compatível com OpenAI de Ollama e pode **auto-descobrir modelos com capacidade de ferramenta** quando você optar por `OLLAMA_API_KEY` (ou um perfil de autenticação) e não definir uma entrada explícita `models.providers.ollama`.

# # Começo rápido

1. Instale Ollama: https://olama.ai

2. Puxe um modelo:

```bash
ollama pull llama3.3
# or
ollama pull qwen2.5-coder:32b
# or
ollama pull deepseek-r1:32b
```

3. Habilite Ollama para OpenClaw (qualquer valor funciona; Ollama não requer uma chave real):

```bash
# Set environment variable
export OLLAMA_API_KEY="ollama-local"

# Or configure in your config file
openclaw config set models.providers.ollama.apiKey "ollama-local"
```

4. Use modelos Ollama:

```json5
{
  agents: {
    defaults: {
      model: { primary: "ollama/llama3.3" },
    },
  },
}
```

# # Descoberta do modelo (fornecedor implícito)

Quando você definir <<CODE0> (ou um perfil de autenticação) e ** não definir `models.providers.ollama`, OpenClaw descobre modelos da instância local de Ollama em `http://127.0.0.1:11434`:

- Consultas <<CODE0> e `/api/show`
- Mantém apenas modelos que relatam `tools` capacidade
- Marcas `reasoning` quando o modelo relata `thinking`
- Leituras <<CODE5> de <<CODE6> quando disponíveis
- Define `maxTokens` para 10× a janela de contexto
- Define todos os custos em `0`

Isso evita entradas de modelos manuais, mantendo o catálogo alinhado com as capacidades do Ollama.

Para ver quais modelos estão disponíveis:

```bash
ollama list
openclaw models list
```

Para adicionar um novo modelo, basta puxá-lo com Ollama:

```bash
ollama pull mistral
```

O novo modelo será automaticamente descoberto e disponível para uso.

Se você definir <<CODE0> explicitamente, a auto-descoberta é ignorada e você deve definir modelos manualmente (veja abaixo).

Configuração

Configuração básica (descoberta implícita)

A maneira mais simples de ativar Ollama é via variável de ambiente:

```bash
export OLLAMA_API_KEY="ollama-local"
```

## # Configuração explícita (modelos manuais)

Usar uma configuração explícita quando:

- O Ollama corre em outro host/port.
- Você quer forçar janelas de contexto específicas ou listas de modelos.
- Você quer incluir modelos que não relatem suporte de ferramentas.

```json5
{
  models: {
    providers: {
      ollama: {
        // Use a host that includes /v1 for OpenAI-compatible APIs
        baseUrl: "http://ollama-host:11434/v1",
        apiKey: "ollama-local",
        api: "openai-completions",
        models: [
          {
            id: "llama3.3",
            name: "Llama 3.3",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 8192,
            maxTokens: 8192 * 10
          }
        ]
      }
    }
  }
}
```

Se <<CODE0> for definido, você pode omitir `apiKey` na entrada do provedor e OpenClaw irá preenchê-lo para verificação de disponibilidade.

## # URL base personalizado (configuração explícita)

Se Ollama estiver rodando em uma máquina ou porta diferente (explicit config desabilita auto-descoberta, então defina modelos manualmente):

```json5
{
  models: {
    providers: {
      ollama: {
        apiKey: "ollama-local",
        baseUrl: "http://ollama-host:11434/v1",
      },
    },
  },
}
```

# # # Seleção do modelo

Uma vez configurados, todos os seus modelos Ollama estão disponíveis:

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "ollama/llama3.3",
        fallback: ["ollama/qwen2.5-coder:32b"],
      },
    },
  },
}
```

# # Avançado

Modelos raciocinantes

OpenClaw marca modelos como capazes de raciocínio quando Ollama relata `thinking` em <<CODE1>:

```bash
ollama pull deepseek-r1:32b
```

Custos do modelo

Ollama é livre e é executado localmente, então todos os custos do modelo são definidos em $0.

Janelas de contexto

Para modelos auto-descobertos, OpenClaw usa a janela de contexto reportada por Ollama quando disponível, caso contrário, é padrão `8192`. Você pode substituir `contextWindow` e `maxTokens` na configuração explícita do provedor.

# # Resolução de problemas

# # # Ollama não detectado

Certifique-se de que Ollama está em execução e que você define `OLLAMA_API_KEY` (ou um perfil de autenticação), e que você fez **not** defina uma entrada explícita `models.providers.ollama`:

```bash
ollama serve
```

E que a API está acessível:

```bash
curl http://localhost:11434/api/tags
```

# # # Nenhum modelo disponível

OpenClaw apenas auto-descobre modelos que relatam suporte de ferramenta. Se o seu modelo não estiver listado, também:

- Puxar um modelo capaz de ferramentas, ou
- Defina o modelo explicitamente em `models.providers.ollama`.

Para adicionar modelos:

```bash
ollama list  # See what's installed
ollama pull llama3.3  # Pull a model
```

Conexão recusada

Verifique se Ollama está rodando na porta correta:

```bash
# Check if Ollama is running
ps aux | grep ollama

# Or restart Ollama
ollama serve
```

# # Veja também

- [Model Providers] (</concepts/model-providers) - Visão geral de todos os fornecedores
- [Selecção de Modelos] (</concepts/models) Como escolher modelos
- [Configuração] (</gateway/configuration) - Referência de configuração completa
