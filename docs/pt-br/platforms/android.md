---
summary: "Android app (node): connection runbook + Canvas/Chat/Camera"
read_when:
  - Pairing or reconnecting the Android node
  - Debugging Android gateway discovery or auth
  - Verifying chat history parity across clients
---

# App Android (Node)

# # Suporte instantâneo

- Papel: app do nó companheiro (Android não hospeda o Gateway).
- Gateway necessário: sim (executá-lo no macOS, Linux ou Windows via WSL2).
- Instalar: (<<<LINK0>>>) + [Pairing] (<<LINK1>>>>).
- Gateway: [Runbook] (<<<LINK2>>) + [Configuração] (<<LINK3>>).
- Protocolos: [Protocolo Gateway] (<<<LINK4>>>) (nódos + plano de controlo).

# # Controle do sistema

Controle de sistema (lançado/sistemad) vive no host Gateway. Ver [Gateway] (<<<LINK0>>>).

# # Runbook de conexão

Aplicativo de nó Android (mDNS/NSD + WebSocket)

O Android se conecta diretamente ao Gateway WebSocket (padrão <<CODE0>>) e usa o emparelhamento de propriedade do Gateway.

Pré-requisitos

- Você pode executar o Gateway na máquina “master”.
- Android dispositivo / emulador pode chegar ao gateway WebSocket:
- Mesma LAN com mDNS/NSD, **ou **
- Mesma rede de caudas usando Wide-Area Bonjour / unicast DNS-SD (ver abaixo), **ou **
- Máquina/porta de gateway manual (fallback)
- Você pode executar o CLI (<<<CODE0>>) na máquina de gateway (ou via SSH).

# # 1) Iniciar o portal

```bash
openclaw gateway --port 18789 --verbose
```

Confirme em logs que você vê algo como:

- <<CODE0>>

Para as configurações somente de tailnet (recomendado para Viena, Londres), ligue o gateway ao IP tailnet:

- Definir <<CODE0>> em <<CODE1> no host gateway.
- Reinicie o aplicativo de menu Gateway / macOS.

# # # 2) Verificar a descoberta (opcional)

Da máquina de gateway:

```bash
dns-sd -B _openclaw-gw._tcp local.
```

Mais notas de depuração: [Bonjour] (<<<LINK0>>).

### #Tailnet (Vienna, Londres) descoberta via DNS-SD unicast

Android NSD/mDNS descoberta não vai cruzar redes. Se seu nó Android e o gateway estão em diferentes redes, mas conectados via Tailscale, use Wide-Area Bonjour / unicast DNS-SD em vez disso:

1. Configure uma zona DNS-SD (exemplo <<CODE0>>) no host do gateway e publique registros <<CODE1>.
2. Configure o DNS dividido em Tailscale para o seu domínio escolhido apontando para esse servidor DNS.

Detalhes e exemplo Configuração do CoreDNS: [Bonjour](<<LINK0>>>).

# # # 3) Conectar a partir do Android

No aplicativo Android:

- O aplicativo mantém sua conexão de gateway viva através de um serviço **foreground** (notificação persistente).
- Abrir **Configurações**.
- Em **Discovered Gateways**, selecione seu gateway e clique em **Connect**.
- Se mDNS está bloqueado, use **Advanced → Manual Gateway** (host + porto) e **Connect (Manual)**.

Após o primeiro emparelhamento bem sucedido, o Android se conecta automaticamente no lançamento:

- Endpoint manual (se activado), caso contrário
- O último portal descoberto (melhor esforço).

# # # 4) Aprovar emparelhamento (CLI)

Na máquina de gateway:

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
```

Detalhes do pareamento: [Gateway pareamento] (<<<LINK0>>>).

# # # 5) Verifique se o nó está conectado

- Através do estado dos nós:
  ```bash
  openclaw nodes status
  ```
- Via Gateway:
  ```bash
  openclaw gateway call node.list --params "{}"
  ```

### 6) Conversa + história

A folha de bate-papo do nó Android usa a chave de sessão **primária do gateway** (<<<CODE0>>), então o histórico e as respostas são compartilhadas com WebChat e outros clientes:

- História: <<CODE0>>
- Enviar: <<CODE1>>>
- Actualizações (melhor esforço): <<CODE2>>>> → <<CODE3>>>

### 7) Tela + câmara

### # Gateway Canvas Host (recomendado para conteúdo web)

Se você quiser que o nó mostre HTML/CSS/JS real que o agente pode editar no disco, aponte o nó para o host da tela Gateway.

Nota: nós usam o host de lona autônoma em <<CODE0>> (padrão <<CODE1>>).

1. Crie <<CODE0>> no host do gateway.

2. Navegue o nó para ele (LAN):

```bash
openclaw nodes invoke --node "<Android Node>" --command canvas.navigate --params '{"url":"http://<gateway-hostname>.local:18793/__openclaw__/canvas/"}'
```

Tailnet (opcional): se ambos os dispositivos estiverem em Tailscale, use um nome MagicDNS ou IP tailnet em vez de <<CODE0>>, por exemplo <<CODE1>>.

Este servidor injeta um cliente live-reload em HTML e recarrega em alterações de arquivos.
O hospedeiro A2UI vive em <<CODE0>>>.

Comandos de tela (somente antecedentes):

- <<CODE0>>, <<CODE1>, <<CODE2>> (usar <<CODE3> ou <<CODE4> para voltar ao andaime padrão). <<CODE5> retorna <<CODE6>> (padrão <<CODE7>>).
- A2UI: <<CODE8>>, <<CODE9>> (<HTML10>> apelido legado)

Comandos da câmera (somente no primeiro plano; a permissão foi encerrada):

- <<CODE0> (jpg)
- <<CODE1> (mp4)

Ver [Node de câmara](<<<LINK0>>) para parâmetros e auxiliares de CLI.
