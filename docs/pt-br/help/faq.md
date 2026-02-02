---
summary: "Frequently asked questions about OpenClaw setup, configuration, and usage"
---

FAQ

Respostas rápidas mais solução de problemas mais profunda para configurações do mundo real (dev local, VPS, multi-agente, chaves OAuth/API, failover do modelo). Para os diagnósticos em tempo de execução, ver [Troubleshooting] (<<<LINK0>>). Para a referência completa de configuração, veja [Configuração] (<<<LINK1>>).

# # Índice

- [Início rápido e configuração de primeira execução] (<<<LINK0>>>)
- [Estou preso qual é a maneira mais rápida de se soltar?] (<<<LINK1>>>>)
- [Qual é a maneira recomendada de instalar e configurar o OpenClaw?](<<<LINK2>>>)
- [Como abro o painel depois de embarcar?] (<<<LINK3>>>)
- [Como faço para autenticar o painel (token) no localhost vs remoto?](<<<LINK4>>>)
- [De que tempo de execução eu preciso?] (<<<LINK5>>>)
- [Ele funciona em Raspberry Pi?] (<<<LINK6>>>)
- [Alguma dica para instalações de framboesa Pi?] (<<<LINK7>>)
- [Está preso em "Acorde meu amigo" / a bordo não vai eclodir. E agora?](<<<LINK8>>>)
- [Posso migrar minha configuração para uma nova máquina (Mac mini) sem refazer a bordo?](<<LINK9>>)
- [Onde eu vejo o que há de novo na última versão?](<<<LINK10>>>)
- [Não consigo aceder ao Docs.openclaw.ai (erro SSL). E agora?](<<<LINK11>>)
- [Qual é a diferença entre estável e beta?] (<<<LINK12>>>)
- [Como faço para instalar a versão beta, e qual é a diferença entre beta e dev?](<<LINK13>>)
- [Como faço para tentar os bits mais recentes?] (<<<LINK14>>)
- Quanto tempo demora a instalação e a integração?](<<<LINK15>>>)
- [Installer preso? Como posso obter mais feedback?](<<<LINK16>>>)
- [Windows install diz git não encontrado ou openclaw não reconhecido] (<<<LINK17>>>)
- [Os documentos não responderam à minha pergunta - como posso obter uma resposta melhor?](<<LINK18>>)
- [Como faço para instalar OpenClaw no Linux?] (<<<LINK19>>)
- [Como faço para instalar OpenClaw em um VPS?](<<<LINK20>>)
- [Onde estão as guias de instalação da nuvem/VPS?] (<<<LINK21>>)
- [Posso pedir ao OpenClaw para se atualizar?] (<<<LINK22>>)
- [O que o assistente de bordo realmente faz?] (<<<LINK23>>)
- [Eu preciso de uma assinatura Claude ou OpenAI para executar isso?](<<<LINK24>>)
- [Posso usar assinatura Claude Max sem uma chave API] (<<<LINK25>>>)
- [Como funciona a autenticação antrópica "setup-token"?](<<<LINK26>>)
- [Onde encontro uma ficha de configuração antrópica?] (<<<LINK27>>>)
- [Você apoia Claude subscription auth (Claude Code OAuth)?](<<<LINK28>>>)
- [Porque estou a ver <<CODE0>> de Antrópico?] (<<LINK29>>>)
- [O AWS Bedrock é suportado?] (<<<LINK30>>>)
- [Como funciona o Codex auth?] (<<<LINK31>>>)
- [Você suporta a autenticação da subscrição do OpenAI (Codex OAuth)?](<<<LINK32>>)
- [Como configuro Gemini CLI OAuth] (<<<LINK33>>)
- [Um modelo local está OK para conversas casuais?] (<<<LINK34>>)
- [Como faço para manter o tráfego do modelo hospedado em uma região específica?](<<<LINK35>>)
- [Eu tenho que comprar um Mac Mini para instalar isso?](<<<LINK36>>)
- [Eu preciso de um mini Mac para suporte iMessage?](<<<LINK37>>)
- [Se eu comprar um mini Mac para executar OpenClaw, posso conectá-lo ao meu MacBook Pro?](<<<LINK38>>)
- [Posso usar Bun?] (<<<LINK39>>)
- [Telegrama: o que vai em <<CODE1>>?] (<<LINK40>>>)
- [Multiplas pessoas podem usar um número WhatsApp com diferentes instâncias OpenClaw?](<<<LINK41>>)
- [Posso executar um agente de "conversa rápida" e um agente de "Opus para codificação"?](<<LINK42>>)
- [O Homebrew funciona no Linux?](<<<LINK43>>)
- [Qual é a diferença entre a instalação hackable (git) e a instalação npm?] (<<<LINK44>>)
- [Posso alternar entre npm e git instala mais tarde?](<<<LINK45>>>)
- [Devo executar o Gateway no meu laptop ou um VPS?] (<<<LINK46>>>)
- [Quão importante é executar OpenClaw em uma máquina dedicada?](<<<LINK47>>>)
- [Quais são os requisitos mínimos de VPS e o sistema operacional recomendado?](<<<LINK48>>)
- [Posso executar OpenClaw em uma VM e quais são os requisitos](<<<LINK49>>>)
- [O que é OpenClaw?] (<<<LINK50>>)
- [O que é OpenClaw, num parágrafo?] (<<<LINK51>>)
- [Qual é a proposta de valor?](<<<LINK52>>>)
- [Eu só configurei o que devo fazer primeiro] (<<<LINK53>>)
- [Quais são os cinco primeiros casos de uso diário para OpenClaw](<<<LINK54>>)
- [O OpenClaw pode ajudar com anúncios e blogs para um SaaS](<<LINK55>>)
- [Quais são as vantagens vs Claude Code para o desenvolvimento web?](<<<LINK56>>)
- [Competências e automação] (<<<<LINK57>>>)
- [Como faço para personalizar as habilidades sem manter o acordo sujo?] (<<<LINK58>>)
- [Posso carregar as habilidades de uma pasta personalizada?] (<<<LINK59>>>)
- [Como posso usar modelos diferentes para diferentes tarefas?] (<<<LINK60>>>)
- [O bot congela enquanto faz trabalho pesado. Como posso descarregar isso?](<<<LINK61>>>)
- Não disparem! O que devo verificar?](<<<LINK62>>)
- [Como faço para instalar habilidades no Linux?] (<<<LINK63>>)
- [O OpenClaw pode executar tarefas em um cronograma ou continuamente em segundo plano?](<<<LINK64>>>)
- [Posso executar habilidades Apple/macOS somente do Linux?](<<<LINK65>>>)
- [Tem uma integração de Noção ou HeyGen?] (<<< HTML68>>>)
- [Como faço para instalar a extensão Chrome para aquisição do navegador?] (<<<LINK67>>)
- [Sandboxing e memória] (<<<<LINK68>>)
- [Existe um documento dedicado ao Sandboxing?] (<<<LINK69>>>)
- [Como faço para ligar uma pasta host na caixa de areia?] (<<<LINK70>>)
- [Como funciona a memória?] (<<<LINK71>>>)
- [A memória esquece-se das coisas. Como faço para ficar?](<<<LINK72>>)
- [A memória persiste para sempre? Quais são os limites?](<<<LINK73>>)
- [A pesquisa semântica de memória requer uma chave OpenAI API?](<<<LINK74>>)
- [Onde as coisas vivem no disco] (<<<LINK75>>>)
- [Todos os dados são usados com OpenClaw salvos localmente?](<<<LINK76>>)
- [Onde é que o OpenClaw armazena os seus dados?] (<<<LINK77>>)
- [Onde deve AGENTS.md / SOUL.md / UTILIZADOR.md / MEMORY.md viver?](<<LINK78>>)
- [Qual é a estratégia de backup recomendada?] (<<<LINK79>>)
- [Como faço para desinstalar completamente OpenClaw?] (<<<LINK80>>)
- [Os agentes podem trabalhar fora do espaço de trabalho?] (<<<LINK81>>>)
- [Estou em modo remoto - onde está a loja de sessão?] (<<<LINK82>>>)
- [Config basics] (<<<<LINK83>>>)
- [Que formato é a configuração? Onde está?](<<<LINK84>>>)
- [Eu defini <<CODE2>> (ou <<CODE3>>>) e agora nada escuta / a UI diz não autorizado](<<LINK85>>)
- [Por que preciso de um token no localhost agora?](<<<LINK86>>)
- [Tenho que reiniciar depois de mudar a configuração?] (<<<LINK87>>)
- [Como faço para ativar a pesquisa na web (e busca na web)?](<<<LINK88>>)
- [config.apply limpou minha configuração. Como posso recuperar e evitar isso?](<<<LINK89>>)
- [Como faço para executar um Gateway central com trabalhadores especializados em todos os dispositivos?] (<<<LINK90>>>)
- [O navegador OpenClaw pode ser executado sem cabeça?] (<<<LINK91>>)
- [Como usar Brave para o controle do navegador?] (<<<LINK92>>)
- [Gateways remotos + nós] (<<<LINK93>>)
- [Como os comandos se propagam entre Telegram, o gateway e nós?](<<<LINK94>>>)
- [Como meu agente pode acessar meu computador se o Gateway está hospedado remotamente?](<<<LINK95>>)
- [Tailscale está ligado mas não recebo respostas. E agora?](<<<LINK96>>)
- [Podem duas instâncias OpenClaw falar entre si (local + VPS)?](<<<LINK97>>>)
- [Preciso de VPSes separados para múltiplos agentes] (<<<LINK98>>>)
- [Existe um benefício para usar um nó em meu laptop pessoal em vez de SSH de um VPS?] (<<<LINK99>>)
- [Os nós executam um serviço de gateway?] (<<<LINK100>>>)
- [Existe uma maneira API / RPC de aplicar a configuração?](<<<LINK101>>>)
- [O que é uma configuração mínima “sane” para uma primeira instalação?](<<<LINK102>>>)
- [Como faço para configurar Tailscale em um VPS e conectar do meu Mac?] (<<<LINK103>>)
- [Como faço para conectar um nó Mac a um Gateway remoto (Tailscale Serve)?](<<LINK104>>)
- [Devo instalar em um segundo laptop ou simplesmente adicionar um nó?](<<<LINK105>>>)
- [Env vars e .env loading] (<<<LINK106>>>)
- [Como é que OpenClaw carrega variáveis de ambiente?] (<<<LINK107>>>)
- [“Eu comecei o Gateway através do serviço e meus env vars desapareceram.” E agora?](<<<LINK108>>)
- [Eu defini <<CODE4>>, mas o status dos modelos mostra “Shell env: off.” Porquê?](<<<LINK109>>)
- [Sessões e conversas múltiplas] (<<<LINK110>>>>)
- [Como começo uma conversa nova?] (<<<LINK111>>>)
- [Reset de sessões automaticamente se eu nunca enviar <<CODE5>>>>?] (<<LINK112>>>)
- [Existe uma maneira de fazer uma equipe de instâncias OpenClaw um CEO e muitos agentes] (<<<LINK113>>)
- Porque é que o contexto foi truncado? Como posso evitá-lo?](<<<LINK114>>>)
- [Como faço para reiniciar completamente OpenClaw mas mantê-lo instalado?](<<<LINK115>>>)
- [Estou recebendo erros de “contexto muito grande” - como faço para reiniciar ou compactar?](<<LINK116>>)
- [Por que estou vendo “pedido LLM rejeitado: messages.N.content.X.tool use.input: Campo requerido”?](<<LINK117>>>)
- [Porque estou a receber mensagens a cada 30 minutos?] (<<<LINK118>>>)
- [Preciso adicionar uma “conta bot” a um grupo WhatsApp?](<<<LINK119>>>)
- [Como faço para obter o JID de um grupo WhatsApp?] (<<<LINK120>>>)
- [Porque é que o OpenClaw não responde num grupo?](<<<LINK121>>>)
- [Os grupos/threads compartilham contexto com DMs?](<<<LINK122>>>)
- [Quantas áreas de trabalho e agentes posso criar?] (<<<LINK123>>)
- [Posso executar vários bots ou chats ao mesmo tempo (Slack), e como devo configurar isso?](<<<LINK124>>)
- [Modelos: predefinidos, selecção, pseudónimos, mudança] (<<<LINK125>>>)
- [O que é o “modelo padrão”?] (<<<LINK126>>>)
- [Que modelo recomenda?] (<<<LINK127>>>)
- [Como faço para mudar de modelo sem limpar minha configuração?] (<<<LINK128>>>)
- [Posso usar modelos auto- hospedados (llama.cpp, vLLM, Ollama)?](<<<LINK129>>)
- [O que OpenClaw, Flawd e Krill usam para modelos?](<<LINK130>>>)
- [Como faço para mudar de modelo na mosca (sem reiniciar)?](<<<LINK131>>>)
- [Posso usar GPT 5.2 para tarefas diárias e Codex 5.2 para codificação] (<<<LINK132>>>)
- [Por que eu vejo “Modelo ... não é permitido” e então nenhuma resposta?](<<<LINK133>>>)
- [Por que vejo “Modelo desconhecido: minimax/MiniMax-M2.1”?](<<LINK134>>)
- [Posso usar MiniMax como padrão e OpenAI para tarefas complexas?](<<<LINK135>>>)
- [Opus / soneto / gpt são atalhos incorporados?] (<<<LINK136>>>)
- [Como defino/sobrepor atalhos de modelos (aliases)?](<<<LINK137>>>)
- [Como faço para adicionar modelos de outros provedores como OpenRouter ou Z.AI?](<<<LINK138>>)
- [Modelo failover e “Todos os modelos falharam”](<<<LINK139>>)
- [Como funciona o failover?] (<<<LINK140>>>)
- [O que significa este erro?] (<<<LINK141>>>)
- [Fix checklist for <<CODE6>>>] (<<LINK142>>>)
- [Por que também tentou o Google Gemini e falhou?] (<<<LINK143>>>)
- [Perfis de autenticação: o que são e como gerenciá- los] (<<<LINK144>>>>)
- [O que é um perfil de autenticação?] (<<<LINK145>>>)
- [O que são IDs de perfil típicos?](<<<LINK146>>>)
- [Posso controlar qual perfil de autenticação é tentado primeiro?] (<<<LINK147>>>)
- [Chave OAuth vs API: qual é a diferença?](<<<LINK148>>>)
- [Porta: portas, “já em execução” e modo remoto](<<<LINK149>>>)
- [Que porta usa o Gateway?] (<<<LINK150>>>)
- [Porque é que <<CODE7>>> diz <<CODE8>>> mas <<CODE9>>>?](<<LINK151>>>>)
- [Porque é que <<CODE10>> mostra <<CODE11>>> e <<CODE12>> diferentes?] (<<LINK152>>>>)
- [O que significa “outra instância de gateway já está ouvindo”?](<<<LINK153>>>)
- [Como faço para executar OpenClaw em modo remoto (cliente se conecta a um Gateway em outro lugar)?](<<<LINK154>>>)
- [A UI Controle diz “não autorizado” (ou continua reconectando). E agora?](<<<LINK155>>)
- [Eu set <<CODE13>> mas ele não pode se ligar / nada escuta] (<<LINK156>>)
- [Posso executar vários Gateways na mesma máquina?] (<<<LINK157>>>)
- [O que significa “aperto de mão inválido” / código 1008?] (<<<LINK158>>>)
- [Logging e depuração] (<<<LINK159>>>)
- [Onde estão os registos?] (<<<LINK160>>>)
- [Como faço para iniciar/parar/iniciar o serviço Gateway?](<<<LINK161>>>)
- [Fechei meu terminal no Windows - como faço para reiniciar OpenClaw?] (<<<LINK162>>>)
- [A porta está aberta mas as respostas nunca chegam. O que devo verificar?](<<<LINK163>>)
- ["Desligado do gateway: nenhuma razão" - e agora?](<<<LINK164>>>)
- [Telegram setMyCommands falha com erros de rede. O que devo verificar?](<<<LINK165>>)
- [TUI não mostra saída. O que devo verificar?](<<<LINK166>>>)
- [Como parar completamente e iniciar o Gateway?] (<<LINK167>>>)
- [ELI5: <<CODE14>> vs <<CODE15>>>>](<<LINK168>>>)
- [Qual é a maneira mais rápida de obter mais detalhes quando algo falha?](<<<LINK169>>>)
- [Media & anexos] (<<<LINK170>>>)
- [Minha habilidade gerou uma imagem/PDF, mas nada foi enviado] (<<<LINK171>>>)
- [Controlo de segurança e acesso](<<<LINK172>>>)
- [É seguro expor OpenClaw a DMs de entrada?](<<<LINK173>>>)
- [A injecção imediata é apenas uma preocupação para os bots públicos?] (<<< HTML190>>>)
- [Se meu bot tem sua própria conta GitHub e-mail ou número de telefone] (<<<LINK175>>>)
- [Posso dar-lhe autonomia sobre as minhas mensagens de texto e é tão seguro] (<<<LINK176>>>>)
- [Posso usar modelos mais baratos para tarefas de assistente pessoal?](<<<LINK177>>)
- [Eu corri <<CODE16>> no Telegram, mas não consegui um código de pareamento](<<LINK178>>)
- [WhatsApp: vai enviar mensagens aos meus contactos? Como funciona o pareamento?](<<<LINK179>>)
- [Comandos de bate-papo, abortar tarefas e “não vai parar”](<<<LINK180>>)
- [Como paro as mensagens internas do sistema de mostrar no chat] (<<<LINK181>>)
- [Como faço para parar/cancelar uma tarefa em execução?] (<<<LINK182>>)
- [Como faço para enviar uma mensagem de discórdia do Telegram? (“Mensagem de contexto cruzado negado”)(<<<LINK183>>>)
- [Por que parece que o bot “ignores” mensagens de fogo rápido?](<<<LINK184>>>)

# # Primeiros 60 segundos se algo estiver partido

1. **Estatuto rápido (primeira verificação)**

   ```bash
   openclaw status
   ```

Resumo local rápido: OS + atualização, alcance de gateway/serviço, agentes/sessões, configuração do provedor + problemas de execução (quando gateway é alcançável).

2. **Relatório Pastável (seguro para partilhar) **

   ```bash
   openclaw status --all
   ```

Diagnóstico somente leitura com cauda de log (tokens editados).

3. **Daemon + estado do porto**

   ```bash
   openclaw gateway status
   ```

Mostra a capacidade de alcance do supervisor em tempo de execução vs RPC, o URL do alvo da sonda e qual configuração do serviço provavelmente utilizado.

4. ** Sondas profundas**

   ```bash
   openclaw status --deep
   ```

Executa verificações de saúde do gateway + sondas de provedor (requer um gateway acessível). Ver [Saúde] (<<<LINK0>>>).

5. **Carregar o último registo

   ```bash
   openclaw logs --follow
   ```

Se o RPC está para baixo, voltar para:

   ```bash
   tail -f "$(ls -t /tmp/openclaw/openclaw-*.log | head -1)"
   ```

Os registos de ficheiros estão separados dos registos de serviços; veja [Logging] (<<<LINK0>>) e [Troubleshooting] (<<LINK1>>).

6. ** Execute o médico (reparações)**

   ```bash
   openclaw doctor
   ```

Reparações/migrações config/state + executa verificações de saúde. Ver [Doctor] (<<<LINK0>>>).

7. **Snapshot Gateway**
   ```bash
   openclaw health --json
   openclaw health --verbose   # shows the target URL + config path on errors
   ```
Pergunta ao gateway em execução para um instantâneo completo (somente WS). Ver [Saúde] (<<<LINK0>>>).

# # Início rápido e configuração de primeira execução

Estou preso, qual é a maneira mais rápida de se desprender

Use um agente de IA local que pode **ver sua máquina**. Isso é muito mais eficaz do que pedir
em Discórdia, porque a maioria dos casos "Eu estou preso" são ** problemas de configuração local ou ambiente** que
Os ajudantes remotos não podem inspecionar.

- **Código de Claude**: https://www.anthropic.com/claude-code/
- **OpenAI Codex**: https://openai.com/codex/

Essas ferramentas podem ler o repo, executar comandos, inspecionar registros e ajudar a corrigir o nível de sua máquina
configuração (PATH, serviços, permissões, arquivos de autenticação). Dê-lhes o **checkout completo da fonte** via
a instalação hackable (git):

```bash
curl -fsSL https://openclaw.bot/install.sh | bash -s -- --install-method git
```

Isto instala OpenClaw ** a partir de um git checkout**, para que o agente possa ler o código + documentos e
razão sobre a versão exata que você está executando. Você sempre pode mudar para estável mais tarde
Reexecutando o instalador sem <<CODE0>>>.

Dica: peça ao agente para ** planejar e supervisionar** a correção (passo a passo), em seguida, execute apenas o
comandos necessários. Isso mantém as mudanças pequenas e mais fáceis de auditoria.

Se você descobrir um erro ou correção real, por favor, arquive um problema do GitHub ou envie um PR:
https://github.com/openclaw/openclaw/issues
https://github.com/openclaw/openclaw/pulls

Comece com estes comandos (compartilhar saídas ao pedir ajuda):

```bash
openclaw status
openclaw models status
openclaw doctor
```

O que eles fazem:

- <<CODE0>>: instantâneo rápido do gateway/saúde do agente + configuração básica.
- <<CODE1>>: verifica a disponibilidade do fornecedor + modelo.
- <<CODE2>>: valida e repara problemas comuns de configuração/estado.

Outras verificações CLI úteis: <<CODE0>>, <<CODE1>>,
<<CODE2>>, <<CODE3>>.

Ciclo de depuração rápido: [Primeiro 60 segundos se algo estiver quebrado] (<<<LINK0>>>).
Instalar docs: [Instalar](<<<LINK1>>), [Installer flags](<<LINK2>>>>), [Atualizar](<<<LINK3>>>>).

## # Qual é a maneira recomendada de instalar e configurar OpenClaw

O repo recomenda correr a partir do código fonte e usar o assistente de integração:

```bash
curl -fsSL https://openclaw.bot/install.sh | bash
openclaw onboard --install-daemon
```

O assistente também pode construir ativos UI automaticamente. Depois de embarcar, você normalmente executa o Gateway no porto **18789**.

Da fonte (contributores/dev):

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
pnpm ui:build # auto-installs UI deps on first run
openclaw onboard
```

Se você ainda não tem uma instalação global, execute-a via <<CODE0>>.

Como é que abro o painel depois de entrar?

O assistente agora abre seu navegador com uma URL tokenized do painel logo após a integração e também imprime o link completo (com token) no resumo. Mantenha a aba aberta; se não foi lançada, copie/copie o URL impresso na mesma máquina. Os itens permanecem locais para o seu host- nada é obtido do navegador.

### Como faço para autenticar o token do painel em localhost vs remoto

**Host local (mesma máquina):**

- Abrir <<CODE0>>>.
- Se pedir autorização, execute <<CODE1>> e use o link tokenized (<<CODE2>>).
- O token é o mesmo valor que <<CODE3>> (ou <<CODE4>>>) e é armazenado pela IU após a primeira carga.

** Não na máquina local:**

- **Tailscale Serve** (recomendado): manter a ligação loopback, executar <<CODE0>>>, abrir <<CODE1>>. Se <<CODE2>> for <<CODE3>>, os cabeçalhos de identidade satisfazem a autenticação (sem token).
- **Tailnet binding**: executar <<CODE4>>, abrir <<CODE5>>, colar token em configurações de painel.
- ** Túnel SHSS**: <<CODE6> então aberto <<CODE7>>> de <<CODE8>>.

Ver [Dashboard](<<<LINK0>>) e [Superfícies Web](<<LINK1>>>) para os modos de ligação e detalhes de autenticação.

De que tempo de corrida preciso

Node **>= 22** é necessário. <<CODE0>> é recomendado. Bun é ** não recomendado** para o Gateway.

Será que funciona em Framboesa Pi

Sim. O Gateway é leve - lista de documentos **512MB-1GB RAM**, **1 core**, e cerca de **500MB**
disco como suficiente para uso pessoal, e note que um **Raspberry Pi 4 pode executá-lo**.

Se você quiser headroom extra (logs, mídia, outros serviços), **2GB é recomendado**, mas é
Não é um mínimo difícil.

Dica: um pequeno Pi / VPS pode hospedar o Gateway, e você pode emparelhar ** nós** em seu laptop / telefone para
Ecrã/câmara/canvas local ou execução de comandos. Ver [Nodes] (<<<LINK0>>>).

# # # Qualquer dica para instalação de framboesa Pi

Versão curta: funciona, mas esperar bordas ásperas.

- Use um SO de **64 bits e mantenha Node >= 22.
- Prefere a instalação **hackable (git)** para que você possa ver logs e atualizar rapidamente.
- Comece sem canais/competências, depois adicione-os um por um.
- Se você atingir problemas binários estranhos, geralmente é um problema de compatibilidade ARM**.

Docs: [Linux] (<<<LINK0>>), [Install] (<<LINK1>>>).

# # # Está preso em acordar o meu amigo a bordo não vai chocar

Essa tela depende do portal ser acessível e autenticado. O TUI também envia
Acorda, meu amigo, automaticamente na primeira escotilha. Se você ver essa linha com ** nenhuma resposta**
O agente nunca fugiu.

1. Reinicie o portal:

```bash
openclaw gateway restart
```

2. Verificar status + autenticação:

```bash
openclaw status
openclaw models status
openclaw logs --follow
```

3. Se ainda estiver pendurado, corra:

```bash
openclaw doctor
```

Se o Gateway for remoto, certifique-se de que a conexão túnel/tailscale está acima e que a UI
está apontada para a porta direita. Ver [Acesso remoto] (<<<LINK0>>>).

# # # Posso migrar minha configuração para uma nova máquina Mac mini sem refazer a bordo

Sim. Copie o diretório ** state** e **workspace**, então execute Doctor uma vez. Isto
mantém o seu bot “ exatamente o mesmo” (memória, histórico de sessão, autenticação e canal
estado) desde que você copie ** ambas as localizações**:

1. Instale Openclaw na nova máquina.
2. Cópia <<CODE0>> (padrão: <<CODE1>>>) da máquina antiga.
3. Copie seu espaço de trabalho (padrão: <<CODE2>>>).
4. Executar <<CODE3>> e reiniciar o serviço Gateway.

Isso preserva config, perfis de autenticação, créditos do WhatsApp, sessões e memória. Se você estiver dentro
modo remoto, lembre-se que o host gateway possui a loja de sessão e espaço de trabalho.

**Importante:** se você apenas commit/push seu espaço de trabalho para GitHub, você está suportando
up **memory + bootstrap files**, mas **not** session history or auth. Aqueles que vivem.
<<CODE0>> (por exemplo <<CODE1>>>).

Relacionados: [Migrando](<<<LINK0>>), [Onde as coisas vivem no disco](<<LINK1>>),
[Espaço de trabalho do agente](<<<LINK2>>), [Doctor](<<LINK3>>>),
[Modo remoto] (<<<LINK4>>>>).

# # # Onde vejo o que há de novo na última versão

Verifique o changelog do GitHub:
https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md

As entradas mais novas estão no topo. Se a seção superior estiver marcada **Unreleased**, a próxima data
seção é a versão mais recente enviada. As inscrições são agrupadas por **Highlights**, **Changes**, e
**Fixes** (mais documentos/outras seções quando necessário).

## # Eu não posso acessar Docs.openclaw.ai erro SSL O que agora

Algumas conexões Comcast/Xfinity bloqueiam incorretamente <<CODE0>> via Xfinity
Segurança Avançada. Desative-o ou allowlist <<CODE1>>, então tente novamente. Mais
detalhe: [Troubleshooting] (<<<LINK0>>>).
Por favor, ajude-nos a desbloqueá-lo reportando aqui: https://spa.xfinity.com/check url status.

Se você ainda não pode chegar ao site, os documentos são espelhados no GitHub:
https://github.com/openclaw/openclaw/tree/main/docs

Qual é a diferença entre estável e beta

**Stable** e **beta** são **npm dist-tags**, não linhas de código separadas:

- <<CODE0> = estável
- <<CODE1>> = compilação precoce para testes

Nós enviamos construções para **beta**, testá-los, e uma vez que uma construção é sólida nós **promover
a mesma versão para <<CODE0>>**. É por isso que beta e estável pode apontar para o
* mesma versão**.

Veja o que mudou:
https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md

## # Como faço para instalar a versão beta e qual é a diferença entre beta e dev

**Beta** é a dist-tag npm <<CODE0>> (pode corresponder <<CODE1>>).
**Dev** é a cabeça em movimento de <<CODE2>> (git); quando publicado, ele usa a npm dist-tag <<CODE3>>.

Um-liners (macOS/Linux):

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.bot/install.sh | bash -s -- --beta
```

```bash
curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.bot/install.sh | bash -s -- --install-method git
```

Instalador do Windows (PowerShell):
https://openclaw.ai/install.ps1

Mais detalhes: [Canais de desenvolvimento](<<<LINK0>>) e [Fixadores de instalação](<<LINK1>>>).

# # # Quanto tempo é que a instalação e a integração normalmente levam

Guia bruto:

- **Instalar:** 2-5 minutos
- ** Onboarding:** 5-15 minutos dependendo de quantos canais/modelos você configurar

Se for suspenso, utilize [Installer sticed] (<<<LINK0>>>)
e o ciclo de depuração rápido em [Im sticked] (<<<LINK1>>>).

Como faço para tentar as últimas partes

Duas opções:

1. **Dev canal (git checkout):**

```bash
openclaw update --channel dev
```

Isso muda para o ramo <<CODE0>> e atualizações da fonte.

2. ** Instalar hackable (do site do instalador):**

```bash
curl -fsSL https://openclaw.bot/install.sh | bash -s -- --install-method git
```

Isso lhe dá um repo local que você pode editar, em seguida, atualizar via git.

Se preferir um clone limpo manualmente, use:

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
```

Documentos: [Atualização] (<<<LINK0>>), [Canais de desenvolvimento] (<<LINK1>>),
[Instalar] (<<<LINK2>>>).

# # # Instalador preso Como posso obter mais feedback

Executar novamente o instalador com **verbose output**:

```bash
curl -fsSL https://openclaw.bot/install.sh | bash -s -- --verbose
```

Instalar Beta com verbose:

```bash
curl -fsSL https://openclaw.bot/install.sh | bash -s -- --beta --verbose
```

Para uma instalação hackeável (git):

```bash
curl -fsSL https://openclaw.bot/install.sh | bash -s -- --install-method git --verbose
```

Mais opções: [Flags de instalação](<<<LINK0>>>).

# # # # Windows install diz git não encontrado ou openclaw não reconhecido

Dois problemas comuns do Windows:

**1) erro npm git / git não encontrado**

- Instale **Git para Windows** e certifique-se de que <<CODE0> está em seu PATH.
- Fecha e reabre o PowerShell, e depois repete o instalador.

**2) openclaw não é reconhecido após a instalação**

- A sua pasta global não está no PATH.
- Verifica o caminho.
  ```powershell
  npm config get prefix
  ```
- Garantir que <<CODE0> está em PATH (na maioria dos sistemas está <<CODE1>>>).
- Fechar e reabrir PowerShell depois de atualizar PATH.

Se você quiser a configuração mais suave do Windows, use **WSL2** em vez do Windows nativo.
Docs: [Windows](<<<LINK0>>>).

Os médicos não responderam à minha pergunta. Como é que consigo uma resposta melhor?

Use a instalação **hackable (git)** para que você tenha a fonte completa e documentos localmente, em seguida, pergunte
seu bot (ou Claude/Codex)  a partir dessa pasta  para que ele possa ler o repo e responder com precisão.

```bash
curl -fsSL https://openclaw.bot/install.sh | bash -s -- --install-method git
```

Mais detalhes: [Instalar](<<<LINK0>>>) e [bandeiras Installer](<<<LINK1>>).

### Como faço para instalar Openclaw no Linux

Resposta curta: siga o guia Linux e execute o assistente de integração.

- Caminho rápido do Linux + serviço de instalação: [Linux](<<<LINK0>>).
- Passo a passo: [Começar] (<<<LINK1>>>).
- Instalador + atualizações: [Instalar e atualizar] (<<<LINK2>>>).

Como faço para instalar Openclaw em um VPS

Qualquer VPS Linux funciona. Instale no servidor e use SSH/Tailscale para chegar ao Gateway.

Guias: [exe.dev](<<<LINK0>>), [Hetzner](<<LINK1>>>>), [Fly.io](<<LINK2>>>>).
Acesso remoto: [Portão remoto] (<<<LINK3>>>).

## # Onde estão os guias de instalação do CloudVPS

Mantemos um hub de hospedagem** com os provedores comuns. Escolha um e siga o guia:

- [Alojamento VPS] (<<<LINK0>>>) (todos os fornecedores num só local)
- [Fly.io] (<<<LINK1>>>)
- [Hetzner] (<<<LINK2>>>)
- [exe.dev] (<<<LINK3>>>)

Como funciona na nuvem: o **Gateway é executado no servidor**, e você a acessa
do seu laptop/telefone através da interface de controle (ou escala de cauda/SSH). Seu estado + espaço de trabalho
vive no servidor, então trate o host como a fonte da verdade e faça backup dela.

Você pode emparelhar ** nós** (Mac/iOS/Android/headless) para que a nuvem Gateway para acessar
tela local/câmera/canvas ou executar comandos em seu laptop, mantendo o
Portão na nuvem.

Hub: [Plataformas] (<<<LINK0>>>). Acesso remoto: [Portão remoto] (<<<LINK1>>>).
Nós: [Nos] (<<<LINK2>>), [Nos CLI] (<<LINK3>>>).

# # # Posso pedir ao Openclaw para se atualizar

Resposta curta: **possível, não recomendada**. O fluxo de atualização pode reiniciar o
Gateway (que deixa cair a sessão ativa), pode precisar de um git checkout limpo, e
pode solicitar confirmação. Mais seguro: execute atualizações de uma shell como operador.

Usar o CLI:

```bash
openclaw update
openclaw update status
openclaw update --channel stable|beta|dev
openclaw update --tag <dist-tag|version>
openclaw update --no-restart
```

Se você deve automatizar de um agente:

```bash
openclaw update --yes --no-restart
openclaw gateway restart
```

Docs: [Atualização] (<<<LINK0>>), [Atualização] (<<LINK1>>>>).

# # O que faz o assistente de bordo realmente

<<CODE0> é o caminho de configuração recomendado. Em ** modo local** ele te leva através:

- **Modelo/auth setup** (Anthropic **setup-token** recomendado para assinaturas Claude, OpenAI Codex OAuth suportado, chaves API opcional, LM Studio modelos locais suportados)
- ** Local de trabalho** + arquivos bootstrap
- ** Configuração da porta** (bind/port/auth/tailscale)
- **Fornecedores** (WhatsApp, Telegram, Discord, Mattermost (plugin), Signal, iMessage)
- ** Daemon install** (LaunchAgent on macOS; systemd user unit on Linux/WSL2)
- ** Controlos de saúde** e **Selecção de competências**

Ele também avisa se o seu modelo configurado é desconhecido ou ausente.

Preciso de uma assinatura Claude ou OpenAI para executar isto

Não. Você pode executar OpenClaw com **API chaves** (Anthropic/OpenAI/outros) ou com
**Somente modelos locais** para que seus dados permaneçam em seu dispositivo. Assinaturas (Claude
Pro/Max ou OpenAI Codex) são formas opcionais de autenticar esses provedores.

Docs: [Anthropic] (<<<LINK0>>), [OpenAI] (<<LINK1>>),
[Modelos locais](<<<LINK2>>), [Modelos](<<LINK3>>>).

## # Posso usar assinatura Claude Max sem uma chave API

Sim. Você pode autenticar com um **setup-token**
em vez de uma chave API. Este é o caminho da subscrição.

Subscrições Claude Pro/Max ** não incluem uma chave de API**, então esta é a
abordagem correcta para as contas de subscrição. Importante: você deve verificar com
Anthropic que este uso é permitido sob sua política de assinatura e termos.
Se você quiser o caminho mais explícito e suportado, use uma chave Anthropic API.

## # Como funciona a instalação antrópica

<<CODE0> gera uma string **token** via Claude Code CLI (não está disponível no console web). Você pode executá-lo em ** qualquer máquina**. Escolha ** Token antrópico (paste setup-token)** no assistente ou cole-o com <<CODE1>>. O token é armazenado como um perfil de autenticação para o provedor **antrópico** e usado como uma chave API (sem atualização automática). Mais detalhes: [OAuth] (<<<LINK0>>>).

Onde é que encontro uma agenda antrópica

É **não** na Consola Antrópica. A configuração é gerada pelo código **Claude CLI** em ** qualquer máquina**:

```bash
claude setup-token
```

Copie o token que ele imprime, em seguida, escolha **Token antrópico (paste setup-token)** no assistente. Se você quiser executá-lo no host gateway, use <<CODE0>>>. Se você correu <<CODE1>> em outro lugar, cole-o no host gateway com <<CODE2>>. Ver [Antrópico] (<<<LINK0>>>>).

## # Você apoia Claude assinatura auth (Claude Pro/Max)

Sim — via **setup-token**. O OpenClaw não reutiliza mais tokens Claude Code CLI OAuth; use uma chave API de configuração ou Anthropic. Gere o token em qualquer lugar e cole-o na máquina de gateway. Ver [Antrópico] (<<<LINK0>>) e [OAuth] (<<LINK1>>>).

Nota: O acesso à assinatura de Claude é regido pelos termos da Anthropic. Para a produção ou cargas de trabalho multi-usuários, as chaves API são geralmente a escolha mais segura.

## # Por que estou vendo HTTP 429 ratelimberror da Anthropic

Isso significa que seu limite de cota/taxa antrópica** está esgotado para a janela atual. Se você
utilizar uma assinatura **Claude** (setup-token ou Claude Code OAuth), esperar pela janela para
redefinir ou atualizar seu plano. Se você usar uma chave **Anthropic API **, verifique a Console Anthropic
para utilização/billing e aumentar os limites, conforme necessário.

Dica: defina um modelo **fallback** para que OpenClaw possa continuar respondendo enquanto um provedor é limitado por taxa.
Ver [Modelos] (<<<LINK0>>) e [OAuth] (<<LINK1>>>).

O AWS Bedrock é suportado

Sim - via **Amazon Bedrock (Converso)** provedor com **configuração manual**. Você deve fornecer credenciais/região AWS no host gateway e adicionar uma entrada do provedor Bedrock em sua configuração de modelos. Ver [Amazon Bedrock] (<<<LINK0>>) e [Fornecedores de modelos] (<<LINK1>>>). Se preferir um fluxo de chave gerenciado, um proxy compatível com OpenAI na frente do Bedrock ainda é uma opção válida.

Como funciona o Codex Auth?

OpenClaw suporta **OpenAI Code (Codex)** via OAuth (ChatGPT sign-in). O assistente pode executar o fluxo OAuth e definirá o modelo padrão para <<CODE0> quando apropriado. Ver [Fornecedores de modelos] (<<<LINK0>>) e [Wizard] (<<LINK1>>).

## # Você suporta OpenAI assinatura auth Codex OAuth

Sim. OpenClaw suporta totalmente **OpenAI Code (Codex) subscription OAuth**. O assistente de integração
pode executar o fluxo de OAuth para você.

Ver [OAuth] (<<<LINK0>>), [Fornecedores de modelos] (<<LINK1>>>), e [Wizard] (<<LINK2>>>).

Como faço para montar o Gemini CLI OAuth

Gemini CLI usa um fluxo de autenticação **plugin**, não um ID do cliente ou segredo em <<CODE0>>.

Passos:

1. Active o plugin: <<CODE0>>
2. Login: <<CODE1>>

Isto armazena os tokens OAuth em perfis de autenticação na máquina de gateway. Detalhes: [Fornecedores de modelos](<<<LINK0>>>).

## # É um modelo local OK para conversas casuais

Normalmente não. OpenClaw precisa de grande contexto + segurança forte; pequenas cartas truncam e vazam. Se você precisar, execute o **largest** MiniMax M2.1 build que você pode localmente (LM Studio) e veja [/gateway/local-models](<<<LINK0>>>). Modelos menores/quantizados aumentam o risco de injeção imediata - ver [Segurança] (<<<LINK1>>>).

### Como faço para manter o tráfego de modelo hospedado em uma região específica

Escolha os parâmetros definidos na região. OpenRouter expõe opções hospedadas pelos EUA para MiniMax, Kimi e GLM; escolha a variante hospedada pelos EUA para manter dados na região. Você ainda pode listar Anthropic/OpenAI ao lado destes usando <<CODE0> para que os fallbacks permaneçam disponíveis respeitando o provedor regional que você selecionar.

# # # Tenho de comprar um Mac Mini para instalar isto

Não. O OpenClaw é executado no macOS ou Linux (Windows via WSL2). Um mini Mac é opcional - algumas pessoas
comprar um como um anfitrião sempre, mas um pequeno VPS, servidor doméstico, ou Raspberry Pi-class caixa funciona também.

Você só precisa de um Mac **para ferramentas somente para macOS**. Para o iMessage, você pode manter o Gateway no Linux
e executar <<CODE0>> em qualquer Mac sobre SSH apontando <<CODE1>> para um invólucro SSH.
Se você quiser outras ferramentas apenas para macOS, execute o Gateway em um Mac ou emparelhe um nó macOS.

Docs: [iMessage](<<<LINK0>>), [Nodes](<<LINK1>>>>), [Modo remoto Mac](<<LINK2>>>>).

Preciso de um mini Mac para suporte iMessage

Você precisa de ** algum dispositivo macOS** assinado em Mensagens. Faz ** não tem que ser um mini Mac -
qualquer Mac funciona. As integrações iMessage do OpenClaw são executadas no macOS (BlueBubbles ou <<CODE0>>), enquanto
O portal pode correr para outro lado.

Configuração comum:

- Execute o Gateway no Linux/VPS, e ponto <<CODE0>> em uma embalagem SSH que
roda <<CODE1>> no Mac.
- Execute tudo no Mac se quiser a configuração mais simples de uma máquina.

Documentos: [iMessage] (<<<LINK0>>), [BlueBubbles] (<<LINK1>>),
[Modo remoto Mac] (<<<LINK2>>>).

# # # Se eu comprar um mini Mac para executar OpenClaw posso conectá-lo ao meu MacBook Pro

Sim. O mini **Mac pode executar o Gateway**, e seu MacBook Pro pode se conectar como um
**Node** (dispositivo de acompanhamento). Nós não executar o Gateway - eles fornecem extra
capacidades como tela/câmera/canvas e <<CODE0>> nesse dispositivo.

Padrão comum:

- Gateway no Mac mini (sempre-on).
- MacBook Pro executa o aplicativo macOS ou um host de nó e pares para o Gateway.
- Utilizar <<CODE0>>/ <<CODE1>> para o ver.

Docs: [Nodes] (<<<LINK0>>), [Nodes CLI] (<<LINK1>>>).

Posso usar o Bun?

Bun é ** não recomendado**. Vemos bugs em tempo de execução, especialmente com WhatsApp e Telegram.
Use **Node** para gateways estáveis.

Se ainda quiser experimentar com o Bun, faça-o num portal de não-produção
sem WhatsApp/Telegram.

# # # Telegram o que vai em permitirDe

<<CODE0> é ** ID do utilizador do Telegrama do remetente humano** (numérico, recomendado) ou <<CODE1>>>. Não é o nome de usuário bot.

Mais seguro (sem bot de terceiros):

- DM o seu bot, então execute <<CODE0>>> e leia <<CODE1>>>>.

API oficial do Bot:

- DM seu bot, em seguida, chamar <<CODE0>>> e ler <<CODE1>>>.

Terceiros (menos privados):

- DM <<CODE0>> ou <<CODE1>>>.

Ver [/canais/telegrama] (<<<LINK0>>>).

## # Pode várias pessoas usar um número WhatsApp com diferentes instâncias OpenClaw

Sim, via **Roteamento multiagente**. Ligar o WhatsApp de cada remetente ** (peer <<CODE0>>, remetente E.164 like <<CODE1>>) a um diferente <<CODE2>>>, então cada pessoa tem sua própria área de trabalho e loja de sessão. As respostas ainda vêm da mesma conta do WhatsApp**, e o controle de acesso ao DM (<<<CODE3>> / <<CODE4>>) é global por conta do WhatsApp. Ver [Roteamento Multi-Agente] (<<<LINK0>>) e [WhatsApp](<<LINK1>>).

## # Posso executar um agente de chat rápido e um Opus para agente de codificação

Sim. Use roteamento multi-agente: dê a cada agente seu próprio modelo padrão e, em seguida, ligue rotas de entrada (conta do provedor ou pares específicos) a cada agente. O exemplo de configuração vive em [Multi-Agent Routing] (<<<LINK0>>). Ver também [Modelos] (<<<LINK1>>) e [Configuração] (<<LINK2>>).

O Homebrew trabalha no Linux?

Sim. Homebrew suporta Linux (Linuxbrew). Configuração rápida:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.profile
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
brew install <formula>
```

Se você executar OpenClaw via systemd, certifique-se de que o PATH de serviço inclui <<CODE0>> (ou seu prefixo de cerveja) então <<CODE1>>-instalado ferramentas resolver em shells não-login.
Recentes compilações também preparam bin dirs comuns de usuários em serviços de sistema Linux (por exemplo <<CODE2>>, <<CODE3>>, <<CODE4>>>, <<CODE5>>) e honra <<CODE6>>, <<CODE7>>>, <<CODE8>>>, <<CODE9>>, <HTML10>>>, <HTML11>>>>, e <<CODE12>>>>> quando definido.

## # Qual é a diferença entre a instalação git hackable e a instalação npm

- **Hackable (git) install:** full source checkout, editável, melhor para contribuidores.
Você executa builds localmente e pode patch code/docs.
- **npm install:** global CLI install, no repo, best for “just execute it.”
As actualizações vêm das dist-tags do npm.

Docs: [Começando](<<<LINK0>>), [Atualizando](<<LINK1>>>).

## # Posso trocar entre npm e git instala mais tarde

Sim. Instale o outro sabor e, em seguida, execute o Doctor para que os pontos de serviço de gateway no novo ponto de entrada.
Isto **não exclui os seus dados** - só altera a instalação do código OpenClaw. Seu estado
(<<<CODE0>>) e o espaço de trabalho (<<CODE1>>>) permanecem intocados.

Desde npm → git:

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
openclaw doctor
openclaw gateway restart
```

De git → npm:

```bash
npm install -g openclaw@latest
openclaw doctor
openclaw gateway restart
```

O médico detecta um ponto de entrada de gateway e se oferece para reescrever a configuração do serviço para corresponder à instalação atual (use <<CODE0>> em automação).

Dicas de backup: veja [Estratégia de backup] (<<<LINK0>>).

# # Devo usar o portal no meu portátil ou um VPS

Resposta curta: ** se você quiser confiabilidade 24/7, use um VPS**. Se você quiser o
fricção mais baixa e você está bem com sono / reinicialize, executá-lo localmente.

**Laptop (porta local)**

- ** Prós:** sem custo do servidor, acesso direto a arquivos locais, janela do navegador ao vivo.
- **Cons:** sleep/network drops = desligamentos, atualizações/reboots do sistema operacional interrompem, devem ficar acordados.

** VPS / nuvem**

- ** Prós:** sempre on, rede estável, sem problemas de sono laptop, mais fácil de manter em execução.
- **Cons:** muitas vezes executar sem cabeça (usar capturas de tela), acesso a arquivos remotos apenas, você deve SSH para atualizações.

** Nota específica do OpenClaw:** WhatsApp/Telegram/Slack/Mattermost (plugin)/Discord all work fine from a VPS. A única troca real é ** navegador sem cabeça** vs uma janela visível. Ver [Browser] (<<<LINK0>>>).

**Recomendado padrão:** VPS se você tivesse desligamentos de gateway antes. Local é ótimo quando você está usando ativamente o Mac e quer acesso a arquivos locais ou automação de interface com um navegador visível.

## # Quão importante é executar Openclaw em uma máquina dedicada

Não exigido, mas ** recomendado para confiabilidade e isolamento**.

- **Host dedicado (VPS/Mac mini/Pi):** sempre-on, menos interrupções de sono/reboot, permissões mais limpas, mais fácil de continuar funcionando.
- ** laptop/desktop compartilhado:** totalmente bom para testes e uso ativo, mas espere pausas quando a máquina dorme ou atualiza.

Se você quiser o melhor dos dois mundos, mantenha o Gateway em um host dedicado e emparelhe seu laptop como um **node** para as ferramentas locais de tela/câmera/exec. Ver [Nodes] (<<<LINK0>>>).
Para orientação em matéria de segurança, consultar [Segurança] (<<<LINK1>>>).

## # Quais são os requisitos mínimos de VPS e OS recomendados

Openclaw é leve. Para um Gateway básico + um canal de chat:

- ** No mínimo absoluto:** 1 vCPU, 1GB RAM, ~500MB disco.
- ** Recomendado:** 1-2 vCPU, 2GB RAM ou mais para headroom (logs, mídia, múltiplos canais). As ferramentas de nó e a automação do navegador podem ter fome de recursos.

OS: use **Ubuntu LTS** (ou qualquer Debian/Ubuntu moderno). O caminho de instalação do Linux é melhor testado lá.

Docs: [Linux](<<<LINK0>>), [VPS hosting](<<LINK1>>>).

# # # Posso executar Openclaw em uma VM e quais são os requisitos

Sim. Trate uma VM como uma VPS: ela precisa estar sempre ligada, alcançável e ter o suficiente
RAM para o Gateway e quaisquer canais que você ativar.

Orientação inicial:

- ** No mínimo absoluto:** 1 vCPU, 1GB de RAM.
- **Recomendado:** 2GB de RAM ou mais se você executar vários canais, automação do navegador ou ferramentas de mídia.
- ** OS:** Ubuntu LTS ou outro Debian/Ubuntu moderno.

Se você estiver no Windows, **WSL2 é a configuração de estilo VM mais fácil** e tem a melhor ferramenta
compatibilidade. Veja [Windows](<<LINK0>>), [VPS hosting](<<LINK1>>>).
Se você estiver executando macOS em uma VM, veja [macOS VM](<<<LINK2>>>).

# # O que é Openclaw?

## O que é Openclaw em um parágrafo

Openclaw é um assistente pessoal de IA que você executa em seus próprios dispositivos. Ele responde nas superfícies de mensagens que você já usa (WhatsApp, Telegram, Slack, Mattermost (plugin), Discord, Google Chat, Signal, iMessage, WebChat) e também pode fazer voz + tela ao vivo em plataformas suportadas. O **Gateway** é o plano de controle sempre-no; o assistente é o produto.

Qual é a proposta de valor

Openclaw não é "apenas um papel Claude." É um avião de controle **local-first** que permite executar um
assistente capaz em ** seu próprio hardware**, acessível a partir dos aplicativos de chat que você já usa, com
sessões de estado, memória e ferramentas - sem passar o controle de seus fluxos de trabalho para um hospedado
SaaS.

Destaques:

- **Seus dispositivos, seus dados:** execute o Gateway onde quiser (Mac, Linux, VPS) e mantenha o
espaço de trabalho + histórico de sessão local.
- ** Canais reais, não uma caixa de areia web:** WhatsApp/Telegram/Slack/Discord/Sinal/iMessage/etc,
mais voz móvel e tela em plataformas suportadas.
- **Modelo de diagnóstico:** use Anthropic, OpenAI, MiniMax, OpenRouter, etc., com roteamento per-agent
e fracasso.
- ** Opção somente local:** execute modelos locais para que **todos os dados possam permanecer em seu dispositivo** se você quiser.
- ** Roteamento multi- agente:** Agentes separados por canal, conta ou tarefa, cada um com o seu próprio
espaço de trabalho e padrões.
- ** Código aberto e hackeável:** inspecionar, estender e self-host sem bloqueio do fornecedor.

Docs: [Gateway](<<<LINK0>>), [Canais](<<LINK1>>>>), [Multi-agent](<<LINK2>>>),
[Memória] (<<<LINK3>>>).

Acabei de preparar o que devo fazer primeiro

Bons primeiros projectos:

- Construir um site (WordPress, Shopify, ou um site estático simples).
- Prototipe um aplicativo móvel (de fora, telas, plano API).
- Organize arquivos e pastas (limpeza, nomeação, marcação).
- Conecte o Gmail e automatize resumos ou acompanhamentos.

Ele pode lidar com grandes tarefas, mas funciona melhor quando você dividi-los em fases e
utilizar subagentes para trabalhos paralelos.

## # Quais são os cinco melhores casos de uso diário para Openclaw

Todos os dias vencem normalmente como:

- **Reuniões pessoais:** resumos de caixa de entrada, calendário e notícias que você se importa.
- **Pesquisa e redação:** pesquisa rápida, resumos e primeiros rascunhos para e-mails ou documentos.
- **Lembranças e acompanhamentos:** cron ou batimentos cardíacos impulsionados empurrão e checklists.
- Automatização do navegador:** preenchimento de formulários, coleta de dados e repetição de tarefas web.
- **Cross device coordination:** envie uma tarefa do seu telefone, deixe o Gateway executá-la em um servidor e obtenha o resultado de volta no chat.

## # Pode OpenClaw ajudar com anúncios e blogs de liderança para um SaaS

Sim para **pesquisa, qualificação e redação**. Ele pode digitalizar sites, construir listas curtas,
resumir perspectivas, e escrever outreach ou anúncio copiar rascunhos.

Para ** outreach ou anúncios **, mantenha um humano no loop. Evite spam, siga as leis locais e
políticas de plataforma, e rever qualquer coisa antes de ser enviado. O padrão mais seguro é deixar
Openclaw rascunho e você aprova.

Docs: [Segurança] (<<<LINK0>>>).

## # Quais são as vantagens contra Claude Code para desenvolvimento web

OpenClaw é um ** assistente pessoal** e camada de coordenação, não uma substituição do IDE. Utilização
Código Claude ou Codex para o laço de codificação direta mais rápido dentro de um repo. Usar Openclaw quando você
quer memória durável, acesso entre dispositivos e orquestração de ferramentas.

Vantagens:

- ** Memória persistente + espaço de trabalho** entre sessões
- ** Acesso multiplataforma** (WhatsApp, Telegram, TUI, WebChat)
- **Orquestração de ferramentas** (browser, arquivos, agendamento, ganchos)
- ** Sempre no Gateway** (correr em um VPS, interagir de qualquer lugar)
- **Nodes** para navegador/tela/câmera/exec local

Apresentação: https://openclaw.ai/showcase

# # Habilidades e automação

## # Como faço para personalizar as habilidades sem manter o acordo sujo

Usar sobreposições gerenciadas em vez de editar a cópia do repo. Coloque as suas alterações em <<CODE0>> (ou adicione uma pasta via <<CODE1>>> em <<CODE2>>). Precedência é <<CODE3>> > <<CODE4>> > empacotada, assim que gerencia sobreposições ganhar sem tocar git. Apenas edições a montante devem viver no repositório e sair como RPs.

# # # Posso carregar habilidades de uma pasta personalizada

Sim. Adicionar diretórios extras via <<CODE0>> em <<CODE1>> (mais baixa precedência). A precedência padrão permanece: <<CODE2>> → <<CODE3> → bundled → <<CODE4>>. <<CODE5> instala-se em <<CODE6>> por padrão, que OpenClaw trata como <<CODE7>>.

## # Como posso usar modelos diferentes para diferentes tarefas

Hoje os padrões suportados são:

- **Trabalhos de Cron**: trabalhos isolados podem definir um <<CODE0>> sobreposição por trabalho.
- **Sub-agentes**: tarefas de rota para separar agentes com diferentes modelos padrão.
- **Comutador sob demanda**: use <<CODE1> para alternar o modelo de sessão atual a qualquer momento.

Veja [Trabalhos de Cron](<<<LINK0>>), [Roteamento Multi-Agente](<<LINK1>>>), e [Comandos de Slash](<<LINK2>>>>).

O robô congela enquanto faz um trabalho pesado.

Use **sub-agentes** para tarefas longas ou paralelas. Subagentes executados na sua própria sessão,
retornar um resumo, e manter seu chat principal responsivo.

Peça ao seu bot para "promover um sub-agente para esta tarefa" ou use <<CODE0>>.
Use <<CODE1>> em chat para ver o que o Gateway está fazendo agora (e se está ocupado).

Dica do item: tarefas longas e subagentes ambos consomem tokens. Se o custo é uma preocupação, definir um
modelo mais barato para subagentes via <<CODE0>>.

Docs: [Subagentes] (<<<LINK0>>>).

Cron ou lembretes não disparam O que devo verificar?

O Cron corre dentro do processo da Gateway. Se o portal não estiver a funcionar continuamente,
os trabalhos agendados não serão executados.

Lista de verificação:

- Confirmar que o cron está activado (<<<CODE0>>) e que <<CODE1>> não está definido.
- Verifique se o Gateway está em funcionamento 24/7 (sem dormir / reiniciar).
- Verifique as configurações do fuso horário da tarefa (<<<CODE2>> vs host).

Depurar:

```bash
openclaw cron run <jobId> --force
openclaw cron runs --id <jobId> --limit 50
```

Docs: [Trabalhos de Cron] (<<<LINK0>>), [Cron vs Heartbeat] (<<LINK1>>>).

## # Como faço para instalar habilidades no Linux

Use ** ClawHub** (CLI) ou solte habilidades em seu espaço de trabalho. O macOS Skills UI não está disponível no Linux.
Procure habilidades em https://clawhub.com.

Instale o ClawHub CLI (escolha um gerenciador de pacotes):

```bash
npm i -g clawhub
```

```bash
pnpm add -g clawhub
```

## # Pode OpenClaw executar tarefas em um cronograma ou continuamente em segundo plano

Sim. Use o programador Gateway:

- **Trabalhos de Cron** para tarefas agendadas ou recorrentes (persistir através de reinícios).
- **Heartbeat** para “sessão principal” verificações periódicas.
- **Trabalhos isolados** para agentes autônomos que postam resumos ou entregam para chats.

Docs: [Trabalhos de Cron] (<<<LINK0>>), [Cron vs Heartbeat] (<<LINK1>>),
[Heartbeat] (<<<LINK2>>>).

**Posso executar apenas as habilidades do MacOS do Linux**

Não directamente. As habilidades do macOS são garantidas por <<CODE0> mais os binários necessários, e as habilidades só aparecem no prompt do sistema quando são elegíveis no host **Gateway**. No Linux, as habilidades <<CODE1>>-somente (como <<CODE2>>, <<CODE3>>, <<CODE4>) não carregarão a menos que você sobreponha o gating.

Você tem três padrões suportados:

**Opção A - execute o Gateway em um Mac (simples).**
Execute o Gateway onde existem os binários do macOS, em seguida, conecte-se a partir do Linux em [modo remoto](<<LINK0>>>) ou sobre Tailscale. A carga de habilidades normalmente porque o anfitrião Gateway é macOS.

** Opção B - use um nó macOS (sem SSH).**
Execute o Gateway no Linux, emparelhe um nó macOS (appmenubar) e defina **Node Run Commands** para "Sempre Pergunte" ou "Sempre Permita" no Mac. OpenClaw pode tratar as habilidades somente do macOS como elegíveis quando os binários necessários existem no nó. O agente executa essas habilidades através da ferramenta <<CODE0>>. Se você escolher "Sempre Perguntar", aprovando "Sempre Permitir" no prompt adiciona esse comando à lista de permissões.

** Opção C - binários macOS proxy sobre SSH (avançado).**
Mantenha o Gateway no Linux, mas faça com que os binários CLI necessários resolvam as embalagens SSH que são executadas em um Mac. Em seguida, sobreponha a habilidade para permitir Linux para que ele permaneça elegível.

1. Crie uma embalagem SSH para o binário (exemplo: <<CODE0>>>):
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   exec ssh -T user@mac-host /opt/homebrew/bin/imsg "$@"
   ```
2. Coloque o invólucro em <<CODE0>> no host Linux (por exemplo <<CODE1>>>).
3. Sobrescrever os metadados de habilidade (espaço de trabalho ou <<CODE2>>) para permitir Linux:
   ```markdown
   ---
   name: imsg
   description: iMessage/SMS CLI for listing chats, history, watch, and sending.
   metadata: { "openclaw": { "os": ["darwin", "linux"], "requires": { "bins": ["imsg"] } } }
   ---
   ```
4. Inicie uma nova sessão para que o instantâneo de habilidades refresque.

Para iMessage especificamente, você também pode apontar <<CODE0>> em uma embalagem SSH (OpenClaw só precisa de stdio). Ver [iMessage] (<<<LINK0>>>).

# # # Você tem um Notion ou integração HeyGen

Hoje não foi construído.

Opções:

- ** Habilidade personalizada / plugin:** melhor para acesso confiável à API (Noção / HeyGen ambos têm APIs).
- Automatização do navegador:** funciona sem código, mas é mais lento e frágil.

Se você quiser manter o contexto por cliente (workflows de agências), um padrão simples é:

- Uma página de Noção por cliente (contexto + preferências + trabalho activo).
- Peça ao agente para ir buscar essa página no início de uma sessão.

Se você quiser uma integração nativa, abra uma solicitação de recursos ou construa uma habilidade
alvejando essas APIs.

Capacidades de instalação:

```bash
clawhub install <skill-slug>
clawhub update --all
```

ClawHub instala em <<CODE0>> sob seu diretório atual (ou cai de volta para seu espaço de trabalho OpenClaw configurado); OpenClaw trata isso como <<CODE1>> na próxima sessão. Para habilidades compartilhadas entre agentes, coloque-as em <<CODE2>>. Algumas habilidades esperam binários instalados via Homebrew; no Linux isso significa Linuxbrew (veja a entrada Perguntas frequentes do Homebrew Linux acima). Ver [Skills] (<<<LINK0>>) e [ClawHub] (<<LINK1>>).

### Como faço para instalar a extensão Chrome para aquisição de navegador

Use o instalador incorporado e carregue a extensão descompactada no Chrome:

```bash
openclaw browser extension install
openclaw browser extension path
```

Em seguida, Chrome → <<CODE0>> → habilitar "Modo de desenvolvimento" → "Carregar desempacotado" → escolha essa pasta.

Guia completo (incluindo o portal remoto + notas de segurança): [Extensão do cronómetro](<<<LINK0>>>)

Se o Gateway é executado na mesma máquina que o Chrome (configuração padrão), você geralmente ** não precisa de nada extra.
Se o Gateway for executado em outro lugar, execute um host de nó na máquina do navegador para que o Gateway possa proxy das ações do navegador.
Você ainda precisa clicar no botão extensão na aba que você deseja controlar (ele não se auto-attach).

# # Sandboxing e memória

# # Há um médico dedicado ao Sandboxing

Sim. Ver [Sandboxing] (<<<LINK0>>>). Para configuração específica do Docker (gateway completo em imagens do Docker ou sandbox), veja [Docker](<<LINK1>>).

** Posso manter os DMs pessoais, mas tornar grupos públicos sandboxed com um agente**

Sim - se seu tráfego privado é **DMs** e seu tráfego público é **groups**.

Use <<CODE0>> para que sessões de grupo/canal (chaves não principais) sejam executadas no Docker, enquanto a sessão principal do DM permanece no host. Em seguida, restringir quais ferramentas estão disponíveis em sessões sandboxed via <<CODE1>>>.

Configuração do percurso + configuração do exemplo: [Grupos: DMs pessoais + grupos públicos](<<<LINK0>>>)

Referência da configuração da chave: [Configuração do portal] (<<<LINK0>>)

## # Como é que encaixo uma pasta de host na caixa de areia

Define <<CODE0>> para <<CODE1>> (por exemplo, <<CODE2>>>). Global + per-agent liga-se merge; as ligações per-agent são ignoradas quando <<CODE3>>. Use <<CODE4>> para qualquer coisa sensível e lembre-se que liga as paredes do sistema de arquivos sandbox. Ver [Sandboxing](<<<LINK0>>) e [Sandbox vs Tool Policy vs Elevated](<<LINK1>>) para exemplos e notas de segurança.

Como funciona a memória?

A memória OpenClaw é apenas arquivos Markdown na área de trabalho do agente:

- Notas diárias em <<CODE0>>
- Notas de longo prazo com curadoria em <<CODE1>> (somente sessões principais/privadas)

Openclaw também executa um **silent pré-compaction memory flush** para lembrar o modelo
escrever notas duráveis antes da auto-compactação. Isto só é executado quando o espaço de trabalho
é gravável (somente as sandboxes o ignoram). Ver [Memory] (<<<LINK0>>>).

A memória continua a esquecer-se das coisas Como é que o faço ficar

Peça ao bot para **escrever o fato para memória**. Notas de longo prazo pertencem a <<CODE0>>>,
contexto de curto prazo vai para <<CODE1>>>.

Esta é ainda uma área que estamos a melhorar. Ajuda a lembrar o modelo para armazenar memórias;
saberá o que fazer. Se continuar a esquecer-se, verifique se o Gateway está a usar o mesmo
espaço de trabalho em cada execução.

Docs: [Memory] (<<<LINK0>>), [Agent workspace] (<<LINK1>>>).

### A busca semântica de memória requer uma chave OpenAI API

Somente se você usar **OpenAI embeddings**. Codex OAuth cobre chat/compleções e
não ** concede acesso às incorporações, então ** assina com o Codex (OAuth ou o
O login do Codex CLI)** não ajuda na busca semântica de memória. Incorporações OpenAI
ainda precisa de uma chave API real (<<<CODE0>> ou <<CODE1>>>>).

Se você não definir um provedor explicitamente, o OpenClaw seleciona automaticamente um provedor quando ele
pode resolver uma chave API (perfisauth, <<CODE0>>, ou env vars).
Prefere OpenAI se uma chave OpenAI resolver, caso contrário Gemini se uma chave Gemini
resolve. Se nenhuma das chaves estiver disponível, a pesquisa de memória permanece desactivada até que você
configurá-lo. Se você tiver um caminho de modelo local configurado e presente, OpenClaw
prefere <<CODE1>>>>.

Se preferir permanecer local, definir <<CODE0>> (e opcionalmente
<<CODE1>>). Se você quiser incorporar Gemini, configure
<<CODE2> e fornecer <<CODE3>> (ou
<<CODE4>>). Nós suportamos **OpenAI, Gemini ou incorporação local**
modelos - ver [Memory](<<<LINK0>>) para os detalhes de configuração.

A memória persiste para sempre Quais são os limites

Os arquivos de memória vivem no disco e persistem até que você os exclua. O limite é o seu
armazenamento, não o modelo. O contexto de ** sessão** ainda é limitado pelo modelo
janela de contexto, tão longas conversas podem compactar ou truncar. É por isso que
a busca de memória existe - ela puxa apenas as partes relevantes de volta ao contexto.

Docs: [Memory] (<<<LINK0>>), [Contexto] (<<LINK1>>>).

# # Onde as coisas vivem no disco

## # Todos os dados são usados com OpenClaw salvos localmente

No - **O estado da OpenClaw é local**, mas **Os serviços externos ainda veem o que você envia**.

- **Local por padrão:** sessões, arquivos de memória, configuração e espaço de trabalho ao vivo no host Gateway
(<<<CODE0>> + sua pasta de espaço de trabalho).
- **Remote by necessary:** mensagens que envia aos fornecedores de modelos (Anthropic/OpenAI/etc.)
suas APIs e plataformas de chat (WhatsApp/Telegram/Slack/etc.) armazenam dados de mensagens em seus
servidores.
- ** Você controla a pegada:** usando modelos locais mantém prompts em sua máquina, mas canal
o tráfego ainda passa pelos servidores do canal.

Relacionado: [Espaço de trabalho do agente] (<<<LINK0>>), [Memory] (<<LINK1>>>).

Onde é que o Openclaw guarda os seus dados?

Tudo vive em <<CODE0>> (padrão: <<CODE1>>):

□ Caminho
-----------------------------------------
Configuração principal (JSON5)
Importação de OAuth legada (copiada em perfis de autenticação na primeira utilização)
Perfis de autenticação (chaves OAuth + API)
(Gestão automática)
(p. ex. <<CODE5>>)
* < <<CODE6>>
História e estado da conversação (por agente)
(por agente)

Caminho do agente único legado: <<CODE0>> (migrado por <<CODE1>>>).

Seu espaço de trabalho** (AGENTS.md, arquivos de memória, habilidades, etc.) é separado e configurado via <<CODE0>> (padrão: <<CODE1>>).

Onde deve viver AGENTSmd Soulmd Usarmd

Esses arquivos vivem no **agent workspace**, não <<CODE0>>.

- ** Espaço de trabalho (por agente)**: <<CODE0>>, <<CODE1>>, <<CODE2>>, <<CODE3>>,
<<CODE4>> (ou <<CODE5>>), <<CODE6>>, opcional <<CODE7>>.
- **Dir Estado (<<CODE8>>>)**: config, credenciais, perfis de autenticação, sessões, logs,
e habilidades compartilhadas (<<<CODE9>>).

O espaço de trabalho padrão é <<CODE0>>, configurável via:

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}
```

Se o bot “esquece” após um reinício, confirme que o Gateway está usando o mesmo
espaço de trabalho em cada lançamento (e lembre-se: modo remoto usa o ** gateway host's**
espaço de trabalho, não seu laptop local).

Dica: se você quiser um comportamento durável ou preferência, peça ao bot para ** escrevê-lo em
AGENTS.md ou MEMORY.md** em vez de confiar no histórico do chat.

Ver [Espaço de trabalho do agente] (<<<LINK0>>) e [Memória] (<<LINK1>>).

Qual é a estratégia de backup recomendada?

Coloque seu **agent workspace** em um **private** git repo e faça backup em algum lugar
privado (por exemplo GitHub privado). Isto captura memória + AGENTES/SOUL/USER
arquivos, e permite que você restaure a “mente” do assistente mais tarde.

Não cometer nada em <<CODE0>> (credenciais, sessões, fichas).
Se você precisar de uma restauração completa, faça backup tanto da área de trabalho quanto do diretório de estado
separadamente (ver a questão da migração acima).

Docs: [Espaço de trabalho do agente](<<<LINK0>>>).

Como faço para desinstalar completamente Openclaw

Veja o guia dedicado: [Desinstalar](<<<LINK0>>>).

Os agentes podem trabalhar fora do espaço de trabalho

Sim. O espaço de trabalho é o **default cwd** e âncora de memória, não uma caixa de areia dura.
Caminhos relativos resolvem-se dentro do espaço de trabalho, mas caminhos absolutos podem acessar outros
locais da máquina a menos que o sandboxing esteja activo. Se necessitar de isolamento, utilize
[<<<CODE0>>](<<LINK0>>>>) ou configurações de sandbox por agente. Se você
quer um repo para ser o diretório de trabalho padrão, ponto que agente
<<CODE1>> para a raiz do repo. O repo OpenClaw é apenas código fonte; mantenha o
espaço de trabalho separado a menos que você intencionalmente quer que o agente trabalhe dentro dele.

Exemplo (repo como padrão cwd):

```json5
{
  agents: {
    defaults: {
      workspace: "~/Projects/my-repo",
    },
  },
}
```

## # Estou em modo remoto onde está a loja de sessões

O estado da sessão pertence ao host ** gateway**. Se você estiver em modo remoto, a loja de sessão que você se importa está na máquina remota, não no laptop local. Ver [Gestão de sessão] (<<<LINK0>>>).

Noções básicas de configuração

## # Que formato é a configuração Onde está?

OpenClaw lê uma configuração opcional **JSON5** de <<CODE0>>> (padrão: <<CODE1>>):

```
$OPENCLAW_CONFIG_PATH
```

Se o arquivo estiver faltando, ele usa padrões seguros (incluindo uma área de trabalho padrão de <<CODE0>>).

Eu ajusto gatewaybind lan ou tailnet e agora nada escuta a UI diz não autorizado

Não se liga ao loopback **requer autorização**. Configure <<CODE0>>> + <<CODE1>>> (ou use <<CODE2>>).

```json5
{
  gateway: {
    bind: "lan",
    auth: {
      mode: "token",
      token: "replace-me",
    },
  },
}
```

Notas:

- <<CODE0>> é para ** chamadas CLI remotas** somente; não permite a autenticação local do gateway.
- A interface de controle autentica-se via <<CODE1>> (armazenada em configurações de app/UI). Evite colocar tokens em URLs.

# # # Porque preciso de um token no localhost agora

O assistente gera um token de gateway por padrão (mesmo em loopback) então ** os clientes locais WS devem autenticar**. Isto bloqueia outros processos locais de chamar o Gateway. Colar o token na configuração Control UI (ou na configuração do seu cliente) para se conectar.

Se você **realmente** quer loopback aberto, remova <<CODE0>> de sua configuração. O médico pode gerar um token para você a qualquer momento: <<CODE1>>>.

## # Tenho de reiniciar depois de mudar de configuração

O Gateway observa a configuração e suporta recarga quente:

- <<CODE0> (default): alterações seguras de aplicação quente, reiniciar para as críticas
- <<CODE1>>, <<CODE2>>, <<CODE3>>> são também suportados

## # Como posso ativar a busca na web e busca na web

<<CODE0> funciona sem uma chave API. <<CODE1>> requer uma API de pesquisa corajosa
Chave. **Recomendado:** correr <<CODE2>> para o conservar
<<CODE3>>>. Meio ambiente alternativo: definido <<CODE4>>> para o
Processo do portal.

```json5
{
  tools: {
    web: {
      search: {
        enabled: true,
        apiKey: "BRAVE_API_KEY_HERE",
        maxResults: 5,
      },
      fetch: {
        enabled: true,
      },
    },
  },
}
```

Notas:

- Se utilizar listas de autorizações, adicione <<CODE0>/<<CODE1>>> ou <<CODE2>>>.
- <<CODE3> é ativado por padrão (a menos que explicitamente desabilitado).
- Daemons ler env vars de <<CODE4>> (ou o ambiente de serviço).

Documentos: [Ferramentas Web](<<<LINK0>>>).

## # Como faço para executar um portal central com trabalhadores especializados através de dispositivos

O padrão comum é ** um Gateway** (por exemplo, Raspberry Pi) mais ** nós** e ** agentes**:

- **Gateway (central):** possui canais (Signal/WhatsApp), roteamento e sessões.
- ** Nós (dispositivos):** Macs/iOS/Android se conectam como periféricos e expõem ferramentas locais (<<<CODE0>>, <<CODE1>>, <<CODE2>>>).
- ** Agentes (trabalhadores):** cérebros/espaços de trabalho separados para papéis especiais (por exemplo, “Hetzner ops”, “Dados pessoais”).
- ** Sub-agentes:** desova trabalho de fundo de um agente principal quando você quer paralelismo.
- ** Tui:** conecte-se ao Gateway e mude de agentes/sessões.

Docs: [Nodes](<<<LINK0>>), [Acesso remoto](<<<LINK1>>>), [Multi-Agent Routing](<<LINK2>>), [Sub-agentes](<<LINK3>>>), [TUI](<<LINK4>>>).

## # O navegador OpenClaw pode correr sem cabeça

Sim. É uma opção de configuração:

```json5
{
  browser: { headless: true },
  agents: {
    defaults: {
      sandbox: { browser: { headless: true } },
    },
  },
}
```

O padrão é <<CODE0>> (cabeçalho). A falta de cabeça é mais susceptível de desencadear controlos anti-bots em alguns locais. Ver [Browser] (<<<LINK0>>>).

Headless usa o mesmo motor Chromium** e funciona para a maioria da automação (formas, cliques, raspagem, logins). As principais diferenças:

- Nenhuma janela do navegador visível (use screenshots se precisar de visual).
- Alguns sites são mais rigorosos sobre automação em modo sem cabeça (CAPTCHAs, anti-bot).
Por exemplo, X/Twitter muitas vezes bloqueia sessões sem cabeça.

## # Como eu uso Bravo para o controle do navegador

Defina <<CODE0>> para o seu binário corajoso (ou qualquer navegador baseado em Chromium) e reinicie o Gateway.
Veja os exemplos completos de configuração em [Browser](<<<LINK0>>>).

# # Gateways remotos + nós

### Como os comandos propagam entre Telegram o gateway e nós

As mensagens de telegrama são tratadas pela **porta**. O gateway executa o agente e
só então chama nós sobre o **Gateway WebSocket** quando uma ferramenta de nó é necessária:

Telegram → Gateway → Agente → <<CODE0> → Node → Gateway → Telegram

Os nós não vêem o tráfego de provedores de entrada; eles só recebem chamadas RCC de nó.

Como é que o meu agente pode aceder ao meu computador se o Gateway está hospedado remotamente

Resposta curta: ** par seu computador como um nó**. O portal corre para outro lado, mas pode
chamar <<CODE0>> ferramentas (tela, câmera, sistema) em sua máquina local sobre o Gateway WebSocket.

Configuração típica:

1. Execute o Gateway no host sempre-on (VPS/home server).
2. Coloque o host Gateway + seu computador na mesma tailnet.
3. Certifique-se de que o WS Gateway é acessível (tailnet ligação ou túnel SSH).
4. Abra o app macOS localmente e conecte-se em ** Remote sobre o modo SSH** (ou tailnet direta)
então ele pode registrar como um nó.
5. Aprovar o nó no portal:
   ```bash
   openclaw nodes pending
   openclaw nodes approve <requestId>
   ```

Nenhuma ponte TCP separada é necessária; nós conectam sobre o Gateway WebSocket.

Lembrete de segurança: parear um nó macOS permite <<CODE0>> nessa máquina. Apenas
partilhe dispositivos em que confia e reveja [Segurança](<<<LINK0>>>).

Docs: [Nodes](<<<LINK0>>), [Protocolo Gateway](<<LINK1>>>), [modo remoto macOS](<<LINK2>>>), [Segurança](<<LINK3>>>>).

## # Tailscale está conectado mas eu não recebo respostas E agora?

Verifique o básico:

- Gateway está rodando: <<CODE0>>>
- Saúde no portal: <<CODE1>>
- Saúde dos canais: <<CODE2>>

Em seguida, verifique a autenticação e roteamento:

- Se utilizar Tailscale Serve, certifique-se de que <<CODE0> está correctamente definido.
- Se você se conectar através do túnel SSH, confirme que o túnel local está acima e aponta para a porta direita.
- Confirme que suas allowlists (DM ou grupo) incluem sua conta.

Docs: [Tailscale] (<<<LINK0>>), [Acesso remoto] (<<LINK1>>>), [Canais] (<<<LINK2>>>).

## # Podem duas instâncias OpenClaw falar um com o outro VPS local

Sim. Não há nenhuma ponte "de baixo para baixo" integrada, mas você pode ligá-lo em alguns
Maneiras fiáveis:

**Simples:** use um canal de chat normal que ambos os bots podem acessar (Telegram/Slack/WhatsApp).
Faça com que Bot A envie uma mensagem para Bot B, então deixe que Bot B responda como de costume.

**CLI bridge (generic):** execute um script que chama o outro Gateway com
<<CODE0>>, visando um bate-papo onde o outro bot
Ouve. Se um bot estiver em um VPS remoto, aponte seu CLI para aquele Gateway remoto
via SSH/Tailscale (ver [Acesso remoto] (<<<LINK0>>>)).

Padrão de exemplo (correr de uma máquina que pode alcançar o portal de destino):

```bash
openclaw agent --message "Hello from local bot" --deliver --channel telegram --reply-to <chat-id>
```

Dica: adicione um guardrail para que os dois bots não façam loop infinitamente (somente menton, canal
allowlists, ou uma regra de "não responder às mensagens bot").

Docs: [Acesso remoto](<<<LINK0>>), [Agente CLI](<<LINK1>>>), [Agente enviar](<<LINK2>>>>).

Preciso de VPS separados para vários agentes

Não. Um Gateway pode hospedar vários agentes, cada um com seu próprio espaço de trabalho, padrões de modelo,
e roteamento. Essa é a configuração normal e é muito mais barato e mais simples do que correr
um VPS por agente.

Use VPSes separados apenas quando você precisar de isolamento rígido (limites de segurança) ou muito
diferentes configurações que você não deseja compartilhar. Caso contrário, mantenha um portal e
utilizar múltiplos agentes ou subagentes.

## # Há um benefício para usar um nó em meu laptop pessoal em vez de SSH de um VPS

Sim - nós são a maneira de primeira classe de chegar ao seu laptop de um Gateway remoto, e eles
desbloquear mais do que acesso de shell. O Gateway é executado no macOS/Linux (Windows via WSL2) e é
leve (um pequeno VPS ou Raspberry Pi-class caixa é bom; 4 GB RAM é abundância), então um comum
a configuração é um host sempre-on mais seu laptop como um nó.

- ** Não é necessário introduzir SSH. Nós conectamos ao Gateway WebSocket e usamos o emparelhamento de dispositivos.
- **Controles de execução seguros.** <<CODE0> é fechado por listas de allowlists/aprovações de nó nesse laptop.
- **Mais ferramentas de dispositivos.** Os nós expõem <<CODE1>>, <<CODE2>> e <<CODE3>> além de <<CODE4>>.
- Automatização local do navegador. Mantenha o Gateway em um VPS, mas execute o Chrome localmente e retransmita o controle
com a extensão Chrome + um host de nó no laptop.

SSH é bom para acesso ad-hoc shell, mas nós são mais simples para fluxos de trabalho de agentes em curso e
Automação de dispositivos.

Docs: [Nodes] (<<<LINK0>>>), [Nodes CLI] (<<LINK1>>>>>), [Extensão de cromo] (<<<LINK2>>>>>).

## # Devo instalar em um segundo laptop ou apenas adicionar um nó

Se você só precisa ** ferramentas locais** (tela/câmera/exec) no segundo laptop, adicioná-lo como um
**Node**. Isso mantém um único Gateway e evita a configuração duplicada. Ferramentas de nó locais são
atualmente macOS-somente, mas planejamos estendê-los para outros SOs.

Instale um segundo Gateway apenas quando você precisar de ** isolamento rígido** ou dois bots totalmente separados.

Docs: [Nodes](<<<LINK0>>>), [Nodes CLI](<<LINK1>>>>), [Multiple gateways](<<LINK2>>>>).

## # Os nós executam um serviço de gateway

Não. Apenas ** um gateway** deve ser executado por host a menos que você execute perfis isolados intencionalmente (ver [gateways múltiplos](<<<LINK0>>)). Os nós são periféricos que se ligam
para o gateway (nós iOS/Android, ou "modo de nó" do macOS no aplicativo da barra de menu). Para o nó sem cabeça
hosts e controle CLI, veja [Node host CLI] (<<<LINK1>>).

É necessário reiniciar completamente para as alterações <<CODE0>>, <HTML1>>>> e <<CODE2>.

## # Existe uma maneira API RPC de aplicar a configuração

Sim. <<CODE0>> valida + escreve a configuração completa e reinicia o Gateway como parte da operação.

### configapply limpou minha configuração Como faço para recuperar e evitar isso

<<CODE0> substitui a configuração **inteira**. Se você enviar um objeto parcial, tudo
O outro é removido.

Recuperar:

- Restaurar a partir de backup (git ou um copiado <<CODE0>>>).
- Se você não tiver backup, volte a executar <<CODE1>> e reconfigure canais/modelos.
- Se isso foi inesperado, arquive um bug e inclua sua última configuração conhecida ou qualquer backup.
- Um agente de codificação local pode frequentemente reconstruir uma configuração de trabalho a partir de logs ou histórico.

Evitar:

- Utilizar <<CODE0> para pequenas alterações.
- Use <<CODE1>> para edições interativas.

Docs: [Config] (<<<LINK0>>), [Configure] (<<LINK1>>>>), [Doctor] (<<LINK2>>>>).

## # O que é uma configuração mínima sã para uma primeira instalação

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

Isso define seu espaço de trabalho e restringe quem pode ativar o bot.

# # # Como faço para configurar Tailscale em um VPS e conectar do meu Mac

Passos mínimos:

1. **Instalar + login no VPS**
   ```bash
   curl -fsSL https://tailscale.com/install.sh | sh
   sudo tailscale up
   ```
2. **Instalar + login no seu Mac**
- Use a aplicação Tailscale e entre na mesma tailnet.
3. ** Enable MagicDNS (recomendado) **
- No console de administração Tailscale, habilite o MagicDNS para que o VPS tenha um nome estável.
4. **Use o nome da máquina da tailnet**
- SSH: <<CODE0>>
- Gateway WS: <<CODE1>>

Se você quiser a interface de controle sem SSH, use Tailscale Serve no VPS:

```bash
openclaw gateway --tailscale serve
```

Isso mantém o gateway ligado ao loopback e expõe HTTPS via Tailscale. Ver [Tailscale] (<<<LINK0>>>).

### Como eu conecto um nó Mac a um serviço remoto Gateway Tailscale

Servir expõe a ** Controle de Gateway UI + WS**. Os nós ligam-se ao mesmo ponto final do Gateway WS.

Configuração recomendada:

1. ** Certifique-se de que o VPS + Mac estão na mesma tailnet**.
2. **Use o aplicativo macOS no modo Remoto** (alvo SH pode ser o hostname tailnet).
O aplicativo irá tunelar a porta Gateway e se conectar como um nó.
3. **Aprove o nó** no gateway:
   ```bash
   openclaw nodes pending
   openclaw nodes approve <requestId>
   ```

Docs: [Protocolo de Gateway](<<<LINK0>>), [Discovery](<<LINK1>>>), [modo remoto macOS](<<LINK2>>>>).

# # Env vars e .env carregando

### Como é que o OpenClaw carrega variáveis de ambiente

OpenClaw lê env vars do processo pai (shell, launchd/systemd, CI, etc.) e também carrega:

- <<CODE0> da pasta de trabalho actual
- um recuo global <<CODE1>> de <<CODE2>> (também conhecido por <<CODE3>>)

Nenhum arquivo <<CODE0> > substitui env vars existentes.

Você também pode definir env vars em linha na configuração (aplicado apenas se faltar no env do processo):

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: { GROQ_API_KEY: "gsk-..." },
  },
}
```

Ver [/ambiente](<<<LINK0>>>) para precedência total e fontes.

Comecei o portal através do serviço e os meus Env Vars desapareceram E agora?

Duas correções comuns:

1. Coloque as chaves em falta em <<CODE0> para que eles sejam captados mesmo quando o serviço não herdar seu shell env.
2. Habilitar importação shell (opt-in conveniência):

```json5
{
  env: {
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}
```

Isso executa sua shell de login e importa apenas chaves esperadas em falta (nunca substitui). Env var equivalentes:
<<CODE0>>, <<CODE1>>

# # # Eu set COPILOTGITHUBTOKEN mas o status dos modelos mostra shell env fora Porquê

<<CODE0> relata se **shell env import** está habilitada. “Env shell: desligado”
does **not** significa que seus vars env estão faltando - significa apenas OpenClaw não irá carregar
sua shell de login automaticamente.

Se o Gateway for executado como um serviço (lançado/systemd), ele não herdará sua shell
ambiente. Corrigir fazendo um destes:

1. Coloque o símbolo em <<CODE0>>:
   ```
   COPILOT_GITHUB_TOKEN=...
   ```
2. Ou habilitar a importação da shell (<<<CODE0>>).
3. Ou adicioná-lo à sua configuração <<CODE1> bloco (aplica-se apenas se faltar).

Reinicie o gateway e verifique novamente:

```bash
openclaw models status
```

As fichas co-piloto são lidas a partir de <<CODE0>> (também <<CODE1>>/ <<CODE2>>).
Ver [/conceitos/fornecedores de modelos] (<<<LINK0>>) e [/ambiente] (<<LINK1>>>).

# # Sessões e várias conversas

Como é que começo uma conversa nova?

Enviar <<CODE0>> ou <<CODE1>> como uma mensagem autônoma. Ver [Gestão de sessão] (<<<LINK0>>>).

## # Fazer sessões reset automaticamente se eu nunca enviar novo

Sim. Sessões expiram após <<CODE0>> (padrão **60**). O **próximo**
a mensagem inicia um novo ID de sessão para aquela tecla de chat. Isto não apaga
transcrições - ele só começa uma nova sessão.

```json5
{
  session: {
    idleMinutes: 240,
  },
}
```

## # Há uma maneira de fazer uma equipe de instâncias OpenClaw um CEO e muitos agentes

Sim, via **roteamento multiagentes** e **subagentes**. Você pode criar um coordenador
agente e vários agentes trabalhadores com seus próprios espaços de trabalho e modelos.

Dito isto, esta é melhor vista como uma ** experiência divertida**. É um símbolo pesado e muitas vezes
menos eficiente do que usar um bot com sessões separadas. O modelo típico nós
vision é um bot que você fala, com sessões diferentes para trabalho paralelo. Isso.
bot também pode gerar sub-agentes quando necessário.

Docs: [Roteamento multiagente](<<<LINK0>>>), [Subagentes](<<LINK1>>>), [Agentes CLI](<<LINK2>>>>).

# # # Porque é que o contexto ficou truncado no meio da tarefa Como posso evitá-lo?

O contexto da sessão é limitado pela janela do modelo. chats longos, grandes saídas de ferramentas, ou muitos
arquivos podem desencadear compactação ou truncamento.

O que ajuda:

- Peça ao bot para resumir o estado atual e escrevê-lo em um arquivo.
- Use <<CODE0>> antes de tarefas longas, e <<CODE1>> ao mudar de tópicos.
- Mantenha contexto importante no espaço de trabalho e peça ao bot para lê-lo de volta.
- Use sub-agentes para trabalhos longos ou paralelos para que o chat principal permaneça menor.
- Escolha um modelo com uma janela de contexto maior se isso acontece frequentemente.

## # Como faço para reiniciar completamente OpenClaw mas mantê-lo instalado

Usar o comando de reset:

```bash
openclaw reset
```

Reset completo não- interactivo:

```bash
openclaw reset --scope full --yes --non-interactive
```

Em seguida, repetir a bordo:

```bash
openclaw onboard --install-daemon
```

Notas:

- O assistente de onboard também oferece **Reset** se vir uma configuração existente. Ver [Wizard] (<<<LINK0>>>).
- Se você usou perfis (<<<CODE0>/ <<CODE1>>>>>>), repor cada dir estado (os padrões são <<CODE2>>>).
- Dev reset: <<CODE3>>> (somente em dev; limpa a configuração do dev + credenciais + sessões + espaço de trabalho).

## # Estou a obter erros de contexto demasiado grandes como faço para reiniciar ou compactar

Utilizar um destes:

- **Compacto** (mantém a conversa, mas resume turnos mais antigos):

  ```
  /compact
  ```

ou <<CODE0>> para orientar o resumo.

- **Reset** (ID de sessão nova para a mesma tecla de chat):
  ```
  /new
  /reset
  ```

Se continuar a acontecer:

- Activar ou sintonizar ** poda de sessão** (<<<CODE0>>) para aparar a saída antiga da ferramenta.
- Use um modelo com uma janela de contexto maior.

Docs: [Compactação](<<<LINK0>>), [Poda de Sessão](<<LINK1>>>>), [Gestão de Sessão](<<LINK2>>>>).

# # # # Por que estou vendo LLM request rejeited messagesNcontentXtooluseuseinput Field required

Este é um erro de validação do provedor: o modelo emitiu um bloco <<CODE0>> sem o necessário
<<CODE1>>>. Isso geralmente significa que o histórico de sessão está obsoleto ou corrompido (muitas vezes após longos threads
ou uma mudança de ferramenta/esquema).

Corrigir: iniciar uma nova sessão com <<CODE0>> (mensagem standalone).

Porque estou a receber mensagens a cada 30 minutos

Heartbeats corre a cada **30m** por padrão. Ajustar ou desativá-los:

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "2h", // or "0m" to disable
      },
    },
  },
}
```

Se <<CODE0>> existir, mas estiver efetivamente vazio (apenas linhas em branco e marcação para baixo)
cabeçalhos como <<CODE1>>), OpenClaw ignora a execução do batimento cardíaco para salvar chamadas API.
Se o arquivo estiver faltando, o batimento cardíaco ainda é executado e o modelo decide o que fazer.

O agente substitui o uso <<CODE0>>>>. Docs: [Heartbeat] (<<<LINK0>>>).

## # Eu preciso adicionar uma conta bot a um grupo WhatsApp

Não. O OpenClaw é executado em ** sua própria conta**, então se você estiver no grupo, o OpenClaw pode vê-lo.
Por padrão, as respostas do grupo são bloqueadas até que você permita os remetentes (<<CODE0>>>).

Se você quiser que apenas **você** seja capaz de ativar as respostas do grupo:

```json5
{
  channels: {
    whatsapp: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
    },
  },
}
```

Como é que consigo o JID de um grupo WhatsApp

Opção 1 (mais rápida): registros de cauda e enviar uma mensagem de teste no grupo:

```bash
openclaw logs --follow --json
```

Procurar <<CODE0>> (ou <<CODE1>>>) que termine em <<CODE2>>, como:
<<CODE3>>>.

Opção 2 (se já configurado/allowlist): grupos de lista da configuração:

```bash
openclaw directory groups list --channel whatsapp
```

Docs: [WhatsApp](<<<LINK0>>), [Diretório](<<LINK1>>>), [Logs](<<LINK2>>>>).

# # # Porque é que o OpenClaw não responde num grupo

Duas causas comuns:

- Mencione a ligação. Você deve @mention o bot (ou corresponder <<CODE0>>>).
- Configurou <<CODE1>> sem <<CODE2>> e o grupo não está autorizado.

Ver [Grupos](<<<LINK0>>) e [Mensagens do grupo](<<LINK1>>>).

## # Fazer groupsthreads compartilhar contexto com DMs

Conversas diretas colapsam na sessão principal por padrão. Grupos/canais têm suas próprias chaves de sessão, e tópicos de Telegram / tópicos Discord são sessões separadas. Ver [Grupos](<<<LINK0>>) e [Mensagens do grupo](<<LINK1>>>).

## # Quantos espaços de trabalho e agentes posso criar

Sem limites. Dezenas (até centenas) estão bem, mas cuidado para:

- Crescimento do disco:** sessões + transcrições vivem em <<CODE0>>.
- ** Custo do token: ** mais agentes significa mais uso de modelo concorrente.
- **Ops overhead:** per-agent auth profiles, workspaces, and canal roteing.

Dicas:

- Manter um **activo** espaço de trabalho por agente (<<<CODE0>>>).
- Sessões antigas (delete JSONL ou armazenar entradas) se o disco crescer.
- Utilizar <<CODE1>> para detectar desfasamentos de perfis e espaços de trabalho perdidos.

## # Posso executar vários bots ou chats ao mesmo tempo Slack e como devo configurar isso

Sim. Use **Roteamento Multi-Agente** para executar múltiplos agentes isolados e encaminhar mensagens de entrada por
canal/conta/par. Slack é suportado como um canal e pode ser ligado a agentes específicos.

O acesso do navegador é poderoso, mas não "fazer nada que uma lata humana" - anti-bot, CAPTCHAs, e MFA pode
Ainda bloquear a automação. Para o controle do navegador mais confiável, use o relé de extensão Chrome
na máquina que executa o navegador (e mantenha o Gateway em qualquer lugar).

Configuração das melhores práticas:

- Host sempre no Gateway (VPS/Mac mini).
- Um agente por papel (ligações).
- Canal(es) de fenda ligado a esses agentes.
- Navegador local via relé de extensão (ou um nó) quando necessário.

Docs: [Multi-Agent Routing] (<<<LINK0>>), [Slack] (<<LINK1>>),
[Browser] (<<<LINK2>>), [Extensão de cromo] (<<LINK3>>>), [Nodes] (<<LINK4>>>).

# # # Modelos: padrões, seleção, apelidos, comutação

## # Qual é o modelo padrão

O modelo padrão do OpenClaw é o que você definir como:

```
agents.defaults.model.primary
```

Os modelos são referenciados como <<CODE0>> (exemplo: <<CODE1>>>). Se você omitir o provedor, o OpenClaw atualmente assume <<CODE2>> como um recuo temporário de deprecação - mas você ainda deve **explicativamente** definido <<CODE3>>>.

# # Que modelo recomendas

** Default recomendado:** <<CODE0>>>.
** Boa alternativa:** <<CODE1>>>.
** Fiável (menos caracteres):** <<CODE2>>> - quase tão bom quanto Opus, apenas menos personalidade.
**Orçamento:** <<CODE3>>>.

MiniMax M2.1 tem seus próprios documentos: [MiniMax] (<<<LINK0>>>) e
[Modelos locais](<<<LINK1>>>).

Regra do polegar: use o **o melhor modelo que você pode pagar** para o trabalho de apostas altas, e um mais barato
modelo para chat de rotina ou resumos. Você pode encaminhar modelos por agente e usar subagentes para
paralelizar tarefas longas (cada subagente consome tokens). Ver [Modelos] (<<<LINK0>>) e
[Subagentes] (<<<LINK1>>>).

Advertência forte: modelos mais fracos/over-quantizados são mais vulneráveis a
injecção e comportamento inseguro. Ver [Segurança] (<<<LINK0>>>).

Mais contexto: [Modelos](<<<LINK0>>>).

# # # Eu posso usar modelos selfhosted llamacpp vLLM Ollama

Sim. Se seu servidor local expor uma API compatível com OpenAI, você pode apontar um
fornecedor personalizado nele. Ollama é suportado diretamente e é o caminho mais fácil.

Nota de segurança: modelos menores ou fortemente quantizados são mais vulneráveis a alertar
injecção. Recomendamos fortemente **grandes modelos** para qualquer bot que possa usar ferramentas.
Se você ainda quiser modelos pequenos, habilite sandboxing e allowlists de ferramentas rigorosas.

Docs: [Ollama] (<<<LINK0>>), [Modelos locais] (<<LINK1>>),
[Fornecedores de modelos](<<<LINK2>>), [Segurança](<<LINK3>>>),
[Sandboxing] (<<<LINK4>>>).

## # Como faço para mudar de modelo sem limpar minha configuração

Use comandos **model** ou edite apenas os campos **model**. Evite substituições completas de configuração.

Opções seguras:

- <<CODE0> em chat (rápido, por sessão)
- <<CODE1>> (atualiza apenas a configuração do modelo)
- <<CODE2>> (interactiva)
- editar <<CODE3>> em <<CODE4>

Evite <<CODE0>> com um objeto parcial, a menos que pretenda substituir toda a configuração.
Se você substituiu a configuração, restaure a partir de backup ou re-run <<CODE1> para reparar.

Docs: [Modelos](<<<LINK0>>), [Configurar](<<LINK1>>>), [Config](<<LINK2>>>), [Doctor](<<LINK3>>>>>).

## # O que é que Openclaw, Clawd e Krill usam para modelos

- ** OpenClaw + Flawd:** Anthropic Opus (<<CODE0>>>) - ver [Anthropic] (<<LINK0>>).
- **Krill:** MiniMax M2.1 (<<<CODE1>>) - ver [MiniMax] (<<LINK1>>).

## # Como faço para mudar de modelo sem reiniciar

Use o comando <<CODE0>> como uma mensagem autônoma:

```
/model sonnet
/model haiku
/model opus
/model gpt
/model gpt-mini
/model gemini
/model gemini-flash
```

Você pode listar os modelos disponíveis com <<CODE0>>, <<CODE1>>>>, ou <<CODE2>>>.

<<CODE0>> (e <<CODE1>>>) mostra um selecionador compacto e numerado. Selecionar por número:

```
/model 3
```

Você também pode forçar um perfil de autenticação específico para o provedor (por sessão):

```
/model opus@anthropic:default
/model opus@anthropic:work
```

Dica: <<CODE0>> mostra qual agente está ativo, que <<CODE1> arquivo está sendo usado, e qual perfil de autenticação será testado em seguida.
Ele também mostra o endpoint do provedor configurado (<<<CODE2>>>) e o modo API (<<CODE3>>>>>) quando disponível.

** Como desvincular um perfil que defini com perfil**

Repetição <<CODE0>> ** sem** o sufixo <<CODE1>>:

```
/model anthropic/claude-opus-4-5
```

Se você quiser retornar ao padrão, escolha-o de <<CODE0>> (ou envie <<CODE1>>).
Utilizar <<CODE2>> para confirmar qual o perfil de autenticação activo.

## # Posso usar GPT 5.2 para tarefas diárias e Codex 5.2 para codificação

Sim. Definir um como padrão e alternar conforme necessário:

- ** Interruptor rápido (por sessão):** <<CODE0>> para tarefas diárias, <<CODE1>>> para codificação.
- **Padrão + interruptor:** definido <<CODE2>> para <<CODE3>>, em seguida, mude para <<CODE4>> ao codificar (ou ao contrário).
- **Subagentes:** tarefas de codificação de rota para subagentes com um modelo padrão diferente.

Ver [Modelos] (<<<LINK0>>) e [Comandos Slash] (<<LINK1>>).

# # # Por que eu vejo Modelo não é permitido e, em seguida, nenhuma resposta

Se <<CODE0>> for definido, torna-se a ** lista de licenças** para <<CODE1>> e qualquer
sessão anulada. Escolhendo um modelo que não está nessa lista retorna:

```
Model "provider/model" is not allowed. Use /model to list available models.
```

Esse erro é devolvido ** em vez de** uma resposta normal. Corrigir: adicionar o modelo
<<CODE0>>, remover a lista de permissões, ou escolher um modelo de <<CODE1>>.

# # # Por que eu vejo o modelo desconhecido minimaxMiniMaxM21

Isso significa que o provedor ** não está configurado** (sem configuração ou autenticação do provedor MiniMax
perfil foi encontrado), de modo que o modelo não pode ser resolvido. Uma correção para esta detecção é
em **2026.1.12** (não lançado no momento da escrita).

Corrigir a lista de verificação:

1. Atualize para **2026.1.12** (ou execute a partir da fonte <<CODE0>>), então reinicie o gateway.
2. Certifique-se de que MiniMax está configurado (wizard ou JSON), ou que uma chave de API MiniMax
existe em perfis env/auth para que o provedor possa ser injetado.
3. Use o modelo exato id (caso-sensível): <<CODE1>> ou
<<CODE2>>>.
4. Executar:
   ```bash
   openclaw models list
   ```
e escolher na lista (ou <<CODE0>> no chat).

Ver [MiniMax] (<<<LINK0>>) e [Modelos] (<<LINK1>>>).

# # # Posso usar MiniMax como meu padrão e OpenAI para tarefas complexas

Sim. Use **MiniMax como padrão** e mude de modelo **por sessão** quando necessário.
Fallbacks são para **errors**, não "tarefas difíceis", então use <<CODE0>> ou um agente separado.

** Opção A: interruptor por sessão**

```json5
{
  env: { MINIMAX_API_KEY: "sk-...", OPENAI_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "minimax/MiniMax-M2.1" },
      models: {
        "minimax/MiniMax-M2.1": { alias: "minimax" },
        "openai/gpt-5.2": { alias: "gpt" },
      },
    },
  },
}
```

Depois:

```
/model gpt
```

**Opção B: agentes separados**

- Agente A padrão: MiniMax
- Agente B padrão: OpenAI
- Rota por agente ou utilização <<CODE0>> para comutar

Documentos: [Modelos](<<<LINK0>>), [Roteamento Multi-Agente](<<LINK1>>), [MiniMax](<<LINK2>>), [OpenAI](<<LINK3>>>).

## # São opus soneto gpt atalhos embutidos

Sim. O OpenClaw envia algumas abreviações padrão (apenas aplicadas quando o modelo existe em <<CODE0>>>):

- <<CODE0>> → <<CODE1>>>
- <<CODE2>> → <<CODE3>>
- <<CODE4>> → <<CODE5>>
- <<CODE6>> → <<CODE7>>>
- <<CODE8>> → <<CODE9>>>
- <<CODE10>> → <<CODE11>>

Se você definir seu próprio nome com o mesmo nome, seu valor ganha.

### Como defino os atalhos de modelos

Os nomes são de <<CODE0>>>>. Exemplo:

```json5
{
  agents: {
    defaults: {
      model: { primary: "anthropic/claude-opus-4-5" },
      models: {
        "anthropic/claude-opus-4-5": { alias: "opus" },
        "anthropic/claude-sonnet-4-5": { alias: "sonnet" },
        "anthropic/claude-haiku-4-5": { alias: "haiku" },
      },
    },
  },
}
```

Em seguida, <<CODE0>> (ou <<CODE1> quando suportado) resolve para esse ID modelo.

### Como faço para adicionar modelos de outros provedores como OpenRouter ou ZAI

OpenRouter (pay-per-token; muitos modelos):

```json5
{
  agents: {
    defaults: {
      model: { primary: "openrouter/anthropic/claude-sonnet-4-5" },
      models: { "openrouter/anthropic/claude-sonnet-4-5": {} },
    },
  },
  env: { OPENROUTER_API_KEY: "sk-or-..." },
}
```

Z.AI (modelos GLM):

```json5
{
  agents: {
    defaults: {
      model: { primary: "zai/glm-4.7" },
      models: { "zai/glm-4.7": {} },
    },
  },
  env: { ZAI_API_KEY: "..." },
}
```

Se você referenciar um provedor/modelo mas a chave de provedor requerida está faltando, você receberá um erro de autenticação em tempo de execução (por exemplo, <<CODE0>>).

** Nenhuma chave de API encontrada para provedor após adicionar um novo agente**

Isto geralmente significa que o **novo agente** tem uma loja de autenticação vazia. A autenticação é por agente e
armazenado em:

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

Opções de correção:

- Executar <<CODE0>> e configurar a autenticação durante o assistente.
- Ou copiar <<CODE1>> do agente principal <<CODE2>> para o agente novo <<CODE3>>>.

Não ** reutilizar <<CODE0>>> entre agentes; causa colisões de autenticação/sessão.

# # Modelo failover e “Todos os modelos falharam”

Como funciona o failover?

O fracasso acontece em duas etapas:

1. **Rotação de perfil de autenticação** dentro do mesmo provedor.
2. **Modelo backback** para o próximo modelo em <<CODE0>>.

Cooldowns aplicam-se a perfis falhantes (backoff exponencial), para que o OpenClaw possa continuar respondendo mesmo quando um provedor está limitado ou falhando temporariamente.

O que significa este erro?

```
No credentials found for profile "anthropic:default"
```

Isso significa que o sistema tentou usar o perfil de autenticação ID <<CODE0>>, mas não conseguiu encontrar credenciais para ele na loja de autenticação esperada.

### Corrigir checklist para Nenhuma credenciais encontradas para perfil anthropicdefault

- ** Confirmar onde vivem os perfis de autenticação** (caminhos novos vs legados)
- Atual: <<CODE0>>
- Legado: <<CODE1>> (migrado por <<CODE2>>)
- ** Confirme que o seu Env Var está carregado pelo Gateway**
- Se você definir <<CODE3>> no seu shell, mas executar o Gateway via systemd/lannched, ele pode não herdá-lo. Coloque-o em <<CODE4>> ou habilite <<CODE5>>>.
- ** Certifique-se de que você está editando o agente correto**
- Configurações multiagentes significam que pode haver vários arquivos <<CODE6>>.
- ** Modelo/Estado de verificação de sanidade
- Use <<CODE7>> para ver modelos configurados e se os provedores são autenticados.

**Checklist fixo para Não foram encontradas credenciais para o perfil antrópico **

Isto significa que a execução está presa a um perfil de autenticação antrópico, mas o Gateway
não o encontra na sua loja de autenticação.

- **Use uma ficha de configuração**
- Executar <<CODE0>>, em seguida, colar com <<CODE1>>.
- Se o token foi criado noutra máquina, use <<CODE2>>>.
- **Se você quiser usar uma chave API em vez disso**
- Coloque <<CODE3>> em <<CODE4>> no hospedeiro **gateway**.
- Limpar qualquer ordem que force um perfil desaparecido.
    ```bash
    openclaw models auth order clear --provider anthropic
    ```
- ** Confirme que você está executando comandos no host gateway**
- No modo remoto, perfis de autenticação vivem na máquina de gateway, não no seu portátil.

# # # Porque é que também tentou o Google Gemini e falhou

Se a configuração do seu modelo incluir o Google Gemini como um backback (ou você mudou para uma abreviação Gemini), o OpenClaw irá tentar durante o backback do modelo. Se você não configurou as credenciais do Google, você verá <<CODE0>>>.

Corrigir: ou fornecer a autenticação do Google, ou remover/evitar modelos do Google em <<CODE0>> / pseudônimos assim que fallback não roteie lá.

**Requisição de LLM rejeitada mensagem pensando assinatura necessária google antigravidade **

Causa: o histórico de sessão contém ** blocos sem assinaturas** (frequentemente de
um fluxo abortado/parcial). Google Antigravity requer assinaturas para blocos de pensamento.

Corrigir: OpenClaw agora tira blocos de pensamento sem assinatura para o Google Antigravity Claude. Se ainda aparecer, inicie uma nova sessão** ou defina <<CODE0>> para esse agente.

# # Perfis de autenticação: o que são e como gerenciá-los

Relacionados: [/conceitos/auth](<<<LINK0>>) (Fluxos de autenticação, armazenamento de fichas, padrões de contas múltiplas)

# # O que é um perfil de autenticação

Um perfil de autenticação é um registro credencial (chave OAuth ou API) ligado a um provedor. Os perfis vivem em:

```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

## O que são IDs de perfil típicos

O OpenClaw utiliza IDs prefixados como:

- <<CODE0>> (comum quando não existe identidade de e- mail)
- <<CODE1> para identidades OAuth
- IDs personalizados que escolher (por exemplo, <<CODE2>>>)

# # # Posso controlar qual perfil de autenticação é tentado primeiro

Sim. A configuração suporta metadados opcionais para perfis e um pedido por provedor (<<<CODE0>>). Isto faz **not** armazenar segredos; ele mapeia IDs para provedor / modo e define ordem de rotação.

OpenClaw pode pular temporariamente um perfil se estiver em um curto **coolingdown** (limites de taxa/tempo limite/auth falhas) ou um maior ** disabled** estado (billing / créditos insuficientes). Para inspecionar isso, execute <<CODE0>>> e verifique <<CODE1>>>. Tuning: <<CODE2>>>.

Você também pode definir um **per-agent** ordem sobreposição (armazenado no <<CODE0>>> desse agente) através do CLI:

```bash
# Defaults to the configured default agent (omit --agent)
openclaw models auth order get --provider anthropic

# Lock rotation to a single profile (only try this one)
openclaw models auth order set --provider anthropic anthropic:default

# Or set an explicit order (fallback within provider)
openclaw models auth order set --provider anthropic anthropic:work anthropic:default

# Clear override (fall back to config auth.order / round-robin)
openclaw models auth order clear --provider anthropic
```

Para atingir um agente específico:

```bash
openclaw models auth order set --provider anthropic --agent main anthropic:default
```

## # OAuth vs API chave qual é a diferença

O OpenClaw suporta ambos:

- **OAuth** muitas vezes aproveita o acesso à subscrição (se aplicável).
- ** As chaves API** utilizam faturamento pay-per-token.

O assistente suporta explicitamente Anthropic setup-token e OpenAI Codex OAuth e pode armazenar chaves API para você.

# # Gateway: portas, “já em execução”, e modo remoto

Que porta é que o portal usa?

<<CODE0> controla a porta multiplexada única para WebSocket + HTTP (Control UI, ganchos, etc.).

Precedência:

```
--port > OPENCLAW_GATEWAY_PORT > gateway.port > default 18789
```

### Por que o status do gateway openclaw diz Runtime em execução, mas a sonda RPC falhou

Porque "running" é a visão** do supervisor (lançado/systemd/schtasks). A sonda RPC é a CLI conectando-se ao gateway WebSocket e chamando <<CODE0>>.

Usar <<CODE0>> e confiar nestas linhas:

- <<CODE0>> (a URL que a sonda realmente usou)
- <<CODE1>> (o que está realmente ligado no porto)
- <<CODE2>> (razão raiz comum quando o processo está vivo, mas a porta não está ouvindo)

# # # # Por que o status do gateway openclaw mostra o serviço Config cli e Config diferente

Você está editando um arquivo de configuração enquanto o serviço está executando outro (muitas vezes um <<CODE0>>> / <<CODE1>> descompasso).

Corrigir:

```bash
openclaw gateway install --force
```

Execute isso do mesmo ambiente <<CODE0>> / que você quer que o serviço use.

## # O que é que outra instância de gateway já está ouvindo significa

O OpenClaw impõe um bloqueio de tempo de execução ao vincular o ouvinte WebSocket imediatamente na inicialização (padrão <<CODE0>>>). Se a ligação falhar com <<CODE1>>, lança <<CODE2>> indicando outra instância já está ouvindo.

Corrigir: parar a outra instância, liberar a porta, ou correr com <<CODE0>>.

## # Como faço para executar OpenClaw em modo remoto cliente se conecta a um Gateway em outro lugar

Definir <<CODE0>> e apontar para uma URL WebSocket remota, opcionalmente com um token/senha:

```json5
{
  gateway: {
    mode: "remote",
    remote: {
      url: "ws://gateway.tailnet:18789",
      token: "your-token",
      password: "your-password",
    },
  },
}
```

Notas:

- <<CODE0>> só começa quando <<CODE1> é <<CODE2>> (ou passa a bandeira de substituição).
- O aplicativo macOS observa o arquivo de configuração e muda de modos ao vivo quando esses valores mudam.

### A interface de controlo diz não autorizada ou continua a ligar-se

Seu gateway está rodando com a autenticação ativada (<<<CODE0>>), mas a UI não está enviando o token/senha correspondente.

Factos (de código):

- O Control UI armazena o token no navegador localStorage chave <<CODE0>.
- A UI pode importar <<CODE1>> (e/ou <<CODE2>>>>) uma vez, em seguida, tira-o da URL.

Corrigir:

- Mais rápido: <<CODE0>> (impressões + cópias link tokenized, tenta abrir; mostra dica SSH se sem cabeça).
- Se ainda não tiver um token: <<CODE1>>>.
- Se remoto, primeiro o túnel: <<CODE2>> em seguida, abra <<CODE3>>>.
- Definir <<CODE4>> (ou <<CODE5>>>) na máquina de gateway.
- Nas configurações de interface de controle, cole o mesmo token (ou refresque com uma única vez <<CODE6>> link).
- Ainda preso? Executar <<CODE7>> e seguir [Troubleshooting](<<LINK0>>>). Ver [Dashboard](<<<LINK1>>>) para detalhes de autenticação.

Eu configurei a tailnet do gatewaybind mas não pode ligar nada ouve

<<CODE0> vincular escolhe um IP de escala de cauda de suas interfaces de rede (100.64.0.0/10). Se a máquina não está na Tailscale (ou a interface está baixa), não há nada para ligar.

Corrigir:

- Iniciar Tailscale na máquina (por isso tem um endereço 100.x), ou
- Mudar para <<CODE0>>/ <<CODE1>>>>>.

Nota: <<CODE0>> é explícita. <<CODE1> prefere loopback; use <<CODE2>> quando você quer uma ligação somente de tailnet.

# # # Eu posso executar vários Gateways no mesmo anfitrião

Normalmente nenhum Gateway pode executar vários canais de mensagens e agentes. Use vários Gateways apenas quando você precisa de redundância (ex: bot de resgate) ou isolamento duro.

Sim, mas você deve isolar:

- <<CODE0> (por exemplo, configuração)
- <<CODE1> (estado de por-instança)
- <<CODE2>> (isolamento do espaço de trabalho)
- <<CODE3> (portes únicos)

Configuração rápida (recomendada):

- Usar <<CODE0>> por instância (auto-cria <<CODE1>>).
- Defina um único <<CODE2>> em cada configuração de perfil (ou passe <<CODE3>> para corridas manuais).
- Instale um serviço por perfil: <<CODE4>>>.

Os perfis também sufixos (<<<CODE0>>>; legado <<CODE1>>>, <<CODE2>>, <<CODE3>>>).
Guia completo: [Gateways múltiplos] (<<<LINK0>>>).

## # O que significa código de aperto de mão inválido 1008

O Gateway é um servidor **WebSocket**, e espera que a primeira mensagem
ser um quadro <<CODE0>>. Se receber mais alguma coisa, fecha a ligação.
com ** código 1008** (violação de política).

Causas comuns:

- Você abriu o URL **HTTP** em um navegador (<<<CODE0>>>) em vez de um cliente WS.
- Usou o caminho errado.
- Um proxy ou túnel despojado de cabeçalhos de autenticação ou enviou um pedido não-Gateway.

Correcções rápidas:

1. Use o URL WS: <<CODE0>> (ou <<CODE1>> se HTTPS).
2. Não abra a porta WS em uma guia normal do navegador.
3. Se a autenticação estiver ligada, inclua o token/password no quadro <<CODE2>>.

Se você estiver usando o CLI ou TUI, o URL deve se parecer com:

```
openclaw tui --url ws://<host>:18789 --token <token>
```

Detalhes do protocolo: [Protocolo Gateway] (<<<LINK0>>>).

# # Registro e depuração

Onde estão os troncos?

Registos de ficheiros (estruturados):

```
/tmp/openclaw/openclaw-YYYY-MM-DD.log
```

Você pode definir um caminho estável via <<CODE0>>>. O nível de log do arquivo é controlado por <<CODE1>>>. A verbosidade da consola é controlada por <<CODE2>> e <<CODE3>>>.

Cauda de registo mais rápida:

```bash
openclaw logs --follow
```

Registos de serviço/supervisor (quando o gateway é executado via launched/systemd):

- macOS: <<CODE0>> e <<CODE1>>> (padrão: <<CODE2>>>; utilização de perfis <<CODE3>>)
- Linux: <<CODE4>>
- Janelas: <<CODE5>>

Ver [Troubleshooting] (<<<LINK0>>>) para mais.

Como faço para iniciar o serviço de Gateway

Use os ajudantes de gateway:

```bash
openclaw gateway status
openclaw gateway restart
```

Se você executar o gateway manualmente, <<CODE0> pode recuperar a porta. Ver [Gateway] (<<<LINK0>>>).

### Eu fechei meu terminal no Windows como faço para reiniciar OpenClaw

Existem **dois modos de instalação do Windows**:

**1) WSL2 (recomendado):** o Gateway é executado dentro do Linux.

Abra PowerShell, digite WSL e reinicie:

```powershell
wsl
openclaw gateway status
openclaw gateway restart
```

Se você nunca instalou o serviço, inicie-o em primeiro plano:

```bash
openclaw gateway run
```

**2) Windows nativos (não recomendado):** o Gateway é executado diretamente no Windows.

Abrir PowerShell e executar:

```powershell
openclaw gateway status
openclaw gateway restart
```

Se o executar manualmente (sem serviço), utilize:

```powershell
openclaw gateway run
```

Docs: [Windows (WSL2)](<<<LINK0>>), [Gateway service runbook](<<LINK1>>).

O portal está pronto mas as respostas nunca chegam O que devo verificar?

Comece com uma rápida varredura de saúde:

```bash
openclaw status
openclaw models status
openclaw channels status
openclaw logs --follow
```

Causas comuns:

- Modelo de autenticação não carregado na máquina **gateway** (verifique <<CODE0>>).
- Respostas de emparelhamento/bloqueio da lista de canais (verifique configuração do canal + logs).
- WebChat/Dashboard está aberto sem o token certo.

Se você é remoto, confirme que a conexão túnel/tailscale está acima e que o
Gateway WebSocket é acessível.

Docs: [Canais] (<<<LINK0>>), [Resolução de problemas] (<<LINK1>>>), [Acesso remoto] (<<LINK2>>>).

# # # Desligado do portal, não há razão para o quê agora

Isso geralmente significa que a UI perdeu a conexão WebSocket. Verificar:

1. O portal está funcionando? <<CODE0>>
2. O Portal é saudável? <<CODE1>>
3. A UI tem o símbolo certo? <<CODE2>>
4. Se remoto, o túnel/tailscale está ligado?

Em seguida, troncos de cauda:

```bash
openclaw logs --follow
```

Documentos: [Dashboard](<<<LINK0>>), [Acesso remoto](<<LINK1>>>), [Troubleshooting](<<LINK2>>>>).

## # Telegram setMyCommands falha com erros de rede O que devo verificar?

Iniciar com logs e status do canal:

```bash
openclaw channels status
openclaw channels logs --channel telegram
```

Se você estiver em um VPS ou por trás de um proxy, confirme que HTTPS é permitido e o DNS funciona.
Se o Gateway for remoto, certifique-se de que você está olhando para logs no anfitrião Gateway.

Docs: [Telegrama] (<<<LINK0>>), [Solução de problemas do canal] (<<LINK1>>>).

# # # TUI não mostra saída O que devo verificar

Primeiro confirme que o Gateway é acessível e o agente pode correr:

```bash
openclaw status
openclaw models status
openclaw logs --follow
```

No TUI, use <<CODE0>> para ver o estado atual. Se espera respostas numa conversa
canal, verifique se a entrega está ativada (<<<CODE1>>>).

Docs: [TUI] (<<<LINK0>>), [Comandos Slash] (<<LINK1>>>).

Como é que paro completamente e depois começo o portal

Se você instalou o serviço:

```bash
openclaw gateway stop
openclaw gateway start
```

Isso para/inicia o serviço ** supervised** (lançado no macOS, systemd no Linux).
Use isto quando o Gateway correr no fundo como um daemon.

Se estiver em primeiro plano, pare com Ctrl-C, então:

```bash
openclaw gateway run
```

Docs: [Runbook serviço Gateway] (<<<LINK0>>).

## # ELI5 openclaw gateway reinicie vs openclaw gateway

- <<CODE0>>: reinicia o serviço de fundo** (lançado/sistemad).
- <<CODE1>>: executa o gateway ** no primeiro plano** para esta sessão de terminal.

Se você instalou o serviço, use os comandos de gateway. Utilizar <<CODE0>> quando
Você quer uma corrida única, primeiro plano.

Qual é a maneira mais rápida de obter mais detalhes quando algo falha

Inicie o Gateway com <<CODE0> para obter mais detalhes do console. Em seguida, inspecione o arquivo de log para erros de autenticação do canal, roteamento do modelo e RPC.

# # Mídia & anexos

## # Minha habilidade gerou uma imagemPDF mas nada foi enviado

Os anexos de saída do agente devem incluir uma linha <<CODE0>> (na sua própria linha). Veja [OpenClaw assistant setup] (<<<LINK0>>) e [Agent send](<<LINK1>>>).

Envio de CLI:

```bash
openclaw message send --target +15555550123 --message "Here you go" --media /path/to/file.png
```

Verifique também:

- O canal alvo suporta mídia de saída e não é bloqueado por allowlists.
- O arquivo está dentro dos limites de tamanho do provedor (imagens são redimensionadas para max 2048px).

Ver [Imagens] (<<<LINK0>>>).

# # Segurança e controle de acesso

É seguro expor a Openclaw a DMs

Tratar os DMs de entrada como dados não confiáveis. Os padrões são projetados para reduzir o risco:

- O comportamento padrão em canais com capacidade para DM é ** paring**:
- Os remetentes desconhecidos recebem um código de emparelhamento; o bot não processa sua mensagem.
- Aprovar com: <<CODE0>>
- Os pedidos pendentes são limitados em **3 por canal**; verifique <<CODE1>> se um código não chegou.
- A abertura pública de DM requer opt-in explícito (<<<CODE2>> e allowlist <<CODE3>>>).

Executar <<CODE0>> para políticas de DM de risco de superfície.

É uma injecção rápida apenas uma preocupação para bots públicos

Não. A injeção imediata é sobre ** conteúdo não confiável**, não apenas quem pode DM o bot.
Se o seu assistente ler conteúdo externo (busca/fetch web, páginas do navegador, e-mails,
documentos, anexos, logs colados), que o conteúdo pode incluir instruções que tentem
para sequestrar o modelo. Isso pode acontecer mesmo se ** você é o único remetente**.

O maior risco é quando as ferramentas estão habilitadas: o modelo pode ser enganado em
Exfiltrar contexto ou ferramentas de chamada em seu nome. Reduzir o raio de explosão em:

- usando um agente "leitor" somente para leitura ou deficiente para resumir conteúdo não confiável
- manter fora <<CODE0>/ <<CODE1>/ <<CODE2>> para agentes habilitados para ferramentas
- sandboxing e ferramentas estritas allowlists

Detalhes: [Segurança] (<<<LINK0>>>).

# # # Se o meu bot tiver seu próprio e-mail conta GitHub ou número de telefone

Sim, para a maioria das instalações. Isolando o bot com contas separadas e números de telefone
reduz o raio de explosão se algo correr mal. Isso também facilita a rotação
credenciais ou revogar o acesso sem afetar suas contas pessoais.

Começar pequeno. Dar acesso apenas às ferramentas e contas que você realmente precisa, e expandir
mais tarde, se necessário.

Docs: [Segurança] (<<<LINK0>>), [Pairing] (<<LINK1>>>>).

# # # Posso dar-lhe autonomia sobre as minhas mensagens de texto e é tão seguro

Nós **não** recomendamos total autonomia sobre suas mensagens pessoais. O padrão mais seguro é:

- Mantenha os DMs em modo ** paring** ou uma lista de permissão apertada.
- Use um número ** separado ou conta** se você quiser que ele envie uma mensagem em seu nome.
- Deixe-o redigir, então ** aprove antes de enviar**.

Se quiser experimentar, faça-o numa conta dedicada e mantenha-a isolada. Ver
[Segurança] (<<<LINK0>>>).

## # Posso usar modelos mais baratos para tarefas de assistente pessoal

Sim, ** se** o agente é somente para chat e a entrada é confiável. Níveis menores são
mais suscetíveis ao sequestro de instruções, por isso evite-os para agentes habilitados para ferramentas
ou ao ler conteúdo não confiável. Se você precisa usar um modelo menor, bloqueie
ferramentas e correr dentro de uma caixa de areia. Ver [Segurança] (<<<LINK0>>>).

Comecei no Telegram mas não consegui um código de emparelhamento.

Códigos de pareamento são enviados **apenas** quando um remetente desconhecido envia mensagens do bot e
<<CODE0>> está habilitado. <<CODE1> por si só não gera um código.

Verificar os pedidos pendentes:

```bash
openclaw pairing list telegram
```

Se você quiser acesso imediato, allowlist seu remetente id ou set <<CODE0>
por essa conta.

WhatsApp vai enviar mensagens aos meus contactos Como funciona o pareamento

Não. A política padrão do WhatsApp DM é ** paring**. Os remetentes desconhecidos só recebem um código de pareamento e sua mensagem é ** não processada**. O OpenClaw só responde aos chats que recebe ou para explicitar, envia-lhe o gatilho.

Aprovar o emparelhamento com:

```bash
openclaw pairing approve whatsapp <code>
```

Listar os pedidos pendentes:

```bash
openclaw pairing list whatsapp
```

Prompt de número de telefone Wizard: é usado para definir seu **allowlist / proprietário** para que seus próprios DMs são permitidos. Não é usado para envio automático. Se você executar em seu número pessoal WhatsApp, use esse número e habilite <<CODE0>>.

# # # Comandos de bate-papo, abortar tarefas e “não vai parar”

### Como paro as mensagens internas do sistema de mostrar no chat

A maioria das mensagens internas ou de ferramentas só aparecem quando **verbose** ou **raciocínio** está habilitado
para aquela sessão.

Corrigir no chat onde você vê:

```
/verbose off
/reasoning off
```

Se ainda estiver barulhento, verifique as configurações da sessão na interface de controle e configure o verbose
a **herda**. Também confirmar que você não está usando um perfil bot com <<CODE0>> definido
para <<CODE1> na configuração.

Docs: [Pensando e verbose] (<<<LINK0>>), [Segurança] (<<LINK1>>).

## # Como eu paro de cancelar uma tarefa em execução

Enviar qualquer um destes ** como uma mensagem independente** (sem corte):

```
stop
abort
esc
wait
exit
interrupt
```

Estes são gatilhos abortados (não comandos slash).

Para processos de fundo (a partir da ferramenta exec), você pode pedir ao agente para executar:

```
process action:kill sessionId:XXX
```

Visão geral dos comandos Slash: ver [Comandos Slash] (<<<LINK0>>).

A maioria dos comandos deve ser enviada como uma mensagem ** standalone** que começa com <<CODE0>>, mas alguns atalhos (como <<CODE1>>>) também funcionam em linha para remetentes listados.

## # Como faço para enviar uma mensagem Discord do Telegram Crosscontext mensagem negada

Blocos OpenClaw **cross-provider** mensagens por padrão. Se uma chamada de ferramenta estiver ligada
para Telegram, ele não vai enviar para Discord a menos que você explicitamente permitir.

Habilitar mensagens entre fornecedores para o agente:

```json5
{
  agents: {
    defaults: {
      tools: {
        message: {
          crossContext: {
            allowAcrossProviders: true,
            marker: { enabled: true, prefix: "[from {channel}] " },
          },
        },
      },
    },
  },
}
```

Reinicie o gateway após a configuração da edição. Se você quiser isso para um único
agente, defina-o em <<CODE0>> em vez disso.

# # # Porque parece que o bot ignora mensagens de fogo rápido

O modo fila controla como novas mensagens interagem com uma execução em voo. Usar <<CODE0>> para alterar os modos:

- <<CODE0>> - novas mensagens redirecionam a tarefa atual
- <<CODE1>> - executar mensagens uma de cada vez
- <<CODE2>> - mensagens em lote e resposta uma vez (padrão)
- <<CODE3>> - dirigir agora, em seguida, processar backlog
- <<CODE4>> - abortar a execução atual e iniciar de novo

Você pode adicionar opções como <<CODE0>> para modos de seguimento.

# # Responder à pergunta exata do registro de captura de tela / chat

**Q: “Qual é o modelo padrão para Anthropic com uma chave API?”**

**A:**No OpenClaw, credenciais e seleção de modelos são separadas. A configuração <<CODE0>> (ou o armazenamento de uma chave de API antrópica em perfis de autenticação) permite a autenticação, mas o modelo padrão é o que quer que você configure em <<CODE1>>> (por exemplo, <<CODE2>>> ou <<CODE3>>>). Se você ver <<CODE4>>, significa que o Gateway não conseguiu encontrar credenciais antrópicas no esperado <<CODE5>> para o agente que está em execução.

---

Ainda preso? Pergunte em [Discord](<<<LINK0>>>) ou abra uma discussão [GitHub](<<LINK1>>>).
