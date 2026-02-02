---
summary: "Run the ACP bridge for IDE integrations"
read_when:
  - Setting up ACP-based IDE integrations
  - Debugging ACP session routing to the Gateway
---

# acp

Execute a ponte ACP (Agent Client Protocol) que fala com um OpenClaw Gateway.

Este comando fala ACP sobre stdio para IDEs e remete prompts para o Gateway
sobre WebSocket. Mantém as sessões ACP mapeadas para as teclas de sessão Gateway.

Utilização

```bash
openclaw acp

# Remote Gateway
openclaw acp --url wss://gateway-host:18789 --token <token>

# Attach to an existing session key
openclaw acp --session agent:main:main

# Attach by label (must already exist)
openclaw acp --session-label "support inbox"

# Reset the session key before the first prompt
openclaw acp --session agent:main:main --reset-session
```

## Cliente ACP (depuração)

Use o cliente ACP integrado para verificar a sanidade mental da ponte sem um IDE.
Ela gera a ponte ACP e permite que você digite alertas interativamente.

```bash
openclaw acp client

# Point the spawned bridge at a remote Gateway
openclaw acp client --server-args --url wss://gateway-host:18789 --token <token>

# Override the server command (default: openclaw)
openclaw acp client --server "node" --server-args openclaw.mjs acp --url ws://127.0.0.1:19001
```

## Como usar isto

Use o ACP quando um IDE (ou outro cliente) fala Protocolo do Cliente Agent e você deseja
para conduzir uma sessão OpenClaw Gateway.

1. Certifique-se de que o Gateway está funcionando (local ou remoto).
2. Configure o alvo do Gateway (config ou flags).
3. Aponte seu IDE para executar`openclaw acp`sobre stdio.

Configuração do exemplo (persistido):

```bash
openclaw config set gateway.remote.url wss://gateway-host:18789
openclaw config set gateway.remote.token <token>
```

Exemplo de execução direta (sem gravação de configuração):

```bash
openclaw acp --url wss://gateway-host:18789 --token <token>
```

## Selecionando agentes

Os ACP não escolhem directamente agentes. Rota pela chave da sessão do Gateway.

Usar as teclas de sessão do agente para atingir um agente específico:

```bash
openclaw acp --session agent:main:main
openclaw acp --session agent:design:main
openclaw acp --session agent:qa:bug-123
```

Cada sessão ACP mapeia para uma única chave de sessão Gateway. Um agente pode ter muitos
sessões; ACP padrão para uma sessão`acp:<uuid>`isolada a menos que você sobreponha
a chave ou o rótulo.

## Configuração do editor Zed

Adicionar um agente ACP personalizado em`~/.config/zed/settings.json`(ou usar a interface de configuração do Zed):

```json
{
  "agent_servers": {
    "OpenClaw ACP": {
      "type": "custom",
      "command": "openclaw",
      "args": ["acp"],
      "env": {}
    }
  }
}
```

Para atingir um Gateway ou agente específico:

```json
{
  "agent_servers": {
    "OpenClaw ACP": {
      "type": "custom",
      "command": "openclaw",
      "args": [
        "acp",
        "--url",
        "wss://gateway-host:18789",
        "--token",
        "<token>",
        "--session",
        "agent:design:main"
      ],
      "env": {}
    }
  }
}
```

Em Zed, abra o painel Agent e selecione "OpenClaw ACP" para iniciar um tópico.

## Mapeamento de sessão

Por padrão, as sessões ACP recebem uma chave de sessão de Gateway isolada com um prefixo`acp:`.
Para reutilizar uma sessão conhecida, passe uma chave de sessão ou etiqueta:

-`--session <key>`: use uma chave específica de sessão Gateway.
-`--session-label <label>`: resolver uma sessão existente por rótulo.
-`--reset-session`: menta um novo ID de sessão para essa chave (mesma chave, nova transcrição).

Se seu cliente ACP suporta metadados, você pode substituir por sessão:

```json
{
  "_meta": {
    "sessionKey": "agent:main:main",
    "sessionLabel": "support inbox",
    "resetSession": true
  }
}
```

Saiba mais sobre as teclas de sessão em [/conceitos/sessão]/concepts/session.

## Opções

-`--url <url>`: Gateway WebSocket URL (por omissão para gateway.remote.url quando configurado).
- Token da porta.
- Senha do portal.
-`--session <key>`: tecla de sessão padrão.
-`--session-label <label>`: etiqueta de sessão padrão para resolver.
-`--require-existing`: falha se a chave/rótulo da sessão não existir.
-`--reset-session`: redefinir a chave de sessão antes da primeira utilização.
-`--no-prefix-cwd`: não prefixe prompts com o diretório de trabalho.
-`--verbose, -v`: registo detalhado no stderr.

## # Opções`acp client`

-`--cwd <dir>`: Directório de trabalho da sessão ACP.
-`--server <command>`: Comando do servidor ACP (por omissão:`openclaw`.
-`--server-args <args...>`: argumentos adicionais passados ao servidor ACP.
-`--server-verbose`: habilitar o registro de verbose no servidor ACP.
-`--verbose, -v`: registo do cliente.
