---
summary: "Per-agent sandbox + tool restrictions, precedence, and examples"
title: Multi-Agent Sandbox & Tools
read_when: "You want per-agent sandboxing or per-agent tool allow/deny policies in a multi-agent gateway."
status: active
---

# Multi-Agent Sandbox & Configuração de Ferramentas

# # Visão geral

Cada agente em uma configuração multi-agente agora pode ter o seu próprio:

- ** Configuração da caixa de areia** (<<<CODE0>> substitui <<CODE1>>)
- ** Restrições da ferramenta** (<<<<CODE2> / <<CODE3>>>, mais <<CODE4>>)

Isso permite que você execute vários agentes com diferentes perfis de segurança:

- Assistente pessoal com acesso total
- Família/agentes de trabalho com ferramentas restritas
- Agentes voltados para o público em caixas de areia

<<CODE0>> pertence a <<CODE1>> (global ou por agente) e é executado uma vez
quando o recipiente é criado.

Auth é por agente: cada agente lê do seu próprio <<CODE0>> auth store em:

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

As credenciais não são ** partilhadas entre agentes. Nunca reutilize <<CODE0>> entre os agentes.
Se você quiser compartilhar créditos, copie <<CODE1>> para o outro agente <<CODE2>>.

Para saber como o sandboxing se comporta em tempo de execução, consulte [Sandboxing] (<<<LINK0>>>).
Para depuração “por que isso está bloqueado?”, consulte [Sandbox vs Tool Policy vs Elevated](<<LINK1>>>) e <<CODE0>>>.

---

# # Exemplos de configuração

Exemplo 1: Agente pessoal + restrito da família

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "name": "Personal Assistant",
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" }
      },
      {
        "id": "family",
        "name": "Family Bot",
        "workspace": "~/.openclaw/workspace-family",
        "sandbox": {
          "mode": "all",
          "scope": "agent"
        },
        "tools": {
          "allow": ["read"],
          "deny": ["exec", "write", "edit", "apply_patch", "process", "browser"]
        }
      }
    ]
  },
  "bindings": [
    {
      "agentId": "family",
      "match": {
        "provider": "whatsapp",
        "accountId": "*",
        "peer": {
          "kind": "group",
          "id": "120363424282127706@g.us"
        }
      }
    }
  ]
}
```

**Resultado:**

- <<CODE0> agente: roda no host, acesso completo à ferramenta
- <<CODE1> agente: Funciona no Docker (um recipiente por agente), apenas <<CODE2> ferramenta

---

Exemplo 2: Agente de trabalho com caixa de areia compartilhada

```json
{
  "agents": {
    "list": [
      {
        "id": "personal",
        "workspace": "~/.openclaw/workspace-personal",
        "sandbox": { "mode": "off" }
      },
      {
        "id": "work",
        "workspace": "~/.openclaw/workspace-work",
        "sandbox": {
          "mode": "all",
          "scope": "shared",
          "workspaceRoot": "/tmp/work-sandboxes"
        },
        "tools": {
          "allow": ["read", "write", "apply_patch", "exec"],
          "deny": ["browser", "gateway", "discord"]
        }
      }
    ]
  }
}
```

---

### Exemplo 2b: Perfil de codificação global + agente somente para mensagens

```json
{
  "tools": { "profile": "coding" },
  "agents": {
    "list": [
      {
        "id": "support",
        "tools": { "profile": "messaging", "allow": ["slack"] }
      }
    ]
  }
}
```

**Resultado:**

- agentes padrão obter ferramentas de codificação
- <<CODE0> agente é apenas mensagens (+ ferramenta Slack)

---

Exemplo 3: Diferentes modos de caixa de areia por agente

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main", // Global default
        "scope": "session"
      }
    },
    "list": [
      {
        "id": "main",
        "workspace": "~/.openclaw/workspace",
        "sandbox": {
          "mode": "off" // Override: main never sandboxed
        }
      },
      {
        "id": "public",
        "workspace": "~/.openclaw/workspace-public",
        "sandbox": {
          "mode": "all", // Override: public always sandboxed
          "scope": "agent"
        },
        "tools": {
          "allow": ["read"],
          "deny": ["exec", "write", "edit", "apply_patch"]
        }
      }
    ]
  }
}
```

---

# # Precedência de configuração

Quando tanto global (<<CODE0>>) como específico do agente (<<CODE1>>>) as configurações existem:

Configuração da Caixa de Areia

Configurações específicas do agente sobrepõem-se ao global:

```
agents.list[].sandbox.mode > agents.defaults.sandbox.mode
agents.list[].sandbox.scope > agents.defaults.sandbox.scope
agents.list[].sandbox.workspaceRoot > agents.defaults.sandbox.workspaceRoot
agents.list[].sandbox.workspaceAccess > agents.defaults.sandbox.workspaceAccess
agents.list[].sandbox.docker.* > agents.defaults.sandbox.docker.*
agents.list[].sandbox.browser.* > agents.defaults.sandbox.browser.*
agents.list[].sandbox.prune.* > agents.defaults.sandbox.prune.*
```

**Notas:**

- <<CODE0>> substitui <<CODE1>> por esse agente (ignorado quando o escopo da caixa de areia resolve <<CODE2>>>).

Restrições de Ferramentas

A ordem de filtragem é:

1. ** Perfil da ferramenta** (<<<CODE0> ou <<CODE1>>)
2. ** Perfil da ferramenta fornecido** (<<<CODE2>> ou <<CODE3>>>)
3. **Política global da ferramenta** (<<<CODE4>>/ <<CODE5>>)
4. **Política da ferramenta do fornecedor** (<<<CODE6>>>)
5. **Política de ferramenta específica do agente** (<<<CODE7>>>)
6. **Política do fornecedor de agentes** (<<<CODE8>>>)
7. ** Política da ferramenta da caixa de areia** (<<<CODE9>> ou <<CODE10>>)
8. ** Política de ferramentas de subagentes** (<<<CODE11>>, se aplicável)

Cada nível pode restringir ainda mais as ferramentas, mas não pode conceder ferramentas negadas de níveis anteriores.
Se <<CODE0>> for definido, substitui <<CODE1>> por esse agente.
Se <<CODE2> for definido, ele substitui <<CODE3>> por esse agente.
As chaves da ferramenta do fornecedor aceitam tanto <<CODE4>> (por exemplo, <<CODE5>>>) como <<CODE6>> (por exemplo, <<CODE7>>>>>).

Grupos de ferramentas (shorthands)

Políticas de ferramentas (global, agente, sandbox) suportam <<CODE0> entradas que se expandem para múltiplas ferramentas de concreto:

- <<CODE0>>: <<CODE1>>, <<CODE2>>, <<CODE3>>
- <<CODE4>>: <<CODE5>>, <<CODE6>>, <<CODE7>>, <<CODE8>
- <<CODE9>>: <<CODE10>>, <<CODE11>>, <<CODE12>>, <<CODE13>>, <<CODE14>>
- <<CODE15>>: <<CODE16>>, <<CODE17>>
- <<CODE18>>: <<CODE19>>, <<CODE20>>
- <<CODE21>>: <<CODE22>>>, <<CODE23>>
- <<CODE24>>: <<CODE25>>
- <<CODE26>>: <<CODE27>>
- <<CODE28>>: todas as ferramentas OpenClaw incorporadas (exclui plugins de provedores)

Modo Elevado

<<CODE0> é a linha de base global (sender-based allowlist). <<CODE1> pode restringir ainda mais elevada para agentes específicos (ambos devem permitir).

Padrões de atenuação:

- Negar <<CODE0>> para agentes não confiáveis (<<CODE1>>>)
- Evite listar remetentes que encaminham para agentes restritos
- Desabilitar elevado globalmente (<<<CODE2>>) se você só quer execução sandboxed
- Desactivar valores elevados por agente (<<< HTML3>>>>) para perfis sensíveis

---

# # Migração de Agente Único

**Antes (agente único):**

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.openclaw/workspace",
      "sandbox": {
        "mode": "non-main"
      }
    }
  },
  "tools": {
    "sandbox": {
      "tools": {
        "allow": ["read", "write", "apply_patch", "exec"],
        "deny": []
      }
    }
  }
}
```

** Depois (multi-agente com diferentes perfis):**

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" }
      }
    ]
  }
}
```

O legado <<CODE0>>configurações são migradas por <<CODE1>>; preferem <<CODE2>> + <<CODE3> em andamento.

---

# # Exemplos de restrição de ferramentas

Agente apenas para leitura

```json
{
  "tools": {
    "allow": ["read"],
    "deny": ["exec", "write", "edit", "apply_patch", "process"]
  }
}
```

### Agente de Execução Seguro (sem modificações de ficheiros)

```json
{
  "tools": {
    "allow": ["read", "exec", "process"],
    "deny": ["write", "edit", "apply_patch", "browser", "gateway"]
  }
}
```

# # Agente Só de Comunicação

```json
{
  "tools": {
    "allow": ["sessions_list", "sessions_send", "sessions_history", "session_status"],
    "deny": ["exec", "write", "edit", "apply_patch", "read", "browser"]
  }
}
```

---

# # Pitfall comum: "non-main"

<<CODE0> é baseado em <<CODE1>> (padrão <<CODE2>>),
Não a identificação do agente. Sessões de grupo/canal sempre têm suas próprias chaves, então eles
são tratados como não principais e serão sandboxed. Se queres que um agente nunca
sandbox, definido <<CODE3>>>>.

---

Teste

Depois de configurar sandbox multi-agente e ferramentas:

1. **Verificar a resolução do agente:**

   ```exec
   openclaw agents list --bindings
   ```

2. **Verify sandbox containers:**

   ```exec
   docker ps --filter "name=openclaw-sbx-"
   ```

3. ** Restrições da ferramenta de teste:**
- Enviar uma mensagem exigindo ferramentas restritas
- Verificar que o agente não pode usar ferramentas negadas

4. **Monitor logs:**
   ```exec
   tail -f "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/logs/gateway.log" | grep -E "routing|sandbox|tools"
   ```

---

# # Resolução de problemas

## # Agente que não é sandboxed apesar de <<CODE0>>

- Verifique se há um global <<CODE0>> que o sobreponha
- A configuração específica do agente tem precedência, assim definido <<CODE1>>

### Ferramentas ainda disponíveis apesar da lista negada

- Verifique a ordem de filtragem da ferramenta: global → agente → sandbox → subagente
- Cada nível só pode restringir ainda mais, não conceder de volta
- Verificar com registos: <<CODE0>>>

# # # Container não isolado por agente

- Definir <<CODE0>> na configuração da sandbox específica do agente
- O padrão é <<CODE1>> que cria um recipiente por sessão

---

# # Veja também

- [Roteamento Multi-Agente] (<<<LINK0>>>)
- [Configuração da caixa de areia] (<<<LINK1>>>)
- [Gestão de Sessão] (<<< HTML2>>>>)
