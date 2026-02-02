---
summary: "CLI onboarding wizard: guided setup for gateway, workspace, channels, and skills"
read_when:
  - Running or configuring the onboarding wizard
  - Setting up a new machine
---

Assistente de bordo (CLI)

O assistente de onboarding é a ** forma recomendada** de configurar OpenClaw no macOS,
Linux, ou Windows (via WSL2; fortemente recomendado).
Ele configura um Gateway local ou uma conexão de Gateway remota, além de canais, habilidades,
e o espaço de trabalho defaults em um fluxo guiado.

Ponto de entrada primário:

```bash
openclaw onboard
```

Primeiro bate-papo mais rápido: abra a interface de controle (sem necessidade de configuração do canal). Executar
<<CODE0>> e chat no navegador. Docs: [Dashboard] (<<<LINK0>>>).

Reconfiguração posterior:

```bash
openclaw configure
```

Recomendado: configure uma chave Brave Search API para que o agente possa usar <<CODE0>
(<<<CODE1> funciona sem uma chave). Caminho mais fácil: <<CODE2>>>
que armazena <<CODE3>>>>. Docs: [Ferramentas Web](<<<LINK0>>>).

# # QuickStart vs Avançado

O assistente começa com ** QuickStart** (padrão) vs ** Advanced** (controle total).

**QuickStart** mantém os padrões:

- Gateway local (loopback)
- Padrão do espaço de trabalho (ou espaço de trabalho existente)
- Porta de entrada **18789**
- Gateway auth **Token** (gerado automaticamente, mesmo em loopback)
- Exposição em escala de cauda **Off**
- Telegram + WhatsApp DMs padrão para ** allowlist** (você será solicitado para o seu número de telefone)

**Avançado** expõe cada passo (modo, espaço de trabalho, gateway, canais, daemon, habilidades).

# # O que o feiticeiro faz

** Modo local (por omissão)** guia-o através de:

- Modelo/auth (Código OpenAI (Codex) assinatura OAuth, chave de API antrópica (recomendado) ou configuração-token (colar), mais opções MiniMax/GLM/Moonshot/AI Gateway)
- Local de trabalho + arquivos bootstrap
- Configurações do gateway (porta/bind/auth/tailscale)
- Fornecedores (Telegrama, WhatsApp, Discórdia, Google Chat, Mattermost (plugin), Sinal)
- Daemon install (LaunchAgent / unidade de usuário systemd)
- Verificação de saúde
- Competências (recomendadas)

** Modo remoto** só configura o cliente local para se conectar a um Gateway em outro lugar.
Ele não ** instalar ou alterar nada no host remoto.

Para adicionar mais agentes isolados (separar espaço de trabalho + sessões + autenticação), use:

```bash
openclaw agents add <name>
```

Dica: <<CODE0> faz **não** implica modo não-interativo. Use <<CODE1>> (e <<CODE2>>>) para scripts.

# # Detalhes do fluxo (local)

1. ** Existing config detection**
- Se <<CODE0>> existir, escolha **Keep / Modify / Reset**.
- Repetir a execução do assistente não ** Limpar nada a menos que você explicitamente escolher **Repor **
(ou passar <<CODE1>>>>).
- Se a configuração é inválida ou contém chaves legadas, o assistente para e pergunta
correr <<CODE2>> antes de continuar.
- Reset usa <<CODE3>> (nunca <<CODE4>>>) e oferece escopos:
- Apenas configuração
- Configuração + credenciais + sessões
- Reset completo (também remove espaço de trabalho)

2. **Modelo/Auth**
- ** Chave de API antrópica (recomendada)**: usa <<CODE0>> se presente ou prompts para uma chave, em seguida, salva-a para uso do daemon.
- ** OAuth antrópico (Claude Code CLI)**: no macOS o assistente verifica o item Keychain "Claude Code-credentials" (escolha "Always Allow" para iniciar não bloquear); no Linux/Windows ele reutiliza <<CODE1> se presente.
- ** Token antrópico (paste setup-token)**: executar <<CODE2>> em qualquer máquina, em seguida, colar o token (você pode nomeá-lo; em branco = padrão).
- **OpenAI Code (Codex) subscription (Codex CLI)**: se <<CODE3> existe, o assistente pode reutilizá-lo.
- **OpenAI Code (Codex) subscription (OAuth)**: browser flow; cole o <<CODE4>>.
- Define <<CODE5>> para <<CODE6> quando o modelo está desligado ou <<CODE7>>>.
- **OpenAI API chave**: usa <<CODE8>> se presente ou prompts para uma chave, em seguida, salva-lo para <<CODE9> para lançado pode lê-lo.
- **OpenCode Zen (proxy multimodelo)**: prompts para <<CODE10>> (ou <<CODE11>>, obtê-lo em https://opencode.ai/auth).
- ** Chave API**: guarda a chave para si.
- **Vercel AI Gateway (proxy multimodelo)**: prompts para <<CODE12>>.
- Mais detalhes: [Vercel AI Gateway] (<<<LINK0>>)
- **MiniMax M2.1**: config é auto-escrita.
- Mais detalhes: [MiniMax](<<<LINK1>>)
- ** Síntese (Antrópico- compatível)**: instruções para <<CODE13>>.
- Mais detalhes: [Sintético] (<<<<LINK2>>)
- **Moonshot (Kimi K2)**: a configuração é escrita automaticamente.
- **Kimi Coding**: config é auto-escrita.
- Mais pormenores: [I.A. (Kimi + Kimi Coding)] (<<<LINK3>>>)
- **Skip**: nenhuma autorização configurada ainda.
- Escolha um modelo padrão de opções detectadas (ou digite provedor/modelo manualmente).
- Wizard executa uma verificação de modelo e avisa se o modelo configurado é desconhecido ou falta a autenticação.

- Credenciais OAuth vivem em <<CODE0>>; perfis de autenticação vivem em <<CODE1>> (chaves API + OAuth).
- Mais detalhes: [/conceitos/auth] (<<<LINK0>>)

3. ** Espaço de trabalho**
- Padrão <<CODE0>> (configurável).
- Semeia os arquivos de espaço de trabalho necessários para o ritual de bootstrap do agente.
- layout completo do espaço de trabalho + guia de backup: [Espaço de trabalho do agente] (<<<LINK0>>>)

4. **Gateway**
- Porta, ligação, modo de autenticação, exposição em escala de cauda.
- Recomendação de autenticação: mantenha **Token** mesmo para loopback assim que os clientes WS locais devem autenticar.
- Desactivar a autenticação apenas se confiar plenamente em todos os processos locais.
- As ligações não- loopback ainda requerem autorização.

5. **Canais **
- [WhatsApp](<<<LINK0>>): login opcional de QR.
- [Telegrama] (<<<LINK1>>): token bot.
- [Discord] (<<<LINK2>>): token bot.
- [Google Chat](<<<LINK3>>): conta de serviço JSON + público webhook.
- [Mattermost] (<<<LINK4>>) (plugin): token bot + URL base.
- [Signal] (<<<LINK5>>): opcional <<CODE0>>> instalar + configuração da conta.
- [iMessage] (<<<LINK6>>>): local <<CODE1>>> Caminho CLI + acesso DB.
- Segurança DM: padrão é emparelhamento. Primeiro o DM envia um código; aprove via <<CODE2>>> ou use allowlists.

6. **Daemon install**
- LaunchAgent
- Requer uma sessão de usuário logada; para sem cabeça, use um LaunchDaemon personalizado (não enviado).
- Linux (e Windows via WSL2): unidade de usuário systemd
- Wizard tenta habilitar a permanência via <<CODE0> para que o Gateway fique em cima após o logout.
- Maio prompt para sudo (escrita <<CODE1>>); tenta sem sudo primeiro.
- **Seleção de tempo:** Node (recomendado; exigido para WhatsApp/Telegram). Bun é ** não recomendado**.

7. ** Controlo de saúde**
- Inicia o Gateway (se necessário) e executa <<CODE0>>>.
- Dica: <<CODE1> adiciona sondas de saúde de gateway para saída de status (requer um gateway acessível).

8. ** Competências (recomendadas) **
- Lê as competências disponíveis e verifica os requisitos.
- Permite escolher um gerenciador de nós: **npm / pnpm** (bun não recomendado).
- Instala dependências opcionais (alguns usam Homebrew no macOS).

9. **Terminar**
- Resumo + próximos passos, incluindo aplicativos iOS/Android/macOS para recursos extras.

- Se nenhuma GUI for detectada, o assistente imprime instruções SSH para a interface de controle em vez de abrir um navegador.
- Se os ativos do Control UI estiverem faltando, o assistente tenta construí-los; o retorno é <<CODE0>> (auto-instala deps UI).

# # Modo remoto

O modo remoto configura um cliente local para se conectar a um Gateway em outro lugar.

O que você vai definir:

- URL do Gateway Remoto (<<<CODE0>>)
- Indicar se o Gateway remoto necessita de autorização (recomendado)

Notas:

- Nenhuma instalação remota ou alterações do daemon são realizadas.
- Se o Gateway for apenas loopback, use o túnel SSH ou uma rede de cauda.
- Dica de descoberta:
- macOS: Bonjour (<<<CODE0>>)
- Linux: Avahi (<<<CODE1>>)

# # Adicione outro agente

Usar <<CODE0>> para criar um agente separado com sua própria área de trabalho,
sessões e perfis de autenticação. Executando sem <<CODE1> lança o assistente.

O que define:

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>

Notas:

- Os espaços de trabalho padrão seguem <<CODE0>>>.
- Adicionar <<CODE1>> para encaminhar mensagens de entrada (o assistente pode fazer isso).
- Bandeiras não interactivas: <<CODE2>>, <<CODE3>>, <<CODE4>>, <<CODE5>>.

# # Modo não- interactivo

Usar <<CODE0>> para automatizar ou programar a bordo:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice apiKey \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback \
  --install-daemon \
  --daemon-runtime node \
  --skip-skills
```

Adicionar <<CODE0>> para um resumo legível por máquina.

Exemplo Gemini:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice gemini-api-key \
  --gemini-api-key "$GEMINI_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

Exemplo Z.AI:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice zai-api-key \
  --zai-api-key "$ZAI_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

Vercel AI Exemplo do portal:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice ai-gateway-api-key \
  --ai-gateway-api-key "$AI_GATEWAY_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

Exemplo Moonshot:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice moonshot-api-key \
  --moonshot-api-key "$MOONSHOT_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

Exemplo sintético:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice synthetic-api-key \
  --synthetic-api-key "$SYNTHETIC_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

Exemplo do OpenCode Zen:

```bash
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice opencode-zen \
  --opencode-zen-api-key "$OPENCODE_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback
```

Adicionar o exemplo do agente (não- interactivo):

```bash
openclaw agents add work \
  --workspace ~/.openclaw/workspace-work \
  --model openai/gpt-5.2 \
  --bind whatsapp:biz \
  --non-interactive \
  --json
```

# # Wizard Gateway RPC

O Gateway expõe o fluxo do assistente sobre RPC (<<<CODE0>>, <<CODE1>>, <<CODE2>>, <<CODE3>>).
Clientes (macOS app, Control UI) podem renderizar passos sem re-implementar a lógica de integração.

# # Configuração do sinal (sinal-cli)

O assistente pode instalar <<CODE0>> das versões do GitHub:

- Transfere o ativo de liberação apropriado.
- Conserva- a em <<CODE0>>>.
- Escreve <<CODE1>> para a sua configuração.

Notas:

- As construções da JVM exigem **Java 21**.
- As construções nativas são usadas quando disponíveis.
- Windows usa WSL2; signal-cli install segue o fluxo Linux dentro WSL.

# # O que o feiticeiro escreve

Campos típicos em <<CODE0>>:

- <<CODE0>>
- <<CODE1>>/ <<CODE2>> (se o Minimax for escolhido)
- <<CODE3> (modo, ligação, auth, escala de cauda)
- <<CODE4>>, <<CODE5>>, <<CODE6>>, <<CODE7>>
- Listas de allowlists de canais (Slack/Discord/Matrix/Microsoft Teams) quando você optar durante as prompts (nomes resolvem IDs quando possível).
- <<CODE8>>
- <<CODE9>>
- <<CODE10>>
- <<CODE11>>
- <<CODE12>>
- <<CODE13>>

<<CODE0> escreve <<CODE1>> e opcional <<CODE2>>>.

As credenciais do WhatsApp são <<CODE0>>>.
As sessões são armazenadas em <<CODE1>>>>.

Alguns canais são entregues como plugins. Quando você escolhe um durante o embarque, o assistente
irá pedir para instalá-lo (npm ou um caminho local) antes de poder ser configurado.

# # Docs relacionados

- app macOS a bordo: [A bordo] (<<<LINK0>>>)
- Referência da configuração: [Configuração do portal] (<<<LINK1>>>)
- Fornecedores: [WhatsApp] (<<<LINK2>>), [Telegrama] (<<LINK3>>>), [Discord] (<<LINK4>>), [Google Chat] (<<LINK5>>>), [Signal] (<<LINK6>>>), [iMessage] (<<<LINK7>>)
- Habilidades: [Skills](<<<LINK8>>), [Skills config](<<LINK9>>)
