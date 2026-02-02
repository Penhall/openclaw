---
summary: "Top-level overview of OpenClaw, features, and purpose"
read_when:
  - Introducing OpenClaw to newcomers
---

Open Claw

>  "EXFOLIAR! EXFOLIAR!"  — Uma lagosta espacial, provavelmente

<p align="center">
    <img
        src="/assets/openclaw-logo-text-dark.png"
        alt="OpenClaw"
        width="500"
        class="dark:hidden"
    />
    <img
        src="/assets/openclaw-logo-text.png"
        alt="OpenClaw"
        width="500"
        class="hidden dark:block"
    />
</p>

<p align="center">
<strong>Qualquer sistema operacional + WhatsApp/Telegram/Discord/iMessage gateway para agentes de IA (Pi).<</strong><<br />
Plugins adicionar Mattermost e muito mais.
Envie uma mensagem, obtenha uma resposta do agente — do seu bolso.
</p>

<p align="center">
  <a href="https://github.com/openclaw/openclaw">GitHub</a> ·
  <a href="https://github.com/openclaw/openclaw/releases">Releases</a> ·
  <a href="/">Docs</a> ·
<a href="/start/openclaw">OpenClaw assistente de configuração<</a>
</p>

OpenClaw liga WhatsApp (via WhatsApp Web / Baileys), Telegram (Bot API / grammY), Discord (Bot API / canales.discord.js), e iMessage (imsg CLI) a agentes de codificação como [Pi](<<LINK0>>). Plugins adicionar Mattermost (Bot API + WebSocket) e muito mais.
Openclaw também é o poder do assistente Openclaw.

# # Começa aqui

- ** Nova instalação a partir de zero:** [Começar] (<<<LINK0>>>)
- ** Configuração guiada (recomendada):** [Wizard] (<<<<LINK1>>>) (<<CODE0>>)
- ** Abra o painel de bordo (local Gateway):** http://127.0.0.1:18789/ (ou http://localhost:18789/)

Se o Gateway estiver rodando no mesmo computador, esse link abre a interface de controle do navegador
imediatamente. Se falhar, inicie o Gateway primeiro: <<CODE0>>>.

# # Painel (UI de Controlo de Navegadores)

O painel é o navegador Controlar UI para chat, configuração, nós, sessões e muito mais.
Padrão local: http://127.0.0.1:18789/
Acesso remoto: [Superfícies Web] (<<<LINK0>>) e [Escala de Tails (<<LINK1>>)

<p align="center">
<img src="whatsapp-openclaw.jpg" alt="OpenClaw" width="420" />
</p>

# # Como funciona

```
WhatsApp / Telegram / Discord / iMessage (+ plugins)
        │
        ▼
  ┌───────────────────────────┐
  │          Gateway          │  ws://127.0.0.1:18789 (loopback-only)
  │     (single source)       │
  │                           │  http://<gateway-host>:18793
  │                           │    /__openclaw__/canvas/ (Canvas host)
  └───────────┬───────────────┘
              │
              ├─ Pi agent (RPC)
              ├─ CLI (openclaw …)
              ├─ Chat UI (SwiftUI)
              ├─ macOS app (OpenClaw.app)
              ├─ iOS node via Gateway WS + pairing
              └─ Android node via Gateway WS + pairing
```

A maioria das operações fluem através do **Gateway** (<<<CODE0>>), um único processo de longa duração que possui conexões de canal e o plano de controle WebSocket.

# # Modelo de rede

- **One Gateway por host (recomendado)**: é o único processo autorizado para possuir a sessão Web WhatsApp. Se você precisar de um bot de resgate ou isolamento restrito, execute vários gateways com perfis e portas isoladas; veja [Gateways múltiplos](<<<LINK0>>).
- **Loopback-first**: Gateway WS defaults to <<CODE0>.
- O assistente agora gera um token de gateway por padrão (mesmo para loopback).
- Para acesso à Tailnet, execute <<CODE1>> (o token é necessário para ligações não- loopback).
- **Nodes**: conecte-se ao Gateway WebSocket (LAN/tailnet/SSH conforme necessário); a ponte TCP legada é desactualizada/removida.
- **Host Canvas**: servidor de arquivos HTTP em <<CODE2>> (default <<CODE3>>), servindo <<CODE4>> para o nó WebViews; veja [Configuração do portal](<<LINK1>>>) (<<CODE5>>>).
- ** Uso remoto**: Túnel SSH ou tailnet/VPN; ver [Acesso remoto] (<<<LINK2>>>) e [Discovery] (<<LINK3>>>).

# # Características (alto nível)

- ** Integração WhatsApp** — Usa Baileys para o protocolo WhatsApp Web
- ** **Telegram Bot** - DM + grupos via GrammY
- **Discord Bot** - DM + guild canais via canal.discord.js
- ** Bot Matermost (plugin)** — Token Bot + Eventos WebSocket
— Integração CLI (macOS)
- **Agent bridge** — Pi (modo RPC) com transmissão de ferramentas
- "Streaming + blocking** - "Block streaming + Telegram rascunho de detalhes de streaming" ([/conceitos/streaming] (<<<LINK0>>)
- **Roteamento de agentes múltiplos** — Contas/parceiros de fornecedores de rotas para agentes isolados (espaço de trabalho + sessões por agente)
- **Assinatura da autorização** — Antrópico (Claude Pro/Max) + OpenAI (ChatGPT/Codex) via OAuth
Sessões** — Conversas directas colapsam em partilha <<CODE0>> (padrão); grupos são isolados
- **Group Chat Support** — Mention-based by default; o proprietário pode alternar <<CODE1>
- Suporte à mídia** — Envie e receba imagens, áudio, documentos
- Notas de voz** — Gancho de transcrição opcional
- **WebChat + app macOS** — Acompanhante local da barra de menus UI + para ops e voz wake
- ** nó iOS** — Emparelha como um nó e expõe uma superfície de tela
- **Node Android** — Pares como um nó e expõe Canvas + Chat + Câmera

Nota: caminhos legados de Claude/Codex/Gemini/Opencode foram removidos; Pi é o único caminho código-agente.

# # Começo rápido

Requisitos de tempo de execução: **Node ≥ 22**.

```bash
# Recommended: global install (npm/pnpm)
npm install -g openclaw@latest
# or: pnpm add -g openclaw@latest

# Onboard + install the service (launchd/systemd user service)
openclaw onboard --install-daemon

# Pair WhatsApp Web (shows QR)
openclaw channels login

# Gateway runs via the service after onboarding; manual run is still possible:
openclaw gateway --port 18789
```

Mudar entre npm e git instala mais tarde é fácil: instale o outro sabor e execute <<CODE0>> para atualizar o ponto de entrada do serviço de gateway.

Fonte (desenvolvimento):

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build # auto-installs UI deps on first run
pnpm build
openclaw onboard --install-daemon
```

Se você ainda não tiver uma instalação global, execute o passo de integração via <<CODE0>> do repo.

Arranque rápido multi- instance (opcional):

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/a.json \
OPENCLAW_STATE_DIR=~/.openclaw-a \
openclaw gateway --port 19001
```

Enviar uma mensagem de teste (requer um Gateway em execução):

```bash
openclaw message send --target +15555550123 --message "Hello from OpenClaw"
```

# # Configuração (opcional)

A configuração vive em <<CODE0>>>>.

- Se você **não fizer nada**, OpenClaw usa o binário Pi empacotado no modo RPC com sessões por entrega.
- Se você quiser bloqueá-lo, comece com regras de menção <<CODE0>> e (para grupos).

Exemplo:

```json5
{
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
  messages: { groupChat: { mentionPatterns: ["@openclaw"] } },
}
```

# # Docs

- Começa aqui.
- [Duss hubs (todas as páginas ligadas)] (<<<LINK0>>>)
- [Ajuda] (<<<LINK1>>) ←  correções comuns + solução de problemas 
- [Configuração](<<<LINK2>>>)
- [Exemplos de configuração](<<<LINK3>>>)
- [Comandos de linha] (<<<LINK4>>>)
- [Roteamento multiagente] (<<<LINK5>>)
- [Atualização/retrocesso] (<<<<LINK6>>>)
- [Pairing (DM + nós)] (<<<LINK7>>>)
- [Modo Nix] (<<<LINK8>>>)
- [Configuração do assistente OpenClaw] (<<<LINK9>>>)
- [Habilidades] (<<<LINK10>>>)
- [Skills config] (<<<LINK11>>>)
- [Templates do espaço de trabalho] (<<<LINK12>>)
- [Adaptadores RPC] (<<<<LINK13>>>)
- [Corredor de portas] (<<<LINK14>>>)
- [nós (iOS/Android)] (<<<LINK15>>>)
- [Superfícies Web (IU de controlo)](<<<LINK16>>>)
- [Discovery + transportes](<<<LINK17>>>)
- [Acesso remoto](<<<LINK18>>>)
- Fornecedores e UX:
- [WebChat] (<<<LINK19>>>)
- [IU de controlo (browser)](<<<LINK20>>)
- [Telegrama] (<<<LINK21>>>)
- [Discórdia] (<<<LINK22>>)
- [Mattermost (plugin)] (<<<LINK23>>)
- [iMessage] (<<<LINK24>>>)
- [Grupos] (<<<LINK25>>)
- [Mensagens de grupo WhatsApp] (<<<LINK26>>)
- [Mídia: imagens] (<<<LINK27>>)
- [Mídia: áudio] (<<<LINK28>>>)
- Aplicações de acompanhantes:
- [aplicativo macOS] (<<<LINK29>>>)
- [aplicativo iOS] (<<<LINK30>>>)
- [Aplicativo Android] (<<<LINK31>>>)
- [Windows (WSL2)] (<<<LINK32>>)
- [Aplicativo Linux] (<<<LINK33>>)
- Operações e segurança:
- [Sessões] (<<<LINK34>>)
- [Trabalhos de Cron] (<<<LINK35>>)
- [Anzóis Web] (<<<LINK36>>)
- [Anzóis de Gmail (Pub/Sub)] (<<<LINK37>>)
- [Segurança] (<<<LINK38>>>)
- [Responsão de problemas] (<<<LINK39>>)

# # O nome

** Open Claw = CLAW + TARDIS** - porque cada lagosta espacial precisa de uma máquina de tempo e espaço.

---

"Estamos todos apenas brincando com nossos próprios prompts."  — uma IA, provavelmente alta em fichas

# # Créditos

- ** Peter Steinberger** ([@ steipete] (<<<LINK0>>)] — Criador, encantador de lagostas
- **Mario Zechner** ([@badlogicc](<<LINK1>>)) Pi criador, segurança pen-tester
- ** Clawd** - A lagosta espacial que exigiu um nome melhor

# # Contribuidores Principais

- **Maxim Vovshin** (@Hyaxia, 36747317+Hyaxia@users.noreply.github.com) — Habilidades do observador de blog
- **Nacho Iacovino** (@nachoiacovino, nacho.iacovino@gmail.com) — Análise de localização (Telegram + WhatsApp)

# # Licença

MIT — Livre como lagosta no oceano

---

Estamos todos a brincar com as nossas próprias instruções. Uma IA, provavelmente alta em fichas
