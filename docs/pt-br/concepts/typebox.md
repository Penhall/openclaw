---
summary: "TypeBox schemas as the single source of truth for the gateway protocol"
read_when:
  - Updating protocol schemas or codegen
---

# TypeBox como fonte de protocolo de verdade

Última atualização: 2026-01-10

TypeBox é uma biblioteca de esquemas TypeScript-first. Usamo-lo para definir o **Gateway
WebSocket protocol** (handshake, request/response, server events). Esses esquemas.
** validação de tempo de execução**, ** exportação de esquema JSON**, e ** codegen Swift** para
A aplicação macOS. Uma fonte de verdade; tudo o mais é gerado.

Se quiser o contexto de protocolo de nível superior, comece com
[Arquitectura do portal] /concepts/architecture.

## Modelo mental (30 segundos)

Cada mensagem WS Gateway é um dos três quadros:

- **Pedido**:`{ type: "req", id, method, params }`- **Resposta**:`{ type: "res", id, ok, payload | error }`- **Evento**:`{ type: "event", event, payload, seq?, stateVersion? }`

O primeiro quadro **deve ser uma solicitação`connect`. Depois disso, os clientes podem chamar
métodos (por exemplo,`health`,`send`,`chat.send` e subscrever eventos (por exemplo,`presence`,`tick`,`agent`.

Fluxo de ligação (mínimo):

```
Client                    Gateway
  |---- req:connect -------->|
  |<---- res:hello-ok --------|
  |<---- event:tick ----------|
  |---- req:health ---------->|
  |<---- res:health ----------|
```

Métodos comuns + acontecimentos:

Exemplos de Categoria
---------- ---------------------------------------------------------------------------------------------------
OUTXCODE0 ,`health`,`status`,`connect`deve ser o primeiro
OUTXCODE4,`poll`,`agent`,`agent.wait`. Os efeitos secundários necessitam de`idempotencyKey`.`chat.history`;`health`0;`health`1;`health`2; WebChat usa estes
Sessões`health`3,`health`4,`health`5`health`6,`health`7,`health`8`health`9,`status`0,`status`1,`status`2,`status`3,`status`4

A lista autorizativa vive em`src/gateway/server.ts``METHODS`,`EVENTS`.

## Onde vivem os esquemas

- Fonte:`src/gateway/protocol/schema.ts`- Validadores de tempo de execução (AJV):`src/gateway/protocol/index.ts`- Servidor aperto de mão + despacho método:`src/gateway/server.ts`- Cliente de nós:`src/gateway/client.ts`- Esquema JSON gerado:`dist/protocol.schema.json`- Modelos Swift Gerados:`apps/macos/Sources/OpenClawProtocol/GatewayModels.swift`

## Oleoduto atual

-`pnpm protocol:gen`- escreve JSON Schema (draft-07) ao`dist/protocol.schema.json`-`pnpm protocol:gen:swift`- gera modelos de gateway Swift
-`pnpm protocol:check`- executa ambos os geradores e verifica a saída está comprometida

## Como os esquemas são usados em tempo de execução

- **Lado do servidor**: cada quadro de entrada é validado com AJV. Apenas o aperto de mão
aceita um pedido`connect`cujos parâmetros correspondam ao`ConnectParams`.
- ** Lado do cliente**: o cliente JS valida quadros de eventos e respostas antes
a usá-los.
- ** Superfície dométodo**: o Gateway anuncia o`methods`suportado e`events`em`hello-ok`.

## Quadros de exemplo

Ligar (primeira mensagem):

```json
{
  "type": "req",
  "id": "c1",
  "method": "connect",
  "params": {
    "minProtocol": 2,
    "maxProtocol": 2,
    "client": {
      "id": "openclaw-macos",
      "displayName": "macos",
      "version": "1.0.0",
      "platform": "macos 15.1",
      "mode": "ui",
      "instanceId": "A1B2"
    }
  }
}
```

Olá-ok resposta:

```json
{
  "type": "res",
  "id": "c1",
  "ok": true,
  "payload": {
    "type": "hello-ok",
    "protocol": 2,
    "server": { "version": "dev", "connId": "ws-1" },
    "features": { "methods": ["health"], "events": ["tick"] },
    "snapshot": {
      "presence": [],
      "health": {},
      "stateVersion": { "presence": 0, "health": 0 },
      "uptimeMs": 0
    },
    "policy": { "maxPayload": 1048576, "maxBufferedBytes": 1048576, "tickIntervalMs": 30000 }
  }
}
```

Pedido + resposta:

```json
{ "type": "req", "id": "r1", "method": "health" }
```

```json
{ "type": "res", "id": "r1", "ok": true, "payload": { "ok": true } }
```

Evento:

```json
{ "type": "event", "event": "tick", "payload": { "ts": 1730000000 }, "seq": 12 }
```

## Cliente mínimo (Node.js)

Fluxo útil mais pequeno: conectar + saúde.

```ts
import { WebSocket } from "ws";

const ws = new WebSocket("ws://127.0.0.1:18789");

ws.on("open", () => {
  ws.send(
    JSON.stringify({
      type: "req",
      id: "c1",
      method: "connect",
      params: {
        minProtocol: 3,
        maxProtocol: 3,
        client: {
          id: "cli",
          displayName: "example",
          version: "dev",
          platform: "node",
          mode: "cli",
        },
      },
    }),
  );
});

ws.on("message", (data) => {
  const msg = JSON.parse(String(data));
  if (msg.type === "res" && msg.id === "c1" && msg.ok) {
    ws.send(JSON.stringify({ type: "req", id: "h1", method: "health" }));
  }
  if (msg.type === "res" && msg.id === "h1") {
    console.log("health:", msg.payload);
    ws.close();
  }
});
```

## Exemplo trabalhado: adicionar um método de ponta a ponta

Exemplo: adicione uma nova solicitação`system.echo`que retorna`{ ok: true, text }`.

1. **Schema (fonte da verdade)**

Adicionar ao`src/gateway/protocol/schema.ts`:

```ts
export const SystemEchoParamsSchema = Type.Object(
  { text: NonEmptyString },
  { additionalProperties: false },
);

export const SystemEchoResultSchema = Type.Object(
  { ok: Type.Boolean(), text: NonEmptyString },
  { additionalProperties: false },
);
```

Adicionar tanto ao`ProtocolSchemas`quanto aos tipos de exportação:

```ts
  SystemEchoParams: SystemEchoParamsSchema,
  SystemEchoResult: SystemEchoResultSchema,
```

```ts
export type SystemEchoParams = Static<typeof SystemEchoParamsSchema>;
export type SystemEchoResult = Static<typeof SystemEchoResultSchema>;
```

2. **Validação **

Em`src/gateway/protocol/index.ts`, exporte um validador AJV:

```ts
export const validateSystemEchoParams = ajv.compile<SystemEchoParams>(SystemEchoParamsSchema);
```

3. ** Comportamento do servidor**

Adicionar um manipulador no`src/gateway/server-methods/system.ts`:

```ts
export const systemHandlers: GatewayRequestHandlers = {
  "system.echo": ({ params, respond }) => {
    const text = String(params.text ?? "");
    respond(true, { ok: true, text });
  },
};
```

Registre-o no`src/gateway/server-methods.ts`(já funde`systemHandlers`,
Em seguida, adicione`"system.echo"`ao`METHODS`no`src/gateway/server.ts`.

4. **Regenerar **

```bash
pnpm protocol:check
```

5. ** Testes + documentos

Adicione um teste de servidor em`src/gateway/server.*.test.ts`e observe o método em docs.

## Comportamento de codegen rápido

O gerador Swift emite:

-`GatewayFrame`enum com os casos`req`,`res`,`event`e`unknown`- structs/enums da carga útil fortemente digitados
- valores`ErrorCode`e`GATEWAY_PROTOCOL_VERSION`

Tipos de quadros desconhecidos são preservados como cargas brutas para compatibilidade com o futuro.

## Versionamento + compatibilidade

-`PROTOCOL_VERSION`vive em`src/gateway/protocol/schema.ts`.
- Os clientes enviam`minProtocol`+`maxProtocol`; o servidor rejeita incompatibilidades.
- Os modelos Swift mantêm tipos de quadros desconhecidos para evitar quebrar clientes mais velhos.

## Esquema padrões e convenções

- A maioria dos objetos usa`additionalProperties: false`para cargas rígidas.
-`NonEmptyString`é o padrão para IDs e nomes de método/evento.
- O`GatewayFrame`de alto nível utiliza um **discriminador** em`type`.
- Métodos com efeitos secundários geralmente requerem um`idempotencyKey`em parâmetros
(exemplo:`send`,`poll`,`agent`,`chat.send`.

## Esquema vivo JSON

Gerado JSON Schema está no repo em`dist/protocol.schema.json`. A
arquivo bruto publicado está tipicamente disponível em:

- https://raw.githubusercontent.com/openclaw/openclaw/main/dist/protocol.schema.json

## Quando mudas de esquema

1. Atualizar os esquemas TypeBox.
2. Executar`pnpm protocol:check`.
3. Cometer o esquema regenerado + modelos Swift.
