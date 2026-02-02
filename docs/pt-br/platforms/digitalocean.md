---
summary: "OpenClaw on DigitalOcean (simple paid VPS option)"
read_when:
  - Setting up OpenClaw on DigitalOcean
  - Looking for cheap VPS hosting for OpenClaw
---

Openclaw no DigitalOcean

# # Objetivo

Execute um Gateway OpenClaw persistente no DigitalOcean por **$6/mês** (ou $4/mo com preços reservados).

Se você quiser uma opção de $0/mês e não se importe com a configuração específica do provedor ARM +, consulte o [Guia de Nuvem de Oracle](<<LINK0>>).

# # Comparação de custos (2026)

Previdência Plan Plano Especificações Preço/mo Notas
--------------- ---------------- -------------
* Oracle Cloud * Sempre livre de ARM * até 4 OCPU, 24GB RAM * $0 * ARM, capacidade limitada / peculiaridades de inscrição *
* Hetzner * CX22 * 2 vCPU * 4GB de RAM * 3,79 € (~$4) * Opção mais barata paga *
• DigitalOcean • Basic 1 vCPU, 1GB de RAM • $6 • Interface fácil, bons documentos
Computação de nuvem de Vultr 1 vCPU, 1GB de RAM de $6
Linode □ Nanode 1 vCPU, 1GB de RAM

** Escolher um fornecedor: **

- DigitalOcean: configuração UX + previsível mais simples (este guia)
- Hetzner: bom preço/perf (ver [Guia Hetzner] (<<<LINK0>>>))
- Oracle Cloud: pode ser $0/mês, mas é mais finicky e ARM-somente (veja [guia Oracle](<<LINK1>>))

---

# # Pré-requisitos

- Conta DigitalOcean ([assinatura com crédito grátis de 200 dólares] (<<<LINK0>>>))
- Par de chaves SSH (ou vontade de usar senha)
- 20 minutos.

# # 1) Criar uma gota

1. Entrar em [DigitalOcean] (<<<LINK0>>)
2. Clique em **Criar → Gotas**
3. Escolha:
- **Região:** Mais próximo de você (ou seus usuários)
- **Imagem:** Ubuntu 24.04 LTS
- **Tamanho:** Basic → Regular → **$6/mo** (1 vCPU, 1GB RAM, 25GB SSD)
- **Autenticação:** Chave SSH (recomendada) ou senha
4. Clique em **Criar gota **
5. Observe o endereço IP

# # 2) Conectar através de SSH

```bash
ssh root@YOUR_DROPLET_IP
```

# # 3) Instalar OpenClaw

```bash
# Update system
apt update && apt upgrade -y

# Install Node.js 22
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs

# Install OpenClaw
curl -fsSL https://openclaw.bot/install.sh | bash

# Verify
openclaw --version
```

# # 4) Correr a bordo

```bash
openclaw onboard --install-daemon
```

O feiticeiro irá guiá-lo.

- Modelo de autenticação (chaves API ou OAuth)
- Configuração do canal (Telegrama, WhatsApp, Discórdia, etc.)
- Token Gateway (gerado automaticamente)
- Instalação do servidor (systemd)

## 5) Verificar a Porta

```bash
# Check status
openclaw status

# Check service
systemctl --user status openclaw-gateway.service

# View logs
journalctl --user -u openclaw-gateway.service -f
```

# # 6) Acesse o Painel

O gateway se liga ao loopback por padrão. Para aceder à interface de controlo:

** Opção A: Túnel SSH (recomendado)

```bash
# From your local machine
ssh -L 18789:localhost:18789 root@YOUR_DROPLET_IP

# Then open: http://localhost:18789
```

**Opção B: Servir em escala de cauda (HTTPS, loopback-only)**

```bash
# On the droplet
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up

# Configure Gateway to use Tailscale Serve
openclaw config set gateway.tailscale.mode serve
openclaw gateway restart
```

Abrir: <<CODE0>>

Notas:

- Servir mantém o Gateway loopback-somente e autentica através de cabeçalhos de identidade Tailscale.
- Para exigir token/password, definir <<CODE0>> ou utilizar <<CODE1>>>.

**Opção C: ligação tailnet (sem serviço)**

```bash
openclaw config set gateway.bind tailnet
openclaw gateway restart
```

Abrir: <<CODE0>> (preciso).

# # 7) Conecte seus canais

Telegrama

```bash
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

WhatsApp

```bash
openclaw channels login whatsapp
# Scan QR code
```

Ver [Canais](<<<LINK0>>>) para outros prestadores.

---

# # Otimizações para 1GB de RAM

A gota de $6 só tem 1GB de RAM. Para manter as coisas a correr bem:

## # Adicionar swap (recomendado)

```bash
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

# # Usa um modelo mais leve

Se estiver a fazer OOMs, considere:

- Usando modelos baseados em API (Claude, GPT) em vez de modelos locais
- Configurando <<CODE0>> para um modelo mais pequeno

Monitora a memória

```bash
free -h
htop
```

---

# # Persistência

Todos os estados vivem em:

- <<CODE0>> — configuração, credenciais, dados da sessão
- <<CODE1>> – espaço de trabalho (SOUL.md, memória, etc.)

Estes sobrevivem a reinicialização. Reforçá-los periodicamente:

```bash
tar -czvf openclaw-backup.tar.gz ~/.openclaw ~/.openclaw/workspace
```

---

# # Alternativa livre da nuvem do Oracle

Oracle Cloud oferece **Sempre Grátis** instâncias ARM que são significativamente mais poderosas do que qualquer opção paga aqui — por $0/mês.

* O que você começa * Especificações *
----------------- ----------------------
* 4 OCPUs** * ARM Ampere A1
Mais do que suficiente
Armazenamento de 200GB** Volume de bloco
* Para sempre livre** Sem cobranças de cartão de crédito

**Caveats:**

- Inscrição pode ser finicky (tentar se falhar)
- Arquitetura ARM — a maioria das coisas funcionam, mas alguns binários precisam de construções ARM

Para o guia completo de configuração, consulte [Oracle Cloud](<<LINK0>>>). Para dicas de inscrição e solução de problemas no processo de inscrição, consulte este [guia comunitário](<<LINK1>>).

---

# # Resolução de problemas

O portal não começa

```bash
openclaw gateway status
openclaw doctor --non-interactive
journalctl -u openclaw --no-pager -n 50
```

# # # Porto já em uso

```bash
lsof -i :18789
kill <PID>
```

Sem memória

```bash
# Check memory
free -h

# Add more swap
# Or upgrade to $12/mo droplet (2GB RAM)
```

---

# # Veja também

- [Guia Hetzner] (<<<LINK0>>) — mais barato, mais poderoso
- [Docker install] (<<<LINK1>>) — configuração em contentores
- [Tailscale] (<<<LINK2>>) — acesso remoto seguro
- [Configuração] (<<<LINK3>>>) — referência de configuração completa
