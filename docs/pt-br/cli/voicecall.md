---
summary: "CLI reference for `openclaw voicecall` (voice-call plugin command surface)"
read_when:
  - You use the voice-call plugin and want the CLI entry points
  - You want quick examples for `voicecall call|continue|status|tail|expose`
---

#`openclaw voicecall`

`voicecall`é um comando fornecido por plugins. Só aparece se o plug- in de chamada de voz estiver instalado e ativado.

Documento primário:

- Plug- in de chamada de voz: [Chamada de voz] /plugins/voice-call

## Comandos comuns

```bash
openclaw voicecall status --call-id <id>
openclaw voicecall call --to "+15555550123" --message "Hello" --mode notify
openclaw voicecall continue --call-id <id> --message "Any questions?"
openclaw voicecall end --call-id <id>
```

## Expondo webhooks (Tailscale)

```bash
openclaw voicecall expose --mode serve
openclaw voicecall expose --mode funnel
openclaw voicecall unexpose
```

Nota de segurança: apenas expor o endpoint webhook para redes em que você confia. Preferir Tailscale Servir sobre Funil quando possível.
