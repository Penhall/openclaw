---
summary: "Timezone handling for agents, envelopes, and prompts"
read_when:
  - You need to understand how timestamps are normalized for the model
  - Configuring the user timezone for system prompts
---

Horários

OpenClaw padroniza timestamps para que o modelo veja um tempo de referência **.

## Envelopes de mensagens (local por padrão)

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

-`envelopeTimezone: "utc"`utiliza UTC.
-`envelopeTimezone: "user"`utiliza`agents.defaults.userTimezone`(regressa ao fuso horário do hospedeiro).
- Utilizar um fuso horário explícito da IANA (por exemplo,`"Europe/Vienna"` para uma compensação fixa.
-`envelopeTimestamp: "off"`remove datas absolutas dos cabeçalhos de envelope.
-`envelopeElapsed: "off"`remove os sufixos de tempo decorrido (estilo`+2m`.

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

## Cargas úteis da ferramenta (dados do provedor brutos + campos normalizados)

Chamadas de ferramentas `channels.discord.readMessages`,`channels.slack.readMessages`, etc.) retornam **marcas temporais do provedor de raw**.
Também anexamos campos normalizados para consistência:

-`timestampMs`-`timestampUtc`(ISO 8601 UTC string)

Os campos de provedores brutos estão preservados.

## fuso horário do usuário para o prompt do sistema

Defina`agents.defaults.userTimezone`para dizer ao modelo o fuso horário local do usuário. Se for
unset, OpenClaw resolve o **host timezone em tempo de execução** (sem gravação de configuração).

```json5
{
  agents: { defaults: { userTimezone: "America/Chicago" } },
}
```

O prompt do sistema inclui:

- secção`Current Date & Time`com hora local e fuso horário
-`Time format: 12-hour`ou`24-hour`

Você pode controlar o formato prompt com`agents.defaults.timeFormat``auto`ou`12`ou`24`.

Veja [Data & Tempo]/date-time para o comportamento completo e exemplos.
