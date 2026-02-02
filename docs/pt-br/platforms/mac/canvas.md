---
summary: "Agent-controlled Canvas panel embedded via WKWebView + custom URL scheme"
read_when:
  - Implementing the macOS Canvas panel
  - Adding agent controls for visual workspace
  - Debugging WKWebView canvas loads
---

# Canvas (aplicativo macOS)

A aplicação macOS incorpora um painel de Canvas ** controlado por agentes usando <<CODE0>>. Ele
é um espaço de trabalho visual leve para HTML/CSS/JS, A2UI e pequeno interativo
Superfícies de IU.

# # Onde a Canvas vive

O estado da tela é armazenado sob o suporte da aplicação:

- <<CODE0>>

O painel Canvas serve esses arquivos através de um esquema **custom URL**:

- <<CODE0>>

Exemplos:

- <<CODE0>> → <<CODE1>>>
- <<CODE2>> → <<CODE3>>
- <<CODE4>> → <<CODE5>>

Se não existir <<CODE0>> na raiz, o aplicativo mostra uma **built-in scaffold page**.

# # Comportamento do painel

- Painel sem bordas, redimensionável ancorado perto da barra de menu (ou cursor do mouse).
- Lembra-se do tamanho/posição por sessão.
- Auto-recarrega quando os arquivos de lona local mudam.
- Apenas um painel de tela é visível de cada vez (sessão é trocada conforme necessário).

Canvas podem ser desabilitadas de Configurações → **Permitir Canvas**. Quando desativado, canvas
os comandos do nó retornam <<CODE0>>>.

# # Superfície da API do agente

A tela é exposta através do **Gateway WebSocket**, para que o agente possa:

- mostrar/esconder o painel
- navegar para um caminho ou URL
- avaliar o JavaScript
- capturar uma imagem de instantâneo

Exemplos de CLI:

```bash
openclaw nodes canvas present --node <id>
openclaw nodes canvas navigate --node <id> --url "/"
openclaw nodes canvas eval --node <id> --js "document.title"
openclaw nodes canvas snapshot --node <id>
```

Notas:

- <<CODE0> aceita ** caminhos de tela locais**, <<CODE1> URLs e <<CODE2>>> URLs.
- Se passar <<CODE3>>, a Tela mostra o andaime local ou <<CODE4>>.

# # A2UI na tela

A2UI é hospedado pelo host Gateway canvas e renderizado dentro do painel Canvas.
Quando o Gateway anuncia um host Canvas, o aplicativo macOS se auto-navega para
Página de host A2UI na primeira abertura.

URL da máquina A2UI padrão:

```
http://<gateway-host>:18793/__openclaw__/a2ui/
```

### Comandos A2UI (v0.8)

Canvas aceita **A2UI v0.8** server→mensagens de cliente:

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>
- <<CODE3>>

<<CODE0> (v0.9) não é suportado.

Exemplo de CLI:

```bash
cat > /tmp/a2ui-v0.8.jsonl <<'EOFA2'
{"surfaceUpdate":{"surfaceId":"main","components":[{"id":"root","component":{"Column":{"children":{"explicitList":["title","content"]}}}},{"id":"title","component":{"Text":{"text":{"literalString":"Canvas (A2UI v0.8)"},"usageHint":"h1"}}},{"id":"content","component":{"Text":{"text":{"literalString":"If you can read this, A2UI push works."},"usageHint":"body"}}}]}}
{"beginRendering":{"surfaceId":"main","root":"root"}}
EOFA2

openclaw nodes canvas a2ui push --jsonl /tmp/a2ui-v0.8.jsonl --node <id>
```

Fumaça rápida:

```bash
openclaw nodes canvas a2ui push --node <id> --text "Hello from A2UI"
```

# # Agente disparador corre de Canvas

Canvas podem desencadear novas execuções de agentes através de links profundos:

- <<CODE0>>

Exemplo (em JS):

```js
window.location.href = "openclaw://agent?message=Review%20this%20design";
```

O aplicativo pede confirmação, a menos que seja fornecida uma chave válida.

# # Notas de segurança

- Canvas scheme blocos diretório transversal; arquivos devem viver sob o root da sessão.
- Conteúdo local Canvas usa um esquema personalizado (sem servidor loopback necessário).
- Externo <<CODE0>> URLs só são permitidas quando explicitamente navegadas.
