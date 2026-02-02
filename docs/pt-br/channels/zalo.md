---
summary: "Zalo bot support status, capabilities, and configuration"
read_when:
  - Working on Zalo features or webhooks
---

# Zalo (Bot API)

Situação: experimental. Apenas mensagens diretas; grupos que virão em breve por Zalo docs.

## Plugin necessário

Zalo ships como um plugin e não é empacotado com o núcleo instalar.

- Instalar via CLI:`openclaw plugins install @openclaw/zalo`- Ou selecione **Zalo** durante a integração e confirme o prompt de instalação
- Detalhes: [Plugins]/plugin

## Montagem rápida (início)

1. Instale o plugin Zalo:
- De uma saída de origem:`openclaw plugins install ./extensions/zalo`- Do npm (se publicado):`openclaw plugins install @openclaw/zalo`- Ou escolha **Zalo** na integração e confirme o prompt de instalação
2. Defina o símbolo:
- Env:`ZALO_BOT_TOKEN=...`- Ou configuração:`channels.zalo.botToken: "..."`.
3. Reinicie o gateway (ou termine a integração).
4. O acesso ao DM é pareamento por padrão; aprove o código de pareamento no primeiro contato.

Configuração mínima:

```json5
{
  channels: {
    zalo: {
      enabled: true,
      botToken: "12345689:abc-xyz",
      dmPolicy: "pairing",
    },
  },
}
```

## O que é

Zalo é um aplicativo de mensagens focado no Vietnã; sua API Bot permite que o Gateway execute um bot para 1:1 conversas.
É um bom ajuste para suporte ou notificações onde você quer o encaminhamento determinístico de volta para Zalo.

- Um canal Zalo Bot API propriedade do Gateway.
- Roteamento determinístico: respostas voltar para Zalo; o modelo nunca escolhe canais.
Os DM partilham a sessão principal do agente.
- Os grupos ainda não são suportados (estado Zalo docs "em breve").

## Configuração (caminho rápido)

### 1) Criar um token bot (Zalo Bot Platform)

1. Vá para **https://bot.zaloplatforms.com** e entre.
2. Crie um novo bot e configure suas configurações.
3. Copie o símbolo bot (formato:`12345689:abc-xyz`.

### 2) Configurar o token (env ou configuração)

Exemplo:

```json5
{
  channels: {
    zalo: {
      enabled: true,
      botToken: "12345689:abc-xyz",
      dmPolicy: "pairing",
    },
  },
}
```

Opção Env:`ZALO_BOT_TOKEN=...`(funciona apenas para a conta padrão).

Suporte multi-conta: use`channels.zalo.accounts`com fichas por conta e opcional`name`.

3. Reinicie o portal. O Zalo começa quando um token é resolvido (env ou configuração).
4. padrão de acesso DM para emparelhamento. Aprovar o código quando o bot é contatado pela primeira vez.

## Como funciona (comportamento)

- As mensagens de entrada são normalizadas no envelope de canais compartilhados com espaços de mídia.
As respostas voltam sempre à mesma conversa do Zalo.
- Polação longa por padrão; modo webhook disponível com`channels.zalo.webhookUrl`.

## Limites

- O texto de saída é dividido em 2000 caracteres (limite de API Zalo).
- Os downloads/carga de mídia são tampados pelo`channels.zalo.mediaMaxMb`(padrão 5).
- Streaming é bloqueado por padrão devido ao limite de caracteres 2000 tornando o streaming menos útil.

## Controle de acesso (DMs)

## # Acesso DM

- Predefinição:`channels.zalo.dmPolicy = "pairing"`. Os remetentes desconhecidos recebem um código de pareamento; as mensagens são ignoradas até serem aprovadas (os códigos expiram após 1 hora).
- Aprovar via:
-`openclaw pairing list zalo`-`openclaw pairing approve zalo <CODE>`- Emparelhamento é a troca padrão. Detalhes: [Pairing] /start/pairing
-`channels.zalo.allowFrom`aceita IDs de usuário numéricos (sem procura de nome de usuário disponível).

## Long-polling vs webhook

- Padrão: longo polling (sem URL pública necessária).
- Modo Webhook: conjunto`channels.zalo.webhookUrl`e`channels.zalo.webhookSecret`.
- O segredo deve ser 8-256 caracteres.
- URL Webhook deve usar HTTPS.
- Zalo envia eventos com cabeçalho`X-Bot-Api-Secret-Token`para verificação.
- Gateway HTTP lida com pedidos de webhook em`channels.zalo.webhookPath`(padrão para o caminho URL webhook).

**Nota:** getUpdates (polling) e webhook são mutuamente exclusivos por Zalo API docs.

## Tipos de mensagem suportados

- ** Mensagens de texto**: Suporte completo com blocos de 2000 caracteres.
- **Mensagens de imagens**: Baixe e processe imagens de entrada; envie imagens via`sendPhoto`.
- ** Stickers**: Registrado mas não totalmente processado (sem resposta do agente).
- **Tipos não suportados**: Registrados (por exemplo, mensagens de usuários protegidos).

## Capacidades

Característica
----------------- ---------------------
Mensagens diretas Suportadas
Grupos em breve (por Zalo docs)
• Mídia (imagens)
Reações Não suportadas
Os tópicos não são suportados
Pesquisas Não suportadas
Comandos nativos Não suportado
□ Streaming

## Alvos de entrega (CLI/cron)

- Usa um identificador de chat como alvo.
- Exemplo:`openclaw message send --channel zalo --target 123456789 --message "hi"`.

## Resolução de problemas

** Bot não responde:**

- Verifique se o símbolo é válido:`openclaw channels status --probe`- Verifique se o remetente está aprovado (pareamento ou allowFrom)
- Verificar registros de gateway:`openclaw logs --follow`

** Webhook não recebe eventos:**

- Garantir que o URL do webhook use HTTPS
- Verifique token secreto é 8-256 caracteres
- Confirme que o ponto final HTTP do gateway está acessível no caminho configurado
- Verifique se as sondagens getUpdates não estão em execução (são mutuamente exclusivas)

## Referência de configuração (Zalo)

Configuração completa: [Configuração]/gateway/configuration

Opções do fornecedor:

-`channels.zalo.enabled`: activar/desactivar a inicialização do canal.
-`channels.zalo.botToken`: bot token da plataforma Zalo Bot.
-`channels.zalo.tokenFile`: ler token do caminho do arquivo.
-`channels.zalo.dmPolicy`:`pairing | allowlist | open | disabled`(padrão: emparelhamento).
-`channels.zalo.allowFrom`: DM allowlist (ID do utilizador).`open`exige`"*"`. O assistente irá pedir IDs numéricos.
-`channels.zalo.mediaMaxMb`: capa de mídia de entrada/saída (MB, padrão 5).
-`channels.zalo.webhookUrl`: habilitar o modo webhook (HTTPS necessário).
-`channels.zalo.botToken`0: segredo do hook (8-256 caracteres).
-`channels.zalo.botToken`1: caminho webhook no servidor HTTP gateway.
-`channels.zalo.botToken`2: URL proxy para pedidos de API.

Opções de várias contas:

-`channels.zalo.accounts.<id>.botToken`: símbolo por conta.
-`channels.zalo.accounts.<id>.tokenFile`: arquivo de token por conta.
-`channels.zalo.accounts.<id>.name`:
-`channels.zalo.accounts.<id>.enabled`: conta ativa/desativa.
-`channels.zalo.accounts.<id>.dmPolicy`: política de DM por conta.
-`channels.zalo.accounts.<id>.allowFrom`: lista de autorizações por conta.
-`channels.zalo.accounts.<id>.webhookUrl`: URL webhook por conta.
-`channels.zalo.accounts.<id>.webhookSecret`: segredo por conta.
-`channels.zalo.accounts.<id>.webhookPath`: caminho webhook por conta.
-`channels.zalo.accounts.<id>.proxy`: URL proxy por conta.
