---
summary: "Bun workflow (experimental): installs and gotchas vs pnpm"
read_when:
  - You want the fastest local dev loop (bun + watch)
  - You hit Bun install/patch/lifecycle script issues
---

# Bun (experimental)

Objetivo: executar este repo com **Bun** (opcional, não recomendado para WhatsApp/Telegram)
sem divergir dos fluxos de trabalho do pnpm.

Não recomendado para o tempo de execução do Gateway** (bugs do WhatsApp/Telegram). Use o nó para a produção.

# # Situação

- Bun é um tempo de execução local opcional para executar diretamente TypeScript (<<<CODE0>>, <<CODE1>>>).
- <<CODE2> é o padrão para builds e permanece totalmente suportado (e usado por algumas ferramentas de documentos).
- Bun não pode usar <<CODE3>> e irá ignorá-lo.

Instalar

Predefinição:

```sh
bun install
```

Nota: <<CODE0>/<<CODE1>> são gitignored, por isso não há repo churn de qualquer forma. Se você quiser  no lockfile writes :

```sh
bun install --no-save
```

# # Compilar / Teste (Bun)

```sh
bun run build
bun run vitest run
```

# # Roteiros de ciclo de vida da barra (bloqueados por padrão)

Bun pode bloquear scripts do ciclo de vida da dependência, a menos que explicitamente confiável (<<CODE0>> / <<CODE1>>>).
Para este repo, os scripts comumente bloqueados não são necessários:

- <<CODE0>> <<CODE1>>: verificações Node major >= 20 (corremos Node 22+).
- <<CODE2>> <<CODE3>>: emite avisos sobre esquemas de versões incompatíveis (sem artefatos de construção).

Se você atingir um problema em tempo de execução real que exija esses scripts, confie neles explicitamente:

```sh
bun pm trust @whiskeysockets/baileys protobufjs
```

# # Caveats

- Alguns scripts ainda são hard code pnpm (por exemplo, <<CODE0>>, <<CODE1>>, <<CODE2>>>). Faz isso via pnpm por enquanto.
