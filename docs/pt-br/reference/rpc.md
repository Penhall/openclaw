---
summary: "RPC adapters for external CLIs (signal-cli, imsg) and gateway patterns"
read_when:
  - Adding or changing external CLI integrations
  - Debugging RPC adapters (signal-cli, imsg)
---

# Adaptadores RPC

Openclaw integra CLIs externos via JSON-RPC. Dois padrões são usados hoje.

# # Padrão A: servidor HTTP (sinal- cli)

- `signal-cli` é executado como um daemon com JSON-RPC sobre HTTP.
- O fluxo de eventos é SSE (`/api/v1/events`).
- Sonda de saúde: `/api/v1/check`.
- OpenClaw possui ciclo de vida quando `channels.signal.autoStart=true`.

Ver [Sinal] (</channels/signal) para configuração e parâmetros.

# # # Padrão B: processo infantil stdio (imsg)

- OpenClaw gera `imsg rpc` como processo infantil.
- JSON-RPC é delimitado em linha sobre stdin/stdout (um objeto JSON por linha).
- Nenhuma porta TCP, nenhum daemon necessário.

Métodos principais utilizados:

- `watch.subscribe` → notificações (`method: "message"`)
- <<CODE2>
- `send`
- <<CODE4> (sonda/diagnóstico)

Ver [iMessage](/channels/imessage) para configuração e endereçamento (`chat_id` preferido).

# # Orientações do adaptador

- Gateway possui o processo (start/stop ligado ao ciclo de vida do provedor).
- Mantenha os clientes RPC resilientes: tempo limite, reiniciar na saída.
- Prefere IDs estáveis (por exemplo, `chat_id`) sobre strings de exibição.
