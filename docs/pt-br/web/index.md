---
summary: "Gateway web surfaces: Control UI, bind modes, and security"
read_when:
  - You want to access the Gateway over Tailscale
  - You want the browser Control UI and config editing
---

# Web (Gateway)

O Gateway serve uma pequena **browser Control UI** (Vite + Lit) da mesma porta que o Gateway WebSocket:

- padrão: `http://<host>:18789/`
- prefixo opcional: definido `gateway.controlUi.basePath` (por exemplo, `/openclaw`)

Capacidades ao vivo em [Control UI] (</web/control-ui).
Esta página centra-se em modos de ligação, segurança e superfícies viradas para a web.

# # Webhooks

Quando <<CODE0>, o Gateway também expõe um pequeno endpoint webhook no mesmo servidor HTTP.
Ver [Configuração do portal](</gateway/configuration) → `hooks` para autácia + cargas.

## Configuração (por omissão)

A interface de controle é ** habilitado por padrão** quando os ativos estão presentes (`dist/control-ui`).
Você pode controlá-lo através da configuração:

```json5
{
  gateway: {
    controlUi: { enabled: true, basePath: "/openclaw" }, // basePath optional
  },
}
```

# # Acesso em escala de cauda

## # Serviço Integrado (recomendado)

Mantenha o Gateway em loopback e deixe Tailscale servir proxy:

```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "serve" },
  },
}
```

Em seguida, inicie o portal:

```bash
openclaw gateway
```

Abrir:

- <<CODE0> (ou o seu configurado `gateway.controlUi.basePath`)

# # Tailnet bin + token

```json5
{
  gateway: {
    bind: "tailnet",
    controlUi: { enabled: true },
    auth: { mode: "token", token: "your-token" },
  },
}
```

Em seguida, inicie o gateway (token necessário para ligações não-loopback):

```bash
openclaw gateway
```

Abrir:

- <<CODE0> (ou o seu configurado `gateway.controlUi.basePath`)

## # Internet pública (Funil)

```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "funnel" },
    auth: { mode: "password" }, // or OPENCLAW_GATEWAY_PASSWORD
  },
}
```

# # Notas de segurança

- Gateway auth é exigida por padrão (token/password ou cabeçalhos de identidade Tailscale).
- Non-loopback liga-se ainda **require** um token/password compartilhado (<<CODE0> ou env).
- O assistente gera um token de gateway por padrão (mesmo no loopback).
- A IU envia `connect.params.auth.token` ou `connect.params.auth.password`.
- Com Serve, cabeçalhos de identidade Tailscale pode satisfazer authen
`gateway.auth.allowTailscale` é `true` (sem token/senha necessária). Definir
<<CODE5> para exigir credenciais explícitas. Ver
[Tailscale] (</gateway/tailscale) e [Segurança] (/gateway/security).
- <<CODE6> requer `gateway.auth.mode: "password"` (password partilhada).

# # Construindo a UI

O Gateway serve arquivos estáticos de `dist/control-ui`. Construir com:

```bash
pnpm ui:build # auto-installs UI deps on first run
```
