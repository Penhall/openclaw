---
summary: "Install OpenClaw declaratively with Nix"
read_when:
  - You want reproducible, rollback-able installs
  - You're already using Nix/NixOS/Home Manager
  - You want everything pinned and managed declaratively
---

Instalação do Nix

A maneira recomendada de executar OpenClaw com Nix é via **[nix-openclaw](<<LINK0>>)** — um módulo Home Manager incluído em baterias.

# # Início Rápido

Colar isto ao seu agente de IA (Claude, Cursor, etc.):

```text
I want to set up nix-openclaw on my Mac.
Repository: github:openclaw/nix-openclaw

What I need you to do:
1. Check if Determinate Nix is installed (if not, install it)
2. Create a local flake at ~/code/openclaw-local using templates/agent-first/flake.nix
3. Help me create a Telegram bot (@BotFather) and get my chat ID (@userinfobot)
4. Set up secrets (bot token, Anthropic key) - plain files at ~/.secrets/ is fine
5. Fill in the template placeholders and run home-manager switch
6. Verify: launchd running, bot responds to messages

Reference the nix-openclaw README for module options.
```

Guia completo: [github.com/openclaw/nix-openclaw](<<<LINK0>>)**
>
> O repo nix-openclaw é a fonte de verdade para a instalação do Nix. Esta página é apenas uma visão geral rápida.

# # O que tens

- Gateway + app macOS + ferramentas (sussurro, spotify, câmeras) — todas fixadas
- Serviço lançado que sobrevive a reinicialização
- Sistema de plug-in com configuração declarativa
- Retrocesso instantâneo: <<CODE0>>

---

# # Modo Nix Runtime Behavior

Quando <<CODE0> é definido (automático com nix-openclaw):

O OpenClaw suporta um modo **Nix** que torna a configuração determinística e desativa fluxos de auto-instalação.
Habilitá- lo exportando:

```bash
OPENCLAW_NIX_MODE=1
```

No macOS, o aplicativo GUI não herda automaticamente shell env vars. Podes.
também habilitar modo Nix através de padrões:

```bash
defaults write bot.molt.mac openclaw.nixMode -bool true
```

### Configuração + caminhos de estado

OpenClaw lê a configuração do JSON5 de <<CODE0>> e armazena dados mutáveis em <<CODE1>.

- <<CODE0>> (padrão: <<CODE1>>)
- <<CODE2>> (padrão: <<CODE3>>)

Ao correr sob o Nix, defina estes explicitamente para locais gerenciados pelo Nix de modo que o estado de execução e a configuração
Fique fora da loja imutável.

## # Comportamento em tempo de execução no modo Nix

- Os fluxos de auto-instalação e auto-mutação estão desativados
- Mensagens de remediação específicas do Nix em falta
- UI superfícies de um banner de modo Nix somente leitura quando presente

# # Nota de embalagem (macOS)

O fluxo de embalagens do macOS espera um modelo Info.plist estável em:

```
apps/macos/Sources/OpenClaw/Resources/Info.plist
```

[<<<CODE0>>](<<LINK0>>>) copia este modelo para o pacote de aplicativos e patches campos dinâmicos
(ID bundle, versão/build, Git SHA, teclas Sparkle). Isto mantém a plist deterministic para SwiftPM
embalagem e compila Nix (que não dependem de uma cadeia de ferramentas Xcode completa).

# # Relacionado

- [nix- openclaw] (<<<LINK0>>) — guia de configuração completo
- [Wizard] (<<<LINK1>>) — configuração CLI não-Nix
- [Docker] (<<<LINK2>>) — configuração em contentores
