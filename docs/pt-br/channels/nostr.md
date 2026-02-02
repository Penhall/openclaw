---
summary: "Nostr DM channel via NIP-04 encrypted messages"
read_when:
  - You want OpenClaw to receive DMs via Nostr
  - You're setting up decentralized messaging
---

# Nostr

** Status:** plugin opcional (desativado por padrão).

Nostr é um protocolo descentralizado para as redes sociais. Este canal permite que o OpenClaw receba e responda a mensagens diretas criptografadas (DMs) via NIP-04.

## Instalar (a pedido)

A bordo (recomendado)

- O assistente de onboarding `openclaw onboard` e`openclaw channels add`listam plugins de canais opcionais.
- Selecionar Nostr pede que você instale o plugin sob demanda.

Instalar por omissão:

- **Dev canal + git checkout disponível:** usa o caminho local do plugin.
- **Stable/Beta:** downloads do npm.

Você sempre pode substituir a escolha no prompt.

Instalação manual

```bash
openclaw plugins install @openclaw/nostr
```

Usar uma saída local (fluxos de trabalho de dev):

```bash
openclaw plugins install --link <path-to-openclaw>/extensions/nostr
```

Reinicie o Gateway após instalar ou habilitar plugins.

## Montagem rápida

1. Gerar um keypair Nostr (se necessário):

```bash
# Using nak
nak key generate
```

2. Adicionar à configuração:

```json
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}"
    }
  }
}
```

3. Exportar a chave:

```bash
export NOSTR_PRIVATE_KEY="nsec1..."
```

4. Reinicie o Portal.

## Referência de configuração

. . chave . . Tipo . . padrão . . Descrição .
-------------- ----------- ------------------------------------------ ----------------- ----------------------------------------------------
□`privateKey``privateKey`O`nsec`ou formato hex
•`relays`• string[] •`['wss://relay.damus.io', 'wss://nos.lol']`• URLs de transmissão (WebSocket)
•`dmPolicy`*`allowFrom`* string[] *`[]`*`enabled``enabled``true``true`O Activar/desactivar o canal`nsec`0`nsec`0`nsec`0`nsec`1`nsec`1`nsec`1

## Metadados de perfil

Os dados do perfil são publicados como um evento NIP-01`kind:0`. Você pode gerenciá-lo a partir da interface de controle (Canais -> Nostr -> Perfil) ou configurá-lo diretamente na configuração.

Exemplo:

```json
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "profile": {
        "name": "openclaw",
        "displayName": "OpenClaw",
        "about": "Personal assistant DM bot",
        "picture": "https://example.com/avatar.png",
        "banner": "https://example.com/banner.png",
        "website": "https://example.com",
        "nip05": "openclaw@example.com",
        "lud16": "openclaw@example.com"
      }
    }
  }
}
```

Notas:

- URLs de perfil devem usar`https://`.
- Importar de relés mescla campos e preserva substituições locais.

## Controle de acesso

## Políticas de DM

- ** paring** (padrão): remetentes desconhecidos recebem um código de pareamento.
- ** allowlist**: apenas os pubkeys em`allowFrom`podem DM.
- **aberto**: DM de entrada pública (exige`allowFrom: ["*"]`.
- ** Desactivado**: ignorar DMs de entrada.

## # Exemplo de lista de permissão

```json
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "dmPolicy": "allowlist",
      "allowFrom": ["npub1abc...", "npub1xyz..."]
    }
  }
}
```

## Formatos-chave

Formatos aceitos:

- ** Chave privada:**`nsec...`ou 64-char hex
- **Pubkeys `allowFrom`:**`npub...`ou hex

## Relés

Padrões:`relay.damus.io`e`nos.lol`.

```json
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "relays": ["wss://relay.damus.io", "wss://relay.primal.net", "wss://nostr.wine"]
    }
  }
}
```

Dicas:

- Use 2-3 relés para redundância.
- Evite muitos relés (latência, duplicação).
- Relés pagos podem melhorar a confiabilidade.
- Relés locais são bons para testes `ws://localhost:7777`.

## Apoio ao protocolo

□ NIP □ Status
------- ------------ -------- ----------------------------------------------------
O formato básico do evento + metadados do perfil
* NIP-04 * Suportado * DMs criptografados `kind:4` *
□ NIP-17 □ Planeado
* NIP-44 * Planeado * Criptografia versionada *

Teste

Retransmissão local

```bash
# Start strfry
docker run -p 7777:7777 ghcr.io/hoytech/strfry
```

```json
{
  "channels": {
    "nostr": {
      "privateKey": "${NOSTR_PRIVATE_KEY}",
      "relays": ["ws://localhost:7777"]
    }
  }
}
```

Teste manual

1. Note o bot pubkey (npub) de logs.
2. Abra um cliente Nostr (Damus, Amethyst, etc.).
3. DM o bot pubkey.
4. Verifique a resposta.

## Resolução de problemas

Não receber mensagens

- Verifique se a chave privada é válida.
- Garantir que URLs de relé são alcançáveis e usar`wss://`(ou`ws://`para local).
- Confirmar`enabled`não é`false`.
- Verifique os registos do portal para verificar os erros de ligação.

Não enviar respostas

- O retransmissor aceita as cartas.
- Verificar conectividade de saída.
- Cuidado com os limites da taxa de retransmissão.

## Duplicar respostas

- Espera-se que use vários relés.
- As mensagens são deduplicadas pelo ID do evento; apenas a primeira entrega desencadeia uma resposta.

## Segurança

- Nunca cometa chaves privadas.
- Use variáveis de ambiente para chaves.
- Considere`allowlist`para bots de produção.

## Limitações (MVP)

- Apenas mensagens directas (sem conversas em grupo).
- Nada de anexos à comunicação social.
- NIP-04 apenas (NIP-17 pacote de presente planeado).
