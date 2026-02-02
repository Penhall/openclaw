---
summary: "CLI reference for `openclaw browser` (profiles, tabs, actions, extension relay)"
read_when:
  - You use `openclaw browser` and want examples for common tasks
  - You want to control a browser running on another machine via a node host
  - You want to use the Chrome extension relay (attach/detach via toolbar button)
---

#`openclaw browser`

Gerencie o servidor de controle do navegador do OpenClaw e execute ações do navegador (tabs, instantâneos, capturas de tela, navegação, cliques, digitação).

Relacionados:

- Ferramenta de navegador + API: [ferramentas de navegador] /tools/browser
- Relé de extensão do Chrome: [Extensão do cromo] /tools/chrome-extension

## Bandeiras comuns

-`--url <gatewayWsUrl>`: Gateway WebSocket URL (defaults to config).
-`--token <token>`: Ficha do portal (se necessário).
-`--timeout <ms>`: tempo limite de solicitação (ms).
-`--browser-profile <name>`: escolha um perfil de navegador (por omissão na configuração).
-`--json`: saída legível por máquina (onde suportada).

## Início rápido (local)

```bash
openclaw browser --browser-profile chrome tabs
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

## Perfil

Os perfis são chamados de configurações de roteamento de navegador. Na prática:

-`openclaw`: lança/liga-se a uma instância dedicada ao Chrome gerenciada pelo OpenClaw (dir de dados do usuário isolado).
-`chrome`: controla o(s) separado(s) Chrome(s) existente(s) através do relé de extensão Chrome.

```bash
openclaw browser profiles
openclaw browser create-profile --name work --color "#FF5A36"
openclaw browser delete-profile --name work
```

Usar um perfil específico:

```bash
openclaw browser --browser-profile work tabs
```

## Tabs

```bash
openclaw browser tabs
openclaw browser open https://docs.openclaw.ai
openclaw browser focus <targetId>
openclaw browser close <targetId>
```

## Instantâneo / captura de tela / ações

Instantâneo:

```bash
openclaw browser snapshot
```

Imagem:

```bash
openclaw browser screenshot
```

Navegar/clicar/tipo (automatização de interface baseada em ref):

```bash
openclaw browser navigate https://example.com
openclaw browser click <ref>
openclaw browser type <ref> "hello"
```

## Relé de extensão do Chrome (anexar através do botão da barra de ferramentas)

Este modo permite ao agente controlar uma página Chrome existente que você anexa manualmente (não se attach automaticamente).

Instale a extensão desempacotada para um caminho estável:

```bash
openclaw browser extension install
openclaw browser extension path
```

Em seguida, Chrome →`chrome://extensions`→ habilitar "Modo de desenvolvimento" → "Carregar desempacotado" → selecione a pasta impressa.

Guia completo: [Extensão do cromo]/tools/chrome-extension

## Controle remoto do navegador (proxy host nós)

Se o Gateway é executado em uma máquina diferente do navegador, execute um host **node** na máquina que tem Chrome/Brave/Edge/Chromium. O Gateway irá proxy de ações de navegador para esse nó (sem servidor de controle de navegador separado necessário).

Use`gateway.nodes.browser.mode`para controlar a rota automática e`gateway.nodes.browser.node`para fixar um nó específico se múltiplos estão conectados.

Segurança + configuração remota: [ferramenta do navegador]/tools/browser, [acesso remoto]/gateway/remote, [Tailscale]/gateway/tailscale, [Segurança]/gateway/security
