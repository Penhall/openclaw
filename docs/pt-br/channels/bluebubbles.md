---
summary: "iMessage via BlueBubbles macOS server (REST send/receive, typing, reactions, pairing, advanced actions)."
read_when:
  - Setting up BlueBubbles channel
  - Troubleshooting webhook pairing
  - Configuring iMessage on macOS
---

# BlueBubbles (macOS REST)

Status: plugin empacotado que fala com o servidor macOS BlueBubbles sobre HTTP. **Recomendado para integração iMessage** devido à sua API mais rica e configuração mais fácil em comparação com o legado do canal imsg.

## Visão geral

- Funciona no macOS através da aplicação auxiliar BlueBubbles ([bluebubbles.app]https://bluebubbles.app.
- Recomendado/testado: macOS Sequoia (15). macOS Tahoe (26) funciona; a edição está atualmente quebrada no Tahoe, e atualizações de ícones de grupo podem relatar sucesso, mas não sincronização.
- OpenClaw fala com ele através de sua API REST `GET /api/v1/ping`,`POST /message/text`,`POST /chat/:id/*`.
- As mensagens recebidas chegam através de webhooks; respostas de saída, indicadores de digitação, recibos de leitura e tapbacks são chamadas REST.
- Os acessórios e adesivos são ingeridos como meios de entrada (e aparecidos ao agente quando possível).
- Emparelhamento/allowlist funciona da mesma forma que outros canais `/start/pairing`etc.) com códigos`channels.bluebubbles.allowFrom`+ emparelhamento.
- As reações são surrounded como eventos do sistema tal como Slack/Telegram assim que os agentes podem "mention"-los antes de responder.
- Recursos avançados: editar, não enviar, responder threading, efeitos de mensagem, gestão de grupo.

## Começo rápido

1. Instale o servidor BlueBubbles no seu Mac (siga as instruções em [bluebubbles.app/install]https://bluebubbles.app/install.
2. Na configuração BlueBubbles, habilite a API web e defina uma senha.
3. Executar`openclaw onboard`e selecione BlueBubbles, ou configurar manualmente:
   ```json5
   {
     channels: {
       bluebubbles: {
         enabled: true,
         serverUrl: "http://192.168.1.100:1234",
         password: "example-password",
         webhookPath: "/bluebubbles-webhook",
       },
     },
   }
   ```
4. Ponto BlueBubbles webhooks para o seu gateway (exemplo:`https://your-gateway-host:3000/bluebubbles-webhook?password=<password>`.
5. Inicie o gateway; ele irá registrar o manipulador webhook e começar a emparelhar.

## Onboarding

BlueBubbles está disponível no assistente de configuração interativo:

```
openclaw onboard
```

O assistente pede:

- ** URL do servidor** (obrigatório): Endereço do servidor BlueBubbles (por exemplo,`http://192.168.1.100:1234`
- ** Password** (obrigatório): senha da API das configurações do BlueBubbles Server
- **Webhook path** (opcional): Predefinições para`/bluebubbles-webhook`- ** Política de DM**: emparelhamento, allowlist, aberto ou desativado
- **Permitir lista**: Números de telefone, e-mails ou alvos de chat

Você também pode adicionar BlueBubbles via CLI:

```
openclaw channels add bluebubbles --http-url http://192.168.1.100:1234 --password <password>
```

## Controle de acesso (DMs + grupos)

DM:

- Predefinição:`channels.bluebubbles.dmPolicy = "pairing"`.
- Os remetentes desconhecidos recebem um código de pareamento; as mensagens são ignoradas até serem aprovadas (os códigos expiram após 1 hora).
- Aprovar via:
-`openclaw pairing list bluebubbles`-`openclaw pairing approve bluebubbles <CODE>`- Emparelhamento é a troca padrão. Detalhes: [Pairing] /start/pairing

Grupos:

-`channels.bluebubbles.groupPolicy = open | allowlist | disabled`(por omissão:`allowlist`.
- Controlos`channels.bluebubbles.groupAllowFrom`que podem desencadear em grupos quando o`allowlist`é definido.

## # Mencionar gating (grupos)

BlueBubbles suporta o gating de menção para chats em grupo, combinando o comportamento do iMessage/WhatsApp:

- Utiliza`agents.list[].groupChat.mentionPatterns`(ou`messages.groupChat.mentionPatterns` para detectar menções.
- Quando o`requireMention`está habilitado para um grupo, o agente só responde quando mencionado.
- Comandos de controle de remetentes autorizados.

Configuração por grupo:

```json5
{
  channels: {
    bluebubbles: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15555550123"],
      groups: {
        "*": { requireMention: true }, // default for all groups
        "iMessage;-;chat123": { requireMention: false }, // override for specific group
      },
    },
  },
}
```

## Command gating

- Os comandos de controlo (por exemplo,`/config`,`/model` requerem autorização.
- Usa`allowFrom`e`groupAllowFrom`para determinar a autorização de comando.
- Os remetentes autorizados podem executar comandos de controle mesmo sem mencionar em grupos.

## Datilografia + recibos de leitura

- ** Indicadores de tipagem**: Enviado automaticamente antes e durante a geração de resposta.
- **Receitas de leitura**: Controladas pelo`channels.bluebubbles.sendReadReceipts`(padrão:`true`.
- ** Indicadores de tipagem**: OpenClaw envia digitando eventos de início; BlueBubbles limpa digitando automaticamente em envio ou tempo limite (parada manual via DELETE não é confiável).

```json5
{
  channels: {
    bluebubbles: {
      sendReadReceipts: false, // disable read receipts
    },
  },
}
```

## Acções avançadas

BlueBubbles suporta ações avançadas de mensagens quando habilitado na configuração:

```json5
{
  channels: {
    bluebubbles: {
      actions: {
        reactions: true, // tapbacks (default: true)
        edit: true, // edit sent messages (macOS 13+, broken on macOS 26 Tahoe)
        unsend: true, // unsend messages (macOS 13+)
        reply: true, // reply threading by message GUID
        sendWithEffect: true, // message effects (slam, loud, etc.)
        renameGroup: true, // rename group chats
        setGroupIcon: true, // set group chat icon/photo (flaky on macOS 26 Tahoe)
        addParticipant: true, // add participants to groups
        removeParticipant: true, // remove participants from groups
        leaveGroup: true, // leave group chats
        sendAttachment: true, // send attachments/media
      },
    },
  },
}
```

Acções disponíveis:

- ** reacção**: Adicionar/remover reações de tapback `messageId`,`emoji`,`remove`
- **edit**: Editar uma mensagem enviada `messageId`,`text`
- ** unsend**: Não enviar uma mensagem `messageId`
- **Resposta**: Resposta a uma mensagem específica `messageId`,`text`,`to`
- **Enviar com efeito**: Enviar com efeito iMessage `text`,`emoji`0,`emoji`1)
- **RenameGroup**: Renomear uma conversa de grupo `emoji`2,`emoji`3)
- **setGroupIcon**: Defina o ícone/foto de um bate-papo de grupo `emoji`4,`emoji`5) — flácido no macOS 26 Tahoe (API pode retornar o sucesso, mas o ícone não sincroniza).
- ** AddParticipante**: Adicionar alguém a um grupo `emoji`6,`emoji`7)
- **removerParticipante**: Remova alguém de um grupo `emoji`8,`emoji`9)
- **leaveGroup**: Deixe uma conversa em grupo `remove`0)
- **Enviar anexo**: Enviar meios/arquivos `remove`1,`remove`2,`remove`3,`remove`4)
- Memos de voz: definir`remove`5 com **MP3** ou **CAF** áudio para enviar como uma mensagem de voz iMessage. BlueBubbles converte MP3 → CAF ao enviar memorandos de voz.

IDs de mensagens (curto vs cheio)

OpenClaw pode aparecer  curto  IDs de mensagem (por exemplo,`1`,`2` para salvar fichas.

-`MessageSid`/`ReplyToId`podem ser IDs curtos.
-`MessageSidFull`/`ReplyToIdFull`contém os identificadores completos do fornecedor.
- IDs curtos são na memória; eles podem expirar ao reiniciar ou despejo de cache.
- As ações aceitam`messageId`curto ou completo, mas IDs curtos errarão se não estiverem mais disponíveis.

Use IDs completos para automação e armazenamento duradouros:

- Modelos:`{{MessageSidFull}}`,`{{ReplyToIdFull}}`- Contexto:`MessageSidFull`/`ReplyToIdFull`em cargas úteis de entrada

Ver [Configuração]/gateway/configuration para as variáveis do modelo.

## Block streaming

Controlar se as respostas são enviadas como uma única mensagem ou transmitidas em blocos:

```json5
{
  channels: {
    bluebubbles: {
      blockStreaming: true, // enable block streaming (default behavior)
    },
  },
}
```

## Mídia + limites

- Os anexos de entrada são baixados e armazenados no cache de mídia.
- Tampa de mídia via`channels.bluebubbles.mediaMaxMb`(padrão: 8 MB).
- O texto de saída é cortado para`channels.bluebubbles.textChunkLimit`(padrão: 4000 caracteres).

## Referência de configuração

Configuração completa: [Configuração]/gateway/configuration

Opções do fornecedor:

-`channels.bluebubbles.enabled`: Activar/desactivar o canal.
-`channels.bluebubbles.serverUrl`: BlueBubbles REST API URL base.
-`channels.bluebubbles.password`: senha da API.
-`channels.bluebubbles.webhookPath`: Caminho do ponto final do Webhook (padrão:`/bluebubbles-webhook`.
-`channels.bluebubbles.dmPolicy`:`pairing | allowlist | open | disabled`(por omissão:`pairing`.
-`channels.bluebubbles.allowFrom`: Lista de autorizações de DM (handles, emails, números E.164,`chat_id:*`,`channels.bluebubbles.serverUrl`0).
-`channels.bluebubbles.serverUrl`1:`channels.bluebubbles.serverUrl`2 (por omissão:`channels.bluebubbles.serverUrl`3).
-`channels.bluebubbles.serverUrl`4: Lista de remetentes de grupo.
-`channels.bluebubbles.serverUrl`5: Configuração por grupo `channels.bluebubbles.serverUrl`6, etc.).
-`channels.bluebubbles.serverUrl`7: Enviar recibos de leitura (por omissão:`channels.bluebubbles.serverUrl`8).
-`channels.bluebubbles.serverUrl`9: Activar a transmissão de blocos (por omissão:`channels.bluebubbles.password`0).
-`channels.bluebubbles.password`1: Tamanho do pedaço de saída em caracteres (padrão: 4000).
-`channels.bluebubbles.password`2:`channels.bluebubbles.password`3 (por omissão) divide-se apenas quando excede o`channels.bluebubbles.password`4;`channels.bluebubbles.password`5 divide-se em linhas em branco (limites de parágrafos) antes de se cortar o comprimento.
-`channels.bluebubbles.password`6: Tampa de mídia de entrada em MB (padrão: 8).
-`channels.bluebubbles.password`7: Máx mensagens de grupo para o contexto (0 desactiva).
-`channels.bluebubbles.password`8: Limite de história do DM.
-`channels.bluebubbles.password`9: Activar/desactivar acções específicas.
-`channels.bluebubbles.webhookPath`0: Configuração multi-conta.

Opções globais relacionadas:

-`agents.list[].groupChat.mentionPatterns`(ou`messages.groupChat.mentionPatterns`.
-`messages.responsePrefix`.

## Endereçamento / alvos de entrega

Preferir`chat_guid`para roteamento estável:

-`chat_guid:iMessage;-;+15555550123`(preferidos para grupos)
-`chat_id:123`-`chat_identifier:...`- pegas directas:`+15555550123`,`user@example.com`- Se um punho direto não tem um bate-papo DM existente, OpenClaw irá criar um via`POST /api/v1/chat/new`. Isto requer que a API privada BlueBubbles seja ativada.

## Segurança

- Os pedidos do Webhook são autenticados comparando o`guid`/`password`consulta params ou cabeçalhos contra`channels.bluebubbles.password`. São também aceites pedidos do`localhost`.
- Mantenha a senha API e webhook endpoint secreto (trate-os como credenciais).
- Confiança localhost significa que um proxy reverso do mesmo host pode ignorar involuntariamente a senha. Se você proxy do gateway, requeira autenticação no proxy e configure`gateway.trustedProxies`. Ver [Segurança do portal] /gateway/security#reverse-proxy-configuration.
- Habilite as regras de firewall HTTPS + no servidor BlueBubbles se expô-lo fora da sua LAN.

## Resolução de problemas

- Se a digitação / leitura de eventos parar de funcionar, verifique os registros webhook BlueBubbles e verifique se o caminho do gateway corresponde`channels.bluebubbles.webhookPath`.
- Os códigos de pareamento expiram após uma hora; use`openclaw pairing list bluebubbles`e`openclaw pairing approve bluebubbles <code>`.
- As reações requerem a API privada BlueBubbles `POST /api/v1/message/react`; garantir que a versão do servidor a exponha.
- Editar/desenviar requer macOS 13+ e uma versão compatível do servidor BlueBubbles. No macOS 26 (Tahoe), a edição está atualmente quebrada devido a alterações na API privada.
- Atualizações de ícones de grupo podem ser flácidas no macOS 26 (Tahoe): a API pode retornar o sucesso, mas o novo ícone não sincroniza.
- OpenClaw auto-esconde ações conhecidas-quebradas com base na versão macOS do servidor BlueBubbles. Se a edição ainda aparecer no macOS 26 (Tahoe), desative-o manualmente com`channels.bluebubbles.actions.edit=false`.
- Para informações relativas ao estatuto/saúde:`openclaw status --all`ou`openclaw status --deep`.

Para referência geral do fluxo de trabalho do canal, consulte [Canais] /channels e o guia [Plugins] /plugins.
