---
summary: "LINE Messaging API plugin setup, config, and usage"
read_when:
  - You want to connect OpenClaw to LINE
  - You need LINE webhook + credential setup
  - You want LINE-specific message options
---

LINE (plugin)

LINE conecta-se ao OpenClaw através da API LINE Messaging. O plugin é executado como um webhook
receptor no gateway e usa seu token de acesso de canal + segredo de canal para
autenticação.

Estado: suportado através do plugin. Mensagens diretas, chats de grupo, mídia, locais, Flex
mensagens, mensagens de modelo e respostas rápidas são suportadas. Reações e fios
não são suportados.

## Plugin necessário

Instale o plug-in LINE:

```bash
openclaw plugins install @openclaw/line
```

Obtenção local (quando em execução a partir de um git repo):

```bash
openclaw plugins install ./extensions/line
```

Configuração

1. Crie uma conta LINE Developers e abra o Console:
https://developers.line.biz/console/
2. Crie (ou escolha) um Provedor e adicione um canal **Messaging API**.
3. Copie o token de acesso do canal** e o segredo do canal** das configurações do canal.
4. Habilite **Use webhook** nas configurações da API de Mensagens.
5. Defina o URL do webhook para o seu ponto final do gateway (HTTPS necessário):

```
https://gateway-host/line/webhook
```

O gateway responde à verificação webhook da LINE (GET) e eventos de entrada (POST).
Se precisar de um caminho personalizado, defina`channels.line.webhookPath`ou`channels.line.accounts.<id>.webhookPath`e atualizar o URL em conformidade.

Configurar

Configuração mínima:

```json5
{
  channels: {
    line: {
      enabled: true,
      channelAccessToken: "LINE_CHANNEL_ACCESS_TOKEN",
      channelSecret: "LINE_CHANNEL_SECRET",
      dmPolicy: "pairing",
    },
  },
}
```

Vars de Env (conta padrão apenas):

-`LINE_CHANNEL_ACCESS_TOKEN`-`LINE_CHANNEL_SECRET`

Token/secret files:

```json5
{
  channels: {
    line: {
      tokenFile: "/path/to/line-token.txt",
      secretFile: "/path/to/line-secret.txt",
    },
  },
}
```

Contas múltiplas:

```json5
{
  channels: {
    line: {
      accounts: {
        marketing: {
          channelAccessToken: "...",
          channelSecret: "...",
          webhookPath: "/line/marketing",
        },
      },
    },
  },
}
```

## Controle de acesso

Mensagens diretas padrão para emparelhamento. Os remetentes desconhecidos recebem um código de pareamento e o seu
as mensagens são ignoradas até serem aprovadas.

```bash
openclaw pairing list line
openclaw pairing approve line <CODE>
```

Listas de licenças e políticas:

-`channels.line.dmPolicy`:`pairing | allowlist | open | disabled`-`channels.line.allowFrom`: IDs de usuário de linha autorizados para DM
-`channels.line.groupPolicy`:`allowlist | open | disabled`-`channels.line.groupAllowFrom`: IDs de usuário de linha permitidos para grupos
- Substituições por grupo:`channels.line.groups.<groupId>.allowFrom`

IDs de linha são sensíveis a casos. IDs válidos se parecem com:

- Usuário:`U`+ 32 caracteres hex
- Grupo:`C`+ 32 caracteres hex
- Quarto:`R`+ 32 caracteres hex

## Comportamento da mensagem

- O texto está dividido em 5000 caracteres.
- Formatação de marcação é despojada; blocos de código e tabelas são convertidos em Flex
cartas, quando possível.
- As respostas de transmissão são buffered; LINE recebe blocos completos com um carregamento
animação enquanto o agente trabalha.
- Os downloads de mídia são tampados por`channels.line.mediaMaxMb`(padrão 10).

### Dados do canal (mensagens ricas)

Use`channelData.line`para enviar respostas rápidas, locais, cartões Flex ou modelo
mensagens.

```json5
{
  text: "Here you go",
  channelData: {
    line: {
      quickReplies: ["Status", "Help"],
      location: {
        title: "Office",
        address: "123 Main St",
        latitude: 35.681236,
        longitude: 139.767125,
      },
      flexMessage: {
        altText: "Status card",
        contents: {
          /* Flex payload */
        },
      },
      templateMessage: {
        type: "confirm",
        text: "Proceed?",
        confirmLabel: "Yes",
        confirmData: "yes",
        cancelLabel: "No",
        cancelData: "no",
      },
    },
  },
}
```

O plugin LINE também envia um comando`/card`para predefinições de mensagens Flex:

```
/card info "Welcome" "Thanks for joining!"
```

## Resolução de problemas

- ** A verificação do Webhook falha:** garantir que o URL do webhook seja HTTPS e o`channelSecret`corresponde à consola LINE.
- ** Nenhum evento de entrada:** confirmar o caminho webhook corresponde`channels.line.webhookPath`e que o portal é acessível a partir do LINE.
- ** Erros de download da mídia:** levantar`channels.line.mediaMaxMb`se a mídia exceder o
limite padrão.
