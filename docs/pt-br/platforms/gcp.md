---
summary: "Run OpenClaw Gateway 24/7 on a GCP Compute Engine VM (Docker) with durable state"
read_when:
  - You want OpenClaw running 24/7 on GCP
  - You want a production-grade, always-on Gateway on your own VM
  - You want full control over persistence, binaries, and restart behavior
---

# Openclaw no motor de computação GCP (Docker, Guia VPS de produção)

# # Objetivo

Execute um Gateway OpenClaw persistente em um motor de computação GCP VM usando Docker, com estado durável, binários cozidos e comportamento de reinício seguro.

Se você quiser "OpenClaw 24/7 por ~$5-12/mo", esta é uma configuração confiável no Google Cloud.
Os preços variam de acordo com o tipo e a região da máquina; escolha a menor VM que se adequa à sua carga de trabalho e aumente a escala se você atingir OOMs.

# # O que estamos fazendo (termos simples)?

- Criar um projeto GCP e habilitar faturamento
- Criar uma VM do motor de computação
- Instalar o Docker (tempo de execução da aplicação isolada)
- Iniciar o portal OpenClaw em Docker
- Persista <<CODE0>> + <<CODE1>> na máquina (sobrevivências reinicia/reconstrui)
- Acesse a interface de controle do seu laptop através de um túnel SSH

O Gateway pode ser acessado através de:

- Reencaminhamento de porta SSH de seu laptop
- Exposição direta à porta se você gerenciar firewall e tokens você mesmo

Este guia usa Debian no GCP Compute Engine.
O Ubuntu também funciona; mapeia os pacotes de acordo.
Para o fluxo genérico do Docker, ver [Docker] (<<<LINK0>>>).

---

# # Caminho rápido (operadores experientes)

1. Criar projeto GCP + habilitar a API do motor de computação
2. Criar VM do motor de computação (e2-pequeno, Debian 12, 20GB)
3. SSH na VM
4. Instalar o Docker
5. Clone repositório OpenClaw
6. Criar diretórios host persistentes
7. Configurar <<CODE0>> e <<CODE1>>>
8. Asse binários necessários, compilação e lançamento

---

# # O que precisas

- Conta GCP (nível livre elegível para e2-micro)
- CLI gcloud instalado (ou usar Console Cloud)
- Acesso SSH do seu laptop
- Conforto básico com SSH + cópia/cola
- 20-30 minutos.
- Docker e Docker Compõem
- Credenciais de autenticação de modelo
- Credenciais de provedor opcional
- WhatsApp QR
- Token bot de telegrama
- Gmail OAuth

---

# # 1) Instalar CLI gcloud (ou usar Console)

**Opção A: gcloud CLI** (recomendado para automação)

Instalar a partir de https://cloud.google.com/sdk/docs/install

Inicializar e autenticar:

```bash
gcloud init
gcloud auth login
```

**Opção B: Console em nuvem**

Todas as etapas podem ser feitas através da interface web em https://console.cloud.google.com

---

2) Criar um projeto GCP

** CLI:**

```bash
gcloud projects create my-openclaw-project --name="OpenClaw Gateway"
gcloud config set project my-openclaw-project
```

Ativar faturamento em https://console.cloud.google.com/billing (obrigatório para o motor de computação).

Habilitar a API do motor de computação:

```bash
gcloud services enable compute.googleapis.com
```

**Console:**

1. Vá para IAM & Admin > Criar projeto
2. Nome e criar
3. Habilitar faturamento para o projeto
4. Navegue para APIs e Serviços > Habilitar APIs > pesquisa "Compute Engine API" > Activar

---

# # 3) Criar a VM

**Tipos de máquinas:**

Tipo , Especificações , Custo , Notas
---------------------------------
2 vCPU, 2GB RAM ~$12/mo Recomendado
2 vCPU (compartilhado), 1GB de RAM, nível livre elegível, Maio OOM sob carga

** CLI:**

```bash
gcloud compute instances create openclaw-gateway \
  --zone=us-central1-a \
  --machine-type=e2-small \
  --boot-disk-size=20GB \
  --image-family=debian-12 \
  --image-project=debian-cloud
```

**Console:**

1. Vá para o motor de computação > instâncias VM > Criar instância
2. Nome: <<CODE0>>>
3. Região: <<CODE1>>, Zona: <<CODE2>>
4. Tipo de máquina: <<CODE3>>
5. Disco de inicialização: Debian 12, 20GB
6. Criar

---

# # 4) SSH na VM

** CLI:**

```bash
gcloud compute ssh openclaw-gateway --zone=us-central1-a
```

**Console:**

Clique no botão "SSH" ao lado da sua VM no painel do motor de computação.

Nota: A propagação da chave SSH pode levar 1-2 minutos após a criação da VM. Se a conexão for recusada, aguarde e tente novamente.

---

## 5) Instalar o Docker (na VM)

```bash
sudo apt-get update
sudo apt-get install -y git curl ca-certificates
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
```

Sair e voltar para a mudança de grupo para fazer efeito:

```bash
exit
```

Em seguida, SSH de volta em:

```bash
gcloud compute ssh openclaw-gateway --zone=us-central1-a
```

Verificar:

```bash
docker --version
docker compose version
```

---

## 6) Clone o repositório OpenClaw

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
```

Este guia assume que você irá construir uma imagem personalizada para garantir a persistência binária.

---

# # 7) Criar diretórios host persistentes

Os recipientes de docker são efêmeros.
Todo o estado de longa duração deve viver no hospedeiro.

```bash
mkdir -p ~/.openclaw
mkdir -p ~/.openclaw/workspace
```

---

## 8) Configurar variáveis de ambiente

Crie <<CODE0>> na raiz do repositório.

```bash
OPENCLAW_IMAGE=openclaw:latest
OPENCLAW_GATEWAY_TOKEN=change-me-now
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_GATEWAY_PORT=18789

OPENCLAW_CONFIG_DIR=/home/$USER/.openclaw
OPENCLAW_WORKSPACE_DIR=/home/$USER/.openclaw/workspace

GOG_KEYRING_PASSWORD=change-me-now
XDG_CONFIG_HOME=/home/node/.openclaw
```

Gerar segredos fortes:

```bash
openssl rand -hex 32
```

** Não commit este arquivo. **

---

## 9) Configuração do Docker Compor

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
      # Recommended: keep the Gateway loopback-only on the VM; access via SSH tunnel.
      # To expose it publicly, remove the `127.0.0.1:` prefix and firewall accordingly.
      - "127.0.0.1:${OPENCLAW_GATEWAY_PORT}:18789"

      # Optional: only if you run iOS/Android nodes against this VM and need Canvas host.
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

## 10) Asse binários necessários na imagem (crítico)

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

# # 11) Construir e lançar

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

## 12) Verificar o Portal

```bash
docker compose logs -f openclaw-gateway
```

Sucesso:

```
[gateway] listening on ws://0.0.0.0:18789
```

---

# # 13) Acesso do seu laptop

Criar um túnel SSH para a frente da porta Gateway:

```bash
gcloud compute ssh openclaw-gateway --zone=us-central1-a -- -L 18789:127.0.0.1:18789
```

Abra no seu navegador:

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

---

# # Atualizações

Para atualizar OpenClaw na VM:

```bash
cd ~/openclaw
git pull
docker compose build
docker compose up -d
```

---

# # Resolução de problemas

** Ligação SHS recusada**

A propagação da chave SSH pode levar 1-2 minutos após a criação da VM. Espere e tente novamente.

** OS Problemas de login**

Verifique o seu perfil de Login do SO:

```bash
gcloud compute os-login describe-profile
```

Certifique-se de que sua conta tem as permissões IAM necessárias (Compute OS Login ou Compute OS Admin Login).

** Fora de memória (OOM)

Se utilizar e2-micro e atingir OOM, atualizar para e2-pequeno ou e2-medium:

```bash
# Stop the VM first
gcloud compute instances stop openclaw-gateway --zone=us-central1-a

# Change machine type
gcloud compute instances set-machine-type openclaw-gateway \
  --zone=us-central1-a \
  --machine-type=e2-small

# Start the VM
gcloud compute instances start openclaw-gateway --zone=us-central1-a
```

---

# # Contas de serviço (melhores práticas de segurança)

Para uso pessoal, sua conta de usuário padrão funciona bem.

Para automação ou pipelines CI/CD, crie uma conta de serviço dedicada com permissões mínimas:

1. Criar uma conta de serviço:

   ```bash
   gcloud iam service-accounts create openclaw-deploy \
     --display-name="OpenClaw Deployment"
   ```

2. Grant Compute instância papel administrativo (ou papel personalizado mais estreito):
   ```bash
   gcloud projects add-iam-policy-binding my-openclaw-project \
     --member="serviceAccount:openclaw-deploy@my-openclaw-project.iam.gserviceaccount.com" \
     --role="roles/compute.instanceAdmin.v1"
   ```

Evite usar o papel de proprietário para automação. Use o princípio do menor privilégio.

Ver https://cloud.google.com/iam/docs/compreending-roles para detalhes de papel IAM.

---

# # Próximos passos

- Configurar canais de mensagens: [Canais](<<<LINK0>>)
- Emparelhe os dispositivos locais como nós: [Nos] (<<<LINK1>>>)
- Configurar o Gateway: [Configuração do Gateway] (<<<LINK2>>)
