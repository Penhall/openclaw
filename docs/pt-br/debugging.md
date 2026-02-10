---
summary: "Debugging tools: watch mode, raw model streams, and tracing reasoning leakage"
read_when:
  - You need to inspect raw model output for reasoning leakage
  - You want to run the Gateway in watch mode while iterating
  - You need a repeatable debugging workflow
---

Depuração

Esta página cobre helpers de depuração para saída de streaming, especialmente quando um
provedor mistura raciocínio em texto normal.

## A depuração em tempo de execução substitui

Use`/debug`em bate-papo para definir ** apenas para execução** sobreposições de configuração (memória, não disco).`/debug`está desativado por padrão; habilite com`commands.debug: true`.
Isto é útil quando você precisa alternar configurações obscuras sem editar`openclaw.json`.

Exemplos:

```
/debug show
/debug set messages.responsePrefix="[openclaw]"
/debug unset messages.responsePrefix
/debug reset
```

`/debug reset`limpa todas as substituições e retorna à configuração no disco.

## Modo de observação do portal

Para iteração rápida, execute o gateway sob o monitor de arquivos:

```bash
pnpm gateway:watch --force
```

Este mapa para:

```bash
tsx watch src/entry.ts gateway --force
```

Adicionar quaisquer bandeiras CLI gateway após`gateway:watch`e eles serão passados
em cada reinicialização.

## Perfil Dev + gateway dev (--dev)

Use o perfil dev para isolar o estado e girar uma configuração segura e descartável para
a depuração. Existem duas bandeiras`--dev`:

- **`--dev`global (perfil):** estado dos isolados sob`~/.openclaw-dev`e
padrão a porta de gateway para`19001`(portas derivadas mudam com ela).
- **`gateway --dev`: diz ao Gateway para criar automaticamente uma configuração padrão +
espaço de trabalho** quando faltando (e pular BOOTSTRAP.md).

Fluxo recomendado (dev profile + dev bootstrap):

```bash
pnpm gateway:dev
OPENCLAW_PROFILE=dev openclaw tui
```

Se ainda não tiver uma instalação global, execute o CLI via`pnpm openclaw ...`.

O que isto faz:

1. **Isolação de perfis** `--dev`global)
-`OPENCLAW_PROFILE=dev`-`OPENCLAW_STATE_DIR=~/.openclaw-dev`-`OPENCLAW_CONFIG_PATH=~/.openclaw-dev/openclaw.json`-`OPENCLAW_GATEWAY_PORT=19001`(deslocamento navegador/canvas em conformidade)

2. **Dev bootstrap** `gateway --dev`
- Grava uma configuração mínima se faltar `gateway.mode=local`, vincular loopback).
- Define`agent.workspace`para o espaço de trabalho dev.
- Define`agent.skipBootstrap=true`(sem BOOTSTRAP.md).
- Semeia os arquivos de espaço de trabalho se faltando:`AGENTS.md`,`SOUL.md`,`TOOLS.md`,`IDENTITY.md`,`USER.md`,`HEARTBEAT.md`.
- Identidade padrão: **C3-PO** (droid protocol).
- Salta os fornecedores de canais no modo dev `gateway.mode=local`0).

Reiniciar o fluxo (novo início):

```bash
pnpm gateway:dev:reset
```

Nota:`--dev`é uma bandeira de perfil **global** e é comido por alguns corredores.
Se precisar de soletrar, utilize o formulário env var:

```bash
OPENCLAW_PROFILE=dev openclaw gateway --dev --reset
```

`--reset`limpa a configuração, credenciais, sessões e a área de trabalho do dev (usando`trash`, não`rm`, então recria a configuração padrão do dev.

Dica: se um gateway não- dev já estiver em execução (lançado/systemd), pare-o primeiro:

```bash
openclaw gateway stop
```

## Registro de fluxo bruto (OpenClaw)

OpenClaw pode registrar o **raw assistente stream** antes de qualquer filtragem/formatação.
Esta é a melhor maneira de ver se o raciocínio está chegando como deltas de texto simples
(ou como blocos de pensamento separados).

Activar através do CLI:

```bash
pnpm gateway:watch --force --raw-stream
```

Sobreposição do caminho opcional:

```bash
pnpm gateway:watch --force --raw-stream --raw-stream-path ~/.openclaw/logs/raw-stream.jsonl
```

Env vars equivalentes:

```bash
OPENCLAW_RAW_STREAM=1
OPENCLAW_RAW_STREAM_PATH=~/.openclaw/logs/raw-stream.jsonl
```

Ficheiro por omissão:

`~/.openclaw/logs/raw-stream.jsonl`

## Pedacinho cru (pi-mono)

Para capturar **raw OpenAI-compat pedaços** antes de serem analisados em blocos,
O pi-mono expõe um registador separado:

```bash
PI_RAW_STREAM=1
```

Caminho opcional:

```bash
PI_RAW_STREAM_PATH=~/.pi-mono/logs/raw-openai-completions.jsonl
```

Ficheiro por omissão:

`~/.pi-mono/logs/raw-openai-completions.jsonl`

> Nota: isso só é emitido por processos usando pi-mono
>`openai-completions`fornecedor.

## Notas de segurança

- Os registros de fluxo bruto podem incluir prompts completos, saída de ferramenta e dados do usuário.
- Mantém os registos locais e apaga-os após a depuração.
- Se partilhares registos, limpa os segredos e o PII primeiro.
