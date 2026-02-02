---
summary: "Automated, hardened OpenClaw installation with Ansible, Tailscale VPN, and firewall isolation"
read_when:
  - You want automated server deployment with security hardening
  - You need firewall-isolated setup with VPN access
  - You're deploying to remote Debian/Ubuntu servers
---

Instalação Ansível

A maneira recomendada de implantar OpenClaw para servidores de produção é via **[openclaw-ansible](<<LINK0>>>)** — um instalador automatizado com arquitetura de segurança.

# # Início Rápido

Instalação de um comando:

```bash
curl -fsSL https://raw.githubusercontent.com/openclaw/openclaw-ansible/main/install.sh | bash
```

Guia completo: [github.com/openclaw/openclaw-ansível](<<<LINK0>>)**
>
> O openclaw-ansível repo é a fonte de verdade para implantação Ansível. Esta página é uma visão geral rápida.

# # O que você ganha

- **Segurança de primeira linha de fogo**: UFW + isolamento de encaixe (apenas SSH + Tailscale acessível)
- ** VPN de Taliscale**: Acesso remoto seguro sem expor publicamente os serviços
- ** Docker**: Recipientes isolados para caixas de areia, ligações locais apenas para máquinas de dormir
- ** Defesa em profundidade**: arquitetura de segurança de 4 camadas
- Configuração de um comando**: Implantação completa em minutos
- Integração sistemática**: Iniciar automaticamente no arranque com endurecimento

# # Requisitos

- **OS**: Debian 11+ ou Ubuntu 20.04+
- ** Acesso**: Privilégios de raiz ou sudo
- ** Rede**: Ligação à Internet para instalação de pacotes
- **Ansível**: 2.14+ (instalado automaticamente por script de arranque rápido)

# # O Que Fica Instalado

O playbook Ansível instala e configura:

1. **Tailscale** (mesh VPN para acesso remoto seguro)
2. **Firewall UFW** (SSH + portas de tailscale somente)
3. **Docker CE + Compose V2** (para sandboxes de agente)
4. **Node.js 22.x + pnpm** (dependências de execução)
5. ** OpenClaw** (baseado em máquinas, não em contentores)
6. ** Serviço sistematizado** (auto-iniciar com endurecimento de segurança)

Nota: O gateway roda ** diretamente no host** (não no Docker), mas as sandboxes do agente usam o Docker para isolamento. Ver [Sandboxing](<<<LINK0>>>) para mais detalhes.

Configuração Pós-Instalação

Após a instalação terminar, mude para o usuário openclaw:

```bash
sudo -i -u openclaw
```

O script pós-instalação irá guiá-lo através de:

1. ** assistente Onboarding**: Configurar configurações OpenClaw
2. **Login do fornecedor**: Conecte WhatsApp/Telegram/Discord/Signal
3. ** Teste de gateway**: Verificar a instalação
4. ** Configuração em escala de tail**: Conectar à malha VPN

Comandos rápidos

```bash
# Check service status
sudo systemctl status openclaw

# View live logs
sudo journalctl -u openclaw -f

# Restart gateway
sudo systemctl restart openclaw

# Provider login (run as openclaw user)
sudo -i -u openclaw
openclaw channels login
```

# # Arquitetura de Segurança

# # 4-Layer Defense

1. **Firewall (UFW)**: Apenas SSH (22) + Tailscale (41641/udp) expostos publicamente
2. **VPN (Tailscale)**: Gateway acessível apenas através de rede VPN
3. ** Isolamento do Docker**: DOCKER-USER iptables cadeia previne exposição externa porta
4. **Endurecimento sistematizado**: NoNewPrivileges, PrivateTmp, user unprivileged

Verificação

Ensaio de superfície de ataque externa:

```bash
nmap -p- YOUR_SERVER_IP
```

Deve mostrar apenas a porta 22** (SSH) aberta. Todos os outros serviços (porta, Docker) estão bloqueados.

Disponibilidade de Docker

O Docker está instalado para ** agent sandboxes** (execução de ferramenta isolada), não para executar o gateway em si. O gateway se liga apenas ao localhost e é acessível via Tailscale VPN.

Ver [Multi-Agent Sandbox & Tools] (<<<LINK0>>>) para configuração sandbox.

Instalação manual

Se preferir controle manual sobre a automação:

```bash
# 1. Install prerequisites
sudo apt update && sudo apt install -y ansible git

# 2. Clone repository
git clone https://github.com/openclaw/openclaw-ansible.git
cd openclaw-ansible

# 3. Install Ansible collections
ansible-galaxy collection install -r requirements.yml

# 4. Run playbook
./run-playbook.sh

# Or run directly (then manually execute /tmp/openclaw-setup.sh after)
# ansible-playbook playbook.yml --ask-become-pass
```

# # Atualizando Openclaw

O instalador Ansible configura OpenClaw para atualizações manuais. Ver [Atualização](<<<LINK0>>>) para o fluxo de atualização padrão.

Para repetir o playbook Ansível (por exemplo, para alterações de configuração):

```bash
cd openclaw-ansible
./run-playbook.sh
```

Nota: Isto é idempotente e seguro para correr várias vezes.

# # Resolução de problemas

Firewall bloqueia a minha ligação

Se estiveres trancada para fora.

- Assegure-se de que você pode acessar via Tailscale VPN primeiro
- Acesso SSH (porto 22) é sempre permitido
- O gateway é **apenas** acessível via Tailscale por design

O serviço não vai começar

```bash
# Check logs
sudo journalctl -u openclaw -n 100

# Verify permissions
sudo ls -la /opt/openclaw

# Test manual start
sudo -i -u openclaw
cd ~/openclaw
pnpm start
```

Problemas com a caixa de areia

```bash
# Verify Docker is running
sudo systemctl status docker

# Check sandbox image
sudo docker images | grep openclaw-sandbox

# Build sandbox image if missing
cd /opt/openclaw/openclaw
sudo -u openclaw ./scripts/sandbox-setup.sh
```

O login do provedor falhou

Certifique-se de que você está rodando como o usuário <<CODE0>>:

```bash
sudo -i -u openclaw
openclaw channels login
```

# # Configuração Avançada

Para arquitetura de segurança detalhada e solução de problemas:

- [Arquitectura de segurança] (<<<LINK0>>)
- [Detalhes técnicos] (<<<LINK1>>>)
- [Guia de Resolução de Problemas] (<<<LINK2>>>)

# # Relacionado

- [ansível em aberto](<<<LINK0>>) — guia de implantação completo
- [Docker] (<<<LINK1>>) — configuração de gateway em contentores
- [Sandboxing] (<<<LINK2>>>) — configuração da caixa de areia do agente
- [Multi-Agent Sandbox & Tools] (<<<LINK3>>) — isolamento por agente
