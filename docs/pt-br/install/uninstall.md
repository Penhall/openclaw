---
summary: "Uninstall OpenClaw completely (CLI, service, state, workspace)"
read_when:
  - You want to remove OpenClaw from a machine
  - The gateway service is still running after uninstall
---

Desinstalar

Dois caminhos:

- ** Caminho fácil** se <<CODE0>> ainda estiver instalado.
- Remoção manual de serviço** se o CLI se foi, mas o serviço ainda está em execução.

# # Caminho fácil (CLI ainda instalado)

Recomendado: usar o desinstalador incorporado:

```bash
openclaw uninstall
```

Não- interactiva (automatização / npx):

```bash
openclaw uninstall --all --yes --non-interactive
npx -y openclaw uninstall --all --yes --non-interactive
```

Passos manuais (mesmo resultado):

1. Pare o serviço de gateway:

```bash
openclaw gateway stop
```

2. Desinstale o serviço de gateway (lançado/systemd/schtasks):

```bash
openclaw gateway uninstall
```

3. Excluir estado + configuração:

```bash
rm -rf "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
```

Se você definir <<CODE0>> para uma localização personalizada fora da dir estado, apague esse arquivo também.

4. Excluir seu espaço de trabalho (opcional, remove arquivos de agente):

```bash
rm -rf ~/.openclaw/workspace
```

5. Remova a instalação CLI (escolha a que você usou):

```bash
npm rm -g openclaw
pnpm remove -g openclaw
bun remove -g openclaw
```

6. Se você instalou o aplicativo macOS:

```bash
rm -rf /Applications/OpenClaw.app
```

Notas:

- Se você usou perfis (<<<CODE0> / <<CODE1>>>>>>), repetir o passo 3 para cada dir estado (os padrões são <<CODE2>>>).
- No modo remoto, a dir do estado vive no host **gateway**, então execute os passos 1-4 lá também.

# # Remoção manual de serviço (CLI não instalado)

Use isso se o serviço de gateway continuar em execução, mas <<CODE0>> estiver faltando.

### macOS (lançado)

Rótulo padrão é <<CODE0>> (ou <<CODE1>>>; legado <<CODE2>>> pode ainda existir):

```bash
launchctl bootout gui/$UID/bot.molt.gateway
rm -f ~/Library/LaunchAgents/bot.molt.gateway.plist
```

Se você usou um perfil, substitua o rótulo e nome da plist por <<CODE0>>. Remover qualquer legado <<CODE1>>> plists se presente.

## # Linux (unidade de usuário sistematizada)

Nome unitário padrão é <<CODE0>> (ou <<CODE1>>>):

```bash
systemctl --user disable --now openclaw-gateway.service
rm -f ~/.config/systemd/user/openclaw-gateway.service
systemctl --user daemon-reload
```

## # Janelas (Tarefa agendada)

O nome da tarefa padrão é <<CODE0>> (ou <<CODE1>>>>>).
O script de tarefas vive sob sua dir estado.

```powershell
schtasks /Delete /F /TN "OpenClaw Gateway"
Remove-Item -Force "$env:USERPROFILE\.openclaw\gateway.cmd"
```

Se você usou um perfil, apague o nome da tarefa correspondente e <<CODE0>>>.

# # Instalação normal vs saída de código

## # Instalação normal (install.sh / npm / pnpm / bun)

Se você usou <<CODE0>> ou <<CODE1>>>>, o CLI foi instalado com <<CODE2>>>.
Remova-o com <<CODE3>> (ou <<CODE4>/ <HTML5>> se você instalou dessa forma).

### Obtenção de código fonte (git clone)

Se correr de um repo checkout (<<<CODE0>> + <<CODE1>>/ <<CODE2>>):

1. Desinstale o serviço de gateway **antes** excluir o repo (use o caminho fácil acima ou remoção de serviço manual).
2. Excluir o diretório repo.
3. Remover estado + espaço de trabalho como mostrado acima.
