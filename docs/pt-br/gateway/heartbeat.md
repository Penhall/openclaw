---
summary: "Heartbeat polling messages and notification rules"
read_when:
  - Adjusting heartbeat cadence or messaging
  - Deciding between heartbeat and cron for scheduled tasks
---

Batimentos cardíacos

> **Heartbeat vs Cron?** Veja [Cron vs Heartbeat](<<<LINK0>>>) para orientação sobre quando usar cada.

Heartbeat corre ** agentes periódicos gira** na sessão principal para que o modelo possa
superfície qualquer coisa que precise de atenção sem spam você.

# # Início rápido (início)

1. Deixe batimentos cardíacos ativados (padrão é <<CODE0>>, ou <<CODE1>>> para OAuth/setup-token Antrópico) ou definir sua própria cadência.
2. Crie uma pequena lista de verificação <<CODE2>> no espaço de trabalho do agente (opcional, mas recomendado).
3. Decida onde as mensagens devem ir (<<<CODE3> é o padrão).
4. Opcional: permitir a entrega do raciocínio cardíaco para transparência.
5. Opcional: restringir os batimentos cardíacos às horas activas (hora local).

Configuração do exemplo:

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last",
        // activeHours: { start: "08:00", end: "24:00" },
        // includeReasoning: true, // optional: send separate `Reasoning:` message too
      },
    },
  },
}
```

Padrões

- Intervalo: <<CODE0>> (ou <<CODE1>> quando OAuth/setup-token Antrópico é o modo de autenticação detectado). Definir <<CODE2>> ou por agente <<CODE3>>>>; utilizar <<CODE4>>>> para desactivar.
- Corpo imediato (configurado via <<CODE5>>>):
<<CODE6>>
- O prompt cardíaco é enviado **verbatim** como a mensagem do usuário. O sistema
prompt inclui uma seção “Heartbeat” e a execução é marcada internamente.
- As horas activas (<<<CODE7>>) são verificadas no fuso horário configurado.
Fora da janela, os batimentos cardíacos são ignorados até o próximo tique dentro da janela.

# # Para que serve o coração?

O prompt padrão é intencionalmente amplo:

- **Antecedentes**: “Considera tarefas pendentes” estimula o agente a rever
follow-ups (caixa de entrada, calendário, lembretes, trabalho em fila) e surja qualquer coisa urgente.
- ** Check-in humano**: “Check-up às vezes no seu humano durante o dia”
ocasional leve “qualquer coisa que você precisa?” mensagem, mas evita spam noturno
usando seu fuso horário local configurado (veja [/conceitos/ fuso horário](<<<LINK0>>>)).

Se quiser que um batimento cardíaco faça algo muito específico (por exemplo, “verifique Gmail PubSub
stats” ou “verify gateway health”), definido <<CODE0>> (ou
<<CODE1>>) para um corpo personalizado (enviar verbatim).

# # Contrato de resposta

- Se nada precisar de atenção, responda com **<<<<CODE0>**.
- Durante os batimentos cardíacos, o OpenClaw trata <<CODE1>> como uma ack quando aparece
no ** início ou fim ** da resposta. O token é despojado e a resposta é
caiu se o conteúdo restante for ** <<CODE2>>** (padrão: 300).
- Se <<CODE3> aparecer no meio ** de uma resposta, não é tratado
especialmente.
- Para alertas, ** não inclui <<CODE4>>>; devolve apenas o texto de alerta.

Batimentos cardíacos externos, perdidos <<CODE0>> no início/fim de uma mensagem é despojado
e registrado; uma mensagem que é apenas <<CODE1>> é descartada.

Configuração

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m", // default: 30m (0m disables)
        model: "anthropic/claude-opus-4-5",
        includeReasoning: false, // default: false (deliver separate Reasoning: message when available)
        target: "last", // last | none | <channel id> (core or plugin, e.g. "bluebubbles")
        to: "+15551234567", // optional channel-specific override
        prompt: "Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.",
        ackMaxChars: 300, // max chars allowed after HEARTBEAT_OK
      },
    },
  },
}
```

## # Escopo e precedência

- <<CODE0> define o comportamento cardíaco global.
- <<CODE1> se funde no topo; se algum agente tiver <<CODE2>> block, ** apenas aqueles agentes** executar batimentos cardíacos.
- <<CODE3> define padrões de visibilidade para todos os canais.
- <<CODE4> sobrepõe os padrões do canal.
- <<CODE5> (canais multiconta) substitui as configurações por canal.

Batimentos cardíacos por agente

Se alguma entrada <<CODE0> incluir uma entrada <<CODE1>> bloco, ** apenas aqueles agentes**
Faça batimentos cardíacos. O bloco por agente se funde em cima de <<CODE2>>
(assim você pode definir padrões compartilhados uma vez e substituir por agente).

Exemplo: dois agentes, apenas o segundo agente executa batimentos cardíacos.

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last",
      },
    },
    list: [
      { id: "main", default: true },
      {
        id: "ops",
        heartbeat: {
          every: "1h",
          target: "whatsapp",
          to: "+15551234567",
          prompt: "Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.",
        },
      },
    ],
  },
}
```

Notas de campo

- <<CODE0>>: intervalo de batimento cardíaco (corda de duração; unidade padrão = minutos).
- <<CODE1>>: sobreposição opcional do modelo para corridas cardíacas (<<CODE2>>).
- <<CODE3>>: quando activada, também envia a mensagem separada <<CODE4>> quando disponível (a mesma forma que <<CODE5>>).
- <<CODE6>>: tecla de sessão opcional para corridas cardíacas.
- <<CODE7>> (padrão): sessão principal do agente.
- Chave de sessão explícita (cópia de <<CODE8>> ou da [sessões CLI](<<LINK0>>>)).
- Formatos-chave de sessão: ver [Sessões] (<<<LINK1>>) e [Grupos] (<<LINK2>>).
- <<CODE9>>:
- <<CODE10>> (padrão): entregue no último canal externo usado.
- canal explícito: <<CODE11>>/ <<CODE12>>/ <<CODE13>>/ <<CODE14>>/ <<CODE15>>/ <<CODE16>>/ <HTML20>>>/ <HTML21>>>.
- <<CODE19>>: executar o batimento cardíaco mas ** não administrar** externamente.
- <<CODE20>>: sobreposição opcional do destinatário (ID específico do canal, por exemplo, E.164 para WhatsApp ou um ID de chat do Telegram).
- <<CODE21>>: substitui o corpo de prompt padrão (não mesclado).
- <<CODE22>>: valores máximos permitidos após <<CODE23>> antes do parto.

# # Comportamento de entrega

- Heartbeats executado na sessão principal do agente por padrão (<<CODE0>>>),
ou <<CODE1> quando <<CODE2>>. Definir <<CODE3>> para sobrepor a
sessão de canal específica (Discord/WhatsApp/etc.).
- <<CODE4> só afecta o contexto de execução; a entrega é controlada por <<CODE5>> e <<CODE6>>.
- Para fornecer a um canal/ destinatário específico, definir <<CODE7>>> + <HTML8>>>>>. Com
<<CODE9>>, a entrega usa o último canal externo para essa sessão.
- Se a fila principal estiver ocupada, o batimento cardíaco é ignorado e repetido mais tarde.
- Se <<CODE10> resolver sem destino externo, a execução ainda acontece mas não
mensagem de saída é enviada.
- As respostas apenas de batimento cardíaco não ** mantêm a sessão viva; a última <<CODE11>>
é restaurado de modo que a expiração ociosa se comporta normalmente.

# # Controles de visibilidade

Por padrão, <<CODE0>> agradecimentos são suprimidos enquanto conteúdo alerta é
Entregue. Você pode ajustar isso por canal ou por conta:

```yaml
channels:
  defaults:
    heartbeat:
      showOk: false # Hide HEARTBEAT_OK (default)
      showAlerts: true # Show alert messages (default)
      useIndicator: true # Emit indicator events (default)
  telegram:
    heartbeat:
      showOk: true # Show OK acknowledgments on Telegram
  whatsapp:
    accounts:
      work:
        heartbeat:
          showAlerts: false # Suppress alert delivery for this account
```

Precedência: por conta → por canal → predefinições de canais → predefinições incorporadas.

O que cada bandeira faz

- <<CODE0>>: envia um <<CODE1>> reconhecimento quando o modelo retorna uma resposta somente OK.
- <<CODE2>>: envia o conteúdo de alerta quando o modelo retorna uma resposta não-OK.
- <<CODE3>: emite eventos indicadores para superfícies de estado da IU.

Se ** todos os três** são falsos, OpenClaw ignora o batimento cardíaco completamente (sem chamada de modelo).

## # Por canal vs por conta exemplos

```yaml
channels:
  defaults:
    heartbeat:
      showOk: false
      showAlerts: true
      useIndicator: true
  slack:
    heartbeat:
      showOk: true # all Slack accounts
    accounts:
      ops:
        heartbeat:
          showAlerts: false # suppress alerts for the ops account only
  telegram:
    heartbeat:
      showOk: true
```

Padrões comuns

□ Objetivo □ Configuração
-------------------------------------------------------- -------------------------------------------------------------------------------------------------------------------------
O comportamento padrão (silêncio OKs, alertas on)  (sem necessidade de configuração) 
* Totalmente silencioso (sem mensagens, sem indicador)
Apenas para indicadores (sem mensagens)
OK apenas num canal

# # HEARTBEAT.md (opcional)

Se um arquivo <<CODE0>> existe na área de trabalho, o prompt padrão diz a
Agente para o ler. Pense nisso como sua “checklist do coração”: pequeno, estável, e
seguro incluir a cada 30 minutos.

Se <<CODE0>> existir, mas estiver efetivamente vazio (apenas linhas em branco e marcação para baixo)
cabeçalhos como <<CODE1>>), OpenClaw ignora a execução do batimento cardíaco para salvar chamadas API.
Se o arquivo estiver faltando, o batimento cardíaco ainda é executado e o modelo decide o que fazer.

Mantenha-o minúsculo (checklist curto ou lembretes) para evitar inchaço imediato.

Exemplo <<CODE0>>:

```md
# Heartbeat checklist

- Quick scan: anything urgent in inboxes?
- If it’s daytime, do a lightweight check-in if nothing else is pending.
- If a task is blocked, write down _what is missing_ and ask Peter next time.
```

### O agente pode atualizar HEARTBEAT.Md?

Sim — se você pedir.

<<CODE0> é apenas um arquivo normal na área de trabalho do agente, então você pode dizer a
algo como:

- “Atualizar <<CODE0>> para adicionar uma verificação diária do calendário.”
- “Reescrever <<CODE1> para que seja mais curto e focado em acompanhamentos de caixa de entrada.”

Se você quiser que isso aconteça proativamente, você também pode incluir uma linha explícita em
seu coração pronto como: “Se a lista de verificação ficar velha, atualize HEARTBEAT.md
com uma melhor.”

Nota de segurança: não coloque segredos (chaves API, números de telefone, fichas privadas) em
<<CODE0>> — torna-se parte do contexto imediato.

# # Despertar manual (a pedido)

Você pode colocar um evento do sistema e ativar um batimento cardíaco imediato com:

```bash
openclaw system event --text "Check for urgent follow-ups" --mode now
```

Se vários agentes tiverem <<CODE0>>> configurado, um wake manual executa cada um desses
batimentos cardíacos do agente imediatamente.

Use <<CODE0>> para esperar pelo próximo tique agendado.

# # Razão da entrega (opcional)

Por padrão, os batimentos cardíacos fornecem apenas a carga útil final “resposta”.

Se você quiser transparência, habilite:

- <<CODE0>>

Quando activado, os batimentos cardíacos também irão fornecer uma mensagem separada prefixada
<<CODE0>> (a mesma forma que <<CODE1>>>). Isto pode ser útil quando o agente
está gerenciando várias sessões/codexes e você quer ver por que ele decidiu ping
você — mas também pode vazar mais detalhes internos do que você quer. Prefiro mantê-lo.
fora nas conversas em grupo.

# # Consciência de custo

Batimentos cardíacos fazem turnos de agente. Intervalos mais curtos queimam mais fichas. Manter
<<CODE0> pequeno e considere um mais barato <<CODE1>> ou <<CODE2>> se
só quer atualizações internas de estado.
