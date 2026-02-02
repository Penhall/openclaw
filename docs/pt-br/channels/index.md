---
summary: "Messaging platforms OpenClaw can connect to"
read_when:
  - You want to choose a chat channel for OpenClaw
  - You need a quick overview of supported messaging platforms
---

Canais de Conversa

OpenClaw pode falar com você em qualquer aplicativo de chat que você já use. Cada canal se conecta através do Gateway.
O texto é suportado em todos os lugares; os meios e as reações variam por canal.

## Canais suportados

- [WhatsApp]/channels/whatsapp — Mais popular; usa Baileys e requer emparelhamento QR.
- [Telegram]/channels/telegram — Bot API via grammY; suporta grupos.
- [Discord]/channels/discord — Discord Bot API + Gateway; suporta servidores, canais e DMs.
- [Slack]/channels/slack — Bolt SDK; aplicativos de espaço de trabalho.
- [Google Chat] /channels/googlechat — Aplicativo do Google Chat API via HTTP webhook.
- [Mattermost]/channels/mattermost — Bot API + WebSocket; canais, grupos, DMs (plugin, instalado separadamente).
- [Sinal] /channels/signal — sinal-cli; focado na privacidade.
- [BlueBubbles]/channels/bluebubbles — **Recomendado para iMessage**; usa o servidor BlueBubbles macOS REST API com suporte completo de recursos (edit, unsend, efeitos, reações, gerenciamento de grupo — edição atualmente quebrada no macOS 26 Tahoe).
- [iMessage]/channels/imessage — apenas macOS; integração nativa via imsg (legacy, considere BlueBubbles para novas configurações).
- [Microsoft Teams]/channels/msteams — Bot Framework; suporte empresarial (plugin, instalado separadamente).
- [LINE]/channels/telegram0) — LINE Messaging API bot (plugin, instalado separadamente).
- [Nextcloud Talk] /channels/telegram1) — Conversa auto- hospedada via Nextcloud Talk (plugin, instalado separadamente).
- [Matrix]/channels/telegram2) — Protocolo Matrix (plugin, instalado separadamente).
- [Nostr]/channels/telegram3) — DMs descentralizados via NIP-04 (plugin, instalado separadamente).
- [Tlon]/channels/telegram4) — mensageiro baseado em Urbit (plugin, instalado separadamente).
- [Twitch] /channels/telegram5) — Bate-papo de Twitch via ligação IRC (plugin, instalado separadamente).
- [Zalo] /channels/telegram6) — Zalo Bot API; o mensageiro popular do Vietname (plugin, instalado separadamente).
- [Zalo Personal]/channels/telegram7) — Conta pessoal do Zalo através do login do QR (plugin, instalado separadamente).
- [WebChat] /channels/telegram8) — Gateway WebChat UI sobre WebSocket.

## Notas

- Canais podem ser executados simultaneamente; configure múltiplos e OpenClaw irá rotear por chat.
- A configuração mais rápida é geralmente **Telegram** (simples bot token). WhatsApp requer emparelhamento QR e
armazena mais estado no disco.
- O comportamento do grupo varia por canal; veja [Grupos] /concepts/groups.
- Emparelhamento de DM e lista de allowlists são aplicados para segurança; ver [Segurança] /gateway/security.
- Interiores do telegrama: [notas de grama] /channels/grammy.
- Resolução de problemas:
- Os fornecedores de modelos estão documentados separadamente; ver [Modelo Providers] /providers/models.
