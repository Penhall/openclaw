---
summary: "How to run tests locally (vitest) and when to use force/coverage modes"
read_when:
  - Running or fixing tests
---

Testes

- Kit de teste completo (suites, ao vivo, Docker): [Testação] (</testing)

- <<CODE0>: Mata qualquer processo de gateway que mantenha a porta de controle padrão, então executa a suíte Vitest completa com uma porta de gateway isolada para que os testes do servidor não colidam com uma instância em execução. Use isto quando um gateway anterior executar a porta esquerda 18789 ocupada.
- <<CODE1>: Corre Vitest com cobertura V8. Os limiares globais são 70% linhas/ramos/funções/declarações. A cobertura exclui pontos de entrada pesados de integração (fiação CLI, pontes gateway/telegram, servidor estático webchat) para manter o alvo focado na lógica de teste unitário.
- <<CODE2>: Executa testes de fumaça de gateway de ponta a ponta (multi-instance WS/HTTP/node pareamento).
- <<CODE3>: Executa os testes ao vivo do provedor (minimax/zai). Requer chaves API e `LIVE=1` (ou provedor-específico `*_LIVE_TEST=1`) para desestabilizar.

# # Modelo banco de latência (chaves locais)

Programa: [`scripts/bench-model.ts`](https://github.com/openclaw/openclaw/blob/main/scripts/bench-model.ts)

Uso:

- <<CODE0>
- Env opcional: `MINIMAX_API_KEY`, `MINIMAX_BASE_URL`, `MINIMAX_MODEL`, `ANTHROPIC_API_KEY`
- Prompt padrão: “Responda com uma única palavra: ok. Sem pontuação ou texto extra.”

Última corrida (2025-12-31, 20 corridas):

- mediana mínima de 1279 ms (min. 1114, máx. 2431)
- opus mediana 2454ms (min 1224, max 3170)

# # Onboarding E2E (Docker)

Docker é opcional; isso só é necessário para os testes de fumaça embarcados em containerized.

Fluxo total de arranque a frio num contentor Linux limpo:

```bash
scripts/e2e/onboard-docker.sh
```

Este script impulsiona o assistente interativo através de um pseudo-tty, verifica arquivos config/workspace/session, então inicia o gateway e executa `openclaw health`.

# # QR importar fumo (Docker)

Garante `qrcode-terminal` cargas sob Nó 22+ em Docker:

```bash
pnpm test:docker:qr
```
