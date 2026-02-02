---
summary: "Elevated exec mode and /elevated directives"
read_when:
  - Adjusting elevated mode defaults, allowlists, or slash command behavior
---

# Modo elevado ( / diretivas elevadas)

# # O que faz

- <<CODE0> é executado no host de gateway e mantém aprovações executivas (igual ao `/elevated ask`).
- <<CODE2> é executado no host gateway **e** auto-aprova exec (aprovações exec skips).
- <<CODE3> é executado no host de gateway, mas mantém aprovações executivas (igual ao `/elevated on`).
- <<CODE5>/`ask` do **not** force `exec.security=full`; a política de segurança/tarefa configurada ainda se aplica.
- Só muda o comportamento quando o agente é **sandboxed** (caso contrário, o executivo já roda no host).
- Formulários de directiva: `/elevated on|off|ask|full`, `/elev on|off|ask|full`.
- Apenas `on|off|ask|full` são aceitos; qualquer outra coisa retorna uma dica e não muda o estado.

# # O que controla (e o que não controla)

- ** Gates de disponibilidade**: <<CODE0> é a linha de base global. <<CODE1> pode restringir ainda mais elevado por agente (ambos devem permitir).
- ** Estado por sessão**: <<CODE2> define o nível elevado para a chave de sessão atual.
- ** Diretriz em linha**: `/elevated on|ask|full` dentro de uma mensagem se aplica apenas a essa mensagem.
- ** Grupos**: Em chats de grupo, diretrizes elevadas só são honradas quando o agente é mencionado. As mensagens somente de comando que ignoram os requisitos de menção são tratadas como mencionado.
- ** Execução host**: forças elevadas `exec` para o host gateway; `full` também define `security=full`.
- **Aprovações**: `full` ignora aprovações executivas; `on`/`ask` honra-as quando as regras de allowlist/ask exigem.
- **Agentes não sandboxizados**: no-op para localização; apenas afeta a localização, registro e status.
- **A política da ferramenta ainda se aplica**: se `exec` for negada pela política da ferramenta, a elevação não pode ser usada.
- **Separar de `/exec`**: `/exec` ajusta os padrões por sessão para os remetentes autorizados e não requer elevação.

# # Ordem de resolução

1. Diretriz em linha sobre a mensagem (aplica-se apenas a essa mensagem).
2. Substituição da sessão (configurado enviando uma mensagem somente de diretiva).
3. Padrão global (`agents.defaults.elevatedDefault` na configuração).

# # Definir um padrão de sessão

- Enviar uma mensagem que é **apenas** a diretiva (whitespace permitido), por exemplo, `/elevated full`.
- Resposta de confirmação (<`Elevated mode set to full...`/ <CODE2>>).
- Se o acesso elevado estiver desactivado ou o remetente não estiver na lista aprovada, a directiva responde com um erro accionável e não altera o estado da sessão.
- Enviar `/elevated` (ou `/elevated:`) sem argumento para ver o nível atual elevado.

# # Disponibilidade + allowlists

- Gate de recurso: `tools.elevated.enabled` (o padrão pode ser desligado via config, mesmo que o código o suporte).
- Lista de autorização do remetente: <<CODE1> com listas de autorização por fornecedor (por exemplo, `discord`, `whatsapp`).
- Porta por agente: `agents.list[].tools.elevated.enabled` (opcional; só pode restringir ainda mais).
- Per-allowlist: `agents.list[].tools.elevated.allowFrom` (opcional; quando definido, o remetente deve corresponder ** ambos** global + per-agent allowlists).
- Retrocesso da discórdia: se `tools.elevated.allowFrom.discord` for omitido, a lista `channels.discord.dm.allowFrom` é utilizada como retrocesso. Definir `tools.elevated.allowFrom.discord` (mesmo `[]`) para sobrepor. Por-agente allowlists fazer ** not** use o backback.
- Todas as portas devem passar; caso contrário elevado é tratado como indisponível.

# # Registro + status

- As chamadas executivas estão registadas.
- O estado da sessão inclui o modo elevado (por exemplo, `elevated=ask`, `elevated=full`).
