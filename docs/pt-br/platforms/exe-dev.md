---
summary: "Run OpenClaw Gateway on exe.dev (VM + HTTPS proxy) for remote access"
read_when:
  - You want a cheap always-on Linux host for the Gateway
  - You want remote Control UI access without running your own VPS
---

# exe.dev

Objetivo: OpenClaw Gateway rodando em uma VM exe.dev, acessível do seu laptop via: <<CODE0>

Esta página assume o padrão de exe.dev **exeuntu** image. Se você escolheu uma distro diferente, mapeie os pacotes de acordo.

# # Caminho rápido iniciante

1. [https://exe.new/openclaw](<<<LINK0>>)
2. Preencha sua chave de autenticação / token se necessário
3. Clique em "Agente" ao lado da sua VM, e espere...
4. ??
5. Lucro

# # O que precisas

- conta exe.dev
- <<CODE0>Acesso a [exe.dev](<<LINK0>>) máquinas virtuais (opcional)

# # Instalação automatizada com Shelley

O agente do Shelley, [exe.dev](<<<LINK0>>), pode instalar o OpenClaw instantaneamente com o nosso
rápido. O prompt utilizado é como abaixo:

```
Set up OpenClaw (https://docs.openclaw.ai/install) on this VM. Use the non-interactive and accept-risk flags for openclaw onboarding. Add the supplied auth or token as needed. Configure nginx to forward from the default port 18789 to the root location on the default enabled site config, making sure to enable Websocket support. Pairing is done by "openclaw devices list" and "openclaw device approve <request id>". Make sure the dashboard shows that OpenClaw's health is OK. exe.dev handles forwarding from port 8000 to port 80/443 and HTTPS for us, so the final "reachable" should be <vm-name>.exe.xyz, without port specification.
```

# # Instalação manual

# # 1) Criar a VM

Do seu dispositivo:

```bash
ssh exe.dev new
```

Em seguida, conecte-se:

```bash
ssh <vm-name>.exe.xyz
```

Dica: mantenha esta VM **stateful**. OpenClaw armazena estado em <<CODE0>>> e <<CODE1>>>.

2) Instalar pré-requisitos (na VM)

```bash
sudo apt-get update
sudo apt-get install -y git curl jq ca-certificates openssl
```

# # 3) Instalar OpenClaw

Executar o script de instalação OpenClaw:

```bash
curl -fsSL https://openclaw.bot/install.sh | bash
```

# # 4) Configurar nginx para proxy OpenClaw para porta 8000

Editar <<CODE0>> com

```
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    listen 8000;
    listen [::]:8000;

    server_name _;

    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;

        # WebSocket support
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Standard proxy headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeout settings for long-lived connections
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
}
```

## 5) Acesse OpenClaw e conceda privilégios

Acesso <<CODE0>>>. Aprovar
dispositivos com <<CODE1>> e <<CODE2>>>. Na dúvida,
use Shelley do seu navegador!

# # Acesso Remoto

O acesso remoto é tratado pela autenticação de [exe.dev](<<LINK0>>>). Por
padrão, o tráfego HTTP da porta 8000 é encaminhado para <<CODE0>>
com e- mail auth.

# # Atualizando

```bash
npm i -g openclaw@latest
openclaw doctor
openclaw gateway restart
openclaw health
```

Guia: [Atualização](<<<LINK0>>>)
