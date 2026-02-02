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

# # Fluxo de mensagens (alto nível)

```
Inbound message
  -> routing/bindings -> session key
  -> queue (if a run is active)
  -> agent run (streaming + tools)
  -> outbound replies (channel limits + chunking)
```

Os botões de teclas estão em configuração:

- <<CODE0>> para prefixos, filas e comportamento de grupo.
- <<CODE1>> para block streaming e blocking defaults.
- Substituições de canais (<<<CODE2>>, <<CODE3>>>, etc.) para tampas e botões de transmissão.

Ver [Configuração](<<<LINK0>>>) para esquema completo.

# # Inbound dedupe

Os canais podem devolver a mesma mensagem após reconectar. Openclaw mantém um
cache de curta duração chaveada pelo canal/conta/peer/session/message id para duplicar
as entregas não desencadeiam outra corrida de agentes.

# # Inbound debouncing

Mensagens consecutivas rápidas do mesmo remetente** podem ser agrupadas em um único
Virar por <<CODE0>>>. Debouncing é escopo por canal + conversa
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

# # Sessões e dispositivos

As sessões são propriedade do gateway, não dos clientes.

- Conversas directas entram em colapso na chave principal do agente.
- Grupos/canais têm suas próprias chaves de sessão.
- A loja de sessões e as transcrições estão ao vivo.

Vários dispositivos/canais podem mapear para a mesma sessão, mas o histórico não é totalmente
sincronizado com todos os clientes. Recomendação: usar um dispositivo primário por muito tempo
conversas para evitar contextos divergentes. A UI de controle e TUI sempre mostrar o
A transcrição da sessão suportada pelo gateway, então eles são a fonte da verdade.

Detalhes: [Gestão de sessão](<<<LINK0>>>).

# # Corpos de entrada e contexto histórico

OpenClaw separa o corpo **prompt** do corpo **command**:

- <<CODE0>>: texto imediato enviado ao agente. Isto pode incluir envelopes de canal e
invólucros de histórico opcional.
- <<CODE1>>: texto de utilizador bruto para análise de directivas/comandos.
- <<CODE2>>: apelido legado para <<CODE3>> (servido para compatibilidade).

Quando um canal fornece histórico, ele usa um invólucro compartilhado:

- <<CODE0>>
- <<CODE1>>

Para ** chats não-diretivos** (grupos/canais/quartos), o corpo da mensagem atual** é prefixado com o
sender label (o mesmo estilo usado para os itens do histórico). Isto mantém em tempo real e em fila/história
mensagens consistentes no prompt do agente.

Os buffers de histórico são **pending-only**: incluem mensagens de grupo que  not 
desencadeia uma execução (por exemplo, messagens expiradas por menção) e **exclua mensagens**
já na transcrição da sessão.

A remoção da diretiva só se aplica à seção **mensagem atual** então histórico
permanece intacta. Canais que embrulham o histórico devem definir <<CODE0>> (ou
<<CODE1>>) para o texto da mensagem original e manter <<CODE2>> como o prompt combinado.
Os buffers de histórico são configuráveis via <<CODE3>> (global
padrão) e substituições por canal como <<CODE4>> ou
<<CODE5> (set <<CODE6>> para desactivar).

# # Fila e seguimento

Se uma execução já estiver ativa, as mensagens de entrada podem ser em fila de espera, direcionadas para o
execução atual, ou coletado para uma volta de acompanhamento.

- Configurar via <<CODE0>> (e <HTML1>>>>>>).
- Modos: <<CODE2>>, <<CODE3>>, <<CODE4>>, <<CODE5>, mais variantes de backlog.

Detalhes: [Fila] (<<<LINK0>>>).

# # Fluxos, blocos e lotes

O streaming em bloco envia respostas parciais enquanto o modelo produz blocos de texto.
Chunking respeita limites de texto do canal e evita dividir código cercado.

Configuração da chave:

- <<CODE0> (<<CODE1>>, default off)
- <<CODE2> (<<CODE3>>>)
- <<CODE4> (<<CODE5>>)
- <<CODE6>
- <<CODE7>> (pausa tipo humano entre as respostas em bloco)
- Substituições de canais: <<CODE8>> e <<CODE9>> (canais de não-telegrama requerem explicitamente <<CODE10>>>)

Detalhes: [Streaming + blocking] (<<<LINK0>>>).

# # Raciocínio de visibilidade e fichas

Openclaw pode expor ou ocultar raciocínio de modelo:

- <<CODE0> controla a visibilidade.
- Raciocínio de conteúdo ainda conta para uso de token quando produzido pelo modelo.
- O telegrama suporta o fluxo de raciocínio na bolha de rascunho.

Detalhes: [Pensando + directivas de raciocínio](<<<LINK0>>) e [Uso Token](<<LINK1>>>).

# # Prefixos, threading e respostas

A formatação da mensagem de saída é centralizada em <<CODE0>>:

- <<CODE0> (prefixo de saída) e <<CODE1> (Prefixo de entrada do WhatsApp)
- Responder threading via <<CODE2>> e padrões por canal

Detalhes: [Configuração](<<<LINK0>>>) e documentos de canal.
