---
summary: "Gateway-owned node pairing (Option B) for iOS and other remote nodes"
read_when:
  - Implementing node pairing approvals without macOS UI
  - Adding CLI flows for approving remote nodes
  - Extending gateway protocol with node management
---

# Emparelhamento do Gateway (Opção B)

No emparelhamento de Gateway, o **Gateway** é a fonte da verdade para a qual nós
podem participar. UIs (app macOS, futuros clientes) são apenas frontends que
Aprovar ou rejeitar pedidos pendentes.

**Importante:** Os nós WS usam ** par de dispositivos** (papel <<CODE0>>>) durante <<CODE1>>.
<<CODE2> é uma loja de emparelhamento separada e não ** portão o aperto de mão WS.
Apenas clientes que explicitamente chamam <<CODE3>> usam esse fluxo.

# # Conceitos

- **Pedido pendente**: um nó solicitado para participar; requer aprovação.
- ** Nó emparelhado**: nó aprovado com um token de autenticação emitido.
- **Transportes**: o ponto final Gateway WS avança pedidos mas não decide
associação. (O apoio da ponte TCP é desactualizado/removido).

# # Como o emparelhamento funciona

1. Um nó conecta-se ao WS Gateway e solicita emparelhamento.
2. O Gateway armazena uma solicitação ** pendente e emite <<CODE0>>.
3. Você aprova ou rejeita o pedido (CLI ou UI).
4. Na aprovação, o Gateway emite um **novo token** (tokens são girados no re-pair).
5. O nó reconecta usando o token e agora é "pared".

Pedidos pendentes expiram automaticamente após **5 minutos**.

# # Fluxo de trabalho CLI (amigável sem cabeça)

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes reject <requestId>
openclaw nodes status
openclaw nodes rename --node <id|name|ip> --name "Living Room iPad"
```

<<CODE0> mostra nós pareados/conectados e suas capacidades.

# # Superfície API (protocolo de porta)

Eventos:

- <<CODE0>> — emitido quando é criado um novo pedido pendente.
- <<CODE1>> – emitido quando um pedido é aprovado/rejeitado/expirado.

Métodos:

- <<CODE0>> — criar ou reutilizar um pedido pendente.
- <<CODE1>> — lista pendente + nós pareados.
- <<CODE2>> — aprovar um pedido pendente (toque de emissão).
- <<CODE3>> — rejeitar um pedido pendente.
- <<CODE4>> — verificar <<CODE5>>>.

Notas:

- <<CODE0> é idempotente por nó: chamadas repetidas retornam as mesmas
Pedido pendente.
- Aprovação ** sempre gera um novo token; nenhum token é retornado de
<<CODE1>>>.
- Os pedidos podem incluir <<CODE2>> como uma dica para os fluxos de auto-aprovação.

# # Auto-aprovação (macOS app)

O aplicativo macOS pode opcionalmente tentar uma aprovação ** silenciosa ** quando:

- o pedido estiver marcado com <<CODE0>>>, e
- o aplicativo pode verificar uma conexão SSH para o host gateway usando o mesmo usuário.

Se a aprovação silenciosa falhar, ela cai de volta para o prompt “Aproximar/Rejeitar” normal.

# # Armazenamento (local, privado)

O estado de pareamento é armazenado sob o diretório de estado do Gateway (padrão <<CODE0>>):

- <<CODE0>>
- <<CODE1>>

Se você substituir <<CODE0>>, a pasta <<CODE1>> se move com ela.

Notas de segurança:

- Tokens são segredos; trate <<CODE0> como sensíveis.
- Girar um token requer nova aprovação (ou apagar a entrada do nó).

# # Comportamento de transporte

- O transporte é **sem estado**; não armazena a adesão.
- Se o Gateway estiver offline ou o emparelhamento estiver desativado, os nós não podem emparelhar.
- Se o Gateway estiver em modo remoto, o emparelhamento ainda acontece contra a loja remota Gateway.
