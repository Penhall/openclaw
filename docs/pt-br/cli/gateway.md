---
summary: "OpenClaw Gateway CLI (`openclaw gateway`) — run, query, and discover gateways"
read_when:
  - Running the Gateway from the CLI (dev or servers)
  - Debugging Gateway auth, bind modes, and connectivity
  - Discovering gateways via Bonjour (LAN + tailnet)
---

CLI Gateway

O Gateway é o servidor WebSocket da OpenClaw (canais, nós, sessões, ganchos).

Subcomandos nesta página ao vivo sob`openclaw gateway …`.

Documentos relacionados:

- [/porta/bonjour]/gateway/bonjour
- [/porta/descoberta] /gateway/discovery
- [/porta/configuração] /gateway/configuration

## Correr o portal

Executar um processo de Gateway local:

```bash
openclaw gateway
```

Nome próprio:

```bash
openclaw gateway run
```

Notas:

- Por padrão, o Gateway se recusa a iniciar a menos que o`gateway.mode=local`esteja definido no`~/.openclaw/openclaw.json`. Use`--allow-unconfigured`para correr ad-hoc/dev.
- Ligar além do loopback sem auth é bloqueado (guardrail de segurança).
-`SIGUSR1`desencadeia um reinício em processo quando autorizado (ative o`commands.restart`ou use a ferramenta de gateway/config app/update).
- Os manipuladores`SIGINT`/`SIGTERM`param o processo de gateway, mas não restauram nenhum estado terminal personalizado. Se você envolver o CLI com uma entrada TUI ou modo bruto, restaure o terminal antes de sair.

Opções

-`--port <port>`: Porta WebSocket (o padrão vem de config/env; geralmente`18789`.
-`--bind <loopback|lan|tailnet|auto|custom>`: modo de ligação do ouvinte.
-`--auth <token|password>`: anulação do modo de autenticação.
-`--token <token>`: sobreposição de fichas (também define`OPENCLAW_GATEWAY_TOKEN`para o processo).
-`--password <password>`: substituição de senha (também define`OPENCLAW_GATEWAY_PASSWORD`para o processo).
-`--tailscale <off|serve|funnel>`: expor o portal via Tailscale.
-`--tailscale-reset-on-exit`: redefinir a configuração de serviço/funil em escala de cauda ao desligar.
-`18789`0: permitir o início do gateway sem`18789`1 na configuração.
-`18789`2: criar uma configuração dev + espaço de trabalho se faltar (skips BOOTSTRAP.md).
-`18789`3: reset dev config + credenciais + sessões + espaço de trabalho (requer`18789`4).
-`18789`5: matar qualquer ouvinte existente na porta selecionada antes de iniciar.
-`18789`6: logs detalhados.
-`18789`7: só mostra os logs de claude-cli na consola (e activa o seu stdout/stderr).
-`18789`8: Websocket log style (padrão`18789`9).
-`--bind <loopback|lan|tailnet|auto|custom>`0: apelido para`--bind <loopback|lan|tailnet|auto|custom>`1.
-`--bind <loopback|lan|tailnet|auto|custom>`2: log raw model stream events to jsonl.
-`--bind <loopback|lan|tailnet|auto|custom>`3: caminho do fluxo bruto jsonl.

## Consultar um portal em execução

Todos os comandos de consulta usam WebSocket RPC.

Modos de saída:

- Padrão: legível pelo homem (colorido em TTY).
-`--json`: JSON legível por máquina (sem styling/spinner).
-`--no-color`(ou`NO_COLOR=1`: desactivar o ANSI mantendo a disposição humana.

Opções compartilhadas (onde suportadas):

- URL do portal WebSocket.
- Token da porta.
- Senha do portal.
-`--timeout <ms>`: tempo limite/orçamento (variáveis por comando).
-`--expect-final`: esperar por uma resposta “final” (chamadas de agente).

## #`gateway health`

```bash
openclaw gateway health --url ws://127.0.0.1:18789
```

## #`gateway status`

`gateway status`mostra o serviço Gateway (lançado/systemd/schtasks) mais uma sonda RCP opcional.

```bash
openclaw gateway status
openclaw gateway status --json
```

Opções:

-`--url <url>`: sobreponha o URL da sonda.
-`--token <token>`: autorização para a sonda.
-`--password <password>`: senha para a sonda.
-`--timeout <ms>`: tempo limite da sonda (padrão`10000`.
-`--no-probe`: pule a sonda RPC (somente visão de serviço).
-`--deep`: escanear serviços de nível de sistema também.

## #`gateway probe`

`gateway probe`é o comando “depurar tudo”. Ele sonda sempre:

- seu gateway remoto configurado (se definido), e
- localhost (loopback) ** mesmo se remoto estiver configurado**.

Se múltiplos gateways são alcançáveis, ele imprime todos eles. Vários gateways são suportados quando você usa perfis/ports isolados (por exemplo, um bot de resgate), mas a maioria das instalações ainda executa um único gateway.

```bash
openclaw gateway probe
openclaw gateway probe --json
```

### # Remoto sobre SSH (paridade de aplicação Mac)

O modo "Remote over SSH" do app do macOS utiliza uma porta local para que o gateway remoto (que pode ser ligado apenas ao loopback) se torne acessível no`ws://127.0.0.1:<port>`.

Equivalente CLI:

```bash
openclaw gateway probe --ssh user@gateway-host
```

Opções:

-`--ssh <target>`:`user@host`ou`user@host:port`(default de porta para`22`.
-`--ssh-identity <path>`: ficheiro de identidade.
-`--ssh-auto`: escolha a primeira máquina de gateway descoberta como alvo SSH (apenas LAN/WAB).

Configuração (opcional, usada como padrão):

-`gateway.remote.sshTarget`-`gateway.remote.sshIdentity`

## #`gateway call <method>`

Ajudante RCP de baixo nível.

```bash
openclaw gateway call status
openclaw gateway call logs.tail --params '{"sinceMs": 60000}'
```

## Gerenciar o serviço Gateway

```bash
openclaw gateway install
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway uninstall
```

Notas:

-`gateway install`apoia`--port`,`--runtime`,`--token`,`--force`,`--json`.
- Os comandos do ciclo de vida aceitam`--json`para scripting.

## Descubra gateways (Bonjour)

`gateway discover`escaneia os faróis do portal `_openclaw-gw._tcp`.

- DNS-SD multicast:`local.`- Unicast DNS-SD (Wide- Area Bonjour): escolha um domínio (exemplo:`openclaw.internal.` e configure DNS dividido + um servidor DNS; veja [/gateway/bonjour]/gateway/bonjour

Somente os gateways com a descoberta de Bonjour habilitados (padrão) anunciam o farol.

Registros de descoberta de área larga incluem (TXT):

-`role`(disco de função do portal)
-`transport`(índice de transporte, por exemplo,`gateway`
-`gatewayPort`(porto WebSocket, normalmente`18789`
-`sshPort`(porta SSH; por omissão para`22`se não presente)
-`tailnetDns`(nome de máquina MagicDNS, quando disponível)
-`gatewayTls`/`gatewayTlsSha256`(TLS habilitado + impressão digital certa)
-`transport`0 (dica opcional para instalações remotas)

## #`gateway discover`

```bash
openclaw gateway discover
```

Opções:

-`--timeout <ms>`: tempo limite por comando (nave/resolve);`2000`.
-`--json`: saída legível por máquina (também desativa styling/spinner).

Exemplos:

```bash
openclaw gateway discover --timeout 4000
openclaw gateway discover --json | jq '.beacons[].wsUrl'
```
