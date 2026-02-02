---
summary: "PeekabooBridge integration for macOS UI automation"
read_when:
  - Hosting PeekabooBridge in OpenClaw.app
  - Integrating Peekaboo via Swift Package Manager
  - Changing PeekabooBridge protocol/paths
---

# Ponte Peekaboo (macOS UI automação)

OpenClaw pode hospedar **PeekabooBridge** como uma automação de interface local, consciente de permissão
corretor. Isto permite que o <<CODE0>> Automação de interface de unidade CLI enquanto reutiliza o
permissões TCC do aplicativo macOS.

# # O que isto é (e não é)

- **Host**: OpenClaw.app pode atuar como um host PeekabooBridge.
- **Cliente**: utilizar a superfície <<CODE0>> CLI (sem separado <<CODE1>>>).
- **UI**: sobreposições visuais ficam em Peekaboo.app; OpenClaw é um apresentador de corretores fino.

# # Activar a ponte

Na aplicação macOS:

- Configurações → **Enable Peekaboo Bridge**

Quando habilitado, o OpenClaw inicia um servidor de soquete UNIX local. Se desabilitado, a máquina
é interrompido e <<CODE0>> irá voltar para outros hospedeiros disponíveis.

# # Ordem de descoberta do cliente

Os clientes do Peekaboo normalmente tentam hosts nesta ordem:

1. Peekaboo.app (UX completo)
2. Claude.app (se instalado)
3. Openclaw.app (intermediador fino)

Use <<CODE0>> para ver qual máquina está ativa e qual
o caminho do socket está em uso. Você pode substituir com:

```bash
export PEEKABOO_BRIDGE_SOCKET=/path/to/bridge.sock
```

# # Segurança & permissões

- A ponte valida ** assinaturas de código de chamada**; uma lista de permissões de TeamIDs é
forçado (Peekaboo host TeamID + OpenClaw app TeamID).
- Requisita tempo depois de 10 segundos.
- Se as permissões necessárias estão faltando, a ponte retorna uma mensagem de erro clara
em vez de lançar Configurações do Sistema.

# # Comportamento de instantâneo (automatização)

Os instantâneos são armazenados na memória e expiram automaticamente após uma janela curta.
Se você precisar de retenção mais longa, recapture o cliente.

# # Resolução de problemas

- Se <<CODE0> reporta “client ponte não está autorizado”, garantir que o cliente está
assinado ou executado corretamente com <<CODE1>>
no modo **debug** somente.
- Se nenhum host for encontrado, abra um dos aplicativos do host (Peekaboo.app ou OpenClaw.app)
e confirmar as permissões são concedidas.
