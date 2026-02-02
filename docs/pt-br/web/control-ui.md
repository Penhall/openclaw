---
summary: "Browser-based control UI for the Gateway (chat, nodes, config)"
read_when:
  - You want to operate the Gateway from a browser
  - You want Tailnet access without SSH tunnels
---

Controle de UI (browser)

O Control UI é um pequeno aplicativo **Vite + Lit** de uma página servido pelo Gateway:

- padrão: `http://<host>:18789/`
- prefixo opcional: definido `gateway.controlUi.basePath` (por exemplo, `/openclaw`)

Ele fala diretamente para o Gateway WebSocket** na mesma porta.

# # Abre rápido (local)

Se o Gateway estiver a correr no mesmo computador, abra:

- http://127.0.0.1:18789/ (ou http://localhost:18789/)

Se a página não for carregada, inicie o Gateway primeiro: `openclaw gateway`.

O Auth é fornecido durante o aperto de mão WebSocket via:

- <<CODE0>
- <<CODE1>
O painel de configurações do painel permite armazenar um token; as senhas não são persistidas.
O assistente de integração gera um token de gateway por padrão, então cole-o aqui na primeira conexão.

# # O que pode fazer (hoje)

- Conversar com o modelo via Gateway WS (`chat.history`, `chat.send`, `chat.abort`, `chat.inject`)
- Chamadas de ferramenta de fluxo + cartões de saída de ferramenta ao vivo em Chat (eventos de agente)
- Canais: WhatsApp/Telegram/Discord/Slack + canais plugin (Mattermost, etc.) status + login QR + configuração por canal (<`channels.status`, `web.login.*`, `config.patch`)
- Instâncias: lista de presenças + actualização (<`system-presence`)
- Sessões: lista + pensamento por sessão/verbose substitui (`sessions.list`, `sessions.patch`)
- Trabalhos do Cron: list/add/run/ habilitar/desativar + histórico de execução (`cron.*`)
- Habilidades: status, habilitar/desativar, instalar, atualizações da chave API (`skills.*`)
- Nós: lista + tampas (`node.list`)
- Aprovações Exec: edit gateway or nodo allowlists + pedir política para `exec host=gateway/node` (`exec.approvals.*`)
- Configuração: view/edit `~/.openclaw/openclaw.json` (`config.get`, `config.set`)
- Configuração: aplicar + reiniciar com validação (`config.apply`) e acordar a última sessão ativa
- Config escreve incluem um guarda base-hash para evitar edições simultâneas
- Esquema de configuração + renderização de formulários (<`config.schema`, incluindo esquemas de plugin + canal); O editor RAW JSON permanece disponível
- Depuração: estado/saúde/modelos instantâneos + log de eventos + chamadas manuais de RPC (`status`, `health`, `models.list`)
- Registos: cauda ao vivo dos registos de ficheiros de gateway com filtro/exportação (`logs.tail`)
- Atualização: execute um pacote/git update + reinicie (`update.run`) com um relatório de reinício

# # Comportamento de conversa

- <<CODE0> é ** sem bloqueio**: ocorre imediatamente com `{ runId, status: "started" }` e os fluxos de resposta através de <<CODE2> acontecimentos.
- Reenviar com o mesmo <<CODE3> retorna <<CODE4> durante a execução, e <<CODE5> após a conclusão.
- `chat.inject` adiciona uma nota de assistente à transcrição da sessão e transmite um evento `chat` para atualizações somente de UI (sem execução do agente, sem entrega do canal).
- Pára.
- Clique em **Pare** (chamadas `chat.abort`)
- Tipo `/stop` (ou `stop|esc|abort|wait|exit|interrupt`) para abortar fora da banda
- `chat.abort` suporta `{ sessionKey }` (não `runId`) para abortar todas as execuções ativas para essa sessão

# # Acesso à tailnet (recomendado)

## # Serviço Integrado de Tailscale (preferido)

Mantenha o Gateway em loopback e deixe Tailscale Servir proxy com HTTPS:

```bash
openclaw gateway --tailscale serve
```

Abrir:

- <<CODE0> (ou o seu configurado `gateway.controlUi.basePath`)

Por padrão, os pedidos de Servir podem autenticar através de cabeçalhos de identidade Tailscale
(<`tailscale-user-login`) quando <<CODE1> é `true`. Openclaw
verifica a identidade, resolvendo o endereço `x-forwarded-for` com
<<CODE4> e combinando-o com o cabeçalho, e só aceita estes quando o
request hits loopback com cabeçalhos de Tailscale `x-forwarded-*`. Definir
`gateway.auth.allowTailscale: false` (ou força `gateway.auth.mode: "password"`)
se você deseja exigir um token/senha mesmo para o tráfego Servir.

# # # Ligar à tailnet + token

```bash
openclaw gateway --bind tailnet --token "$(openssl rand -hex 32)"
```

Em seguida, abra:

- <<CODE0> (ou o seu configurado `gateway.controlUi.basePath`)

Colar o token nas configurações de UI (enviado como `connect.params.auth.token`).

# # HTTP inseguro

Se você abrir o painel sobre HTTP simples (`http://<lan-ip>` ou <CODE1>>),
o navegador roda em um contexto **não seguro** e bloqueia WebCrypto. Por padrão,
OpenClaw **blocos** Controlar conexões de UI sem identidade do dispositivo.

**Recomendada correção:** use HTTPS (Tailscale Serve) ou abra a UI localmente:

- <<CODE0> (Servo)
- <<CODE1> (na máquina de gateway)

**Exemplo de baixo grau (token-only sobre HTTP):**

```json5
{
  gateway: {
    controlUi: { allowInsecureAuth: true },
    bind: "tailnet",
    auth: { mode: "token", token: "replace-me" },
  },
}
```

Isso desativa identidade do dispositivo + pareamento para a interface de controle (mesmo em HTTPS). Utilização
Só se confiar na rede.

Veja [Tailscale](</gateway/tailscale) para orientação de configuração HTTPS.

# # Construindo a UI

O Gateway serve arquivos estáticos de `dist/control-ui`. Construir com:

```bash
pnpm ui:build # auto-installs UI deps on first run
```

Base absoluta opcional (quando você deseja URLs de ativos fixos):

```bash
OPENCLAW_CONTROL_UI_BASE_PATH=/openclaw/ pnpm ui:build
```

Para desenvolvimento local (separar servidor dev):

```bash
pnpm ui:dev # auto-installs UI deps on first run
```

Em seguida, aponte a IU para a URL do Gateway WS (por exemplo, `ws://127.0.0.1:18789`).

# # Depuração/teste: servidor dev + Gateway remoto

A interface de controle é arquivos estáticos; o alvo WebSocket é configurável e pode ser
diferente da origem HTTP. Isto é útil quando deseja o servidor Vite dev
localmente, mas o Portal corre para outro lado.

1. Inicie o servidor dev UI: <<CODE0>
2. Abra um URL como:

```text
http://localhost:5173/?gatewayUrl=ws://<gateway-host>:18789
```

Autorização única opcional (se necessário):

```text
http://localhost:5173/?gatewayUrl=wss://<gateway-host>:18789&token=<gateway-token>
```

Notas:

- <<CODE0> é armazenado em localStorage após a carga e removido do URL.
- <<CODE1> é armazenado em localStorage; <<CODE2> é mantido apenas na memória.
- Use `wss://` quando o Gateway estiver por trás do TLS (Tailscale Serve, HTTPS proxy, etc.).

Detalhes da configuração do acesso remoto: [Acesso remoto] (</gateway/remote).
