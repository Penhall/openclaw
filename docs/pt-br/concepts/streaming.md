---
summary: "Streaming + chunking behavior (block replies, draft streaming, limits)"
read_when:
  - Explaining how streaming or chunking works on channels
  - Changing block streaming or channel chunking behavior
  - Debugging duplicate/early block replies or draft streaming
---

Fluxos + blocos

Openclaw tem duas camadas separadas de “streaming”:

- **Block streaming (canais):** emite **blocos completados** como o assistente escreve. Estas são mensagens de canal normais (não deltas de token).
- ** Transmissão token-ish (apenas no Telegram):** atualização de uma bolha ** com texto parcial durante a geração; mensagem final é enviada no final.

Há ** nenhuma transmissão real do token** para mensagens externas do canal hoje. A transmissão de rascunho de telegrama é a única superfície de fluxo parcial.

## Block streaming (mensagens de canal)

O streaming em bloco envia a saída do assistente em pedaços grossos à medida que se torna disponível.

```
Model output
  └─ text_delta/events
       ├─ (blockStreamingBreak=text_end)
       │    └─ chunker emits blocks as buffer grows
       └─ (blockStreamingBreak=message_end)
            └─ chunker flushes at message_end
                   └─ channel send (block replies)
```

Legenda:

-`text_delta/events`: eventos de fluxo modelo (pode ser esparso para modelos não-streaming).
-`chunker`:`EmbeddedBlockChunker`aplicando limites min/máx. + preferência de ruptura.
-`channel send`: mensagens de saída reais (respostas em bloco).

**Controles:**

-`agents.defaults.blockStreamingDefault`:`"on"`/`"off"`(default off).
- Substituição de canais:`*.blockStreaming`(e variantes por conta) para forçar`"on"`/`"off"`por canal.
-`agents.defaults.blockStreamingBreak`:`"text_end"`ou`"message_end"`.
-`agents.defaults.blockStreamingChunk`:`"on"`0.
-`"on"`1:`"on"`2 (blocos de fusão antes do envio).
- Tampa dura do canal:`"on"`3 (por exemplo,`"on"`4).
- Modo de bloco de canal:`"on"`5 `"on"`6 padrão,`"on"`7 divide em linhas em branco (limites de parágrafos) antes de blocos de comprimento).
- Discord soft cap:`"on"`8 (padrão 17) divide respostas altas para evitar o recorte de UI.

**Semântica de fronteira:**

-`text_end`: blocos de fluxo assim que o bloco emite; flush em cada`text_end`.
-`message_end`: espere até que a mensagem assistente termine, em seguida, flush buffered saída.

`message_end`ainda usa o bloco se o texto tamponado exceder o`maxChars`, para que possa emitir vários pedaços no final.

## Algoritmo de quebra (baixo/alto)

O bloco é implementado pelo`EmbeddedBlockChunker`:

- ** Baixo limite:** não emitir até buffer >=`minChars`(a menos que forçado).
- **Alto limite:** preferem divisões antes de`maxChars`; se forçado, dividido em`maxChars`.
- **Preferência de ruptura:**`paragraph`→`newline`→`sentence`→`whitespace`→ ruptura dura.
- ** Cercas de código:** nunca dividir dentro de cercas; quando forçado em`maxChars`, fechar + reabrir a cerca para manter Markdown válido.

`maxChars`está preso ao canal`textChunkLimit`, portanto você não pode exceder as tampas por canal.

## Coalescing (blocos de fusão fluídos)

Quando a transmissão de blocos está ativada, o OpenClaw pode ** misturar blocos consecutivos**
Antes de os enviar para fora. Isso reduz o “spam de linha única” enquanto ainda fornece
Produção progressiva.

- Coalescing espera por **gapsidle** `idleMs` antes de rubor.
- Os tampões são tampados pelo`maxChars`e irão ruborizar se excederem.
-`minChars`impede que pequenos fragmentos sejam enviados até que se acumule texto suficiente
(o flush final envia sempre o texto restante).
- Joiner é derivado de`blockStreamingChunk.breakPreference``paragraph`→`

`,`newline`→`
`,`sentence`→ espaço).
- As substituições de canais estão disponíveis via`*.blockStreamingCoalesce`(incluindo configurações por conta).
- Coalesce padrão`maxChars`0 é batido para 1500 para Signal / Slack / Discord, a menos que ultrapassado.

### Caminhando como um humano entre blocos

Quando o streaming do bloco está habilitado, você pode adicionar uma pausa ** aleatória** entre
respostas em bloco (após o primeiro bloco). Isto faz com que as respostas multi-bolha sentir
mais natural.

- Configuração:`agents.defaults.humanDelay`(sobrepor por agente via`agents.list[].humanDelay`.
- Modos:`off`(padrão),`natural`(800–2500ms),`custom``minMs`/`maxMs`.
- Aplica-se apenas a ** respostas em bloco **, não respostas finais ou resumos de ferramentas.

### “Pedaços ou tudo”

Este mapa para:

- ** Pedaços de estribo:**`blockStreamingDefault: "on"`+`blockStreamingBreak: "text_end"`(saída à medida que vai). Os canais de não-telegrama também precisam de`*.blockStreaming: true`.
- **Stream everything in end:**`blockStreamingBreak: "message_end"`(flush uma vez, possivelmente múltiplos pedaços se muito longo).
- ** Nenhuma transmissão em bloco:**`blockStreamingDefault: "off"`(apenas resposta final).

** Nota do canal:** Para canais não- Telegram, a transmissão em bloco é ** off a menos que**`*.blockStreaming`é explicitamente definido como`true`. Telegram pode transmitir rascunhos
`channels.telegram.streamMode` sem respostas em bloco.

Lembrete de localização de configuração: os padrões`blockStreaming*`estão ao vivo`agents.defaults`, não a configuração da raiz.

## Telegram rascunho de transmissão (token-ish)

O Telegram é o único canal com streaming de rascunho:

- Usa Bot API`sendMessageDraft`em ** chats privados com tópicos**.
-`channels.telegram.streamMode: "partial" | "block" | "off"`.
-`partial`: redigir atualizações com o texto mais recente.
-`block`: rascunho de atualizações em blocos em bloco (mesmas regras de blocos).
-`off`: nenhum rascunho.
- Projecto de configuração do bloco (apenas para`streamMode: "block"`:`channels.telegram.draftChunk`(por omissão:`minChars: 200`,`maxChars: 800`.
- A transmissão de rascunho é separada da transmissão de blocos; as respostas de blocos estão desligadas por padrão e somente ativadas pelo`*.blockStreaming: true`em canais não- Telegram.
- A resposta final ainda é uma mensagem normal.
-`channels.telegram.streamMode: "partial" | "block" | "off"`0 escreve raciocinando na bolha de rascunho (telegrama somente).

Quando o rascunho de streaming está ativo, o OpenClaw desabilita o streaming de blocos para essa resposta para evitar o duplo fluxo.

```
Telegram (private + topics)
  └─ sendMessageDraft (draft bubble)
       ├─ streamMode=partial → update latest text
       └─ streamMode=block   → chunker updates draft
  └─ final reply → normal message
```

Legenda:

-`sendMessageDraft`: bolha de rascunho de telegrama (não uma mensagem real).
-`final reply`: mensagem normal de Telegrama.
