---
summary: Node + tsx "__name is not a function" crash notes and workarounds
read_when:
  - Debugging Node-only dev scripts or watch mode failures
  - Investigating tsx/esbuild loader crashes in OpenClaw
---

# Nó + tsx "\ \ name is not a function" crash

# # Resumo

Executar Openclaw via Node com <<CODE0>> falha na inicialização com:

```
[openclaw] Failed to start CLI: TypeError: __name is not a function
    at createSubsystemLogger (.../src/logging/subsystem.ts:203:25)
    at .../src/agents/auth-profiles/constants.ts:25:20
```

Isso começou depois de trocar scripts dev de Bun para <<CODE0>> (comprometer <<CODE1>>, 2026-01-06). O mesmo caminho de execução funcionou com Bun.

# # Ambiente

- Nó: v25.x (observado em v25.3.0)
- tsx: 4.21.0
- OS: macOS (repro também provável em outras plataformas que executam Node 25)

# # Repro (somente nós)

```bash
# in repo root
node --version
pnpm install
node --import tsx src/entry.ts status
```

# # Mínimo repro em repo

```bash
node --import tsx scripts/repro/tsx-name-repro.ts
```

# # Verificação da versão do nó

- Node 25.3.0: falhas
- Node 22.22.0 (Homebrew <<CODE0>>): falhas
- Node 24: ainda não instalado aqui; precisa de verificação

# # Notas / hipótese

- <<CODE0> usa o esbuild para transformar o TS/ESM. O esbuild <<CODE1> emite um <<CODE2> helper e envolve definições de funções com <<CODE3>>>.
- O crash indica que <<CODE4> existe, mas não é uma função em tempo de execução, o que implica que o ajudante está faltando ou substituído para este módulo no caminho do carregador Node 25.
- Problemas semelhantes <<CODE5>> de helper foram relatados em outros consumidores de esbuild quando o helper está faltando ou reescrito.

# # História da regressão

- <<CODE0>> (2026-01-06): scripts alterados de Bun para tsx para tornar Bun opcional.
- Antes disso (caminho Bun), <<CODE1>>> e <<CODE2>> funcionaram.

# # Contornos

- Use Bun para scripts dev (reversão temporária atual).
- Use Node + tsc watch, então execute a saída compilada:
  ```bash
  pnpm exec tsc --watch --preserveWatchOutput
  node --watch openclaw.mjs status
  ```
- Confirmado localmente: <<CODE0>> + <<CODE1> funciona no Node 25.
- Desabilitar esbuild keepNames no carregador TS, se possível (preveni <<CODE2>> inserção helper); tsx não expõe isso atualmente.
- Test Node LTS (22/24) com <<CODE3>> para ver se o problema é Node 25–específico.

# # Referências

- https://opennext.js.org/cloudflare/howtos/keep names
- https://esbuild.github.io/api/#keep-names
- https://github.com/evanw/esbuild/issues/1031

# # Próximos passos

- Repro no Node 22/24 para confirmar regressão Node 25.
- Teste <<CODE0>> por noite ou pino para versão anterior se existir uma regressão conhecida.
- Se reproduzir em Node LTS, arquive um repro mínimo upstream com o <<CODE1>> stack trace.
