---
summary: "CLI reference for `openclaw plugins` (list, install, enable/disable, doctor)"
read_when:
  - You want to install or manage in-process Gateway plugins
  - You want to debug plugin load failures
---

#`openclaw plugins`

Gerenciar plugins/extensões do Gateway (carregados em processo).

Relacionados:

- Sistema de plug-ins: [Plugins] /plugin
- Manifesto de plug- in + esquema: [Infest de Plug- in] /plugins/manifest
- Endurecimento da segurança: [Segurança] /gateway/security

## Comandos

```bash
openclaw plugins list
openclaw plugins info <id>
openclaw plugins enable <id>
openclaw plugins disable <id>
openclaw plugins doctor
openclaw plugins update <id>
openclaw plugins update --all
```

Plugins agrupados enviam com OpenClaw mas começam desativados. Usar`plugins enable`para
Activa-os.

Todos os plugins devem enviar um arquivo`openclaw.plugin.json`com um esquema JSON em linha
`configSchema`, mesmo que vazio). Manifestações ou esquemas ausentes/inválidos impedem
o plugin da validação de configuração de carregamento e falha.

Instalar

```bash
openclaw plugins install <path-or-spec>
```

Nota de segurança: tratar plugin instala como código em execução. Prefere versões fixas.

Arquivos apoiados:`.zip`,`.tgz`,`.tar.gz`,`.tar`.

Use`--link`para evitar copiar um diretório local (adiciona ao`plugins.load.paths`:

```bash
openclaw plugins install -l ./my-plugin
```

Actualização

```bash
openclaw plugins update <id>
openclaw plugins update --all
openclaw plugins update <id> --dry-run
```

As atualizações só se aplicam aos plug-ins instalados a partir do npm (tracked in`plugins.installs`.
