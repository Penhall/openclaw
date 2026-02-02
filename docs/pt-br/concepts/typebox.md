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
[Arquitetura do portal](<<<LINK0>>>).

# # Modelo mental (30 segundos)

Cada mensagem WS Gateway é um dos três quadros:

- **Pedido**: <<CODE0>>
- **Resposta**: <<CODE1>>
- **Evento**: <<CODE2>>

O primeiro quadro **deve ser uma solicitação <<CODE0>>. Depois disso, os clientes podem chamar
métodos (p. ex. <<CODE1>>>, <HTML2>>>, <HTML3>>>>) e subscrever eventos (p. ex.
<<CODE4>>, <<CODE5>>, <<CODE6>>).

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
O núcleo deve ser o primeiro.
* Mensagens < <<CODE4>>>, <<CODE5>>, <<CODE6>>, <<CODE7>>
Conversar com <<CODE9>>, <<CODE10>>, <<CODE11>, <<CODE12>> O WebChat usa estes
Sessões < <<CODE13>>, <<CODE14>>, <<CODE15>> administrador de sessão .
□ Nós <<CODE16>>, <<CODE17>>, <<CODE18>> Gateway WS + ações de nó
Acontecimentos < <<CODE19>>, <<CODE20>>, <<CODE21>>, <<CODE22>>, <<CODE23>>, <<CODE24>> Servidor de servidor de push

A lista de autores vive em <<CODE0>> (<<CODE1>>, <<CODE2>>).

# # Onde vivem os esquemas

- Fonte: <<CODE0>>
- Validadores de tempo de execução (AJV): <<CODE1>>
- Aperto de mão do servidor + expedição do método: <<CODE2>>
- Cliente de nós: <<CODE3>>>
- Esquema JSON gerado: <<CODE4>>
- Modelos Swift gerados: <<CODE5>>

# # Oleoduto atual

- <<CODE0>>
- escreve JSON Schema (draft-07) para <<CODE1>>
- <<CODE2>>
- gera modelos de gateway Swift
- <<CODE3>>
- executa ambos os geradores e verifica a saída está comprometida

# # Como os esquemas são usados em tempo de execução

- **Lado do servidor**: cada quadro de entrada é validado com AJV. Apenas o aperto de mão
aceita uma solicitação <<CODE0>> cujos parâmetros correspondem a <<CODE1>>>.
- ** Lado do cliente**: o cliente JS valida quadros de eventos e respostas antes
a usá-los.
- ** Superfície do método**: o Gateway anuncia o suporte <<CODE2>> e
<<CODE3>> em <HTML4>>>.

# # Quadros de exemplo

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

# # Cliente mínimo (Node.js)

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

# # Exemplo trabalhado: adicionar um método de ponta a ponta

Exemplo: adicione uma nova solicitação <<CODE0>> que retorna <<CODE1>>.

1. **Schema (fonte da verdade)**

Adicionar a <<CODE0>>:

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

Adicionar ambos aos tipos <<CODE0>> e de exportação:

```ts
  SystemEchoParams: SystemEchoParamsSchema,
  SystemEchoResult: SystemEchoResultSchema,
```

```ts
export type SystemEchoParams = Static<typeof SystemEchoParamsSchema>;
export type SystemEchoResult = Static<typeof SystemEchoResultSchema>;
```

2. **Validação **

Em <<CODE0>>, exportar um validador AJV:

```ts
export const validateSystemEchoParams = ajv.compile<SystemEchoParams>(SystemEchoParamsSchema);
```

3. ** Comportamento do servidor**

Adicionar um manipulador em <<CODE0>>:

```ts
export const systemHandlers: GatewayRequestHandlers = {
  "system.echo": ({ params, respond }) => {
    const text = String(params.text ?? "");
    respond(true, { ok: true, text });
  },
};
```

Registre-o em <<CODE0>> (já funde <<CODE1>>),
em seguida, adicionar <<CODE2>> a <<CODE3>> em <<CODE4>>.

4. **Regenerar **

```bash
pnpm protocol:check
```

5. ** Testes + documentos

Adicione um teste de servidor em <<CODE0>> e observe o método em docs.

# # Comportamento de codegen rápido

O gerador Swift emite:

- <<CODE0>> enum com <<CODE1>>, <<CODE2>>, <<CODE3>>, e <<CODE4>>> casos
- structs/enums da carga útil fortemente digitados
- <<CODE5> valores e <<CODE6>>

Tipos de quadros desconhecidos são preservados como cargas brutas para compatibilidade com o futuro.

# # Versionamento + compatibilidade

- <<CODE0> vive em <<CODE1>.
- Os clientes enviam <<CODE2>>> + <<CODE3>>>; o servidor rejeita incompatibilidades.
- Os modelos Swift mantêm tipos de quadros desconhecidos para evitar quebrar clientes mais velhos.

# # Esquema padrões e convenções

- A maioria dos objetos usa <<CODE0>> para cargas rígidas.
- <<CODE1> é o padrão para IDs e nomes de método/evento.
- O nível superior <<CODE2>> utiliza um **discriminador** em <<CODE3>>.
- Métodos com efeitos secundários requerem geralmente um <<CODE4> em parâmetros
(exemplo: <<CODE5>>, <<CODE6>>, <<CODE7>>, <<CODE8>>).

# # Esquema vivo JSON

O esquema gerado de JSON está no repo em <<CODE0>>>. A
arquivo bruto publicado está tipicamente disponível em:

- https://raw.githubusercontent.com/openclaw/openclaw/main/dist/protocol.schema.json

# # Quando mudas de esquema

1. Atualizar os esquemas TypeBox.
2. Executar <<CODE0>>>.
3. Cometer o esquema regenerado + modelos Swift.
