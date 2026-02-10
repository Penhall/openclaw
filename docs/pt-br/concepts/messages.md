---
summary: "Message flow, sessions, queueing, and reasoning visibility"
read_when:
  - Explaining how inbound messages become replies
  - Clarifying sessions, queueing modes, or streaming behavior
  - Documenting reasoning visibility and usage implications
---

Mensagens

Esta página liga-se como o OpenClaw lida com mensagens, sessões, filas de espera,
streaming, e visibilidade de raciocínio.

## Fluxo de mensagens (alto nível)

```
Inbound message
  -> routing/bindings -> session key
  -> queue (if a run is active)
  -> agent run (streaming + tools)
  -> outbound replies (channel limits + chunking)
```

Os botões de teclas estão em configuração:

-`messages.*`para prefixos, filas e comportamento de grupo.
-`agents.defaults.*`para block streaming e blocing defaults.
- Substituições de canais `channels.whatsapp.*`,`channels.telegram.*`, etc.) para tampas e botões de transmissão.

Ver [Configuração]/gateway/configuration para esquema completo.

## Inbound dedupe

Os canais podem devolver a mesma mensagem após reconectar. Openclaw mantém um
cache de curta duração chaveada pelo canal/conta/peer/session/message id para duplicar
as entregas não desencadeiam outra corrida de agentes.

## Inbound debouncing

Mensagens consecutivas rápidas do mesmo remetente** podem ser agrupadas em um único
Agente ligado via`messages.inbound`. Debouncing é escopo por canal + conversa
e usa a mensagem mais recente para resposta threading/IDs.

Configuração (padrão global + sobreposições por canal):

```json5
{
  messages: {
    inbound: {
      debounceMs: 2000,
      byChannel: {
        whatsapp: 5000,
        slack: 1500,
        discord: 1500,
      },
    },
  },
}
```

Notas:

- Debounce aplica-se a ** apenas texto** mensagens; mídia/attachments flush imediatamente.
- Comandos de controlo a desligar para que permaneçam independentes.

## Sessões e dispositivos

As sessões são propriedade do gateway, não dos clientes.

- Conversas directas entram em colapso na chave principal do agente.
- Grupos/canais têm suas próprias chaves de sessão.
- A loja de sessões e as transcrições estão ao vivo.

Vários dispositivos/canais podem mapear para a mesma sessão, mas o histórico não é totalmente
sincronizado com todos os clientes. Recomendação: usar um dispositivo primário por muito tempo
conversas para evitar contextos divergentes. A UI de controle e TUI sempre mostrar o
A transcrição da sessão suportada pelo gateway, então eles são a fonte da verdade.

Detalhes: [Gestão de sessão] /concepts/session.

## Corpos de entrada e contexto histórico

OpenClaw separa o corpo **prompt** do corpo **command**:

-`Body`: texto rápido enviado ao agente. Isto pode incluir envelopes de canal e
invólucros de histórico opcional.
-`CommandBody`: texto de usuário bruto para análise de diretiva/comando.
-`RawBody`: apelido antigo para`CommandBody`(mantido para compatibilidade).

Quando um canal fornece histórico, ele usa um invólucro compartilhado:

-`[Chat messages since your last reply - for context]`-`[Current message - respond to this]`

Para ** chats não-diretivos** (grupos/canais/quartos), o corpo da mensagem atual** é prefixado com o
sender label (o mesmo estilo usado para os itens do histórico). Isto mantém em tempo real e em fila/história
mensagens consistentes no prompt do agente.

Os buffers de histórico são **pending-only**: incluem mensagens de grupo que  not 
desencadeia uma execução (por exemplo, messagens expiradas por menção) e **exclua mensagens**
já na transcrição da sessão.

A remoção da diretiva só se aplica à seção **mensagem atual** então histórico
permanece intacta. Canais que embrulham o histórico devem definir`CommandBody`(ou`RawBody` para o texto da mensagem original e manter`Body`como o alerta combinado.
Os buffers de histórico são configuráveis via`messages.groupChat.historyLimit`(global
padrão) e sobreposições por canal como`channels.slack.historyLimit`ou`channels.telegram.accounts.<id>.historyLimit`(define`0`para desactivar).

## Fila e seguimento

Se uma execução já estiver ativa, as mensagens de entrada podem ser em fila de espera, direcionadas para o
execução atual, ou coletado para uma volta de acompanhamento.

- Configurar via`messages.queue`(e`messages.queue.byChannel`.
- Modos:`interrupt`,`steer`,`followup`,`collect`, mais variantes de atraso.

Detalhes: [Fila] /concepts/queue.

## Fluxos, blocos e lotes

O streaming em bloco envia respostas parciais enquanto o modelo produz blocos de texto.
Chunking respeita limites de texto do canal e evita dividir código cercado.

Configuração da chave:

-`agents.defaults.blockStreamingDefault``on|off`, default off)
-`agents.defaults.blockStreamingBreak``text_end|message_end`
-`agents.defaults.blockStreamingChunk``minChars|maxChars|breakPreference`
-`agents.defaults.blockStreamingCoalesce`-`agents.defaults.humanDelay`(pausa humana entre as respostas em bloco)
- Substituições de canais:`*.blockStreaming`e`*.blockStreamingCoalesce`(canais de não-telegrama requerem`on|off`0)

Detalhes: [Streaming + blocking] /concepts/streaming.

## Raciocínio de visibilidade e fichas

Openclaw pode expor ou ocultar raciocínio de modelo:

-`/reasoning on|off|stream`controla a visibilidade.
- Raciocínio de conteúdo ainda conta para uso de token quando produzido pelo modelo.
- O telegrama suporta o fluxo de raciocínio na bolha de rascunho.

Detalhes: [Pensando + diretivas de raciocínio]/tools/thinking e [Uso de token]/token-use.

## Prefixos, threading e respostas

Formatação de mensagens de saída é centralizada em`messages`:

-`messages.responsePrefix`(prefixo de saída) e`channels.whatsapp.messagePrefix`(prefixo de entrada WhatsApp)
- Responder threading via`replyToMode`e por canal padrão

Detalhes: [Configuração] /gateway/configuration#messages e documentos de canal.
