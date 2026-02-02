---
summary: "Bonjour/mDNS discovery + debugging (Gateway beacons, clients, and common failure modes)"
read_when:
  - Debugging Bonjour discovery issues on macOS/iOS
  - Changing mDNS service types, TXT records, or discovery UX
---

Bonjour / descoberta mDNS

Openclaw usa Bonjour (mDNS / DNS-SD) como uma conveniência **LAN-somente** para descobrir
um Gateway ativo (endpoint WebSocket). É o melhor esforço e não substitui ** SSH ou
Conectividade baseada na cauda.

# # Bonjour de ampla área (DNS-SD Unicast) sobre escala de cauda

Se o nó e gateway estão em diferentes redes, mDNS multicast não vai cruzar o
limite. Você pode manter a mesma descoberta UX, mudando para ** DNS-SD unicast**
("Wide-Area Bonjour") sobre Tailscale.

Passos de alto nível:

1. Execute um servidor DNS no host gateway (alcançável sobre a Tailnet).
2. Publique registros DNS-SD para <<CODE0>> sob uma zona dedicada
(exemplo: <<CODE1>>).
3. Configure Tailscale ** split DNS** para que seu domínio escolhido resolva através disso
Servidor DNS para clientes (incluindo iOS).

OpenClaw suporta qualquer domínio de descoberta; <<CODE0>> é apenas um exemplo.
Os nós iOS/Android navegam tanto por <<CODE1>> quanto por seu domínio de área ampla configurado.

### Configuração do portal (recomendado)

```json5
{
  gateway: { bind: "tailnet" }, // tailnet-only (recommended)
  discovery: { wideArea: { enabled: true } }, // enables wide-area DNS-SD publishing
}
```

### Configuração única do servidor DNS (host de porta)

```bash
openclaw dns setup --apply
```

Isto instala o CoreDNS e configura- o para:

- ouvir na porta 53 apenas nas interfaces Tailscale do gateway
- servir o seu domínio escolhido (exemplo: <<CODE0>>>) de <<CODE1>>

Validar a partir de uma máquina ligada à rede de caudas:

```bash
dns-sd -B _openclaw-gw._tcp openclaw.internal.
dig @<TAILNET_IPV4> -p 53 _openclaw-gw._tcp.openclaw.internal PTR +short
```

Configuração do DNS em escala de cauda

Na consola de administração Tailscale:

- Adicione um servidor de nomes apontando para o IP tailnet do gateway (UDP/TCP 53).
- Adicione DNS dividido para que seu domínio de descoberta use esse servidor de nomes.

Uma vez que os clientes aceitam o DNS tailnet, os nós iOS podem navegar
<<CODE0>> no seu domínio de descoberta sem multicast.

Segurança do ouvinte no portal (recomendado)

A porta Gateway WS (padrão <<CODE0>>) se liga ao loopback por padrão. Para redes de LAN
acessar, vincular explicitamente e manter a autenticação ativada.

Para as configurações de rede de cauda:

- Definir <<CODE0>> em <<CODE1>>.
- Reinicie o Gateway (ou reinicie o app da barra de menus do macOS).

# # O que anuncia

Apenas o Gateway anuncia <<CODE0>>>.

# # Tipos de serviços

- <<CODE0>> — farol de transporte por gateway (utilizado por nós macOS/iOS/Android).

# # Teclas TXT (indicações não secretas)

O Gateway anuncia pequenas dicas não-secretas para tornar os fluxos de UI convenientes:

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>
- <<CODE3>> (Gateway WS + HTTP)
- <<CODE4>> (somente quando o TLS está activo)
- <<CODE5>> (apenas quando o TLS estiver activo e a impressão digital estiver disponível)
- <<CODE6>> (somente quando a máquina de lona estiver habilitada; padrão <<CODE7>>>)
- <<CODE8>> (por omissão até 22 quando não anulado)
- <<CODE9>>
- <<CODE10>> (opcional; caminho absoluto para um ponto de entrada <<CODE11> executável)
- <<CODE12>> (Dica opcional quando a Tailnet estiver disponível)

# # Depuração no macOS

Ferramentas úteis incorporadas:

- Procurar instâncias:
  ```bash
  dns-sd -B _openclaw-gw._tcp local.
  ```
- Resolver uma instância (substituir <<CODE0>>>):
  ```bash
  dns-sd -L "<instance>" _openclaw-gw._tcp local.
  ```

Se a navegação funcionar, mas a resolução falhar, você geralmente está atingindo uma política de LAN ou
Problema de resolução mDNS.

# # Depuração nos diários do portal

O Gateway escreve um ficheiro de registo (impresso na inicialização como
<<CODE0>>). Procurar por <<CODE1>>> linhas, especialmente:

- <<CODE0>>
- <<CODE1>>/ <<CODE2>>
- <<CODE3>>

# # Depuração no nó iOS

O nó iOS usa <<CODE0>> para descobrir <<CODE1>>>.

Para capturar registros:

- Configurações → Gateway → Avançado → **Discovery Debug Logs**
- Configurações → Gateway → Advanced → **Discovery Logs** → reproduz → **Copy**

O log inclui transições de estado do navegador e alterações de configuração de resultados.

# # Modos comuns de falha

- **Bonjour não cruza redes**: use Tailnet ou SSH.
- **Multicast bloqueado**: algumas redes Wi-Fi desactivam mDNS.
- **Dormir / churn de interface**: macOS pode soltar temporariamente resultados mDNS; retry.
- **Browse funciona mas resolver falhas**: manter nomes de máquina simples (evitar emojis ou
pontuação), em seguida, reiniciar o Gateway. O nome da instância de serviço deriva de
o nome do host, então nomes excessivamente complexos podem confundir alguns resolvedores.

# # Nomes de instância escapados (<<<CODE0>>)

Bonjour/DNS-SD muitas vezes escapa de bytes em nomes de instância de serviço como decimal <<CODE0>
sequências (por exemplo, espaços tornam-se <<CODE1>>>>).

- Isto é normal ao nível do protocolo.
- As UI devem ser descodificadas para visualização (usos iOS <<CODE0>>).

# # Desativando / configuração

- <<CODE0>> desactiva a publicidade (legacia: <<CODE1>>).
- <<CODE2> em <<CODE3> controla o modo de ligação Gateway.
- <<CODE4> substitui a porta SSH anunciada no TXT (legacia: <<CODE5>>).
- <<CODE6> publica uma dica MagicDNS em TXT (legacia: <<CODE7>>).
- <<CODE8>> substitui o caminho CLI anunciado (legacia: <<CODE9>>).

# # Docs relacionados

- Política de descoberta e selecção dos transportes: [Discovery] (<<<LINK0>>)
- Emparelhamento de nós + aprovações: [Emparelhamento de gateway](<<<LINK1>>>)
