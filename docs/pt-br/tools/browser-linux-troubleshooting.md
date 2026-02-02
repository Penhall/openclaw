---
summary: "Fix Chrome/Brave/Edge/Chromium CDP startup issues for OpenClaw browser control on Linux"
read_when: "Browser control fails on Linux, especially with snap Chromium"
---

# Solução de problemas do navegador (Linux)

# # Problema: "Falhou para iniciar Chrome CDP na porta 18800"

O servidor de controle do navegador OpenClaw não consegue iniciar o Chrome/Brave/Edge/Chromium com o erro:

```
{"error":"Error: Failed to start Chrome CDP on port 18800 for profile \"openclaw\"."}
```

Causa Raíz

No Ubuntu (e muitas distros Linux), a instalação padrão do Chromium é um pacote **snap**. O confinamento do AppArmor do Snap interfere em como o OpenClaw cria e monitora o processo do navegador.

O comando <<CODE0> instala um pacote stub que redireciona para snap:

```
Note, selecting 'chromium-browser' instead of 'chromium'
chromium-browser is already the newest version (2:1snap1-0ubuntu2).
```

Este não é um navegador real — é apenas uma embalagem.

### Solução 1: Instalar o Google Chrome (Recomendado)

Instale o pacote oficial do Google Chrome <<CODE0>, que não é sandboxed pelo snap:

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install -y  # if there are dependency errors
```

Em seguida, atualize sua configuração do OpenClaw (<`~/.openclaw/openclaw.json`):

```json
{
  "browser": {
    "enabled": true,
    "executablePath": "/usr/bin/google-chrome-stable",
    "headless": true,
    "noSandbox": true
  }
}
```

### Solução 2: Usar o Crómio de Encaixe com o Modo Anexar Apenas

Se você precisa usar o Chromium snap, configure o OpenClaw para anexar a um navegador iniciado manualmente:

1. Actualizar a configuração:

```json
{
  "browser": {
    "enabled": true,
    "attachOnly": true,
    "headless": true,
    "noSandbox": true
  }
}
```

2. Iniciar o Chromium manualmente:

```bash
chromium-browser --headless --no-sandbox --disable-gpu \
  --remote-debugging-port=18800 \
  --user-data-dir=$HOME/.openclaw/browser/openclaw/user-data \
  about:blank &
```

3. Opcionalmente criar um serviço de usuário systemd para auto-iniciar Chrome:

```ini
# ~/.config/systemd/user/openclaw-browser.service
[Unit]
Description=OpenClaw Browser (Chrome CDP)
After=network.target

[Service]
ExecStart=/snap/bin/chromium --headless --no-sandbox --disable-gpu --remote-debugging-port=18800 --user-data-dir=%h/.openclaw/browser/openclaw/user-data about:blank
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

Habilitar com: `systemctl --user enable --now openclaw-browser.service`

Verificando o Navegador Funciona

Verificar o estado:

```bash
curl -s http://127.0.0.1:18791/ | jq '{running, pid, chosenBrowser}'
```

Navegação de teste:

```bash
curl -s -X POST http://127.0.0.1:18791/start
curl -s http://127.0.0.1:18791/tabs
```

Referência de configuração

□ Opção □ Descrição
------------- ------------------------------------------------------------------------------------------------------------------------------------ ----------
Ativar o controle do navegador
□ `browser.executablePath`
* `browser.headless` * Executar sem GUI * <<CODE4>
(precisado para algumas configurações Linux)
Não inicie o navegador, apenas anexe-se ao existente
Porta do Protocolo de DevTools do Chrome

## # Problema: "O relé de extensão do cromo está em execução, mas nenhuma aba está conectada"

Você está usando o perfil `chrome` (relé de extensão). Espera a Openclaw
extensão do navegador para ser anexado a uma aba ao vivo.

Opções de correção:

1. **Use o navegador gerenciado:** `openclaw browser start --browser-profile openclaw`
(ou definido `browser.defaultProfile: "openclaw"`).
2. **Use o relé de extensão:** instale a extensão, abra uma aba e clique no
Ícone de extensão do OpenClaw para anexá-lo.

Notas:

- O perfil <<CODE0> usa seu navegador Chromium ** padrão do sistema ** quando possível.
- Perfis locais <<CODE1> auto-atribuir `cdpPort`/`cdpUrl`; apenas definir aqueles para CDP remoto.
