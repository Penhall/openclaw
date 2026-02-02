---
summary: "How the mac app embeds the gateway WebChat and how to debug it"
read_when:
  - Debugging mac WebChat view or loopback port
---

# WebChat (aplicativo macOS)

O aplicativo da barra de menus do macOS incorpora a interface WebChat como uma visão nativa do SwiftUI. Ele
liga- se ao Gateway e por omissão à ** sessão principal** para o seleccionado
agente (com um interruptor de sessão para outras sessões).

- **Modo local**: conecta diretamente ao WebSocket Gateway local.
- ** Modo remoto**: encaminha a porta de controle Gateway sobre SSH e usa que
túnel como o plano de dados.

# # Lançamento e depuração

- Manual: Menu de lagosta → “Abrir chat”.
- Auto- aberto para testes:
  ```bash
  dist/OpenClaw.app/Contents/MacOS/OpenClaw --webchat
  ```
- Diários:`./scripts/clawlog.sh`(subsistema`bot.molt`, categoria`WebChatSwiftUI`).

# # Como está ligado

- Plano de dados: Métodos WS Gateway`chat.history`,`chat.send`,`chat.abort`,
  `chat.inject`e eventos`chat`,`agent`,`presence`,`tick`,`health`.
- Sessão: padrão para a sessão primária (`main`, ou`global`quando o âmbito é
global). A UI pode alternar entre sessões.
- Onboarding usa uma sessão dedicada para manter a configuração de primeira execução separada.

# # Superfície de segurança

- Modo remoto encaminha apenas a porta de controle Gateway WebSocket sobre SSH.

# # Limitações conhecidas

- A UI é otimizada para sessões de chat (não para um navegador completo).
