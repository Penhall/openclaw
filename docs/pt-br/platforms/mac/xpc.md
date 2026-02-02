---
summary: "macOS IPC architecture for OpenClaw app, gateway node transport, and PeekabooBridge"
read_when:
  - Editing IPC contracts or menu bar app IPC
---

# Openclaw macOS arquitetura IPC

** Modelo atual:** um soquete Unix local conecta o serviço de host **node** ao aplicativo **macOS** para aprovações executivas +`system.run`. A`openclaw-mac`debug CLI existe para verificação de descoberta / conexão; ações do agente ainda fluim através do Gateway WebSocket e`node.invoke`. Automação UI usa PeekabooBridge.

# # Objetivos

- Uma única instância de aplicativo GUI que possui todo o trabalho voltado para TCC (notificações, gravação de tela, microfone, fala, AppleScript).
- Uma pequena superfície para automação: Comandos Gateway + nó, além de PeekabooBridge para automação UI.
- Permissões previsíveis: sempre o mesmo ID do pacote assinado, lançado pelo lançamento, então o TCC concede stick.

# # Como funciona

Portão + transporte de nós

- O aplicativo executa o Gateway (modo local) e se conecta a ele como um nó.
- As ações do agente são realizadas através`node.invoke`(p. ex.`system.run`,`system.notify`,`canvas.*`).

## # Serviço de nós + aplicativo IPC

- Um serviço de host sem cabeça liga-se ao Gateway WebSocket.
- Não.`system.run`As solicitações são encaminhadas para o aplicativo macOS através de um soquete Unix local.
- O aplicativo executa o exec no contexto UI, solicita se necessário, e retorna saída.

Figura (SCI):

```
Agent -> Gateway -> Node Service (WS)
                      |  IPC (UDS + token + HMAC + TTL)
                      v
                  Mac App (UI + TCC + system.run)
```

## # PeekabooBridge (Automação UI)

- A automação de UI utiliza um soquete UNIX separado chamado`bridge.sock`e o protocolo PeekabooBridge JSON.
- Ordem de preferência do anfitrião (cliente): Peekaboo.app → Claude.app → OpenClaw.app → execução local.
- Segurança: hosts de ponte exigem um TeamID permitido; DEBUG-somente mesma porta de escape UID é vigiado por`PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1`(Convenção Peekaboo).
- Veja: [Uso PeekabooBridge] (</platforms/mac/peekaboo) para detalhes.

# # Fluxos operacionais

- Reiniciar/reconstruir:`SIGN_IDENTITY="Apple Development: <Developer Name> (<TEAMID>)" scripts/restart-mac.sh`
- Mata instâncias existentes
- Pacote Swift build +
- Writes/bootstraps/kickstarts the LaunchAgent
- Uma única instância: app sai mais cedo se outra instância com o mesmo ID do pacote estiver em execução.

# # Notas de endurecimento

- Prefere uma partida TeamID para todas as superfícies privilegiadas.
- PeekabooBridge:`PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1`(debug-only) pode permitir chamadas do mesmo UID para o desenvolvimento local.
- Toda a comunicação permanece apenas local; nenhuma tomada de rede está exposta.
- Os prompts TCC são originários apenas do pacote de aplicativos GUI; mantenham o ID do pacote assinado estável em reconstruções.
- Endurecimento IPC: modo soquete`0600`, token, verificação de UID por pares, desafio/resposta HMAC, TTL curto.
