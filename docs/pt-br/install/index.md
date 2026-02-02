---
summary: "Install OpenClaw (recommended installer, global install, or from source)"
read_when:
  - Installing OpenClaw
  - You want to install from GitHub
---

Instalar

Use o instalador, a menos que tenha uma razão para não o fazer. Monta o CLI e vai a bordo.

# # Instalação rápida (recomendada)

```bash
curl -fsSL https://openclaw.bot/install.sh | bash
```

Janelas (Powershell):

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

Próxima etapa (se você pulou a bordo):

```bash
openclaw onboard --install-daemon
```

# # Requisitos do sistema

- **Node >=22**
- macOS, Linux ou Windows via WSL2
- <<CODE0> somente se você construir a partir da fonte

# # Escolha o seu caminho de instalação

# # # 1) script do instalador (recomendado)

Instala <<CODE0>> globalmente via npm e executa onboarding.

```bash
curl -fsSL https://openclaw.bot/install.sh | bash
```

Parâmetros do instalador:

```bash
curl -fsSL https://openclaw.bot/install.sh | bash -s -- --help
```

Detalhes: [Installer internals](<<<LINK0>>>).

Não-interactivo (a bordo do skip):

```bash
curl -fsSL https://openclaw.bot/install.sh | bash -s -- --no-onboard
```

## # 2) Instalação global (manual)

Se já tem Nó:

```bash
npm install -g openclaw@latest
```

Se você tem libvips instalados globalmente (comum no macOS via Homebrew) e <<CODE0> não consegue instalar, force binários pré-construídos:

```bash
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest
```

Se você ver <<CODE0>>, instalar ferramentas de compilação (macOS: Xcode CLT + <<CODE1>>) ou usar a solução <<CODE2> acima para pular a compilação nativa.

Ou:

```bash
pnpm add -g openclaw@latest
```

Depois:

```bash
openclaw onboard --install-daemon
```

## # 3) Da fonte (contributores/dev)

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build # auto-installs UI deps on first run
pnpm build
openclaw onboard --install-daemon
```

Dica: se você ainda não tiver uma instalação global, execute comandos de repo via <<CODE0>>.

# # # 4) Outras opções de instalação

- Docker: [Docker] (<<<LINK0>>>)
- Nix: [Nix]
- Ansível: [Ansível](<<<LINK2>>)
- Bun (apenas CLI): [Bun] (<<<LINK3>>>)

# # Depois de instalar

- Executar a bordo: <<CODE0>>>
- Verificação rápida: <<CODE1>>>
- Verificar a saúde da porta de entrada: <<CODE2>> + <<CODE3>>
- Abra o painel: <<CODE4>>

# # # Método de instalação: npm vs git (instalador)

O instalador suporta dois métodos:

- <<CODE0> (padrão): <<CODE1>>
- <<CODE2>: clonar/build a partir do GitHub e correr a partir de uma saída de origem

Bandeiras CLI

```bash
# Explicit npm
curl -fsSL https://openclaw.bot/install.sh | bash -s -- --install-method npm

# Install from GitHub (source checkout)
curl -fsSL https://openclaw.bot/install.sh | bash -s -- --install-method git
```

Bandeiras comuns:

- <<CODE0>>
- <<CODE1>> (padrão: <<CODE2>>)
- <<CODE3>> (skip <<CODE4>> ao utilizar uma saída existente)
- <<CODE5>> (promessas desativadas; requeridas em CI/automação)
- <<CODE6>> (imprimir o que aconteceria; não fazer alterações)
- <<CODE7> (escorrega a bordo)

## # Variáveis de ambiente

Env vars equivalentes (úteis para automação):

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>
- <<CODE3>>
- <<CODE4>>
- <<CODE5>>
- <<CODE6>> (padrão: <<CODE7>>>; evita <<CODE8>> construção contra libvips do sistema)

## Resolução de problemas: <<CODE0> não encontrado (PATH)

Diagnóstico rápido:

```bash
node -v
npm -v
npm prefix -g
echo "$PATH"
```

Se <<CODE0> (macOS/Linux) ou <<CODE1> (Windows) é **não** presente dentro <<CODE2>>, seu shell não pode encontrar binários globais npm (incluindo <<CODE3>>).

Corrigir: adicione-o ao seu ficheiro de arranque da shell (zsh: <<CODE0>>, bash: <<CODE1>>):

```bash
# macOS / Linux
export PATH="$(npm prefix -g)/bin:$PATH"
```

No Windows, adicione a saída de <<CODE0>> ao seu PATH.

Em seguida, abra um novo terminal (ou <<CODE0>> em zsh / <<CODE1>> em bash).

# # Atualizar / desinstalar

- Actualizações: [Atualização] (<<<<LINK0>>>)
- Migrar para uma nova máquina: [Migrar] (<<<LINK1>>>)
- Desinstalar: [Desinstalar] (<<<LINK2>>)
