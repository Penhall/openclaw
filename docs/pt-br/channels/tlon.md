---
summary: "Tlon/Urbit support status, capabilities, and configuration"
read_when:
  - Working on Tlon/Urbit channel features
---

# Tlon (plugin)

Tlon é um mensageiro descentralizado construído em Urbit. OpenClaw se conecta à sua nave Urbit e pode
responder a DMs e mensagens de chat de grupo. As respostas do grupo requerem uma menção @ por padrão e podem
ser restringidos através de listas de licenças.

Estado: suportado através do plugin. DMs, menções de grupo, respostas de discussão e recuo de mídia somente texto
(URL anexado à legenda). Reações, pesquisas e uploads de mídia nativas não são suportados.

## Plugin necessário

Tlon envia como um plugin e não é empacotado com o núcleo instalar.

Instalar via CLI (registro npm):

```bash
openclaw plugins install @openclaw/tlon
```

Obtenção local (quando em execução a partir de um git repo):

```bash
openclaw plugins install ./extensions/tlon
```

Detalhes: [Plugins]/plugin

Configuração

1. Instale o plugin Tlon.
2. Reúna o URL do seu navio e código de login.
3. Configurar`channels.tlon`.
4. Reinicie o portal.
5. DM o bot ou mencioná-lo em um canal de grupo.

Configuração mínima (conta única):

```json5
{
  channels: {
    tlon: {
      enabled: true,
      ship: "~sampel-palnet",
      url: "https://your-ship-host",
      code: "lidlut-tabwed-pillex-ridrup",
    },
  },
}
```

## Canais de grupo

A descoberta automática está activada por omissão. Você também pode fixar canais manualmente:

```json5
{
  channels: {
    tlon: {
      groupChannels: ["chat/~host-ship/general", "chat/~host-ship/support"],
    },
  },
}
```

Desactivar a descoberta automática:

```json5
{
  channels: {
    tlon: {
      autoDiscoverChannels: false,
    },
  },
}
```

## Controle de acesso

Lista de autorizações de DM (vazio = permitir todos):

```json5
{
  channels: {
    tlon: {
      dmAllowlist: ["~zod", "~nec"],
    },
  },
}
```

Autorização do grupo (restrita por omissão):

```json5
{
  channels: {
    tlon: {
      defaultAuthorizedShips: ["~zod"],
      authorization: {
        channelRules: {
          "chat/~host-ship/general": {
            mode: "restricted",
            allowedShips: ["~zod", "~nec"],
          },
          "chat/~host-ship/announcements": {
            mode: "open",
          },
        },
      },
    },
  },
}
```

## Alvos de entrega (CLI/cron)

Use estes com`openclaw message send`ou entrega de cron:

- DM:`~sampel-palnet`ou`dm/~sampel-palnet`- Grupo:`chat/~host-ship/channel`ou`group:~host-ship/channel`

## Notas

- As respostas de grupo exigem uma menção (por exemplo,`~your-bot-ship` para responder.
- Respostas de thread: se a mensagem de entrada está em um thread, o OpenClaw responde em thread.
- Mídia:`sendMedia`volta para texto + URL (sem upload nativo).
