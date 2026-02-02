---
summary: "Behavior and config for WhatsApp group message handling (mentionPatterns are shared across surfaces)"
read_when:
  - Changing group message rules or mentions
---

# Mensagens de grupo (canal web WhatsApp)

Objetivo: deixe Clawd sentar-se em grupos WhatsApp, acordar apenas quando pinged, e manter esse tópico separado da sessão pessoal DM.

Nota:`agents.list[].groupChat.mentionPatterns`agora é usado pelo Telegram/Discord/Slack/iMessage também; este documento foca no comportamento específico do WhatsApp. Para configurações multi-agentes, defina`agents.list[].groupChat.mentionPatterns`por agente (ou use`messages.groupChat.mentionPatterns`como um recurso global).

## O que é implementado (2025-12-03)

- Modos de activação:`mention`(padrão) ou`always`.`mention`requer um ping (verdadeiro WhatsApp @-menções via`mentionedJids`, padrões de regex, ou E.164 do bot em qualquer lugar do texto).`always`desperta o agente em cada mensagem, mas ele deve responder apenas quando ele pode adicionar valor significativo; caso contrário, ele retorna o símbolo silencioso`NO_REPLY`. Os padrões podem ser configurados na configuração `channels.whatsapp.groups` e substituídos por grupo via`/activation`. Quando o`channels.whatsapp.groups`é definido, ele também atua como uma lista de allowable grupo (incluir`"*"`para permitir todos).
- Política de grupo:`always`0 controla se as mensagens de grupo são aceites `always`1).`always`2 utiliza o`always`3 (fallback: OCTXCODE) O padrão é`always`5 (bloqueado até adicionar remetentes).
- Sessões por grupo: as teclas de sessão parecem`always`6, portanto comandos como`always`7 ou`always`8 (enviados como mensagens autônomas) são explorados para esse grupo; o estado pessoal do DM é intocado. Batimentos cardíacos são ignorados para threads de grupo.
- Injecção de contexto: ** mensagens de grupo apenas para uso pendente** (padrão 50) que  did not  desencadeou uma execução são prefixadas sob`always`9, com a linha de disparo sob`mention`0. As mensagens já na sessão não são reinjetadas.
- Sender surfacing: cada grupo agora termina com`mention`1 para que Pi saiba quem está falando.
- Ephemeral/view-once: nós desembrulhamos aqueles antes de extrair texto/mencias, então pings dentro deles ainda disparam.
- Prompt de sistema de grupo: na primeira volta de uma sessão de grupo (e sempre que o`mention`2 muda o modo) injetamos um curto borrão no prompt de sistema como o`mention`3 Se os metadados não estiverem disponíveis, ainda dizemos ao agente que é uma conversa de grupo.

## Exemplo de configuração (WhatsApp)

Adicione um bloco`groupChat`ao`~/.openclaw/openclaw.json`para que pings de nome de exibição funcionem mesmo quando WhatsApp tira o`@`visual no corpo de texto:

```json5
{
  channels: {
    whatsapp: {
      groups: {
        "*": { requireMention: true },
      },
    },
  },
  agents: {
    list: [
      {
        id: "main",
        groupChat: {
          historyLimit: 50,
          mentionPatterns: ["@?openclaw", "\\+?15555550123"],
        },
      },
    ],
  },
}
```

Notas:

- Os regexes são insensíveis; eles cobrem um ping de nome de exibição como`@openclaw`e o número bruto com ou sem`+`/espaços.
- WhatsApp ainda envia menções canônicas via`mentionedJids`quando alguém toca no contato, então o número de retorno raramente é necessário, mas é uma rede de segurança útil.

## # Comando de ativação (somente proprietário)

Usar o comando de chat do grupo:

-`/activation mention`-`/activation always`

Apenas o número de proprietário (do`channels.whatsapp.allowFrom`, ou o próprio E.164 do bot quando não definido) pode alterar isso. Enviar`/status`como uma mensagem autônoma no grupo para ver o modo de ativação atual.

## Como usar

1. Adicione a sua conta WhatsApp (a única que executa OpenClaw) ao grupo.
2. Diga`@openclaw …`(ou inclua o número). Apenas os remetentes autorizados podem atirá-lo a menos que você defina`groupPolicy: "open"`.
3. O prompt do agente incluirá contexto recente do grupo mais o marcador`[from: …]`que segue assim que possa dirigir-se à pessoa certa.
4. As directivas ao nível das sessões `/verbose on`,`/think high`,`/new`ou`/reset`,`/compact` aplicam-se apenas à sessão desse grupo; enviam-nas como mensagens autónomas para que se registem. A sua sessão pessoal de DM continua independente.

## Teste / verificação

- Fumaça manual:
- Enviar um`@openclaw`ping no grupo e confirmar uma resposta que faz referência ao nome do remetente.
- Envie um segundo ping e verifique se o bloco de histórico está incluído e então limpo no próximo turno.
- Verificar os registos dos gateways (correr com`--verbose` para ver as entradas`inbound web message`que mostram o`from: <groupJid>`e o sufixo`[from: …]`.

## Considerações conhecidas

- Os batimentos cardíacos são intencionalmente ignorados para grupos para evitar transmissões ruidosas.
- Supressão de eco usa a string de lote combinado; se você enviar texto idêntico duas vezes sem menções, apenas o primeiro receberá uma resposta.
- Entradas de armazenamento de sessão aparecerão como`agent:<agentId>:whatsapp:group:<jid>`na loja de sessão `~/.openclaw/agents/<agentId>/sessions/sessions.json`por padrão); uma entrada em falta apenas significa que o grupo ainda não acionou uma execução.
- Os indicadores de tipo nos grupos seguem o`agents.defaults.typingMode`(por omissão:`message`quando não mencionados).
