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

# # A depuração em tempo de execução substitui

Use <<CODE0> em chat para definir ** apenas para execução** sobreposições de configuração (memória, não disco).
<<CODE1>> está desativado por padrão; habilite com <<CODE2>>.
Isto é útil quando você precisa alternar configurações obscuras sem editar <<CODE3>>>.

Exemplos:

```
/debug show
/debug set messages.responsePrefix="[openclaw]"
/debug unset messages.responsePrefix
/debug reset
```

<<CODE0> limpa todas as substituições e retorna à configuração on-disk.

# # Modo de observação do portal

Para iteração rápida, execute o gateway sob o monitor de arquivos:

```bash
pnpm gateway:watch --force
```

Este mapa para:

```bash
tsx watch src/entry.ts gateway --force
```

Adicione todas as bandeiras CLI do gateway após <<CODE0> e elas serão passadas
em cada reinicialização.

# # Perfil Dev + gateway dev (--dev)

Use o perfil dev para isolar o estado e girar uma configuração segura e descartável para
a depuração. Existem duas bandeiras** <<CODE0>>>:

- ** Estado global <<CODE0>> (perfil):** estado dos isolados em <<CODE1>>> e
padrão a porta de gateway para <<CODE2>> (portas derivadas mudam com ele).
- **<<<CODE3>>: diz ao Gateway para criar automaticamente uma configuração padrão +
espaço de trabalho** quando faltando (e pular BOOTSTRAP.md).

Fluxo recomendado (dev profile + dev bootstrap):

```bash
pnpm gateway:dev
OPENCLAW_PROFILE=dev openclaw tui
```

Se ainda não tiver uma instalação global, execute o CLI via <<CODE0>>.

O que isto faz:

1. **Isolação do perfil** (global <<CODE0>>)
- <<CODE1>>
- <<CODE2>>
- <<CODE3>>
- <<CODE4>> (Narrowser/canvas mudar em conformidade)

2. **Dev bootstrap** (<<<CODE0>>>)
- Escreve uma configuração mínima se faltar (<<<CODE1>>, vincular loopback).
- Define <<CODE2>> para o espaço de trabalho dev.
- Sets <<CODE3>> (sem BOOTSTRAP.md).
- Semeia os arquivos de espaço de trabalho se faltando:
<<CODE4>>, <<CODE5>>, <<CODE6>>, <<CODE7>>, <<CODE8>>, <<CODE9>>>.
- Identidade padrão: **C3-PO** (droid protocol).
- Ignora os fornecedores de canais no modo dev (<<<CODE10>>>).

Reiniciar o fluxo (novo início):

```bash
pnpm gateway:dev:reset
```

Nota: <<CODE0> é uma bandeira de perfil **global** e é comido por alguns corredores.
Se precisar de soletrar, utilize o formulário env var:

```bash
OPENCLAW_PROFILE=dev openclaw gateway --dev --reset
```

<<CODE0> limpa a configuração, credenciais, sessões e o espaço de trabalho dev (usando
<<CODE1>>, não <<CODE2>>), em seguida, recria a configuração padrão dev.

Dica: se um gateway não- dev já estiver em execução (lançado/systemd), pare-o primeiro:

```bash
openclaw gateway stop
```

# # Registro de fluxo bruto (OpenClaw)

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

<<CODE0>>

# # Pedacinho cru (pi-mono)

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

<<CODE0>>

> Nota: isso só é emitido por processos usando pi-mono
> <<CODE0>> fornecedor.

# # Notas de segurança

- Os registros de fluxo bruto podem incluir prompts completos, saída de ferramenta e dados do usuário.
- Mantém os registos locais e apaga-os após a depuração.
- Se partilhares registos, limpa os segredos e o PII primeiro.
