---
summary: "Exec tool usage, stdin modes, and TTY support"
read_when:
  - Using or modifying the exec tool
  - Debugging stdin or TTY behavior
---

Ferramenta Exec

Executar comandos de shell na área de trabalho. Suporta primeiro plano + execução de fundo via `process`.
Se <<CODE1> for proibido, <<CODE2> é executado síncrono e ignora `yieldMs`/<CODE4>>.
As sessões de fundo são exploradas por agente; `process` somente vê sessões do mesmo agente.

# # Parâmetros

- <<CODE0> (obrigatório)
- <<CODE1> (por omissão para cwd)
- <<CODE2> (substitui a chave/valor)
- <<CODE3> (padrão 10000): auto-background após atraso
- <<CODE4> (bool): fundo imediatamente
- <<CODE5> (segundos, por omissão 1800): kill na expiração
- <<CODE6> (bool): correr num pseudo-terminal quando disponível (CLIs, agentes codificadores, UI terminal)
- `host` (`sandbox | gateway | node`): onde executar
- `security` (`deny | allowlist | full`): modo de execução para `gateway`/`node`
- <<CODE13> (`off | on-miss | always`): avisos de aprovação para `gateway`/<<CODE16>
- <<CODE17> (cadeia): nome/id do nó para `host=node`
- `elevated` (bool): modo de pedido elevado (host de porta); `security=full` só é forçado quando a resolução elevada é `full`

Notas:

- <<CODE0> por omissão <<CODE1>.
- <<CODE2> é ignorado quando o sandboxing está desligado (exec já roda no host).
- <<CODE3>/`node` as aprovações são controladas por `~/.openclaw/exec-approvals.json`.
- <<CODE6> requer um nó emparelhado (aplicativo de companhia ou host de nó sem cabeça).
- Se estiverem disponíveis múltiplos nós, definir `exec.node` ou `tools.exec.node` para seleccionar um.
- Nos anfitriões não-Windows, o executivo usa `SHELL` quando definido; se `SHELL` for `fish`, prefere `bash` (ou `sh`)
A partir de <<CODE14> para evitar scripts incompatíveis com peixes, então cai para `SHELL` se nenhum deles existir.
- Importante: sandboxing is **off by default**. Se a caixa de areia estiver desligada, `host=sandbox` roda diretamente sobre
o host gateway (sem contêiner) e ** não requer aprovações**. Para exigir aprovações,
`host=gateway` e configurar aprovações executivas (ou ativar sandboxing).

Configuração

- `tools.exec.notifyOnExit` (padrão: true): quando true, as sessões executivas de fundo enqueam um evento do sistema e pedem um batimento cardíaco na saída.
- <<CODE1> (por omissão: 10000): emitir um único aviso de "correção" quando um executivo com a homologação for superior a este (0 desactiva).
- <<CODE2> (por omissão: `sandbox`)
- `tools.exec.security` (por omissão: `deny` para sandbox, `allowlist` para gateway + nó quando desactivado)
- `tools.exec.ask` (por omissão: `on-miss`)
- `tools.exec.node` (padrão: não definido)
- `tools.exec.pathPrepend`: lista de pastas a preparar para `PATH` para execução.
- `tools.exec.safeBins`: binários seguros apenas de stdin que podem ser executados sem entradas explícitas na lista de permissões.

Exemplo:

```json5
{
  tools: {
    exec: {
      pathPrepend: ["~/bin", "/opt/oss/bin"],
    },
  },
}
```

Manuseio do caminho

- `host=gateway`: funde o seu login-shell `PATH` no ambiente exec (a menos que a chamada executiva
já define `env.PATH`). O próprio daemon ainda é executado com um mínimo `PATH`:
- macOS: `/opt/homebrew/bin`, `/usr/local/bin`, `/usr/bin`, `/bin`
- Linux: `/usr/local/bin`, `/usr/bin`, `/bin`
- `host=sandbox`: corre `sh -lc` (concha de logina) dentro do recipiente, pelo que `/etc/profile` pode reiniciar `PATH`.
OpenClaw prepreends `env.PATH` após o fornecimento de perfil através de um env var interno (sem interpolação shell);
<<CODE16> também se aplica aqui.
- `host=node`: apenas o env sobrepõe-se ao nó. <<CODE18> só se aplica
Se a chamada executiva já definir `env.PATH`. Hosts de nós sem cabeça aceitam <<CODE20> somente quando se prepara
o nó PATH da máquina (sem substituição). A queda de nós macOS <<CODE21> > substitui inteiramente.

Ligação de nó por agente (use o índice da lista de agentes na configuração):

```bash
openclaw config get agents.list
openclaw config set agents.list[0].tools.exec.node "node-id-or-name"
```

UI de controle: a aba Nós inclui um pequeno painel de "ligação de nó Exec" para as mesmas configurações.

# # A sessão substitui (`/exec`)

Utilizar `/exec` para definir **por sessão** defaults para `host`, `security`, `ask` e `node`.
Enviar `/exec` sem argumentos para mostrar os valores atuais.

Exemplo:

```
/exec host=gateway security=allowlist ask=on-miss node=mac-1
```

# # Modelo de autorização

`/exec` é honrado apenas por ** remetentes autorizados** (canal allowlists/pairing plus `commands.useAccessGroups`).
Ele atualiza **session state only** e não escreve config. Para desactivar o executivo, negue-o através da ferramenta
política (`tools.deny: ["exec"]` ou por agente). As aprovações da máquina ainda se aplicam, a menos que esteja explicitamente definido
`security=full` e `ask=off`.

# # Aprovações Exec (aplicativo de companhia / host de nós)

Agentes sandboxed podem exigir aprovação por solicitação antes de <<CODE0> correr no gateway ou host de nó.
Ver [Aprovações exec](</tools/exec-approvals) para a política, lista de licenças e fluxo de IU.

Quando são necessárias homologações, a ferramenta executiva retorna imediatamente com
`status: "approval-pending"` e um ID de aprovação. Uma vez aprovado (ou negado / cronometrado),
o Gateway emite eventos do sistema (`Exec finished`/ <CODE2>>). Se o comando ainda estiver
Após <<CODE3>, é emitido um único aviso `Exec running`.

# # Allowlist + caixas seguras

Allowlist executing coincide com ** caminhos binários resolvidos apenas** (sem partidas de base). Quando
`security=allowlist`, comandos shell são autorizados automaticamente apenas se cada segmento de tubulação for
allowlist ou uma caixa segura. O encadeamento (`;`, <CODE2>>, <CODE3>>) e os redirecionamentos são rejeitados em
modo allowlist.

# # Exemplos

Primeiro plano:

```json
{ "tool": "exec", "command": "ls -la" }
```

Contexto + sondagem:

```json
{"tool":"exec","command":"npm run build","yieldMs":1000}
{"tool":"process","action":"poll","sessionId":"<id>"}
```

Enviar chaves (estilo tmux):

```json
{"tool":"process","action":"send-keys","sessionId":"<id>","keys":["Enter"]}
{"tool":"process","action":"send-keys","sessionId":"<id>","keys":["C-c"]}
{"tool":"process","action":"send-keys","sessionId":"<id>","keys":["Up","Up","Enter"]}
```

Enviar (enviar apenas CR):

```json
{ "tool": "process", "action": "submit", "sessionId": "<id>" }
```

Colar (bracked por padrão):

```json
{ "tool": "process", "action": "paste", "sessionId": "<id>", "text": "line1\nline2\n" }
```

## appl patch (experimental)

<<CODE0> é uma subferramenta de `exec` para edições estruturadas de vários arquivos.
Activar explicitamente:

```json5
{
  tools: {
    exec: {
      applyPatch: { enabled: true, allowModels: ["gpt-5.2"] },
    },
  },
}
```

Notas:

- Apenas disponível para modelos OpenAI/OpenAI Codex.
- Política de ferramenta ainda se aplica; `allow: ["exec"]` implicitamente permite `apply_patch`.
- A configuração vive em `tools.exec.applyPatch`.
