---
summary: "Refactor plan: exec host routing, node approvals, and headless runner"
read_when:
  - Designing exec host routing or exec approvals
  - Implementing node runner + UI IPC
  - Adding exec host security modes and slash commands
---

# Plano de refatoração da máquina Exec

# # Objetivos

- Adicionar `exec.host` + `exec.security` à execução de rota através de **sandbox**, **gateway** e **node**.
- Manter predefinições **safe**: nenhuma execução cross-host a menos que explicitamente habilitada.
- Dividir execução em um serviço de corredor ** sem cabeça** com UI opcional (macOS app) via IPC local.
- Fornecer **per-agent** policy, allowlist, ask mode, and node binding.
- Suporte **ask modes** que funcionam  com  ou  sem  allowlists.
- Plataforma cruzada: Soquete Unix + autenticação token (paridade macOS/Linux/Windows).

# # Não-objetivos

- Nenhuma migração legada ou suporte a esquemas legados.
- Sem PTY/streaming para exec de nó (apenas saída agregada).
- Nenhuma nova camada de rede além da Ponte + Gateway existente.

# # Decisões (trancadas)

- ** Teclas de confirmação:** `exec.host` + `exec.security` (per-agente permitido).
- **Elevação:** manter `/elevated` como alias para acesso total ao gateway.
- ** Pergunta por omissão:** `on-miss`.
- ** Armazenagem de homologações:** `~/.openclaw/exec-approvals.json` (JSON, nenhuma migração de legados).
- **Runner:** serviço de sistema sem cabeça; aplicativo UI hospeda um soquete Unix para aprovações.
- **Node identity:** use existent `nodeId`.
- **Socket auth: ** Soquete Unix + token (cross-platform); dividido mais tarde, se necessário.
- **Node host state:** `~/.openclaw/node.json` (node id + token).
- ** macOS execu host:** execute `system.run` dentro do aplicativo macOS; node host service forwards requests over local IPC.
- ** Nenhum ajudante XPC:** fique com o soquete Unix + token + checks peer.

# # Conceitos-chave

Anfitrião

- <<CODE0>: Docker exec (comportamento atual).
- <<CODE1>: exec na máquina de gateway.
- `node`: exec no corredor de nó via Bridge (`system.run`).

# # Modo de segurança

- <<CODE0>: bloquear sempre.
- <<CODE1>: permitir apenas correspondências.
- <<CODE2>: permitir tudo (equivalente ao elevado).

# # # Perguntar modo

- <<CODE0>: nunca pergunte.
- <<CODE1>: perguntar apenas quando a allowlist não corresponder.
- <<CODE2>: perguntar sempre.

Ask é **independente** de allowlist; a allowlist pode ser usada com `always` ou `on-miss`.

## # Resolução política (por exec)

1. Resolver `exec.host` (tool param → agente sobreposição → padrão global).
2. Resolver `exec.security` e `exec.ask` (mesma precedência).
3. Se o hospedeiro for `sandbox`, prossiga com o executivo local sandbox.
4. Se o host for `gateway` ou `node`, aplique a política de segurança + pedir nesse host.

# # Segurança padrão

- Padrão `exec.host = sandbox`.
- Padrão `exec.security = deny` para `gateway` e `node`.
- Padrão `exec.ask = on-miss` (só relevante se a segurança permitir).
- Se nenhuma ligação de nó estiver definida, **o agente pode direcionar qualquer nó**, mas somente se a política permitir.

# # Superfície de configuração

## # Parâmetros da ferramenta

- `exec.host` (opcional): `sandbox | gateway | node`.
- `exec.security` (opcional): `deny | allowlist | full`.
- `exec.ask` (opcional): `off | on-miss | always`.
- `exec.node` (opcional): id/nome do nó a utilizar quando `host=node`.

Teclas de configuração (global)

- <<CODE0>
- <<CODE1>
- <<CODE2>
- <<CODE3> (ligação por defeito)

Teclas de configuração (por agente)

- <<CODE0>
- <<CODE1>
- <<CODE2>
- `agents.list[].tools.exec.node`

Apelido

- <<CODE0> = conjunto `tools.exec.host=gateway`, `tools.exec.security=full` para a sessão do agente.
- `/elevated off` = restaurar as configurações exec anteriores para a sessão do agente.

# # Loja de aprovações (JSON)

Localização: <<CODE0>

Objectivo:

- Política local + allowlists para o host ** execução** (gateway ou corredor de nó).
- Pergunta quando não houver UI.
Credenciais IPC para clientes de UI.

Esquema proposto (v1):

```json
{
  "version": 1,
  "socket": {
    "path": "~/.openclaw/exec-approvals.sock",
    "token": "base64-opaque-token"
  },
  "defaults": {
    "security": "deny",
    "ask": "on-miss",
    "askFallback": "deny"
  },
  "agents": {
    "agent-id-1": {
      "security": "allowlist",
      "ask": "on-miss",
      "allowlist": [
        {
          "pattern": "~/Projects/**/bin/rg",
          "lastUsedAt": 0,
          "lastUsedCommand": "rg -n TODO",
          "lastResolvedPath": "/Users/user/Projects/.../bin/rg"
        }
      ]
    }
  }
}
```

Notas:

- Nenhum formato legado.
- `askFallback` aplica-se apenas quando <<CODE1> é necessário e não é possível aceder a IU.
- Permissões do arquivo: `0600`.

# # Serviço de corredor (sem cabeça)

Papel

- Aplicar localmente <<CODE0> + <<CODE1>.
- Execute comandos de sistema e retorno de saída.
- Emit Bridge eventos para o ciclo de vida exec (opcional, mas recomendado).

Ciclo de vida de serviço

- Lançado/daemon no serviço de sistema macOS; no Linux/Windows.
- Aprovações JSON é local do anfitrião de execução.
- UI hospeda um soquete Unix local; os corredores se conectam sob demanda.

## Integração de IU (aplicativo macOS)

IPC

- Soquete Unix em <<CODE0> (0600).
- Token armazenado em <<CODE1> (0600).
- Cheques de pares: só com UID.
- Desafio/resposta: nonce + HMAC (token, request-hash) para evitar replay.
- TTL curto (por exemplo, 10s) + carga útil máxima + limite de taxa.

## # Perguntar fluxo (macOS app exec host)

1. O serviço de nós recebe `system.run` do portal.
2. O serviço de nós conecta-se ao soquete local e envia o pedido prompt/exec.
3. App valida peer + token + HMAC + TTL, então mostra o diálogo se necessário.
4. App executa o comando em contexto UI e retorna saída.
5. O serviço de nós devolve a saída ao gateway.

Se a UI faltar:

- Aplicar `askFallback` (`deny|allowlist|full`).

Diagrama (SCI)

```
Agent -> Gateway -> Bridge -> Node Service (TS)
                         |  IPC (UDS + token + HMAC + TTL)
                         v
                     Mac App (UI + TCC + system.run)
```

# # Identidade do nó + ligação

- Use o <<CODE0> existente do emparelhamento Bridge.
- Modelo de ligação:
- <<CODE1> restringe o agente a um nó específico.
- Se não estiver definido, o agente pode escolher qualquer nó (a política ainda obriga os padrões).
- Resolução de seleção de nós:
- <<CODE2> correspondência exacta
- `displayName` (normalizado)
- `remoteIp`
- prefixo <<CODE5> (>= 6 caracteres)

# # Eventos

# # Que vê eventos

- Os eventos do sistema são **por sessão** e mostrados ao agente no próximo prompt.
- Armazenado na fila da memória de gateway (<`enqueueSystemEvent`).

Texto do evento

- <<CODE0>
- `Exec finished (node=<id>, id=<runId>, code=<code>)` + cauda de saída opcional
- <<CODE2>

Transporte

Opção A (recomendada):

- Runner envia Ponte `event` quadros `exec.started` / `exec.finished`.
- Gateway <<CODE3> mapeia estes em `enqueueSystemEvent`.

Opção B:

- Gateway <<CODE0> lida com o ciclo de vida diretamente (síncrono apenas).

# # Fluxos de exercício

Hospedeiro da caixa de areia

- Comportamento existente `exec` (Docker ou host quando não está a salvo).
- PTY suportado apenas no modo não-sandbox.

Hospedeiro da porta

- O processo Gateway é executado na sua própria máquina.
- Força local `exec-approvals.json` (segurança/perguntas/allowlist).

# # Node host

- Chamadas de porta `node.invoke` com `system.run`.
- O corredor aplica aprovações locais.
- Runner retorna stdout/stderr agregado.
- Opcional Ponte eventos para início/terminação/negação.

# # Tampas de saída

- Cap combinado stdout+stderr em **200k**; manter **tail 20k** para eventos.
- Truncar com um sufixo claro (por exemplo, `"… (truncated)"`).

# # Comandos de corte

- <<CODE0>
- Per-agent, por-sessão sobrepõe; não-persistente a menos que salvo via config.
- <<CODE1> continua a ser um atalho para `host=gateway security=full` (com `full` que ignora aprovações).

# # História entre plataformas

O serviço de corredor é o alvo de execução portátil.
- IU é opcional; se faltar, aplica-se `askFallback`.
- Windows/Linux suportam as mesmas aprovações protocolo JSON + soquete.

# # Fases de implementação

### Fase 1: configuração + encaminhamento executivo

- Adicionar esquema de configuração para `exec.host`, <CODE1>>, <CODE2>>, `exec.node`.
- Atualizar canalização ferramenta para respeitar `exec.host`.
- Adicionar comando `/exec` slash e manter `/elevated` alias.

### Fase 2: aprovações loja + aplicação de gateway

- Aplicar `exec-approvals.json` leitor/escritor.
- Enforce allowlist + pedir modos para `gateway` host.
- Adicione tampas de saída.

Fase 3: aplicação do corredor de nó

- Atualizar corredor de nó para impor allowlist + ask.
- Adicione Unix socket prompt bridge para o aplicativo macOS UI.
- Fio `askFallback`.

Fase 4: eventos

- Adicionar nó → gateway Ponte eventos para o ciclo de vida exec.
- Mapa para `enqueueSystemEvent` para as instruções do agente.

Fase 5: Polimento da IU

- Aplicativo Mac: editor allowlist, switcher per-agent, pedir UI política.
- Controlos vinculativos de nós (opcional).

# # Plano de testes

- Testes unitários: correspondência na lista de allowlists (glob + case-insensível).
- Testes unitários: precedência da resolução de políticas (tool param → agente sobreposição → global).
- Testes de integração: fluxos de negação/permissão/permissão.
- Testes de eventos de ponte: evento de nó → roteamento de eventos de sistema.

# # Riscos abertos

- Indisponibilidade de IU: garantir o respeito de `askFallback`.
- Comandos de longa duração: contar com tempo limite + caps de saída.
- Ambiguidade de múltiplos nós: erro a menos que a ligação de nós ou param de nó explícito.

# # Docs relacionados

- [Ferramenta Exec] (</tools/exec)
- [Aprovações exec] (</tools/exec-approvals)
- [Nos] (</nodes)
- [Modo elevado] (</tools/elevated)
