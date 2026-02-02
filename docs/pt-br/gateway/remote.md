---
summary: "Remote access using SSH tunnels (Gateway WS) and tailnets"
read_when:
  - Running or troubleshooting remote gateway setups
---

# Acesso remoto (SSH, túneis e tailnets)

Este repo suporta “remote over SSH” mantendo um único Gateway (o mestre) rodando em um host dedicado (desktop/servidor) e conectando clientes a ele.

- Para **operadores (você / o aplicativo macOS)**: O túnel SSH é o retorno universal.
- Para **nodes (iOS/Android e futuros dispositivos)**: conecte-se ao Gateway **WebSocket** (LAN/tailnet ou túnel SSH, conforme necessário).

# # A ideia central

- O Gateway WebSocket liga-se a **loopback** na sua porta configurada (padrão para 18789).
- Para uso remoto, você encaminha essa porta loopback sobre SSH (ou usa uma tailnet/VPN e túnel menos).

# # Configuração comum de VPN/tailnet (onde o agente vive)

Pense no anfitrião **Gateway** como “onde o agente vive”. Possui sessões, perfis de autenticação, canais e estado.
Seu laptop/desktop (e nós) se conectam a essa máquina.

###1) Sempre no Gateway na sua tailnet (VPS ou servidor doméstico)

Execute o Gateway em um host persistente e alcance-o através de **Tailscale** ou SSH.

- **Melhor UX:** manter <<CODE0>> e usar **Tailscale Serve** para a UI Controle.
- **Fallback:** manter loopback + túnel SSH de qualquer máquina que precise de acesso.
- **Exemplos:** [exe.dev](<<LINK0>>>) (VM fácil) ou [Hetzner](<<LINK1>>) (produção VPS).

Isto é ideal quando seu laptop dorme muitas vezes, mas você quer o agente sempre ligado.

# # # 2) Home desktop executa o Gateway, laptop é controle remoto

O laptop não roda o agente. Liga-se remotamente:

- Use o app do macOS **Remote sobre o modo SSH** (Configurações → Geral → “OpenClaw corre”).
- O aplicativo abre e gerencia o túnel, por isso WebChat + verificações de saúde "apenas trabalhar".

Runbook: [acesso remoto macOS](<<<LINK0>>>).

# # # 3) Laptop executa o Gateway, acesso remoto de outras máquinas

Mantenha o portal local mas exponha-o em segurança.

- túnel SSH para o portátil a partir de outras máquinas, ou
- Tailscale Servir a interface de controle e manter o Gateway loopback-somente.

Guia: [Tailscale] (<<<LINK0>>) e [Web overview] (<<LINK1>>>).

# # Fluxo de comando (o que corre onde)

Um serviço de gateway possui canais state +. Os nós são periféricos.

Exemplo de fluxo (telegrama → nó):

- A mensagem do telegrama chega ao **Gateway**.
- Gateway executa o **agent** e decide se chama uma ferramenta de nó.
- Gateway chama o **node** sobre o Gateway WebSocket (<<<CODE0>RPC).
- Node retorna o resultado; Gateway responde novamente ao Telegram.

Notas:

- ** Nós não executam o serviço de gateway.** Apenas um gateway deve ser executado por host, a menos que você execute perfis isolados intencionalmente (veja [Gateways múltiplos](<<LINK0>>)).
- app macOS "modo nó" é apenas um cliente de nó sobre o Gateway WebSocket.

# # Túnel SSH (CLI + ferramentas)

Crie um túnel local para o remoto Gateway WS:

```bash
ssh -N -L 18789:127.0.0.1:18789 user@host
```

Com o túnel para cima:

- <<CODE0>> e <<CODE1>> agora chegam ao portal remoto via <<CODE2>>.
- <<CODE3> também pode direcionar o URL encaminhado via <<CODE4> quando necessário.

Nota: substituir <<CODE0>> por seu configurado <<CODE1>>> (ou <<CODE2>/<HTML3>>>>).

# # CLI por omissão remota

Você pode persistir um alvo remoto para que os comandos CLI o usem por padrão:

```json5
{
  gateway: {
    mode: "remote",
    remote: {
      url: "ws://127.0.0.1:18789",
      token: "your-token",
    },
  },
}
```

Quando o gateway for somente loopback, mantenha a URL em <<CODE0>> e abra o túnel SSH primeiro.

# # Conversar com UI sobre SSH

O WebChat já não usa uma porta HTTP separada. O chat UI SwiftUI conecta diretamente ao Gateway WebSocket.

- Avançar <<CODE0>> sobre o SSH (ver acima), em seguida, ligar os clientes a <<CODE1>>>.
- No macOS, prefira o modo “Remote over SSH” do aplicativo, que gerencia o túnel automaticamente.

# # app macOS “Remote over SSH”

O aplicativo da barra de menus do macOS pode conduzir a mesma configuração de ponta a ponta (cheques de status remotos, WebChat e roading Voice Wake).

Runbook: [acesso remoto macOS](<<<LINK0>>>).

# # Regras de segurança (remote/VPN)

Versão curta: **mantenha o Gateway loopback-only** a menos que tenha certeza de que precisa de um link.

- ** Loopback + SSH/Tailscale Serve** é o padrão mais seguro (sem exposição pública).
- ** Não- loopback liga- se** (<<<CODE0>/<HTML1>>>/<<CODE2>>, ou <<CODE3> quando o loopback não está disponível) deve utilizar tokens/senhas de autenticação.
- <<CODE4> é **somente** para chamadas CLI remotas – não ** habilita a autenticação local.
- <<CODE5> prende o certificado remoto de SLT quando utiliza <<CODE6>>.
- **Tailscale Serve** pode autenticar através de cabeçalhos de identidade quando <<CODE7>>.
Configure-o em <<CODE8>> se quiser tokens/senhas.
- Tratar o controle do navegador como acesso ao operador: tailnet-only + emparelhamento de nó deliberado.

Mergulho profundo: [Segurança] (<<<LINK0>>>).
