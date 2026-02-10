---
summary: "How OpenClaw presence entries are produced, merged, and displayed"
read_when:
  - Debugging the Instances tab
  - Investigating duplicate or stale instance rows
  - Changing gateway WS connect or system-event beacons
---

Presença

OpenClaw “presença” é uma visão leve, melhor-esforço de:

- o próprio **Gateway**, e
- **clientes conectados ao Gateway** (mac app, WebChat, CLI, etc.)

Presença é usada principalmente para renderizar o app do macOS **Instances** tab and to
fornecer visibilidade rápida do operador.

## Campos de presença (o que aparece)

Entradas de presença são objetos estruturados com campos como:

-`instanceId`(opcional mas fortemente recomendado): identidade estável do cliente (geralmente`connect.client.instanceId`
-`host`: nome de hospedeiro amigo do homem
-`ip`: endereço IP do melhor esforço
-`version`: texto de versão do cliente
-`deviceFamily`/`modelIdentifier`: dicas de hardware
- CÓDIGO DE PTU7: CÓDIGO DE PTU8, CÓDIGO DE PTU9, CÓDIGO DE PTUX10, CÓDIGO DE PTU11, CÓDIGO DE PTU12, CÓDIGO DE PTU13, CÓDIGO DE PTU14, ...
-`connect.client.instanceId`5: “segundos desde a última entrada do utilizador” (se conhecido)
- CÓDIGO DE PTU16: CÓDIGO DE PTU17, CÓDIGO DE PTU18, CÓDIGO DE PTU19, CÓDIGO DE PTU20, ...
-`host`1: data da última actualização (ms desde a época)

## Produtores (de onde vem a presença)

Entradas de presença são produzidas por várias fontes e ** fusão**.

### 1) Entrada no portal

O Gateway sempre semeia uma entrada "self" na inicialização para que UI mostre o host gateway
mesmo antes de qualquer cliente se conectar.

### 2) WebSocket connect

Cada cliente WS começa com um pedido`connect`. No aperto de mão bem sucedido o
O portal aumenta a entrada de presença para essa ligação.

#### Porque os comandos CLI não aparecem

O CLI muitas vezes se conecta para comandos abreviados. Para evitar spamming o
Lista de instâncias,`client.mode === "cli"`é **not** transformado em uma entrada de presença.

## # 3)`system-event`beacons

Os clientes podem enviar faróis periódicos mais ricos através do método`system-event`. O mac
aplicativo usa isso para relatar o nome do host, IP e`lastInputSeconds`.

### 4) Nó conecta (papel: nó)

Quando um nó se conecta sobre o Gateway WebSocket com`role: node`, o Gateway
upserts uma entrada de presença para esse nó (mesmo fluxo como outros clientes WS).

## Mesclar + regras dedupe (por que`instanceId`importa)

As entradas de presença são armazenadas em um único mapa de memória:

- As inscrições são chaveadas por uma chave de **presença**.
- A melhor chave é um`instanceId`estável (do`connect.client.instanceId` que sobrevive reinicia.
- As chaves são insensíveis.

Se um cliente reconectar sem um`instanceId`estável, ele pode aparecer como um
**duplicate** row.

## TTL e tamanho limitado

A presença é intencionalmente efêmera:

- ** TTL:** as entradas com mais de 5 minutos são podadas
- ** Entradas máximas:** 200 (o mais antigo caiu primeiro)

Isto mantém a lista fresca e evita o crescimento ilimitado da memória.

## Caverna remota/túnel (IPs de retrocesso)

Quando um cliente se conecta sobre um túnel SSH / porta local para frente, o Gateway pode
ver o endereço remoto como`127.0.0.1`. Para evitar sobrescrever um bom cliente
IP, endereços remotos loopback são ignorados.

## Consumidores

Página do macOS

O aplicativo macOS renderiza a saída de`system-presence`e aplica um pequeno status
indicador (Ativo/Ocioso/Estado) com base na idade da última atualização.

## Dicas de depuração

- Para ver a lista crua, chame`system-presence`contra o Gateway.
- Se vir duplicados:
- confirmar clientes enviar um`client.instanceId`estável no aperto de mão
- confirmar que os faróis periódicos utilizam o mesmo`instanceId`- verificar se falta a entrada derivada da ligação`instanceId`(esperam-se duplicados)
