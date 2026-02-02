---
summary: "Broadcast a WhatsApp message to multiple agents"
read_when:
  - Configuring broadcast groups
  - Debugging multi-agent replies in WhatsApp
status: experimental
---

# Grupos de transmissão

** Status: ** Experimental
** Versão:** Adicionado em 2026.1.9

## Visão geral

Grupos de transmissão permitem que vários agentes processem e respondam simultaneamente à mesma mensagem. Isso permite que você crie equipes de agentes especializados que trabalham juntos em um único grupo WhatsApp ou DM — todos usando um número de telefone.

Âmbito atual: **WhatsApp somente** (canal web).

Os grupos de transmissão são avaliados após listas de canais e regras de ativação do grupo. Nos grupos WhatsApp, isso significa que transmissões acontecem quando o OpenClaw normalmente responderia (por exemplo: na menção, dependendo das configurações do seu grupo).

## Casos de uso

### 1. Equipas de Agentes Especializados

Implantar múltiplos agentes com responsabilidades atômicas focadas:

```
Group: "Development Team"
Agents:
  - CodeReviewer (reviews code snippets)
  - DocumentationBot (generates docs)
  - SecurityAuditor (checks for vulnerabilities)
  - TestGenerator (suggests test cases)
```

Cada agente processa a mesma mensagem e proporciona sua perspectiva especializada.

### 2. Suporte multi-língua

```
Group: "International Support"
Agents:
  - Agent_EN (responds in English)
  - Agent_DE (responds in German)
  - Agent_ES (responds in Spanish)
```

3. Fluxos de Trabalho de Garantia de Qualidade

```
Group: "Customer Support"
Agents:
  - SupportAgent (provides answer)
  - QAAgent (reviews quality, only responds if issues found)
```

4. Automação de tarefas

```
Group: "Project Management"
Agents:
  - TaskTracker (updates task database)
  - TimeLogger (logs time spent)
  - ReportGenerator (creates summaries)
```

Configuração

Configuração Básica

Adicionar uma secção`broadcast`de topo (ao lado do`bindings`. As chaves são IDs do WhatsApp:

- chats de grupo: grupo JID (por exemplo,`120363403215116621@g.us`
- DM: Número de telefone E.164 (por exemplo,`+15551234567`

```json
{
  "broadcast": {
    "120363403215116621@g.us": ["alfred", "baerbel", "assistant3"]
  }
}
```

**Resultado:** Quando o Openclaw responder neste chat, ele executará todos os três agentes.

## # Estratégia de processamento

Controle como agentes processam mensagens:

Paralelo (Padrão)

Todos os agentes processam simultaneamente:

```json
{
  "broadcast": {
    "strategy": "parallel",
    "120363403215116621@g.us": ["alfred", "baerbel"]
  }
}
```

Sequencial

Os agentes processam em ordem (espera-se o final anterior):

```json
{
  "broadcast": {
    "strategy": "sequential",
    "120363403215116621@g.us": ["alfred", "baerbel"]
  }
}
```

Exemplo completo

```json
{
  "agents": {
    "list": [
      {
        "id": "code-reviewer",
        "name": "Code Reviewer",
        "workspace": "/path/to/code-reviewer",
        "sandbox": { "mode": "all" }
      },
      {
        "id": "security-auditor",
        "name": "Security Auditor",
        "workspace": "/path/to/security-auditor",
        "sandbox": { "mode": "all" }
      },
      {
        "id": "docs-generator",
        "name": "Documentation Generator",
        "workspace": "/path/to/docs-generator",
        "sandbox": { "mode": "all" }
      }
    ]
  },
  "broadcast": {
    "strategy": "parallel",
    "120363403215116621@g.us": ["code-reviewer", "security-auditor", "docs-generator"],
    "120363424282127706@g.us": ["support-en", "support-de"],
    "+15555550123": ["assistant", "logger"]
  }
}
```

## Como Funciona

## Fluxo de mensagens

1. ** Mensagem recebida** chega em um grupo WhatsApp
2. **Verificação da transmissão**: Verificação do sistema se o ID dos pares está em`broadcast`3. **Se na lista de difusão**:
- Todos os agentes listados processam a mensagem
- Cada agente tem sua própria chave de sessão e contexto isolado
- Os agentes processam em paralelo (padrão) ou sequencialmente
4. **Se não estiver na lista de difusão**:
- Aplicação de roteamento normal (primeira ligação)

Nota: os grupos de transmissão não ignoram as listas de licenças de canal ou as regras de ativação de grupo (menciamentos/comandos/etc). Eles só mudam  que agentes executam  quando uma mensagem é elegível para processamento.

Isolamento da Sessão

Cada agente de um grupo de transmissão mantém-se completamente separado:

- ** Teclas de selecção** `agent:alfred:whatsapp:group:120363...`vs`agent:baerbel:whatsapp:group:120363...`
- ** Histórico de conversa** (o agente não vê as mensagens de outros agentes)
- ** Espaço de trabalho** (separar sandboxes se configurado)
- **Acesso à ferramenta** (diferentes listas de permissão/negação)
- ** Memória/contexto** (IDENTITY.md separado, SOUL.md, etc.)
- **Group context buffer** (mensagens de grupo recentes usadas para o contexto) é compartilhado por par, então todos os agentes de transmissão veem o mesmo contexto quando acionados

Isto permite que cada agente tenha:

- Personalidades diferentes
- Acesso a ferramentas diferentes (por exemplo, somente leitura vs leitura- escrita)
- Modelos diferentes (por exemplo, opus vs soneto)
- Diferentes habilidades instaladas

Exemplo: Sessões Isoladas

No grupo`120363403215116621@g.us`com agentes`["alfred", "baerbel"]`:

**Contexto de Alfredo:**

```
Session: agent:alfred:whatsapp:group:120363403215116621@g.us
History: [user message, alfred's previous responses]
Workspace: /Users/pascal/openclaw-alfred/
Tools: read, write, exec
```

** Contexto de Bärbel:**

```
Session: agent:baerbel:whatsapp:group:120363403215116621@g.us
History: [user message, baerbel's previous responses]
Workspace: /Users/pascal/openclaw-baerbel/
Tools: read only
```

## Melhores Práticas

## 1. Mantenha os agentes focados

Designar cada agente com uma única responsabilidade clara:

```json
{
  "broadcast": {
    "DEV_GROUP": ["formatter", "linter", "tester"]
  }
}
```

Bom:** Cada agente tem um trabalho
文 ** Mau:** Um agente genérico "dev-helper"

## # 2. Use Nomes descritivos

Deixe claro o que cada agente faz:

```json
{
  "agents": {
    "security-scanner": { "name": "Security Scanner" },
    "code-formatter": { "name": "Code Formatter" },
    "test-generator": { "name": "Test Generator" }
  }
}
```

### 3. Configurar o acesso diferente da ferramenta

Dê aos agentes apenas as ferramentas de que necessitam:

```json
{
  "agents": {
    "reviewer": {
      "tools": { "allow": ["read", "exec"] } // Read-only
    },
    "fixer": {
      "tools": { "allow": ["read", "write", "edit", "exec"] } // Read-write
    }
  }
}
```

## 4. Monitor de desempenho

Com muitos agentes, considere:

- Usando`"strategy": "parallel"`(padrão) para velocidade
- Limitando grupos de transmissão a 5-10 agentes
- Usando modelos mais rápidos para agentes mais simples

### 5. Lidar com falhas graciosamente

Os agentes falham de forma independente. O erro de um agente não bloqueia os outros:

```
Message → [Agent A ✓, Agent B ✗ error, Agent C ✓]
Result: Agent A and C respond, Agent B logs error
```

## Compatibilidade

Provedores

Os grupos de transmissão trabalham atualmente com:

- □ WhatsApp (implementado)
- Telegrama (planejado)
- Discórdia (planejada)
- Slack (planeado)

Roteamento

Grupos de transmissão trabalham ao lado do roteamento existente:

```json
{
  "bindings": [
    {
      "match": { "channel": "whatsapp", "peer": { "kind": "group", "id": "GROUP_A" } },
      "agentId": "alfred"
    }
  ],
  "broadcast": {
    "GROUP_B": ["agent1", "agent2"]
  }
}
```

-`GROUP_A`: Só o Alfred responde (roteamento normal)
-`GROUP_B`: agente1 e agente2 respondem (transmissão)

**Precedência:**`broadcast`tem prioridade sobre`bindings`.

## Resolução de problemas

Agentes que não respondem

** Verificar:**

1. IDs de agente existem em`agents.list`2. Formato de identificação de pares está correto (por exemplo,`120363403215116621@g.us`
3. Os agentes não estão em listas de negação

**Depurar:**

```bash
tail -f ~/.openclaw/logs/gateway.log | grep broadcast
```

## Apenas um agente a responder

**Causa:** O ID dos pares pode estar em`bindings`mas não em`broadcast`.

**Fix:** Adicionar à configuração da transmissão ou remover das ligações.

Problemas de desempenho

** Se lento com muitos agentes:**

- Reduzir o número de agentes por grupo
- Use modelos mais leves (sonnet em vez de opus)
- Verifique a hora de inicialização da sandbox

## Exemplos

Exemplo 1: Equipe de Revisão de Código

```json
{
  "broadcast": {
    "strategy": "parallel",
    "120363403215116621@g.us": [
      "code-formatter",
      "security-scanner",
      "test-coverage",
      "docs-checker"
    ]
  },
  "agents": {
    "list": [
      {
        "id": "code-formatter",
        "workspace": "~/agents/formatter",
        "tools": { "allow": ["read", "write"] }
      },
      {
        "id": "security-scanner",
        "workspace": "~/agents/security",
        "tools": { "allow": ["read", "exec"] }
      },
      {
        "id": "test-coverage",
        "workspace": "~/agents/testing",
        "tools": { "allow": ["read", "exec"] }
      },
      { "id": "docs-checker", "workspace": "~/agents/docs", "tools": { "allow": ["read"] } }
    ]
  }
}
```

**O usuário envia:** Excerto de código
**Respostas: **

- formatação de código: "Indentação corrigida e sugestões de tipo adicionadas"
- escaneador de segurança: "Habilidade de injeção SQL na linha 12"
- cobertura de teste: "A cobertura é 45%, falta testes para casos de erro"
- docs-checker: "Missing docstring for function`process_data`"

Exemplo 2: Suporte multilíngue

```json
{
  "broadcast": {
    "strategy": "sequential",
    "+15555550123": ["detect-language", "translator-en", "translator-de"]
  },
  "agents": {
    "list": [
      { "id": "detect-language", "workspace": "~/agents/lang-detect" },
      { "id": "translator-en", "workspace": "~/agents/translate-en" },
      { "id": "translator-de", "workspace": "~/agents/translate-de" }
    ]
  }
}
```

## Referência da API

Esquema de configuração

```typescript
interface OpenClawConfig {
  broadcast?: {
    strategy?: "parallel" | "sequential";
    [peerId: string]: string[];
  };
}
```

Campos

-`strategy`(opcional): Como processar agentes
-`"parallel"`(padrão): Todos os agentes processam simultaneamente
-`"sequential"`: Os agentes processam em ordem de matriz
-`[peerId]`: Grupo WhatsApp JID, número E.164 ou outra identificação por pares
- Valor: Array de IDs de agente que devem processar mensagens

## Limitações

1. **Agentes máximos:** Sem limite rígido, mas mais de 10 agentes podem ser lentos
2. **Contexto compartilhado:** Os agentes não vêem as respostas uns dos outros (por design)
3. ** Ordem da mensagem: ** Respostas paralelas podem chegar em qualquer ordem
4. ** Limites de taxa: ** Todos os agentes contam para limites de taxa WhatsApp

## Melhorias futuras

Características planeadas:

- [ ] Modo de contexto compartilhado (agentes veem as respostas uns dos outros)
- [ ] Coordenação do agente (agentes podem sinalizar uns aos outros)
- [ ] Seleção de agentes dinâmicos (escolha de agentes com base no conteúdo da mensagem)
- Prioridades do agente (alguns agentes respondem antes dos outros)

## Veja também

- [Configuração Multi-Agente] /multi-agent-sandbox-tools
/concepts/channel-routing
/concepts/sessions
