---
summary: "Retry policy for outbound provider calls"
read_when:
  - Updating provider retry behavior or defaults
  - Debugging provider send errors or rate limits
---

# Política de repetição

## Objetivos

- Tente novamente por solicitação HTTP, não por fluxo multi-step.
- Preservar encomendas tentando apenas o passo atual.
- Evite duplicar operações não-idepotentes.

Padrões

- Tentativas: 3
- Limite máximo de atraso: 30000 ms
- Jitter: 0,1 (10 por cento)
- Predefinição do fornecedor:
- Telegram min atraso: 400 ms
- Discórdia atraso min: 500 ms

## Comportamento

Discórdia

- Repetições apenas em erros de limite de taxa (HTTP 429).
- Usa Discord`retry_after`quando disponível, caso contrário exponencial backoff.

Telegrama

- Repetições de erros transitórios (429, tempo limite, conexão/reset/fechado, temporariamente indisponível).
- Usa`retry_after`quando disponível, caso contrário exponencial backoff.
- Os erros de análise Markdown não são repetidos; eles voltam ao texto simples.

Configuração

Definir política de repetição por provedor em`~/.openclaw/openclaw.json`:

```json5
{
  channels: {
    telegram: {
      retry: {
        attempts: 3,
        minDelayMs: 400,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
    discord: {
      retry: {
        attempts: 3,
        minDelayMs: 500,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
  },
}
```

## Notas

- Repetições aplicar por pedido (mensagem enviar, upload de mídia, reação, votação, adesivo).
- Os fluxos compósitos não voltam a tentar etapas completas.
