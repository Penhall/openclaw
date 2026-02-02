---
summary: "iOS node app: connect to the Gateway, pairing, canvas, and troubleshooting"
read_when:
  - Pairing or reconnecting the iOS node
  - Running the iOS app from source
  - Debugging gateway discovery or canvas commands
---

# App iOS (Node)

Disponibilidade: visualização interna. O aplicativo iOS ainda não é distribuído publicamente.

# # O que faz

- Liga-se a um Gateway sobre WebSocket (LAN ou tailnet).
- Expo capacidades de nó: Tela, Instantâneo de tela, Captura de câmera, Localização, Modo de conversa, Voz wake.
- Recebe <<CODE0>>> comandos e reporta os eventos de status do nó.

# # Requisitos

- Gateway rodando em outro dispositivo (macOS, Linux ou Windows via WSL2).
- Caminho da rede:
- A mesma LAN via Bonjour, ou
- Tailnet via DNS- SD unicast (domínio de exemplo: <<CODE0>>), **ou **
- Máquina/porta manual (fallback).

# # Início rápido (par + ligação)

1. Inicie o portal:

```bash
openclaw gateway --port 18789
```

2. No aplicativo iOS, abra Configurações e escolha um gateway descoberto (ou habilite o Host Manual e digite host/port).

3. Aprovar o pedido de emparelhamento no host gateway:

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
```

4. Verificar a conexão:

```bash
openclaw nodes status
openclaw gateway call node.list --params "{}"
```

# # Descobrir caminhos

Bonjour (LAN)

O Gateway anuncia <<CODE0>> em <<CODE1>>. O aplicativo iOS lista estes automaticamente.

# # Tailnet (cross-network)

Se mDNS estiver bloqueado, use uma zona DNS-SD unicast (escolha um domínio; exemplo: <<CODE0>>>) e Tailscale split DNS.
Ver [Bonjour](<<<LINK0>>>) para o exemplo CoreDNS.

# # Máquina manual/porta

Em Configurações, habilite **Manual Host** e insira o gateway host + porto (padrão <<CODE0>>>).

# # Tela + A2UI

O nó iOS renderiza uma tela WKWebView. Use <<CODE0>> para conduzi-lo:

```bash
openclaw nodes invoke --node "iOS Node" --command canvas.navigate --params '{"url":"http://<gateway-host>:18793/__openclaw__/canvas/"}'
```

Notas:

- O anfitrião da tela Gateway serve <<CODE0>> e <<CODE1>>>.
- O nó iOS navega automaticamente para A2UI ao conectar quando um URL de host de tela é anunciado.
- Voltar ao andaime embutido com <<CODE2>> e <<CODE3>>>>.

Avaliação da tela / instantâneo

```bash
openclaw nodes invoke --node "iOS Node" --command canvas.eval --params '{"javaScript":"(() => { const {ctx} = window.__openclaw; ctx.clearRect(0,0,innerWidth,innerHeight); ctx.lineWidth=6; ctx.strokeStyle=\"#ff2d55\"; ctx.beginPath(); ctx.moveTo(40,40); ctx.lineTo(innerWidth-40, innerHeight-40); ctx.stroke(); return \"ok\"; })()"}'
```

```bash
openclaw nodes invoke --node "iOS Node" --command canvas.snapshot --params '{"maxWidth":900,"format":"jpeg"}'
```

# # Voz desperta + modo de conversa

- O modo Voice wake e Talk está disponível em Definições.
- iOS pode suspender áudio de fundo; tratar as funcionalidades de voz como o melhor esforço quando o aplicativo não está ativo.

# # Erros comuns

- <<CODE0>>: traga o aplicativo iOS para o primeiro plano (os comandos canvas/câmera/tela exigem).
- <<CODE1>: o Gateway não anunciou uma URL de host de tela; verifique <<CODE2>> em [Configuração de Gateway](<<LINK0>>).
- Prompt de pareamento nunca aparece: execute <<CODE3>> e aprove manualmente.
- Reconectar falha após a reinstalação: o token de emparelhamento Keychain foi limpo; re-par o nó.

# # Docs relacionados

- [Pairing] (<<<LINK0>>>)
- [Discovery] (<<<LINK1>>>)
- [Bonjour] (<<<LINK2>>>)
