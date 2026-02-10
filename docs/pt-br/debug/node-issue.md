---
summary: Node + tsx "__name is not a function" crash notes and workarounds
read_when:
  - Debugging Node-only dev scripts or watch mode failures
  - Investigating tsx/esbuild loader crashes in OpenClaw
---

# Nó + tsx "\ \ name is not a function" crash

## Resumo

Executar Openclaw via Node com`tsx`falha na inicialização com:

```
[openclaw] Failed to start CLI: TypeError: __name is not a function
    at createSubsystemLogger (.../src/logging/subsystem.ts:203:25)
    at .../src/agents/auth-profiles/constants.ts:25:20
```

Isso começou depois de mudar scripts dev de Bun para`tsx`(compromete`2871657e`, 2026-01-06). O mesmo caminho de execução funcionou com Bun.

## Ambiente

- Nó: v25.x (observado em v25.3.0)
- tsx: 4.21.0
- OS: macOS (repro também provável em outras plataformas que executam Node 25)

## Repro (somente nós)

```bash
# in repo root
node --version
pnpm install
node --import tsx src/entry.ts status
```

## Mínimo repro em repo

```bash
node --import tsx scripts/repro/tsx-name-repro.ts
```

## Verificação da versão do nó

- Node 25.3.0: falhas
- Node 22.22.0 `node@22`Homebrew): falhas
- Node 24: ainda não instalado aqui; precisa de verificação

## Notas / hipótese

-`tsx`usa esbuild para transformar TS/ESM. O`keepNames`da esbuild emite um ajudante`__name`e envolve definições de função com`__name(...)`.
- A falha indica que`__name`existe mas não é uma função em tempo de execução, o que implica que o ajudante está faltando ou substituído para este módulo no caminho do carregador Node 25.
- Problemas de ajuda`__name`semelhantes foram relatados em outros consumidores de esbuild quando o ajudante está faltando ou reescrito.

## História da regressão

-`2871657e`(2026-01-06): scripts alterados de Bun para tsx para tornar Bun opcional.
- Antes disso, funcionava o`openclaw status`e o`gateway:watch`.

## Contornos

- Use Bun para scripts dev (reversão temporária atual).
- Use Node + tsc watch, então execute a saída compilada:
  ```bash
  pnpm exec tsc --watch --preserveWatchOutput
  node --watch openclaw.mjs status
  ```
- Confirmado localmente:`pnpm exec tsc -p tsconfig.json`+`node openclaw.mjs status`funciona no no 25.
- Desactivar o esbuild keepNames no carregador TS, se possível (preveni a inserção do auxiliar`__name`; o tsx não expõe isto de momento.
- Teste Nó LTS (22/24) com`tsx`para ver se a questão é Nó 25–específica.

## Referências

- https://opennext.js.org/cloudflare/howtos/keep names
- https://esbuild.github.io/api/#keep-names
- https://github.com/evanw/esbuild/issues/1031

## Próximos passos

- Repro no Node 22/24 para confirmar regressão Node 25.
- Teste`tsx`por noite ou pino para versão anterior se existir uma regressão conhecida.
- Se reproduzir em Node LTS, arquive um repro mínimo upstream com o`__name`stack trace.
