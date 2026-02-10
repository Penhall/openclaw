---
summary: "Command queue design that serializes inbound auto-reply runs"
read_when:
  - Changing auto-reply execution or concurrency
---

# Fila de Comando (2026-01-16)

Nós serializamos as execuções de auto-resposta de entrada (todos os canais) através de uma pequena fila de processos para evitar que várias execuções de agentes colidam, ao mesmo tempo que ainda permite paralelismo seguro através de sessões.

## Porque

- Auto-reply runs pode ser caro (chamadas LLM) e pode colidir quando várias mensagens de entrada chegam perto juntos.
- Serialização evita competir por recursos compartilhados (arquivos de sessão, logs, CLI stdin) e reduz a chance de limites de taxa a montante.

## Como funciona

- Uma fila FIFO consciente da faixa drena cada faixa com uma tampa de concorrência configurável (padrão 1 para faixas não configuradas; padrões principais para 4, subagente para 8).
-`runEmbeddedPiAgent`em espera pela chave de sessão** (linha`session:<key>` para garantir apenas uma execução activa por sessão.
- Cada execução de sessão é então enfileirada em uma faixa **global** `main`por padrão) para que o paralelismo global seja cappado por`agents.defaults.maxConcurrent`.
- Quando o registro de verbose está ativado, as execuções em fila de espera emitem um curto aviso se esperarem mais de ~2s antes de iniciar.
- Os indicadores de digitação ainda disparam imediatamente em fila (quando suportado pelo canal) para que a experiência do usuário fique inalterada enquanto esperamos nossa vez.

## Modos de fila (por canal)

As mensagens de entrada podem orientar a execução atual, esperar por uma volta de seguimento, ou fazer ambas:

-`steer`: injete imediatamente na execução atual (cancela chamadas pendentes de ferramentas após o próximo limite de ferramentas). Se não transmitir, volta para o seguimento.
-`followup`: em fila para a próxima volta do agente após a execução atual terminar.
-`collect`: coalesce todas as mensagens em fila de espera em um ** single** turno de seguimento (padrão). Se as mensagens visam canais/threads diferentes, elas drenam individualmente para preservar o roteamento.
-`steer-backlog`(também conhecido por`steer+backlog`: dirigir agora **e** preservar a mensagem para uma volta de acompanhamento.
-`interrupt`(legacy): aborte a execução ativa para essa sessão e, em seguida, execute a nova mensagem.
-`queue`(alias de legado): o mesmo que`steer`.

Steer-backlog significa que você pode obter uma resposta de seguimento após a corrida orientada, então
As superfícies de streaming podem parecer duplicatas. Prefere`collect`/`steer`se quiser
Uma resposta por mensagem de entrada.
Enviar`/queue collect`como um comando autônomo (por sessão) ou definir`messages.queue.byChannel.discord: "collect"`.

Por omissão (quando desactivado na configuração):

- Todas as superfícies →`collect`

Configurar globalmente ou por canal via`messages.queue`:

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

## Opções da fila

As opções aplicam-se ao`followup`, ao`collect`e ao`steer-backlog`(e ao`steer`quando este for retomado):

-`debounceMs`: esperar silêncio antes de iniciar uma viragem de seguimento (prevendo “continuar, continuar”).
-`cap`: mensagens máximas em fila por sessão.
- OUTXCODE2: política de transbordamento `old`,`new`,`summarize`.

Resumir mantém uma lista curta de mensagens lançadas e injeta-as como um prompt de seguimento sintético.
Padrões:`debounceMs: 1000`,`cap: 20`,`drop: summarize`.

## Per-sessão substitui

- Envie`/queue <mode>`como um comando independente para armazenar o modo para a sessão atual.
- Opções podem ser combinadas:`/queue collect debounce:2s cap:25 drop:summarize`-`/queue default`ou`/queue reset`autoriza o cancelamento da sessão.

## Âmbito e garantias

- Aplica-se ao agente de resposta automática é executado em todos os canais de entrada que usam o gateway response pipeline (WhatsApp web, Telegram, Slack, Discord, Signal, iMessage, webchat, etc.).
- A faixa padrão `main` é ampla para o processo de entrada + batimentos cardíacos principais; definir`agents.defaults.maxConcurrent`para permitir várias sessões em paralelo.
- Podem existir pistas adicionais (por exemplo,`cron`,`subagent` para que os trabalhos de base possam funcionar em paralelo sem bloquear as respostas de entrada.
- As faixas por sessão garantem que apenas um agente corre toca uma determinada sessão de cada vez.
- Nenhuma dependência externa ou threads de trabalhador de fundo; puro TypeScript + promises.

## Resolução de problemas

- Se os comandos parecerem emperrados, habilite os logs verbose e procure por linhas “em fila para ...ms” para confirmar que a fila está esgotando.
- Se precisar de profundidade na fila, habilite os logs de verbose e observe as linhas de tempo da fila.
