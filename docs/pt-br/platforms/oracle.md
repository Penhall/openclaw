---
summary: "OpenClaw on Oracle Cloud (Always Free ARM)"
read_when:
  - Setting up OpenClaw on Oracle Cloud
  - Looking for low-cost VPS hosting for OpenClaw
  - Want 24/7 OpenClaw on a small server
---

# Openclaw on Oracle Cloud (OCI)

# # Objetivo

Execute um Gateway OpenClaw persistente na Oracle Cloud **Sempre Livre** Nível ARM.

O nível livre da Oracle pode ser um ótimo ajuste para OpenClaw (especialmente se você já tem uma conta OCI), mas vem com tradeoffs:

- Arquitetura ARM (a maioria das coisas funcionam, mas alguns binários podem ser apenas x86)
- Capacidade e inscrição pode ser finicky

# # Comparação de custos (2026)

Previdência Plan Plano Especificações Preço/mo Notas
-------------- ------------------ -----------
Oráculo Nuvem Sempre livre ARM até 4 OCPU, 24GB de RAM, capacidade limitada
* Hetzner * CX22 * 2 vCPU, 4GB de RAM ~ $4 * Opção paga mais barata
• DigitalOcean • Basic 1 vCPU, 1GB de RAM • $6 • Interface fácil, bons documentos
Computação de nuvem de Vultr 1 vCPU, 1GB de RAM de $6
Linode □ Nanode 1 vCPU, 1GB de RAM

---

# # Pré-requisitos

- Conta da Oracle Cloud ([sinal](<https://www.oracle.com/cloud/free/)) — consulte [Guia de inscrição da comunidade](<https://gist.github.com/rssnyder/51e3cfedd730e7dd5f4a816143b25dbd) se tiver problemas
- Conta de tailscale (livre em [tailscale.com](https://tailscale.com))
- 30 minutos.

1) Criar uma instância OCI

1. Entrar em [Console de nuvem de oracle] (<https://cloud.oracle.com/)
2. Navegar para **Computar → Instâncias → Criar instância**
3. Configurar:
- Nome:** `openclaw`
- ** Imagem:** Ubuntu 24.04 (aarch64)
- ** Forma:** `VM.Standard.A1.Flex` (Ampere ARM)
- ** OCPU:** 2 (ou até 4)
- ** Memória:** 12 GB (ou até 24 GB)
- ** Volume da bola:** 50 GB (até 200 GB livre)
- ** Chave SHSS: ** Adicionar a sua chave pública
4. Clique em ** Criar **
5. Observe o endereço IP público

**Dica: ** Se a criação de instância falhar com "Sem capacidade", tente um domínio de disponibilidade diferente ou tente novamente mais tarde. A capacidade de nível livre é limitada.

# # 2) Conectar e Atualizar

```bash
# Connect via public IP
ssh ubuntu@YOUR_PUBLIC_IP

# Update system
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential
```

**Nota:** `build-essential` é necessária para a compilação de algumas dependências.

# # 3) Configurar o usuário e o nome do host

```bash
# Set hostname
sudo hostnamectl set-hostname openclaw

# Set password for ubuntu user
sudo passwd ubuntu

# Enable lingering (keeps user services running after logout)
sudo loginctl enable-linger ubuntu
```

# # 4) Instalar escala de cauda

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --ssh --hostname=openclaw
```

Isso habilita o Tailscale SSH, para que você possa se conectar via <<CODE0> de qualquer dispositivo em sua tailnet — nenhum IP público necessário.

Verificar:

```bash
tailscale status
```

**De agora em diante, conecte-se via Tailscale:** `ssh ubuntu@openclaw` (ou use o IP Tailscale).

# # 5) Instalar OpenClaw

```bash
curl -fsSL https://openclaw.bot/install.sh | bash
source ~/.bashrc
```

Quando solicitado "Como você quer chocar seu bot?", selecione **"Faça isso mais tarde"**.

> Nota: Se você clicar em problemas de compilação ARM-native, comece com pacotes de sistema (por exemplo, `sudo apt install -y build-essential`) antes de chegar ao Homebrew.

# # 6) Configurar Gateway (loopback + token auth) e ativar Tailscale Serve

Usar a autenticação do token como o padrão. É previsível e evita a necessidade de quaisquer bandeiras de controle de IU “inseguro”.

```bash
# Keep the Gateway private on the VM
openclaw config set gateway.bind loopback

# Require auth for the Gateway + Control UI
openclaw config set gateway.auth.mode token
openclaw doctor --generate-gateway-token

# Expose over Tailscale Serve (HTTPS + tailnet access)
openclaw config set gateway.tailscale.mode serve
openclaw config set gateway.trustedProxies '["127.0.0.1"]'

systemctl --user restart openclaw-gateway
```

# # 7) Verificar

```bash
# Check version
openclaw --version

# Check daemon status
systemctl --user status openclaw-gateway

# Check Tailscale Serve
tailscale serve status

# Test local response
curl http://localhost:18789
```

8) Bloquear a segurança VCN

Agora que tudo está a funcionar, bloqueie o VCN para bloquear todo o tráfego, excepto o Tailscale. A Rede de Nuvem Virtual da OCI atua como um firewall na borda da rede — o tráfego é bloqueado antes de chegar à sua instância.

1. Ir para **Networking → Redes de nuvem virtual** no Console OCI
2. Clique em seu VCN → **Listas de segurança** → Lista de segurança padrão
3. **Remover** todas as regras de entrada, exceto:
- <<CODE0> (Tailscale)
4. Mantenha as regras de saída padrão (permitir todas as saídas)

Isso bloqueia o SSH na porta 22, HTTP, HTTPS e tudo mais na borda da rede. A partir de agora, você só pode se conectar via Tailscale.

---

# # Acesse a interface de controle

A partir de qualquer dispositivo em sua rede Tailscale:

```
https://openclaw.<tailnet-name>.ts.net/
```

Substituir `<tailnet-name>` pelo nome da sua rede de cauda (visível em `tailscale status`).

Não é necessário nenhum túnel SSH. A escala de caudas fornece:

- Criptografia HTTPS (certas automáticas)
- Autenticação via identidade Tailscale
- Acesso de qualquer dispositivo na sua tailnet (laptop, telefone, etc.)

---

# # Segurança: VCN + Escala de cauda (linha de base recomendada)

Com o VCN bloqueado (somente o UDP 41641 aberto) e o Gateway ligado ao loopback, você obtém forte defesa em profundidade: o tráfego público é bloqueado na borda da rede, e o acesso do administrador acontece na sua tailnet.

Esta configuração muitas vezes remove o  need  para regras de firewall baseadas em host extra puramente para parar a força bruta SSH na Internet — mas você ainda deve manter o sistema operacional atualizado, executar `openclaw security audit`, e verificar que você não está ouvindo acidentalmente em interfaces públicas.

O que já está protegido

Passo Tradicional Necessário?
-----------------------------------
O firewall do UFW Não bloco VCN antes que o tráfego chegue à instância
Falhar2ban Não Nenhuma força bruta se a porta 22 bloqueada em VCN
Endurecimento do sshd Não, SSH não usa Sshd
□ Desactivar o login do root
Autenticação SSH-somente da chave
O endurecimento do IPv6 Normalmente não depende das configurações do seu VCN/subnet; verifique o que é realmente atribuído/exposto

# # Ainda Recomendado

- ** Permissões de crédito:** <<CODE0>
- ** Auditoria de segurança:** `openclaw security audit`
- ** Actualizações do sistema:** <<CODE2> regularmente
- **Monitor Tailscale:** Dispositivos de revisão em [Console de administrador de Talescale](<https://login.tailscale.com/admin)

Verifique a postura de segurança

```bash
# Confirm no public ports listening
sudo ss -tlnp | grep -v '127.0.0.1\|::1'

# Verify Tailscale SSH is active
tailscale status | grep -q 'offers: ssh' && echo "Tailscale SSH active"

# Optional: disable sshd entirely
sudo systemctl disable --now ssh
```

---

# # Regresso: Túnel SSH

Se Tailscale Serve não estiver funcionando, use um túnel SSH:

```bash
# From your local machine (via Tailscale)
ssh -L 18789:127.0.0.1:18789 ubuntu@openclaw
```

Em seguida, abra `http://localhost:18789`.

---

# # Resolução de problemas

### A criação da instância falha ("Sem capacidade")

As instâncias ARM de nível livre são populares. Tente:

- Domínio de disponibilidade diferente
- Repetir durante as horas fora do pico (início da manhã)
- Use o filtro "Sempre Livre" ao selecionar a forma

A escala de cauda não se liga

```bash
# Check status
sudo tailscale status

# Re-authenticate
sudo tailscale up --ssh --hostname=openclaw --reset
```

O portal não começa

```bash
openclaw gateway status
openclaw doctor --non-interactive
journalctl --user -u openclaw-gateway -n 50
```

Não consigo alcançar a interface de controle

```bash
# Verify Tailscale Serve is running
tailscale serve status

# Check gateway is listening
curl http://localhost:18789

# Restart if needed
systemctl --user restart openclaw-gateway
```

## # Questões binárias do ARM

Algumas ferramentas podem não ter construções ARM. Verificar:

```bash
uname -m  # Should show aarch64
```

A maioria dos pacotes npm funciona bem. Para os binários, procure `linux-arm64` ou `aarch64`.

---

# # Persistência

Todos os estados vivem em:

- `~/.openclaw/` — configuração, credenciais, dados da sessão
- <<CODE1> – espaço de trabalho (SOUL.md, memória, artefactos)

Recuar periodicamente:

```bash
tar -czvf openclaw-backup.tar.gz ~/.openclaw ~/.openclaw/workspace
```

---

# # Veja também

- [Acesso remoto ao portal] (</gateway/remote) — outros padrões de acesso remoto
- [Integração em escala tail] (</gateway/tailscale) — documentos completos em escala tail
- [Configuração do portal] (</gateway/configuration) — todas as opções de configuração
- [DigitalOcean guide] (</platforms/digitalocean) — se você quiser pagar + inscrição mais fácil
- [Guia Hetzner] (/platforms/hetzner) Alternativa baseada no encaixe
