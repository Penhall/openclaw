---
summary: "End-to-end guide for running OpenClaw as a personal assistant with safety cautions"
read_when:
  - Onboarding a new assistant instance
  - Reviewing safety/permission implications
---

Construindo um assistente pessoal com OpenClaw

OpenClaw é um WhatsApp + Telegram + Discord + iMessage gateway para **Pi** agentes. Plug-ins adicionar Mattermost. Este guia é a configuração "assistente pessoal": um número dedicado do WhatsApp que se comporta como seu agente sempre ligado.

## # # Segurança primeiro

Você está colocando um agente em uma posição para:

- execute comandos em sua máquina (dependendo de sua configuração de ferramenta Pi)
- ler/escrever arquivos em seu espaço de trabalho
- envie mensagens de volta através do WhatsApp/Telegram/Discord/Mattermost (plugin)

Iniciar conservador:

- Sempre definir <<CODE0>> (nunca executar open-to-the-world em seu Mac pessoal).
- Use um número WhatsApp dedicado para o assistente.
- Batimentos cardíacos a cada 30 minutos. Desactivar até confiar na configuração, definindo <<CODE1>>>.

# # Pré-requisitos

- Node **22+**
- OpenClaw disponível no PATH (recomendado: instalação global)
- Um segundo número de telefone (SIM/eSIM/pré-pago) para o assistente

```bash
npm install -g openclaw@latest
# or: pnpm add -g openclaw@latest
```

Fonte (desenvolvimento):

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build # auto-installs UI deps on first run
pnpm build
pnpm link --global
```

# # A configuração de dois telefones (recomendado)

Queres isto:

```
Your Phone (personal)          Second Phone (assistant)
┌─────────────────┐           ┌─────────────────┐
│  Your WhatsApp  │  ──────▶  │  Assistant WA   │
│  +1-555-YOU     │  message  │  +1-555-ASSIST  │
└─────────────────┘           └────────┬────────┘
                                       │ linked via QR
                                       ▼
                              ┌─────────────────┐
                              │  Your Mac       │
                              │  (openclaw)      │
                              │    Pi agent     │
                              └─────────────────┘
```

Se você vincular seu WhatsApp pessoal ao OpenClaw, cada mensagem para você se torna “input agente”. Isso raramente é o que você quer.

# # 5 minutos de início rápido

1. Emparelhe WhatsApp Web (mostra QR; digitalize com o telefone assistente):

```bash
openclaw channels login
```

2. Inicie o portal (deixe-o em execução):

```bash
openclaw gateway --port 18789
```

3. Coloque uma configuração mínima em <<CODE0>>:

```json5
{
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

Agora message o número de assistente do seu telefone autorizado.

Quando a integração termina, nós abrimos automaticamente o painel com seu token de gateway e imprimimos o link tokenized. Para reabrir mais tarde: <<CODE0>>>.

# # Dar ao agente um espaço de trabalho (AGENTES)

OpenClaw lê instruções de operação e “memória” de seu diretório de espaço de trabalho.

Por padrão, OpenClaw usa <<CODE0>> como o espaço de trabalho do agente, e irá criá-lo (mais starter <<CODE1>>, <<CODE2>>, <<CODE3>>, <<CODE4>>, <<CODE5>>>) automaticamente na configuração/primeira execução do agente. <<CODE6>> só é criado quando o espaço de trabalho é novo (não deve voltar depois de deletá-lo).

Dica: trate esta pasta como a “memória” do OpenClaw e faça dela um git repo (idealmente privado) para que seus arquivos de memória <<CODE0>>+ sejam copiados. Se o git estiver instalado, novos espaços de trabalho são iniciados automaticamente.

```bash
openclaw setup
```

layout completo do espaço de trabalho + guia de backup: [Espaço de trabalho do agente](<<<LINK0>>)
Fluxo de trabalho de memória: [Memory] (<<<LINK1>>)

Opcional: escolher um espaço de trabalho diferente com <<CODE0>> (suporta <<CODE1>>).

```json5
{
  agent: {
    workspace: "~/.openclaw/workspace",
  },
}
```

Se você já enviar seus próprios arquivos de espaço de trabalho de um repo, você pode desativar a criação de arquivos bootstrap inteiramente:

```json5
{
  agent: {
    skipBootstrap: true,
  },
}
```

# # A configuração que a transforma em “um assistente”

O OpenClaw é padrão para uma boa configuração assistente, mas você normalmente vai querer sintonizar:

- persona/instruções em <<CODE0>>
- padrões de pensamento (se desejado)
- batimentos cardíacos (uma vez que confia nele)

Exemplo:

```json5
{
  logging: { level: "info" },
  agent: {
    model: "anthropic/claude-opus-4-5",
    workspace: "~/.openclaw/workspace",
    thinkingDefault: "high",
    timeoutSeconds: 1800,
    // Start with 0; enable later.
    heartbeat: { every: "0m" },
  },
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
      groups: {
        "*": { requireMention: true },
      },
    },
  },
  routing: {
    groupChat: {
      mentionPatterns: ["@openclaw", "openclaw"],
    },
  },
  session: {
    scope: "per-sender",
    resetTriggers: ["/new", "/reset"],
    reset: {
      mode: "daily",
      atHour: 4,
      idleMinutes: 10080,
    },
  },
}
```

# # Sessões e memória

- Arquivos de sessão: <<CODE0>>
- Metadados de sessão (utilização da ficha, última rota, etc.): <<CODE1>> (legacia: <<CODE2>>)
- <<CODE3>> ou <<CODE4> inicia uma nova sessão para esse chat (configurável via <<CODE5>>). Se enviado sozinho, o agente responde com um pequeno olá para confirmar o reset.
- <<CODE6> compacta o contexto da sessão e reporta o restante orçamento do contexto.

# # Batimentos cardíacos (modo pró-activo)

Por padrão, o OpenClaw executa um batimento cardíaco a cada 30 minutos com o prompt:
<<CODE0>>
Definir <<CODE1>> para desativar.

- Se <<CODE0>> existe, mas é efetivamente vazio (apenas linhas em branco e cabeçalhos de marcação como <<CODE1>>), OpenClaw ignora a execução do batimento cardíaco para salvar chamadas API.
- Se faltar o ficheiro, o batimento cardíaco continua a correr e o modelo decide o que fazer.
- Se o agente responder com <<CODE2>>> (opcionalmente com enchimento curto; veja <<CODE3>>), OpenClaw suprime a entrega de saída para esse batimento cardíaco.
- Batimentos cardíacos executar turnos de agente completo - intervalos mais curtos queimar mais fichas.

```json5
{
  agent: {
    heartbeat: { every: "30m" },
  },
}
```

# # Mídia dentro e fora

Anexos de entrada (imagens/áudio/docs) podem ser exibidos ao seu comando através de modelos:

- <<CODE0>> (caminho do ficheiro temporário local)
- <<CODE1> (pseudo-URL)
- <<CODE2>> (se a transcrição de áudio estiver activa)

Anexos de saída do agente: incluir <<CODE0>> em sua própria linha (sem espaços). Exemplo:

```
Here’s the screenshot.
MEDIA:/tmp/screenshot.png
```

OpenClaw extrai estes e os envia como mídia ao lado do texto.

# # Lista de operações

```bash
openclaw status          # local status (creds, sessions, queued events)
openclaw status --all    # full diagnosis (read-only, pasteable)
openclaw status --deep   # adds gateway health probes (Telegram + Discord)
openclaw health --json   # gateway health snapshot (WS)
```

Os logs vivem em <<CODE0>> (padrão: <<CODE1>>).

# # Próximos passos

- WebChat: [WebChat] (<<<LINK0>>)
- Operações do Gateway: (<<<LINK1>>>)
- Acordes Cron +: [Trabalhos Cron] (<<<LINK2>>)
- companheiro da barra de menus do macOS: [App macOS OpenClaw] (<<<LINK3>>)
- Aplicação do nó iOS: [aplicativo iOS](<<<LINK4>>)
- App do nó Android: [App Android] (<<<LINK5>>)
- Estado do Windows: [Windows (WSL2)] (<<<LINK6>>)
- Estado do Linux: [aplicativo Linux](<<<LINK7>>)
- Segurança: [Segurança] (<<<LINK8>>>)
