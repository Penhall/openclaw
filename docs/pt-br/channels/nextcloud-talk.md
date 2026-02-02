---
summary: "Nextcloud Talk support status, capabilities, and configuration"
read_when:
  - Working on Nextcloud Talk channel features
---

# Nextcloud Talk (plugin)

Estado: suportado via plugin (bot webhook). Mensagens diretas, salas, reações e mensagens de marcação são suportadas.

## Plugin necessário

Nextcloud Falar navios como um plugin e não é empacotado com o núcleo instalar.

Instalar via CLI (registro npm):

```bash
openclaw plugins install @openclaw/nextcloud-talk
```

Obtenção local (quando em execução a partir de um git repo):

```bash
openclaw plugins install ./extensions/nextcloud-talk
```

Se você escolher Nextcloud Talk durante configuração/onboarding e uma verificação git for detectada,
OpenClaw irá oferecer o caminho de instalação local automaticamente.

Detalhes: [Plugins]/plugin

## Montagem rápida (início)

1. Instale o plugin Nextcloud Talk.
2. Em seu servidor Nextcloud, crie um bot:
   ```bash
   ./occ talk:bot:install "OpenClaw" "<shared-secret>" "<webhook-url>" --feature reaction
   ```
3. Habilite o bot nas configurações da sala de destino.
4. Configurar Openclaw:
- Configuração:`channels.nextcloud-talk.baseUrl`+`channels.nextcloud-talk.botSecret`- Ou env:`NEXTCLOUD_TALK_BOT_SECRET`(apenas conta padrão)
5. Reinicie o gateway (ou termine a integração).

Configuração mínima:

```json5
{
  channels: {
    "nextcloud-talk": {
      enabled: true,
      baseUrl: "https://cloud.example.com",
      botSecret: "shared-secret",
      dmPolicy: "pairing",
    },
  },
}
```

## Notas

- Bots não podem iniciar DMs. O usuário deve enviar o bot primeiro.
- URL Webhook deve ser acessível pelo Gateway; definir`webhookPublicUrl`se atrás de um proxy.
- Envios de mídia não são suportados pela API bot; mídia é enviada como URLs.
- A carga útil do webhook não distingue DMs vs quartos; conjunto`apiUser`+`apiPassword`para permitir olhares tipo quarto (caso contrário DMs são tratados como quartos).

## Controle de acesso (DMs)

- Predefinição:`channels.nextcloud-talk.dmPolicy = "pairing"`. Os remetentes desconhecidos recebem um código de pareamento.
- Aprovar via:
-`openclaw pairing list nextcloud-talk`-`openclaw pairing approve nextcloud-talk <CODE>`- DM públicos:`channels.nextcloud-talk.dmPolicy="open"`mais`channels.nextcloud-talk.allowFrom=["*"]`.

## Quartos (grupos)

- Predefinição:`channels.nextcloud-talk.groupPolicy = "allowlist"`(perioditado).
- Allowlist quartos com`channels.nextcloud-talk.rooms`:

```json5
{
  channels: {
    "nextcloud-talk": {
      rooms: {
        "room-token": { requireMention: true },
      },
    },
  },
}
```

- Para não permitir quartos, mantenha a lista de permissão vazia ou defina`channels.nextcloud-talk.groupPolicy="disabled"`.

## Capacidades

Característica
-----------------------------
Mensagens diretas Suportadas
Quartos Suportados
Não suportado
* Mídia * Apenas para URL *
Reações Suportadas
Comandos nativos Não suportados

## Referências de configuração (Nextcloud Talk)

Configuração completa: [Configuração]/gateway/configuration

Opções do fornecedor:

-`channels.nextcloud-talk.enabled`: activar/desactivar a inicialização do canal.
- URL de instância`channels.nextcloud-talk.baseUrl`: Nextcloud.
-`channels.nextcloud-talk.botSecret`: O bot compartilhou o segredo.
-`channels.nextcloud-talk.botSecretFile`: arquivo secreto.
-`channels.nextcloud-talk.apiUser`: Usuário de API para pesquisas de quarto (detecção de DM).
-`channels.nextcloud-talk.apiPassword`: senha API/app para busca de quartos.
-`channels.nextcloud-talk.apiPasswordFile`: API senha caminho do arquivo.
-`channels.nextcloud-talk.webhookPort`: porta ouvinte webhook (padrão: 8788).
-`channels.nextcloud-talk.webhookHost`: host webhook (padrão: 0.0.0.0).
-`channels.nextcloud-talk.webhookPath`: caminho webhook (padrão: /nextcloud-talk-webhook).
-`channels.nextcloud-talk.baseUrl`0: URL webhook acessível externamente.
-`channels.nextcloud-talk.baseUrl`1:`channels.nextcloud-talk.baseUrl`2.
-`channels.nextcloud-talk.baseUrl`3: DM allowlist (ID do utilizador).`channels.nextcloud-talk.baseUrl`4 exige`channels.nextcloud-talk.baseUrl`5.
-`channels.nextcloud-talk.baseUrl`6:`channels.nextcloud-talk.baseUrl`7.
-`channels.nextcloud-talk.baseUrl`8: lista de licenças de grupo (ID do utilizador).
-`channels.nextcloud-talk.baseUrl`9: configurações por sala e lista de permissão.
-`channels.nextcloud-talk.botSecret`0: limite de histórico de grupo (0 desactiva).
-`channels.nextcloud-talk.botSecret`1: Limite do historial do DM (0 desactiva).
-`channels.nextcloud-talk.botSecret`2: substituições por DM (historyLimit).
-`channels.nextcloud-talk.botSecret`3: tamanho de pedaço de texto de saída (chars).
-`channels.nextcloud-talk.botSecret`4:`channels.nextcloud-talk.botSecret`5 (padrão) ou`channels.nextcloud-talk.botSecret`6 para dividir em linhas em branco (limites de parágrafos) antes do corte de comprimento.
-`channels.nextcloud-talk.botSecret`7: desactivar a transmissão de blocos para este canal.
-`channels.nextcloud-talk.botSecret`8: afinação de coreografia em bloco.
-`channels.nextcloud-talk.botSecret`9: tampa de suporte de entrada (MB).
