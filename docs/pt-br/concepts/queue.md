---
summary: "Command queue design that serializes inbound auto-reply runs"
read_when:
  - Changing auto-reply execution or concurrency
---

# Fila de Comando (2026-01-16)

Nós serializamos as execuções de auto-resposta de entrada (todos os canais) através de uma pequena fila de processos para evitar que várias execuções de agentes colidam, ao mesmo tempo que ainda permite paralelismo seguro através de sessões.

# # Porque

- Auto-reply runs pode ser caro (chamadas LLM) e pode colidir quando várias mensagens de entrada chegam perto juntos.
- Serialização evita competir por recursos compartilhados (arquivos de sessão, logs, CLI stdin) e reduz a chance de limites de taxa a montante.

# # Como funciona

- Uma fila FIFO consciente da faixa drena cada faixa com uma tampa de concorrência configurável (padrão 1 para faixas não configuradas; padrões principais para 4, subagente para 8).
- <<CODE0> > em espera pela chave de sessão** (linha <<CODE1>>) para garantir apenas uma execução activa por sessão.
- Cada execução de sessão é então enfileirada em uma faixa **global** (<<<CODE2> por padrão) para que o paralelismo global seja limitado por <<CODE3>>>.
- Quando o registro de verbose está ativado, as execuções em fila de espera emitem um curto aviso se esperarem mais de ~2s antes de iniciar.
- Os indicadores de digitação ainda disparam imediatamente em fila (quando suportado pelo canal) para que a experiência do usuário fique inalterada enquanto esperamos nossa vez.

# # Modos de fila (por canal)

As mensagens de entrada podem orientar a execução atual, esperar por uma volta de seguimento, ou fazer ambas:

- <<CODE0>>: injetar imediatamente na execução atual (cancels pendentes chamadas de ferramenta após o próximo limite de ferramenta). Se não transmitir, volta para o seguimento.
- <<CODE1>>: em fila para a próxima volta do agente após o fim da execução atual.
- <<CODE2>: coalesce todas as mensagens em fila de espera em uma volta de seguimento **single** (padrão). Se as mensagens visam canais/threads diferentes, elas drenam individualmente para preservar o roteamento.
- <<CODE3>> (também conhecido por <HTML4>>>): conduzir agora **e** preservar a mensagem para uma volta de seguimento.
- <<CODE5> (legacy): aborte a execução ativa para essa sessão e, em seguida, execute a mensagem mais recente.
- <<CODE6> (alias de legado): o mesmo que <<CODE7>>>.

Steer-backlog significa que você pode obter uma resposta de seguimento após a corrida orientada, então
As superfícies de streaming podem parecer duplicatas. Preferir <<CODE0>/<<CODE1>> se quiser
Uma resposta por mensagem de entrada.
Enviar <<CODE2>> como um comando autônomo (por sessão) ou definido <<CODE3>>.

Por omissão (quando desactivado na configuração):

- Todas as superfícies → <<CODE0>>

Configurar globalmente ou por canal via <<CODE0>>:

```json5
{
  messages: {
    queue: {
      mode: "collect",
      debounceMs: 1000,
      cap: 20,
      drop: "summarize",
      byChannel: { discord: "collect" },
    },
  },
}
```

# # Opções da fila

As opções aplicam-se a <<CODE0>>, <<CODE1>>, e <<CODE2>> (e a <<CODE3>> quando o seguimento é retomado):

- <<CODE0>>: esperar silêncio antes de iniciar uma viragem de seguimento (preveni “ continuar, continuar”).
- <<CODE1>>: mensagens em fila máxima por sessão.
- <<CODE2>>: política de transbordamento (<<CODE3>>, <<CODE4>>, <<CODE5>>).

Resumir mantém uma lista curta de mensagens lançadas e injeta-as como um prompt de seguimento sintético.
Padrões: <<CODE0>>, <<CODE1>>, <<CODE2>>>.

# # Per-sessão substitui

- Envie <<CODE0>> como um comando autônomo para armazenar o modo para a sessão atual.
- As opções podem ser combinadas: <<CODE1>>
- <<CODE2>> ou <<CODE3> elimina o cancelamento da sessão.

# # Âmbito e garantias

- Aplica-se ao agente de resposta automática é executado em todos os canais de entrada que usam o gateway response pipeline (WhatsApp web, Telegram, Slack, Discord, Signal, iMessage, webchat, etc.).
- A faixa padrão (<<<CODE0>>) é de todo o processo para entrada + batimentos cardíacos principais; definido <<CODE1>> para permitir várias sessões em paralelo.
- Podem existir pistas adicionais (por exemplo, <<CODE2>>, <<CODE3>>>) para que as tarefas de fundo possam ser executadas em paralelo sem bloquear as respostas de entrada.
- As faixas por sessão garantem que apenas um agente corre toca uma determinada sessão de cada vez.
- Nenhuma dependência externa ou threads de trabalhador de fundo; puro TypeScript + promises.

# # Resolução de problemas

- Se os comandos parecerem emperrados, habilite os logs verbose e procure por linhas “em fila para ...ms” para confirmar que a fila está esgotando.
- Se precisar de profundidade na fila, habilite os logs de verbose e observe as linhas de tempo da fila.
