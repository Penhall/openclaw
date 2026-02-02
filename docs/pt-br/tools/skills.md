---
summary: "Skills: managed vs workspace, gating rules, and config/env wiring"
read_when:
  - Adding or modifying skills
  - Changing skill gating or load rules
---

# Habilidades (OpenClaw)

OpenClaw usa pastas de habilidades compatíveis com ** para ensinar o agente a usar ferramentas. Cada habilidade é um diretório contendo uma `SKILL.md` com matéria frontal YAML e instruções. OpenClaw carrega **competências combinadas** mais substituições locais opcionais, e filtra-as em tempo de carga com base em ambiente, configuração e presença binária.

# # Locais e precedência

As habilidades são carregadas de **três lugares**:

1. **Competências confusas**: enviada com a instalação (pacote npm ou OpenClaw.app)
2. **Competências gerenciadas/locais**: <<CODE0>
3. **Competências no espaço de trabalho**: `<workspace>/skills`

Se um nome de habilidade conflitos, precedência é:

`<workspace>/skills` (mais alto) → `~/.openclaw/skills` → competências agrupadas (mais baixo)

Além disso, você pode configurar pastas de habilidade extra (mais baixa precedência) via
`skills.load.extraDirs` em `~/.openclaw/openclaw.json`.

# # Per-agente vs habilidades compartilhadas

Em ** setups multi-agente**, cada agente tem seu próprio espaço de trabalho. Isso significa:

- ** Competências por agente** viver em <<CODE0> apenas para esse agente.
- ** Competências partilhadas** viver em `~/.openclaw/skills` (gerido/local) e são visíveis
** todos os agentes** na mesma máquina.
- ** Pastas compartilhadas** também podem ser adicionadas via `skills.load.extraDirs` (mais baixo
precedência) se você quiser um pacote de habilidades comuns usado por vários agentes.

Se o mesmo nome de habilidade existe em mais de um lugar, a precedência usual
aplica-se: workspace ganha, em seguida, gerenciado/local, em seguida, empacotado.

# # Plugins + habilidades

Plugins podem enviar suas próprias habilidades listando `skills` diretórios em
<<CODE1> (caminhos relativos à raiz do plugin). Carregar as habilidades do plug-in
quando o plugin estiver habilitado e participar das regras de precedência de habilidades normais.
Você pode gate-los via `metadata.openclaw.requires.config` na configuração do plugin
entrada. Ver [Plugins](/plugin) para descoberta/configuração e [Ferramentas](/tools) para a
ferramenta superfície essas habilidades ensinam.

## ClawHub (instalar + sincronizar)

ClawHub é o registro público de habilidades para OpenClaw. Navegar em
https://clawhub.com. Use-o para descobrir, instalar, atualizar e fazer backup de habilidades.
Guia completo: [ClawHub] (</tools/clawhub).

Fluxos comuns:

- Instale uma habilidade em seu espaço de trabalho:
- <<CODE0>
- Atualizar todas as habilidades instaladas:
- <<CODE1>
- Sincronizar (scan + publicar atualizações):
- <<CODE2>

Por padrão, `clawhub` instala em `./skills` sob seu trabalho atual
diretório (ou cai de volta para o espaço de trabalho OpenClaw configurado). Escolhas Openclaw
na próxima sessão.

# # Notas de segurança

- Tratar as competências de terceiros como ** código fidedigno**. Leia-os antes de habilitar.
- Prefere correr sandboxed para entradas não confiáveis e ferramentas arriscadas. Ver [Sandboxing] (</gateway/sandboxing).
- <<CODE0> e <<CODE1> injectam segredos no processo de ** máquina**
para a volta do agente (não a caixa de areia). Mantenha segredos fora de alertas e registros.
- Para um modelo de ameaça mais amplo e listas de verificação, ver [Segurança] (</gateway/security).

# # Formato (AgenteSkills + Pi-compatível)

<<CODE0> deve incluir, pelo menos:

```markdown
---
name: nano-banana-pro
description: Generate or edit images via Gemini 3 Pro Image
---
```

Notas:

- Seguimos a especificação do Agente Skills para layout/intenção.
- O analisador usado pelo agente incorporado suporta **linha única** somente chaves de matéria frontal.
- `metadata` deve ser um objecto JSON de linha única**.
- Use <<CODE1> em instruções para referenciar o caminho da pasta de habilidades.
- Teclas de matéria frontal opcionais:
- `homepage` — URL emergido como “Site Web” na interface macOS Skills (também suportado via `metadata.openclaw.homepage`).
- `user-invocable` — `true|false` (padrão: `true`). Quando <<CODE7>, a habilidade é exposta como um comando de barra de usuário.
- `disable-model-invocation` — `true|false` (padrão: `false`). Quando <<CODE11>, a habilidade é excluída do modelo prompt (ainda disponível via invocação do usuário).
- `command-dispatch` — `tool` (facultativo). Quando definido como `tool`, o comando slash ignora o modelo e envia diretamente para uma ferramenta.
- `command-tool` — nome da ferramenta a invocar quando `command-dispatch: tool` for definido.
- `command-arg-mode` — `raw` (padrão). Para despacho de ferramentas, encaminha o texto args bruto para a ferramenta (sem análise de núcleo).

A ferramenta é invocada com parâmetros:
`{ command: "<raw args>", commandName: "<slash command>", skillName: "<skill name>" }`.

# # Gating (filtros de tempo de carga)

OpenClaw ** habilidades filtrantes no tempo de carga** usando `metadata` (linha única JSON):

```markdown
---
name: nano-banana-pro
description: Generate or edit images via Gemini 3 Pro Image
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["uv"], "env": ["GEMINI_API_KEY"], "config": ["browser.enabled"] },
        "primaryEnv": "GEMINI_API_KEY",
      },
  }
---
```

Campo `metadata.openclaw`:

- <<CODE0> – incluir sempre a habilidade (escorregar outros portões).
- `emoji` — emoji opcional utilizado pela interface macOS Skills.
- `homepage` — URL opcional apresentado como “Site Web” na interface macOS Skills.
- `os` — lista facultativa de plataformas (`darwin`, `linux`, `win32`). Se definido, a habilidade só é elegível nesses sistemas operacionais.
- `requires.bins` — lista; cada uma deve existir em `PATH`.
- `requires.anyBins` — lista; pelo menos uma deve existir em `PATH`.
- `requires.env` — lista; env var deve existir ** ou** deve ser fornecido na configuração.
- `requires.config` — lista de caminhos `openclaw.json` que devem ser verdadeiros.
- `primaryEnv` — nome env var associado a `skills.entries.<name>.apiKey`.
- `install` — matriz facultativa de especificações de instalador utilizadas pelo macOS Skills UI (brew/node/go/uv/download).

Nota sobre sandboxing:

- <<CODE0> é verificado no **host** no tempo de carga de habilidade.
- Se um agente é sandbox, o binário também deve existir ** dentro do recipiente**.
Instale-o via `agents.defaults.sandbox.docker.setupCommand` (ou uma imagem personalizada).
<<CODE2> é executado uma vez após a criação do recipiente.
Instalações de pacotes também requerem saída de rede, um root gravável FS, e um usuário root na sandbox.
Exemplo: a habilidade `summarize` (<CODE4>>) precisa do `summarize` CLI
na caixa de areia para correr lá.

Exemplo do instalador:

```markdown
---
name: gemini
description: Use Gemini CLI for coding assistance and Google search lookups.
metadata:
  {
    "openclaw":
      {
        "emoji": "♊️",
        "requires": { "bins": ["gemini"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "gemini-cli",
              "bins": ["gemini"],
              "label": "Install Gemini CLI (brew)",
            },
          ],
      },
  }
---
```

Notas:

- Se vários instaladores estão listados, o gateway escolhe uma opção **single** preferida (brew quando disponível, caso contrário nó).
- Se todos os instaladores são `download`, OpenClaw lista cada entrada para que você possa ver os artefatos disponíveis.
- Especificações do instalador podem incluir `os: ["darwin"|"linux"|"win32"]` para filtrar opções por plataforma.
- Node instala honra `skills.install.nodeManager` em `openclaw.json` (padrão: npm; opções: npm/pnpm/yarn/bun).
Isso só afeta **skill installs**; o tempo de execução do Gateway ainda deve ser Node
(O Bun não é recomendado para o WhatsApp/Telegram).
- Vá instala: se `go` estiver faltando e `brew` estiver disponível, o gateway instala Go via Homebrew primeiro e define `GOBIN` para Homebrew `bin` quando possível.
- Baixar instalações: `url` (necessário), `archive` (`tar.gz` `tar.bz2` `zip`), `extract` (padrão: auto quando o arquivo foi detectado), `stripComponents`>, `targetDir` (padrão: `~/.openclaw/tools/<skillKey>`).

Se não `metadata.openclaw` estiver presente, a habilidade é sempre elegível (a menos que
desactivado na configuração ou bloqueado por <<CODE1> para competências agrupadas).

# # # Substituição de configuração (`~/.openclaw/openclaw.json`)

Competências agrupadas/geridas podem ser comutadas e fornecidas com valores env:

```json5
{
  skills: {
    entries: {
      "nano-banana-pro": {
        enabled: true,
        apiKey: "GEMINI_KEY_HERE",
        env: {
          GEMINI_API_KEY: "GEMINI_KEY_HERE",
        },
        config: {
          endpoint: "https://example.invalid",
          model: "nano-pro",
        },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

Nota: se o nome da habilidade contém hífens, cite a chave (JSON5 permite chaves citadas).

As chaves de configuração correspondem ao nome ** por omissão. Se uma habilidade define
`metadata.openclaw.skillKey`, use essa chave em `skills.entries`.

Regras:

- <<CODE0> desabilita a habilidade, mesmo que seja empacotada/instalada.
- <<CODE1>: injectada ** apenas se ** a variável já não estiver definida no processo.
- <<CODE2>: conveniência para as competências que declaram `metadata.openclaw.primaryEnv`.
- `config`: saco opcional para campos personalizados por habilidade; chaves personalizadas devem viver aqui.
- <<CODE5>: lista facultativa de autorizações apenas para **compilações**. Se estiver pronto, apenas
as competências agrupadas na lista são elegíveis (competências geridas/espaço de trabalho não afectadas).

# # Injecção do ambiente (por agente)

Quando uma execução de um agente começa, OpenClaw:

1. Lê metadados de habilidade.
2. Aplica qualquer `skills.entries.<key>.env` ou `skills.entries.<key>.apiKey` a
`process.env`.
3. Constrói o prompt do sistema com ** competências elegíveis**.
4. Restaura o ambiente original após o fim da execução.

Isto é **escoberto para a execução do agente**, não um ambiente global shell.

# # Fotos da sessão (performance)

OpenClaw instantâneos das habilidades elegíveis **quando uma sessão começa** e reutiliza essa lista para turnos subsequentes na mesma sessão. Alterações nas habilidades ou configuração têm efeito na próxima nova sessão.

As habilidades também podem atualizar no meio da sessão quando o observador de habilidades está habilitado ou quando um novo nó remoto elegível aparece (ver abaixo). Pense nisso como um **hot reload**: a lista atualizada é captada na próxima volta do agente.

# # Nós remotos do macOS (gateway Linux)

Se o Gateway estiver rodando no Linux, mas um nó **macOS** estiver conectado **com `system.run` permitido** (a segurança de aprovações Exec não está definida como `deny`), OpenClaw pode tratar as habilidades somente do macOS como elegíveis quando os binários necessários estiverem presentes nesse nó. O agente deve executar essas habilidades através da ferramenta `nodes` (tipicamente `nodes.run`).

Isso depende do nó reportando seu suporte de comando e em uma sonda bin via `system.run`. Se o nó macOS ficar offline mais tarde, as habilidades permanecem visíveis; as invocações podem falhar até que o nó se reconecte.

# # Observador de habilidades (auto-refresh)

Por padrão, o OpenClaw observa pastas de habilidade e bate o instantâneo de habilidades quando <<CODE0> os arquivos mudam. Configurar isto em `skills.load`:

```json5
{
  skills: {
    load: {
      watch: true,
      watchDebounceMs: 250,
    },
  },
}
```

# # Impacto do item (lista de competências)

Quando as habilidades são elegíveis, OpenClaw injeta uma lista XML compacta de habilidades disponíveis no prompt do sistema (via `formatSkillsForPrompt` em `pi-coding-agent`). O custo é determinístico:

- **Base aérea (apenas quando ≥1 habilidade):** 195 caracteres.
- ** Por habilidade:** 97 caracteres + o comprimento dos valores de XML escalonados `<name>`, `<description>` e `<location>`.

Fórmula (caracteres):

```
total = 195 + Σ (97 + len(name_escaped) + len(description_escaped) + len(location_escaped))
```

Notas:

- A fuga de XML se expande `& < > " '` em entidades (<CODE1>>, <CODE2>>, etc.), aumentando o comprimento.
- As contagens variam de acordo com o tokenizador modelo. Uma estimativa de estilo OpenAI áspero é ~4 caracteres / token, por isso **97 caracteres 24 tokens** por habilidade mais seus comprimentos de campo reais.

# # Ciclo de vida de habilidades gerenciadas

OpenClaw envia um conjunto de competências de base como **competências
instalar (pacote npm ou OpenClaw.app). <<CODE0> existe para locais
substitui (por exemplo, pinning / patching uma habilidade sem alterar o pacote
(copiar). As habilidades do espaço de trabalho são de propriedade do usuário e sobrepõem-se tanto em conflitos de nomes.

# # Referência de configuração

Veja [Skills config](</tools/skills-config) para o esquema completo de configuração.

# # Procurando mais habilidades?

Acesse https://clawhub.com.

---
