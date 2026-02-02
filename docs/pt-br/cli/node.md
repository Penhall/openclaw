---
summary: "CLI reference for `openclaw node` (headless node host)"
read_when:
  - Running the headless node host
  - Pairing a non-macOS node for system.run
---

#`openclaw node`

Execute um host de nó ** sem cabeça** que se conecta ao Gateway WebSocket e expõe`system.run`/`system.which`nesta máquina.

## Por que usar um host de nó?

Use um host de nó quando quiser que os agentes ** executem comandos em outras máquinas** na sua
rede sem instalar um aplicativo completo companheiro macOS lá.

Casos comuns de utilização:

- Execute comandos em caixas remotas de Linux/Windows (build servidores, máquinas de laboratório, NAS).
- Manter exec **sandboxed** no gateway, mas delegar as execuções aprovadas para outros hosts.
- Forneça um alvo de execução leve e sem cabeça para nós de automação ou CI.

A execução ainda é guardada pelas aprovações ** e per-agent allowlists na
host de nó, para que você possa manter o acesso de comando no escopo e explícito.

## Proxy do navegador (zero-config)

Hosts de nós anunciam automaticamente um proxy de navegador se`browser.enabled`não for
desabilitado no nó. Isto permite ao agente usar a automação do navegador nesse nó
sem configuração extra.

Desactiva- o no nó, se necessário:

```json5
{
  nodeHost: {
    browserProxy: {
      enabled: false,
    },
  },
}
```

## Corre (antecedentes)

```bash
openclaw node run --host <gateway-host> --port 18789
```

Opções:

-`--host <host>`: Host Gateway WebSocket (padrão:`127.0.0.1`
-`--port <port>`: Porta do portal WebSocket (por omissão:`18789`
-`--tls`: Use TLS para a conexão de gateway
-`--tls-fingerprint <sha256>`: Impressões digitais do certificado TLS (sha256)
-`--node-id <id>`: Sobrescrever o ID do nó (limpa o símbolo de pareamento)
-`--display-name <name>`: Sobrescrever o nome da exibição do nó

## Serviço (fundo)

Instale uma máquina de nó sem cabeça como serviço de usuário.

```bash
openclaw node install --host <gateway-host> --port 18789
```

Opções:

-`--host <host>`: Host Gateway WebSocket (padrão:`127.0.0.1`
-`--port <port>`: Porta do portal WebSocket (por omissão:`18789`
-`--tls`: Use TLS para a conexão de gateway
-`--tls-fingerprint <sha256>`: Impressões digitais do certificado TLS (sha256)
-`--node-id <id>`: Sobrescrever o ID do nó (limpa o símbolo de pareamento)
-`--display-name <name>`: Sobrescrever o nome da exibição do nó
-`--runtime <runtime>`: Tempo de serviço `node`ou`127.0.0.1`0)
-`127.0.0.1`1: Reinstalar/sobrescrever se já estiver instalado

Gerenciar o serviço:

```bash
openclaw node status
openclaw node stop
openclaw node restart
openclaw node uninstall
```

Use`openclaw node run`para uma máquina de nó de primeiro plano (sem serviço).

Comandos de serviço aceitam`--json`para saída legível por máquina.

## Emparelhamento

A primeira conexão cria uma solicitação pendente de par de nós no Gateway.
Aprovar através de:

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
```

A máquina de nó armazena o seu ID de nó, token, nome de exibição e informações de conexão de gateway em`~/.openclaw/node.json`.

## Aprovações exec

`system.run`é fechado por aprovações locais:

-`~/.openclaw/exec-approvals.json`- [Aprovações exec] /tools/exec-approvals
-`openclaw approvals --node <id|name|ip>`(edição do portal)
