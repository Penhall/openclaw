---
summary: "Manual logins for browser automation + X/Twitter posting"
read_when:
  - You need to log into sites for browser automation
  - You want to post updates to X/Twitter
---

# login do navegador + postagem do X/Twitter

# # login manual (recomendado)

Quando um site requer login, ** entre manualmente** no perfil do navegador **host** (o navegador openclaw).

Não dê ao modelo as suas credenciais. Os logins automatizados frequentemente ativam defesas anti-bot e podem bloquear a conta.

Voltar ao documento principal do navegador: [Browser](</tools/browser).

# # Que perfil Chrome é usado?

OpenClaw controla um perfil **dedicado do Chrome** (nomeado `openclaw`, UI alaranjada). Isto é separado do seu perfil diário do navegador.

Duas maneiras fáceis de acessá-lo:

1. **Pergunte ao agente para abrir o navegador** e, em seguida, faça login em si mesmo.
2. **Abrir via CLI**:

```bash
openclaw browser start
openclaw browser open https://x.com
```

Se você tem vários perfis, passe `--browser-profile <name>` (o padrão é `openclaw`).

# # X/Twitter: fluxo recomendado

- **Leia/pesquisa/threads:** use a habilidade **bird** CLI (sem navegador, estável).
- Repo: https://github.com/steipete/bird
- ** Atualizações pós:** use o navegador **host** (agente manual).

# # Sandboxing + acesso ao navegador host

Sessões de navegador Sandboxed são ** mais prováveis de desencadear detecção de bots. Para X/Twitter (e outros sites restritos), prefira o navegador **host**.

Se o agente for sandbox, a ferramenta do navegador é padrão na sandbox. Para permitir o controle da máquina:

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        browser: {
          allowHostControl: true,
        },
      },
    },
  },
}
```

Em seguida, alvo do navegador host:

```bash
openclaw browser open https://x.com --browser-profile openclaw --target host
```

Ou desabilitar sandboxing para o agente que posta atualizações.
