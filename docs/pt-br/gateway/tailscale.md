---
summary: "Integrated Tailscale Serve/Funnel for the Gateway dashboard"
read_when:
  - Exposing the Gateway Control UI outside localhost
  - Automating tailnet or public dashboard access
---

# Tailscale (Painel Gateway)

OpenClaw pode auto-configurar Tailscale **Serve** (tailnet) ou **Funil** (público) para o
Painel Gateway e porta WebSocket. Isto mantém o portal ligado ao loopback enquanto
Tailscale fornece cabeçalhos de identidade HTTPS, roteamento e (para Servir).

# # Modos

- <<CODE0>>: Serve somente com cauda via <<CODE1>>>>. O gateway permanece em <<CODE2>>>.
- <<CODE3>>: HTTPS público via <<CODE4>>>>. OpenClaw requer uma senha compartilhada.
- <<CODE5>>: Padrão (sem automação em escala de cauda).

# # Auth

Definir <<CODE0>> para controlar o aperto de mão:

- <<CODE0>> (padrão quando <<CODE1>> é definido)
- <<CODE2>> (segredo compartilhado via <<CODE3>> ou configuração)

Quando <<CODE0> e <<CODE1>> for <<CODE2>>,
válido Serve proxy requests pode autenticar através de cabeçalhos de identidade Tailscale
(<<<CODE3>>) sem fornecer um token/senha. Verificações OpenClaw
a identidade, resolvendo o <<CODE4>>> endereço através da escala de caudas local
daemon (<<CODE5>>) e combinando-o com o cabeçalho antes de aceitá-lo.
Openclaw só trata um pedido como Servir quando chega de loopback com
Escala de cauda <<CODE6>>, <<CODE7>>>, e <<CODE8>>
Cabeçalhos.
Para exigir credenciais explícitas, definir <<CODE9>>> ou
força <<CODE10>>>.

# # Exemplos de configuração

## # Apenas na tailnet (Servo)

```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "serve" },
  },
}
```

Abrir: <<CODE0>> (ou o seu configurado <<CODE1>>>)

### Apenas para cauda (ligado ao IP para cauda)

Use isto quando quiser que o Gateway ouça diretamente no IP da Tailnet (sem serviço/funil).

```json5
{
  gateway: {
    bind: "tailnet",
    auth: { mode: "token", token: "your-token" },
  },
}
```

Ligar a partir de outro dispositivo Tailnet:

- UI de controlo: <<CODE0>>
- WebSocket: <<CODE1>>

Nota: o loopback (<<CODE0>>) não funcionará neste modo.

## # Internet pública (Funil + senha compartilhada)

```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "funnel" },
    auth: { mode: "password", password: "replace-me" },
  },
}
```

Preferir <<CODE0>> sobre o envio de uma senha para o disco.

# # Exemplos de CLI

```bash
openclaw gateway --tailscale serve
openclaw gateway --tailscale funnel --auth password
```

# # Notas

- O serviço/funil em escala de cauda requer o <<CODE0>> CLI para ser instalado e logado.
- <<CODE1> se recusa a iniciar, a menos que o modo de autenticação seja <<CODE2>> para evitar a exposição pública.
- Definir <<CODE3>> se quiser que o OpenClaw desfaça <<CODE4>>
ou <<CODE5> configuração ao desligar.
- <<CODE6> é uma ligação directa à Tailnet (sem HTTPS, sem Serve/Funil).
- <<CODE7> prefere loopback; use <<CODE8>> se você quiser apenas Tailnet.
- Serve/Funil só expõe a **Controlo da via de entrada UI + WS**. Conectar os nós
o mesmo ponto final do Gateway WS, então Serve pode funcionar para o acesso de nó.

# # Controle do navegador (Portão remoto + navegador local)

Se você executar o Gateway em uma máquina, mas quiser conduzir um navegador em outra máquina,
execute um host **node** na máquina do navegador e mantenha ambos na mesma tailnet.
O Gateway irá proxy de ações do navegador para o nó; nenhum servidor de controle separado ou URL de Servir necessário.

Evite Funnel para controle do navegador; trate o emparelhamento de nós como acesso ao operador.

# # Pré-requisitos de escala de cauda + limites

- Servir requer HTTPS ativado para sua tailnet; o CLI solicita se estiver faltando.
- Servir injecções Cabeçalhos de identidade em escala de cauda; Funil não.
- Funil requer Tailscale v1.38.3+, MagicDNS, HTTPS habilitado e um atributo de nó funil.
- Funil só suporta portas <<CODE0>>, <<CODE1>>>, e <<CODE2>> sobre TLS.
- Funil no macOS requer a variante de app Tailscale de código aberto.

# # Saiba mais

- Tailscale Servir visão geral: https://tailscale.com/kb/1312/serve
- <<CODE0> comando: https://tailscale.com/kb/1242/tailscale-serve
- Visão geral do funnel da escala de cauda: https://tailscale.com/kb/1223/tailscale-funnel
- <<CODE1> comando: https://tailscale.com/kb/1311/tailscale-funnel
