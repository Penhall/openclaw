---
summary: "Platform support overview (Gateway + companion apps)"
read_when:
  - Looking for OS support or install paths
  - Deciding where to run the Gateway
---

Plataformas

O núcleo OpenClaw está escrito no TypeScript. **Node é o tempo de execução recomendado**.
Bun não é recomendado para o Gateway (WhatsApp/Telegram bugs).

Existem aplicativos para o macOS (menu bar app) e nós móveis (iOS/Android). Janelas e
Aplicativos companheiros Linux são planejados, mas o Gateway é totalmente suportado hoje.
Aplicativos de companheiro nativos para Windows também são planejados; o Gateway é recomendado via WSL2.

# # Escolha o seu SO

- macOS: [macOS](<<<LINK0>>)
- iOS: [IOS](<<<LINK1>>>)
- Android: [Android](<<<LINK2>>)
- Windows: [Windows] (<<<LINK3>>>)
- Linux: [Linux] (<<<LINK4>>)

# # VPS & hospedagem

- hub VPS: [alojamento VPS] (<<<LINK0>>)
- Fly.io: [Fly.io] (<<<LINK1>>)
- Hetzner (Docker): [Hetzner] (<<<LINK2>>)
- GCP (motor de computação): [GCP] (<<<LINK3>>>)
- exe.dev (proxy VM + HTTPS): [exe.dev](<<LINK4>>>)

# # Ligações comuns

- Guia de instalação: [Começar] (<<<LINK0>>)
- Manual do Gateway: [Gateway] (<<<LINK1>>>)
- Configuração do gateway: [Configuração] (<<<LINK2>>)
- Estado do serviço: <<CODE0>>>

# # Serviço de gateway instalar (CLI)

Utilizar um destes (todos suportados):

- Assistente (recomendado): <<CODE0>>
- Directo: <<CODE1>>
- Configurar fluxo: <<CODE2>> → selecione **Serviço Gateway**
- Reparação/migração: <<CODE3>> (ofertas para instalar ou corrigir o serviço)

O alvo do serviço depende do sistema operacional:

- macOS: LaunchAgent (<<<CODE0> ou <<CODE1>>>; legado <<CODE2>>)
- Linux/WSL2: serviço de usuário systemd (<<<CODE3>>)
