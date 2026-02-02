---
summary: "Beginner guide: from zero to first message (wizard, auth, channels, pairing)"
read_when:
  - First time setup from zero
  - You want the fastest path from install → onboarding → first message
---

Começar

Objetivo: ir de **zero** → **primeiro chat de trabalho** (com padrões sãos) o mais rápido possível.

Bate-papo mais rápido: abra a interface de controle (sem necessidade de configuração do canal). Executar <<CODE0>>
e conversar no navegador, ou abrir <<CODE1>> no host gateway.
Docs: [Dashboard] (<<<LINK0>>>) e [Control UI] (<<LINK1>>>).

Localização recomendada: use o assistente ** CLI onboarding** (<<CODE0>>>). Estabelece:

- modelo/auth (OAuth recomendado)
- configurações de gateway
- canais (WhatsApp/Telegram/Discord/Mattermost (plugin)/...)
- padrões de pareamento (DM seguros)
- espaço de trabalho bootstrap + competências
- serviço de fundo opcional

Se você quiser as páginas de referência mais profundas, pule para: [Wizard](<<<LINK0>>>), [Setup](<<LINK1>>>), [Pairing](<<LINK2>>>), [Security](<<LINK3>>>).

Nota de boxe de areia: <<CODE0>> usa <<CODE1>> (padrão <<CODE2>>),
então as sessões de grupo/canal são sandbox. Se você quer que o agente principal sempre
executar na máquina, definir uma sobreposição explícita por agente:

```json
{
  "routing": {
    "agents": {
      "main": {
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" }
      }
    }
  }
}
```

# # 0) Pré-requisitos

- Nó < < HTML0>>>
- <<CODE1>> (opcional; recomendado se você compilar a partir da fonte)
- ** Recomendado:** Chave de API de pesquisa corajosa para pesquisa web. Caminho mais fácil:
<<CODE2>> (armazena <<CODE3>>>).
Ver [Ferramentas Web] (<<<LINK0>>>).

macOS: se você planeja construir os aplicativos, instale Xcode / CLT. Para o portal CLI + apenas, Node é suficiente.
Windows: use **WSL2** (Ubuntu recomendado). WSL2 é fortemente recomendado; Windows nativo é não testado, mais problemático, e tem pior compatibilidade de ferramenta. Instale o WSL2 primeiro e execute os passos do Linux dentro do WSL. Ver [Windows (WSL2)](<<<LINK0>>>).

# # 1) Instalar o CLI (recomendado)

```bash
curl -fsSL https://openclaw.bot/install.sh | bash
```

Opções do instalador (método de instalação, não-interativo, do GitHub): [Instalar](<<LINK0>>>).

Janelas (Powershell):

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

Alternativa (instalação global):

```bash
npm install -g openclaw@latest
```

```bash
pnpm add -g openclaw@latest
```

# # 2) Execute o assistente de onboarding (e instale o serviço)

```bash
openclaw onboard --install-daemon
```

O que você vai escolher:

- ** Local vs Remoto** gateway
- ** Auth**: OpenAI Code (Codex) subscription (OAuth) ou API. Para Anthropic recomendamos uma chave API; <<CODE0>> também é suportado.
- **Fornecedores**: login do WhatsApp QR, tokens de bot Telegram/Discord, tokens de plugin Mattermost, etc.
- ** Daemon**: instalação de fundo (lançado/sistemad; WSL2 usa systemd)
- **Runtime**: Node (recomendado; exigido para WhatsApp/Telegram). Bun é ** não recomendado**.
- ** Token Gateway**: o assistente gera um por padrão (mesmo em loopback) e o armazena em <<CODE1>.

Documento do assistente: [Wizard] (<<<LINK0>>)

# # # Auth: onde vive (importante)

- ** Caminho Antrópico Recomendado:** definir uma chave API (o Wizard pode armazená-la para uso de serviço). <<CODE0> também é suportado se você quiser reutilizar credenciais do Claude Code.

- Credenciais OAuth (importação de legado): <<CODE0>>
- Perfis de autenticação (chaves OAuth + API): <<CODE1>>

Ponta sem cabeça/servidor: faça OAuth em uma máquina normal primeiro, depois copie <<CODE0>> para o host gateway.

# # 3) Iniciar o portal

Se você instalou o serviço durante o embarque, o Gateway já deve estar rodando:

```bash
openclaw gateway status
```

Execução manual (foreground):

```bash
openclaw gateway --port 18789 --verbose
```

Painel (loopback local): <<CODE0>>
Se um token estiver configurado, cole-o na configuração Control UI (armazenado como <<CODE1>>>).

Aviso de explosão (WhatsApp + Telegram):** Bun tem problemas conhecidos com estes
canais. Se você usar o WhatsApp ou Telegram, execute o Gateway com **Node**.

## 3.5) Verificação rápida (2 min)

```bash
openclaw status
openclaw health
openclaw security audit --deep
```

# # 4) Par + conectar sua primeira superfície de bate-papo

## # WhatsApp (Login QR)

```bash
openclaw channels login
```

Digitalize através do WhatsApp → Configurações → Dispositivos vinculados.

Documento do WhatsApp: [WhatsApp] (<<<LINK0>>)

# # # Telegrama / Discórdia / outros

O assistente pode escrever tokens/config para você. Se preferir configuração manual, comece com:

- Telegrama: [Telegrama] (<<<LINK0>>)
- Discórdia: [Discord] (<<<LINK1>>>)
- Mattermost: [Mattermost] (<<<LINK2>>>)

** Dica DM do Telegrama:** seu primeiro DM retorna um código de pareamento. Aprovar (veja o próximo passo) ou o bot não responderá.

5) Segurança do DM (aprovações parentais)

Postura padrão: DMs desconhecidos recebem um código curto e as mensagens não são processadas até serem aprovadas.
Se o seu primeiro DM não receber resposta, aprove o emparelhamento:

```bash
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <code>
```

Documento de pareamento: [Pairing] (<<<LINK0>>>)

# # Da fonte (desenvolvimento)

Se você estiver hackeando o próprio OpenClaw, corra a partir da fonte:

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build # auto-installs UI deps on first run
pnpm build
openclaw onboard --install-daemon
```

Se você ainda não tiver uma instalação global, execute o passo de integração via <<CODE0>> do repo.
<<CODE1> também agrupa ativos A2UI; se você precisar executar apenas esse passo, use <<CODE2>>.

Gateway (a partir deste acordo):

```bash
node openclaw.mjs gateway --port 18789 --verbose
```

## 7) Verificar de ponta a ponta

Em um novo terminal, envie uma mensagem de teste:

```bash
openclaw message send --target +15555550123 --message "Hello from OpenClaw"
```

Se <<CODE0> mostrar “no auth configured”, volte para o assistente e defina OAuth/key auth – o agente não será capaz de responder sem ele.

Dica: <<CODE0>> é o melhor relatório de depuração somente para leitura.
Sondas de saúde: <<CODE1>> (ou <<CODE2>>>) pergunta a porta de entrada para um instantâneo de saúde.

# # Próximos passos (opcional, mas ótimo)

- app da barra de menus do macOS + voice wake: [macOS app] (<<<LINK0>>>)
- nós iOS/Android (Canvas/câmera/voz): [Nos](<<<LINK1>>>)
- Acesso remoto (tunel SH / Tailscale Serve): [Acesso remoto] (<<<LINK2>>>) e [Tailscale] (<<LINK3>>)
- Configuração sempre ligada / VPN: [Acesso remoto] (<<<<LINK4>>>), [exe.dev](<<LINK5>>), [Hetzner] (<<LINK6>>>), [macOS remoto](<<LINK7>>)
