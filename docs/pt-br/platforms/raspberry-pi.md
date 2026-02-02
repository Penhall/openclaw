---
summary: "OpenClaw on Raspberry Pi (budget self-hosted setup)"
read_when:
  - Setting up OpenClaw on a Raspberry Pi
  - Running OpenClaw on ARM devices
  - Building a cheap always-on personal AI
---

Openclaw em Raspberry Pi

# # Objetivo

Executar um persistente, sempre-em OpenClaw Gateway em um Pi Framboesa para **~$35-80** custo único (sem taxas mensais).

Perfeito para:

- Assistente pessoal de IA 24/7
- Domótica hub
- Bot Telegram/WhatsApp de baixa potência e sempre disponível

# # Requisitos de Hardware

□ Pi Model □ RAM Funciona? Notas
------------------- -------------------------------------------------
Mais rápido, recomendado
Ponto doce para a maioria dos usuários
*Pi 4** * 2GB
*Pi 4** * 1GB *Possível com swap, configuração mínima *
*Pi 3B+** * 1GB * Lento * Funciona mas lento *
Não recomendado

** Especificações mínimas:** 1GB de RAM, 1 core, 500MB de disco
**Recomendado:** 2GB + RAM, 64-bit OS, 16GB + cartão SD (ou SSD USB)

# # Do que vais precisar

- Framboesa Pi 4 ou 5 (2GB+ recomendado)
- Cartão MicroSD (16GB+) ou SSD USB (melhor desempenho)
- Fonte de alimentação (recomendado oficial Pi PSU)
- Conexão de rede (Ethernet ou WiFi)
- 30 minutos.

# # 1) Flash the OS

Use **Raspberry Pi OS Lite (64 bits)** — nenhum desktop necessário para um servidor sem cabeça.

1. Download [Raspberry Pi Imager] (<https://www.raspberrypi.com/software/)
2. Escolha OS: **Raspberry Pi OS Lite (64 bits)**
3. Clique no ícone da engrenagem (ou) para pré-configurar:
- Definir nome da máquina: `gateway-host`
- Activar SSH
- Definir nome de usuário/senha
- Configurar WiFi (se não usar Ethernet)
4. Flash para o seu cartão SD / unidade USB
5. Inserir e arrancar o Pi

# # 2) Conectar através de SSH

```bash
ssh user@gateway-host
# or use the IP address
ssh user@192.168.x.x
```

3) Configuração do Sistema

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y git curl build-essential

# Set timezone (important for cron/reminders)
sudo timedatectl set-timezone America/Chicago  # Change to your timezone
```

# # 4) Instalar Node.js 22 (ARM64)

```bash
# Install Node.js via NodeSource
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs

# Verify
node --version  # Should show v22.x.x
npm --version
```

# # 5) Adicionar Troca (Importante por 2GB ou menos)

A troca impede quebras fora de memória:

```bash
# Create 2GB swap file
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Optimize for low RAM (reduce swappiness)
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

# # 6) Instalar OpenClaw

## # Opção A: Instalação Padrão (Recomendada)

```bash
curl -fsSL https://openclaw.bot/install.sh | bash
```

## # Opção B: Instalação hackeável (para correção)

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
npm install
npm run build
npm link
```

A instalação hackable lhe dá acesso direto a logs e código — útil para depuração de problemas específicos do ARM.

## 7) Correr a bordo

```bash
openclaw onboard --install-daemon
```

Siga o assistente:

1. ** Modo Gateway:** Local
2. ** Auth:** teclas API recomendadas (OAuth pode ser finicky em pi sem cabeça)
3. **Canais:** Telegrama é mais fácil de começar com
4. ** Daemon:** Sim (systemd)

# # 8) Verificar instalação

```bash
# Check status
openclaw status

# Check service
sudo systemctl status openclaw

# View logs
journalctl -u openclaw -f
```

# # 9) Acesse o Painel

Como o Pi está sem cabeça, use um túnel SSH:

```bash
# From your laptop/desktop
ssh -L 18789:localhost:18789 user@gateway-host

# Then open in browser
open http://localhost:18789
```

Ou use Tailscale para acesso sempre em:

```bash
# On the Pi
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Update config
openclaw config set gateway.bind tailnet
sudo systemctl restart openclaw
```

---

# # Otimizações de desempenho

## # Use um SSD USB (Melhoramento de Huge)

Os cartões SD são lentos e desgastam. Um SSD USB melhora drasticamente o desempenho:

```bash
# Check if booting from USB
lsblk
```

Veja [Guia de inicialização USB do Pi](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#usb-mass-storage-boot) para configuração.

Reduzir o uso da memória

```bash
# Disable GPU memory allocation (headless)
echo 'gpu_mem=16' | sudo tee -a /boot/config.txt

# Disable Bluetooth if not needed
sudo systemctl disable bluetooth
```

# # # Monitorar recursos

```bash
# Check memory
free -h

# Check CPU temperature
vcgencmd measure_temp

# Live monitoring
htop
```

---

# # Notas Específicas de ARM

# # Compatibilidade binária

A maioria dos recursos OpenClaw funcionam no ARM64, mas alguns binários externos podem precisar de construções ARM:

□ Ferramenta □ Estado ARM64 Notas
------------------ --------------- ---------------------------------------------------
Node.js Funciona muito bem
* WhatsApp (Baileys) * Puro JS, sem problemas *
* Telegram *
□ gog (Gmail CLI)
* Chromium (browser)

Se uma habilidade falhar, verifique se seu binário tem uma compilação ARM. Muitas ferramentas Go/Rust fazem; algumas não.

# # 32-bit vs 64-bit

**Sempre use 64-bit OS.** Node.js e muitas ferramentas modernas exigem-no. Verificar com:

```bash
uname -m
# Should show: aarch64 (64-bit) not armv7l (32-bit)
```

---

Configuração recomendada do modelo

Como o Pi é apenas o Gateway (modelos executados na nuvem), use modelos baseados em API:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-20250514",
        "fallbacks": ["openai/gpt-4o-mini"]
      }
    }
  }
}
```

**Não tente executar LLMs locais em um Pi** — mesmo modelos pequenos são muito lentos. Deixe Claude/GPT fazer o trabalho pesado.

---

# # Iniciar automaticamente na inicialização

O assistente de integração configura isto, mas para verificar:

```bash
# Check service is enabled
sudo systemctl is-enabled openclaw

# Enable if not
sudo systemctl enable openclaw

# Start on boot
sudo systemctl start openclaw
```

---

# # Resolução de problemas

# # Fora de Memória (OOM)

```bash
# Check memory
free -h

# Add more swap (see Step 5)
# Or reduce services running on the Pi
```

# # Desempenho lento

- Use SSD USB em vez de cartão SD
- Desactivar os serviços não utilizados: `sudo systemctl disable cups bluetooth avahi-daemon`
- Verificar a aceleração da CPU: `vcgencmd get_throttled` (deverá retornar `0x0`)

O serviço não começa

```bash
# Check logs
journalctl -u openclaw --no-pager -n 100

# Common fix: rebuild
cd ~/openclaw  # if using hackable install
npm run build
sudo systemctl restart openclaw
```

## # Questões binárias do ARM

Se uma habilidade falhar com "erro de formato de execução":

1. Verifique se o binário tem uma compilação ARM64
2. Tente construir de origem
3. Ou usar um recipiente Docker com suporte ARM

Gotas de Wi-Fi

Para pis sem cabeça no WiFi:

```bash
# Disable WiFi power management
sudo iwconfig wlan0 power off

# Make permanent
echo 'wireless-power off' | sudo tee -a /etc/network/interfaces
```

---

# # Comparação de custos

Setup , custo único , custo mensal , notas
----------------- ------------------------------------
*Pi 4 (2GB)** ~$45
*Pi 4 (4GB)** ~$55 * $0 Recomendado *
*Pi 5 (4GB)** ~$60 * $0 * Melhor desempenho *
*Pi 5 (8GB)** ~$80 * $0 * Overkill mas à prova de futuro *
* DigitalOcean * $0 * $6/mo * $72/ano *
* Hetzner * $0 €3,79/mo * ~$50/ano *

**Break-even:** A Pi paga por si mesma em ~6-12 meses vs nuvem VPS.

---

# # Veja também

- [Guia Linux] (</platforms/linux) — configuração geral do Linux
- [Guia DigitalOceano] (</platforms/digitalocean) — alternativa de nuvem
- [Guia Hetzner] (/platforms/hetzner) Configuração do Docker
- [Tailscale] (</gateway/tailscale) — acesso remoto
- [Nodes] (</nodes) — emparelhe seu laptop/telefone com o gateway Pi
