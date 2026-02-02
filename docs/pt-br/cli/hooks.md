---
summary: "CLI reference for `openclaw hooks` (agent hooks)"
read_when:
  - You want to manage agent hooks
  - You want to install or update hooks
---

#`openclaw hooks`

Gerenciar hooks de agentes (automações orientadas a eventos para comandos como`/new`,`/reset`e inicialização de gateway).

Relacionados:

- Ganchos:
- Ganchos de plug- in: [Plugins] /plugin#plugin-hooks

## Lista Todos os Ganchos

```bash
openclaw hooks list
```

Listar todos os ganchos descobertos do espaço de trabalho, gerenciados e diretórios empacotados.

**Opções:**

-`--eligible`: Mostrar apenas ganchos elegíveis (requisitos cumpridos)
-`--json`: Saída como JSON
-`-v, --verbose`: Mostrar informações detalhadas, incluindo requisitos em falta

**Exemplo de saída:**

```
Hooks (4/4 ready)

Ready:
  🚀 boot-md ✓ - Run BOOT.md on gateway startup
  📝 command-logger ✓ - Log all command events to a centralized audit file
  💾 session-memory ✓ - Save session context to memory when /new command is issued
  😈 soul-evil ✓ - Swap injected SOUL content during a purge window or by random chance
```

** Exemplo (verbose): **

```bash
openclaw hooks list --verbose
```

Mostra os requisitos em falta para ganchos inelegíveis.

**Exemplo (JSON):**

```bash
openclaw hooks list --json
```

Retorna JSON estruturado para uso programático.

## Obter informações do gancho

```bash
openclaw hooks info <name>
```

Mostrar informações detalhadas sobre um gancho específico.

** Argumentos:**

-`<name>`: Nome do gancho (por exemplo,`session-memory`

**Opções:**

-`--json`: Produção como JSON

** Exemplo: **

```bash
openclaw hooks info session-memory
```

** Saída:**

```
💾 session-memory ✓ Ready

Save session context to memory when /new command is issued

Details:
  Source: openclaw-bundled
  Path: /path/to/openclaw/hooks/bundled/session-memory/HOOK.md
  Handler: /path/to/openclaw/hooks/bundled/session-memory/handler.ts
  Homepage: https://docs.openclaw.ai/hooks#session-memory
  Events: command:new

Requirements:
  Config: ✓ workspace.dir
```

## Verifique Ganchos Elegibilidade

```bash
openclaw hooks check
```

Mostrar o resumo do estado de elegibilidade do gancho (quantos estão prontos vs. não estão prontos).

**Opções:**

-`--json`: Produção como JSON

**Exemplo de saída:**

```
Hooks Status

Total hooks: 4
Ready: 4
Not ready: 0
```

## Habilitar um gancho

```bash
openclaw hooks enable <name>
```

Habilite um gancho específico adicionando-o à sua configuração `~/.openclaw/config.json`.

**Nota:** Ganchos gerenciados por plugins mostram`plugin:<id>`em`openclaw hooks list`e
não pode ser ativado/desativado aqui. Activar/desactivar o plugin em vez disso.

** Argumentos:**

-`<name>`: Nome do gancho (por exemplo,`session-memory`

** Exemplo: **

```bash
openclaw hooks enable session-memory
```

** Saída:**

```
✓ Enabled hook: 💾 session-memory
```

** O que faz:**

- Verifica se o gancho existe e é elegível
- Atualiza`hooks.internal.entries.<name>.enabled = true`em sua configuração
- Grava a configuração no disco

** Depois de activar:**

- Reinicie o gateway para que ganchos reload (aplicativo de barra de menu reinicie no macOS, ou reinicie seu processo de gateway no dev).

## Desactivar um Gancho

```bash
openclaw hooks disable <name>
```

Desativar um gancho específico atualizando sua configuração.

** Argumentos:**

-`<name>`: Nome do gancho (por exemplo,`command-logger`

** Exemplo: **

```bash
openclaw hooks disable command-logger
```

** Saída:**

```
⏸ Disabled hook: 📝 command-logger
```

** Depois de desativar:**

- Reinicie o gateway para que os ganchos reload

## Instalar ganchos

```bash
openclaw hooks install <path-or-spec>
```

Instale um pacote de gancho de uma pasta local/arquivo ou npm.

** O que faz:**

- Copia o gancho em`~/.openclaw/hooks/<id>`- Permite os ganchos instalados no`hooks.internal.entries.*`- Regista a instalação no âmbito do`hooks.internal.installs`

**Opções:**

-`-l, --link`: Linkar um diretório local em vez de copiar (adiciona-o ao`hooks.internal.load.extraDirs`

**Arquivos apoiados:**`.zip`,`.tgz`,`.tar.gz`,`.tar`

**Exemplos:**

```bash
# Local directory
openclaw hooks install ./my-hook-pack

# Local archive
openclaw hooks install ./my-hook-pack.zip

# NPM package
openclaw hooks install @openclaw/my-hook-pack

# Link a local directory without copying
openclaw hooks install -l ./my-hook-pack
```

## Atualizar ganchos

```bash
openclaw hooks update <id>
openclaw hooks update --all
```

Atualizar pacotes de gancho instalados (apenas instala npm).

**Opções:**

-`--all`: Atualizar todos os pacotes de gancho rastreados
-`--dry-run`: Mostrar o que mudaria sem escrever

## Ganchos Ajuntados

## # memória de sessão

Salva o contexto de sessão em memória quando você emite`/new`.

**Ativar:**

```bash
openclaw hooks enable session-memory
```

** Saída:**`~/.openclaw/workspace/memory/YYYY-MM-DD-slug.md`

**Ver:** [documentação da memória da sessão]/hooks#session-memory

### comando-logger

Regista todos os eventos de comando num ficheiro de auditoria centralizado.

**Ativar:**

```bash
openclaw hooks enable command-logger
```

** Saída:**`~/.openclaw/logs/commands.log`

** Ver registos:**

```bash
# Recent commands
tail -n 20 ~/.openclaw/logs/commands.log

# Pretty-print
cat ~/.openclaw/logs/commands.log | jq .

# Filter by action
grep '"action":"new"' ~/.openclaw/logs/commands.log | jq .
```

** Veja:** [documentação do logger de comando]/hooks#command-logger

Soul-Evil

Swaps injetado conteúdo`SOUL.md`com`SOUL_EVIL.md`durante uma janela de purga ou por acaso.

**Ativar:**

```bash
openclaw hooks enable soul-evil
```

** Veja:** [Anzóis do Mal da SOUL] /hooks/soul-evil

Boot-md

Executa`BOOT.md`quando o gateway começa (após o início dos canais).

** Eventos**:`gateway:startup`

** Enable**:

```bash
openclaw hooks enable boot-md
```

**Ver:** [documentação do arranque- md]/hooks#boot-md
