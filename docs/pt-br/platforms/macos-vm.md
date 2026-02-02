---
summary: "Run OpenClaw in a sandboxed macOS VM (local or hosted) when you need isolation or iMessage"
read_when:
  - You want OpenClaw isolated from your main macOS environment
  - You want iMessage integration (BlueBubbles) in a sandbox
  - You want a resettable macOS environment you can clone
  - You want to compare local vs hosted macOS VM options
---

# Openclaw em macOS VMs (Sandboxing)

# # Predefinição recomendada (a maioria dos usuários)

- **Small Linux VPS** para um Gateway sempre-em e baixo custo. Ver [Alojamento VPS] (</vps).
- ** Hardware dedicado** (Mac mini ou Linux box) se você quiser controle completo e um ** IP residencial** para automação de navegador. Muitos sites bloqueiam IPs de data center, então a navegação local muitas vezes funciona melhor.
- **Hybrid:** mantenha o Gateway em um VPS barato e conecte seu Mac como um **node** quando você precisar de automação navegador / UI. Ver [Nodes] (</nodes) e [Relator de via remota] (/gateway/remote).

Use uma VM do macOS quando você precisa especificamente de recursos somente do macOS (iMessage/BlueBubbles) ou queira isolamento restrito do seu Mac diário.

# # opções de VM do macOS

# # # VM local no Mac de Silício Apple (Lume)

Execute OpenClaw em uma caixa de areia MacOS VM em seu Apple Silicon Mac existente usando [Lume](https://cua.ai/docs/lume).

Isto dá-lhe:

- Ambiente macOS completo em isolamento (o seu anfitrião permanece limpo)
- Suporte iMessage via BlueBubbles (impossível no Linux/Windows)
- Reset instantâneo clonando VMs
- Sem custos adicionais de hardware ou nuvem

## # Provedores de Mac hospedados (nuvem)

Se você quer macOS na nuvem, provedores Mac hospedados também funcionam:

- [MacStadium] (<https://www.macstadium.com/) ( Macs hospedados)
- Outros fornecedores Mac hospedados também funcionam; siga seus documentos VM + SSH

Depois de ter acesso SSH a uma VM do macOS, continue no passo 6 abaixo.

---

# # Caminho rápido (Lume, usuários experientes)

1. Instalar Lume
2. `lume create openclaw --os macos --ipsw latest`
3. Assistente de configuração completo, ativar o login remoto (SSH)
4. <<CODE1>
5. SSH em, instalar OpenClaw, configurar canais
6. Feito

---

# # O que precisas (Lume)

- Apple Silicon Mac (M1/M2/M3/M4)
- macOS Sequoia ou posterior no hospedeiro
- ~60 GB de espaço livre em disco por VM
- 20 minutos.

---

# # 1) Instalar Lume

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/trycua/cua/main/libs/lume/scripts/install.sh)"
```

Se <<CODE0> não estiver no seu PATH:

```bash
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.zshrc && source ~/.zshrc
```

Verificar:

```bash
lume --version
```

Docs: [Instalação Lume] (<https://cua.ai/docs/lume/guide/getting-started/installation)

---

# # 2) Criar o macOS VM

```bash
lume create openclaw --os macos --ipsw latest
```

Isso baixa o macOS e cria a VM. Uma janela VNC abre automaticamente.

Nota: O download pode demorar um pouco dependendo da sua conexão.

---

# # 3) Assistente de configuração completo

Na janela VNC:

1. Selecione idioma e região
2. Ignorar o ID Apple (ou iniciar sessão se quiser iMessage mais tarde)
3. Crie uma conta de usuário (lembre-se do nome de usuário e senha)
4. Pular todos os recursos opcionais

Após a configuração completa, habilitar SSH:

1. Configurações do sistema aberto → Geral → Compartilhamento
2. Habilitar "Login remoto"

---

# # 4) Obter o endereço IP da VM

```bash
lume get openclaw
```

Procure o endereço IP (normalmente `192.168.64.x`).

---

5) SSH na VM

```bash
ssh youruser@192.168.64.X
```

Substituir `youruser` pela conta que criou e o IP pelo IP da sua VM.

---

# # 6) Instalar OpenClaw

Dentro da VM:

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

Siga as instruções de onboarding para configurar seu provedor de modelo (Anthropic, OpenAI, etc.).

---

## 7) Configurar canais

Editar o ficheiro de configuração:

```bash
nano ~/.openclaw/openclaw.json
```

Adicione seus canais:

```json
{
  "channels": {
    "whatsapp": {
      "dmPolicy": "allowlist",
      "allowFrom": ["+15551234567"]
    },
    "telegram": {
      "botToken": "YOUR_BOT_TOKEN"
    }
  }
}
```

Em seguida, faça login no WhatsApp (scan QR):

```bash
openclaw channels login
```

---

# # 8) Execute a VM sem cabeça

Parar a VM e reiniciar sem exibição:

```bash
lume stop openclaw
lume run openclaw --no-display
```

A VM corre ao fundo. O daemon do OpenClaw mantém o portal a funcionar.

Para verificar o estado:

```bash
ssh youruser@192.168.64.X "openclaw status"
```

---

# # Bônus: integração iMessage

Esta é a característica assassina de correr no macOS. Use [BlueBubbles] (<https://bluebubbles.app) para adicionar iMessage ao OpenClaw.

Dentro da VM:

1. Baixe BlueBubbles de bluebubbles.app
2. Entre com o ID Apple
3. Habilite a API Web e defina uma senha
4. Ponto BlueBubbles webhooks em seu gateway (exemplo: `https://your-gateway-host:3000/bluebubbles-webhook?password=<password>`)

Adicionar à sua configuração do OpenClaw:

```json
{
  "channels": {
    "bluebubbles": {
      "serverUrl": "http://localhost:1234",
      "password": "your-api-password",
      "webhookPath": "/bluebubbles-webhook"
    }
  }
}
```

Reinicia o portal. Agora seu agente pode enviar e receber iMensages.

Detalhes completos da configuração: [Canal BlueBubbles] (</channels/bluebubbles)

---

# # Salvar uma imagem dourada

Antes de personalizar ainda mais, instantâneo seu estado limpo:

```bash
lume stop openclaw
lume clone openclaw openclaw-golden
```

Reiniciar a qualquer momento:

```bash
lume stop openclaw && lume delete openclaw
lume clone openclaw-golden openclaw
lume run openclaw --no-display
```

---

# # Correndo 24 horas por dia

Mantenha a VM rodando por:

- Manter o Mac ligado
- Desativando o sono em Configurações do Sistema → Energy Saver
- Utilizar <<CODE0> se necessário

Para verdadeiro sempre, considere um mini Mac dedicado ou um pequeno VPS. Ver [Alojamento VPS] (</vps).

---

# # Resolução de problemas

□ Problema
□ -------------------------------------------------------------------------------------------------------------------------
Não é possível SSH para a VM Verificar "Login remoto" está habilitado nas configurações do sistema da VM
O IP da VM não está a mostrar O esperar que a VM arranque totalmente, execute novamente <<CODE0>
O comando Lume não foi encontrado.
□ WhatsApp QR not scaning Certifique-se de que você está logado na VM (não host) ao executar `openclaw channels login`

---

# # Docs relacionados

- [Alojamento VPS] (</vps)
- [Nós] (/nodes)
- [Relatório remoto do portal] (</gateway/remote)
- [Canal BlueBubbles] (</channels/bluebubbles)
- [Lume Quickstart] (<https://cua.ai/docs/lume/guide/getting-started/quickstart)
- [Lume CLI Reference] (<https://cua.ai/docs/lume/reference/cli-reference)
- [Configuração da VM sem supervisão] (<https://cua.ai/docs/lume/guide/fundamentals/unattended-setup) (avançada)
- [Docker Sandboxing] (</install/docker) (abordagem de isolamento alternativo)
