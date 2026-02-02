---
summary: "Mattermost bot setup and OpenClaw config"
read_when:
  - Setting up Mattermost
  - Debugging Mattermost routing
---

# Mattermost (plugin)

Estado: suportado através de plugin (toque de bot + eventos WebSocket). Canais, grupos e DMs são suportados.
Mattermost é uma plataforma de mensagens de equipe self-hostable; veja o site oficial em
[mattermost.com]https://mattermost.com para detalhes do produto e downloads.

## Plugin necessário

Mattermost ships como um plugin e não é empacotado com a instalação do núcleo.

Instalar via CLI (registro npm):

```bash
openclaw plugins install @openclaw/mattermost
```

Obtenção local (quando em execução a partir de um git repo):

```bash
openclaw plugins install ./extensions/mattermost
```

Se você escolher Mattermost durante a configuração/onboarding e um git checkout for detectado,
OpenClaw irá oferecer o caminho de instalação local automaticamente.

Detalhes: [Plugins]/plugin

## Montagem rápida

1. Instale o plugin Mattermost.
2. Crie uma conta bot Mattermost e copie o símbolo **bot **.
3. Copie o URL mais importante ** (por exemplo,`https://chat.example.com`.
4. Configure OpenClaw e inicie o gateway.

Configuração mínima:

```json5
{
  channels: {
    mattermost: {
      enabled: true,
      botToken: "mm-token",
      baseUrl: "https://chat.example.com",
      dmPolicy: "pairing",
    },
  },
}
```

## Variáveis de ambiente (conta padrão)

Configure estes na máquina de gateway se preferir o env vars:

-`MATTERMOST_BOT_TOKEN=...`-`MATTERMOST_URL=https://chat.example.com`

Env vars aplica- se apenas à conta **default** `default`. Outras contas devem usar valores de configuração.

## Modos de conversa

A matéria mais responde aos DMs automaticamente. O comportamento do canal é controlado pelo`chatmode`:

-`oncall`(padrão): responda somente quando @ mencionado em canais.
-`onmessage`: responda a cada mensagem de canal.
-`onchar`: responda quando uma mensagem começa com um prefixo de gatilho.

Exemplo de configuração:

```json5
{
  channels: {
    mattermost: {
      chatmode: "onchar",
      oncharPrefixes: [">", "!"],
    },
  },
}
```

Notas:

-`onchar`ainda responde a expressões explícitas.
-`channels.mattermost.requireMention`é homenageado por configs legados, mas`chatmode`é preferido.

## Controle de acesso (DMs)

- Padrão:`channels.mattermost.dmPolicy = "pairing"`(enviadores desconhecidos recebem um código de pareamento).
- Aprovar via:
-`openclaw pairing list mattermost`-`openclaw pairing approve mattermost <CODE>`- DM públicos:`channels.mattermost.dmPolicy="open"`mais`channels.mattermost.allowFrom=["*"]`.

## Canais (grupos)

- Predefinição:`channels.mattermost.groupPolicy = "allowlist"`(perioditado).
- Os remetentes da lista de licenças com`channels.mattermost.groupAllowFrom`(IDs do utilizador ou`@username`.
- Canais abertos:`channels.mattermost.groupPolicy="open"`(periodização).

## Alvos para entrega de saída

Use estes formatos de destino com`openclaw message send`ou cron/webhooks:

-`channel:<id>`para um canal
-`user:<id>`para um DM
-`@username`para um DM (resolvido através da API Mattermost)

IDs nus são tratados como canais.

## Multi-conta

Mattermost suporta várias contas no`channels.mattermost.accounts`:

```json5
{
  channels: {
    mattermost: {
      accounts: {
        default: { name: "Primary", botToken: "mm-token", baseUrl: "https://chat.example.com" },
        alerts: { name: "Alerts", botToken: "mm-token-2", baseUrl: "https://alerts.example.com" },
      },
    },
  },
}
```

## Resolução de problemas

- Nenhuma resposta nos canais: garantir que o bot está no canal e mencioná-lo (de plantão), usar um prefixo de gatilho (onchar), ou definir`chatmode: "onmessage"`.
- Erros de autenticação: verifique o token bot, URL base e se a conta está ativada.
- Problemas de contas múltiplas: Env vars só se aplicam à conta`default`.
