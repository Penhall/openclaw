---
summary: "Nodes: pairing, capabilities, permissions, and CLI helpers for canvas/camera/screen/system"
read_when:
  - Pairing iOS/Android nodes to a gateway
  - Using node canvas/camera for agent context
  - Adding new node commands or CLI helpers
---

# Nós

A **node** é um dispositivo companheiro (macOS/iOS/Android/headless) que se conecta ao Gateway **WebSocket** (mesma porta que os operadores) com <<CODE0>> e expõe uma superfície de comando (por exemplo, <<CODE1>>>, <<CODE2>>, <<CODE3>>) via <<CODE4>>. Detalhes do protocolo: [Protocolo Gateway](<<<LINK0>>>).

Transporte de legado: [Protocolo da ponte](<<<LINK0>>) (TCP JSONL; desactualizado/ removido para os nós actuais).

macOS também pode ser executado em modo **node**: o aplicativo da barra de menus conecta-se ao servidor WS do Gateway e expõe seus comandos locais de lona/câmera como um nó (assim <<CODE0>> funciona contra este Mac).

Notas:

- Nós são **periféricos**, não gateways. Eles não executam o serviço de gateway.
- Mensagens de Telegram/WhatsApp/etc. pousam na **porta**, não em nós.

# # Emparelhamento + status

** Os nós WS usam o emparelhamento do dispositivo.** Os nós apresentam uma identidade do dispositivo durante <<CODE0>>; o Gateway
cria uma solicitação de emparelhamento do dispositivo para <<CODE1>>>. Aprovar através dos dispositivos CLI (ou UI).

CLI:

```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
```

Notas:

- <<CODE0> marca um nó como **pared** quando seu papel de emparelhamento do dispositivo inclui <<CODE1>>.
- <<CODE2> (CLI: <<CODE3>>) é um gateway de propriedade separada
loja de emparelhamento de nó; faz ** not** gate the WS <<CODE4>> aperto de mão.

# # Máquina remota do nó (system.run)

Use um host **node** quando seu Gateway é executado em uma máquina e você quer comandos
para executar em outro. O modelo ainda fala com o **gateway**; o gateway
forwards <<CODE0> chama para o host **node** quando <<CODE1> é selecionado.

O que corre para onde

- **Gateway host**: recebe mensagens, executa o modelo, routes tool calls.
- **Node host**: executa <<CODE0>>/<<CODE1>> na máquina do nó.
- **Aprovações**: forçadas no host do nó via <<CODE2>>.

## # Iniciar uma máquina de nós (precurso)

Na máquina do nó:

```bash
openclaw node run --host <gateway-host> --port 18789 --display-name "Build Node"
```

## # Iniciar uma máquina de nós (serviço)

```bash
openclaw node install --host <gateway-host> --port 18789 --display-name "Build Node"
openclaw node restart
```

# # # Par + nome

Na máquina de gateway:

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes list
```

Opções de nomeação:

- <<CODE0>> em <<CODE1>/ <<CODE2> (persiste em <<CODE3> no nó).
- <<CODE4> (sobreposição do portal).

## # Allowlist the commands

As aprovações exec são **por host de nó**. Adicionar entradas de lista de permissões do gateway:

```bash
openclaw approvals allowlist add --node <id|name|ip> "/usr/bin/uname"
openclaw approvals allowlist add --node <id|name|ip> "/usr/bin/sw_vers"
```

As aprovações vivem no host do nó em <<CODE0>>.

Ponto executivo no nó

Configurar os padrões (configuração do portal):

```bash
openclaw config set tools.exec.host node
openclaw config set tools.exec.security allowlist
openclaw config set tools.exec.node "<id-or-name>"
```

Ou por sessão:

```
/exec host=node security=allowlist node=<id-or-name>
```

Uma vez definido, qualquer chamada <<CODE0>> com <<CODE1> é executada no host do nó (sujeito ao
Lista/aprovações de nó).

Relacionados:

- [CLI da máquina do nó] (<<<LINK0>>>)
- [Ferramenta Exec] (<<<LINK1>>>)
- [Aprovações exec] (<<<<LINK2>>>)

# # Invocando comandos

Nível baixo (RPC bruto):

```bash
openclaw nodes invoke --node <idOrNameOrIp> --command canvas.eval --params '{"javaScript":"location.href"}'
```

Ajudantes de nível superior existem para os fluxos de trabalho comuns “dar ao agente um anexo MEDIA”.

# # Capturas de tela (snapshots de varredura)

Se o nó está mostrando o Canvas (WebView), <<CODE0>> retorna <<CODE1>>.

Ajudante CLI (escreve para um arquivo temporário e imprime <<CODE0>>):

```bash
openclaw nodes canvas snapshot --node <idOrNameOrIp> --format png
openclaw nodes canvas snapshot --node <idOrNameOrIp> --format jpg --max-width 1200 --quality 0.9
```

# # # Controles de tela

```bash
openclaw nodes canvas present --node <idOrNameOrIp> --target https://example.com
openclaw nodes canvas hide --node <idOrNameOrIp>
openclaw nodes canvas navigate https://example.com --node <idOrNameOrIp>
openclaw nodes canvas eval --node <idOrNameOrIp> --js "document.title"
```

Notas:

- <<CODE0> aceita URLs ou caminhos de arquivos locais (<<CODE1>>), mais opcional <<CODE2>> para posicionamento.
- <<CODE3> aceita JS em linha (<<CODE4>>) ou um arg posicional.

## # A2UI (Canvas)

```bash
openclaw nodes canvas a2ui push --node <idOrNameOrIp> --text "Hello"
openclaw nodes canvas a2ui push --node <idOrNameOrIp> --jsonl ./payload.jsonl
openclaw nodes canvas a2ui reset --node <idOrNameOrIp>
```

Notas:

- Apenas o A2UI v0.8 JSONL é suportado (v0.9/createSurface é rejeitado).

# # Fotos + vídeos (câmara de nós)

Fotos (<<<CODE0>>>):

```bash
openclaw nodes camera list --node <idOrNameOrIp>
openclaw nodes camera snap --node <idOrNameOrIp>            # default: both facings (2 MEDIA lines)
openclaw nodes camera snap --node <idOrNameOrIp> --facing front
```

Videoclipes (<<<CODE0>>>):

```bash
openclaw nodes camera clip --node <idOrNameOrIp> --duration 10s
openclaw nodes camera clip --node <idOrNameOrIp> --duration 3000 --no-audio
```

Notas:

- O nó deve ser **foregrounded** para <<CODE0>> e <<CODE1>> (chamadas de fundo retornam <<CODE2>>>).
- A duração do clip é pinçada (atualmente <<CODE3>>>) para evitar cargas de base sobredimensionadas64.
- Android irá pedir por <<CODE4>/<HTML5>>> permissões quando possível; permissões negadas falham com <<CODE6>>>.

# # Gravações de tela (nós)

Os nós expõem <<CODE0>> (mp4). Exemplo:

```bash
openclaw nodes screen record --node <idOrNameOrIp> --duration 10s --fps 10
openclaw nodes screen record --node <idOrNameOrIp> --duration 10s --fps 10 --no-audio
```

Notas:

- <<CODE0> exige que a aplicação do nó seja em primeiro plano.
- Android irá mostrar o sistema tela captura prompt antes de gravar.
- As gravações de tela são pinçadas para <<CODE1>>>.
- <<CODE2> desabilita a captura do microfone (suportado no iOS/Android; o macOS usa o áudio de captura do sistema).
- Use <<CODE3>> para selecionar um visor quando várias telas estão disponíveis.

# # Localização (nós)

Os nós expõem <<CODE0>> quando a Localização está habilitada nas configurações.

Ajudante CLI:

```bash
openclaw nodes location get --node <idOrNameOrIp>
openclaw nodes location get --node <idOrNameOrIp> --accuracy precise --max-age 15000 --location-timeout 10000
```

Notas:

- A localização é **off por padrão**.
- “Sempre” requer permissão do sistema; busca de fundo é o melhor esforço.
- A resposta inclui lat/lon, precisão (metros) e timestamp.

# # SMS (nós Android)

Os nós Android podem expor <<CODE0>> quando o usuário concede **SMS** permissão e o dispositivo suporta telefonia.

Invocação de baixo nível:

```bash
openclaw nodes invoke --node <idOrNameOrIp> --command sms.send --params '{"to":"+15555550123","message":"Hello from OpenClaw"}'
```

Notas:

- O prompt de permissão deve ser aceito no dispositivo Android antes que a capacidade seja anunciada.
- Os dispositivos Wi-Fi sem telefonia não anunciam <<CODE0>>>.

# # Comandos do sistema (nós host / nó mac)

O nó macOS expõe <<CODE0>>, <HTML1>>>>, e <<CODE2>>.
O hospedeiro sem cabeça expõe <<CODE3>>>, <<CODE4>>> e <<CODE5>>.

Exemplos:

```bash
openclaw nodes run --node <idOrNameOrIp> -- echo "Hello from mac node"
openclaw nodes notify --node <idOrNameOrIp> --title "Ping" --body "Gateway ready"
```

Notas:

- <<CODE0> retorna o código stdout/stderr/exit na carga útil.
- <<CODE1> respeita o estado de autorização de notificação na aplicação macOS.
- <<CODE2> suporta <<CODE3>>, <<CODE4>>, <<CODE5>> e <<CODE6>>.
- <<CODE7>> suporta <<CODE8>>> e <<CODE9>>>.
- nós macOS gota <<CODE10>> substitui; hosts de nó sem cabeça só aceitam <<CODE11>> quando prepara o PATH do host do nó.
- No modo nó macOS, <<CODE12>> é fechado por aprovações executivas na aplicação macOS (Configurações → aprovações Exec).
Ask/allowlist/full comportam-se da mesma forma que o host do nó sem cabeça; prompt negado retorna <<CODE13>>>.
- No hospedeiro sem cabeça, <<CODE14>> é fechado por aprovações executivas (<<CODE15>>>).

# # Ligação de nó Exec

Quando vários nós estão disponíveis, você pode ligar exec a um nó específico.
Isso define o nó padrão para <<CODE0>> (e pode ser substituído por agente).

Padrão global:

```bash
openclaw config set tools.exec.node "node-id-or-name"
```

Substituição por agente:

```bash
openclaw config get agents.list
openclaw config set agents.list[0].tools.exec.node "node-id-or-name"
```

Desactivar para permitir qualquer nó:

```bash
openclaw config unset tools.exec.node
openclaw config unset agents.list[0].tools.exec.node
```

# # Mapa de Permissões

Os nós podem incluir um <<CODE0>> mapa em <<CODE1>>/ <<CODE2>>, chaveado por nome de permissão (por exemplo, <<CODE3>>, <<CODE4>>>) com valores booleanos (<<CODE5>> = concedido).

# # Máquina de nó sem cabeça (cross-platform)

Openclaw pode executar um host de nó ** sem cabeça** (sem UI) que se conecta ao Gateway
WebSocket e expõe <<CODE0>>/<HTML1>>>>. Isto é útil no Linux/Windows
ou para executar um nó mínimo ao lado de um servidor.

Iniciar:

```bash
openclaw node run --host <gateway-host> --port 18789
```

Notas:

- O pareamento ainda é necessário (o Gateway mostrará um prompt de aprovação de nó).
- O host do nó armazena seu id de nó, token, nome de exibição e informações de conexão de gateway em <<CODE0>>.
- As aprovações exec são aplicadas localmente via <<CODE1>>
(ver [Aprovações exec] (<<<<LINK0>>>)).
- No macOS, o host de nó sem cabeça prefere o host executivo do aplicativo companheiro quando alcançável e cai
voltar à execução local se a aplicação não estiver disponível. Definir <<CODE2>> para requerer
o aplicativo, ou <<CODE3>> para desativar o retorno.
- Adicionar <<CODE4>> / <<CODE5>> quando o Gateway WS utiliza o TLS.

# # Modo de nó Mac

- O aplicativo do macOS se conecta ao servidor Gateway WS como um nó (então <<CODE0> funciona contra este Mac).
- No modo remoto, o aplicativo abre um túnel SSH para a porta Gateway e se conecta a <<CODE1>>.
