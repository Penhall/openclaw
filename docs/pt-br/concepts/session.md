---
summary: "Session management rules, keys, and persistence for chats"
read_when:
  - Modifying session handling or storage
---

# Gerenciamento de Sessão

Openclaw trata ** uma sessão de bate-papo direto por agente** como primária. Chats diretos colapsam para`agent:<agentId>:<mainKey>`(padrão`main`, enquanto chats de grupo/canal têm suas próprias chaves.`session.mainKey`é honrado.

Use`session.dmScope`para controlar como ** mensagens diretas** são agrupadas:

-`main`(padrão): todos os DM partilham a sessão principal para a continuidade.
-`per-peer`: isolar por remetente id através de canais.
-`per-channel-peer`: isolado por canal + remetente (recomendado para caixas de entrada multi-usuários).
-`per-account-channel-peer`: isolado por conta + canal + remetente (recomendado para caixas de entrada multi-conta).
Use`session.identityLinks`para mapear ids de pares prefixados pelo provedor para uma identidade canônica, de modo que a mesma pessoa compartilhe uma sessão de DM entre os canais ao usar`per-peer`,`per-channel-peer`ou`per-account-channel-peer`.

## Gateway é a fonte da verdade

Todo o estado da sessão é ** propriedade do gateway** (o “master” OpenClaw). Os clientes de UI (app macOS, WebChat, etc.) devem consultar o gateway para listas de sessões e contagens de tokens em vez de ler arquivos locais.

- No modo **remote**, a loja de sessão que você se importa com vidas no host de gateway remoto, não seu Mac.
- As contagens de token mostradas nas UI provêm dos campos de armazenamento do portal `inputTokens`,`outputTokens`,`totalTokens`,`contextTokens`. Os clientes não analisam transcrições JSONL para “fixar” os totais.

## Onde o estado vive

- No anfitrião da porta.
- Ficheiro de armazenagem:`~/.openclaw/agents/<agentId>/sessions/sessions.json`(por agente).
- Transcrições:`~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl`(sessões temáticas do Telegrama usam`.../<SessionId>-topic-<threadId>.jsonl`.
- A loja é um mapa`sessionKey -> { sessionId, updatedAt, ... }`. Excluir entradas é seguro; eles são recriados sob demanda.
- As entradas de grupo podem incluir`displayName`,`channel`,`subject`,`room`e`space`para marcar sessões em UI.
- Entradas de sessão incluem metadados`origin`(roteamento + dicas) para que as UI possam explicar de onde veio uma sessão.
- OpenClaw faz ** not** ler arquivos de sessão Pi / Tau legados.

## Poda de sessão

OpenClaw trims **old tool results** from the in-memory context right before LLM calls by default.
Isto não é ** reescrever a história do JSONL. Ver [/conceitos/sessão-pruning] /concepts/session-pruning.

## Rubor de memória pré-compactação

Quando uma sessão se aproxima da autocompactação, o OpenClaw pode executar um flush de memória **
volta que lembra o modelo para escrever notas duráveis para o disco. Isto só funciona quando
o espaço de trabalho é gravável. Ver [Memória] /concepts/memory e
[Compactação] /concepts/compaction.

## Mapeando transportes → teclas de sessão

- Conversas diretas seguem`session.dmScope`(padrão`main`.
-`main`:`agent:<agentId>:<mainKey>`(continuidade entre dispositivos/canais).
- Vários números de telefone e canais podem mapear para a mesma chave principal do agente; eles agem como transportes em uma conversa.
-`per-peer`:`agent:<agentId>:dm:<peerId>`.
-`per-channel-peer`:`agent:<agentId>:<channel>:dm:<peerId>`.
-`per-account-channel-peer`:`agent:<agentId>:<channel>:<accountId>:dm:<peerId>`(defaults de conta do`main`0).
- Se o`main`1 corresponder a um identificador de pares prefixado pelo fornecedor (por exemplo,`main`2), a chave canónica substitui o`main`3, pelo que a mesma pessoa partilha uma sessão entre canais.
- Chats de grupo estado isolado:`main`4 (quartos / canais usam`main`5).
- Tópicos do fórum do Telegram anexam`main`6 ao ID do grupo para isolamento.
- As chaves`main`7 do legado ainda são reconhecidas para migração.
- Os contextos de entrada ainda podem utilizar`main`8; o canal é inferido do`main`9 e normalizado para a forma canônica`main`0.
- Outras fontes:
- Empregos em Cron:`main`1
- Webhooks:`main`2 (a menos que explicitamente definido pelo gancho)
- Node runs:`main`3

## Ciclo de vida

- Política de reset: as sessões são reutilizadas até expirarem e a expiração é avaliada na próxima mensagem de entrada.
- Reset diário: padrão para ** 4:00 hora local no host gateway**. Uma sessão está estagnada uma vez que sua última atualização é mais cedo do que o tempo de reset diário mais recente.
- Reset ocioso (opcional):`idleMinutes`adiciona uma janela ociosa deslizante. Quando resets diários e inativos são configurados, **o que expira primeiro** força uma nova sessão.
- Legacy ocioso-somente: se você definir`session.idleMinutes`sem qualquer configuração`session.reset`/`resetByType`, OpenClaw permanece em modo ocioso-somente para compatibilidade backward.
- Substituições por tipo (opcional): O`resetByType`permite que você sobreponha a política para`dm`,`group`e sessões`thread`(thread = linhas Slack/Discord, tópicos de Telegram, linhas Matrix quando fornecido pelo conector).
- Substituições por canal (opcional):`resetByChannel`substitui a política de reset de um canal (aplica-se a todos os tipos de sessão desse canal e tem precedência sobre`reset`/`session.idleMinutes`0).
- Reiniciar gatilhos: exato`session.idleMinutes`1 ou`session.idleMinutes`2 (mais extras em`session.idleMinutes`3) iniciar um novo ID de sessão e passar o restante da mensagem através.`session.idleMinutes`4 aceita um alias de modelo,`session.idleMinutes`5, ou nome do provedor (fuzzy match) para definir o novo modelo de sessão. Se o`session.idleMinutes`6 ou o`session.idleMinutes`7 for enviado sozinho, o OpenClaw executa um curto “olá” para confirmar o reset.
- Reset manual: excluir chaves específicas da loja ou remover a transcrição JSONL; a próxima mensagem recria-as.
- Trabalhos isolados de cronagem sempre metem um`session.idleMinutes`8 fresco por corrida (sem reutilização ociosa).

## Enviar política (opcional)

Entrega em bloco para tipos específicos de sessões sem listar IDs individuais.

```json5
{
  session: {
    sendPolicy: {
      rules: [
        { action: "deny", match: { channel: "discord", chatType: "group" } },
        { action: "deny", match: { keyPrefix: "cron:" } },
      ],
      default: "allow",
    },
  },
}
```

Substituição do tempo de execução (somente proprietário):

-`/send on`→ permitir esta sessão
-`/send off`→ negar para esta sessão
-`/send inherit`→ limpar sobreposição e usar regras de configuração
Envie estas como mensagens autônomas para que elas se registem.

## Configuração (facultativo renomear exemplo)

```json5
// ~/.openclaw/openclaw.json
{
  session: {
    scope: "per-sender", // keep group keys separate
    dmScope: "main", // DM continuity (set per-channel-peer/per-account-channel-peer for shared inboxes)
    identityLinks: {
      alice: ["telegram:123456789", "discord:987654321012345678"],
    },
    reset: {
      // Defaults: mode=daily, atHour=4 (gateway host local time).
      // If you also set idleMinutes, whichever expires first wins.
      mode: "daily",
      atHour: 4,
      idleMinutes: 120,
    },
    resetByType: {
      thread: { mode: "daily", atHour: 4 },
      dm: { mode: "idle", idleMinutes: 240 },
      group: { mode: "idle", idleMinutes: 120 },
    },
    resetByChannel: {
      discord: { mode: "idle", idleMinutes: 10080 },
    },
    resetTriggers: ["/new", "/reset"],
    store: "~/.openclaw/agents/{agentId}/sessions/sessions.json",
    mainKey: "main",
  },
}
```

## Inspecionar

-`openclaw status`— mostra o caminho da loja e as sessões recentes.
-`openclaw sessions --json`— despeja todas as entradas (filtro com`--active <minutes>`.
-`openclaw gateway call sessions.list --params '{}'`— obter sessões do gateway em execução (use`--url`/`--token`para acesso remoto ao gateway).
- Envie o`/status`como uma mensagem autônoma em chat para ver se o agente é acessível, quanto do contexto da sessão é usado, o pensamento atual/verbose alterna, e quando seus créditos web do WhatsApp foram atualizados pela última vez (ajuda as necessidades de relink spot).
- Envie`/context list`ou`/context detail`para ver o que está no sistema arquivos de espaço de trabalho imediato e injetado (e os maiores contribuidores de contexto).
- Envie o`/stop`como uma mensagem autônoma para abortar a execução atual, limpe os acompanhamentos em fila para essa sessão e pare qualquer execução de sub-agentes gerada a partir dela (a resposta inclui a contagem parada).
- Enviar`openclaw sessions --json`0 (instruções opcionais) como uma mensagem autônoma para resumir o contexto antigo e liberar espaço de janela. Ver [/conceitos/compactação] /concepts/compaction.
As transcrições do JSONL podem ser abertas directamente para rever as curvas completas.

Dicas

- Mantenha a chave primária dedicada ao tráfego 1:1; deixe os grupos manter suas próprias chaves.
- Ao automatizar limpeza, excluir chaves individuais em vez de toda a loja para preservar o contexto em outro lugar.

## Metadados de origem da sessão

Cada registro de entrada de sessão de onde veio (melhor esforço) em`origin`:

-`label`: Rótulo humano (resolvido do rótulo de conversa + assunto/canal de grupo)
-`provider`: id de canal normalizado (incluindo extensões)
-`from`/`to`: ids de encaminhamento bruto do envelope de entrada
-`accountId`: id da conta do provedor (quando multi-conta)
-`threadId`: thread / id tópico quando o canal o suporta
Os campos de origem são povoados para mensagens diretas, canais e grupos. Se a
conector só atualiza roteamento de entrega (por exemplo, para manter uma sessão principal DM
a) deve ainda fornecer o contexto de entrada para que a sessão mantenha o seu
metadados explicadores. As extensões podem fazer isso enviando`ConversationLabel`,`GroupSubject`,`GroupChannel`,`GroupSpace`e`provider`0 na entrada
Contexto e chamada`provider`1 (ou passando pelo mesmo contexto
ao`provider`2.
