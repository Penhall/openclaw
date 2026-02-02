---
summary: "Poll sending via gateway + CLI"
read_when:
  - Adding or modifying poll support
  - Debugging poll sends from the CLI or gateway
---

# Pesquisas

## Canais suportados

- WhatsApp (canal web)
- Discórdia
- Equipas MS (Cartões Adaptativos)

## CLI

```bash
# WhatsApp
openclaw message poll --target +15555550123 \
  --poll-question "Lunch today?" --poll-option "Yes" --poll-option "No" --poll-option "Maybe"
openclaw message poll --target 123456789@g.us \
  --poll-question "Meeting time?" --poll-option "10am" --poll-option "2pm" --poll-option "4pm" --poll-multi

# Discord
openclaw message poll --channel discord --target channel:123456789 \
  --poll-question "Snack?" --poll-option "Pizza" --poll-option "Sushi"
openclaw message poll --channel discord --target channel:123456789 \
  --poll-question "Plan?" --poll-option "A" --poll-option "B" --poll-duration-hours 48

# MS Teams
openclaw message poll --channel msteams --target conversation:19:abc@thread.tacv2 \
  --poll-question "Lunch?" --poll-option "Pizza" --poll-option "Sushi"
```

Opções:

-`--channel`:`whatsapp`(padrão),`discord`ou`msteams`-`--poll-multi`: permite selecionar várias opções
-`--poll-duration-hours`: Discord-only (por omissão até 24 quando omitido)

## Porta RCP

Método:`poll`

Parâmetros:

-`to`(texto, obrigatório)
-`question`(cadeia, necessária)
-`options`(cadeia[], necessária)
-`maxSelections`(número, opcional)
-`durationHours`(número, opcional)
-`channel`(texto, opcional, padrão:`whatsapp`
-`idempotencyKey`(cadeia, necessária)

## Diferenças de canais

- WhatsApp: 2-12 opções,`maxSelections`deve estar dentro da contagem de opções, ignora`durationHours`.
- Discórdia: 2-10 opções,`durationHours`preso a 1-768 horas (padrão 24).`maxSelections > 1`permite a seleção múltipla; Discord não suporta uma contagem de seleção estrita.
- Equipas MS: sondagens de cartões adaptativos (gerido pelo OpenClaw). Nenhuma API de pesquisa nativa;`durationHours`é ignorado.

## Ferramenta de agente (Mensagem)

Utilizar a ferramenta`message`com acção`poll``to`,`pollQuestion`,`pollOption`, opcional`pollMulti`,`pollDurationHours`,`channel`.

Nota: A discórdia não tem o modo “escolha exatamente N”;`pollMulti`mapeia para multi-selecionar.
As sondagens de equipes são renderizadas como cartões adaptativos e requerem o gateway para permanecer online
gravar votos em`~/.openclaw/msteams-polls.json`.
