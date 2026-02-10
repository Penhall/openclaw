---
summary: "Telegram allowlist hardening: prefix + whitespace normalization"
read_when:
  - Reviewing historical Telegram allowlist changes
---

# Telegram Allowlist Endurecimento

**Data**: 2026-01-05
** Status**: Completo
**PR**: #216

## Resumo

Telegram allowlists agora aceitam prefixos`telegram:`e`tg:`de forma insensível e toleram
espaço em branco acidental. Isto alinha as verificações de lista de allowlist com a normalização de envio de saída.

## O que mudou

- Os prefixos`telegram:`e`tg:`são tratados da mesma forma (sensível ao caso).
- Os itens da lista de permissões são aparados; os itens vazios são ignorados.

## Exemplos

Todos estes são aceitos para o mesmo ID:

-`telegram:123456`-`TG:123456`-`tg:123456`

## Porque importa

Copiar/colar de logs ou IDs de bate-papo muitas vezes inclui prefixos e espaço em branco. Normalização evita
falsos negativos ao decidir se responder em DM ou grupos.

## Docs relacionados

- [Conversas em grupo] /concepts/groups
- [Oferta de Telegrama] /channels/telegram
