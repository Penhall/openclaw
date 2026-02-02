---
summary: "Harden cron.add input handling, align schemas, and improve cron UI/agent tooling"
owner: "openclaw"
status: "complete"
last_updated: "2026-01-05"
---

# Cron Adicionar Endurecimento & Esquema Alinhamento

# # Contexto

Registros de gateway recentes mostram falhas repetidas <<CODE0>> com parâmetros inválidos (falta de <<CODE1>>, <<CODE2>>, <<CODE3>>, e deformadas <<CODE4>>>>). Isso indica que pelo menos um cliente (provavelmente o caminho de chamada da ferramenta do agente) está enviando cargas de trabalho parcialmente especificadas. Separadamente, há deriva entre os enumes de provedor de cron no TypeScript, esquema de gateway, bandeiras de CLI e tipos de formulário de UI, além de uma incompatibilidade de UI para <<CODE5>> (espera <<CODE6>> enquanto gateway retorna <<CODE7>>).

# # Objetivos

- Pare <<CODE0>> INVALID REQUEST spam, normalizando as cargas comuns de embrulho e inferindo falta <<CODE1> campos.
- Alinhar listas de provedor de cron através do esquema gateway, tipos de cron, documentos CLI e formulários de UI.
- Tornar o esquema de ferramenta do agente cron explícito para que o LLM produza cargas de trabalho corretas.
- Corrigir a exibição Control UI status cron work count.
- Adicione testes para cobrir normalização e comportamento da ferramenta.

# # Não-objetivos

- Mude a semântica de agendamento ou o comportamento de execução de tarefas.
- Adicione novos tipos de programação ou análise de expressão de cron.
- Reveja a UI/UX para cron além das correções de campo necessárias.

# # Achados (gaps atuais)

- <<CODE0>> no gateway exclui <<CODE1>>+<HTML2>>>, enquanto os tipos de TS os incluem.
- Control UI CronStatus espera <<CODE3>>, mas gateway retorna <<CODE4>>>.
- Esquema de ferramenta do agente cron permite objetos arbitrários <<CODE5>>, permitindo entradas malformadas.
- Gateway valida estritamente <<CODE6> sem normalização, então as cargas de carga enroladas falham.

# # O que mudou

- <<CODE0>> e <<CODE1> normalizam agora formas comuns de invólucro e infer campos em falta <<CODE2>>.
- O esquema de ferramenta do Agente Cron corresponde ao esquema de gateway, o que reduz as cargas inválidas.
- Enums de provedores estão alinhados entre gateway, CLI, UI e macOS.
- Control UI usa o campo de contagem <<CODE3>> do gateway para status.

# # Comportamento atual

- ** Normalização:** embrulhadas <<CODE0>>/<<CODE1>> as cargas são desembrulhadas; <<CODE2>> e <<CODE3>> são inferidas quando seguras.
- **Padrões:** padrões seguros são aplicados para <<CODE4>>> e <<CODE5>>> quando faltando.
- **Fornecedores:** Discórdia/Slack/Sinal/iMessage são agora consistentemente superfície através de CLI/UI.

Veja [Trabalhos de Cron](<<<LINK0>>) para a forma e exemplos normalizados.

# # Verificação

- Assista logs de gateway para reduzidos <<CODE0>> Erros INVALID  REQUEST.
- Confirmar Controle UI cron status mostra contagem de tarefas após atualização.

# # Acompanhamentos Opcionais

- Manual Control UI smoke: adicionar um trabalho de cron por provedor + verificar a contagem de trabalho de status.

# # Perguntas abertas

- Deve <<CODE0>> aceitar explicitamente <<CODE1>> de clientes (atualmente não permitido pelo esquema)?
- Devemos permitir <<CODE2>> como um provedor de entrega explícito (atualmente filtrado na resolução de entrega)?
