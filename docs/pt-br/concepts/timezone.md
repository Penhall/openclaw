---
summary: "Timezone handling for agents, envelopes, and prompts"
read_when:
  - You need to understand how timestamps are normalized for the model
  - Configuring the user timezone for system prompts
---

Horários

OpenClaw padroniza timestamps para que o modelo veja um tempo de referência **.

# # Envelopes de mensagens (local por padrão)

As mensagens de entrada são enroladas em um envelope como:

```
[Provider ... 2026-01-05 16:26 PST] message text
```

A hora no envelope é **host-local por padrão**, com precisão de minutos.

Você pode sobrepor isso com:

```json5
{
  agents: {
    defaults: {
      envelopeTimezone: "local", // "utc" | "local" | "user" | IANA timezone
      envelopeTimestamp: "on", // "on" | "off"
      envelopeElapsed: "on", // "on" | "off"
    },
  },
}
```

- <<CODE0> utiliza UTC.
- <<CODE1> usa <<CODE2>> (regressa ao fuso horário da máquina).
- Utilizar um fuso horário IANA explícito (por exemplo, <<CODE3>>>>) para um deslocamento fixo.
- <<CODE4> remove datas absolutas dos cabeçalhos de envelope.
- <<CODE5> remove os sufixos temporais decorridos (estilo <<CODE6>>).

Exemplos

** Local (padrão):**

```
[Signal Alice +1555 2026-01-18 00:19 PST] hello
```

** Fuso- horário corrigido: **

```
[Signal Alice +1555 2026-01-18 06:19 GMT+1] hello
```

** Tempo decorrido: **

```
[Signal Alice +1555 +2m 2026-01-18T05:19Z] follow-up
```

# # Cargas úteis da ferramenta (dados do provedor brutos + campos normalizados)

Chamadas de ferramentas (<<<CODE0>>, <<CODE1>>>, etc.) retornam **marcas temporais do provedor de raw**.
Também anexamos campos normalizados para consistência:

- <<CODE0>> (UTC epoch milissegundos)
- <<CODE1> (cadeia UTC ISO 8601)

Os campos de provedores brutos estão preservados.

# # fuso horário do usuário para o prompt do sistema

Definir <<CODE0>> para dizer ao modelo o fuso horário local do usuário. Se for
unset, OpenClaw resolve o **host timezone em tempo de execução** (sem gravação de configuração).

```json5
{
  agents: { defaults: { userTimezone: "America/Chicago" } },
}
```

O prompt do sistema inclui:

- <<CODE0> secção com hora local e fuso horário
- <<CODE1>> ou <<CODE2>>>

Você pode controlar o formato prompt com <<CODE0>> (<<CODE1>> <<CODE2>> <<CODE3>).

Veja [Data & Tempo](<<<LINK0>>>) para o comportamento completo e exemplos.
