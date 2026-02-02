---
summary: "Windows (WSL2) support + companion app status"
read_when:
  - Installing OpenClaw on Windows
  - Looking for Windows companion app status
---

# Windows (WSL2)

Openclaw no Windows é recomendado **via WSL2** (Ubuntu recomendado). A
CLI + Gateway executado dentro do Linux, que mantém o tempo de execução consistente e faz
ferramentas muito mais compatíveis (Node/Bun/pnpm, binários Linux, habilidades). Nativo
As instalações do Windows são não testadas e mais problemáticas.

Aplicativos companheiras do Windows nativos são planejados.

# # Instalar (WSL2)

- [Começar] (</start/getting-started) (usar dentro do WSL)
- [Instalar & actualizar] (</install/updating)
- Guia oficial WSL2 (Microsoft): https://learn.microsoft.com/windows/wsl/install

# # Gateway

- [Corretório do portal] (</gateway)
- [Configuração] (</gateway/configuration)

# # Serviço de gateway instalar (CLI)

Dentro do WSL2:

```
openclaw onboard --install-daemon
```

Ou:

```
openclaw gateway install
```

Ou:

```
openclaw configure
```

Selecione **Serviço Gateway** quando solicitado.

Reparação/migração:

```
openclaw doctor
```

# # Avançado: expor serviços WSL sobre LAN (portproxy)

WSL tem sua própria rede virtual. Se outra máquina precisar de alcançar um serviço
executando **inside WSL** (SSH, um servidor TTS local, ou o Gateway), você deve
encaminhar uma porta do Windows para o IP WSL atual. O IP WSL muda após reiniciar,
assim você pode precisar atualizar a regra de encaminhamento.

Exemplo (PowerShell ** como Administrador**):

```powershell
$Distro = "Ubuntu-24.04"
$ListenPort = 2222
$TargetPort = 22

$WslIp = (wsl -d $Distro -- hostname -I).Trim().Split(" ")[0]
if (-not $WslIp) { throw "WSL IP not found." }

netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=$ListenPort `
  connectaddress=$WslIp connectport=$TargetPort
```

Permitir a porta através do Windows Firewall (uma vez):

```powershell
New-NetFirewallRule -DisplayName "WSL SSH $ListenPort" -Direction Inbound `
  -Protocol TCP -LocalPort $ListenPort -Action Allow
```

Actualizar o 'portproxy' após reiniciar o WSL:

```powershell
netsh interface portproxy delete v4tov4 listenport=$ListenPort listenaddress=0.0.0.0 | Out-Null
netsh interface portproxy add v4tov4 listenport=$ListenPort listenaddress=0.0.0.0 `
  connectaddress=$WslIp connectport=$TargetPort | Out-Null
```

Notas:

- SSH de outra máquina tem como alvo o **Windows host IP** (exemplo: `ssh user@windows-host -p 2222`).
- Os nós remotos devem apontar para uma URL ** alcançável** Gateway (não `127.0.0.1`);
<<CODE2> para confirmar.
- Use `listenaddress=0.0.0.0` para acesso LAN; <<CODE4> mantém-no local apenas.
- Se você quiser este automático, registre uma tarefa agendada para executar a atualização
passo no login.

# # Instalação passo-a-passo WSL2

# # # 1) Instalar WSL2 + Ubuntu

Abrir PowerShell (Admin):

```powershell
wsl --install
# Or pick a distro explicitly:
wsl --list --online
wsl --install -d Ubuntu-24.04
```

Reiniciar se o Windows perguntar.

## # 2) Habilitar systemd (obrigatório para instalação de gateway)

No seu terminal WSL:

```bash
sudo tee /etc/wsl.conf >/dev/null <<'EOF'
[boot]
systemd=true
EOF
```

Depois da PowerShell:

```powershell
wsl --shutdown
```

Reabrir o Ubuntu e verificar:

```bash
systemctl --user status
```

# # # 3) Instalar OpenClaw (dentro do WSL)

Siga o fluxo Linux Introdução dentro do WSL:

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build # auto-installs UI deps on first run
pnpm build
openclaw onboard
```

Guia completo: [Começar] (</start/getting-started)

# # Aplicativo companheiro do Windows

Ainda não temos um aplicativo companheiro do Windows. Contribuições são bem-vindas se você quiser
contribuições para que isso aconteça.
