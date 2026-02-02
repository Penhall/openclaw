---
summary: "Node discovery and transports (Bonjour, Tailscale, SSH) for finding the gateway"
read_when:
  - Implementing or changing Bonjour discovery/advertising
  - Adjusting remote connection modes (direct vs SSH)
  - Designing node discovery + pairing for remote nodes
---

# Descoberta e transportes

Openclaw tem dois problemas distintos que parecem similares na superfície:

1. **Controle remoto do operador**: o aplicativo da barra de menu do macOS controlando um gateway rodando em outro lugar.
2. ** Emparelhamento de nós**: iOS/Android (e futuros nós) encontrando um gateway e emparelhamento com segurança.

O objetivo do projeto é manter toda a descoberta/publicidade de rede no **Node Gateway** (<<CODE0>>>) e manter os clientes (mac app, iOS) como consumidores.

# # Termos

- **Gateway**: um único processo de gateway de longa duração que possui estado (sessões, emparelhamento, registro de nó) e executa canais. A maioria das configurações usa uma por host; configurações de portas múltiplas isoladas são possíveis.
- **Gateway WS (plano de controlo)**: o ponto final WebSocket em <<CODE0>> por omissão; pode ser ligado à LAN/tailnet via <<CODE1>>>.
- ** Transporte WS direto**: um ponto final do Gateway WS virado para LAN/tailnet (sem SSH).
- ** Transporte de SHS (fallback)**: controle remoto por encaminhamento <<CODE2>> sobre SSH.
- **Legacy TCP bridge (depreciada/removida)**: transporte de nó antigo (ver [Protocolo de ponte](<<LINK0>>)); não mais anunciado para descoberta.

Detalhes do protocolo:

- [Protocolo Gateway] (<<<LINK0>>>)
- [Protocolo de ponte (legacia)](<<<LINK1>>)

# # Por que mantemos ambos “direto” e SSH

- ** Direct WS** é o melhor UX na mesma rede e dentro de uma tailnet:
- auto-descoberta na LAN via Bonjour
- tokens de emparelhamento + ACLs pertencentes ao gateway
- nenhum acesso de shell necessário; superfície do protocolo pode ficar apertado e auditável
- **SSH** continua a ser o retorno universal:
- funciona em qualquer lugar que você tenha acesso SSH (mesmo em redes não relacionadas)
- sobrevive a questões multicast/mDNS
- não requer novas portas de entrada para além de SSH

# # Entradas de descoberta (como os clientes aprendem onde o gateway está)

# # # 1) Bonjour / mDNS (apenas LAN)

Bonjour é o melhor esforço e não atravessa redes. Ele é usado apenas para “mesma LAN” conveniência.

Direcção do alvo:

- O **gateway** anuncia seu ponto final WS via Bonjour.
- Os clientes navegam e mostram uma lista de “escolha um gateway” e armazenam o endpoint escolhido.

Resolução de problemas e detalhes do farol: [Bonjour] (<<<LINK0>>>).

Detalhes do farol de serviço

- Tipos de serviços:
- <<CODE0> (farol de transporte por vias navegáveis)
- Teclas TXT (não secretas):
- <<CODE1>>
- <<CODE2>>
- <<CODE3> (ou seja o que for anunciado)
- <<CODE4>> (Gateway WS + HTTP)
- <<CODE5>> (somente quando o TLS está activo)
- <<CODE6>> (apenas quando o TLS estiver activo e a impressão digital estiver disponível)
- <<CODE7>> (porta de máquina de tela padrão; serve <<CODE8>>>)
- <<CODE9>> (opcional; caminho absoluto para um ponto de entrada executável <<CODE10>>> ou binário)
- <<CODE11> (dica opcional; detectada automaticamente quando a escala de cauda está disponível)

Desactivar/substituir:

- <<CODE0>> desactiva a publicidade.
- <<CODE1> em <<CODE2> controla o modo de ligação Gateway.
- <<CODE3> substitui a porta SSH anunciada em TXT (padrão para 22).
- <<CODE4> publica uma dica <<CODE5>> (MagicDNS).
- <<CODE6> substitui o caminho CLI anunciado.

## # 2) Tailnet (rede cruzada)

Para configurações estilo Londres/Viena, Bonjour não vai ajudar. O objectivo “directo” recomendado é:

- Tailscale MagicDNS nome (preferido) ou um IP tailnet estável.

Se o gateway pode detectá-lo está rodando em Tailscale, ele publica <<CODE0>> como uma dica opcional para clientes (incluindo beacons de ampla área).

## # 3) Manual / alvo SSH

Quando não há rota direta (ou direta está desabilitada), os clientes podem sempre se conectar via SSH encaminhando a porta de gateway loopback.

Ver [Acesso remoto] (<<<LINK0>>>).

# # Seleção de transportes (política de cliente)

Comportamento recomendado do cliente:

1. Se um endpoint direto emparelhado for configurado e alcançável, use-o.
2. Caso contrário, se Bonjour encontrar um gateway na LAN, ofereça uma opção de “Use este gateway” de uma só vez e salve-o como o endpoint direto.
3. Caso contrário, se um DNS/IP tailnet estiver configurado, tente diretamente.
4. Senão, volte para SSH.

# # Emparelhamento + autenticação (transporte direto)

O gateway é a fonte de verdade para admissão de nó/cliente.

- Os pedidos de pareamento são criados/aprovados/rejeitados no gateway (ver [Gateway pareamento] (<<<LINK0>>)).
- O portal obriga:
- autenticação (token / keypair)
- escopos/ACLs (o gateway não é um proxy bruto para todos os métodos)
- limites de taxa

# # Responsabilidades por componente

- **Gateway**: anuncia balizas de descoberta, possui decisões de emparelhamento e hospeda o endpoint WS.
- **macOS app**: ajuda você a escolher um gateway, mostra prompts de emparelhamento e usa SSH apenas como backback.
- **iOS/Android nós**: navegar Bonjour como uma conveniência e se conectar ao Gateway WS emparelhado.
