---
summary: "Gateway WebSocket protocol: handshake, frames, versioning"
read_when:
  - Implementing or updating gateway WS clients
  - Debugging protocol mismatches or connect failures
  - Regenerating protocol schema/models
---

# Protocolo Gateway (WebSocket)

O protocolo Gateway WS é o **plano de controle único + transporte de nós** para
Open Claw. Todos os clientes (CLI, UI web, app macOS, iOS/Android nós, sem cabeça
nós) conectar sobre WebSocket e declarar seu ** papel** + **scope** em
Hora do aperto de mão.

# # Transporte

WebSocket, quadros de texto com cargas JSON.
- Primeiro quadro **deve ser uma solicitação <<CODE0>>.

# # Aperto de mão (conectar)

Gateway → Cliente (desafio pré-conectar):

```json
{
  "type": "event",
  "event": "connect.challenge",
  "payload": { "nonce": "…", "ts": 1737264000000 }
}
```

Cliente → Gateway:

```json
{
  "type": "req",
  "id": "…",
  "method": "connect",
  "params": {
    "minProtocol": 3,
    "maxProtocol": 3,
    "client": {
      "id": "cli",
      "version": "1.2.3",
      "platform": "macos",
      "mode": "operator"
    },
    "role": "operator",
    "scopes": ["operator.read", "operator.write"],
    "caps": [],
    "commands": [],
    "permissions": {},
    "auth": { "token": "…" },
    "locale": "en-US",
    "userAgent": "openclaw-cli/1.2.3",
    "device": {
      "id": "device_fingerprint",
      "publicKey": "…",
      "signature": "…",
      "signedAt": 1737264000000,
      "nonce": "…"
    }
  }
}
```

Gateway → Cliente:

```json
{
  "type": "res",
  "id": "…",
  "ok": true,
  "payload": { "type": "hello-ok", "protocol": 3, "policy": { "tickIntervalMs": 15000 } }
}
```

Quando é emitido um símbolo de dispositivo, <<CODE0>> também inclui:

```json
{
  "auth": {
    "deviceToken": "…",
    "role": "operator",
    "scopes": ["operator.read", "operator.write"]
  }
}
```

# # # Exemplo de nós

```json
{
  "type": "req",
  "id": "…",
  "method": "connect",
  "params": {
    "minProtocol": 3,
    "maxProtocol": 3,
    "client": {
      "id": "ios-node",
      "version": "1.2.3",
      "platform": "ios",
      "mode": "node"
    },
    "role": "node",
    "scopes": [],
    "caps": ["camera", "canvas", "screen", "location", "voice"],
    "commands": ["camera.snap", "canvas.navigate", "screen.record", "location.get"],
    "permissions": { "camera.capture": true, "screen.record": false },
    "auth": { "token": "…" },
    "locale": "en-US",
    "userAgent": "openclaw-ios/1.2.3",
    "device": {
      "id": "device_fingerprint",
      "publicKey": "…",
      "signature": "…",
      "signedAt": 1737264000000,
      "nonce": "…"
    }
  }
}
```

# # Framing

- **Pedido**: <<CODE0>>
- **Resposta**: <<CODE1>>
- **Evento**: <<CODE2>>

Métodos de efeito colateral requerem ** chaves de impotência** (ver esquema).

# # Funções + escopos

Funções

- <<CODE0>> = cliente de avião de controlo (CLI/UI/automação).
- <<CODE1>> = máquina de capacidade (câmera/tela/canvas/system.run).

### Escopo (operador)

Âmbitos comuns:

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>
- <<CODE3>>
- <<CODE4>>

## # Caps/commands/permissions (node)

Os nós declaram reivindicações de capacidade no momento da ligação:

- <<CODE0>>: categorias de capacidade de alto nível.
- <<CODE1>>: comando allowlist para invocar.
- <<CODE2>>: comutadores granulares (p. ex. <<CODE3>>, <<CODE4>>).

O Gateway trata estes como **afirma** e aplica a lista de allowlists do lado do servidor.

# # Presença

- <<CODE0> retorna entradas chaveadas pela identidade do dispositivo.
- As entradas de presença incluem <<CODE1>>, <<CODE2>>> e <<CODE3>> assim UIs pode mostrar uma única linha por dispositivo
mesmo quando se conecta como **operador** e **node**.

## # # Métodos de ajuda

- Os nós podem chamar <<CODE0>> para obter a lista atual de executáveis de habilidades
para verificação automática.

# # Aprovações exec

- Quando um pedido executivo precisa de aprovação, o gateway transmite <<CODE0>>>.
- Os clientes do operador resolvem chamando <<CODE1>> (requer <<CODE2>> escopo).

# # Versionamento

- <<CODE0> vive em <<CODE1>.
- Os clientes enviam <<CODE2>>> + <<CODE3>>>; o servidor rejeita incompatibilidades.
- Os esquemas + modelos são gerados a partir de definições TypeBox:
- <<CODE4>>
- <<CODE5>>
- <<CODE6>>

# # Auth

- Se <<CODE0> (ou <<CODE1>>) for definido, <<CODE2>>
deve corresponder ou a tomada está fechada.
- Após emparelhamento, o Gateway emite um token **dispositivo** escopo para a conexão
papel + escopos. É devolvido em <<CODE3>> e deve ser
persistido pelo cliente para futuras conexões.
- Os tokens dos dispositivos podem ser rodados/revogados via <<CODE4>> e
<<CODE5> (requer <<CODE6> escopo).

# # Identidade do dispositivo + emparelhamento

- Os nós devem incluir uma identidade estável do dispositivo (<<<CODE0>>>) derivada de uma
Impressões digitais de keypar.
- Gateways emitir fichas por dispositivo + papel.
- As aprovações de pareamento são necessárias para novas identificações do dispositivo, a menos que a auto-aprovação local
está activado.
- **As ligações locais** incluem o loopback e o endereço tailnet da própria máquina de gateway
(de modo que a mesma rede de cauda do hospedeiro ainda pode auto-aprovar).
- Todos os clientes WS devem incluir <<CODE1>> identidade durante <<CODE2>> (operador + nó).
A IU de controle pode omiti-la ** somente** quando <<CODE3>> estiver habilitada
(ou <<CODE4>> para utilização em vidro de ruptura).
- As conexões não locais devem assinar o servidor fornecido <<CODE5>>nonce.

# # TLS + pinning

- TLS é suportado para conexões WS.
- Os clientes podem opcionalmente fixar a impressão digital do certificado de gateway (ver <<CODE0>>
config plus <<CODE1>>ou CLI <<CODE2>>>).

# # Escopo

Este protocolo expõe a API **full gateway** (status, canais, modelos, chat,
agente, sessões, nós, aprovações, etc.). A superfície exacta é definida pela
Esquemas TypeBox em <<CODE0>>>.
