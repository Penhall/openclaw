---
summary: "WebSocket gateway architecture, components, and client flows"
read_when:
  - Working on gateway protocol, clients, or transports
---

Arquitetura do portal

Última actualização: 2026-01-22

## Visão geral

- Uma única longa vida **Gateway** possui todas as superfícies de mensagens (WhatsApp via
Baileys, Telegram via GrammY, Slack, Discord, Signal, iMessage, WebChat).
- Control-plane clientes (macOS app, CLI, web UI, automações) conectar ao
Gateway sobre ** WebSocket** na máquina de ligação configurada (por omissão`127.0.0.1:18789`.
- **Nodes** (macOS/iOS/Android/headless) também se conectam sobre **WebSocket**, mas
declarar`role: node`com tampas/comandos explícitos.
- Um Gateway por host; é o único lugar que abre uma sessão do WhatsApp.
- Um host ** canvas** (padrão`18793` serve HTML e A2UI editáveis por agentes.

## Componentes e fluxos

Portão (daemon)

- Mantém ligações com o fornecedor.
- Expo uma API WS dactilografada (pedidos, respostas, eventos servidor-push).
- Valida quadros de entrada contra o esquema JSON.
- Eventos como`agent`,`chat`,`presence`,`health`,`heartbeat`,`cron`.

## # Clientes (mac app / CLI / web admin)

- Uma ligação WS por cliente.
- Enviar pedidos `health`,`status`,`send`,`agent`,`system-presence`.
- Subscrever os acontecimentos `tick`,`agent`,`presence`,`shutdown`.

## # Nós (macOS / iOS / Android / sem cabeça)

- Conecte-se ao mesmo servidor WS** com`role: node`.
- Fornecer uma identidade do dispositivo em`connect`; o pareamento é **com base no dispositivo** (papel`node` e
A aprovação vive na loja de emparelhamento de dispositivos.
- Expor comandos como`canvas.*`,`camera.*`,`screen.record`,`location.get`.

Detalhes do protocolo:

- [Protocolo Gateway] /gateway/protocol

## WebChat

- UI estática que usa o Gateway WS API para histórico de chat e envia.
- Em configurações remotas, conecta-se através do mesmo túnel SSH/Tailscale como outros
Clientes.

## Ciclo de vida da conexão (cliente único)

```
Client                    Gateway
  |                          |
  |---- req:connect -------->|
  |<------ res (ok) ---------|   (or res error + close)
  |   (payload=hello-ok carries snapshot: presence + health)
  |                          |
  |<------ event:presence ---|
  |<------ event:tick -------|
  |                          |
  |------- req:agent ------->|
  |<------ res:agent --------|   (ack: {runId,status:"accepted"})
  |<------ event:agent ------|   (streaming)
  |<------ res:agent --------|   (final: {runId,status,summary})
  |                          |
```

## Protocolo de arame (síntese)

- Transporte: WebSocket, quadros de texto com cargas JSON.
- Primeiro quadro ** deve ser`connect`.
- Depois do aperto de mão:
- Pedidos:`{type:"req", id, method, params}`→`{type:"res", id, ok, payload|error}`- Eventos:`{type:"event", event, payload, seq?, stateVersion?}`- Se o`OPENCLAW_GATEWAY_TOKEN`(ou o`--token` for estabelecido, o`connect.params.auth.token`deve corresponder ou a tomada fecha.
- Para os métodos de efeitos secundários `send`,`agent`, são necessárias chaves de indemnidade `agent`.
Tente novamente com segurança; o servidor mantém um cache dedupe de curta duração.
- Os nós devem incluir`role: "node"`mais tampas/comandos/permissões em`{type:"req", id, method, params}`0.

## Emparelhamento + confiança local

- Todos os clientes WS (operadores + nós) incluem uma identidade de dispositivo** em`connect`.
- Novos IDs de dispositivos exigem aprovação de emparelhamento; o Gateway emite um sinal de dispositivo **
para ligações subsequentes.
- **Local**conecta (loopback ou endereço da própria máquina de gateway) pode ser
auto-aprovado para manter o mesmo-host UX suave.
- **As ligações não locais devem assinar o`connect.challenge`e exigir
Aprovação explícita.
- Gateway auth `gateway.auth.*` ainda se aplica a ** todas as conexões, locais ou
Remoto.

Detalhes: [Protocolo Gateway] /gateway/protocol, [Pairing] /start/pairing,
[Segurança] /gateway/security.

## Datilografia de protocolo e codegen

- Os esquemas TypeBox definem o protocolo.
- O esquema JSON é gerado a partir desses esquemas.
- Modelos rápidos são gerados a partir do esquema JSON.

## Acesso remoto

- Preferido: Tailscale ou VPN.
- Alternativa: Túnel SSH
  ```bash
  ssh -N -L 18789:127.0.0.1:18789 user@host
  ```
- O mesmo aperto de mão + auth token aplicar sobre o túnel.
- TLS + pinning opcional pode ser ativado para WS em configurações remotas.

## Instantâneo das operações

- Início:`openclaw gateway`(foreground, logs para stdout).
- Saúde:`health`sobre o WS (também incluído no`hello-ok`.
- Supervisão: lançado/sistemado para reinicialização automática.

## Invariantes

- Exactamente um Gateway controla uma única sessão Baileys por anfitrião.
- O aperto de mão é obrigatório; qualquer primeiro quadro não-JSON ou não-conectar é um fechamento difícil.
- Os eventos não são reproduzidos; os clientes devem atualizar as lacunas.
