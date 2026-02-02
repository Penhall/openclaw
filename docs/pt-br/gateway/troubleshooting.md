---
summary: "Quick troubleshooting guide for common OpenClaw failures"
read_when:
  - Investigating runtime issues or failures
---

* Resolução de problemas *

Quando a Openclaw se comportar mal, aqui está como consertá-la.

Comece com as FAQs [Primeiros 60 segundos](<<<LINK0>>) se você quiser apenas uma receita de triagem rápida. Esta página vai mais fundo em falhas de execução e diagnósticos.

Atalhos específicos do fornecedor: [/canais/destruição de problemas](<<<LINK0>>>)

# # Status & Diagnósticos

Comandos de triagem rápida (em ordem):

Comando O que lhe diz Quando usá-lo
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Resumo local: OS + atualização, alcancebilidade/modo de gateway, serviço, agentes/sessões, estado de configuração do provedor
* <<CODE1>> * Diagnóstico local completo (somente leitura, pastoso, seguro) incl. cauda log Quando você precisa compartilhar um relatório de depuração
□ <<CODE2>> □ Executa verificações de saúde de gateway (incl. sondas de provedor; requer gateway acessível)
□ < <<CODE3>> Quando você suspeita que você está sondando o portal errado
<<CODE4>> Pergunta ao gateway em execução para o status do canal (e, opcionalmente, sondas) Quando o gateway é acessível, mas os canais se comportam mal
Estado de supervisão (lançado/sistemad/schtasks), PID/saída em tempo de execução, último erro de gateway Quando o serviço “parece carregado” mas nada é executado
(melhor sinal para problemas de execução) Quando você precisa da razão de falha real

**Sharing output:** prefira <<CODE0>> (edita fichas). Se você colar <<CODE1>>, considere a configuração <<CODE2>> primeiro (previsões).

Ver também: [Cheques de saúde] (<<<LINK0>>) e [Logging] (<<LINK1>>>).

# # Questões comuns

## # Nenhuma chave API encontrada para provedor "antrópico"

Isso significa que a loja de autenticação do agente está vazia** ou faltando credenciais antrópicas.
Auth é **por agente**, então um novo agente não herdará as chaves do agente principal.

Opções de correção:

- Repetir a bordo e escolher **Anthropic** para esse agente.
- Ou cole uma ficha de configuração na máquina **gateway**:
  ```bash
  openclaw models auth setup-token --provider anthropic
  ```
- Ou copiar <<CODE0>> da dir principal do agente para a dir nova do agente.

Verificar:

```bash
openclaw models status
```

### A atualização do token OAuth falhou (subscrição antrópica do Claude)

Isso significa que o token de OAuth Antrópico armazenado expirou e a atualização falhou.
Se você está em uma assinatura Claude (sem chave API), a solução mais confiável é
mude para um **Claude Code setup-token** e cole-o no **gateway host**.

** Recomendado (configurado): **

```bash
# Run on the gateway host (paste the setup-token)
openclaw models auth setup-token --provider anthropic
openclaw models status
```

Se você gerou o token em outro lugar:

```bash
openclaw models auth paste-token --provider anthropic
openclaw models status
```

Mais detalhes: [Antrópico] (<<<LINK0>>) e [OAuth] (<<LINK1>>).

### A interface de controle falha em HTTP ("identidade necessária" / "falha na conexão")

Se você abrir o painel sobre HTTP simples (por exemplo, <<CODE0>> ou
<<CODE1>>), o navegador roda em um contexto **não seguro** e
bloqueia WebCrypto, para que a identidade do dispositivo não possa ser gerada.

**Fix:**

- Prefere HTTPS via [Tailscale Serve] (<<<LINK0>>>).
- Ou abra localmente na máquina de gateway: <<CODE0>>.
- Se você tiver que ficar em HTTP, habilite <<CODE1>> e
usar um token de gateway (somente em papel; sem identidade/pareamento do dispositivo). Ver
[Control UI] (<<<LINK1>>>>).

Falhou a análise dos segredos da CI

Isso significa que <<CODE0> encontraram novos candidatos ainda não na linha de base.
Siga [Scanagem secreta] (<<<LINK0>>>).

# # # Serviço Instalado mas Nada está em execução

Se o serviço de gateway estiver instalado, mas o processo sair imediatamente, o serviço
pode aparecer “carregado” enquanto nada está em execução.

** Verificar:**

```bash
openclaw gateway status
openclaw doctor
```

O médico/serviço mostrará o estado de execução (PID/última saída) e as dicas de log.

**Logs:**

- Preferido: <<CODE0>>
- Registos de ficheiros (sempre): <<CODE1>> (ou o seu configurado <<CODE2>>>)
- macOS LaunchAgent (se instalado): <<CODE3>> e <<CODE4>>>
- Linux systemd (se instalado): <<CODE5>>
- Windows: <<CODE6>>

** Enable more loging:**

- Detalhes do ficheiro Bump (persistente JSONL):
  ```json
  { "logging": { "level": "debug" } }
  ```
- Verbosidade do console Bump (apenas saída TTY):
  ```json
  { "logging": { "consoleLevel": "debug", "consoleStyle": "pretty" } }
  ```
- Dica rápida: <<CODE0> afeta **console** apenas saída. Os registros de arquivos permanecem controlados por <<CODE1>>>>.

Veja [/logging](<<<LINK0>>>) para uma visão completa dos formatos, configuração e acesso.

### "Comece a porta bloqueada: definir gateway.mode=local"

Isso significa que a configuração existe, mas <<CODE0>> está desativada (ou não <<CODE1>>>), então o
O portal recusa-se a começar.

**Fix (recomendado): **

- Execute o assistente e defina o modo de execução Gateway como **Local**:
  ```bash
  openclaw configure
  ```
- Ou ajustá-lo directamente.
  ```bash
  openclaw config set gateway.mode local
  ```

** Se você pretendia executar um Gateway remoto em vez disso:**

- Defina um URL remoto e mantenha <<CODE0>>:
  ```bash
  openclaw config set gateway.mode remote
  openclaw config set gateway.remote.url "wss://gateway.example.com"
  ```

** Ad-hoc/dev somente:** passe <<CODE0>> para iniciar o gateway sem
<<CODE1>>>.

** Nenhum arquivo de configuração ainda?** Execute <<CODE0>> para criar uma configuração inicial, então reexecute
O portal.

## # Ambiente de serviço (PATH + tempo de execução)

O serviço de gateway é executado com um **PATH mínimo** para evitar shell/manager cruft:

- macOS: <<CODE0>>, <<CODE1>>, <<CODE2>>, <<CODE3>
- Linux: <<CODE4>>, <<CODE5>>, <<CODE6>>

Isto exclui intencionalmente os gestores de versões (nvm/fnm/volta/asdf) e o pacote
gerenciadores (pnpm/npm) porque o serviço não carrega seu init shell. Tempo de execução
variáveis como <<CODE0>> devem viver em <<CODE1>> (carregado cedo pelo
gateway).
O Exec é executado em <<CODE2>> mesclar sua caixa de login <<CODE3>> no ambiente exec,
ferramentas assim ausentes geralmente significa que seu shell init não está exportando-los (ou definir
<<CODE4>>). Ver [/tools/exec] (<<<LINK0>>>).

Os canais WhatsApp + Telegram requerem **Node**; Bun não é suportado. Se a sua
o serviço foi instalado com Bun ou um caminho Node gerenciado por versões, execute <<CODE0>
migrar para uma instalação do Node do sistema.

## # Habilidade faltando chave API em sandbox

** Sintoma: ** A habilidade funciona no host, mas falha na sandbox com a chave de API faltando.

** Por que:** sandboxed exec corre dentro do Docker e não ** herdar host <<CODE0>>.

**Fix:**

- definido <<CODE0>> (ou por agente <<CODE1>>)
- ou cozer a chave em sua imagem personalizada sandbox
- correr depois <<CODE2>> (ou <<CODE3>>>)

# # Serviço a correr mas Porto a não ouvir

Se o serviço reporta ** rodando** mas nada está ouvindo na porta de gateway,
O portal provavelmente recusou-se a ligar.

** O que significa "correr" aqui**

- <<CODE0>> significa que o seu supervisor (lançado/systemd/schtasks) pensa que o processo está vivo.
- <<CODE1> significa que o CLI poderia realmente se conectar ao WebSocket gateway e chamar <<CODE2>>.
- Sempre confie em <<CODE3>>+<<CODE4>> como as linhas “o que realmente tentamos?”.

** Verificar:**

- <<CODE0>> deve ser <<CODE1>> para <<CODE2>> e para o serviço.
- Se você definir <<CODE3>>, o **CLI padrão** para uma URL remota. O serviço ainda pode ser executado localmente, mas seu CLI pode estar sondando o lugar errado. Use <<CODE4>> para ver a porta + alvo da sonda resolvida do serviço (ou passe <<CODE5>>>).
- <<CODE6>> e <<CODE7>> superficie o **último erro de gateway** de logs quando o serviço parece em execução, mas a porta está fechada.
- As ligações não- loopback (<<<<CODE8>/<<CODE9>>/<<CODE10>>, ou <<CODE11> quando o loopback não está disponível) requerem autorização:
<<CODE12>> (ou <<CODE13>>>).
- <<CODE14>> é apenas para chamadas CLI remotas; não ** habilita a autenticação local.
- <<CODE15>> é ignorado; utilização <<CODE16>>>.

** Se <<CODE0> mostrar um descompasso de configuração**

- <<CODE0>> e <<CODE1>> devem normalmente corresponder.
- Se eles não, você está quase certamente editando uma configuração enquanto o serviço está executando outra.
- Correção: reexecução <<CODE2>> do mesmo <<CODE3>>/ <HTML4>> quer que o serviço seja utilizado.

** Se <<CODE0> reportar problemas de configuração do serviço**

- A configuração do supervisor (lançamento/systemd/schtasks) está faltando padrões atuais.
- Corrigir: executar <<CODE0>> para atualizá-lo (ou <<CODE1>> para uma reescrita completa).

** Se <<CODE0> mencionar “recusar a ligação ... sem autorização”**

- Você ajustou <<CODE0>> para um modo não-loopback (<<CODE1>>/<<CODE2>/<<CODE3>>, ou <<CODE4> quando o loopback não está disponível) mas não configurou a autenticação.
- Corrigir: definir <<CODE5>> + <<CODE6>> (ou exportar <<CODE7>>>>) e reiniciar o serviço.

** Se <<CODE0>> diz <<CODE1>> mas nenhuma interface tailnet foi encontrada**

- O gateway tentou ligar-se a um IP Tailscale (100.64.0.0/10) mas nenhum foi detectado no host.
- Corrigir: aumentar a escala de cauda nessa máquina (ou alterar <<CODE0>> para <<CODE1>>/<<CODE2>>>).

** Se <<CODE0> diz que a sonda usa loopback**

- Isso é esperado para <<CODE0>>: o gateway escuta em <<CODE1>> (todas as interfaces), e loopback ainda deve se conectar localmente.
- Para clientes remotos, use um IP LAN real (não <<CODE2>>) mais a porta, e garantir que a autenticação está configurada.

## # Endereço já em uso (Porto 18789)

Isso significa que algo já está ouvindo na porta de entrada.

** Verificar:**

```bash
openclaw gateway status
```

Ele mostrará o(s) ouvinte(s) e causas prováveis (porta já em execução, túnel SSH).
Se necessário, pare o serviço ou escolha uma porta diferente.

## # Pastas extra de Área de Trabalho Detectadas

Se você atualizou de instalações antigas, você ainda pode ter <<CODE0>> no disco.
Vários diretórios de espaço de trabalho podem causar confusão auth ou estado drif porque
apenas um espaço de trabalho está ativo.

**Fix:** mantenha um único espaço de trabalho ativo e arquivo/remove o resto. Ver
[Espaço de trabalho do agente](<<<LINK0>>>).

## # bate-papo principal em execução em uma área de trabalho sandbox

Sintomas: <<CODE0>> ou as ferramentas de arquivos mostram <<CODE1>> mesmo que você
esperava o espaço de trabalho do anfitrião.

** Por que:** <<CODE0>> chaves desligadas <<CODE1>> (padrão <<CODE2>>).
Sessões de grupo/canal usam suas próprias chaves, então elas são tratadas como não principais e
Obter espaços de trabalho da caixa de areia.

** Opções de reparação:**

- Se você quiser espaços de trabalho de host para um agente: set <<CODE0>>.
- Se você quer acesso à área de trabalho do host dentro da sandbox: set <<CODE1>> para esse agente.

"Agente foi abortado"

O agente foi interrompido no meio da resposta.

Causas:

- O utilizador enviou <<CODE0>>, <<CODE1>>, <<CODE2>>, <<CODE3>>, ou <<CODE4>>>
- Tempo- limite excedido
- O processo caiu.

**Fix:** Basta enviar outra mensagem. A sessão continua.

### "O agente falhou antes de responder: Modelo desconhecido: anthropic/claude-haiku-3-5"

OpenClaw rejeita intencionalmente ** modelos mais antigos / inseguros** (especialmente aqueles mais
vulnerável à injecção imediata). Se vir este erro, o nome do modelo não é
mais tempo suportado.

**Fix:**

- Escolha um modelo **latest** para o provedor e atualize seu config ou alias do modelo.
- Se tiver dúvidas sobre quais os modelos disponíveis, execute <<CODE0>> ou
<<CODE1> e escolha uma suportada.
- Verifica os registos de gateway pela razão detalhada.

Ver também: [Modelos CLI] (<<<LINK0>>) e [Fornecedores de modelos] (<<LINK1>>).

## # Mensagens Não Acionando

** Verificar 1:** O remetente está autorizado?

```bash
openclaw status
```

Procure por <<CODE0>> na saída.

** Verificar 2:** Para chats em grupo, é necessária menção?

```bash
# The message must match mentionPatterns or explicit mentions; defaults live in channel groups/guilds.
# Multi-agent: `agents.list[].groupChat.mentionPatterns` overrides global patterns.
grep -n "agents\\|groupChat\\|mentionPatterns\\|channels\\.whatsapp\\.groups\\|channels\\.telegram\\.groups\\|channels\\.imessage\\.groups\\|channels\\.discord\\.guilds" \
  "${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw/openclaw.json}"
```

** Verificar 3:** Verificar os registos

```bash
openclaw logs --follow
# or if you want quick filters:
tail -f "$(ls -t /tmp/openclaw/openclaw-*.log | head -1)" | grep "blocked\\|skip\\|unauthorized"
```

# # # Código de Emparelhamento Não Chegando

Se <<CODE0>> for <<CODE1>>, os remetentes desconhecidos devem receber um código e sua mensagem é ignorada até ser aprovada.

** Verificar 1:** Um pedido pendente já está à espera?

```bash
openclaw pairing list <channel>
```

As requisições de emparelhamento de DM pendentes são **3 por canal** por padrão. Se a lista estiver cheia, novos pedidos não gerarão um código até que um seja aprovado ou expire.

** Verificar 2:** O pedido foi criado mas nenhuma resposta foi enviada?

```bash
openclaw logs --follow | grep "pairing request"
```

** Verificar 3:** Confirmar <<CODE0>> não é <<CODE1>/<<CODE2>> para esse canal.

### Imagem + Menção Não Funciona

Problema conhecido: Quando você envia uma imagem com APENAS uma menção (sem outro texto), WhatsApp às vezes não inclui os metadados de menção.

** Solução:** Adicione algum texto com a menção:

- ↔ <<CODE0>> + imagem
- <<CODE1>> + imagem

Sessão Não Continuando

** Verificar 1:** O ficheiro da sessão está aí?

```bash
ls -la ~/.openclaw/agents/<agentId>/sessions/
```

** Verificar 2:** A janela de reset é muito curta?

```json
{
  "session": {
    "reset": {
      "mode": "daily",
      "atHour": 4,
      "idleMinutes": 10080 // 7 days
    }
  }
}
```

**Check 3:** Alguém enviou <<CODE0>>, <<CODE1>>, ou um gatilho de reset?

Agente Timing Out

Tempo padrão é de 30 minutos. Para tarefas longas:

```json
{
  "reply": {
    "timeoutSeconds": 3600 // 1 hour
  }
}
```

Ou use a ferramenta <<CODE0>> para comandos de fundo longos.

# # WhatsApp Desligado

```bash
# Check local status (creds, sessions, queued events)
openclaw status
# Probe the running gateway + channels (WA connect + Telegram + Discord APIs)
openclaw status --deep

# View recent connection events
openclaw logs --limit 200 | grep "connection\\|disconnect\\|logout"
```

**Fix:** Normalmente reconecta automaticamente uma vez que o Gateway está rodando. Se você estiver preso, reinicie o processo Gateway (no entanto, você o supervisiona) ou execute-o manualmente com a saída verbose:

```bash
openclaw gateway --verbose
```

Se você está logado / desconectado:

```bash
openclaw channels logout
trash "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials" # if logout can't cleanly remove everything
openclaw channels login --verbose       # re-scan QR
```

# # # A mídia manda falhar

** Verificar 1:** O caminho do arquivo é válido?

```bash
ls -la /path/to/your/image.jpg
```

** Verificar 2:** É muito grande?

- Imagens: max 6MB
- Áudio/Vídeo: max 16MB
- Documentos: max 100MB

** Verificar 3:** Verificar registros de mídia

```bash
grep "media\\|fetch\\|download" "$(ls -t /tmp/openclaw/openclaw-*.log | head -1)" | tail -20
```

Uso de Alta Memória

OpenClaw mantém o histórico de conversas na memória.

**Fix:** Reiniciar periodicamente ou definir limites de sessão:

```json
{
  "session": {
    "historyLimit": 100 // Max messages to keep
  }
}
```

# # Solução comum de problemas

### “Gateway não começa — configuração inválida”

O OpenClaw agora se recusa a iniciar quando a configuração contém chaves desconhecidas, valores malformados ou tipos inválidos.
Isto é intencional por segurança.

Conserte com o Doutor:

```bash
openclaw doctor
openclaw doctor --fix
```

Notas:

- <<CODE0> reporta todas as entradas inválidas.
- <<CODE1> aplica migrações/reparações e reescreve a configuração.
- Comandos diagnósticos como <<CODE2>>, <<CODE3>>, <<CODE4>>, <<CODE5>, e <<CODE6> ainda funcionam mesmo que a configuração seja inválida.

### “Todos os modelos falharam” – o que devo verificar primeiro?

- ** Credenciais** presentes para o(s) provedor(es) que estão sendo tentados (perfis auth + env vars).
- **Modelo de roteamento**: confirmar <<CODE0>> e fallbacks são modelos que você pode acessar.
- ** Registros de gateway** em <<CODE1>> para o erro exato do provedor.
- Estado do modelo**: utilizar <<CODE2>> (chat) ou <<CODE3>> (CLI).

# # # # Eu estou correndo em meu número pessoal WhatsApp – por que é estranho self-chat?

Active o modo de self-chat e allowlist seu próprio número:

```json5
{
  channels: {
    whatsapp: {
      selfChatMode: true,
      dmPolicy: "allowlist",
      allowFrom: ["+15555550123"],
    },
  },
}
```

Veja [Configuração do WhatsApp] (<<<LINK0>>).

O WhatsApp desligou-me. Como posso reabrir?

Execute o comando de login novamente e verifique o código QR:

```bash
openclaw channels login
```

### Construir erros em <<CODE0>> — qual é o caminho padrão de correção?

1. <<CODE0>>
2. <<CODE1>>
3. Verifique problemas do GitHub ou Discórdia
4. Solução temporária: confira um commit mais antigo

### npm install fails (allow-build-scripts / faltando tar ou yargs). E agora?

Se você estiver correndo do código fonte, use o gerenciador de pacotes do repo: **pnpm** (preferido).
O repo declara <<CODE0>>>>.

Recuperação típica:

```bash
git status   # ensure you’re in the repo root
pnpm install
pnpm build
openclaw doctor
openclaw gateway restart
```

Por que: pnpm é o gerenciador de pacotes configurado para este repo.

### Como faço para alternar entre git installs e npm installs?

Use o instalador ** website** e selecione o método de instalação com uma bandeira. Ele
atualiza e reescreve o serviço de gateway para apontar para a nova instalação.

Mudar para git install**:

```bash
curl -fsSL https://openclaw.bot/install.sh | bash -s -- --install-method git --no-onboard
```

Mudar para npm global**:

```bash
curl -fsSL https://openclaw.bot/install.sh | bash
```

Notas:

- O fluxo git só rebase se o repo estiver limpo. Persistir ou alterar stash primeiro.
- Depois de mudar, corra.
  ```bash
  openclaw doctor
  openclaw gateway restart
  ```

## # Telegram block streaming não é dividir texto entre chamadas de ferramenta. Porquê?

O streaming em bloco apenas envia **blocos de texto completos**. Razões comuns para ver uma única mensagem:

- <<CODE0>> é ainda <<CODE1>>>.
- <<CODE2>> é definido como <<CODE3>>>.
- <<CODE4>> é <<CODE5>> ou <<CODE6>>> ** e o rascunho de streaming está ativo**
(papo privado + tópicos). O rascunho de transmissão desactiva a transmissão de blocos nesse caso.
- Suas configurações de <<CODE7>>/coalesce são muito altas, então pedaços são fundidos.
- O modelo emite um grande bloco de texto (sem pontos de resposta média).

Corrigir a lista de verificação:

1. Coloque configurações de streaming de bloco em <<CODE0>>, não a raiz.
2. Definir <<CODE1>> se você quiser respostas reais em bloco multi-mensagem.
3. Use menores limiares de bloco/coalesce durante a depuração.

Ver [Streaming] (<<<LINK0>>>).

### Discórdia não responde no meu servidor mesmo com <<CODE0>>. Porquê?

<<CODE0> apenas controles mencionam ** depois** as listas de autorizações de canais.
Por padrão <<CODE1> é **allowlist**, então guilds devem estar explicitamente habilitados.
Se você definir <<CODE2>>, apenas os canais listados são permitidos; omita-os para permitir todos os canais na guild.

Corrigir a lista de verificação:

1. Definir <<CODE0>> **ou** adicionar uma entrada de lista de allowlist guild (e opcionalmente uma lista de allowlist de canal).
2. Use ** IDs de canais numéricos** em <<CODE1>>.
3. Coloque <<CODE2>> ** em** <<CODE3>> (global ou por canal).
Nível superior <<CODE4>> não é uma chave suportada.
4. Certifique-se que o bot tem **Message Content Intent** e permissões de canal.
5. Executar <<CODE5>> para dicas de auditoria.

Docs: [Discord] (<<<LINK0>>), [Channels solutioning] (<<LINK1>>>).

### Cloud Code Assist API error: invalid tool schema (400). E agora?

Este é quase sempre um **tool compatibilidade esquema** problema. Ajuda ao Código de Nuvem
endpoint aceita um subconjunto restrito de Esquema JSON. Ferramenta de limpeza OpenClaw/normaliza
esquemas em corrente <<CODE0>>, mas a correção ainda não está na última versão (a partir de
13 de janeiro de 2026).

Corrigir a lista de verificação:

1. **Atualizar OpenClaw**:
- Se você pode correr do código fonte, puxe <<CODE0>> e reinicie o gateway.
- Caso contrário, espere pela próxima versão que inclui o esquema de limpeza.
2. Evite palavras-chave não suportadas como <<CODE1>>, <<CODE2>>,
<<CODE3>>, <<CODE4>>, <<CODE5>>, <<CODE6>>, etc.
3. Se você definir ferramentas personalizadas, mantenha o esquema de topo como <<CODE7> com
<<CODE8>> e enums simples.

Ver [Ferramentas] (<<<LINK0>>) e [Esquemas de Tipos] (<<LINK1>>).

# # questões específicas do macOS

## # A aplicação bate ao conceder permissões (Speech/Mic)

Se o aplicativo desaparecer ou mostrar "Abort trap 6" quando você clicar em "Permitir" em um prompt de privacidade:

**Fix 1: Reset TCC Cache**

```bash
tccutil reset All bot.molt.mac.debug
```

**Fix 2: Force New Bundle ID**
Se a redefinição não funcionar, altere o <<CODE0>> em [<<CODE1>>>](<<LINK0>>>) (por exemplo, adicione um <<CODE2>>> sufixo) e reconstrua. Isso força o macOS a tratá-lo como um novo aplicativo.

Portão preso em "Começando..."

O aplicativo se conecta a um gateway local no porto <<CODE0>>. Se ficar preso:

**Fix 1: Pare o supervisor (preferido)**
Se o portal for supervisionado pelo lançamento, matar o PID irá reabastecê-lo. Pare o supervisor primeiro:

```bash
openclaw gateway status
openclaw gateway stop
# Or: launchctl bootout gui/$UID/bot.molt.gateway (replace with bot.molt.<profile>; legacy com.openclaw.* still works)
```

**Fix 2: Porto está ocupado (encontrar o ouvinte)**

```bash
lsof -nP -iTCP:18789 -sTCP:LISTEN
```

Se é um processo não supervisionado, tente uma paragem graciosa primeiro, em seguida, aumentar:

```bash
kill -TERM <PID>
sleep 1
kill -9 <PID> # last resort
```

**Fix 3: Verifique a instalação CLI**
Garantir o nível global <<CODE0>> O CLI está instalado e corresponde à versão do aplicativo:

```bash
openclaw --version
npm install -g openclaw@<version>
```

# # Modo de depuração

Obter registro de verbose:

```bash
# Turn on trace logging in config:
#   ${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw/openclaw.json} -> { logging: { level: "trace" } }
#
# Then run verbose commands to mirror debug output to stdout:
openclaw gateway --verbose
openclaw channels login --verbose
```

# # Locais de registro

Localização do registro
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
(ou <<CODE1>>>)
□ Registos de serviços de Gateway (supervisor) <br />Linux: <<CODE6>> <br /> Janelas: <<CODE7>>
Os ficheiros de sessão são:
* Cache de mídia * <<CODE9>>
Credenciais <<CODE10>>

# # Verificação de Saúde

```bash
# Supervisor + probe target + config paths
openclaw gateway status
# Include system-level scans (legacy/extra services, port listeners)
openclaw gateway status --deep

# Is the gateway reachable?
openclaw health --json
# If it fails, rerun with connection details:
openclaw health --verbose

# Is something listening on the default port?
lsof -nP -iTCP:18789 -sTCP:LISTEN

# Recent activity (RPC log tail)
openclaw logs --follow
# Fallback if RPC is down
tail -20 /tmp/openclaw/openclaw-*.log
```

# # Reiniciar tudo

Opção nuclear:

```bash
openclaw gateway stop
# If you installed a service and want a clean install:
# openclaw gateway uninstall

trash "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
openclaw channels login         # re-pair WhatsApp
openclaw gateway restart           # or: openclaw gateway
```

Isso perde todas as sessões e requer re-pairing WhatsApp.

# # Obtendo Ajuda

1. Primeiro check logs: <<CODE0>>> (padrão: <<CODE1>>>, ou seu configurado <<CODE2>>)
2. Procurar problemas existentes no GitHub
3. Abra uma nova edição com:
- Versão Openclaw
- Excertos de log relevantes
- Passos para reproduzir
- A sua configuração (redact secrets!)

---

"Você já tentou desligá-lo e ligar novamente?"  — Cada pessoa de TI

□

# # # Navegador Não Iniciado (Linux)

Se vir <<CODE0>>:

** Causa mais provável:** Chromium embalado com Snap no Ubuntu.

** Correção rápida:** Instale o Google Chrome em vez disso:

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

Em seguida, definir na configuração:

```json
{
  "browser": {
    "executablePath": "/usr/bin/google-chrome-stable"
  }
}
```

** Guia completo:** Veja [browser-linux-troubleshooting] (<<<LINK0>>)
