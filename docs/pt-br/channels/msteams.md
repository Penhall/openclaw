---
summary: "Microsoft Teams bot support status, capabilities, and configuration"
read_when:
  - Working on MS Teams channel features
---

# Microsoft Teams (plugin)

> "Abandonai toda a esperança, vós que entrais aqui."

Atualizado em: 2026-01-21

Status: são suportados anexos texto + DM; o envio de arquivos canal / grupo requer permissões`sharePointSiteId`+ Gráfico (veja [Enviar arquivos em chats de grupo] #sending-files-in-group-chats. As sondagens são enviadas através de cartões adaptativos.

## Plugin necessário

Microsoft Equipes envia como um plugin e não é empacotado com o núcleo instalar.

**Mudança de ruptura (2026.1.15):** EM As equipas saíram do núcleo. Se você usá-lo, você deve instalar o plugin.

Explicable: mantém o núcleo instala mais leve e permite que as dependências do MS Teams se atualizem independentemente.

Instalar via CLI (registro npm):

```bash
openclaw plugins install @openclaw/msteams
```

Obtenção local (quando em execução a partir de um git repo):

```bash
openclaw plugins install ./extensions/msteams
```

Se você escolher Equipes durante a configuração/onboarding e um git checkout for detectado,
OpenClaw irá oferecer o caminho de instalação local automaticamente.

Detalhes: [Plugins]/plugin

## Montagem rápida (início)

1. Instale o plugin Microsoft Teams.
2. Criar um **Azure Bot** (ID App + cliente secreto + locatário ID).
3. Configure Openclaw com essas credenciais.
4. Expor`/api/messages`(porto 3978 por padrão) através de uma URL pública ou túnel.
5. Instale o pacote de aplicativos Teams e inicie o gateway.

Configuração mínima:

```json5
{
  channels: {
    msteams: {
      enabled: true,
      appId: "<APP_ID>",
      appPassword: "<APP_PASSWORD>",
      tenantId: "<TENANT_ID>",
      webhook: { port: 3978, path: "/api/messages" },
    },
  },
}
```

Nota: chats de grupo são bloqueados por padrão `channels.msteams.groupPolicy: "allowlist"`. Para permitir respostas de grupo, defina`channels.msteams.groupAllowFrom`(ou use`groupPolicy: "open"`para permitir que qualquer membro, mencionado-aberto).

## Objetivos

- Fale com OpenClaw através de equipes DMs, chats de grupo ou canais.
- Mantenha roteamento determinístico: respostas sempre voltar para o canal em que eles chegaram.
- Comportamento seguro do canal (menções necessárias, salvo configuração em contrário).

## A configuração escreve

Por padrão, o Microsoft Teams pode escrever atualizações de configuração acionadas pelo`/config set|unset`(requer`commands.config: true`.

Desactivar com:

```json5
{
  channels: { msteams: { configWrites: false } },
}
```

## Controle de acesso (DMs + grupos)

** Acesso ao DM**

- Predefinição:`channels.msteams.dmPolicy = "pairing"`. Os remetentes desconhecidos são ignorados até serem aprovados.
-`channels.msteams.allowFrom`aceita IDs de objetos AAD, UPNs ou nomes de exibição. O assistente resolve nomes para IDs via Microsoft Graph quando credenciais permitem.

** Acesso em grupo**

- Padrão:`channels.msteams.groupPolicy = "allowlist"`(bloqueado a menos que você adicione`groupAllowFrom`. Use`channels.defaults.groupPolicy`para substituir o padrão quando desativado.
-`channels.msteams.groupAllowFrom`controles que remetentes podem disparar em chats de grupo / canais (cai de volta para`channels.msteams.allowFrom`.
- Definir`groupPolicy: "open"`para permitir qualquer membro (ainda mencionado por padrão).
- Para permitir ** nenhum canal**, definir`channels.msteams.groupPolicy: "disabled"`.

Exemplo:

```json5
{
  channels: {
    msteams: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["user@org.com"],
    },
  },
}
```

**Teams + canal allowlist**

- Respostas de grupo/canal, listando equipas e canais no âmbito do`channels.msteams.teams`.
- Chaves podem ser IDs de equipe ou nomes; chaves de canal podem ser IDs de conversação ou nomes.
- Quando o`groupPolicy="allowlist"`e uma lista de allowlists de equipas estão presentes, apenas equipas/canais listados são aceites (period-gated).
- O assistente de configuração aceita entradas`Team/Channel`e armazena-as para você.
- No arranque, o OpenClaw resolve os nomes da equipa/canal e da lista de utilizadores para IDs (quando as permissões do gráfico permitem)
e registra o mapeamento; entradas não resolvidas são mantidas como digitadas.

Exemplo:

```json5
{
  channels: {
    msteams: {
      groupPolicy: "allowlist",
      teams: {
        "My Team": {
          channels: {
            General: { requireMention: true },
          },
        },
      },
    },
  },
}
```

## Como funciona

1. Instale o plugin Microsoft Teams.
2. Criar um **Azure Bot** (ID aplicativo + secreto + locatário ID).
3. Crie um pacote de aplicativos **Teams** que referencia o bot e inclui as permissões RSC abaixo.
4. Envie/instale o aplicativo Equipes em uma equipe (ou espaço pessoal para DMs).
5. Configure`msteams`em`~/.openclaw/openclaw.json`(ou env vars) e inicie o gateway.
6. O gateway escuta para o tráfego webhook Bot Framework no`/api/messages`por padrão.

## Configuração do Bot Azure (Prerequisitos)

Antes de configurar o OpenClaw, você precisa criar um recurso Azure Bot.

Passo 1: Criar o Bot Azure

1. Vá para [Criar Bot Azure] https://portal.azure.com/#create/Microsoft.AzureBot
2. Preencha a aba **Basics**:

- Campo - Valor
------------------ ---------------------------------------------------------------------------------------
O seu nome de bot, por exemplo,`openclaw-msteams`(deve ser único)
Seleciona a tua subscrição do Azure
** **Grupo de recursos ** ** Criar novo ou usar existente .
Lista de prioridades** Lista de prioridades** Lista de prioridades
Tipo de aplicação ** ** ** **
** ** Tipo de criação** ** ** Criar novo ID do aplicativo da Microsoft**

> ** Aviso de depreciação:** A criação de novos bots multi-doentes foi desactualizada após 2025-07-31. Use ** Single Tenant** para novos bots.

3. Clique em **Revisão + criação** → **Criar** (espera ~1-2 minutos)

Passo 2: Obter credenciais

1. Vá para o seu recurso Azure Bot → **Configuração**
2. Cópia **Microsoft App ID** → este é o seu`appId`3. Clique em **Manage Password** → ir para o Registro do aplicativo
4. Em **Certificados e segredos** → **Novo segredo do cliente** → copiar o **Value** → este é o seu`appPassword`5. Vá para **Overview** → cópia **Directório (doente) ID** → este é o seu`tenantId`

Passo 3: Configurar o Endpoint de Mensagens

1. Em Azure Bot → **Configuração**
2. Definir **Endpoint de mensagem** para o seu URL webhook:
- Produção:`https://your-domain.com/api/messages`- Dev local: Use um túnel (ver [Desenvolvimento Local] #local-development-tunneling abaixo)

Passo 4: Habilitar canal de equipes

1. Em Azure Bot → ** Canais**
2. Clique em **Microsoft Teams** → Configurar → Salvar
3. Aceite os Termos de Serviço

## Desenvolvimento Local (Tunneling)

As equipas não conseguem chegar ao`localhost`. Usar um túnel para o desenvolvimento local:

** Opção A: ngrok**

```bash
ngrok http 3978
# Copy the https URL, e.g., https://abc123.ngrok.io
# Set messaging endpoint to: https://abc123.ngrok.io/api/messages
```

**Opção B: Funil de cauda

```bash
tailscale funnel 3978
# Use your Tailscale funnel URL as the messaging endpoint
```

## Portal de Desenvolvedores de Equipas (Alternativo)

Em vez de criar manualmente um ZIP manifesto, você pode usar o [Teams Developer Portal]https://dev.teams.microsoft.com/apps:

1. Clique em **+ Nova aplicação**
2. Preencha informações básicas (nome, descrição, informações do desenvolvedor)
3. Vá para ** Características do aplicativo** → ** Bot**
4. Selecione **Enter um bot ID manualmente** e colar seu Azure Bot App ID
5. Verifique escopos: **Personal**, **Team**, **Group Chat**
6. Clique em **Distribuir** → **Download app package**
7. Em Equipes: **Apps** → **Manage your apps** → **Upload a custom app** → select the ZIP

Isto é muitas vezes mais fácil do que os manifestos da JSON.

## Testando o Bot

**Opção A: Azure Web Chat (verificar webhook primeiro)**

1. Em Azure Portal → seu recurso Azure Bot → **Teste em Web Chat**
2. Enviar uma mensagem - você deve ver uma resposta
3. Isto confirma seu endpoint webhook funciona antes da configuração das equipes

**Opção B: Equipes (depois da instalação do aplicativo)**

1. Instale o aplicativo Teams (sideload ou catálogo org)
2. Encontre o bot em Equipes e envie um DM
3. Verifique os logs de gateway para a atividade de entrada

## Configuração (somente texto mínimo)

1. **Instalar o plugin Microsoft Teams**
- A partir de npm:`openclaw plugins install @openclaw/msteams`- De um checkout local:`openclaw plugins install ./extensions/msteams`

2. **Inscrição do bot**
- Criar um Bot Azure (veja acima) e nota:
- ID da aplicação
- Segredo do cliente (senha do aplicativo)
- ID do inquilino (doador único)

3. ** Manifesto do aplicativo Teams**
- Incluir uma entrada`bot`com`botId = <App ID>`.
- Âmbito de aplicação:`personal`,`team`,`groupChat`.
-`supportsFiles: true`(necessário para manipulação de arquivos de escopo pessoal).
- Adicione permissões RSC (abaixo).
- Criar ícones:`outline.png`(32x32) e`color.png`(192x192).
- Junta os três ficheiros:`manifest.json`,`outline.png`,`botId = <App ID>`0.

4. **Configurar OpenClaw**

   ```json
   {
     "msteams": {
       "enabled": true,
       "appId": "<APP_ID>",
       "appPassword": "<APP_PASSWORD>",
       "tenantId": "<TENANT_ID>",
       "webhook": { "port": 3978, "path": "/api/messages" }
     }
   }
   ```

Você também pode usar variáveis de ambiente em vez de chaves de configuração:
-`MSTEAMS_APP_ID`-`MSTEAMS_APP_PASSWORD`-`MSTEAMS_TENANT_ID`

5. ** Endpoint da bot **
- Defina o Ponto Final de Mensagens do Bot Azure para:
-`https://<host>:3978/api/messages`(ou o seu caminho/porto escolhido).

6. **Execute o portal**
- O canal Teams começa automaticamente quando o plugin está instalado e a configuração`msteams`existe com credenciais.

## Contexto histórico

-`channels.msteams.historyLimit`controla quantas mensagens de canal/grupo recentes estão envolvidas no prompt.
- Regressa ao`messages.groupChat.historyLimit`. Definir`0`para desabilitar (padrão 50).
- O histórico de DM pode ser limitado com`channels.msteams.dmHistoryLimit`(tornos de usuário).`channels.msteams.dms["<user_id>"].historyLimit`.

## Equipes atuais Permissões RSC (Manifesto)

Estes são os **recursos existentesPermissões específicas** no manifesto do aplicativo Teams. Eles só se aplicam dentro da equipe/chat onde o aplicativo está instalado.

** Para canais (team scope):**

-`ChannelMessage.Read.Group`(Aplicação) - recebe todas as mensagens do canal sem @ mencion
-`ChannelMessage.Send.Group`(Aplicação)
-`Member.Read.Group`(Aplicação)
-`Owner.Read.Group`(Aplicação)
-`ChannelSettings.Read.Group`(Aplicação)
-`TeamMember.Read.Group`(Aplicação)
-`TeamSettings.Read.Group`(Aplicação)

**Para conversas em grupo:**

-`ChatMessage.Read.Chat`(Aplicação) - recebe todas as mensagens de chat do grupo sem @ mention

## Manifesto de Equipes de Exemplo (reditado)

Exemplo mínimo, válido com os campos necessários. Substituir IDs e URLs.

```json
{
  "$schema": "https://developer.microsoft.com/en-us/json-schemas/teams/v1.23/MicrosoftTeams.schema.json",
  "manifestVersion": "1.23",
  "version": "1.0.0",
  "id": "00000000-0000-0000-0000-000000000000",
  "name": { "short": "OpenClaw" },
  "developer": {
    "name": "Your Org",
    "websiteUrl": "https://example.com",
    "privacyUrl": "https://example.com/privacy",
    "termsOfUseUrl": "https://example.com/terms"
  },
  "description": { "short": "OpenClaw in Teams", "full": "OpenClaw in Teams" },
  "icons": { "outline": "outline.png", "color": "color.png" },
  "accentColor": "#5B6DEF",
  "bots": [
    {
      "botId": "11111111-1111-1111-1111-111111111111",
      "scopes": ["personal", "team", "groupChat"],
      "isNotificationOnly": false,
      "supportsCalling": false,
      "supportsVideo": false,
      "supportsFiles": true
    }
  ],
  "webApplicationInfo": {
    "id": "11111111-1111-1111-1111-111111111111"
  },
  "authorization": {
    "permissions": {
      "resourceSpecific": [
        { "name": "ChannelMessage.Read.Group", "type": "Application" },
        { "name": "ChannelMessage.Send.Group", "type": "Application" },
        { "name": "Member.Read.Group", "type": "Application" },
        { "name": "Owner.Read.Group", "type": "Application" },
        { "name": "ChannelSettings.Read.Group", "type": "Application" },
        { "name": "TeamMember.Read.Group", "type": "Application" },
        { "name": "TeamSettings.Read.Group", "type": "Application" },
        { "name": "ChatMessage.Read.Chat", "type": "Application" }
      ]
    }
  }
}
```

## Ressalvas manifestas #

-`bots[].botId`** deve corresponder ao Azure Bot App ID.
-`webApplicationInfo.id`**deve** corresponder ao Azure Bot App ID.
-`bots[].scopes`deve incluir as superfícies que pretende utilizar `personal`,`team`,`groupChat`.
-`bots[].supportsFiles: true`é necessário para o tratamento de arquivos em âmbito pessoal.
-`authorization.permissions.resourceSpecific`deve incluir leitura/enviar do canal se você quiser tráfego do canal.

## # Atualizando uma aplicação existente

Para atualizar um aplicativo Teams já instalado (por exemplo, para adicionar permissões RSC):

1. Atualize seu`manifest.json`com as novas configurações
2. **Incremento do campo`version`** (por exemplo,`1.0.0`→`1.1.0`
3. **Re-zip** o manifesto com ícones `manifest.json`,`outline.png`,`color.png`
4. Envie o novo zip:
- ** Opção A (Teams Admin Center):** Equipes Centro de Administração → Equipes apps → Gerenciar aplicativos → encontrar seu aplicativo → Enviar nova versão
- ** Opção B (Sideload):** Em Equipes → Apps → Gerencie seus aplicativos → Envie um aplicativo personalizado
5. **Para canais de equipa:** Reinstalar o aplicativo em cada equipe para novas permissões para fazer efeito
6. **Fully sair e relançar Equipes** (não apenas fechar a janela) para limpar metadados de aplicativos em cache

## Capacidades: apenas RSC vs Gráfico

### Com **Teams RSC only** (app installed, no Graph API permissions)

Trabalhos:

- Leia a mensagem do canal **texto** conteúdo.
- Enviar mensagem de canal **texto** conteúdo.
- Receba anexos pessoais (DM)**.

NÃO funciona:

- Canal/grupo **imagem ou conteúdo de arquivo** (payload só inclui HTML stub).
- Baixando anexos armazenados no SharePoint/OneDrive.
- Lendo o histórico de mensagens (além do evento webhook ao vivo).

## # Com **Teams RSC + Microsoft Graph Application permissions**

Adiciona:

- Baixando conteúdo hospedado (imagens coladas em mensagens).
- Baixando anexos de arquivos armazenados no SharePoint / OneDrive.
- Lendo o histórico de mensagens via Graph.

### RSC vs Graph API

□ Capacidade □ Permissões RSC
----------------------- ------------------------------------ ------------------------------------
Sim (via webhook) Não (apenas polling)
Sim (pode consultar o histórico)
Setup complexity** Setup complexity** Se manifesta apenas o aplicativo .
Sim (pergunta a qualquer momento)

** Linha do botão:** RSC é para escuta em tempo real; API do gráfico é para acesso histórico. Para recuperar mensagens perdidas enquanto estiver offline, você precisa da API do gráfico com`ChannelMessage.Read.All`(necessita do consentimento do administrador).

### Mídia com recursos gráficos + história (necessário para canais)

Se você precisar de imagens/arquivos em **canais** ou quiser buscar ** histórico de mensagens**, você deve ativar as permissões do Microsoft Graph e conceder o consentimento do administrador.

1. In Entra ID (Azure AD) ** Inscrição do aplicativo**, adicione Microsoft Graph **Permissões de aplicação**:
-`ChannelMessage.Read.All`(anexações de canal + histórico)
-`Chat.Read.All`ou`ChatMessage.Read.All`(conversas de grupo)
2. **Consentimento do administrador do Grant** para o inquilino.
3. Bump the Teams app **manifest version**, re-upload, e **reinstalar o aplicativo em Teams**.
4. **Fully sair e relançar equipes** para limpar metadados de aplicativos em cache.

## Limitações conhecidas

Tempo limite para o Webhook

As equipes entregam mensagens via webhook HTTP. Se o processamento demorar demasiado tempo (por exemplo, respostas lentas do LLM), poderá ver:

- Tempo limite na porta.
- Equipas a tentar novamente a mensagem (causando duplicatas)
- Respostas retiradas

O Openclaw lida com isso retornando rapidamente e enviando respostas proativamente, mas respostas muito lentas ainda podem causar problemas.

Formatação

A marcação das equipas é mais limitada do que o Slack ou Discord:

- Formatação básica funciona: ** bold**,  italic ,`code`, links
- Marcação complexa (tabelas, listas aninhadas) pode não renderizar corretamente
- Cartões adaptativos são suportados para pesquisas e envios de cartões arbitrários (ver abaixo)

Configuração

Configurações de chaves (ver`/gateway/configuration`para padrões de canais compartilhados):

-`channels.msteams.enabled`: activar/desactivar o canal.
-`channels.msteams.appId`,`channels.msteams.appPassword`,`channels.msteams.tenantId`: credenciais bot.
-`channels.msteams.webhook.port`(padrão`3978`
-`channels.msteams.webhook.path`(padrão`/api/messages`
-`channels.msteams.dmPolicy`:`pairing | allowlist | open | disabled`(por omissão: pareamento)
-`channels.msteams.appId`0: allowlist para DMs (IDs de objetos AAD, UPNs ou nomes de exibição). O assistente resolve nomes para IDs durante a configuração quando o acesso ao Gráfico está disponível.
-`channels.msteams.appId`1: tamanho de texto de saída.
-`channels.msteams.appId`2:`channels.msteams.appId`3 (padrão) ou`channels.msteams.appId`4 para dividir em linhas em branco (limites de parágrafos) antes do corte de comprimento.
-`channels.msteams.appId`5: allowlist for inbound anexo hosts (defaults to Microsoft/Teams domains).
-`channels.msteams.appId`6: requer @ mesion em canais/grupos (padrão true).
-`channels.msteams.appId`7:`channels.msteams.appId`8 (ver [Estilo de Resposta]#reply-style-threads-vs-posts.
-`channels.msteams.appId`9: substituição por equipa.
-`channels.msteams.appPassword`0: substituição por equipa.
-`channels.msteams.appPassword`1: a política de ferramentas padrão por equipe sobrepõe-se `channels.msteams.appPassword`2/`channels.msteams.appPassword`3/`channels.msteams.appPassword`4) usada quando falta uma sobreposição de canal.
-`channels.msteams.appPassword`5: a política de ferramentas padrão por equipe por sender (o`channels.msteams.appPassword`6 é suportado).
-`channels.msteams.appPassword`7: substituição por canal.
-`channels.msteams.appPassword`8: substituição por canal.
-`channels.msteams.appPassword`9: sobrepõe a política de ferramentas por canal `channels.msteams.tenantId`0/`channels.msteams.tenantId`1/`channels.msteams.tenantId`2).
-`channels.msteams.tenantId`3: sobrepõe-se a política de ferramentas por canal (suportado o`channels.msteams.tenantId`4).
-`channels.msteams.tenantId`5: SharePoint site ID para uploads de arquivos em chats/canais de grupo (ver [Enviar arquivos em chats de grupo] #sending-files-in-group-chats.

## Roteamento & Sessões

- As teclas de sessão seguem o formato padrão do agente (ver [/conceitos/sessão]/concepts/session:
- Mensagens diretas compartilham a sessão principal `agent:<agentId>:<mainKey>`.
- Mensagens de canal/grupo usam o ID de conversação:
-`agent:<agentId>:msteams:channel:<conversationId>`-`agent:<agentId>:msteams:group:<conversationId>`

## Estilo de Resposta: Tópicos vs Posts

As equipes introduziram recentemente dois estilos de interface de canal sobre o mesmo modelo de dados subjacente:

Descrição do estilo`replyStyle`recomendado
---------------------------------------------------------------------------------------------------------- ------
*Posts** (clássico) *Mensagens aparecem como cartões com respostas encriptadas por baixo de`thread`(padrão)
As mensagens fluem linearmente, mais como o Slack.

** O problema:** A API Teams não expõe qual o estilo de interface que um canal usa. Se utilizar o`replyStyle`errado:

-`thread`em um canal estilo Threads → respostas aparecem aninhadas de forma estranha
-`top-level`em um canal de Posts-estilo → respostas aparecem como posts de topo separados em vez de em-thread

**Solução: ** Configurar`replyStyle`por canal baseado em como o canal é configurado:

```json
{
  "msteams": {
    "replyStyle": "thread",
    "teams": {
      "19:abc...@thread.tacv2": {
        "channels": {
          "19:xyz...@thread.tacv2": {
            "replyStyle": "top-level"
          }
        }
      }
    }
  }
}
```

## Anexos e imagens

** Limitações actuais: **

- **DMs:** Imagens e anexos de arquivos funcionam através de APIs de arquivos bot Teams.
- ** Canais/grupos:** Os anexos estão ao vivo no armazenamento M365 (SharePoint/OneDrive). A carga útil do webhook inclui apenas um stub HTML, não os bytes reais do arquivo. **As permissões da API Graph são necessárias** para baixar anexos do canal.

Sem permissões do Graph, as mensagens do canal com imagens serão recebidas apenas como texto (o conteúdo da imagem não é acessível ao bot).
Por padrão, o OpenClaw só baixa mídia dos hostnames da Microsoft/Teams. Substituir pelo`channels.msteams.mediaAllowHosts`(utilizar o`["*"]`para permitir qualquer hospedeiro).

## Enviando arquivos em chats de grupo

Bots pode enviar arquivos em DMs usando o fluxo FileConsentCard (built-in). No entanto, **enviar arquivos em chats/canais de grupo** requer configuração adicional:

Contexto Como os arquivos são enviados
---------------------------------------
. **DMs** . . Cartão → o usuário aceita → uploads de bots
• **Conversas/canais em grupo** □ Envio para SharePoint → Ligação de partilha □ Requer`sharePointSiteId`+ Permissões de gráfico
* Imagens (qualquer contexto)** Base64-codificado em linha

## # Porque chats em grupo precisam de SharePoint

Os bots não têm uma unidade OneDrive pessoal (o endpoint`/me/drive`Graph API não funciona para identidades de aplicativos). Para enviar arquivos em chats/canais de grupo, o bot envia para um site **SharePoint e cria um link de compartilhamento.

Configuração

1. **Add Graph API permissions** in Entra ID (Azure AD) → App Registration:
-`Sites.ReadWrite.All`(Aplicação) - envie arquivos para SharePoint
-`Chat.Read.All`(Aplicação) - opcional, permite ligações de partilha por utilizador

2. **Consentimento do administrador do Grant** para o inquilino.

3. ** Obtenha o seu ID do site SharePoint:**

   ```bash
   # Via Graph Explorer or curl with a valid token:
   curl -H "Authorization: Bearer $TOKEN" \
     "https://graph.microsoft.com/v1.0/sites/{hostname}:/{site-path}"

   # Example: for a site at "contoso.sharepoint.com/sites/BotFiles"
   curl -H "Authorization: Bearer $TOKEN" \
     "https://graph.microsoft.com/v1.0/sites/contoso.sharepoint.com:/sites/BotFiles"

   # Response includes: "id": "contoso.sharepoint.com,guid1,guid2"
   ```

4. **Configurar OpenClaw:**
   ```json5
   {
     channels: {
       msteams: {
         // ... other config ...
         sharePointSiteId: "contoso.sharepoint.com,guid1,guid2",
       },
     },
   }
   ```

### Comportamento de partilha

Permissão; comportamento de partilha;
-------------------------------------------------------- -----------------------------------------------------------------------------------------
Apenas o`Sites.ReadWrite.All`•`Sites.ReadWrite.All`+`Chat.Read.All`

O compartilhamento por usuário é mais seguro, pois apenas os participantes do chat podem acessar o arquivo. Se a permissão`Chat.Read.All`estiver faltando, o bot cai de volta para o compartilhamento em toda a organização.

Comportamento de retrocesso

Resultado
-----------------------------------------------------------------
Grupo de bate-papo + arquivo +`sharePointSiteId`configurado .
Grupo de bate-papo + arquivo + sem`sharePointSiteId`□ Conversa pessoal + ficheiro □ Fluxo do FileConsentCard (funciona sem SharePoint)
□ Qualquer contexto + imagem

## # Arquivos armazenados local

Os arquivos enviados são armazenados em uma pasta`/OpenClawShared/`na biblioteca de documentos padrão do site do SharePoint configurado.

## Pesquisas (Cartões Adaptos)

OpenClaw envia enquetes de equipes como cartões adaptativos (não existe API de enquete de equipes nativas).

- CLI:`openclaw message poll --channel msteams --target conversation:<id> ...`- Os votos são registrados pela porta de entrada em`~/.openclaw/msteams-polls.json`.
- O portal deve ficar online para gravar votos.
- As pesquisas ainda não publicam automaticamente resumos de resultados (inspecione o arquivo de armazenamento se necessário).

## Cartões adaptativos (arbitrários)

Envie qualquer Cartão Adaptativo JSON para usuários de Equipes ou conversas usando a ferramenta`message`ou CLI.

O parâmetro`card`aceita um objeto JSON de Cartão Adaptativo. Quando o`card`é fornecido, o texto da mensagem é opcional.

** Ferramenta do agente:**

```json
{
  "action": "send",
  "channel": "msteams",
  "target": "user:<id>",
  "card": {
    "type": "AdaptiveCard",
    "version": "1.5",
    "body": [{ "type": "TextBlock", "text": "Hello!" }]
  }
}
```

** CLI:**

```bash
openclaw message send --channel msteams \
  --target "conversation:19:abc...@thread.tacv2" \
  --card '{"type":"AdaptiveCard","version":"1.5","body":[{"type":"TextBlock","text":"Hello!"}]}'
```

Veja [Documentação de cartões adaptativos]https://adaptivecards.io/ para esquema de cartões e exemplos. Para detalhes do formato de destino, consulte [Formatos de alvo]#target-formats abaixo.

## Formatos de destino

Alvos do MSTeam usam prefixos para distinguir entre usuários e conversas:

Tipo de alvo Formato Exemplo
---------------------------------------------------------------------------------------------------
OUTXCODE1
□ Usuário (por nome)`conversation:<conversation-id>``<conversation-id>`(se contiver`@thread`

** Exemplos de CLI:**

```bash
# Send to a user by ID
openclaw message send --channel msteams --target "user:40a1a0ed-..." --message "Hello"

# Send to a user by display name (triggers Graph API lookup)
openclaw message send --channel msteams --target "user:John Smith" --message "Hello"

# Send to a group chat or channel
openclaw message send --channel msteams --target "conversation:19:abc...@thread.tacv2" --message "Hello"

# Send an Adaptive Card to a conversation
openclaw message send --channel msteams --target "conversation:19:abc...@thread.tacv2" \
  --card '{"type":"AdaptiveCard","version":"1.5","body":[{"type":"TextBlock","text":"Hello"}]}'
```

** Exemplos de ferramentas:**

```json
{
  "action": "send",
  "channel": "msteams",
  "target": "user:John Smith",
  "message": "Hello!"
}
```

```json
{
  "action": "send",
  "channel": "msteams",
  "target": "conversation:19:abc...@thread.tacv2",
  "card": {
    "type": "AdaptiveCard",
    "version": "1.5",
    "body": [{ "type": "TextBlock", "text": "Hello" }]
  }
}
```

Nota: Sem o prefixo`user:`, nomes padrão para resolução de grupo/equipe. Use sempre`user:`ao direcionar as pessoas pelo nome de exibição.

## Mensagens proativas

- Mensagens proativas só são possíveis **depois** um usuário interage, porque armazenamos referências de conversa nesse ponto.
- Ver`/gateway/configuration`para o`dmPolicy`e lista de licenças.

## IDs de Equipa e Canal (Conseguido)

O parâmetro`groupId`em URLs de equipes é **NOT** o ID de equipe usado para configuração. Extrair IDs da localização do URL em vez disso:

** URL da equipe:**

```
https://teams.microsoft.com/l/team/19%3ABk4j...%40thread.tacv2/conversations?groupId=...
                                    └────────────────────────────┘
                                    Team ID (URL-decode this)
```

** URL do canal:**

```
https://teams.microsoft.com/l/channel/19%3A15bc...%40thread.tacv2/ChannelName?groupId=...
                                      └─────────────────────────┘
                                      Channel ID (URL-decode this)
```

** Para a configuração:**

- ID da equipa = segmento de localização após`/team/`(URL-decodificado, por exemplo,`19:Bk4j...@thread.tacv2`
- Canal ID = segmento de caminho após`/channel/`(URL-decodificado)
- **Ignore** o parâmetro de consulta`groupId`

## Canais Privados

Os bots têm suporte limitado em canais privados:

Característica Canais Padrão Canais Privados
------------------ -------------------------------
Instalação de bots
• Mensagens em tempo real (webhook)
Sim Sim Pode comportar-se de forma diferente
Sim Se o bot é acessível
Gráfico histórico da API Sim Sim Sim

** Solução alternativa se canais privados não funcionarem:**

1. Use canais padrão para interações bot
2. Use DMs - os usuários sempre podem enviar mensagem do bot diretamente
3. Use API de gráfico para acesso histórico (requer`ChannelMessage.Read.All`

## Resolução de problemas

Questões comuns

- **Imagens não exibidas em canais:** Faltam permissões de gráfico ou consentimento do administrador. Reinstalar o aplicativo Teams e sair/reabrir totalmente Equipes.
- ** Nenhuma resposta no canal:** as menções são exigidas por padrão; set`channels.msteams.requireMention=false`ou configure por equipe/canal.
- ** Descompatibilidade de versão (Equipes ainda mostra manifesto antigo):** remover + re-adicionar o aplicativo e totalmente sair Equipes para atualizar.
- **401 Não autorizado do webhook:** Espera-se que ao testar manualmente sem Azure JWT - o ponto final seja alcançável, mas a autenticação falhou. Use o Web Chat do Azure para testar corretamente.

## # Manifeste erros de upload

- **"O ficheiro Ícone não pode estar vazio":** Os ficheiros de ícones de referências do manifesto que são 0 bytes. Criar ícones PNG válidos (32x32 para`outline.png`, 192x192 para`color.png`.
- **"webAplicationInfo. Id já em uso":** O aplicativo ainda está instalado em outra equipe/chat. Encontre e desinstale-o primeiro, ou aguarde 5-10 minutos para propagação.
- **"Algo deu errado" no upload:** Enviar via https://admin.teams.microsoft.com em vez disso, abrir o navegador DevTools (F12) → Guia de rede, e verificar o corpo de resposta para o erro real.
- ** Falha na carga lateral: ** Tente "Upload um aplicativo para o catálogo de aplicativos da sua org" em vez de "Upload um aplicativo personalizado" - isso muitas vezes ignora restrições de carga lateral.

Permissões RSC não funcionam

1. Verifique`webApplicationInfo.id`corresponde exatamente ao ID do aplicativo do seu bot
2. Re-upload o aplicativo e reinstalar na equipe / conversa
3. Verifique se seu administrador org bloqueou as permissões RSC
4. Confirme que você está usando o escopo certo:`ChannelMessage.Read.Group`para equipes,`ChatMessage.Read.Chat`para chats de grupo

## Referências

Azure Guia de configuração do Bot
- [Teams Developer Portal] https://dev.teams.microsoft.com/apps - criar/gerenciar aplicativos de equipes
- [Teams app manifesto esquema] https://learn.microsoft.com/en-us/microsoftteams/platform/resources/schema/manifest-schema
- [Receber mensagens de canal com RSC] https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/conversations/channel-messages-with-rsc
- [Referência de permissões RSC] https://learn.microsoft.com/en-us/microsoftteams/platform/graph-api/rsc/resource-specific-consent
- [Teams bot file handling] https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/bots-filesv4 (canal/grupo requer gráfico)
https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/conversations/send-proactive-messages
