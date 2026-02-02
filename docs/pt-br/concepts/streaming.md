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

# # Block streaming (mensagens de canal)

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

- <<CODE0>>: eventos de fluxo de modelo (pode ser esparso para modelos não-streaming).
- <<CODE1>>: <<CODE2>> aplicando limites min/máx. + preferência de quebra.
- <<CODE3>>: mensagens de saída reais (respostas em bloco).

**Controles:**

- <<CODE0>>: <<CODE1>/<<CODE2>> (default off).
- Substituições de canais: <<CODE3> (e variantes por conta) para forçar <<CODE4>>/<<CODE5> por canal.
- <<CODE6>>: <<CODE7>> ou <<CODE8>>>.
- <<CODE9>>: <<CODE10>>>.
- <<CODE11>>: <<CODE12>> (blocos de fusão antes do envio).
- Cápsula de canal: <<CODE13>> (por exemplo, <<CODE14>>>).
- Modo de quebra de canal: <<CODE15>> (<<CODE16>default, <<CODE17>> splits em linhas em branco (limites de parágrafo) antes de blocos de comprimento).
- Discord soft cap: <<CODE18> (padrão 17) divide respostas altas para evitar recorte de IU.

**Semântica de fronteira:**

- <<CODE0>>: blocos de corrente assim que o blocker emite; flush em cada <<CODE1>>.
- <<CODE2>>: esperar até que a mensagem assistente termine, em seguida, flush buffered output.

<<CODE0> ainda usa o blocker se o texto tamponado exceder <<CODE1>>, para que possa emitir vários pedaços no final.

# # Algoritmo de quebra (baixo/alto)

O bloco é implementado por <<CODE0>>>:

- ** Baixo limite:** Não emitir até buffer >= <<CODE0>> (a menos que forçado).
- **Ligação elevada:** preferem divisões antes de <<CODE1>>; se forçadas, divididas em <<CODE2>>>.
- **Preferência de interrupção:** <<CODE3>> → <<CODE4>> → <<CODE5>> → <<CODE6> → quebra dura.
- ** Cercas de código:** nunca dividir dentro de cercas; quando forçado em <<CODE7>>, fechar + reabrir a cerca para manter Markdown válido.

<<CODE0> é preso ao canal <<CODE1>>, assim você não pode exceder as tampas por canal.

# # Coalescing (blocos de fusão fluídos)

Quando a transmissão de blocos está ativada, o OpenClaw pode ** misturar blocos consecutivos**
Antes de os enviar para fora. Isso reduz o “spam de linha única” enquanto ainda fornece
Produção progressiva.

- Coalescing espera por **gaps ** (<<<CODE0>>) antes de rubor.
- Os tampões são tampados por <<CODE1> e irão ruborizar se o excederem.
- <<CODE2>> impede que pequenos fragmentos sejam enviados até que se acumule texto suficiente
(o flush final envia sempre o texto restante).
- Joiner é derivado de <<CODE3>>
(<<<CODE4>> → <<CODE5>>, <<CODE6>> → <<CODE7>, <<CODE8>> → espaço).
- Substituições de canais estão disponíveis via <<CODE9>> (incluindo as configurações por conta).
- Coalesce padrão <<CODE10> é batido para 1500 para Signal/Slack/Discord, a menos que anulado.

# # # Caminhando como um humano entre blocos

Quando o streaming do bloco está habilitado, você pode adicionar uma pausa ** aleatória** entre
respostas em bloco (após o primeiro bloco). Isto faz com que as respostas multi-bolha sentir
mais natural.

- Configuração: <<CODE0>> (sobrepor por agente via <<CODE1>>>).
- Modos: <<CODE2>> (padrão), <<CODE3>> (800–2500ms), <<CODE4>> (<<CODE5>/<<CODE6>>>).
- Aplica-se apenas a ** respostas em bloco **, não respostas finais ou resumos de ferramentas.

# # # “Pedaços ou tudo”

Este mapa para:

- ** Pedaços de estribo:** < <<CODE0>> + <<CODE1>> (emigre à medida que avança). Os canais de não-telegrama também necessitam de <<CODE2>>.
- ** Rastreie tudo no final:** <<CODE3>>> (flush uma vez, possivelmente vários pedaços se muito longo).
- ** Nenhuma transmissão em bloco:** <<CODE4>> (apenas resposta final).

** Nota do canal:** Para canais não- Telegram, a transmissão em bloco é ** off a menos que**
<<CODE0> é explicitamente definido como <<CODE1>>>. Telegram pode transmitir rascunhos
(<<<CODE2>>) sem respostas em bloco.

Lembrete de localização de configuração: os padrões <<CODE0> ao vivo
<<CODE1>>, não a configuração da raiz.

# # Telegram rascunho de transmissão (token-ish)

O Telegram é o único canal com streaming de rascunho:

- Usa API bot <<CODE0>> em ** chats privados com tópicos**.
- <<CODE1>>>.
- <<CODE2>>: rascunho de atualizações com o texto mais recente.
- <<CODE3>>: rascunho de atualizações em blocos em bloco (mesma regra de blocos).
- <<CODE4>>: nenhuma transmissão de rascunho.
- Configuração de blocos de rascunho (somente para <<CODE5>>): <<CODE6>> (padrão: <<CODE7>>, <<CODE8>>).
- A transmissão de rascunho é separada da transmissão de blocos; as respostas de blocos são desligadas por padrão e somente ativadas por <<CODE9>> em canais não-Telegram.
- A resposta final ainda é uma mensagem normal.
- <<CODE10> escreve o raciocínio na bolha de rascunho (apenas no Telegrama).

Quando o rascunho de streaming está ativo, o OpenClaw desabilita o streaming de blocos para essa resposta para evitar o duplo fluxo.

```
Telegram (private + topics)
  └─ sendMessageDraft (draft bubble)
       ├─ streamMode=partial → update latest text
       └─ streamMode=block   → chunker updates draft
  └─ final reply → normal message
```

Legenda:

- <<CODE0>>: Bubble de rascunho de telegrama (não é uma mensagem real).
- <<CODE1>>: envio normal de mensagens de Telegrama.
