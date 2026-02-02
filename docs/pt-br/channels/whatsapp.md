---
summary: "WhatsApp (web channel) integration: login, inbox, replies, media, and ops"
read_when:
  - Working on WhatsApp/web channel behavior or inbox routing
---

# WhatsApp (canal web)

Status: WhatsApp Web via somente Baileys. O Gateway possui a(s) sessão(ões).

## Montagem rápida (início)

1. Use um número de telefone ** separado** se possível (recomendado).
2. Configure WhatsApp em`~/.openclaw/openclaw.json`.
3. Execute`openclaw channels login`para verificar o código QR (dispositivos conectados).
4. Inicie o portal.

Configuração mínima:

```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551234567"],
    },
  },
}
```

## Objetivos

- Várias contas WhatsApp (multi-conta) em um processo Gateway.
- Roteamento determinístico: respostas retornar ao WhatsApp, sem roteamento de modelo.
- Modelo vê contexto suficiente para entender as respostas citadas.

## A configuração escreve

Por padrão, WhatsApp é permitido escrever atualizações de configuração acionadas pelo`/config set|unset`(requer`commands.config: true`.

Desactivar com:

```json5
{
  channels: { whatsapp: { configWrites: false } },
}
```

## Arquitetura (que possui o quê)

- **Gateway** possui o soquete Baileys e loop de caixa de entrada.
- **CLI / app macOS** fale com o gateway; nenhum uso direto do Baileys.
- ** Ouvinte ativo** é necessário para envios de saída; caso contrário, o envio falha rapidamente.

## Obtendo um número de telefone (dois modos)

WhatsApp requer um número de celular real para verificação. VoIP e números virtuais geralmente são bloqueados. Existem duas maneiras suportadas de executar Openclaw no WhatsApp:

## # Número dedicado (recomendado)

Use um número de telefone ** separado para OpenClaw. Melhor UX, roteamento limpo, sem auto-conversas. Configuração ideal: **spare/old Android phone + eSIM**. Deixe-o em Wi-Fi e energia, e ligue-o via QR.

** WhatsApp Business:** Você pode usar o WhatsApp Business no mesmo dispositivo com um número diferente. Ótimo para manter seu WhatsApp pessoal separado — instale o WhatsApp Business e registre o número OpenClaw lá.

**Config Sample (número dedicado, allowlist de um usuário):**

```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551234567"],
    },
  },
}
```

** Modo de embalagem (opcional): **
Se você quiser pareamento em vez de allowlist, defina`channels.whatsapp.dmPolicy`para`pairing`. Os remetentes desconhecidos recebem um código de pareamento; aprovam com:`openclaw pairing approve whatsapp <code>`

## Número pessoal (fallback)

Retrocesso rápido: execute OpenClaw em **seu próprio número**. Message yourself (WhatsApp “Message yourself”) para testar para que você não spam contatos. Espere ler códigos de verificação em seu telefone principal durante a configuração e experimentos. ** Deve ativar o modo de self-chat.**
Quando o assistente pedir seu número pessoal do WhatsApp, digite o telefone de onde você irá enviar mensagem (do proprietário/enviar), não o número assistente.

**Config Sample (número pessoal, auto-conversa):**

```json
{
  "whatsapp": {
    "selfChatMode": true,
    "dmPolicy": "allowlist",
    "allowFrom": ["+15551234567"]
  }
}
```

Respostas por omissão ao`[{identity.name}]`quando definidas (caso contrário`[openclaw]`
Se o`messages.responsePrefix`estiver desligado. Defina- o explicitamente para personalizar ou desativar
o prefixo (use`""`para removê-lo).

### Dica de abastecimento de números

- ** Local eSIM** da operadora móvel do seu país (mais confiável)
- Áustria: [quente]https://www.hot.at
- Reino Unido: [giffgaff]https://www.giffgaff.com — SIM gratuito, sem contrato
- ** SIM pré-pago** - barato, só precisa de receber um SMS para verificação

**Evite:** TextNow, Google Voice, a maioria dos serviços de SMS gratuitos — WhatsApp bloqueia esses serviços agressivamente.

**Dica: ** O número só precisa receber um SMS de verificação. Depois disso, as sessões Web do WhatsApp persistem via`creds.json`.

## Por que não Twilio?

- Early OpenClaw constrói suporte Twilio WhatsApp Business integração.
- Os números do WhatsApp Business não são adequados para um assistente pessoal.
- Meta aplica uma janela de resposta de 24 horas; se você não respondeu nas últimas 24 horas, o número de negócio não pode iniciar novas mensagens.
- O uso de alto volume ou “chatty” desencadeia bloqueio agressivo, porque as contas de negócios não são destinadas a enviar dezenas de mensagens assistentes pessoais.
- Resultado: entrega não confiável e bloqueios frequentes, então o suporte foi removido.

## Login + credenciais

- Comando de login:`openclaw channels login`(QR via dispositivos ligados).
- Registo multicontas:`openclaw channels login --account <id>``<id>`=`accountId`.
- Conta padrão (quando`--account`é omitido):`default`se estiver presente, caso contrário, o primeiro id de conta configurado (sortido).
- Credenciais armazenados em`~/.openclaw/credentials/whatsapp/<accountId>/creds.json`.
- Cópia de backup no`creds.json.bak`(recuperado em corrupção).
- Compatibilidade Legacy: instalações antigas armazenadas Baileys arquivos diretamente em`~/.openclaw/credentials/`.
- Encerramento:`openclaw channels logout`(ou`openclaw channels login --account <id>`0) exclui WhatsApp auth state (mas mantém compartilhado`openclaw channels login --account <id>`1).
- O socket logged-out => erro instrui o re-link.

## Fluxo de entrada (DM + grupo)

- Os eventos WhatsApp vêm de`messages.upsert`(Bailes).
- Os ouvintes da caixa de entrada são desligados no desligamento para evitar acumular manipuladores de eventos em testes/reiniciações.
- Os chats de estado/transmissão são ignorados.
- Conversas diretas usam E.164; grupos usam grupo JID.
- ** Política de DM**:`channels.whatsapp.dmPolicy`controla o acesso direto ao chat (padrão:`pairing`.
- Emparelhamento: remetentes desconhecidos recebem um código de emparelhamento (aprovar via`openclaw pairing approve whatsapp <code>`; códigos expiram após 1 hora).
- Aberto: requer`channels.whatsapp.allowFrom`para incluir`"*"`.
- Seu número WhatsApp vinculado é implicitamente confiável, então as mensagens de si mesmos pulam as verificações do`channels.whatsapp.dmPolicy`e do`channels.whatsapp.allowFrom`.

## # Modo número pessoal (fallback)

Se você executar OpenClaw em seu número **pessoal WhatsApp**, habilite`channels.whatsapp.selfChatMode`(veja amostra acima).

Comportamento:

- DMs de saída nunca desencadeiam respostas de pareamento (preveni contatos de spam).
- Os remetentes desconhecidos continuam a seguir o`channels.whatsapp.dmPolicy`.
- Modo de auto-conversa (allowFrom inclui o seu número) evita auto ler recibos e ignora mencionar JIDs.
- Recibos de leitura enviados para DM não-auto-conversa.

## Ler recibos

Por padrão, o gateway marca as mensagens do WhatsApp como lidas (marcas azuis) uma vez que são aceitas.

Desactivar globalmente:

```json5
{
  channels: { whatsapp: { sendReadReceipts: false } },
}
```

Desactivar por conta:

```json5
{
  channels: {
    whatsapp: {
      accounts: {
        personal: { sendReadReceipts: false },
      },
    },
  },
}
```

Notas:

- O modo de auto-conversas ignora sempre os recibos.

## WhatsApp FAQ: envio de mensagens + emparelhamento

**Será que OpenClaw mensagem contatos aleatórios quando eu linkar WhatsApp?**
Não. A política padrão de DM é ** paring**, assim os remetentes desconhecidos só recebem um código de emparelhamento e sua mensagem é ** não processado**. OpenClaw apenas responde aos chats que recebe, ou para enviar você explicitamente gatilho (agente/CLI).

**Como o emparelhamento funciona no WhatsApp?**
Emparelhamento é um portão DM para remetentes desconhecidos:

- Primeiro DM de um novo remetente retorna um código curto (mensagem não é processada).
- Aprovar:`openclaw pairing approve whatsapp <code>`(lista`openclaw pairing list whatsapp`.
- Os códigos expiram após 1 hora; os pedidos pendentes são limitados em 3 por canal.

** Várias pessoas podem usar diferentes instâncias OpenClaw em um número WhatsApp?**
Sim, encaminhando cada remetente para um agente diferente via`bindings`(peer`kind: "dm"`, remetente E.164 como`+15551234567`. Respostas ainda vêm da mesma conta WhatsApp**, e bate-papos diretos colapsam na sessão principal de cada agente, então use **um agente por pessoa**. Controle de acesso DM `dmPolicy`/`allowFrom` é global por conta WhatsApp. Ver [Roteamento Multi-Agente] /concepts/multi-agent.

** Por que você pergunta pelo meu número de telefone no assistente?**
O assistente usa-o para definir o seu **allowlist/owner** para que os seus próprios DMs sejam permitidos. Não é usado para envio automático. Se você executar no seu número pessoal do WhatsApp, use esse mesmo número e habilite`channels.whatsapp.selfChatMode`.

## Normalização da mensagem (o que o modelo vê)

-`Body`é o corpo de mensagem atual com envelope.
- O contexto de resposta citado é ** sempre adicionado**:
  ```
  [Replying to +1555 id:ABC123]
  <quoted text or <media:...>>
  [/Replying]
  ```
- Responder metadados também definidos:
-`ReplyToId`= estrondo
-`ReplyToBody`= corpo ou suporte citado
-`ReplyToSender`= E.164 quando conhecido
- As mensagens de entrada somente de mídia usam espaços:
-`<media:image|video|audio|document|sticker>`

## Grupos

- Mapa de grupos para sessões`agent:<agentId>:whatsapp:group:<jid>`.
- Política de grupo:`channels.whatsapp.groupPolicy = open|disabled|allowlist`(padrão`allowlist`.
- Modos de ativação:
-`mention`(padrão): requer @mention ou regex match.
-`always`: Ativa sempre.
-`/activation mention|always`é apenas proprietário e deve ser enviado como uma mensagem independente.
- Proprietário =`channels.whatsapp.allowFrom`(ou auto E.164 se não definido).
- ** Injecção histórica** (somente para uso pendente):
- Mensagens  não processadas recentes (padrão 50) inseridas em:`[Chat messages since your last reply - for context]`(mensagens já na sessão não são reinjectadas)
- Mensagem actual em:`[Current message - respond to this]`- Sufixo do remetente anexado:`[from: Name (+E164)]`- Metadados de grupo em cache 5 min (sujeito + participantes).

## Resposta entrega (threading)

- WhatsApp Web envia mensagens padrão (sem discussão de resposta citada no gateway atual).
- As etiquetas de resposta são ignoradas neste canal.

## Reações de reconhecimento (reação automática na recepção)

WhatsApp pode enviar automaticamente reações emoji para mensagens recebidas imediatamente após o recebimento, antes que o bot gera uma resposta. Isso fornece feedback instantâneo aos usuários que sua mensagem foi recebida.

**Configuração:**

```json
{
  "whatsapp": {
    "ackReaction": {
      "emoji": "👀",
      "direct": true,
      "group": "mentions"
    }
  }
}
```

**Opções:**

-`emoji`(string): Emoji para ser usado para reconhecimento (por exemplo, "", "", "", "", "". Vazio ou omitido = recurso desativado.
-`direct`(booleano, padrão:`true`: Envie reações em chats diretos/DM.
-`group`(texto, padrão:`"mentions"`: Comportamento de chat em grupo:
-`"always"`: Reagir a todas as mensagens de grupo (mesmo sem @mention)
-`"mentions"`: Reagir apenas quando o bot é @ mencionado
-`"never"`: Nunca reagir em grupos

** Substituição por conta:**

```json
{
  "whatsapp": {
    "accounts": {
      "work": {
        "ackReaction": {
          "emoji": "✅",
          "direct": false,
          "group": "always"
        }
      }
    }
  }
}
```

** Notas de comportamento: **

- Reações são enviadas ** imediatamente** após o recebimento da mensagem, antes de digitar indicadores ou respostas bot.
- Em grupos com`requireMention: false`(ativação: sempre),`group: "mentions"`irá reagir a todas as mensagens (não apenas @mentions).
- Fogo-e-esquecer: falhas de reação são registradas, mas não impeça o bot de responder.
- Participante JID é automaticamente incluído para reações de grupo.
- WhatsApp ignora`messages.ackReaction`; use`channels.whatsapp.ackReaction`em vez disso.

## Ferramenta de agente (reacções)

- Ferramenta:`whatsapp`com acção`react``chatJid`,`messageId`,`emoji`, opcional`remove`.
- Opcional:`participant`(enviador do grupo),`fromMe`(reagindo à sua própria mensagem),`accountId`(multiconta).
- Semântica de remoção de reações: ver [/tools/reactions] /tools/reactions.
- Gating de ferramentas:`channels.whatsapp.actions.reactions`(padrão: habilitado).

## Limites

- O texto de saída é cortado para`channels.whatsapp.textChunkLimit`(padrão 4000).
- Opcional nova linha de blocos: definir`channels.whatsapp.chunkMode="newline"`para dividir em linhas em branco (limites de parágrafo) antes do comprimento de blocos.
- As economias de mídia de entrada são cobertas por`channels.whatsapp.mediaMaxMb`(padrão 50 MB).
- Itens de mídia de saída são tampados por`agents.defaults.mediaMaxMb`(padrão 5 MB).

## Enviar de saída (texto + mídia)

- Usa o ouvinte Web activo; erro se o gateway não estiver em execução.
- Bloco de texto: 4k máximo por mensagem (configurado via`channels.whatsapp.textChunkLimit`, opcional`channels.whatsapp.chunkMode`.
- Mídia:
- Imagem/vídeo/audio/documento suportado.
- Áudio enviado como PTT;`audio/ogg`=>`audio/ogg; codecs=opus`.
- Legenda apenas no primeiro artigo dos media.
- Media fetch suporta HTTP(S) e caminhos locais.
- GIFs animados: WhatsApp espera MP4 com`gifPlayback: true`para looping em linha.
- CLI:`openclaw message send --media <mp4> --gif-playback`- Gateway:`send`params incluem`gifPlayback: true`

## Notas de voz (audio PTT)

WhatsApp envia áudio como ** notas de voz** (bolha PTT).

- Melhores resultados: OGG/Opus. OpenClaw reescreve`audio/ogg`para`audio/ogg; codecs=opus`.
-`[[audio_as_voice]]`é ignorado para WhatsApp (áudio já envia como nota de voz).

## Limites de mídia + otimização

- Cap de saída padrão: 5 MB (por item de mídia).
- Substituição:`agents.defaults.mediaMaxMb`.
- As imagens são auto-otimizadas para JPEG sob cap (redimensionar + varredura de qualidade).
- Oversize media => erro; resposta mídia cai de volta ao aviso de texto.

## Batimentos cardíacos

- ** Batimento cardíaco de Gateway** logs connection health `web.heartbeatSeconds`, padrão 60s).
- ** O batimento cardíaco do agente** pode ser configurado por agente `agents.list[].heartbeat` ou globalmente
via`agents.defaults.heartbeat`(fallback quando não são definidas entradas por agente).
- Usa o prompt cardíaco configurado (por omissão:`Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.` +`HEARTBEAT_OK`skip behavior.
- Entrega padrão para o último canal usado (ou alvo configurado).

## Reconectar comportamento

- Política de reserva:`web.reconnect`:
-`initialMs`,`maxMs`,`factor`,`jitter`,`maxAttempts`.
- Se maxAttempts alcançado, paragens de monitoramento da web (degradado).
- Desligado => parar e exigir re-link.

## Configurar mapa rápido

-`channels.whatsapp.dmPolicy`(política da DM: emparelhamento/allowlist/aberto/desactivado).
-`channels.whatsapp.selfChatMode`(configuração do mesmo telefone; bot usa seu número pessoal do WhatsApp).
-`channels.whatsapp.allowFrom`(DM allowlist). WhatsApp usa números de telefone E.164 (sem nomes de usuário).
-`channels.whatsapp.mediaMaxMb`(inbound media save cap).
-`channels.whatsapp.ackReaction`(reacção automática aquando da recepção da mensagem:`{emoji, direct, group}`.
-`channels.whatsapp.accounts.<accountId>.*`(configurações por conta + opcional`authDir`.
-`channels.whatsapp.accounts.<accountId>.mediaMaxMb`(capa de suporte de entrada por conta).
-`channels.whatsapp.accounts.<accountId>.ackReaction`(por conta sobreposição de reacção).
-`channels.whatsapp.selfChatMode`0 (lista de remetentes do grupo).
-`channels.whatsapp.selfChatMode`1 (política dos grupos).
-`channels.whatsapp.selfChatMode`2 /`channels.whatsapp.selfChatMode`3 (contexto histórico do grupo;`channels.whatsapp.selfChatMode`4 desactiva).
-`channels.whatsapp.selfChatMode`5 (limite de histórico de DM em turnos do usuário).`channels.whatsapp.selfChatMode`6.
-`channels.whatsapp.selfChatMode`7 (lista de permissões do grupo + lista de citações de padrões; use`channels.whatsapp.selfChatMode`8 para permitir todos)
-`channels.whatsapp.selfChatMode`9 (portar as reacções da ferramenta WhatsApp).
-`channels.whatsapp.allowFrom`0 (ou`channels.whatsapp.allowFrom`1)
-`channels.whatsapp.allowFrom`2
-`channels.whatsapp.allowFrom`3 (prefixo de entrada; por conta:`channels.whatsapp.allowFrom`4; depreciado:`channels.whatsapp.allowFrom`5)
-`channels.whatsapp.allowFrom`6 (prefixo de saída)
-`channels.whatsapp.allowFrom`7
-`channels.whatsapp.allowFrom`8
-`channels.whatsapp.allowFrom`9 (sobreposição opcional)
-`channels.whatsapp.mediaMaxMb`0
-`channels.whatsapp.mediaMaxMb`1
-`channels.whatsapp.mediaMaxMb`2
-`channels.whatsapp.mediaMaxMb`3 (sobreposição por agente)
-`channels.whatsapp.mediaMaxMb`4 (escopo, ocioso, loja, mainKey)
-`channels.whatsapp.mediaMaxMb`5 (desactivar a inicialização do canal quando false)
-`channels.whatsapp.mediaMaxMb`6
-`channels.whatsapp.mediaMaxMb`7

## Logs + solução de problemas

- Subsistemas:`whatsapp/inbound`,`whatsapp/outbound`,`web-heartbeat`,`web-reconnect`.
- Arquivo de log:`/tmp/openclaw/openclaw-YYYY-MM-DD.log`(configurável).
- Guia de resolução de problemas:

## Solução de problemas (rápido)

** Não é necessário o login do QR

- Sintoma:`channels status`mostra`linked: false`ou avisa “Não ligado”.
- Corrigir: execute`openclaw channels login`no host do gateway e escaneie o QR (WhatsApp → Configurações → Dispositivos vinculados).

** Ligado, mas desconectado/reconectar loop**

- Sintoma:`channels status`mostra`running, disconnected`ou avisa “Linkado mas desconectado”.
- Corrigir:`openclaw doctor`(ou reiniciar o gateway). Se persistir, volte a ligar-se através do`channels login`e inspeccione o`openclaw logs --follow`.

**Bun runtime**

- Bun é **não recomendado**. WhatsApp (Baileys) e Telegram não são confiáveis em Bun.
Execute o gateway com **Node**. (Veja Começando nota de execução.)
