---
summary: "Network hub: gateway surfaces, pairing, discovery, and security"
read_when:
  - You need the network architecture + security overview
  - You are debugging local vs tailnet access or pairing
  - You want the canonical list of networking docs
---

# Hub de rede

Este hub conecta os documentos do núcleo para como OpenClaw conecta, pares e protege
dispositivos através localhost, LAN e tailnet.

# # Modelo principal

- [Arquitectura do portal] (<<<LINK0>>)
- [Protocolo Gateway] (<<<<LINK1>>>)
- [O livro de instruções do portal] (<<<LINK2>>>)
- [Superfícies Web + modos de ligação] (<<<LINK3>>>)

# # Emparelhamento + identidade

- [Pairing overview (DM + nós)] (<<<LINK0>>>)
- [Emparelhamento de nó de propriedade de Gateway] (<<<LINK1>>)
- [Dispositivos CLI (parelhagem + rotação de fichas)] (<<<LINK2>>>>)
- [As homologações DM](<<<LINK3>>>)

Confiança local:

- As conexões locais (loopback ou endereço tailnet do próprio host do gateway) podem ser
auto-aprovado para emparelhamento para manter o mesmo-host UX suave.
- Clientes não-local tailnet / LAN ainda exigem aprovação emparelhada explícita.

# # Descoberta + transportes

- [Discovery & transports] (<<<LINK0>>>)
- [Bonjour / mDNS] (<<<LINK1>>>)
- [Acesso remoto (SSH)] (<<<LINK2>>>)
- [Tailscale] (<<<LINK3>>>)

# # Nós + transportes

- [Nos visão geral] (<<<<LINK0>>>)
- [Protocolo de ponte (nós legados)] (<<<LINK1>>>)
- [Runbook do nó: iOS] (<<<LINK2>>>)
- [Runbook: Android] (<<<LINK3>>>)

# # Segurança

- [Observação da segurança] (<<<<LINK0>>>)
- [Referência de configuração do portal] (<<<LINK1>>>)
- [Responsão de problemas] (<<<LINK2>>>)
- [Doctor] (<<<LINK3>>>)
