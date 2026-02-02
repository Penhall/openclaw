---
summary: "Inbound channel location parsing (Telegram + WhatsApp) and context fields"
read_when:
  - Adding or modifying channel location parsing
  - Using location context fields in agent prompts or tools
---

Localização do canal a analisar

OpenClaw normaliza locais compartilhados de canais de chat em:

- texto legível pelo homem, anexado ao corpo de entrada, e
- campos estruturados na carga útil do contexto de resposta automática.

Atualmente suportado:

- **Telegrama** (pontos de localização + locais + locais ao vivo)
- ** WhatsApp** (locationMessage + liveLocalizationMessage)
- **Matrix** `m.location`com`geo_uri`

## Formatação de texto

Os locais são renderizados como linhas amigáveis sem parênteses:

- Pin:
-`📍 48.858844, 2.294351 ±12m`- Lugar com nome:
-`📍 Eiffel Tower — Champ de Mars, Paris (48.858844, 2.294351 ±12m)`- Partilha ao vivo:
-`🛰 Live location: 48.858844, 2.294351 ±12m`

Se o canal incluir uma legenda/comentário, é adicionado na linha seguinte:

```
📍 48.858844, 2.294351 ±12m
Meet here
```

## Campos de contexto

Quando um local está presente, estes campos são adicionados ao`ctx`:

-`LocationLat`(número)
-`LocationLon`(número)
-`LocationAccuracy`(número, metros; opcional)
-`LocationName`(texto; opcional)
-`LocationAddress`(texto; opcional)
-`LocationSource``pin | place | live`
-`LocationIsLive`(booleano)

## Notas de canal

- **Telegrama**: mapas de locais para`LocationName/LocationAddress`; locais ao vivo usam`live_period`.
- ** WhatsApp**:`locationMessage.comment`e`liveLocationMessage.caption`são anexados como a linha de legenda.
- **Matrix**:`geo_uri`é analisado como uma localização de pino; altitude é ignorada e`LocationIsLive`é sempre falsa.
