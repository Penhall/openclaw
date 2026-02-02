---
summary: "OpenClaw macOS companion app (menu bar + gateway broker)"
read_when:
  - Implementing macOS app features
  - Changing gateway lifecycle or node bridging on macOS
---

# OpenClaw macOS Companion (menu bar + gateway broker)

O aplicativo macOS é o companheiro **menu-bar para OpenClaw. Tem permissões,
gerencia/liga-se ao Gateway localmente (lançado ou manual), e expõe macOS
capacidades para o agente como um nó.

# # O que faz

- Mostra notificações nativas e status na barra de menu.
- Possui prompts TCC (Notificações, Acessibilidade, Gravação de Tela, Microfone,
Reconhecimento de Fala, Automação/AppleScript).
- Executa ou conecta ao Gateway (local ou remoto).
- Expo ferramentas somente do macOS (Canvas, Câmera, Gravação de Tela, `system.run`).
- Inicia o serviço de host de nó local em modo **remote** (lançado), e o para em modo **local**.
- Hospeda opcionalmente **PeekabooBridge** para automação de UI.
- Instala o CLI global (`openclaw`) via npm/pnpm a pedido (bun não recomendado para a execução do Gateway).

# # Modo Local vs Remoto

- **Local** (padrão): o aplicativo se liga a um Gateway local em execução se presente;
Caso contrário, ele permite o serviço lançado via `openclaw gateway install`.
- ** Remote**: o aplicativo se conecta a um Gateway sobre SSH/Tailscale e nunca começa
um processo local.
O aplicativo inicia o serviço de host local **node** para que o Gateway remoto possa alcançar este Mac.
O aplicativo não cria o Gateway como processo infantil.

# # Controle lançado

O aplicativo gerencia um LaunchAgent de per-usuário rotulado <<CODE0>
(ou `bot.molt.<profile>` ao utilizar <<CODE2>/`OPENCLAW_PROFILE`; legado <<CODE4> ainda descarrega).

```bash
launchctl kickstart -k gui/$UID/bot.molt.gateway
launchctl bootout gui/$UID/bot.molt.gateway
```

Substituir o rótulo por <<CODE0> ao executar um perfil nomeado.

Se o LaunchAgent não estiver instalado, habilite-o a partir do aplicativo ou execute
`openclaw gateway install`.

# # Capacidades de nós (mac)

O aplicativo macOS se apresenta como um nó. Comandos comuns:

- Tela: <<CODE0>, <<CODE1>, `canvas.eval`, <<CODE3>, <<CODE4>
- Câmara: <<CODE5>, <<CODE6>
- Ecrã: `screen.record`
- Sistema: `system.run`, `system.notify`

O nó relata um mapa <<CODE0> para que os agentes possam decidir o que é permitido.

Serviço de nós + aplicativo IPC:

- Quando o serviço de host sem cabeça está em execução (modo remoto), ele se conecta ao Gateway WS como um nó.
- `system.run` executa no aplicativo macOS (Contexto UI/TCC) em um soquete Unix local; prompts + saída stay in-app.

Figura (SCI):

```
Gateway -> Node Service (WS)
                 |  IPC (UDS + token + HMAC + TTL)
                 v
             Mac App (UI + TCC + system.run)
```

# # aprovações exec (system.run)

<<CODE0> é controlada por **Aprovações exec** na aplicação macOS (Configurações → Aprovações exec).
Segurança + ask + allowlist são armazenados localmente no Mac em:

```
~/.openclaw/exec-approvals.json
```

Exemplo:

```json
{
  "version": 1,
  "defaults": {
    "security": "deny",
    "ask": "on-miss"
  },
  "agents": {
    "main": {
      "security": "allowlist",
      "ask": "on-miss",
      "allowlist": [{ "pattern": "/opt/homebrew/bin/rg" }]
    }
  }
}
```

Notas:

- <<CODE0> entradas são padrões glob para caminhos binários resolvidos.
- Escolhendo "Sempre Permitir" no prompt adiciona esse comando à lista de allowlist.
- `system.run` são filtradas as sobreposições do ambiente (drops `PATH`, `DYLD_*`, `LD_*`, `NODE_OPTIONS`, `PYTHON*`, `PERL*`, `RUBYOPT`) e depois fundidas com o ambiente do aplicativo.

# # Ligações profundas

O aplicativo registra o `openclaw://` Esquema de URL para ações locais.

## # <<CODE0>

Ativa uma solicitação de Gateway <<CODE0>.

```bash
open 'openclaw://agent?message=Hello%20from%20deep%20link'
```

Parâmetros da consulta:

- <<CODE0> (obrigatório)
- <<CODE1> (facultativo)
- <<CODE2> (facultativo)
- `deliver` / `to` / `channel` (facultativo)
- `timeoutSeconds` (facultativo)
- `key` (chave opcional do modo não vigiado)

Segurança:

- Sem `key`, o aplicativo pede confirmação.
- Com um valor válido `key`, a execução não é acompanhada (destinada a automações pessoais).

# # Fluxo integrado (típico)

1. Instalar e lançar ** OpenClaw.app**.
2. Complete a lista de permissões (prompts TCC).
3. Certifique-se de que o modo ** Local está ativo e o Gateway está em execução.
4. Instale o CLI se você quiser acesso ao terminal.

# # Compilar & dev workflow (nativo)

- <<CODE0>
- <<CODE1> (ou Xcode)
- Aplicação da embalagem: `scripts/package-mac-app.sh`

# # Conectividade de gateway de depuração (macOS CLI)

Use o CLI de depuração para exercer o mesmo aperto de mão Gateway WebSocket e descoberta
lógica que o aplicativo macOS usa, sem lançar o aplicativo.

```bash
cd apps/macos
swift run openclaw-mac connect --json
swift run openclaw-mac discover --timeout 3000 --json
```

Opções de ligação:

- <<CODE0>: configuração de sobreposição
- <<CODE1>: resolver a partir da configuração (por omissão: configuração ou local)
- <<CODE2>: forçar uma sonda de saúde fresca
- `--timeout <ms>`: tempo limite de solicitação (padrão: `15000`)
- <<CODE5>: saída estruturada para diffing

Opções de descoberta:

- `--include-local`: incluir gateways que seriam filtrados como “local”
- `--timeout <ms>`: janela de descoberta global (padrão: `2000`)
- `--json`: saída estruturada para diffing

Dica: comparar com <<CODE0> para ver se o
O pipeline de descoberta do aplicativo macOS (NWBrowser + tailnet DNS-SD fallback) difere de
a descoberta baseada no Node CLI `dns-sd`.

# # Encanamento de ligação remota ( tuneis SSH)

Quando o aplicativo macOS é executado no modo ** Remote**, ele abre um túnel SSH tão local UI
componentes podem falar com um Gateway remoto como se fosse no localhost.

## # Túnel de controle (porta Gateway WebSocket)

- **Põe:** verificações de saúde, status, Web Chat, config, e outras chamadas de plano de controle.
- ** Porta local:** Porta Gateway (padrão `18789`), sempre estável.
- ** Porta remota:** mesma porta Gateway no host remoto.
- ** Comportamento:** nenhuma porta local aleatória; o aplicativo reutiliza um túnel saudável existente
ou reinicia- o se necessário.
- ** Forma SHSS:** `ssh -N -L <local>:127.0.0.1:<remote>`
SairForwardFalha + opções de manutenção.
- ** Relatório IP:** O túnel SSH usa loopback, então o gateway verá o nó
IP como `127.0.0.1`. Use **Direct (ws/wss)** transporte se quiser o cliente real
IP para aparecer (veja [macOS acesso remoto] (</platforms/mac/remote)).

Para as etapas de configuração, consulte [acesso remoto macOS](</platforms/mac/remote). Para o protocolo
detalhes, ver [Protocolo Gateway] (</gateway/protocol).

# # Docs relacionados

- [Corretório do portal] (</gateway)
- [Gateway (macOS)] (</platforms/mac/bundled-gateway)
- [permissões macOS] (</platforms/mac/permissions)
- [Canvas] (</platforms/mac/canvas)
