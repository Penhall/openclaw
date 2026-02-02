---
summary: "Agent tool surface for OpenClaw (browser, canvas, nodes, message, cron) replacing legacy `openclaw-*` skills"
read_when:
  - Adding or modifying agent tools
  - Retiring or changing `openclaw-*` skills
---

# Ferramentas (OpenClaw)

OpenClaw expõe ** ferramentas de agente de primeira classe** para navegador, canvas, nós e cron.
Estes substituem as antigas habilidades <<CODE0>: as ferramentas são digitadas, sem bombardeio,
e o agente deve confiar neles diretamente.

# # Desativando ferramentas

Você pode permitir/negar globalmente ferramentas via `tools.allow` / `tools.deny` em `openclaw.json`
(negar ganha). Isso impede que ferramentas proibidas sejam enviadas para provedores de modelos.

```json5
{
  tools: { deny: ["browser"] },
}
```

Notas:

- A correspondência é insensível.
- `*` são suportados curingas (`"*"` significa todas as ferramentas).
- Se <<CODE2> apenas referências desconhecidas ou descarregadas nomes de ferramentas de plugins, o OpenClaw registra um aviso e ignora a lista de allowlist para que as ferramentas principais permaneçam disponíveis.

# # Perfil de ferramentas (lista de permissões de base)

<<CODE0> define uma lista de ferramentas de base** antes `tools.allow`/`tools.deny`.
Substituição por agente: `agents.list[].tools.profile`.

Perfil:

- `minimal`: <<CODE1> apenas
- `coding`: `group:fs`, `group:runtime`, `group:sessions`, `group:memory`, `image`
- `messaging`: `group:messaging`, `sessions_list`, `sessions_history`, `sessions_send`, `session_status`
- <<CODE14>: nenhuma restrição (mesmo que não definida)

Exemplo (somente mensagens por padrão, permitir ferramentas Slack + Discord também):

```json5
{
  tools: {
    profile: "messaging",
    allow: ["slack", "discord"],
  },
}
```

Exemplo (perfil de codificação, mas negar exec/processo em toda parte):

```json5
{
  tools: {
    profile: "coding",
    deny: ["group:runtime"],
  },
}
```

Exemplo (perfil de codificação global, agente de suporte apenas para mensagens):

```json5
{
  tools: { profile: "coding" },
  agents: {
    list: [
      {
        id: "support",
        tools: { profile: "messaging", allow: ["slack"] },
      },
    ],
  },
}
```

# # Política de ferramenta específica do provedor

Utilizar `tools.byProvider` para **mais ferramentas de restrição** para fornecedores específicos
(ou um único `provider/model`) sem alterar seus padrões globais.
Substituição por agente: `agents.list[].tools.byProvider`.

Isto é aplicado ** after** o perfil da ferramenta base e ** before** allow/deny lists,
então ele só pode estreitar o conjunto de ferramentas.
As chaves do fornecedor aceitam quer `provider` (por exemplo, `google-antigravity`) quer
<<CODE2> (por exemplo, `openai/gpt-5.2`).

Exemplo (mantenha o perfil de codificação global, mas ferramentas mínimas para o Google Antigravity):

```json5
{
  tools: {
    profile: "coding",
    byProvider: {
      "google-antigravity": { profile: "minimal" },
    },
  },
}
```

Exemplo (fornecedor/modelo-específico allowlist para um endpoint flácido):

```json5
{
  tools: {
    allow: ["group:fs", "group:runtime", "sessions_list"],
    byProvider: {
      "openai/gpt-5.2": { allow: ["group:fs", "sessions_list"] },
    },
  },
}
```

Exemplo (sobreposição específica do agente para um único fornecedor):

```json5
{
  agents: {
    list: [
      {
        id: "support",
        tools: {
          byProvider: {
            "google-antigravity": { allow: ["message", "sessions_list"] },
          },
        },
      },
    ],
  },
}
```

# # Grupos de ferramentas

Políticas de ferramentas (global, agent, sandbox) suportam entradas `group:*` que se expandem para múltiplas ferramentas.
Utilizar estes em `tools.allow`/ `tools.deny`.

Grupos disponíveis:

- `group:runtime`: `exec`, `bash`, `process`
- `group:fs`: `read`, `write`, `edit`, `apply_patch`
- `group:sessions`: `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`
- `group:memory`: `memory_search`, `memory_get`
- `group:web`: `web_search`, `web_fetch`
- `group:ui`: `browser`, `canvas`
- `group:automation`: `cron`, `gateway`
- `group:messaging`: <<CODE28>
- `group:nodes`: <<CODE30>
- `group:openclaw`: todas as ferramentas OpenClaw incorporadas (exclui plugins de provedores)

Exemplo (permitir apenas ferramentas de arquivo + navegador):

```json5
{
  tools: {
    allow: ["group:fs", "browser"],
  },
}
```

# # Plugins + ferramentas

Plugins podem registrar ** ferramentas adicionais** (e comandos CLI) além do conjunto do núcleo.
Veja [Plugins](/plugin) para instalar + config, e [Skills](/tools/skills) para como
instruções de utilização da ferramenta é injetado em alertas. Alguns plugins enviam suas próprias habilidades
ao lado de ferramentas (por exemplo, o plugin de chamada de voz).

Ferramentas de plugin opcionais:

- [Lobster](</tools/lobster): printed workflow runtime with resumible aprovations (exige o CLI Lobster no host gateway).
- [LLM Task](</tools/llm-task): Passo LLM apenas para saída estruturada de fluxo de trabalho (validação opcional do esquema).

# # Inventário de ferramentas

## # <<CODE0>

Aplicar patches estruturados em um ou mais arquivos. Use para edições multi-hunk.
Experimental: habilitar via `tools.exec.applyPatch.enabled` (apenas modelos OpenAI).

## # <<CODE0>

Executar comandos de shell na área de trabalho.

Parâmetros principais:

- <<CODE0> (obrigatório)
- <<CODE1> (auto-background após tempo limite, padrão 10000)
- <<CODE2> (contexto imediato)
- `timeout` (segundos; mata o processo se excedido, padrão 1800)
- <<CODE4> (bool; execute no host se o modo elevado estiver ativado/permitido; só muda de comportamento quando o agente é sandboxed)
- `host` (`sandbox | gateway | node`)
- `security` (`deny | allowlist | full`)
- `ask` (`off | on-miss | always`)
- <<CODE11> (node id/name for `host=node`)
- Precisas de um TTY verdadeiro? Definir `pty: true`.

Notas:

- Retorna <<CODE0> com `sessionId` quando em segundo plano.
- Use `process` para pesquisar/log/write/kill/clear background sessions.
- Se <<CODE3> não for permitido, <<CODE4> é executado síncrono e ignora `yieldMs`/`background`.
- `elevated` é protegido por `tools.elevated` mais qualquer sobreposição `agents.list[].tools.elevated` (ambos devem permitir) e é um apelido para `host=gateway` + `security=full`.
- <<CODE12> só muda o comportamento quando o agente é sandboxed (caso contrário é um no-op).
- <<CODE13> pode atingir um aplicativo companheiro do macOS ou um host de nó sem cabeça (`openclaw node run`).
- aprovações de gateway/node e listas de licenças: [aprovações de execução](</tools/exec-approvals).

## # <<CODE0>

Gerenciar sessões de execução de fundo.

Acções principais:

- <<CODE0>, <<CODE1>, `log`, `write`, `kill`, `clear`, <<CODE6>

Notas:

- <<CODE0> retorna novo estado de saída e saída quando concluído.
- <<CODE1> suporta linhas <<CODE2>/`limit` (omite `offset` para agarrar as últimas linhas N).
- <<CODE5> é avaliado por agente; as sessões de outros agentes não são visíveis.

## # <<CODE0>

Pesquise na web usando Brave Search API.

Parâmetros principais:

- <<CODE0> (obrigatório)
- <<CODE1> (1–10; por omissão de `tools.web.search.maxResults`)

Notas:

- Requer uma chave API Brave (recomendada: `openclaw configure --section web`, ou definida `BRAVE_API_KEY`).
- Habilitar via `tools.web.search.enabled`.
- As respostas estão em cache (padrão 15 min).
- Veja [Ferramentas Web](/tools/web) para configuração.

## # <<CODE0>

Obter e extrair conteúdo legível de uma URL (HTML → markdown/text).

Parâmetros principais:

- <<CODE0> (obrigatório)
- <<CODE1> (`markdown` `text`)
- <<CODE4> (páginas longas)

Notas:

- Habilitar via `tools.web.fetch.enabled`.
- As respostas estão em cache (padrão 15 min).
- Para sites JS-pesados, prefira a ferramenta do navegador.
- Veja [Ferramentas Web](/tools/web) para configuração.
- Ver [Firecrawl](/tools/firecrawl) para o recurso opcional anti-bot.

## # <<CODE0>

Controle o navegador dedicado gerenciado pelo OpenClaw.

Acções principais:

- <<CODE0>, <<CODE1>, `stop`, `tabs`, `open`, `focus`, <<CODE6>
- `snapshot` (aria/ai)
- `screenshot` (retorno do bloco de imagem + `MEDIA:<path>`)
- `act` (acções UI: clique/tipo/pressão/hover/drag/select/fill/resize/wait/avaliar)
- `navigate`, `console`, `pdf`, `upload`, `dialog`

Gestão do perfil:

- `profiles` — listar todos os perfis do navegador com estatuto
- <<CODE1> – criar novo perfil com porta auto-alocada (ou `cdpUrl`)
- `delete-profile` — parar o navegador, apagar os dados do utilizador, remover da configuração (apenas local)
- `reset-profile` — processo de morte de órfão na porta do perfil (apenas local)

Parâmetros comuns:

- `profile` (opcional; por omissão `browser.defaultProfile`)
- <<CODE2> (`sandbox`
- <<CODE6> (opcional; escolhe um identificador de nó/nome específico)
Notas:
- Requer `browser.enabled=true` (padrão é `true`; definido `false` para desativar).
- Todas as ações aceitam parâmetro opcional `profile` para suporte multi-instance.
- Quando `profile` é omitida, utiliza `browser.defaultProfile` (por omissão para "cromado").
- Nomes de perfil: alfanuméricos minúsculas + hífens apenas (máximo 64 caracteres).
- Faixa de porto: 18800-18899 (~100 perfis máx.).
- Perfis remotos são somente anexados (sem início/parar/reset).
- Se um nó com capacidade para navegador estiver conectado, a ferramenta pode direcionar automaticamente para ele (a menos que você pingue `target`).
- `snapshot` defaults to `ai` when Playwright is installed; use `aria` for the accessibility tree.
- `snapshot` também suporta opções de role-snapshot (`interactive`, `compact`, `depth`, `selector`) que retornam refs como `e12`.
- `act` requer `ref` de `snapshot` (numérico `12` de instantâneos de IA, ou `e12` de instantâneos de papéis); utilização `evaluate` para necessidades raras de selecção de CSS.
- Evite `act` → `wait` por padrão; use-o apenas em casos excepcionais (sem estado de IU confiável para esperar).
- <<CODE31> pode passar opcionalmente um <<CODE32> para carregar automaticamente após o armamento.
- <<CODE33> também suporta `inputRef` (aria ref) ou `element` (Seletor CSS) para definir diretamente `<input type="file">`.

## # <<CODE0>

Dirija o nó Canvas (presente, avaliação, instantâneo, A2UI).

Acções principais:

- <<CODE0>, <<CODE1>, `navigate`, <<CODE3>
- `snapshot` (retorno do bloco de imagem + `MEDIA:<path>`)
- <<CODE6>, <<CODE7>

Notas:

- Usa gateway `node.invoke` sob o capô.
- Se não for fornecido <<CODE1>, a ferramenta escolhe um padrão (nodo único conectado ou nó local).
- A2UI é apenas v0.8 (não `createSurface`); o CLI rejeita v0.9 JSONL com erros de linha.
- Fumo rápido: `openclaw nodes canvas a2ui push --node <id> --text "Hello from A2UI"`.

## # <<CODE0>

Descobrir e atingir nós emparelhados; enviar notificações; capturar câmera/tela.

Acções principais:

- <<CODE0>, <<CODE1>
- `pending`, `approve`, `reject` (emparelhagem)
- <<CODE5> (macOS `system.notify`)
- `run` (macOS `system.run`)
- `camera_snap`, `camera_clip`, `screen_record`
- `location_get`

Notas:

- Os comandos da câmara/tela exigem que a aplicação do nó seja em primeiro plano.
- Imagens retornam blocos de imagem + `MEDIA:<path>`.
- Os vídeos retornam `FILE:<path>` (mp4).
- A localização devolve uma carga útil JSON (lat/lon/accuracy/timestamp).
- `run` parâmetros: `command` array argv; opcional `cwd`, `env` (`KEY=VAL`), `commandTimeoutMs`, `invokeTimeoutMs`, <<CODE9>.

Exemplo (`run`):

```json
{
  "action": "run",
  "node": "office-mac",
  "command": ["echo", "Hello"],
  "env": ["FOO=bar"],
  "commandTimeoutMs": 12000,
  "invokeTimeoutMs": 45000,
  "needsScreenRecording": false
}
```

## # <<CODE0>

Analise uma imagem com o modelo de imagem configurado.

Parâmetros principais:

- `image` (caminho ou URL requeridos)
- <<CODE1> (opcional; o padrão é "Descreva a imagem".
- <<CODE2> (sobreposição opcional)
- <<CODE3> (capa de tamanho opcional)

Notas:

- Apenas disponível quando <<CODE0> está configurado (primário ou fallbacks), ou quando um modelo de imagem implícita pode ser inferido a partir de seu modelo padrão + autenticação configurada (melhor emparelhamento).
- Utiliza o modelo de imagem diretamente (independentemente do modelo de chat principal).

## # <<CODE0>

Envie mensagens e canalize ações em Discord/Google Chat/Slack/Telegram/WhatsApp/Sinal/iMessage/MS Teams.

Acções principais:

- `send` (texto + mídia opcional; MS Teams também suporta `card` para cartões adaptativos)
- <<CODE2> (enquetes WhatsApp/Discord/MS Teams)
- `react`/ `reactions`/ `read`/ `edit`/ `delete`
- `pin` / `unpin` / `list-pins`
- <<CODE11>
- `thread-create` / `thread-list` / `thread-reply`
- <<CODE15>
- <<CODE16>
- `member-info` / <<CODE18>
- `emoji-list` / `emoji-upload` / `sticker-upload`
- `role-add` / `role-remove`
- `channel-info` / `channel-list`
- <<CODE26>
- `event-list` / <<CODE28>
- <<CODE29>/ `kick`/ <<CODE31>

Notas:

- `send` rotas WhatsApp via Gateway; outros canais vão diretamente.
- <<CODE1> usa o Gateway para WhatsApp e MS Teams; As pesquisas de discórdia são diretas.
- Quando uma chamada de uma ferramenta de mensagem está ligada a uma sessão de chat ativa, os envios são limitados ao alvo dessa sessão para evitar vazamentos de contexto cruzado.

## # <<CODE0>

Gerenciar trabalhos de cron Gateway e despertar.

Acções principais:

- <<CODE0>, <<CODE1>
- <<CODE2>, `update`, `remove`, `run`, `runs`
- `wake` (enquear evento do sistema + batimento cardíaco imediato opcional)

Notas:

- `add` espera um objeto de trabalho completo (mesmo esquema como `cron.add` RPC).
- <<CODE2> utiliza `{ id, patch }`.

## # <<CODE0>

Reinicie ou aplique atualizações no processo de Gateway em execução (no lugar).

Acções principais:

- `restart` (autoriza + envia `SIGUSR1` para reiniciar em processo; <<CODE2> reiniciar no local)
- `config.get` / `config.schema`
- <<CODE5> (validar + gravar configuração + reiniciar + despertar)
- <<CODE6> (actualização parcial da fusão + reiniciar + despertar)
- `update.run` (atualização de execução + reiniciar + despertar)

Notas:

- Use `delayMs` (por omissão até 2000) para evitar interromper uma resposta em voo.
- <<CODE1> está desativado por padrão; habilite com `commands.restart: true`.

## # <<CODE0> / `sessions_history` / `sessions_send` / `sessions_spawn` / `session_status`

Listar sessões, inspecionar histórico de transcrição ou enviar para outra sessão.

Parâmetros principais:

- `sessions_list`: `kinds?`, `limit?`, `activeMinutes?`, `messageLimit?` (0 = nenhum)
- `sessions_history`: `sessionKey` (ou `sessionId`>), `limit?`, `includeTools?`
- `sessions_send`: `sessionKey` (ou `sessionId`), `message`, `timeoutSeconds?` (0 = incêndio e esquecimento)
- `sessions_spawn`: `task`, `label?`, `agentId?`, `model?`, `runTimeoutSeconds?`, `cleanup?`
- `session_status`: `sessionKey?` (corrente padrão; aceita `sessionId`), `model?` (`default` sobreposição de cleares)

Notas:

- <<CODE0> é a chave canônica de bate-papo direto; global/desconhecido estão ocultos.
- <<CODE1> obtém as últimas mensagens N por sessão (mensagens da ferramenta filtradas).
- <<CODE2> espera pela conclusão final quando `timeoutSeconds > 0`.
- Entrega/anúncio acontece após a conclusão e é o melhor esforço; <<CODE4> confirma que o agente terminou, não que o anúncio foi entregue.
- <<CODE5> inicia uma execução do sub-agente e publica uma resposta de anúncio ao chat do solicitante.
- <<CODE6> não bloqueia e retorna <<CODE7> imediatamente.
- `sessions_send` executa um ping-pong de resposta (resposta `REPLY_SKIP` para parar; voltas máximas via `session.agentToAgent.maxPingPongTurns`, 0–5).
- Após o ping-pong, o agente alvo executa um passo de **announce**; responda `ANNOUNCE_SKIP` para suprimir o anúncio.

## # <<CODE0>

Lista ids do agente que a sessão atual pode atingir com `sessions_spawn`.

Notas:

- O resultado é restrito às listas de autorizações por agente (<`agents.list[].subagents.allowAgents`).
- Quando <<CODE1> é configurado, a ferramenta inclui todos os agentes configurados e marcas `allowAny: true`.

# # Parâmetros (comuns)

Ferramentas apoiadas por gateway (`canvas`, <CODE1>>, `cron`):

- <<CODE0> (padrão `ws://127.0.0.1:18789`)
- <<CODE2> (se activada)
- `timeoutMs`

Ferramenta de navegação:

- `profile` (opcional; por omissão `browser.defaultProfile`)
- <<CODE2> (`sandbox`
- <<CODE6> (facultativo; afixar um identificador de nó/nome específico)

# # Fluxos de agentes recomendados

Automatização do navegador:

1. `browser` → `status`/ <<CODE2>
2. <<CODE3> (ai ou aria)
3. `act` (clique/tipo/impressão)
4. <<CODE5> se precisar de confirmação visual

Desenho da tela:

1. `canvas` → `present`
2. `a2ui_push` (facultativo)
3. `snapshot`

Alvo do nó:

1. `nodes` → `status`
2. `describe` no nó escolhido
3. `notify`/ `run`/ `camera_snap`/ <<CODE6>

# # Segurança

- Evite diretamente `system.run`; use `nodes` → `run` apenas com consentimento explícito do usuário.
- Respeitar o consentimento do usuário para captura de câmera / tela.
- Use `status/describe` para garantir permissões antes de invocar comandos de mídia.

# # Como as ferramentas são apresentadas ao agente

As ferramentas são expostas em dois canais paralelos:

1. ** Texto rápido do sistema**: uma lista legível pelo homem + orientação.
2. **Esquema de ferramentas**: as definições de funções estruturadas enviadas para a API do modelo.

Isso significa que o agente vê tanto “que ferramentas existem” quanto “como chamá-las”. Se uma ferramenta
não aparece no prompt do sistema ou no esquema, o modelo não pode chamá-lo.
