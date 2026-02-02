---
summary: "Exec approvals, allowlists, and sandbox escape prompts"
read_when:
  - Configuring exec approvals or allowlists
  - Implementing exec approval UX in the macOS app
  - Reviewing sandbox escape prompts and implications
---

# Aprovações exec

As aprovações Exec são o aplicativo **companion / nó host guardail** para deixar um agente sandboxed correr
comandos em uma máquina real (<`gateway` ou `node`). Pense nisso como uma trava de segurança.
Os comandos só são permitidos quando a aprovação do utilizador for aprovada pela política + allowlist + (opcional).
As aprovações exec são **além de** para a política de ferramentas e gating elevado (a menos que elevado é definido como `full`, que ignora aprovações).
A política eficaz é a ** mais restrita** de `tools.exec.*` e os padrões de aprovação; se um campo de aprovações for omitido, o <<CODE4> o valor é usado.

Se o aplicativo companheiro UI estiver **não disponível**, qualquer pedido que exija um prompt é
resolvido pelo **ask fallback** (por omissão: negá-lo).

# # Onde se aplica

As aprovações exec são aplicadas localmente no host de execução:

- ** host gateway** → processo `openclaw` na máquina de gateway
- ** host nó** → corredor de nó (macOS app companheiro ou host de nó sem cabeça)

divisão macOS:

- **Node host service** encaminha `system.run` para o aplicativo **macOS** sobre IPC local.
- **macOS app** obriga aprovações + executa o comando no contexto UI.

# # Configurações e armazenamento

As aprovações vivem em um arquivo JSON local no host de execução:

<<CODE0>

Esquema de exemplo:

```json
{
  "version": 1,
  "socket": {
    "path": "~/.openclaw/exec-approvals.sock",
    "token": "base64url-token"
  },
  "defaults": {
    "security": "deny",
    "ask": "on-miss",
    "askFallback": "deny",
    "autoAllowSkills": false
  },
  "agents": {
    "main": {
      "security": "allowlist",
      "ask": "on-miss",
      "askFallback": "deny",
      "autoAllowSkills": true,
      "allowlist": [
        {
          "id": "B0C8C0B3-2C2D-4F8A-9A3C-5A4B3C2D1E0F",
          "pattern": "~/Projects/**/bin/rg",
          "lastUsedAt": 1737150000000,
          "lastUsedCommand": "rg -n TODO",
          "lastResolvedPath": "/Users/user/Projects/.../bin/rg"
        }
      ]
    }
  }
}
```

# # Botões de política

### Segurança (`exec.security`)

- **deny**: bloquear todas as solicitações executivas do anfitrião.
- ** allowlist**: permite apenas comandos listados.
- ** completo**: permitir tudo (equivalente a elevado).

## # Perguntar (`exec.ask`)

- **off**: nunca pronto.
- **on- miss**: prompt somente quando a allowlist não corresponde.
- ** sempre**: prompt em cada comando.

## # Perguntar para trás (`askFallback`)

Se um prompt for necessário, mas nenhuma UI for acessível, o backback decide:

- **deny**: bloco.
- ** allowlist**: só permite se a allowlist corresponder.
- ** Completo**: Permitir.

# # Lista de permissão (por agente)

Allowlists são ** por agente**. Se existirem vários agentes, mude qual agente você é
edição no aplicativo macOS. Os padrões são **caso-insensíveis glob correspondências**.
Padrões devem resolver para ** caminhos binários** (ingressos apenas para o nome de base são ignorados).
Legado <<CODE0> entradas são migradas para `agents.main` em carga.

Exemplos:

- <<CODE0>
- <<CODE1>
- <<CODE2>

Cada faixa de entrada da lista de permissões:

- **id** UUID estável usado para identidade UI (opcional)
- ** última hora utilizada**
- ** último comando usado**
- ** Último caminho resolvido**

# # Auto-permitir CLIs habilidade

Quando **Auto-allow skill CLIs** é habilitado, executáveis referenciados por habilidades conhecidas
são tratados como autorizados em nós (nodo macOS ou host sem cabeça). Isto utiliza
`skills.bins` sobre o RPC Gateway para obter a lista de bin de habilidades. Desactiva isto se quiseres listas de permissões manuais rigorosas.

# # Recipientes seguros (somente no stdin)

`tools.exec.safeBins` define uma pequena lista de binários ** stdin-only** (por exemplo `jq`)
que pode ser executado em modo allowlist **sem** entradas allowlist explícitas. Caixas seguras rejeitam
args de arquivos posicionais e tokens semelhantes ao caminho, então eles só podem operar no fluxo de entrada.
Conchas e redirecionamentos não são permitidos automaticamente no modo allowlist.

O encadeamento de shell (`&&`, `||`, `;`) é permitido quando cada segmento de topo satisfaz a lista de permissão
(incluindo caixas seguras ou auto-permissão de habilidade). As redirecionações permanecem sem suporte no modo allowlist.

Caixas seguras padrão: `jq`, <<CODE1>, `cut`, `sort`, `uniq`, <<CODE5>, `tail`, `tr`, <<CODE8>.

# # Controle a edição de UI

Use o cartão **Control UI → Nós → Aprovações Exec** para editar padrões, per-agent
substitui, e listas de permissão. Escolha um escopo (Padrões ou um agente), ajuste a política,
add/remove allowlist patterns, então **Salvar**. A interface mostra **últimos metadados usados**
por padrão para que você possa manter a lista arrumada.

O selector de destino escolhe **Gateway** (aprovações locais) ou um **Node**. Nós
deve anunciar `system.execApprovals.get/set` (aplicativo macOS ou host de nó sem cabeça).
Se um nó ainda não anuncia aprovações exec, edite seu local
<<CODE1> directamente.

CLI: <<CODE0> suporta gateway ou edição de nós (ver [Aprovações CLI](/cli/approvals)].

# # Fluxo de aprovação

Quando um prompt é necessário, o gateway transmite <<CODE0> para clientes de operador.
O aplicativo Control UI e macOS resolvem-no via `exec.approval.resolve`, em seguida, o gateway avança o
pedido aprovado para o host do nó.

Quando são necessárias homologações, a ferramenta executiva retorna imediatamente com um ID de homologação. Use esse ID para
correlacionar os acontecimentos posteriores do sistema (`Exec finished`/ <CODE1>>). Se nenhuma decisão chegar antes do
tempo limite, a solicitação é tratada como um tempo limite de aprovação e aparece como uma razão de negação.

A janela de confirmação inclui:

- comando + args
- cwd
- agente id
- caminho executável resolvido
- host + metadados de política

Acções:

- ** Permita uma vez** → corra agora
- ** Sempre permitir** → adicionar para allowlist + executar
- **Deny** → block

# # Envio de aprovação para canais de chat

Você pode enviar prompts de aprovação executiva para qualquer canal de chat (incluindo canais de plugins) e aprovar
com `/approve`. Isto usa o oleoduto de entrega normal.

Configuração:

```json5
{
  approvals: {
    exec: {
      enabled: true,
      mode: "session", // "session" | "targets" | "both"
      agentFilter: ["main"],
      sessionFilter: ["discord"], // substring or regex
      targets: [
        { channel: "slack", to: "U12345678" },
        { channel: "telegram", to: "123456789" },
      ],
    },
  },
}
```

Responder no chat:

```
/approve <id> allow-once
/approve <id> allow-always
/approve <id> deny
```

## # macOS IPC fluir

```
Gateway -> Node Service (WS)
                 |  IPC (UDS + token + HMAC + TTL)
                 v
             Mac App (UI + approvals + system.run)
```

Notas de segurança:

- Modo de tomada Unix `0600`, token armazenado em `exec-approvals.json`.
- Verificação por pares do mesmo UID.
- Desafio/resposta (nonce + HMAC token + request hash) + TTL curto.

# # Eventos do sistema

O ciclo de vida do Exec é emergido como mensagens do sistema:

- `Exec running` (apenas se o comando exceder o limiar de aviso de execução)
- <<CODE1>
- <<CODE2>

Estas são postadas na sessão do agente após o nó relatar o evento.
As homologações de gateway-host exec emitem os mesmos eventos de ciclo de vida quando o comando termina (e opcionalmente quando se excede o limite).
Os executivos aprovados reutilizam o ID de aprovação como o `runId` nestas mensagens para facilitar a correlação.

# # Implicações

- **full** é poderoso; prefira allowlists quando possível.
- **ask** mantém você informado enquanto ainda permite aprovações rápidas.
- As listas de autorizações por agente impedem que as aprovações de um agente vazem para outros.
- As aprovações aplicam-se apenas aos pedidos executivos de host de ** remetentes autorizados**. Os remetentes não autorizados não podem emitir `/exec`.
- <<CODE1> é uma conveniência de nível de sessão para operadores autorizados e ignora aprovações por projeto.
Para o exercício de host de bloqueio rígido, configure a segurança das aprovações para `deny` ou negue a ferramenta `exec` via política de ferramentas.

Relacionados:

- [Ferramenta Exec] (</tools/exec)
- [Modo elevado] (</tools/elevated)
- [Skills] (</tools/skills)
