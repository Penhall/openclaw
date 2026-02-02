---
summary: "Plan: one clean plugin SDK + runtime for all messaging connectors"
read_when:
  - Defining or refactoring the plugin architecture
  - Migrating channel connectors to the plugin SDK/runtime
---

# Plug-in SDK + Plano de refator de tempo de execução

Objectivo: cada conector de mensagens é um plugin (conjunto ou externo) usando uma API estável.
Nenhum plugin importa de <<CODE0> diretamente. Todas as dependências passam pelo SDK ou pelo tempo de execução.

# # Por que agora

- Conectores atuais misturam padrões: importações diretas de núcleo, pontes exclusivas de dist e ajudantes personalizados.
- Isso torna as atualizações quebradiço e bloqueia uma superfície de plugin externa limpa.

# # Arquitetura alvo (duas camadas)

# # # 1) Plugin SDK (tempo de compilação, estável, publicável)

Escopo: tipos, ajudantes e utilitários de configuração. Sem estado de corrida, sem efeitos secundários.

Conteúdo (exemplos):

- Tipos: `ChannelPlugin`, adaptadores, `ChannelMeta`, `ChannelCapabilities`, `ChannelDirectoryEntry`.
- Ajudantes de configuração: `buildChannelConfigSchema`, `setAccountEnabledInConfigSection`, `deleteAccountFromConfigSection`,
`applyAccountNameToChannelSection`.
- Ajudantes pareados: `PAIRING_APPROVED_MESSAGE`, `formatPairingApproveHint`.
- Ajudantes a bordo: `promptChannelAccessConfig`, <CODE11>>, tipos de integração.
- Ajudantes param ferramenta: `createActionGate`, `readStringParam`, `readNumberParam`, `readReactionParams`, `jsonResult`.
- Docs link helper: `formatDocsLink`.

Entrega:

- Publicar como `openclaw/plugin-sdk` (ou exportar do núcleo em `openclaw/plugin-sdk`).
- Semver com garantias de estabilidade explícitas.

# # # 2) Plugin Runtime (superfície de execução, injetada)

Escopo: tudo o que toca o comportamento do núcleo de execução.
Acessados via <<CODE0> para que os plugins nunca importem `src/**`.

Superfície proposta (mínimo mas completo):

```ts
export type PluginRuntime = {
  channel: {
    text: {
      chunkMarkdownText(text: string, limit: number): string[];
      resolveTextChunkLimit(cfg: OpenClawConfig, channel: string, accountId?: string): number;
      hasControlCommand(text: string, cfg: OpenClawConfig): boolean;
    };
    reply: {
      dispatchReplyWithBufferedBlockDispatcher(params: {
        ctx: unknown;
        cfg: unknown;
        dispatcherOptions: {
          deliver: (payload: {
            text?: string;
            mediaUrls?: string[];
            mediaUrl?: string;
          }) => void | Promise<void>;
          onError?: (err: unknown, info: { kind: string }) => void;
        };
      }): Promise<void>;
      createReplyDispatcherWithTyping?: unknown; // adapter for Teams-style flows
    };
    routing: {
      resolveAgentRoute(params: {
        cfg: unknown;
        channel: string;
        accountId: string;
        peer: { kind: "dm" | "group" | "channel"; id: string };
      }): { sessionKey: string; accountId: string };
    };
    pairing: {
      buildPairingReply(params: { channel: string; idLine: string; code: string }): string;
      readAllowFromStore(channel: string): Promise<string[]>;
      upsertPairingRequest(params: {
        channel: string;
        id: string;
        meta?: { name?: string };
      }): Promise<{ code: string; created: boolean }>;
    };
    media: {
      fetchRemoteMedia(params: { url: string }): Promise<{ buffer: Buffer; contentType?: string }>;
      saveMediaBuffer(
        buffer: Uint8Array,
        contentType: string | undefined,
        direction: "inbound" | "outbound",
        maxBytes: number,
      ): Promise<{ path: string; contentType?: string }>;
    };
    mentions: {
      buildMentionRegexes(cfg: OpenClawConfig, agentId?: string): RegExp[];
      matchesMentionPatterns(text: string, regexes: RegExp[]): boolean;
    };
    groups: {
      resolveGroupPolicy(
        cfg: OpenClawConfig,
        channel: string,
        accountId: string,
        groupId: string,
      ): {
        allowlistEnabled: boolean;
        allowed: boolean;
        groupConfig?: unknown;
        defaultConfig?: unknown;
      };
      resolveRequireMention(
        cfg: OpenClawConfig,
        channel: string,
        accountId: string,
        groupId: string,
        override?: boolean,
      ): boolean;
    };
    debounce: {
      createInboundDebouncer<T>(opts: {
        debounceMs: number;
        buildKey: (v: T) => string | null;
        shouldDebounce: (v: T) => boolean;
        onFlush: (entries: T[]) => Promise<void>;
        onError?: (err: unknown) => void;
      }): { push: (v: T) => void; flush: () => Promise<void> };
      resolveInboundDebounceMs(cfg: OpenClawConfig, channel: string): number;
    };
    commands: {
      resolveCommandAuthorizedFromAuthorizers(params: {
        useAccessGroups: boolean;
        authorizers: Array<{ configured: boolean; allowed: boolean }>;
      }): boolean;
    };
  };
  logging: {
    shouldLogVerbose(): boolean;
    getChildLogger(name: string): PluginLogger;
  };
  state: {
    resolveStateDir(cfg: OpenClawConfig): string;
  };
};
```

Notas:

O tempo de execução é a única forma de aceder ao comportamento central.
- SDK é intencionalmente pequeno e estável.
- Cada método de execução mapeia uma implementação de núcleo existente (sem duplicação).

# # Plano de migração (faseado, seguro)

Fase 0: andaimes

- Apresentar `openclaw/plugin-sdk`.
- Adicionar `api.runtime` a `OpenClawPluginApi` com a superfície acima.
- Manter as importações existentes durante uma janela de transição (avisos de depreciação).

Fase 1: limpeza da ponte (baixo risco)

- Substituir por extensão `core-bridge.ts` por `api.runtime`.
- Migrar BlueBubbles, Zalo, Zalo Personal primeiro (já perto).
- Remover código de ponte duplicado.

Fase 2: plugins de importação direta leves

- Migrar Matrix para SDK + tempo de execução.
- Validar a lógica de onboarding, diretório, grupo de referência.

#### Fase 3: plugins pesados de importação direta

- Migrar Equipes MS (maior conjunto de ajudantes de execução).
- Garantir resposta/tipagem semântica corresponde ao comportamento atual.

Fase 4: plugins de iMessage

- Mover iMensage para `extensions/imessage`.
- Substituir chamadas diretas por `api.runtime`.
- Mantenha as chaves de configuração, o comportamento CLI e documentos intactos.

Fase 5: aplicação

- Adicionar regra do fio / verificação CI: não <<CODE0> importações de `src/**`.
- Adicionar verificação de compatibilidade SDK/versão plugin (runtime + SDK semver).

# # Compatibilidade e versão

- SDK: Semver, publicado, documentado alterações.
- Tempo de execução: versão por núcleo. Adicionar `api.runtime.version`.
- Plugins declaram um intervalo de tempo de execução necessário (por exemplo, `openclawRuntime: ">=2026.2.0"`).

# # Estratégia de teste

- Testes unitários de nível adaptador (funções de execução exercidas com implementação de núcleo real).
- Testes dourados por plugin: garantir nenhuma deriva de comportamento (roteamento, emparelhamento, allowlist, mencionar gating).
- Uma única amostra de plugin de ponta a ponta usada em CI (install + run + smoke).

# # Perguntas abertas

- Onde hospedar tipos SDK: pacote separado ou exportação de núcleo?
- Distribuição do tipo de execução: no SDK (somente tipos) ou no núcleo?
- Como expor links de documentos para plug-ins empacotados vs externos?
- Permitemos importações diretas limitadas para plug-ins in-repo durante a transição?

# # Critérios de sucesso

- Todos os conectores de canal são plugins usando SDK + tempo de execução.
- Não existem importações <<CODE0> de <<CODE1>.
- Novos modelos de conectores dependem apenas de SDK + tempo de execução.
- Plugins externos podem ser desenvolvidos e atualizados sem acesso de fonte central.

Documentos relacionados: [Plugins](</plugin), [Canais](/channels/index), [Configuração](/gateway/configuration).
