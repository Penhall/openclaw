---
summary: "How the installer scripts work (install.sh + install-cli.sh), flags, and automation"
read_when:
  - You want to understand `openclaw.bot/install.sh`
  - You want to automate installs (CI / headless)
  - You want to install from a GitHub checkout
---

# Instalador interno

OpenClaw envia dois scripts de instalação (servidos de <<CODE0>>>):

- <<CODE0>> — instalador “recomendado” (instalação global npm por padrão; também pode instalar a partir de um checkout GitHub)
- <<CODE1>> — instalador de CLI não amigável à raiz (instala num prefixo com o seu próprio Nó)
- <<CODE2>> — instalador do Windows PowerShell (npm por padrão; instalação git opcional)

Para ver as bandeiras/comportamento atuais, execute:

```bash
curl -fsSL https://openclaw.bot/install.sh | bash -s -- --help
```

Ajuda do Windows (PowerShell):

```powershell
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -?
```

Se o instalador terminar, mas <<CODE0>> não for encontrado em um novo terminal, geralmente é um problema de PATH Node/npm. Ver: [Instalar] (<<<LINK0>>>).

## install.sh (recomendado)

O que faz (alto nível):

- Detectar OS (macOS / Linux / WSL).
- Garantir Node.js **22+** (macOS via Homebrew; Linux via NodeSource).
- Escolha o método de instalação:
- <<CODE0> (padrão): <<CODE1>>
- <<CODE2>: clonar/construir uma saída de código-fonte e instalar um script de wrapper
- No Linux: evite erros globais de permissão do npm, mudando o prefixo do npm para <<CODE3> quando necessário.
- Se atualizar uma instalação existente: executa <<CODE4>> (melhor esforço).
- Para git instala: executa <<CODE5>> após instalar/atualizar (melhor esforço).
- Mitigações <<CODE6>> instalação nativa gotchas por omissão <<CODE7>> (evita a construção contra a libvips do sistema).

Se você  quer  <<CODE0>> para linkar contra uma libvips instalada globalmente (ou você está depurando), definido:

```bash
SHARP_IGNORE_GLOBAL_LIBVIPS=0 curl -fsSL https://openclaw.bot/install.sh | bash
```

## # Discoverability / “git install” prompt

Se você executar o instalador enquanto ** já dentro de uma verificação de código fonte OpenClaw** (detectado via <<CODE0>> + <<CODE1>>), ele pede:

- atualizar e utilizar esta saída (<<<CODE0>>>)
- ou migrar para a instalação global do npm (<<<CODE1>>>)

Em contextos não-interativos (sem TTY / <<CODE0>), você deve passar <<CODE1>> (ou definido <<CODE2>>), caso contrário, o script sai com código <<CODE3>>>>.

# # Porque Git é necessário

Git é necessário para o caminho <<CODE0>> (clone / pull).

Para <<CODE0>> instala, Git é  normalmente  não necessário, mas alguns ambientes ainda acabam precisando dele (por exemplo, quando um pacote ou dependência é obtido através de um URL git). O instalador atualmente garante que Git esteja presente para evitar surpresas <<CODE1>> em distros frescos.

## # Por que npm atinge <<CODE0>> no Linux fresco

Em algumas configurações Linux (especialmente depois de instalar Node através do gerenciador de pacotes do sistema ou NodeSource), o prefixo global do npm aponta para um local root. Em seguida, <<CODE0> falha com erros de permissão <<CODE1>>/<HTML2>>>.

<<CODE0> mitiga isso mudando o prefixo para:

- <<CODE0> (e acrescentando- o a <<CODE1>> em <<CODE2>>/ <<CODE3> quando presente)

## install-cli.sh (instalador de CLI sem raiz)

Este script instala <<CODE0>> em um prefixo (padrão: <<CODE1>>>) e também instala um tempo de execução dedicado do Node sob esse prefixo, para que ele possa funcionar em máquinas onde você não quer tocar no sistema Node/npm.

Ajuda:

```bash
curl -fsSL https://openclaw.bot/install-cli.sh | bash -s -- --help
```

## install.ps1 (Windows PowerShell)

O que faz (alto nível):

- Assegurar Node.js **22+** (winget/chocolatey/Scoop ou manual).
- Escolha o método de instalação:
- <<CODE0> (padrão): <<CODE1>>
- <<CODE2>: clonar/construir uma saída de código-fonte e instalar um script de wrapper
- Executa <<CODE3> em atualizações e git instala (melhor esforço).

Exemplos:

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex -InstallMethod git
```

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex -InstallMethod git -GitDir "C:\\openclaw"
```

Variáveis de ambiente:

- <<CODE0>>
- <<CODE1>>

Requisitos Git:

Se você escolher <<CODE0>> e Git estiver faltando, o instalador imprimirá o
Git para Windows (<<CODE1>>) e saída.

Problemas comuns no Windows:

- **npm error release git / ENOENT**: install Git for Windows e reabrir PowerShell, em seguida, executar o instalador.
- **"openclaw" não é reconhecido**: sua pasta de bin global npm não está em PATH. Utilização da maioria dos sistemas
<<CODE0>>. Você também pode executar <<CODE1>>> e adicionar <<CODE2>> ao PATH, em seguida, reabrir PowerShell.
