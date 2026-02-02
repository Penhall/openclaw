---
summary: "Hooks: event-driven automation for commands and lifecycle events"
read_when:
  - You want event-driven automation for /new, /reset, /stop, and agent lifecycle events
  - You want to build, install, or debug hooks
---

Ganchos

Hooks fornecem um sistema extensível orientado a eventos para automatizar ações em resposta a comandos e eventos de agentes. Ganchos são descobertos automaticamente a partir de diretórios e podem ser gerenciados através de comandos CLI, semelhante a como as habilidades funcionam no OpenClaw.

# # Ser Orientado

Ganchos são pequenos scripts que funcionam quando algo acontece. Existem dois tipos:

- ** Hooks** (esta página): correr dentro do Gateway quando os eventos do agente dispararem, como <<CODE0>>, <<CODE1>>, <<CODE2>>, ou eventos do ciclo de vida.
- ** Webhooks**: webhooks HTTP externos que permitem que outros sistemas desencadeiam o trabalho em OpenClaw. Veja [Webhook Hooks](<<<LINK0>>>) ou use <<CODE3>> para comandos de ajuda do Gmail.

Ganchos também podem ser empacotados dentro de plugins; veja [Plugins](<<<LINK0>>>).

Usos comuns:

- Salve um instantâneo de memória quando você reiniciar uma sessão
- Mantenha uma pista de auditoria de comandos para solução de problemas ou conformidade
- Ativar a automação de seguimento quando uma sessão começa ou termina
- Escreva arquivos na área de trabalho do agente ou chame APIs externas quando os eventos dispararem

Se você pode escrever uma pequena função TypeScript, você pode escrever um gancho. Ganchos são descobertos automaticamente, e você ativa ou desabilita-los através do CLI.

# # Visão geral

O sistema de ganchos permite que você:

- Salvar contexto de sessão na memória quando <<CODE0>> é emitido
- Registre todos os comandos para auditoria
- Ativar automações personalizadas em eventos do ciclo de vida do agente
- Extender o comportamento do Openclaw sem modificar o código central

# # Começar

Ganchos Empalhados

Naves Openclaw com quatro ganchos empacotados que são descobertos automaticamente:

- ** ** memória da sessão**: Salva o contexto de sessão para o espaço de trabalho do seu agente (padrão <<CODE0>>) quando você emite <<CODE1>
- ** ** **: Registra todos os eventos de comando para <<CODE2>
- ** o boot-md**: Executa <<CODE3>> quando o gateway começa (requer ganchos internos ativados)
- * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

Listar os ganchos disponíveis:

```bash
openclaw hooks list
```

Activar um gancho:

```bash
openclaw hooks enable session-memory
```

Verificar o estado do gancho:

```bash
openclaw hooks check
```

Obter informações detalhadas:

```bash
openclaw hooks info session-memory
```

A bordo

Durante o embarque (<<<CODE0>>), você será solicitado a ativar ganchos recomendados. O assistente descobre automaticamente ganchos elegíveis e os apresenta para seleção.

# # Descoberta de Ganchos

Ganchos são descobertos automaticamente a partir de três diretórios (por ordem de precedência):

1. ** Ganchos no espaço de trabalho**: <<CODE0>> (per- agente, precedência máxima)
2. ** Ganchos geridos**: <<CODE1>> (instalado pelo usuário, compartilhado em espaços de trabalho)
3. ** Ganchos cruzados**: <<CODE2>> (enviou com OpenClaw)

Os diretórios de gancho gerenciados podem ser um **single hook** ou um **hook pack** (diretório do pacote).

Cada gancho é um diretório contendo:

```
my-hook/
├── HOOK.md          # Metadata + documentation
└── handler.ts       # Handler implementation
```

# # Ganchos (npm/arquivos)

Hook packs são pacotes npm padrão que exportam um ou mais ganchos via <<CODE0> em
<<CODE1>>>. Instalá- los com:

```bash
openclaw hooks install <path-or-spec>
```

Exemplo <<CODE0>>:

```json
{
  "name": "@acme/my-hooks",
  "version": "0.1.0",
  "openclaw": {
    "hooks": ["./hooks/my-hook", "./hooks/other-hook"]
  }
}
```

Cada entrada aponta para uma pasta de ganchos contendo <<CODE0>> e <<CODE1>>> (ou <<CODE2>>>).
Hook packs podem enviar dependências; eles serão instalados em <<CODE3>>>>.

# # Estrutura do gancho

Hook.md Format

O arquivo <<CODE0> contém metadados em matéria frontal YAML mais documentação Markdown:

```markdown
---
name: my-hook
description: "Short description of what this hook does"
homepage: https://docs.openclaw.ai/hooks#my-hook
metadata:
  { "openclaw": { "emoji": "🔗", "events": ["command:new"], "requires": { "bins": ["node"] } } }
---

# My Hook

Detailed documentation goes here...

## What It Does

- Listens for `/new` commands
- Performs some action
- Logs the result

## Requirements

- Node.js must be installed

## Configuration

No configuration needed.
```

Campos de Metadados

O objeto <<CODE0> suporta:

- **<<<CODE0>**: Mostrar emoji para CLI (por exemplo, <<CODE1>>>)
- ** <<<CODE2>**: Array de eventos para ouvir (por exemplo, <<CODE3>>>)
- **<<<CODE4>**: Exportação nomeada para utilização (por omissão para <<CODE5>>>)
- **<<<CODE6>>**: URL da documentação
- **<<<CODE7>>**: Requisitos facultativos
- **<<<CODE8>**: Binários necessários no PATH (por exemplo, <<CODE9>>>>)
- **<<<CODE10>>**: Pelo menos um destes binários deve estar presente.
- **<<<CODE11>**: Variáveis de ambiente necessárias
- ** <<<CODE12>**: Caminhos de configuração necessários (por exemplo, <<CODE13>>>)
- **<<<CODE14>**: Plataformas necessárias (por exemplo, <<CODE15>>>>)
- **<<<CODE16>>**: Controlos de elegibilidade (booleano)
- **<<<CODE17>>**: Métodos de instalação (para ganchos agrupados: <<CODE18>>>)

Implementação do manipulador

O ficheiro <<CODE0> exporta uma função <<CODE1>>:

```typescript
import type { HookHandler } from "../../src/hooks/hooks.js";

const myHandler: HookHandler = async (event) => {
  // Only trigger on 'new' command
  if (event.type !== "command" || event.action !== "new") {
    return;
  }

  console.log(`[my-hook] New command triggered`);
  console.log(`  Session: ${event.sessionKey}`);
  console.log(`  Timestamp: ${event.timestamp.toISOString()}`);

  // Your custom logic here

  // Optionally send message to user
  event.messages.push("✨ My hook executed!");
};

export default myHandler;
```

Contexto do evento

Cada evento inclui:

```typescript
{
  type: 'command' | 'session' | 'agent' | 'gateway',
  action: string,              // e.g., 'new', 'reset', 'stop'
  sessionKey: string,          // Session identifier
  timestamp: Date,             // When the event occurred
  messages: string[],          // Push messages here to send to user
  context: {
    sessionEntry?: SessionEntry,
    sessionId?: string,
    sessionFile?: string,
    commandSource?: string,    // e.g., 'whatsapp', 'telegram'
    senderId?: string,
    workspaceDir?: string,
    bootstrapFiles?: WorkspaceBootstrapFile[],
    cfg?: OpenClawConfig
  }
}
```

# # Tipos de eventos

## # Eventos de comando

Ativado quando os comandos do agente são emitidos:

- **<<<CODE0>**: Todos os eventos de comando (ouvinte geral)
- **<<<CODE1>**: Quando <<CODE2>> o comando é emitido
- **<<<CODE3>**: Quando <<CODE4>> o comando é emitido
- ** <<<CODE5>**: Quando <<CODE6>> o comando é emitido

## # Eventos de agentes

- **<<<CODE0>**: Antes de os ficheiros de arranque do espaço de trabalho serem injectados (os cascos podem sofrer mutações <<CODE1>>>)

Eventos no portal

Ativado quando o gateway começa:

- **<<<CODE0>**: Após o início dos canais e os ganchos são carregados

## # Ganchos de Resultado de Ferramentas ( API de Plugins)

Esses ganchos não são ouvintes de fluxo de eventos; eles deixam plugins ajustar síncronamente os resultados da ferramenta antes que o OpenClaw os persista.

- **<<CODE0>>**: transformar os resultados da ferramenta antes de serem escritos para a transcrição da sessão. Deve ser síncrono; retornar a carga útil do resultado da ferramenta atualizada ou <<CODE1> para mantê-lo como está. Ver [Agent Loop] (<<<LINK0>>>).

# # Eventos futuros

Tipos de eventos planejados:

- **<<<CODE0>**: Quando uma nova sessão começa
- **<<<CODE1>>**: Quando uma sessão termina
- ** <<<CODE2>>**: Quando um agente encontra um erro
- **<<<CODE3>>**: Quando uma mensagem é enviada
- **<<<CODE4>**: Quando uma mensagem é recebida

# # Criando ganchos personalizados

# # # 1. Escolha a Localização

- ** Ganchos no espaço de trabalho** (<<<CODE0>>): Por- agente, maior precedência
- ** Ganchos geridos** (<<<CODE1>>>): Compartilhado em espaços de trabalho

# # 2. Criar estrutura de diretório

```bash
mkdir -p ~/.openclaw/hooks/my-hook
cd ~/.openclaw/hooks/my-hook
```

# # 3. Crie HOOK.Md

```markdown
---
name: my-hook
description: "Does something useful"
metadata: { "openclaw": { "emoji": "🎯", "events": ["command:new"] } }
---

# My Custom Hook

This hook does something useful when you issue `/new`.
```

## # 4. Criar manipuladores

```typescript
import type { HookHandler } from "../../src/hooks/hooks.js";

const handler: HookHandler = async (event) => {
  if (event.type !== "command" || event.action !== "new") {
    return;
  }

  console.log("[my-hook] Running!");
  // Your logic here
};

export default handler;
```

5. Activar e testar

```bash
# Verify hook is discovered
openclaw hooks list

# Enable it
openclaw hooks enable my-hook

# Restart your gateway process (menu bar app restart on macOS, or restart your dev process)

# Trigger the event
# Send /new via your messaging channel
```

Configuração

# # # Novo Formato de Configuração (Recomendado)

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "session-memory": { "enabled": true },
        "command-logger": { "enabled": false }
      }
    }
  }
}
```

Configuração Per-Hook

Ganchos podem ter configuração personalizada:

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "my-hook": {
          "enabled": true,
          "env": {
            "MY_CUSTOM_VAR": "value"
          }
        }
      }
    }
  }
}
```

Diretórios extra

Carregar ganchos de diretórios adicionais:

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "load": {
        "extraDirs": ["/path/to/more/hooks"]
      }
    }
  }
}
```

### Formato de configuração legado (ainda suportado)

O formato de configuração antigo ainda funciona para compatibilidade ao contrário:

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "handlers": [
        {
          "event": "command:new",
          "module": "./hooks/handlers/my-handler.ts",
          "export": "default"
        }
      ]
    }
  }
}
```

**Migração**: Use o novo sistema baseado em descoberta para novos ganchos. Manipuladores legados são carregados após ganchos baseados em diretórios.

# # Comandos CLI

# # Lista Ganchos

```bash
# List all hooks
openclaw hooks list

# Show only eligible hooks
openclaw hooks list --eligible

# Verbose output (show missing requirements)
openclaw hooks list --verbose

# JSON output
openclaw hooks list --json
```

Informação do Gancho

```bash
# Show detailed info about a hook
openclaw hooks info session-memory

# JSON output
openclaw hooks info session-memory --json
```

Verificar a Elegibilidade

```bash
# Show eligibility summary
openclaw hooks check

# JSON output
openclaw hooks check --json
```

Activar/Desactivar

```bash
# Enable a hook
openclaw hooks enable session-memory

# Disable a hook
openclaw hooks disable command-logger
```

# # Ganchos Ajuntados

## # memória de sessão

Salva o contexto da sessão na memória quando você emite <<CODE0>>.

** Eventos**: <<CODE0>>

** Os requisitos**: <<CODE0>> devem ser configurados

** Saída**: <<CODE0>> (padrão para <<CODE1>>)

** O que faz**:

1. Usa a entrada de sessão pré-reset para localizar a transcrição correta
2. Extrai as últimas 15 linhas de conversa
3. Usa LLM para gerar um arquivo descritivo slush
4. Salva metadados de sessão em um arquivo de memória datado

**Exemplo de saída**:

```markdown
# Session: 2026-01-16 14:30:00 UTC

- **Session Key**: agent:main:main
- **Session ID**: abc123def456
- **Source**: telegram
```

** Exemplos de nomes de arquivos**:

- <<CODE0>>
- <<CODE1>>
- <<CODE2>> (Horário de retorno se a geração da lesma falhar)

** Enable**:

```bash
openclaw hooks enable session-memory
```

### comando-logger

Regista todos os eventos de comando num ficheiro de auditoria centralizado.

** Eventos**: <<CODE0>>

**Requisitos**: Nenhum

** Saída**: <<CODE0>>

** O que faz**:

1. Captura detalhes do evento (action command, timestamp, session key, remetente ID, fonte)
2. Adiciona ao arquivo de log no formato JSONL
3. Corre silenciosamente no fundo

**Exemplo de entradas de log**:

```jsonl
{"timestamp":"2026-01-16T14:30:00.000Z","action":"new","sessionKey":"agent:main:main","senderId":"+1234567890","source":"telegram"}
{"timestamp":"2026-01-16T15:45:22.000Z","action":"stop","sessionKey":"agent:main:main","senderId":"user@example.com","source":"whatsapp"}
```

** Ver registos**:

```bash
# View recent commands
tail -n 20 ~/.openclaw/logs/commands.log

# Pretty-print with jq
cat ~/.openclaw/logs/commands.log | jq .

# Filter by action
grep '"action":"new"' ~/.openclaw/logs/commands.log | jq .
```

** Enable**:

```bash
openclaw hooks enable command-logger
```

Soul-Evil

Swaps injetados <<CODE0>> conteúdo com <<CODE1>> durante uma janela de purga ou por acaso.

** Eventos**: <<CODE0>>

**Docs**: (<<<LINK0>>)

** Saída**: Nenhum arquivo escrito; as trocas acontecem apenas na memória.

** Enable**:

```bash
openclaw hooks enable soul-evil
```

**Config**:

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "soul-evil": {
          "enabled": true,
          "file": "SOUL_EVIL.md",
          "chance": 0.1,
          "purge": { "at": "21:00", "duration": "15m" }
        }
      }
    }
  }
}
```

Boot-md

Executa <<CODE0>> quando o gateway começa (após o início dos canais).
Os ganchos internos devem ser ativados para que isto funcione.

** Eventos**: <<CODE0>>

** Os requisitos**: <<CODE0>> devem ser configurados

** O que faz**:

1. Lê <<CODE0>> do seu espaço de trabalho
2. Executa as instruções através do agente corredor
3. Envia quaisquer mensagens de saída solicitadas através da ferramenta de mensagem

** Enable**:

```bash
openclaw hooks enable boot-md
```

# # Melhores Práticas

Mantenha os manipuladores rápido

Ganchos executados durante o processamento de comando. Mantenha-os leves:

```typescript
// ✓ Good - async work, returns immediately
const handler: HookHandler = async (event) => {
  void processInBackground(event); // Fire and forget
};

// ✗ Bad - blocks command processing
const handler: HookHandler = async (event) => {
  await slowDatabaseQuery(event);
  await evenSlowerAPICall(event);
};
```

# # # Lidar com erros graciosamente

Envolva sempre operações arriscadas:

```typescript
const handler: HookHandler = async (event) => {
  try {
    await riskyOperation(event);
  } catch (err) {
    console.error("[my-handler] Failed:", err instanceof Error ? err.message : String(err));
    // Don't throw - let other handlers run
  }
};
```

# # Filtrar eventos cedo

Retorne mais cedo se o evento não for relevante:

```typescript
const handler: HookHandler = async (event) => {
  // Only handle 'new' commands
  if (event.type !== "command" || event.action !== "new") {
    return;
  }

  // Your logic here
};
```

## # Usar chaves específicas de eventos

Especificar os eventos exatos nos metadados quando possível:

```yaml
metadata: { "openclaw": { "events": ["command:new"] } } # Specific
```

Em vez de:

```yaml
metadata: { "openclaw": { "events": ["command"] } } # General - more overhead
```

# # Depuração

Activar o registo do gancho

O carregamento do gancho de logs de gateway na inicialização:

```
Registered hook: session-memory -> command:new
Registered hook: command-logger -> command
Registered hook: boot-md -> gateway:startup
```

Verifica a Descoberta

Listar todos os ganchos descobertos:

```bash
openclaw hooks list --verbose
```

# # Verifica o registo

No seu encarregado, registre quando se chama:

```typescript
const handler: HookHandler = async (event) => {
  console.log("[my-handler] Triggered:", event.type, event.action);
  // Your logic
};
```

Verificar a Elegibilidade

Verifique por que um gancho não é elegível:

```bash
openclaw hooks info my-hook
```

Procure por requisitos ausentes na saída.

Teste

Diários do Portal

Monitorar os registros de gateway para ver a execução do gancho:

```bash
# macOS
./scripts/clawlog.sh -f

# Other platforms
tail -f ~/.openclaw/gateway.log
```

Teste os ganchos diretamente

Teste seus manipuladores em isolamento:

```typescript
import { test } from "vitest";
import { createHookEvent } from "./src/hooks/hooks.js";
import myHandler from "./hooks/my-hook/handler.js";

test("my handler works", async () => {
  const event = createHookEvent("command", "new", "test-session", {
    foo: "bar",
  });

  await myHandler(event);

  // Assert side effects
});
```

# # Arquitetura

Componentes Principais

- **<<<CODE0>**: Definições de tipo
- **<<<CODE1>>**: Digitalização e carregamento de pastas
- **<<<CODE2>**: HOOK.md análise de metadados
- **<<<CODE3>>**: Verificação da elegibilidade
- **<<<CODE4>**: Relatório de estado
- **<<<CODE5>**: Carregador dinâmico de módulos
- **<<<CODE6>**: comandos CLI
- **<<<CODE7>>**: Carrega ganchos no início do gateway
- **<<<CODE8>>**: Ativa eventos de comando

# # Discovery Flow

```
Gateway startup
    ↓
Scan directories (workspace → managed → bundled)
    ↓
Parse HOOK.md files
    ↓
Check eligibility (bins, env, config, os)
    ↓
Load handlers from eligible hooks
    ↓
Register handlers for events
```

# # Fluxo de eventos

```
User sends /new
    ↓
Command validation
    ↓
Create hook event
    ↓
Trigger hook (all registered handlers)
    ↓
Command processing continues
    ↓
Session reset
```

# # Resolução de problemas

Gancho Não Descoberto

1. Verifique a estrutura do diretório:

   ```bash
   ls -la ~/.openclaw/hooks/my-hook/
   # Should show: HOOK.md, handler.ts
   ```

2. Verifique o formato HOOK.md:

   ```bash
   cat ~/.openclaw/hooks/my-hook/HOOK.md
   # Should have YAML frontmatter with name and metadata
   ```

3. Listar todos os ganchos descobertos:
   ```bash
   openclaw hooks list
   ```

Gancho Não Elegível

Requisitos de verificação:

```bash
openclaw hooks info my-hook
```

Procurar por falta:

- Binários (verifique PATH)
- Variáveis ambientais
- Valores de configuração
- Compatibilidade com o sistema operacional

Gancho Não Executar

1. Verificar o gancho está ativado:

   ```bash
   openclaw hooks list
   # Should show ✓ next to enabled hooks
   ```

2. Reinicie seu processo de gateway para que os ganchos reload.

3. Verifique registros de gateway para erros:
   ```bash
   ./scripts/clawlog.sh | grep hook
   ```

Erros no manipulador

Verificar os erros do TypeScript/import:

```bash
# Test import directly
node -e "import('./path/to/handler.ts').then(console.log)"
```

# # Guia de migração

## # Da configuração do legado à descoberta

**Antes de**:

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "handlers": [
        {
          "event": "command:new",
          "module": "./hooks/handlers/my-handler.ts"
        }
      ]
    }
  }
}
```

**Depois**:

1. Criar diretório de gancho:

   ```bash
   mkdir -p ~/.openclaw/hooks/my-hook
   mv ./hooks/handlers/my-handler.ts ~/.openclaw/hooks/my-hook/handler.ts
   ```

2. Criar HOOK.md:

   ```markdown
   ---
   name: my-hook
   description: "My custom hook"
   metadata: { "openclaw": { "emoji": "🎯", "events": ["command:new"] } }
   ---

   # My Hook

   Does something useful.
   ```

3. Actualizar a configuração:

   ```json
   {
     "hooks": {
       "internal": {
         "enabled": true,
         "entries": {
           "my-hook": { "enabled": true }
         }
       }
     }
   }
   ```

4. Verifique e reinicie seu processo de gateway:
   ```bash
   openclaw hooks list
   # Should show: 🎯 my-hook ✓
   ```

** Benefícios da migração**:

- Descoberta automática
- Gestão de CLI
- Verificação de elegibilidade
- Melhor documentação
- Estrutura consistente

# # Veja também

- [CLI Referência: ganchos](<<<LINK0>>>)
- [Bundled Hooks README] (<<<LINK1>>>)
- [Anzóis Webhook] (<<<LINK2>>>)
- [Configuração](<<<LINK3>>>)
