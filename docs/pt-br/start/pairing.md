---
summary: "Pairing overview: approve who can DM you + which nodes can join"
read_when:
  - Setting up DM access control
  - Pairing a new iOS/Android node
  - Reviewing OpenClaw security posture
---

Emparelhamento

“Pairing” é a aprovação explícita da OpenClaw**.
É utilizado em dois locais:

1. ** Emparelhamento DM** (que é permitido falar com o bot)
2. ** Emparelhamento de nós** (que dispositivos / nós são autorizados a entrar na rede gateway)

Contexto de segurança: [Segurança](<<<LINK0>>)

## 1) Emparelhamento de DM (acesso de chat de entrada)

Quando um canal é configurado com a política de DM <<CODE0>>, os remetentes desconhecidos recebem um código curto e sua mensagem é **não processada** até que você aprove.

Políticas padrão de DM estão documentadas em: [Segurança](<<<LINK0>>)

Códigos de pareamento:

- 8 caracteres, maiúsculas, sem caracteres ambíguos (<<CODE0>>>).
- ** Expirar após 1 hora**. O bot só envia a mensagem de pareamento quando uma nova solicitação é criada (aproximadamente uma vez por hora por remetente).
- Os pedidos de emparelhamento DM pendentes são limitados em **3 por canal** por padrão; os pedidos adicionais são ignorados até que um expira ou é aprovado.

Aprovar um remetente

```bash
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

Canais suportados: <<CODE0>>, <<CODE1>, <<CODE2>>, <<CODE3>, <<CODE4>>, <<CODE5>>.

# # Onde o estado vive

Conservado em <<CODE0>>:

- Pedidos pendentes: <<CODE0>>>
- Conservar na lista de autorizações aprovada: <<CODE1>>

Trate-os como sensíveis (eles porta acesso ao seu assistente).

# # 2) Emparelhamento do dispositivo de nós (iOS/Android/macOS/nós sem cabeça)

Os nós se conectam ao Gateway como **dispositivos** com <<CODE0>>. A Porta
cria uma solicitação de emparelhamento do dispositivo que deve ser aprovada.

## # Aprovar um dispositivo de nó

```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
```

# # Onde o estado vive

Conservado em <<CODE0>>:

- <<CODE0>> (vida curta; os pedidos pendentes expiram)
- <<CODE1>> (dispositivos pareados + fichas)

Notas

- O legado <<CODE0>> API (CLI: <<CODE1>>) é um
loja de emparelhamento separada de propriedade de gateway. Os nós WS ainda requerem emparelhamento do dispositivo.

# # Docs relacionados

- Modelo de segurança + injecção rápida: [Segurança] (<<<LINK0>>>)
- Actualização com segurança (médico): [Atualização] (<<<LINK1>>>)
- Configuração do canal:
- Telegrama: [Telegrama] (<<<LINK2>>>)
- WhatsApp: [WhatsApp] (<<<LINK3>>)
- Sinal: [sinal] (<<<LINK4>>>)
- iMessage: [iMessage] (<<<LINK5>>)
- Discórdia: [Discórdia] (<<<LINK6>>>)
- Slack: [Slack] (<<< HTML7>>>>)
