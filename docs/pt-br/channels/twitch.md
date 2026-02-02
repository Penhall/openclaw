---
summary: "Twitch chat bot configuration and setup"
read_when:
  - Setting up Twitch chat integration for OpenClaw
---

# Twitch (plugin)

Suporte de bate-papo Twitch via conexão IRC. O OpenClaw se conecta como usuário de Twitch (conta bot) para receber e enviar mensagens em canais.

## Plugin necessário

Twitch navios como um plugin e não é empacotado com o núcleo instalar.

Instalar via CLI (registro npm):

```bash
openclaw plugins install @openclaw/twitch
```

Obtenção local (quando em execução a partir de um git repo):

```bash
openclaw plugins install ./extensions/twitch
```

Detalhes: [Plugins]/plugin

## Montagem rápida (início)

1. Crie uma conta de Twitch dedicada para o bot (ou use uma conta existente).
2. Gerar credenciais: [Twitch Token Generator] https://twitchtokengenerator.com/
- Selecione **Bot Token **
- Verificar os âmbitos`chat:read`e`chat:write`- Copie o ID do Cliente** e o Token de Acesso**
3. Encontre o seu ID do utilizador Twitch: https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/
4. Configurar o token:
- Env:`OPENCLAW_TWITCH_ACCESS_TOKEN=...`(apenas conta padrão)
- Ou configuração:`channels.twitch.accessToken`- Se ambos estiverem definidos, a configuração tem precedência (inv fallback é apenas conta padrão).
5. Inicie o portal.

* Importante:** Adicione o controle de acesso `allowFrom`ou`allowedRoles` para evitar que usuários não autorizados acionem o bot.`requireMention`defaults to`true`.

Configuração mínima:

```json5
{
  channels: {
    twitch: {
      enabled: true,
      username: "openclaw", // Bot's Twitch account
      accessToken: "oauth:abc123...", // OAuth Access Token (or use OPENCLAW_TWITCH_ACCESS_TOKEN env var)
      clientId: "xyz789...", // Client ID from Token Generator
      channel: "vevisk", // Which Twitch channel's chat to join (required)
      allowFrom: ["123456789"], // (recommended) Your Twitch user ID only - get it from https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/
    },
  },
}
```

## O que é

- Um canal Twitch da Gateway.
- Roteamento determinístico: respostas sempre voltar para Twitch.
- Cada conta mapeia para uma chave de sessão isolada`agent:<agentId>:twitch:<accountName>`.
-`username`é a conta do bot (que autentica),`channel`é que sala de bate-papo para participar.

## Configuração (detalhada)

Gerar credenciais

Usar [Gerador de Token Twitch] https://twitchtokengenerator.com/:

- Selecione **Bot Token **
- Verificar os âmbitos`chat:read`e`chat:write`- Copie o ID do Cliente** e o Token de Acesso**

Não é necessário registro manual do aplicativo. Tokens expiram após várias horas.

Configurar o bot

** Env var (apenas conta padrão):**

```bash
OPENCLAW_TWITCH_ACCESS_TOKEN=oauth:abc123...
```

**Ou configuração:**

```json5
{
  channels: {
    twitch: {
      enabled: true,
      username: "openclaw",
      accessToken: "oauth:abc123...",
      clientId: "xyz789...",
      channel: "vevisk",
    },
  },
}
```

Se tanto env quanto config estiverem configurados, a configuração terá precedência.

## # Controle de acesso (recomendado)

```json5
{
  channels: {
    twitch: {
      allowFrom: ["123456789"], // (recommended) Your Twitch user ID only
      allowedRoles: ["moderator"], // Or restrict to roles
    },
  },
}
```

**Papeles disponíveis:**`"moderator"`,`"owner"`,`"vip"`,`"subscriber"`,`"all"`.

** Por que IDs de usuário?** Os nomes de usuário podem mudar, permitindo a personificação. IDs de usuário são permanentes.

Encontre seu ID do usuário Twitch: https://www.streamweasels.com/tools/convert-twitch- username-%20to- user-id/ (Converta seu nome de usuário Twitch para ID)

## Tocar atualização (opcional)

Tokens from [Twitch Token Generator] https://twitchtokengenerator.com/ não pode ser automaticamente atualizado - regenerar quando expirado.

Para atualização automática do token, crie sua própria aplicação Twitch no [Twitch Developer Console] https://dev.twitch.tv/console e adicione à configuração:

```json5
{
  channels: {
    twitch: {
      clientSecret: "your_client_secret",
      refreshToken: "your_refresh_token",
    },
  },
}
```

O bot atualiza automaticamente os tokens antes da expiração e registra os eventos de atualização.

## Suporte multi-conta

Use`channels.twitch.accounts`com fichas por conta. Ver `gateway/configuration`/gateway/configuration para o padrão partilhado.

Exemplo (uma conta bot em dois canais):

```json5
{
  channels: {
    twitch: {
      accounts: {
        channel1: {
          username: "openclaw",
          accessToken: "oauth:abc123...",
          clientId: "xyz789...",
          channel: "vevisk",
        },
        channel2: {
          username: "openclaw",
          accessToken: "oauth:def456...",
          clientId: "uvw012...",
          channel: "secondchannel",
        },
      },
    },
  },
}
```

**Nota:** Cada conta precisa do seu próprio token (um token por canal).

## Controle de acesso

## # Restrições baseadas em papéis

```json5
{
  channels: {
    twitch: {
      accounts: {
        default: {
          allowedRoles: ["moderator", "vip"],
        },
      },
    },
  },
}
```

## # Allowlist by User ID (mais seguro)

```json5
{
  channels: {
    twitch: {
      accounts: {
        default: {
          allowFrom: ["123456789", "987654321"],
        },
      },
    },
  },
}
```

## # Lista combinada + papéis

Usuários em`allowFrom`bypass role checkes:

```json5
{
  channels: {
    twitch: {
      accounts: {
        default: {
          allowFrom: ["123456789"],
          allowedRoles: ["moderator"],
        },
      },
    },
  },
}
```

Desactivar a exigência @mention

Por padrão,`requireMention`é`true`. Para desativar e responder a todas as mensagens:

```json5
{
  channels: {
    twitch: {
      accounts: {
        default: {
          requireMention: false,
        },
      },
    },
  },
}
```

## Resolução de problemas

Primeiro, execute comandos de diagnóstico:

```bash
openclaw doctor
openclaw channels status --probe
```

O Bot não responde às mensagens

** Verificar o controle de acesso:** Preparar temporariamente`allowedRoles: ["all"]`para testar.

** Verifique se o bot está no canal:** O bot deve juntar-se ao canal especificado em`channel`.

### Questões do Token

**"Falhou em conectar" ou erros de autenticação:**

- Verificar`accessToken`é o valor do token de acesso OAuth (tipicamente começa com o prefixo`oauth:`
- Código`chat:read`e`chat:write`- Se usar a atualização token, verificar`clientSecret`e`refreshToken`

O toque de atualização não está a funcionar

** Verifique os registros para atualizar eventos:**

```
Using env token source for mybot
Access token refreshed for user 123456 (expires in 14400s)
```

Se você ver "token update desactivado (sem token de atualização)":

- Assegurar que o`clientSecret`é fornecido
- Assegurar que o`refreshToken`é fornecido

Configuração

** Configuração da conta: **

-`username`- Nome de utilizador Bot
-`accessToken`- Ficha de acesso à autorização com`chat:read`e`chat:write`-`clientId`- Twitch ID do cliente (de Token Generator ou seu aplicativo)
-`channel`- Canal para entrar (necessário)
-`enabled`- Activar esta conta (por omissão:`true`
-`clientSecret`- Opcional: Para atualização automática do token
-`refreshToken`- Opcional: Para atualização automática do token
-`accessToken`0 - Token expira em segundos
-`accessToken`1 - Indicador de hora obtido
-`accessToken`2 - Lista de permissões de identificação do utilizador
-`accessToken`3 - Controlo de acesso baseado no papel `accessToken`4)
-`accessToken`5 - Requer @mention (padrão:`accessToken`6)

** Opções do fornecedor:**

-`channels.twitch.enabled`- Activar/desactivar a inicialização do canal
-`channels.twitch.username`- Nome de utilizador do Bot (configuração simplificada de uma conta única)
-`channels.twitch.accessToken`- Token de acesso OAuth (configuração simplificada de uma conta única)
-`channels.twitch.clientId`- Twitch Client ID (configuração simplificada de uma conta única)
-`channels.twitch.channel`- Canal para entrar (configuração simplificada de uma conta única)
-`channels.twitch.accounts.<accountName>`- Configuração multiconta (todos os campos de conta acima)

Exemplo completo:

```json5
{
  channels: {
    twitch: {
      enabled: true,
      username: "openclaw",
      accessToken: "oauth:abc123...",
      clientId: "xyz789...",
      channel: "vevisk",
      clientSecret: "secret123...",
      refreshToken: "refresh456...",
      allowFrom: ["123456789"],
      allowedRoles: ["moderator", "vip"],
      accounts: {
        default: {
          username: "mybot",
          accessToken: "oauth:abc123...",
          clientId: "xyz789...",
          channel: "your_channel",
          enabled: true,
          clientSecret: "secret123...",
          refreshToken: "refresh456...",
          expiresIn: 14400,
          obtainmentTimestamp: 1706092800000,
          allowFrom: ["123456789", "987654321"],
          allowedRoles: ["moderator"],
        },
      },
    },
  },
}
```

## Acções da ferramenta

O agente pode chamar`twitch`com ação:

-`send`- Enviar mensagem para um canal

Exemplo:

```json5
{
  action: "twitch",
  params: {
    message: "Hello Twitch!",
    to: "#mychannel",
  },
}
```

## Segurança & operações

- **Toques de tratamento como senhas** - Nunca commit tokens para git
- **Use atualização automática do token** para bots de longa duração
- **Use listas de permissões de ID de usuário** em vez de nomes de usuário para controle de acesso
- **Monitor logs** para eventos de atualização token e status de conexão
- ** Tokens de cobre minimamente ** - Só solicitar`chat:read`e`chat:write`- ** Se preso**: Reinicie o gateway após confirmar que nenhum outro processo possui a sessão

## Limites

- **500 caracteres** por mensagem (auto-colhida em limites de palavras)
- O Markdown é despojado antes de ser cortado
- Sem limitação de taxa (usa os limites de taxa incorporados do Twitch)
