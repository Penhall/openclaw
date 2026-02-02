---
title: "Node.js + npm (PATH sanity)"
summary: "Node.js + npm install sanity: versions, PATH, and global installs"
read_when:
  - "You installed OpenClaw but `openclaw` is “command not found”"
  - "You’re setting up Node.js/npm on a new machine"
  - "npm install -g ... fails with permissions or PATH issues"
---

# Node.js + npm (sanidade PATH)

A linha de base do OpenClaw é **Node 22+**.

Se você pode executar <<CODE0>> mas depois ver <<CODE1>>>, é quase sempre um problema **PATH**: o diretório onde npm coloca binários globais não está no PATH do seu shell.

# # Diagnóstico rápido

Executar:

```bash
node -v
npm -v
npm prefix -g
echo "$PATH"
```

Se <<CODE0> (macOS/Linux) ou <<CODE1> (Windows) é **não** presente dentro <<CODE2>>, seu shell não pode encontrar binários globais npm (incluindo <<CODE3>>).

# # Fixar: colocar a pasta global do npm no PATH

1. Encontre seu prefixo global npm:

```bash
npm prefix -g
```

2. Adicione o diretório global npm bin ao seu arquivo de inicialização shell:

- zsh: <<CODE0>>
- bash: <<CODE1>>>

Exemplo (substitua o caminho com sua saída <<CODE0>>):

```bash
# macOS / Linux
export PATH="/path/from/npm/prefix/bin:$PATH"
```

Em seguida, abra um novo terminal** (ou execute <<CODE0>> em zsh / <<CODE1> em bash).

No Windows, adicione a saída de <<CODE0>> ao seu PATH.

# # Fix: evite <<CODE0>> / erros de permissão (Linux)

Se <<CODE0> falhar com <<CODE1>>, mude o prefixo global do npm para um diretório com escrita pelo usuário:

```bash
mkdir -p "$HOME/.npm-global"
npm config set prefix "$HOME/.npm-global"
export PATH="$HOME/.npm-global/bin:$PATH"
```

Persista na linha <<CODE0>> em seu arquivo de inicialização shell.

# # Opções de instalação recomendadas do nó

Você terá as poucas surpresas se Node/npm estiverem instalados de uma forma que:

- mantém o Nó actualizado (22+)
- torna o bin dir global estável e em PATH em novas shells

Escolhas comuns:

- macOS: Homebrew (<<<CODE0>>) ou um gestor de versões
- Linux: seu gerenciador de versão preferido, ou uma instalação distro-suportada que fornece Node 22+
- Windows: instalador oficial de Node, <<CODE1>>, ou um gerenciador de versões do Windows Node

Se você usar um gerenciador de versões (nvm/fnm/asdf/etc), certifique-se de que ele seja inicializado na shell que você usa no dia-a-dia (zsh vs bash) para que o PATH que ele define esteja presente quando você executa instaladores.
