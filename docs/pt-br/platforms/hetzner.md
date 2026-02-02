---
summary: "Run OpenClaw Gateway 24/7 on a cheap Hetzner VPS (Docker) with durable state and baked-in binaries"
read_when:
  - You want OpenClaw running 24/7 on a cloud VPS (not your laptop)
  - You want a production-grade, always-on Gateway on your own VPS
  - You want full control over persistence, binaries, and restart behavior
  - You are running OpenClaw in Docker on Hetzner or a similar provider
---

# Openclaw on Hetzner (Docker, Guia VPS de Produção)

# # Objetivo

Execute um OpenClaw Gateway persistente em um VPS Hetzner usando Docker, com estado durável, binários cozidos e comportamento de reinício seguro.

Se você quiser “OpenClaw 24/7 por ~$5”, esta é a configuração confiável mais simples.
Hetzner muda de preço; escolha o menor Debian/Ubuntu VPS e aumente a escala se você clicar em OOMs.

# # O que estamos fazendo (termos simples)?

- Alugar um pequeno servidor Linux (Hetzner VPS)
- Instalar o Docker (tempo de execução da aplicação isolada)
- Iniciar o portal OpenClaw em Docker
- Persista <<CODE0>> + <<CODE1>> na máquina (sobrevivências reinicia/reconstrui)
- Acesse a interface de controle do seu laptop através de um túnel SSH

O Gateway pode ser acessado através de:

- Reencaminhamento de porta SSH de seu laptop
- Exposição direta à porta se você gerenciar firewall e tokens você mesmo

Este guia assume Ubuntu ou Debian em Hetzner.
Se você estiver em outro Linux VPS, mapeie os pacotes de acordo.
Para o fluxo genérico do Docker, ver [Docker] (<<<LINK0>>>).

---

# # Caminho rápido (operadores experientes)

1. Provisão Hetzner VPS
2. Instalar o Docker
3. Clone repositório OpenClaw
4. Criar diretórios host persistentes
5. Configurar <<CODE0>> e <<CODE1>>
6. Asse binários necessários na imagem
7. <<CODE2>>
8. Verifique a persistência e o acesso ao portal

---

# # O que precisas

- Hetzner VPS com acesso root
- Acesso SSH do seu laptop
- Conforto básico com SSH + cópia/cola
- 20 minutos.
- Docker e Docker Compõem
- Credenciais de autenticação de modelo
- Credenciais de provedor opcional
- WhatsApp QR
- Token bot de telegrama
- Gmail OAuth

---

# # 1) Provisão do VPS

Crie um Ubuntu ou Debian VPS em Hetzner.

Ligar como root:

```bash
ssh root@YOUR_VPS_IP
```

Este guia assume que o VPS é de Estado.
Não o trate como uma infra-estrutura descartável.

---

# # 2) Instalar o Docker (no VPS)

```bash
apt-get update
apt-get install -y git curl ca-certificates
curl -fsSL https://get.docker.com | sh
```

Verificar:

```bash
docker --version
docker compose version
```

---

## 3) Clone o repositório OpenClaw

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
```

Este guia assume que você irá construir uma imagem personalizada para garantir a persistência binária.

---

# # 4) Criar diretórios host persistentes

Os recipientes de docker são efêmeros.
Todo o estado de longa duração deve viver no hospedeiro.

```bash
mkdir -p /root/.openclaw
mkdir -p /root/.openclaw/workspace

# Set ownership to the container user (uid 1000):
chown -R 1000:1000 /root/.openclaw
chown -R 1000:1000 /root/.openclaw/workspace
```

---

## 5) Configurar variáveis de ambiente

Crie <<CODE0>> na raiz do repositório.

```bash
OPENCLAW_IMAGE=openclaw:latest
OPENCLAW_GATEWAY_TOKEN=change-me-now
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_GATEWAY_PORT=18789

OPENCLAW_CONFIG_DIR=/root/.openclaw
OPENCLAW_WORKSPACE_DIR=/root/.openclaw/workspace

GOG_KEYRING_PASSWORD=change-me-now
XDG_CONFIG_HOME=/home/node/.openclaw
```

Gerar segredos fortes:

```bash
openssl rand -hex 32
```

** Não commit este arquivo. **

---

# # 6) Configuração do Docker Compose

Criar ou atualizar <<CODE0>>>>.

```yaml
services:
  openclaw-gateway:
    image: ${OPENCLAW_IMAGE}
    build: .
    restart: unless-stopped
    env_file:
      - .env
    environment:
      - HOME=/home/node
      - NODE_ENV=production
      - TERM=xterm-256color
      - OPENCLAW_GATEWAY_BIND=${OPENCLAW_GATEWAY_BIND}
      - OPENCLAW_GATEWAY_PORT=${OPENCLAW_GATEWAY_PORT}
      - OPENCLAW_GATEWAY_TOKEN=${OPENCLAW_GATEWAY_TOKEN}
      - GOG_KEYRING_PASSWORD=${GOG_KEYRING_PASSWORD}
      - XDG_CONFIG_HOME=${XDG_CONFIG_HOME}
      - PATH=/home/linuxbrew/.linuxbrew/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    volumes:
      - ${OPENCLAW_CONFIG_DIR}:/home/node/.openclaw
      - ${OPENCLAW_WORKSPACE_DIR}:/home/node/.openclaw/workspace
    ports:
      # Recommended: keep the Gateway loopback-only on the VPS; access via SSH tunnel.
      # To expose it publicly, remove the `127.0.0.1:` prefix and firewall accordingly.
      - "127.0.0.1:${OPENCLAW_GATEWAY_PORT}:18789"

      # Optional: only if you run iOS/Android nodes against this VPS and need Canvas host.
      # If you expose this publicly, read /gateway/security and firewall accordingly.
      # - "18793:18793"
    command:
      [
        "node",
        "dist/index.js",
        "gateway",
        "--bind",
        "${OPENCLAW_GATEWAY_BIND}",
        "--port",
        "${OPENCLAW_GATEWAY_PORT}",
      ]
```

---

## 7) Asse binários necessários na imagem (crítico)

Instalar binários dentro de um recipiente em execução é uma armadilha.
Tudo instalado em tempo de execução será perdido ao reiniciar.

Todos os binários externos exigidos pelas habilidades devem ser instalados no tempo de construção da imagem.

Os exemplos abaixo mostram apenas três binários comuns:

- <<CODE0> para acesso Gmail
- <<CODE1> para o Google Places
- <<CODE2>> para WhatsApp

Estes são exemplos, não uma lista completa.
Você pode instalar quantos binários forem necessários usando o mesmo padrão.

Se você adicionar novas habilidades mais tarde que dependem de binários adicionais, você deve:

1. Atualizar o arquivo Docker
2. Reconstruir a imagem
3. Reinicie os recipientes

**Example Dockerfile**

```dockerfile
FROM node:22-bookworm

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

# Example binary 1: Gmail CLI
RUN curl -L https://github.com/steipete/gog/releases/latest/download/gog_Linux_x86_64.tar.gz \
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/gog

# Example binary 2: Google Places CLI
RUN curl -L https://github.com/steipete/goplaces/releases/latest/download/goplaces_Linux_x86_64.tar.gz \
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/goplaces

# Example binary 3: WhatsApp CLI
RUN curl -L https://github.com/steipete/wacli/releases/latest/download/wacli_Linux_x86_64.tar.gz \
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/wacli

# Add more binaries below using the same pattern

WORKDIR /app
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./
COPY ui/package.json ./ui/package.json
COPY scripts ./scripts

RUN corepack enable
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build
RUN pnpm ui:install
RUN pnpm ui:build

ENV NODE_ENV=production

CMD ["node","dist/index.js"]
```

---

# # 8) Construir e lançar

```bash
docker compose build
docker compose up -d openclaw-gateway
```

Verificar os binários:

```bash
docker compose exec openclaw-gateway which gog
docker compose exec openclaw-gateway which goplaces
docker compose exec openclaw-gateway which wacli
```

Resultado esperado:

```
/usr/local/bin/gog
/usr/local/bin/goplaces
/usr/local/bin/wacli
```

---

## 9) Verificar o Portal

```bash
docker compose logs -f openclaw-gateway
```

Sucesso:

```
[gateway] listening on ws://0.0.0.0:18789
```

Do seu portátil:

```bash
ssh -N -L 18789:127.0.0.1:18789 root@YOUR_VPS_IP
```

Abrir:

<<CODE0>>

Cola o teu portal.

---

# # O que persiste onde (fonte da verdade)

O OpenClaw corre no Docker, mas o Docker não é a fonte da verdade.
Todo o estado de longa duração deve sobreviver reinicia, reconstruir e reiniciar.

. . Componente . . Localização . . mecanismo de persistência .
-------------------- ------------------------------------------------- -----------------------------------------------------------------------
Configuração do Gateway Montagem do volume da máquina Inclui <<CODE1>>, fichas
Perfis de autenticação de modelos Montagem do volume da máquina, Tokens OAuth, teclas API
* Habilidade configurou * <<CODE3>> Montagem do volume da máquina
□ Espaço de trabalho agente <<CODE4>> Montagem de volume de host
Sessão do WhatsApp Montagem do volume da máquina Preserva o login do QR
□ Chaveiro Gmail <<CODE6>> Volume de host + senha
Binários externos □ A imagem do Docker deve ser assada na hora de compilação .
□ Node runtime □ Sistema de arquivos de containers □ Imagem de Docker
Pacotes do sistema de arquivos do sistema do sistema do sistema do sistema do sistema do sistema do sistema do sistema do sistema do sistema do sistema do sistema do sistema do sistema do sistema do sistema do sistema do sistema do sistema do sistema do sistema do sistema do sistema do sistema do computador
Contêiner de Docker, Ephemeral, reiniciável, seguro para destruir
