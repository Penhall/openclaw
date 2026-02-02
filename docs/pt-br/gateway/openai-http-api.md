---
summary: "Expose an OpenAI-compatible /v1/chat/completions HTTP endpoint from the Gateway"
read_when:
  - Integrating tools that expect OpenAI Chat Completions
---

# OpenAI Chat Completions (HTTP)

O OpenClaw’s Gateway pode servir um pequeno endpoint de Completações de Chat compatível com OpenAI.

Este endpoint é ** desactivado por padrão**. Activar a configuração primeiro.

- <<CODE0>>
- Mesma porta do Gateway (WS + Multiplex HTTP): <<CODE1>>

Sob o capô, as requisições são executadas como um agente normal do Gateway (mesmo codepath como <<CODE0>>), então roteamento/permissões/config correspondem ao seu Gateway.

# # Autenticação

Usa a configuração de autenticação do Gateway. Enviar um símbolo ao portador:

- <<CODE0>>

Notas:

- Quando <<CODE0>, utilizar <<CODE1>> (ou <<CODE2>>>).
- Quando <<CODE3>, utilizar <<CODE4>> (ou <<CODE5>>).

# # Escolhendo um agente

Não são necessários cabeçalhos personalizados: codificar o ID do agente no campo OpenAI <<CODE0>:

- <<CODE0>> (exemplo: <<CODE1>>, <<CODE2>>)
- <<CODE3> (também conhecido por)

Ou alvo de um agente OpenClaw específico pelo cabeçalho:

- <<CODE0>> (padrão: <<CODE1>>)

Avançado:

- <<CODE0> para controlar completamente o roteamento da sessão.

# # Habilitando o ponto final

Definir <<CODE0>> para <<CODE1>>:

```json5
{
  gateway: {
    http: {
      endpoints: {
        chatCompletions: { enabled: true },
      },
    },
  },
}
```

# # Desactivar o ponto final

Definir <<CODE0>> para <<CODE1>>:

```json5
{
  gateway: {
    http: {
      endpoints: {
        chatCompletions: { enabled: false },
      },
    },
  },
}
```

# # Comportamento da sessão

Por padrão, o endpoint é **sem estado por solicitação** (uma nova chave de sessão é gerada cada chamada).

Se a solicitação incluir uma string OpenAI <<CODE0>>, o Gateway deriva uma chave de sessão estável dela, para que chamadas repetidas possam compartilhar uma sessão de agente.

# # Streaming (SSE)

Definir <<CODE0>> para receber Eventos Enviados pelo Servidor (SSE):

- <<CODE0>>
- Cada linha de eventos é <<CODE1>>
- O fluxo termina com <<CODE2>>>

# # Exemplos

Sem transmissão:

```bash
curl -sS http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{
    "model": "openclaw",
    "messages": [{"role":"user","content":"hi"}]
  }'
```

Streaming:

```bash
curl -N http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{
    "model": "openclaw",
    "stream": true,
    "messages": [{"role":"user","content":"hi"}]
  }'
```
