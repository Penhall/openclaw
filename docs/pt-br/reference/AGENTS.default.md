---
summary: "Default OpenClaw agent instructions and skills roster for the personal assistant setup"
read_when:
  - Starting a new OpenClaw agent session
  - Enabling or auditing default skills
---

# AGENTS.md — Assistente Pessoal OpenClaw (padrão)

# # Primeira corrida (recomendado)

OpenClaw usa um diretório de espaço de trabalho dedicado para o agente. Padrão: `~/.openclaw/workspace` (configurado via `agents.defaults.workspace`).

1. Crie o espaço de trabalho (se já não existir):

```bash
mkdir -p ~/.openclaw/workspace
```

2. Copie os modelos de espaço de trabalho padrão para o espaço de trabalho:

```bash
cp docs/reference/templates/AGENTS.md ~/.openclaw/workspace/AGENTS.md
cp docs/reference/templates/SOUL.md ~/.openclaw/workspace/SOUL.md
cp docs/reference/templates/TOOLS.md ~/.openclaw/workspace/TOOLS.md
```

3. Opcional: se você quiser a lista de habilidades assistente pessoal, substituir AGENTS.md com este arquivo:

```bash
cp docs/reference/AGENTS.default.md ~/.openclaw/workspace/AGENTS.md
```

4. Opcional: escolher um espaço de trabalho diferente, definindo `agents.defaults.workspace` (suportes `~`):

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}
```

# # Predefinição de segurança

- Não despejar diretórios ou segredos em bate-papo.
- Não execute comandos destrutivos a menos que explicitamente solicitado.
- Não envie respostas parciais/streaming para superfícies de mensagens externas (apenas respostas finais).

# # Início da sessão (obrigatório)

- Ler `SOUL.md`, `USER.md`, `memory.md`, e hoje + ontem em `memory/`.
- Fá-lo antes de responder.

# # Alma (obrigatória)

- <<CODE0> define identidade, tom e limites. Mantém-no actualizado.
- Se alterar `SOUL.md`, informe o utilizador.
- Você é uma instância nova cada sessão; a continuidade vive nestes arquivos.

# # Espaços compartilhados (recomendados)

- Você não é a voz do usuário; tenha cuidado em chats de grupo ou canais públicos.
- Não partilhe dados privados, informações de contacto ou notas internas.

# # Sistema de memória (recomendado)

- Diário: `memory/YYYY-MM-DD.md` (criar `memory/` se necessário).
- Memória de longo prazo: `memory.md` para fatos, preferências e decisões duráveis.
- No início da sessão, leia hoje + ontem + `memory.md` se presente.
- Captura: decisões, preferências, restrições, laços abertos.
- Evitar segredos a menos que explicitamente solicitado.

# # Ferramentas e habilidades

- Ferramentas vivem em habilidades; siga cada habilidade `SKILL.md` quando você precisar.
- Manter notas específicas do ambiente em `TOOLS.md` (Notas para as competências).

# # Ponta de backup (recomendada)

Se você tratar este espaço de trabalho como “memória” de Clawd, torne-o um repo git (idealmente privado) então `AGENTS.md` e seus arquivos de memória são copiados.

```bash
cd ~/.openclaw/workspace
git init
git add AGENTS.md
git commit -m "Add Clawd workspace"
# Optional: add a private remote + push
```

# # O que Openclaw faz

- Executa o gateway WhatsApp + Pi para que o assistente possa ler/escrever chats, obter contexto e executar habilidades através do Mac host.
- o aplicativo macOS gerencia permissões (gravação de tela, notificações, microfone) e expõe o <<CODE0> CLI através de seu binário empacotado.
- Conversas diretas colapsam na sessão <<CODE1> do agente por padrão; grupos permanecem isolados como <<CODE2> (quartos/canais: `agent:<agentId>:<channel>:channel:<id>`); batimentos cardíacos mantêm as tarefas de fundo vivas.

# # Core Skills (Ativado em Configurações → Habilidades)

- **mcporter** — Ferramenta servidor runtime/CLI para gerenciar backends de habilidades externas.
- **Peekaboo** — Imagens rápidas do macOS com análise opcional de visão de IA.
- **camsnap** — Capture quadros, clipes ou alertas de movimento de câmeras de segurança RTSP/ONVIF.
- **oracle** — Agente CLI pronto para OpenAI com replay de sessão e controle do navegador.
- **8ctl** — Controle seu sono, do terminal.
- **imsg** — Enviar, ler, transmitir iMessage & SMS.
- **wacli** — WhatsApp CLI: sync, search, send.
- **discórdia** — Acções de discórdia: reacção, autocolantes, sondagens. Usar alvos `user:<id>` ou `channel:<id>` (os ids numéricos são ambíguos).
- **gog** — Google Suite CLI: Gmail, Calendário, Unidade, Contactos.
- **Spotify-player** — Cliente do Spotify Terminal para pesquisar/queda/controle de reprodução.
- **sag** — Discurso OnzeLabs com estilo mac dizer UX; fluxos para alto-falantes por padrão.
- **Sonos CLI** — Controla os falantes de Sonos (descobrir/status/playback/volume/agrupamento) a partir de scripts.
- ** blucli** — Joga, agrupa e automatiza os jogadores BluOS dos scripts.
- ** OpenHue CLI** — Philips Controle de iluminação de matiz para cenas e automações.
- **OpenAI Whisper** — Discurso local para texto para ditados rápidos e transcrições de correio de voz.
- ** Gemini CLI** — Google Gemini models from the terminal for fast Q&A.
- **bird** — X/Twitter CLI para tweetar, responder, ler threads e pesquisar sem navegador.
- **agent-tools** — Kit de ferramentas para automações e scripts auxiliares.

# # Notas de uso

- Preferir o <<CODE0> CLI para scripting; mac app lida com permissões.
- Executar instala a partir da aba Habilidades; ele esconde o botão se um binário já está presente.
- Mantenha os batimentos cardíacos ativados para que o assistente possa agendar lembretes, monitorar caixas de entrada e ativar capturas de câmera.
- A interface de lona funciona com sobreposições nativas. Evite colocar controles críticos nas bordas superior esquerda/top-right/bottom; adicione calhas explícitas no layout e não confie em insets de área segura.
- Para verificação orientada pelo navegador, use `openclaw browser` (tabs/status/screenshot) com o perfil Chrome gerenciado pelo OpenClaw.
- Para a inspecção do DOM, utilizar `openclaw browser eval|query|dom|snapshot` (e `--json`/<CODE4>> quando necessitar de saída da máquina).
- Para interações, use `openclaw browser click|type|hover|drag|select|upload|press|wait|navigate|back|evaluate|run` (clique/tipo requer refs instantâneo; use `evaluate` para seletores CSS).
