# Pi Integração Arquitetura

Este documento descreve como OpenClaw se integra com [pi-coding-agent](<<<LINK0>>) e seus pacotes de irmãos (<<CODE0>>>, <<CODE1>>, <<CODE2>>>) para alimentar suas capacidades de agente de IA.

# # Visão geral

OpenClaw usa o pi SDK para incorporar um agente de codificação de IA em sua arquitetura de gateway de mensagens. Em vez de gerar pi como um subprocesso ou usando o modo RPC, OpenClaw importa diretamente e instancia pi's <<CODE0>> via <<CODE1>>. Esta abordagem incorporada fornece:

- Controle total do ciclo de vida da sessão e manipulação de eventos
- Injecção personalizada da ferramenta (mensagem, caixa de areia, acções específicas do canal)
- Personalização rápida do sistema por canal/contexto
- Persistência de sessão com suporte a ramificação/compactação
- Rotação de perfil de autenticação multi-conta com failover
- Comutação do modelo diagnóstico do fornecedor

# # Dependências do pacote

```json
{
  "@mariozechner/pi-agent-core": "0.49.3",
  "@mariozechner/pi-ai": "0.49.3",
  "@mariozechner/pi-coding-agent": "0.49.3",
  "@mariozechner/pi-tui": "0.49.3"
}
```

Pacote
----------------- -----------------------------------------------------------------------------------------------------------------------------------------------------
* < <<CODE0>>
* < <<CODE3>> Tipos
* < <<CODE5>> * SDK de alto nível: <<CODE6>>>, <<CODE7>>, <<CODE8>>, <<CODE9>>, ferramentas integradas
□ < <<CODE10>>

# # Estrutura do arquivo

```
src/agents/
├── pi-embedded-runner.ts          # Re-exports from pi-embedded-runner/
├── pi-embedded-runner/
│   ├── run.ts                     # Main entry: runEmbeddedPiAgent()
│   ├── run/
│   │   ├── attempt.ts             # Single attempt logic with session setup
│   │   ├── params.ts              # RunEmbeddedPiAgentParams type
│   │   ├── payloads.ts            # Build response payloads from run results
│   │   ├── images.ts              # Vision model image injection
│   │   └── types.ts               # EmbeddedRunAttemptResult
│   ├── abort.ts                   # Abort error detection
│   ├── cache-ttl.ts               # Cache TTL tracking for context pruning
│   ├── compact.ts                 # Manual/auto compaction logic
│   ├── extensions.ts              # Load pi extensions for embedded runs
│   ├── extra-params.ts            # Provider-specific stream params
│   ├── google.ts                  # Google/Gemini turn ordering fixes
│   ├── history.ts                 # History limiting (DM vs group)
│   ├── lanes.ts                   # Session/global command lanes
│   ├── logger.ts                  # Subsystem logger
│   ├── model.ts                   # Model resolution via ModelRegistry
│   ├── runs.ts                    # Active run tracking, abort, queue
│   ├── sandbox-info.ts            # Sandbox info for system prompt
│   ├── session-manager-cache.ts   # SessionManager instance caching
│   ├── session-manager-init.ts    # Session file initialization
│   ├── system-prompt.ts           # System prompt builder
│   ├── tool-split.ts              # Split tools into builtIn vs custom
│   ├── types.ts                   # EmbeddedPiAgentMeta, EmbeddedPiRunResult
│   └── utils.ts                   # ThinkLevel mapping, error description
├── pi-embedded-subscribe.ts       # Session event subscription/dispatch
├── pi-embedded-subscribe.types.ts # SubscribeEmbeddedPiSessionParams
├── pi-embedded-subscribe.handlers.ts # Event handler factory
├── pi-embedded-subscribe.handlers.lifecycle.ts
├── pi-embedded-subscribe.handlers.types.ts
├── pi-embedded-block-chunker.ts   # Streaming block reply chunking
├── pi-embedded-messaging.ts       # Messaging tool sent tracking
├── pi-embedded-helpers.ts         # Error classification, turn validation
├── pi-embedded-helpers/           # Helper modules
├── pi-embedded-utils.ts           # Formatting utilities
├── pi-tools.ts                    # createOpenClawCodingTools()
├── pi-tools.abort.ts              # AbortSignal wrapping for tools
├── pi-tools.policy.ts             # Tool allowlist/denylist policy
├── pi-tools.read.ts               # Read tool customizations
├── pi-tools.schema.ts             # Tool schema normalization
├── pi-tools.types.ts              # AnyAgentTool type alias
├── pi-tool-definition-adapter.ts  # AgentTool -> ToolDefinition adapter
├── pi-settings.ts                 # Settings overrides
├── pi-extensions/                 # Custom pi extensions
│   ├── compaction-safeguard.ts    # Safeguard extension
│   ├── compaction-safeguard-runtime.ts
│   ├── context-pruning.ts         # Cache-TTL context pruning extension
│   └── context-pruning/
├── model-auth.ts                  # Auth profile resolution
├── auth-profiles.ts               # Profile store, cooldown, failover
├── model-selection.ts             # Default model resolution
├── models-config.ts               # models.json generation
├── model-catalog.ts               # Model catalog cache
├── context-window-guard.ts        # Context window validation
├── failover-error.ts              # FailoverError class
├── defaults.ts                    # DEFAULT_PROVIDER, DEFAULT_MODEL
├── system-prompt.ts               # buildAgentSystemPrompt()
├── system-prompt-params.ts        # System prompt parameter resolution
├── system-prompt-report.ts        # Debug report generation
├── tool-summaries.ts              # Tool description summaries
├── tool-policy.ts                 # Tool policy resolution
├── transcript-policy.ts           # Transcript validation policy
├── skills.ts                      # Skill snapshot/prompt building
├── skills/                        # Skill subsystem
├── sandbox.ts                     # Sandbox context resolution
├── sandbox/                       # Sandbox subsystem
├── channel-tools.ts               # Channel-specific tool injection
├── openclaw-tools.ts              # OpenClaw-specific tools
├── bash-tools.ts                  # exec/process tools
├── apply-patch.ts                 # apply_patch tool (OpenAI)
├── tools/                         # Individual tool implementations
│   ├── browser-tool.ts
│   ├── canvas-tool.ts
│   ├── cron-tool.ts
│   ├── discord-actions*.ts
│   ├── gateway-tool.ts
│   ├── image-tool.ts
│   ├── message-tool.ts
│   ├── nodes-tool.ts
│   ├── session*.ts
│   ├── slack-actions.ts
│   ├── telegram-actions.ts
│   ├── web-*.ts
│   └── whatsapp-actions.ts
└── ...
```

# # Fluxo de Integração Principal

### 1. Gerindo um agente incorporado

O ponto de entrada principal é <<CODE0>> em <<CODE1>>:

```typescript
import { runEmbeddedPiAgent } from "./agents/pi-embedded-runner.js";

const result = await runEmbeddedPiAgent({
  sessionId: "user-123",
  sessionKey: "main:whatsapp:+1234567890",
  sessionFile: "/path/to/session.jsonl",
  workspaceDir: "/path/to/workspace",
  config: openclawConfig,
  prompt: "Hello, how are you?",
  provider: "anthropic",
  model: "claude-sonnet-4-20250514",
  timeoutMs: 120_000,
  runId: "run-abc",
  onBlockReply: async (payload) => {
    await sendToChannel(payload.text, payload.mediaUrls);
  },
});
```

2. Criação de Sessão

Dentro de <<CODE0>> (chamado por <<CODE1>>>), o pi SDK é utilizado:

```typescript
import { createAgentSession, SessionManager, SettingsManager } from "@mariozechner/pi-coding-agent";

const { session } = await createAgentSession({
  cwd: resolvedWorkspace,
  agentDir,
  authStorage: params.authStorage,
  modelRegistry: params.modelRegistry,
  model: params.model,
  thinkingLevel: mapThinkingLevel(params.thinkLevel),
  systemPrompt: createSystemPromptOverride(appendPrompt),
  tools: builtInTools,
  customTools: allCustomTools,
  sessionManager,
  settingsManager,
  skills: [],
  contextFiles: [],
  additionalExtensionPaths,
});
```

3. Assinatura do evento

<<CODE0> subscreve pi <<CODE1> eventos:

```typescript
const subscription = subscribeEmbeddedPiSession({
  session: activeSession,
  runId: params.runId,
  verboseLevel: params.verboseLevel,
  reasoningMode: params.reasoningLevel,
  toolResultFormat: params.toolResultFormat,
  onToolResult: params.onToolResult,
  onReasoningStream: params.onReasoningStream,
  onBlockReply: params.onBlockReply,
  onPartialReply: params.onPartialReply,
  onAgentEvent: params.onAgentEvent,
});
```

Os eventos tratados incluem:

- <<CODE0>>/ <<CODE1>>/ <<CODE2>> (streaming texto/pensando)
- <<CODE3>>/ <<CODE4>>/ <<CODE5>>
- <<CODE6>>/ <<CODE7>>
- <<CODE8>>/ <<CODE9>>
- <<CODE10>>/ <<CODE11>>

4. A pedir ajuda

Após a configuração, a sessão é solicitada:

```typescript
await session.prompt(effectivePrompt, { images: imageResult.images });
```

O SDK lida com o loop completo do agente: envio para LLM, execução de chamadas de ferramenta, transmissão de respostas.

# # Arquitetura de ferramentas

Pipeline de ferramentas

1. **Base Tools**: pi's <<CODE0>> (ler, bash, editar, escrever)
2. ** Substituições personalizadas**: OpenClaw substitui bash por <<CODE1>/<<CODE2>>, personaliza leitura/edição/escrita para sandbox
3. **OpenClaw Tools**: mensagens, navegador, tela, sessões, cron, gateway, etc.
4. ** Ferramentas de Canal**: Discord/Telegram/Slack/WhatsApp-specific action tools
5. ** Filtragem Política**: Ferramentas filtradas por políticas de perfil, provedor, agente, grupo, sandbox
6. ** Normalização do esquema**: Esquemas limpos para as peculiaridades de Gemini/OpenAI
7. **AbortSignal Wraping**: Ferramentas envolvidas para respeitar os sinais de abortação

Adaptador de Definição de Ferramentas

A assinatura do pi-agent-core <<CODE0> tem uma assinatura diferente <<CODE1>> do que a do pi-coding-agent <<CODE2>>. O adaptador em <<CODE3> liga isto:

```typescript
export function toToolDefinitions(tools: AnyAgentTool[]): ToolDefinition[] {
  return tools.map((tool) => ({
    name: tool.name,
    label: tool.label ?? name,
    description: tool.description ?? "",
    parameters: tool.parameters,
    execute: async (toolCallId, params, onUpdate, _ctx, signal) => {
      // pi-coding-agent signature differs from pi-agent-core
      return await tool.execute(toolCallId, params, signal, onUpdate);
    },
  }));
}
```

## # Estratégia de divisão de ferramentas

<<CODE0> passa todas as ferramentas via <<CODE1>>:

```typescript
export function splitSdkTools(options: { tools: AnyAgentTool[]; sandboxEnabled: boolean }) {
  return {
    builtInTools: [], // Empty. We override everything
    customTools: toToolDefinitions(options.tools),
  };
}
```

Isso garante que a filtragem de políticas do OpenClaw, integração com sandbox e conjunto de ferramentas estendidas permaneçam consistentes entre os provedores.

# # Construção de Prompt de Sistema

O prompt do sistema é construído em <<CODE0>> (<HTML1>>>>). Ele monta um prompt completo com seções, incluindo Tooling, Estilo de Chamada de Ferramenta, Safety guardrails, OpenClaw referência CLI, Habilidades, Docs, Área de Trabalho, Sandbox, Mensagens, Resposta Tags, Voz, Respostas Silenciosas, Heartbeats, metadados Runtime, além de Memória e Reações quando habilitados, e arquivos de contexto opcionais e conteúdo prompt do sistema extra. As seções são aparadas para o modo prompt mínimo utilizado pelos subagentes.

O prompt é passado para pi via <<CODE0> sobreposição:

```typescript
const systemPrompt = createSystemPromptOverride(appendPrompt);
// Returns: (defaultPrompt: string) => trimmed custom prompt
```

# # Gerenciamento de Sessão

Arquivos de sessão

Sessões são arquivos JSONL com estrutura em árvore (ligação ID/parentId). A persistência de Pi <<CODE0> manipula:

```typescript
const sessionManager = SessionManager.open(params.sessionFile);
```

OpenClaw envolve isso com <<CODE0>> para a segurança do resultado da ferramenta.

# # Session Caching

<<CODE0> caches SessionManager instâncias para evitar a análise repetida de arquivos:

```typescript
await prewarmSessionFile(params.sessionFile);
sessionManager = SessionManager.open(params.sessionFile);
trackSessionManagerAccess(params.sessionFile);
```

## # Limitação da História

<<CODE0>> apara o histórico de conversas baseado no tipo de canal (DM vs grupo).

Compactação

Activação de autocompactação no excesso de contexto. <<CODE0> manipula compactação manual:

```typescript
const compactResult = await compactEmbeddedPiSessionDirect({
  sessionId, sessionFile, provider, model, ...
});
```

# # Autenticação e resolução do modelo

Perfis Auth

OpenClaw mantém uma loja de perfil de autenticação com várias chaves de API por provedor:

```typescript
const authStore = ensureAuthProfileStore(agentDir, { allowKeychainPrompt: false });
const profileOrder = resolveAuthProfileOrder({ cfg, store: authStore, provider, preferredProfile });
```

Perfis giram em falhas com o rastreamento de arrefecimento:

```typescript
await markAuthProfileFailure({ store, profileId, reason, cfg, agentDir });
const rotated = await advanceAuthProfile();
```

## # Resolução do modelo

```typescript
import { resolveModel } from "./pi-embedded-runner/model.js";

const { model, error, authStorage, modelRegistry } = resolveModel(
  provider,
  modelId,
  agentDir,
  config,
);

// Uses pi's ModelRegistry and AuthStorage
authStorage.setRuntimeApiKey(model.provider, apiKeyInfo.apiKey);
```

Falhou

<<CODE0> desencadeia o recuo do modelo quando configurado:

```typescript
if (fallbackConfigured && isFailoverErrorMessage(errorText)) {
  throw new FailoverError(errorText, {
    reason: promptFailoverReason ?? "unknown",
    provider,
    model: modelId,
    profileId,
    status: resolveFailoverStatus(promptFailoverReason),
  });
}
```

## Pi Extensões

Openclaw carrega extensões pi personalizadas para comportamento especializado:

Salvaguarda de compactação

<<CODE0> adiciona guardrails à compactação, incluindo orçamento de token adaptativo mais falha de ferramenta e resumos de operação de arquivo:

```typescript
if (resolveCompactionMode(params.cfg) === "safeguard") {
  setCompactionSafeguardRuntime(params.sessionManager, { maxHistoryShare });
  paths.push(resolvePiExtensionPath("compaction-safeguard"));
}
```

Poda de contexto

<<CODE0> implementa poda de contexto baseada em cache-TTL:

```typescript
if (cfg?.agents?.defaults?.contextPruning?.mode === "cache-ttl") {
  setContextPruningRuntime(params.sessionManager, {
    settings,
    contextWindowTokens,
    isToolPrunable,
    lastCacheTouchAt,
  });
  paths.push(resolvePiExtensionPath("context-pruning"));
}
```

# # Streaming & Block resplies

Block Chunking

<<CODE0> gerencia streaming de texto em blocos de resposta discretos:

```typescript
const blockChunker = blockChunking ? new EmbeddedBlockChunker(blockChunking) : null;
```

# # # Pensar/Final Tirar Etiquetas

O fluxo de saída é processado para remover <<CODE0>/<<CODE1>blocos e extrair <<CODE2>> conteúdo:

```typescript
const stripBlockTags = (text: string, state: { thinking: boolean; final: boolean }) => {
  // Strip <think>...</think> content
  // If enforceFinalTag, only return <final>...</final> content
};
```

# # Responder diretivas

Directrizes de resposta como <<CODE0>>, <<CODE1>>, <<CODE2>> são analisadas e extraídas:

```typescript
const { text: cleanedText, mediaUrls, audioAsVoice, replyToId } = consumeReplyDirectives(chunk);
```

# # Tratamento de Erros

## # Classificação de erro

<<CODE0> classifica erros para o tratamento adequado:

```typescript
isContextOverflowError(errorText)     // Context too large
isCompactionFailureError(errorText)   // Compaction failed
isAuthAssistantError(lastAssistant)   // Auth failure
isRateLimitAssistantError(...)        // Rate limited
isFailoverAssistantError(...)         // Should failover
classifyFailoverReason(errorText)     // "auth" | "rate_limit" | "quota" | "timeout" | ...
```

# # Pensando no nível de recuo

Se um nível de pensamento não é suportado, ele cai para trás:

```typescript
const fallbackThinking = pickFallbackThinkingLevel({
  message: errorText,
  attempted: attemptedThinking,
});
if (fallbackThinking) {
  thinkLevel = fallbackThinking;
  continue;
}
```

# # Integração com Caixa de Areia

Quando o modo sandbox está habilitado, ferramentas e caminhos são restritos:

```typescript
const sandbox = await resolveSandboxContext({
  config: params.config,
  sessionKey: sandboxSessionKey,
  workspaceDir: resolvedWorkspace,
});

if (sandboxRoot) {
  // Use sandboxed read/edit/write tools
  // Exec runs in container
  // Browser uses bridge URL
}
```

# # Manuseamento Específico do Provedor

Antrópico

- Recusar a limpeza de cordas mágicas
- Validação de turnos para funções consecutivas
- Compatibilidade do parâmetro Claude Code

Google/Gêmeos

- Correcções de ordem por turnos (<<<CODE0>>)
- Desintoxicação do esquema de ferramentas (<<< HTML1>>>>)
- Desintoxicação do histórico da sessão (<<<CODE2>>)

# # OpenAI

- ferramenta <<CODE0>> para modelos Codex
- Manuseamento de nível de pensamento

# # Integração TUI

Openclaw também tem um modo TUI local que usa componentes pi-tui diretamente:

```typescript
// src/tui/tui.ts
import { ... } from "@mariozechner/pi-tui";
```

Isso fornece a experiência de terminal interativo semelhante ao modo nativo do pi.

# # Principais diferenças de Pi CLI

Aspectos Pi CLI
----------------- ----------------------- ---------------------------------------------------------------------------------------------------------------
* Invocação < <<CODE0>> comando / RPC * SDK via <<CODE1>
Ferramentas □ Ferramentas de codificação padrão
AGENTS.md + prompts
. . Armazenamento de sessão . . . . . . . . . . . . . .
Autenticação Autenticação Única Credencial
□ Extensões □ Carregadas a partir de disco
• Tratamento de eventos; renderização TUI; Callback-based (onBlockReply, etc.)

# # Considerações futuras

Áreas de potencial retrabalho:

1. **Alinhamento da assinatura da ferramenta**: Adaptação entre as assinaturas pi-agent-core e pi-coding-agent
2. ** Embrulho do gestor de sessão**: <<CODE0> adiciona segurança, mas aumenta a complexidade
3. **Carregamento de extensão**: Poderia usar pi <<CODE1>> mais diretamente
4. **A complexidade do manequim **: <<CODE2>> cresceu grande
5. **Diferenças do fornecedor**: Muitos codepaths específicos do provedor que pi poderia potencialmente lidar

# # Testes

Todos os testes existentes que cobrem a integração pi e suas extensões:

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>
- <<CODE3>>
- <<CODE4>>
- <<CODE5>>
- <<CODE6>>
- <<CODE7>>
- <<CODE8>>
- <<CODE9>>
- <<CODE10>>
- <<CODE11>>
- <<CODE12>>
- <<CODE13>>
- <<CODE14>>
- <<CODE15>>
- <<CODE16>>
- <<CODE17>>
- <<CODE18>>
- <<CODE19>>
- <<CODE20>>
- <<CODE21>>
- <<CODE22>>
- <<CODE23>>
- <<CODE24>>
- <<CODE25>>
- <<CODE26>>
- <<CODE27> (vivo)
- <<CODE28>>
- <<CODE29>>
- <<CODE30>>
- <<CODE31>>
- <<CODE32>>
- <<CODE33>>
- <<CODE34>>
- <<CODE35>>
- <<CODE36>>
- <<CODE37>>
- <<CODE38>>
- <<CODE39>>
- <<CODE40>>
- <<CODE41>>
- <<CODE42>>
- <<CODE43>>
- <<CODE44>>
- <<CODE45>>
- <<CODE46>>
- <<CODE47>>
- <<CODE48>>
- <<CODE49>>
- <<CODE50>>
- <<CODE51>>
- <<CODE52>>
- <<CODE53>>
- <<CODE54>>
- <<CODE55>>
- <<CODE56>>
- <<CODE57>>
- <<CODE58>>
- <<CODE59>>
- <<CODE60>>
- <<CODE61>>
- <<CODE62>>
- <<CODE63>>
- <<CODE64>>
- <<CODE65>>
- <<CODE66>>
- <<CODE67>>
- <<CODE68>>
- <<CODE69>>
- <<CODE70>>
- <<CODE71>>
- <<CODE72>>
- <<CODE73>>
- <<CODE74>>
