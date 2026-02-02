---
summary: "Session management rules, keys, and persistence for chats"
read_when:
  - Modifying session handling or storage
---

# Gerenciamento de Sessão

Openclaw trata ** uma sessão de bate-papo direto por agente** como primária. Chats diretos colapsam para <<CODE0>> (padrão <<CODE1>>), enquanto chats grupo/canal têm suas próprias chaves. <<CODE2> é honrado.

Use <<CODE0>> para controlar como ** mensagens diretas** são agrupadas:

- <<CODE0>> (padrão): todos os DMs compartilham a sessão principal para continuidade.
- <<CODE1>>: isolar por id remetente entre os canais.
- <<CODE2>>: isolado por canal + remetente (recomendado para caixas de entrada multi- utilizador).
- <<CODE3>>: isolado por conta + canal + remetente (recomendado para caixas de entrada multiconta).
Use <<CODE4>> para mapear ids de pares pré-fixados pelo provedor para uma identidade canônica de modo que a mesma pessoa compartilhe uma sessão de DM entre os canais ao usar <<CODE5>>, <<CODE6>>>, ou <<CODE7>>.

# # Gateway é a fonte da verdade

Todo o estado da sessão é ** propriedade do gateway** (o “master” OpenClaw). Os clientes de UI (app macOS, WebChat, etc.) devem consultar o gateway para listas de sessões e contagens de tokens em vez de ler arquivos locais.

- No modo **remote**, a loja de sessão que você se importa com vidas no host de gateway remoto, não seu Mac.
- As contagens de token mostradas nas UI provêm dos campos de armazenamento do gateway (<<<CODE0>>, <<CODE1>>, <<CODE2>>, <<CODE3>>>). Os clientes não analisam transcrições JSONL para “fixar” os totais.

# # Onde o estado vive

- No anfitrião da porta.
- Ficheiro de armazenamento: <<CODE0>> (por agente).
- Transcrições: <<CODE1>> (Sessões temáticas de telegrama usam <<CODE2>>>).
- A loja é um mapa <<CODE3>>>. Excluir entradas é seguro; eles são recriados sob demanda.
- As entradas em grupo podem incluir <<CODE4>>, <<CODE5>>, <<CODE6>>, <<CODE7>>, e <<CODE8>> para marcar sessões em UI.
- As entradas de sessão incluem <<CODE9>> metadados (label + roteamento de dicas) para que as UI possam explicar de onde veio uma sessão.
- OpenClaw faz ** not** ler arquivos de sessão Pi / Tau legados.

# # Poda de sessão

OpenClaw trims **old tool results** from the in-memory context right before LLM calls by default.
Isto não é ** reescrever a história do JSONL. Ver [/conceitos/pruning de sessões] (<<<LINK0>>>).

# # Rubor de memória pré-compactação

Quando uma sessão se aproxima da autocompactação, o OpenClaw pode executar um flush de memória **
volta que lembra o modelo para escrever notas duráveis para o disco. Isto só funciona quando
o espaço de trabalho é gravável. Ver [Memória] (<<<LINK0>>>) e
[Compactação] (<<<LINK1>>>).

# # Mapeando transportes → teclas de sessão

- Conversas diretas seguem <<CODE0>>> (padrão <<CODE1>>>).
- <<CODE2>>: <<CODE3>> (continuidade entre dispositivos/canais).
- Vários números de telefone e canais podem mapear para a mesma chave principal do agente; eles agem como transportes em uma conversa.
- <<CODE4>>: <<CODE5>>.
- <<CODE6>>: <<CODE7>>>.
- <<CODE8>>: <<CODE9>>> (accountId defaults to <<CODE10>>).
- Se <<CODE11>> corresponder a um id de pares prefixado pelo fornecedor (por exemplo, <<CODE12>>>), a chave canónica substitui <<CODE13>> de modo que a mesma pessoa partilha uma sessão entre canais.
- Estado de isolamento de chats em grupo: <<CODE14>> (as salas/canais usam <<CODE15>>).
- Tópicos do fórum de telegramas anexam <<CODE16>> ao ID do grupo para isolamento.
- Chaves Legado <<CODE17>> ainda são reconhecidas para migração.
- Os contextos de entrada ainda podem usar <<CODE18>>; o canal é inferido de <<CODE19>> e normalizado para a forma canônica <<CODE20>>.
- Outras fontes:
- Trabalhos em Cron: <<CODE21>>
- Anzóis: <<CODE22>> (a menos que explicitamente definido pelo gancho)
- Execução do nó: <<CODE23>>

# # Ciclo de vida

- Política de reset: as sessões são reutilizadas até expirarem e a expiração é avaliada na próxima mensagem de entrada.
- Reset diário: padrão para ** 4:00 hora local no host gateway**. Uma sessão está estagnada uma vez que sua última atualização é mais cedo do que o tempo de reset diário mais recente.
- Reset ocioso (opcional): <<CODE0>> adiciona uma janela ociosa deslizante. Quando resets diários e inativos são configurados, **o que expira primeiro** força uma nova sessão.
- Legado apenas ocioso: se definir <<CODE1>> sem <<CODE2>>/<<CODE3>> config, OpenClaw fica em modo somente ocioso para compatibilidade backward.
- Por-tipo substitui (opcional): <<CODE4>> permite que você sobreponha a política para <<CODE5>>>, <<CODE6>>> e <<CODE7> sessões (thread = Slack/Discord threads, tópicos de Telegram, Matrix threads quando fornecido pelo conector).
- Substituições por canal (opcional): <<CODE8>> substitui a política de reset para um canal (aplica-se a todos os tipos de sessão para esse canal e tem precedência sobre <<CODE9>>/<<CODE10>>>).
- Reiniciar gatilhos: exato <<CODE11>> ou <<CODE12>> (mais extras em <<CODE13>>) iniciar um novo ID de sessão e passar o restante da mensagem através. <<CODE14> aceita um alias de modelo, <<CODE15>>, ou nome do provedor (fuzzy match) para definir o novo modelo de sessão. Se <<CODE16>> ou <<CODE17>> for enviado sozinho, o OpenClaw corre uma pequena volta de saudação “olá” para confirmar o reset.
- Reset manual: excluir chaves específicas da loja ou remover a transcrição JSONL; a próxima mensagem recria-as.
- Trabalhos isolados de cronagem sempre metem um fresco <<CODE18>> por execução (sem reutilização ociosa).

# # Enviar política (opcional)

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

- <<CODE0> → permitir esta sessão
- <<CODE1> → negar para esta sessão
- <<CODE2>> → limpar sobreposição e usar regras de configuração
Envie estas como mensagens autônomas para que elas se registem.

# # Configuração (facultativo renomear exemplo)

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

# # Inspecionar

- <<CODE0>> — mostra o caminho da loja e as sessões recentes.
- <<CODE1>> — despeja todas as entradas (filtro com <<CODE2>>>).
- <<CODE3>> — obter sessões do gateway em execução (use <<CODE4>>/<<CODE5> para acesso remoto ao gateway).
- Envie <<CODE6>> como uma mensagem independente no chat para ver se o agente é acessível, quanto do contexto da sessão é usado, o pensamento atual/verbose alterna, e quando seus créditos web do WhatsApp foram atualizados pela última vez (ajuda as necessidades de relink spot).
- Enviar <<CODE7>> ou <<CODE8>> para ver o que está no prompt do sistema e arquivos de espaço de trabalho injetados (e os maiores contribuidores de contexto).
- Enviar <<CODE9>> como uma mensagem autônoma para interromper a execução atual, limpar os seguimentos em fila para essa sessão, e parar qualquer sub-agente corre gerado a partir dele (a resposta inclui a contagem parada).
- Enviar <<CODE10>> (instruções opcionais) como uma mensagem autônoma para resumir o contexto antigo e liberar espaço na janela. Ver [/conceitos/compactação] (<<<LINK0>>>).
As transcrições do JSONL podem ser abertas directamente para rever as curvas completas.

Dicas

- Mantenha a chave primária dedicada ao tráfego 1:1; deixe os grupos manter suas próprias chaves.
- Ao automatizar limpeza, excluir chaves individuais em vez de toda a loja para preservar o contexto em outro lugar.

# # Metadados de origem da sessão

Cada registro de entrada de sessão de onde veio (melhor esforço) em <<CODE0>>:

- <<CODE0>>: rótulo humano (resolvido a partir de rótulo de conversação + sujeito/canal de grupo)
- <<CODE1>>: id de canal normalizado (incluindo extensões)
- <<CODE2>>/<<CODE3>>: ids de encaminhamento bruto do envelope de entrada
- <<CODE4>>: id da conta do provedor (quando multi-conta)
- <<CODE5>>: thread/topic id quando o canal o suporta
Os campos de origem são povoados para mensagens diretas, canais e grupos. Se a
conector só atualiza roteamento de entrega (por exemplo, para manter uma sessão principal DM
a) deve ainda fornecer o contexto de entrada para que a sessão mantenha o seu
metadados explicadores. Extensões podem fazer isso enviando <<CODE6>>,
<<CODE7>>, <<CODE8>>, <<CODE9>>, e <<CODE10>> na entrada
contexto e chamada <<CODE11>>> (ou passar pelo mesmo contexto
<<CODE12>>>).
