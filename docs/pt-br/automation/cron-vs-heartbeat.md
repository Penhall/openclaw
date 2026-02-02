---
summary: "Guidance for choosing between heartbeat and cron jobs for automation"
read_when:
  - Deciding how to schedule recurring tasks
  - Setting up background monitoring or notifications
  - Optimizing token usage for periodic checks
---

# Cron vs Heartbeat: Quando usar cada

Ambos os batimentos cardíacos e trabalhos de cron permitem executar tarefas em um cronograma. Este guia ajuda você a escolher o mecanismo certo para o seu caso de uso.

## Guia de Decisão Rápida

Caso de uso Recomendado
---------------------------------------------------- ------------------- -------------------- ---------------------------------------
Verificar caixa de entrada a cada 30 minutos Batimentos cardíacos com outras verificações, contexto consciente
Enviar relatório diário às 9h afiadas
Monitore o calendário para os próximos eventos
□ Execute análise profunda semanal □ Cron (isolado) □ tarefa autônoma, pode usar modelo diferente
Lembre-me em 20 minutos Cron (principal,`--at`
• Verificação de saúde do projeto de fundo

## Batimento cardíaco: Consciência periódica

Os batimentos cardíacos são executados na **sessão principal** em um intervalo regular (padrão: 30 min). Foram feitos para o agente verificar as coisas e revelar tudo o que fosse importante.

Quando usar o batimento cardíaco

- ** Várias verificações periódicas**: Em vez de 5 trabalhos de cron separados, verificando caixa de entrada, calendário, tempo, notificações e status do projeto, um único batimento cardíaco pode lotear todos estes.
- ** Decisões conscientes do contexto**: O agente tem todo o contexto de sessão principal, então pode tomar decisões inteligentes sobre o que é urgente vs. o que pode esperar.
- **Continuidade conversacional**: Correções de batimento cardíaco compartilham a mesma sessão, para que o agente se lembre de conversas recentes e possa acompanhar naturalmente.
- ** Monitorização com baixa overhead**: Um batimento cardíaco substitui muitas pequenas tarefas de votação.

Vantagens do batimento cardíaco

- **Batches múltiplas verificações**: Um agente gira pode rever caixa de entrada, calendário e notificações juntos.
- **Reduz chamadas de API**: Um único batimento cardíaco é mais barato do que 5 trabalhos isolados.
- **Contexto consciente**: O agente sabe no que tens trabalhado e pode priorizar de acordo.
- ** Supressão inteligente**: Se nada precisa de atenção, o agente responde`HEARTBEAT_OK`e nenhuma mensagem é entregue.
- ** Tempo natural**: Deriva ligeiramente com base na carga da fila, o que é bom para a maioria do monitoramento.

## # Exemplo de batimento cardíaco: HEARTBBEAT.md checklist

```md
# Heartbeat checklist

- Check email for urgent messages
- Review calendar for events in next 2 hours
- If a background task finished, summarize results
- If idle for 8+ hours, send a brief check-in
```

O agente lê isto em cada batimento cardíaco e lida com todos os itens de uma só vez.

Configurando o batimento cardíaco

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m", // interval
        target: "last", // where to deliver alerts
        activeHours: { start: "08:00", end: "22:00" }, // optional
      },
    },
  },
}
```

Veja [Heartbeat]/gateway/heartbeat para configuração completa.

## Cron: Programação precisa

Os trabalhos de Cron são executados em **tempos exatos** e podem ser executados em sessões isoladas sem afetar o contexto principal.

Quando usar cron

- ** É necessário o tempo exato**: "Enviar isso às 9:00 todas as segundas-feiras" (não "em algum momento por volta das 9").
- **Tarefas estandardizadas**: Tarefas que não precisam de contexto conversacional.
- **Diferente modelo/pensamento**: Análise pesada que requer um modelo mais poderoso.
- ** Lembra-te de mim em 20 minutos com`--at`.
- **Tarefas frequentes/ruidosas**: Tarefas que estragariam o histórico da sessão principal.
- Activadores externos**: Tarefas que devem ser executadas independentemente de o agente estar de outra forma ativo.

## Vantagens do Cron

- **Tingimento exato**: expressões de cron de 5 campos com suporte a fuso horário.
- ** Isolação de sessão**: Funciona em`cron:<jobId>`sem poluir a história principal.
- **Modelo de substituição**: Use um modelo mais barato ou mais poderoso por trabalho.
- ** Controlo da entrega**: Pode entregar diretamente para um canal; ainda publica um resumo para main por padrão (configurado).
- ** Nenhum contexto de agente necessário**: Executa mesmo se a sessão principal estiver ociosa ou compactada.
- ** Suporte a um tiro**:`--at`para datas futuras precisas.

## # Exemplo de Cron: Briefing diário da manhã

```bash
openclaw cron add \
  --name "Morning briefing" \
  --cron "0 7 * * *" \
  --tz "America/New_York" \
  --session isolated \
  --message "Generate today's briefing: weather, calendar, top emails, news summary." \
  --model opus \
  --deliver \
  --channel whatsapp \
  --to "+15551234567"
```

Isso é executado exatamente às 7:00 horas da hora de Nova Iorque, usa Opus para qualidade, e entrega diretamente para WhatsApp.

## # Exemplo de Cron: lembrete de um tiro

```bash
openclaw cron add \
  --name "Meeting reminder" \
  --at "20m" \
  --session main \
  --system-event "Reminder: standup meeting starts in 10 minutes." \
  --wake now \
  --delete-after-run
```

Ver [Trabalhos Cron]/automation/cron-jobs para uma referência CLI completa.

## Fluxograma de Decisão

```
Does the task need to run at an EXACT time?
  YES -> Use cron
  NO  -> Continue...

Does the task need isolation from main session?
  YES -> Use cron (isolated)
  NO  -> Continue...

Can this task be batched with other periodic checks?
  YES -> Use heartbeat (add to HEARTBEAT.md)
  NO  -> Use cron

Is this a one-shot reminder?
  YES -> Use cron with --at
  NO  -> Continue...

Does it need a different model or thinking level?
  YES -> Use cron (isolated) with --model/--thinking
  NO  -> Use heartbeat
```

## Combinando ambos

A configuração mais eficiente usa ** ambos**:

1. **Heartbeat** lida com monitoramento de rotina (caixa de entrada, calendário, notificações) em uma volta em lote a cada 30 minutos.
2. **Cron** lida com horários precisos (relatórios diários, revisões semanais) e lembretes de um tiro.

Exemplo: Configuração eficiente da automação

** HEARTBEAT.md** (verificado a cada 30 minutos):

```md
# Heartbeat checklist

- Scan inbox for urgent emails
- Check calendar for events in next 2h
- Review any pending tasks
- Light check-in if quiet for 8+ hours
```

**Cron jobs** (tempo preciso):

```bash
# Daily morning briefing at 7am
openclaw cron add --name "Morning brief" --cron "0 7 * * *" --session isolated --message "..." --deliver

# Weekly project review on Mondays at 9am
openclaw cron add --name "Weekly review" --cron "0 9 * * 1" --session isolated --message "..." --model opus

# One-shot reminder
openclaw cron add --name "Call back" --at "2h" --session main --system-event "Call back the client" --wake now
```

## Lagosta: fluxos de trabalho determinísticos com aprovações

Lagosta é o tempo de execução do fluxo de trabalho para ** pipelines de ferramentas multi-step** que precisam de execução determinística e aprovações explícitas.
Use-o quando a tarefa for mais do que um único agente, e você deseja um fluxo de trabalho reutilizável com pontos de verificação humanos.

Quando a lagosta se encaixa

- Automatização multi-passo**: Você precisa de um pipeline fixo de chamadas de ferramentas, não um prompt único.
- ** Portões de aprovação**: Os efeitos secundários devem parar até que você aprove e então retomar.
- **Rentes recuperáveis**: Continue um fluxo de trabalho pausado sem repetir os passos anteriores.

### Como se emparelha com batimentos cardíacos e cron

- **Heartbeat/cron** decide quando acontece uma corrida.
- **Lobster** define  o que passos  acontecem quando a execução começa.

Para fluxos de trabalho programados, use cron ou batimento cardíaco para ativar um agente que chama Lobster.
Para fluxos de trabalho ad-hoc, ligue diretamente para a Lagosta.

## # Notas operacionais (a partir do código)

- A lagosta é executada como um subprocesso local** `lobster`CLI) no modo de ferramenta e retorna um envelope ** JSON**.
- Se a ferramenta retornar`needs_approval`, você retoma com uma bandeira`resumeToken`e`approve`.
- A ferramenta é um plugin ** opcional**; habilite-o aditivamente via`tools.alsoAllow: ["lobster"]`(recomendado).
- Se passar o`lobsterPath`, deve ser um caminho absoluto**.

Ver [Lobster]/tools/lobster para uso completo e exemplos.

## Sessão Principal vs Sessão Isolada

Tanto o batimento cardíaco como o cron podem interagir com a sessão principal, mas de forma diferente:

* Batimento cardíaco * Cron (principal) * Cron (isolado) *
-------- ---------------------- ------------- -----------
Sessão . . Principal . (via evento do sistema) . .
História Partilhada Partilhada
* Contexto completo * Nenhum (começa limpo) *
O modelo principal da sessão do modelo principal do modelo da sessão principal pode sobrepor-se
□ Saída □ Entregue se não`HEARTBEAT_OK`

## # Quando usar o cron da sessão principal

Use`--session main`com`--system-event`quando quiser:

- O lembrete/evento a aparecer no contexto da sessão principal
- O agente para lidar com isso durante o próximo batimento cardíaco com contexto completo
- Nenhuma corrida isolada

```bash
openclaw cron add \
  --name "Check project" \
  --every "4h" \
  --session main \
  --system-event "Time for a project health check" \
  --wake now
```

## Quando usar cron isolado

Use`--session isolated`quando quiser:

- Uma ficha limpa sem contexto prévio
- Diferentes configurações de modelo ou pensamento
- Saída entregue diretamente em um canal (síntese ainda posta em main por padrão)
- História que não estraga a sessão principal

```bash
openclaw cron add \
  --name "Deep analysis" \
  --cron "0 6 * * 0" \
  --session isolated \
  --message "Weekly codebase analysis..." \
  --model opus \
  --thinking high \
  --deliver
```

## Considerações de Custo

□ Mecanismo
----------------- ----------------------------------------------------------------------
* Batimento cardíaco * Uma vez a cada N minutos; escalas com tamanho HEARTBEAT.md *
* Cron (principal) * Adiciona o evento ao próximo batimento cardíaco (sem turno isolado) *
• Cron (isolado) • Agente completo turno por trabalho; pode usar modelo mais barato

** Dicas**:

- Mantenha`HEARTBEAT.md`pequeno para minimizar a sobrecarga do token.
- Cheques semelhantes no batimento cardíaco em vez de múltiplas tarefas.
- Use`target: "none"`no batimento cardíaco se você só quer processamento interno.
- Use cron isolado com um modelo mais barato para tarefas de rotina.

## Relacionado

Configuração do batimento cardíaco
- [Trabalhos de Cron] /automation/cron-jobs - referência CLI de Cron completo e API
- [Sistema] /cli/system - eventos do sistema + controles cardíacos
