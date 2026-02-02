---
summary: "Behavior and config for WhatsApp group message handling (mentionPatterns are shared across surfaces)"
read_when:
  - Changing group message rules or mentions
---

# Mensagens de grupo (canal web WhatsApp)

Objetivo: deixe Clawd sentar-se em grupos WhatsApp, acordar apenas quando pinged, e manter esse tópico separado da sessão pessoal DM.

Nota: <<CODE0>> agora é usado pelo Telegram/Discord/Slack/iMessage também; este documento foca no comportamento específico do WhatsApp. Para configurações multi-agentes, definir <<CODE1>> por agente (ou usar <<CODE2>>> como um retorno global).

# # O que é implementado (2025-12-03)

- Modos de ativação: <<CODE0>> (default) ou <<CODE1>>>. <<CODE2>> requer um ping (verdadeiro WhatsApp @-menções via <<CODE3>>, padrões de regex, ou E.164 do bot em qualquer lugar do texto). <<CODE4> acorda o agente em cada mensagem, mas ele deve responder apenas quando ele pode adicionar valor significativo; caso contrário ele retorna o token silencioso <<CODE5>>. Os padrões podem ser definidos na configuração (<<<CODE6>>>) e substituídos por grupo via <<CODE7>>. Quando <<CODE8> é definido, ele também atua como uma lista de allowlist de grupo (incluir <<CODE9>> para permitir todos).
- Política de grupo: <<CODE10>> controla se as mensagens de grupo são aceites (<<CODE11>>>). <<CODE12>> usa <<CODE13>> (fallback: explícito <<CODE14>>). O padrão é <<CODE15>>> (bloqueado até adicionar remetentes).
- Sessões por grupo: as teclas de sessão se parecem com <<CODE16> assim comandos como <<CODE17>> ou <<CODE18>> (enviadas como mensagens autônomas) são explorados para esse grupo; o estado pessoal do DM é intocado. Batimentos cardíacos são ignorados para threads de grupo.
- Injecção de contexto: ** mensagens de grupo ** apenas-pendentes (padrão 50) que  não  desencadearam uma execução são prefixadas em <<CODE19>>, com a linha de disparo em <<CODE20>>. As mensagens já na sessão não são reinjetadas.
- Sender surfacing: cada grupo agora termina com <<CODE21> para que Pi saiba quem está falando.
- Ephemeral/view-once: nós desembrulhamos aqueles antes de extrair texto/mencias, então pings dentro deles ainda disparam.
- Prompt de sistema de grupo: na primeira volta de uma sessão de grupo (e sempre que <<CODE22> altera o modo) injetamos um borrão curto no prompt de sistema como <<CODE23>>> Se os metadados não estiverem disponíveis, ainda dizemos ao agente que é um chat em grupo.

# # Exemplo de configuração (WhatsApp)

Adicione um bloco <<CODE0>> para <<CODE1> assim os pings de nome de exibição funcionam mesmo quando WhatsApp tira o visual <<CODE2> no corpo de texto:

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

- Os regexes são insensíveis a casos; cobrem um ping de nome de exibição como <<CODE0>> e o número bruto com ou sem <<CODE1>/espaços.
- WhatsApp ainda envia menções canônicas via <<CODE2>> quando alguém toca no contato, então o retorno de número raramente é necessário, mas é uma rede de segurança útil.

## # Comando de ativação (somente proprietário)

Usar o comando de chat do grupo:

- <<CODE0>>
- <<CODE1>>

Somente o número de proprietário (de <<CODE0>>, ou o próprio E.164 do bot quando não definido) pode alterar isso. Enviar <<CODE1>> como uma mensagem autônoma no grupo para ver o modo de ativação atual.

# # Como usar

1. Adicione a sua conta WhatsApp (a única que executa OpenClaw) ao grupo.
2. Diga <<CODE0>> (ou inclua o número). Apenas os remetentes autorizados podem atirá-lo a menos que você defina <<CODE1>>.
3. O prompt do agente incluirá o contexto recente do grupo mais o marcador de rastreamento <<CODE2> para que possa dirigir-se à pessoa certa.
4. Directrizes de nível de sessão (<<<CODE3>>, <<CODE4>>, <<CODE5>> ou <<CODE6>>, <<CODE7>>) aplicam-se apenas à sessão desse grupo; enviam-nas como mensagens autónomas para que se registem. A sua sessão pessoal de DM continua independente.

# # Teste / verificação

- Fumaça manual:
- Envie um ping <<CODE0>> no grupo e confirme uma resposta que faça referência ao nome do remetente.
- Envie um segundo ping e verifique se o bloco de histórico está incluído e então limpo no próximo turno.
- Verificar logs de gateway (correr com <<CODE1>>) para ver <<CODE2>> entradas mostrando <<CODE3>>> e o sufixo <<CODE4>>>.

# # Considerações conhecidas

- Os batimentos cardíacos são intencionalmente ignorados para grupos para evitar transmissões ruidosas.
- Supressão de eco usa a string de lote combinado; se você enviar texto idêntico duas vezes sem menções, apenas o primeiro receberá uma resposta.
- Entradas de armazenamento de sessão aparecerão como <<CODE0>> na loja de sessão (<<CODE1>> por padrão); uma entrada em falta apenas significa que o grupo ainda não acionou uma execução.
- Os indicadores de digitação dos grupos seguem <<CODE2>> (padrão: <<CODE3>> quando não mencionados).
