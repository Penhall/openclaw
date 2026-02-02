---
summary: "SSH tunnel setup for OpenClaw.app connecting to a remote gateway"
read_when: "Connecting the macOS app to a remote gateway over SSH"
---

# Correndo Openclaw.app com um Gateway Remoto

Openclaw.app usa o túnel SSH para se conectar a um gateway remoto. Este guia mostra-lhe como montá-lo.

# # Visão geral

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Machine                          │
│                                                              │
│  OpenClaw.app ──► ws://127.0.0.1:18789 (local port)           │
│                     │                                        │
│                     ▼                                        │
│  SSH Tunnel ────────────────────────────────────────────────│
│                     │                                        │
└─────────────────────┼──────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                         Remote Machine                        │
│                                                              │
│  Gateway WebSocket ──► ws://127.0.0.1:18789 ──►              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

# # Configuração Rápida

Passo 1: Adicionar a Configuração da SSH

Editar <<CODE0>> e adicionar:

```ssh
Host remote-gateway
    HostName <REMOTE_IP>          # e.g., 172.27.187.184
    User <REMOTE_USER>            # e.g., jefferson
    LocalForward 18789 127.0.0.1:18789
    IdentityFile ~/.ssh/id_rsa
```

Substituir <<CODE0>> e <<CODE1>> por seus valores.

Passo 2: Copiar a tecla SSH

Copie sua chave pública para a máquina remota (introduza a senha uma vez):

```bash
ssh-copy-id -i ~/.ssh/id_rsa <REMOTE_USER>@<REMOTE_IP>
```

Passo 3: Preparar o Portal Token

```bash
launchctl setenv OPENCLAW_GATEWAY_TOKEN "<your-token>"
```

Passo 4: Iniciar o túnel SSH

```bash
ssh -N remote-gateway &
```

Passo 5: Reiniciar OpenClaw.app

```bash
# Quit OpenClaw.app (⌘Q), then reopen:
open /path/to/OpenClaw.app
```

O aplicativo agora se conectará ao gateway remoto através do túnel SSH.

---

# # Túnel de início automático no login

Para que o túnel SSH comece automaticamente quando você entrar, crie um Launch Agent.

## # Criar o arquivo PLIST

Gravar isto como <<CODE0>>:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>bot.molt.ssh-tunnel</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/ssh</string>
        <string>-N</string>
        <string>remote-gateway</string>
    </array>
    <key>KeepAlive</key>
    <true/>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

Carregar o agente de lançamento

```bash
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/bot.molt.ssh-tunnel.plist
```

O túnel será agora:

- Iniciar automaticamente quando entrar
- Reiniciar se cair
- Continua a correr no fundo

Nota de legado: remover as sobras <<CODE0>> LançarAgente se presente.

---

# # Resolução de problemas

** Verifique se o túnel está em execução:**

```bash
ps aux | grep "ssh -N remote-gateway" | grep -v grep
lsof -i :18789
```

** Reiniciar o túnel:**

```bash
launchctl kickstart -k gui/$UID/bot.molt.ssh-tunnel
```

** Pare o túnel:**

```bash
launchctl bootout gui/$UID/bot.molt.ssh-tunnel
```

---

# # Como Funciona

O que faz
----------------------------------------------------- --------------------------------------------------------------------------------------------
* <<CODE0>> * Avançar porta local 18789 para porta remota 18789
<<CODE1>> □ SSH sem executar comandos remotos (apenas encaminhamento de porta)
<<CODE2>> □ Reinicia automaticamente o túnel se ele falhar
* <<CODE3>> * Inicia o túnel quando o agente carrega

OpenClaw.app conecta-se a <<CODE0>> em sua máquina cliente. O túnel SSH avança essa ligação à porta 18789 na máquina remota onde o Gateway está a correr.
