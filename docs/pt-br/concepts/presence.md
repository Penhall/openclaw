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

# # Campos de presença (o que aparece)

Entradas de presença são objetos estruturados com campos como:

- <<CODE0> (opcional, mas fortemente recomendada): identidade estável do cliente (geralmente <<CODE1>>>)
- <<CODE2>: nome de hospedeira amigo do ser humano
- <<CODE3>>: endereço IP do melhor esforço
- <<CODE4>: string de versão cliente
- <<CODE5>/ <<CODE6>>: dicas de hardware
- <<CODE7>>: <<CODE8>>, <<CODE9>>, <<CODE10>>, <<CODE11>>, <<CODE12>>, <<CODE13>>, <<CODE14>>, ...
- <<CODE15>>: “segundos desde a última entrada do utilizador” (se conhecido)
- <<CODE16>>: <<CODE17>>, <<CODE18>>, <<CODE19>>, <<CODE20>>, ...
- <<CODE21>>: data da última actualização (ms desde a época)

# # Produtores (de onde vem a presença)

Entradas de presença são produzidas por várias fontes e ** fusão**.

### 1) Entrada no portal

O Gateway sempre semeia uma entrada "self" na inicialização para que UI mostre o host gateway
mesmo antes de qualquer cliente se conectar.

# # # 2) WebSocket connect

Cada cliente WS começa com um <<CODE0>> pedido. No aperto de mão bem sucedido o
O portal aumenta a entrada de presença para essa ligação.

# # # # Porque os comandos CLI não aparecem

O CLI muitas vezes se conecta para comandos abreviados. Para evitar spamming o
Lista de instâncias, <<CODE0>> é **not** transformado em uma entrada de presença.

#### 3) <<CODE0>> beacons

Os clientes podem enviar beacons periódicos mais ricos através do método <<CODE0>>. O mac
app usa isso para relatar o nome do host, IP e <<CODE1>>.

# # # 4) Nó conecta (papel: nó)

Quando um nó se conecta sobre o Gateway WebSocket com <<CODE0>>, o Gateway
upserts uma entrada de presença para esse nó (mesmo fluxo como outros clientes WS).

# # Mesclar + regras dedupe (por que <<CODE0> importa)

As entradas de presença são armazenadas em um único mapa de memória:

- As inscrições são chaveadas por uma chave de **presença**.
- A melhor chave é uma estável <<CODE0>> (de <<CODE1>>) que sobrevive reinicia.
- As chaves são insensíveis.

Se um cliente reconectar sem um estável <<CODE0>>, ele pode aparecer como um
**duplicate** row.

# # TTL e tamanho limitado

A presença é intencionalmente efêmera:

- ** TTL:** as entradas com mais de 5 minutos são podadas
- ** Entradas máximas:** 200 (o mais antigo caiu primeiro)

Isto mantém a lista fresca e evita o crescimento ilimitado da memória.

# # Caverna remota/túnel (IPs de retrocesso)

Quando um cliente se conecta sobre um túnel SSH / porta local para frente, o Gateway pode
ver o endereço remoto como <<CODE0>>>>. Para evitar sobrescrever um bom cliente
IP, endereços remotos loopback são ignorados.

# # Consumidores

Página do macOS

O aplicativo macOS renderiza a saída de <<CODE0> e aplica um status pequeno
indicador (Ativo/Ocioso/Estado) com base na idade da última atualização.

# # Dicas de depuração

- Para ver a lista bruta, chame <<CODE0>> contra o Gateway.
- Se vir duplicados:
- confirmar que os clientes enviam um <<CODE1>> estável no aperto de mão
- confirmar que os faróis periódicos utilizam o mesmo <<CODE2>>
- verificar se falta a entrada derivada da ligação <<CODE3>> (são esperados duplicados)
