---
summary: "Loopback WebChat static host and Gateway WS usage for chat UI"
read_when:
  - Debugging or configuring WebChat access
---

# WebChat (Gateway WebSocket UI)

Status: o chat do macOS/iOS SwiftUI UI fala diretamente com o Gateway WebSocket.

# # O que é

- Uma interface de chat nativa para o gateway (sem navegador incorporado e sem servidor estático local).
- Usa as mesmas sessões e regras de roteamento que outros canais.
- Roteamento determinístico: respostas sempre voltar para WebChat.

# # Começo rápido

1. Inicie o portal.
2. Abra o WebChat UI (macOS/iOS app) ou a guia de chat Control UI.
3. Garanta que a autenticação do gateway está configurada (obrigatória por padrão, mesmo no loopback).

# # Como funciona (comportamento)

- A IU liga-se ao Gateway WebSocket e utiliza `chat.history`, `chat.send` e `chat.inject`.
- `chat.inject` adiciona uma nota assistente diretamente à transcrição e transmite-a para a UI (sem execução do agente).
- O histórico é sempre obtido do gateway (nenhum arquivo local observando).
- Se o gateway é inacessível, WebChat é somente leitura.

# # Uso remoto

- Túneis de modo remoto o WebSocket gateway sobre SSH/Tailscale.
- Você não precisa executar um servidor WebChat separado.

# # Referências de configuração (WebChat)

Configuração completa: [Configuração] (</gateway/configuration)

Opções do canal:

- Nenhum bloco dedicado `webchat.*`. WebChat usa o endpoint gateway + configurações de autenticação abaixo.

Opções globais relacionadas:

- <<CODE0>, <<CODE1>: WebSocket host/port.
- `gateway.auth.mode`, `gateway.auth.token`, <<CODE4>: WebSocket auth.
- `gateway.remote.url`, `gateway.remote.token`, `gateway.remote.password`: alvo de passagem remota.
- `session.*`: armazenamento de sessão e chaves principais por omissão.
