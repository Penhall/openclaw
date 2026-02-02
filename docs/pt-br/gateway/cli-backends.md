---
summary: "CLI backends: text-only fallback via local AI CLIs"
read_when:
  - You want a reliable fallback when API providers fail
  - You are running Claude Code CLI or other local AI CLIs and want to reuse them
  - You need a text-only, tool-free path that still supports sessions and images
---

# Infra-estruturas CLI (fallback runtime)

OpenClaw pode executar ** CLIs de IA locais** como um backback ** somente texto** quando os provedores de API estão em baixo,
taxa limitada, ou temporariamente mau comportamento. Isto é intencionalmente conservador:

- **As ferramentas estão desactivadas** (sem chamadas de ferramentas).
- **Texto em → texto para fora** (confiante).
- ** As sessões são suportadas** (então, as voltas de seguimento permanecem coerentes).
- **Imagens podem ser passadas através de** se o CLI aceita caminhos de imagem.

Este é projetado como uma rede de segurança ** ao invés de um caminho primário. Use-o quando você
quer respostas de texto “sempre funciona” sem depender de APIs externas.

# # Início rápido amigável para principiantes

Você pode usar Claude Code CLI **sem qualquer configuração** (OpenClaw envia um padrão embutido):

```bash
openclaw agent --message "hi" --model claude-cli/opus-4.5
```

Codex CLI também funciona fora da caixa:

```bash
openclaw agent --message "hi" --model codex-cli/gpt-5.2-codex
```

Se o seu gateway é executado sob lançado/systemd e PATH é mínimo, adicione apenas o
caminho do comando:

```json5
{
  agents: {
    defaults: {
      cliBackends: {
        "claude-cli": {
          command: "/opt/homebrew/bin/claude",
        },
      },
    },
  },
}
```

É isso. Sem chaves, nenhuma configuração de autenticação extra necessária além do próprio CLI.

# # Usando-o como um retrocesso

Adicione uma infra- estrutura CLI à sua lista de retrocessos para que ela só seja executada quando os modelos primários falharem:

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-opus-4-5",
        fallbacks: ["claude-cli/opus-4.5"],
      },
      models: {
        "anthropic/claude-opus-4-5": { alias: "Opus" },
        "claude-cli/opus-4.5": {},
      },
    },
  },
}
```

Notas:

- Se utilizar <<CODE0> (allowlist), deve incluir <<CODE1>>>.
- Se o provedor principal falhar (auth, limites de taxa, timeouts), OpenClaw irá
Tente a infra-estrutura CLI em seguida.

# # Visão geral da configuração

Todas as infra-estruturas CLI vivem sob:

```
agents.defaults.cliBackends
```

Cada entrada é chaveada por um **provider id** (por exemplo, <<CODE0>>, <<CODE1>>).
O ID do provedor torna-se o lado esquerdo do seu modelo ref:

```
<provider>/<model>
```

## # Configuração do exemplo

```json5
{
  agents: {
    defaults: {
      cliBackends: {
        "claude-cli": {
          command: "/opt/homebrew/bin/claude",
        },
        "my-cli": {
          command: "my-cli",
          args: ["--json"],
          output: "json",
          input: "arg",
          modelArg: "--model",
          modelAliases: {
            "claude-opus-4-5": "opus",
            "claude-sonnet-4-5": "sonnet",
          },
          sessionArg: "--session",
          sessionMode: "existing",
          sessionIdFields: ["session_id", "conversation_id"],
          systemPromptArg: "--system",
          systemPromptWhen: "first",
          imageArg: "--image",
          imageMode: "repeat",
          serialize: true,
        },
      },
    },
  },
}
```

# # Como funciona

1. **Seleciona uma infra-estrutura** com base no prefixo do provedor (<<CODE0>>>).
2. **Compila um prompt de sistema** usando o mesmo prompt OpenClaw + contexto de espaço de trabalho.
3. **Executa o CLI** com um ID de sessão (se suportado) para que o histórico permaneça consistente.
4. **Parses output** (JSON ou texto simples) e retorna o texto final.
5. **Persists session ids** por backend, por isso os follow-ups reutilizam a mesma sessão CLI.

# # Sessãos

- Se o CLI suportar sessões, definir <<CODE0>> (por ex. <<CODE1>>) ou
<<CODE2>> (placeholder <<CODE3>>>) quando o ID precisa de ser inserido
em várias bandeiras.
- Se o CLI usar um subcomando **resume** com diferentes bandeiras, definir
<<CODE4> (substitui <<CODE5> ao retomar) e opcionalmente <<CODE6>
(para currículos não-JSON).
- <<CODE7>>:
- <<CODE8>>: enviar sempre um ID de sessão (novo UUID se nenhum armazenado).
- <<CODE9>>: só enviar um ID de sessão se um foi armazenado antes.
- <<CODE10>>: nunca envie um ID de sessão.

# # Imagens (passagem)

Se o seu CLI aceitar caminhos de imagem, defina <<CODE0>>:

```json5
imageArg: "--image",
imageMode: "repeat"
```

OpenClaw irá gravar imagens base64 para arquivos temporários. Se <<CODE0>> for definido, os
caminhos são passados como Args CLI. Se <<CODE1> estiver faltando, OpenClaw adiciona o
os caminhos dos ficheiros para o prompt (injecção do local), que é suficiente para que os
carregar arquivos locais de caminhos simples (comportamento CLI do Claude Code).

# # Entradas / saídas

- <<CODE0>> (padrão) tenta processar JSON e extrair texto + id de sessão.
- <<CODE1>> analisa fluxos JSONL (Codex CLI <<CODE2>>) e extrai
última mensagem do agente mais <<CODE3>> quando presente.
- <<CODE4> trata o stdout como resposta final.

Modos de entrada:

- <<CODE0> (padrão) passa o prompt como o último arg CLI.
- <<CODE1> envia o prompt via stdin.
- Se o prompt for muito longo e <<CODE2> for definido, stdin é utilizado.

# # Predefinições (compiladas)

OpenClaw envia um padrão para <<CODE0>>:

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>
- <<CODE3>>
- <<CODE4>>
- <<CODE5>>
- <<CODE6>>
- <<CODE7>>

OpenClaw também envia um padrão para <<CODE0>>:

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>
- <<CODE3>>
- <<CODE4>>
- <<CODE5>>
- <<CODE6>>
- <<CODE7>>

Substituir apenas se necessário (comum: absoluto <<CODE0>> caminho).

# # Limitações

- ** Nenhuma ferramenta OpenClaw** (a infraestrutura CLI nunca recebe chamadas de ferramenta). Alguns CLIs
pode ainda executar o seu próprio agente ferramenta.
- ** Nenhum streaming** (a saída CLI é coletada então retornada).
- **As saídas estruturadas** dependem do formato JSON do CLI.
- ** Sessões CLI do Codex** retomar via saída de texto (sem JSONL), que é menos
estruturado do que a execução inicial <<CODE0>>. Sessões Openclaw ainda funcionam
Normalmente.

# # Resolução de problemas

- ** CLI não encontrado**: definido <<CODE0>> para um caminho completo.
- **Nome do modelo errado**: use <<CODE1>> para mapear <<CODE2>> → Modelo CLI.
- ** Não existe continuidade de sessão**: assegurar que <<CODE3>> é definido e <<CODE4>> não é definido
<<CODE5>> (Codex CLI atualmente não pode retomar com saída JSON).
- **Imagens ignoradas**: set <<CODE6>> (e verificar CLI suporta caminhos de arquivos).
