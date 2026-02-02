---
summary: "Channel-specific troubleshooting shortcuts (Discord/Telegram/WhatsApp)"
read_when:
  - A channel connects but messages don’t flow
  - Investigating channel misconfiguration (intents, permissions, privacy mode)
---

# Resolução de problemas do canal

Iniciar com:

```bash
openclaw doctor
openclaw channels status --probe
```

`channels status --probe`imprime avisos quando pode detectar erros de configuração de canais comuns, e inclui pequenas verificações ao vivo (credenciais, algumas permissões/membros).

## Canais

- Discórdia: [/canais/discord# resolução de problemas] /channels/discord#troubleshooting
- Telegrama: [/canais/telegrama# resolução de problemas] /channels/telegram#troubleshooting
- WhatsApp: [/canais/whatsapp# problemas de resolução rápida] /channels/whatsapp#troubleshooting-quick

## Correcções rápidas do Telegram

- Os logs mostram`HttpError: Network request for 'sendMessage' failed`ou`sendChatAction`→ verifique IPv6 DNS. Se o`api.telegram.org`resolver primeiro o IPv6 e o host não tiver saída IPv6, force o IPv4 ou ative o IPv6. Ver [/canais/telegrama# resolução de problemas] /channels/telegram#troubleshooting.
- Os logs mostram`setMyCommands failed`→ check outbound HTTPS e acessibilidade DNS para`api.telegram.org`(comum em VPS ou proxies bloqueados).
