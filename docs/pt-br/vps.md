---
summary: "VPS hosting hub for OpenClaw (Oracle/Fly/Hetzner/GCP/exe.dev)"
read_when:
  - You want to run the Gateway in the cloud
  - You need a quick map of VPS/hosting guides
---

# Hospedagem VPS

Este hub liga-se aos guias VPS/hosting suportados e explica como a nuvem
As deslocações funcionam a um nível elevado.

# # Escolha um provedor

- **Railway** (um clique + configuração do navegador): [Railway] (<<<LINK0>>>)
- **Northflank** (um clique + configuração do navegador): [Northflank] (<<<LINK1>>)
- ** Nuvem de Oracle (Sempre Livre)**: [Oráculo] (<<<LINK2>>>) $0/mês (Sempre Livre, ARM; capacidade / assinatura pode ser finicky)
- **Fly.io**: [Fly.io](<<LINK3>>)
- ** Hetzner (Docker)**: [Hetzner] (<<<LINK4>>>)
- ** GCP (motor de computação)**: [GCP] (<<<LINK5>>>)
- **exe.dev** (proxy VM + HTTPS): [exe.dev](<<LINK6>>)
- **AWS (EC2/Lightsail/free layer)**: também funciona bem. Guia de vídeo:
https://x.com/techfrenAJ/status/2014934471095812547

# # Como as configurações de nuvem funcionam

- O **Gateway roda no VPS** e possui estado + espaço de trabalho.
- Você se conecta do seu laptop/telefone através da **Control UI** ou **Tailscale/SSH**.
- Tratar o VPS como a fonte da verdade e ** fazer backup** o estado + espaço de trabalho.
- Predefinição segura: manter o Gateway em loopback e acessá-lo através do túnel SSH ou Tailscale Serve.
Se se ligar a <<CODE0>/<<CODE1>>>>, necessita de <<CODE2>>> ou <<CODE3>>>.

Acesso remoto: [Relatório remoto do portal](<<<LINK0>>)
hub das plataformas: [Plataformas](<<<LINK1>>)

# # Usando nós com um VPS

Você pode manter o Gateway na nuvem e par ** nós** em seus dispositivos locais
(Mac/iOS/Android/headless). Os nós fornecem tela local/câmera/canvas e <<CODE0>>
Capacidades enquanto o Portal fica na nuvem.

Docs: [Nos] (<<<LINK0>>), [Nodes CLI] (<<LINK1>>)
