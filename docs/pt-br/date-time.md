---
summary: "Date and time handling across envelopes, prompts, tools, and connectors"
read_when:
  - You are changing how timestamps are shown to the model or users
  - You are debugging time formatting in messages or system prompt output
---

Data e hora

OpenClaw defaults to **host-local timestamps** and **user timezone only in the system prompt**.
Os timestamps do provedor são preservados para que as ferramentas mantenham sua semântica nativa (o tempo atual está disponível via`session_status`.

## Envelopes de mensagens (local por padrão)

As mensagens de entrada são enroladas com um timestamp (precisão de minutos):

```
[Provider ... 2026-01-05 16:26 PST] message text
```

Este envelope timestamp é **host-local por padrão**, independentemente do fuso horário do provedor.

Você pode anular este comportamento:

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
-`envelopeTimezone: "local"`usa o fuso horário do hospedeiro.
-`envelopeTimezone: "user"`utiliza`agents.defaults.userTimezone`(regressa ao fuso horário do hospedeiro).
- Utilizar um fuso horário IANA explícito (por exemplo,`"America/Chicago"` para uma zona fixa.
-`envelopeTimestamp: "off"`remove datas absolutas dos cabeçalhos de envelope.
-`envelopeElapsed: "off"`remove os sufixos de tempo decorridos (estilo`+2m`.

Exemplos

** Local (padrão):**

```
[WhatsApp +1555 2026-01-18 00:19 PST] hello
```

** fuso horário do utilizador: **

```
[WhatsApp +1555 2026-01-18 00:19 CST] hello
```

** Tempo decorrido activado:**

```
[WhatsApp +1555 +30s 2026-01-18T05:19Z] follow-up
```

## Prompt do sistema: Data & Hora atual

Se o fuso- horário do utilizador for conhecido, o prompt do sistema inclui um
** Data atual & Hora** seção com o ** fuso horário apenas** (sem formato relógio/tempo)
para manter o cache rápido estável:

```
Time zone: America/Chicago
```

Quando o agente precisar da hora atual, use a ferramenta`session_status`; o status
cartão inclui uma linha de timestamp.

## Linhas de eventos do sistema (local por padrão)

Os eventos de sistema em fila inseridos no contexto do agente são prefixados com um timestamp usando o
seleção do mesmo fuso horário como envelopes de mensagens (padrão: host- local).

```
System: [2026-01-12 12:19:17 PST] Model switched.
```

## # Configurar fuso horário + formato

```json5
{
  agents: {
    defaults: {
      userTimezone: "America/Chicago",
      timeFormat: "auto", // auto | 12 | 24
    },
  },
}
```

-`userTimezone`define o fuso horário **use-local** para contexto imediato.
-`timeFormat`controles **12h/24h display** no prompt.`auto`segue OS prefs.

## Detecção de formato de tempo (auto)

Quando`timeFormat: "auto"`, o OpenClaw inspeciona a preferência do SO (macOS/Windows)
e volta para a formatação local. O valor detectado é **cached por processo**
para evitar chamadas repetidas do sistema.

## Cargas úteis da ferramenta + conectores (tempo do provedor bruto + campos normalizados)

Ferramentas de canal retornam ** timestamps proviver-native** e adicionam campos normalizados para consistência:

-`timestampMs`: milissegundos de época (UTC)
-`timestampUtc`: string UTC ISO 8601

Os campos de provedores brutos são preservados para que nada seja perdido.

- Slack: strings epoch-like da API
- Discórdia: Horários ISO UTC
- Telegram/WhatsApp: timestamps numéricos/ISO específicos do fornecedor

Se precisar de tempo local, converta-o a jusante usando o fuso horário conhecido.

## Docs relacionados

- [System Prompt] /concepts/system-prompt
- /concepts/timezone
/concepts/messages
