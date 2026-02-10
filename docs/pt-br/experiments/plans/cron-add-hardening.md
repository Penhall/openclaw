---
summary: "Harden cron.add input handling, align schemas, and improve cron UI/agent tooling"
owner: "openclaw"
status: "complete"
last_updated: "2026-01-05"
---

# Cron Adicionar Endurecimento & Esquema Alinhamento

## Contexto

Os logs de gateway recentes mostram falhas repetidas do`cron.add`com parâmetros inválidos (falta de`sessionTarget`,`wakeMode`,`payload`e`schedule`. Isso indica que pelo menos um cliente (provavelmente o caminho de chamada da ferramenta do agente) está enviando cargas de trabalho parcialmente especificadas. Separadamente, há deriva entre enums de provedor de cron no TypeScript, esquema de gateway, bandeiras de CLI e tipos de formulário de UI, além de uma incompatibilidade de UI para`cron.status`(espera`jobCount`enquanto gateway retorna`jobs`.

## Objetivos

- Pare`cron.add`INVALID REQUEST spam, normalizando as cargas de embrulho comuns e inferindo campos`kind`.
- Alinhar listas de provedor de cron através do esquema gateway, tipos de cron, documentos CLI e formulários de UI.
- Tornar o esquema de ferramenta do agente cron explícito para que o LLM produza cargas de trabalho corretas.
- Corrigir a exibição Control UI status cron work count.
- Adicione testes para cobrir normalização e comportamento da ferramenta.

## Não-objetivos

- Mude a semântica de agendamento ou o comportamento de execução de tarefas.
- Adicione novos tipos de programação ou análise de expressão de cron.
- Reveja a UI/UX para cron além das correções de campo necessárias.

## Achados (gaps atuais)

-`CronPayloadSchema`no gateway exclui`signal`+`imessage`, enquanto os tipos TS os incluem.
- Controle UI CronStatus espera`jobCount`, mas o gateway retorna`jobs`.
- Esquema de ferramenta do agente cron permite objetos`job`arbitrários, permitindo entradas malformadas.
- Gateway valida estritamente`cron.add`sem normalização, por isso as cargas úteis envolto falhar.

## O que mudou

-`cron.add`e`cron.update`agora normalizam formas comuns de invólucro e infer campos`kind`.
- O esquema de ferramenta do Agente Cron corresponde ao esquema de gateway, o que reduz as cargas inválidas.
- Enums de provedores estão alinhados entre gateway, CLI, UI e macOS.
- Controlar UI usa o campo de contagem`jobs`do gateway para o status.

## Comportamento atual

- ** Normalização:**`data`/`job`desembrulhados;`schedule.kind`e`payload.kind`são inferidos quando seguros.
- **Padrões:** padrões seguros são aplicados para`wakeMode`e`sessionTarget`quando faltando.
- **Fornecedores:** Discórdia/Slack/Sinal/iMessage são agora consistentemente superfície através de CLI/UI.

Veja [Trabalhos de Cron]/automation/cron-jobs para a forma e exemplos normalizados.

## Verificação

- Assista logs de gateway para erros`cron.add`INVALID REQUEST reduzidos.
- Confirmar Controle UI cron status mostra contagem de tarefas após atualização.

## Acompanhamentos Opcionais

- Manual Control UI smoke: adicionar um trabalho de cron por provedor + verificar a contagem de trabalho de status.

## Perguntas abertas

- Deve`cron.add`aceitar`state`explícito de clientes (atualmente não permitido pelo esquema)?
- Devemos permitir o`webchat`como um provedor de entrega explícito (atualmente filtrado em resolução de entrega)?
