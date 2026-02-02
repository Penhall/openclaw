---
summary: "CLI reference for `openclaw devices` (device pairing + token rotation/revocation)"
read_when:
  - You are approving device pairing requests
  - You need to rotate or revoke device tokens
---

#`openclaw devices`

Gerenciar pedidos de emparelhamento de dispositivos e tokens de dispositivo.

## Comandos

## #`openclaw devices list`

Listar pedidos de pareamento pendentes e dispositivos pareados.

```
openclaw devices list
openclaw devices list --json
```

## #`openclaw devices approve <requestId>`

Aprovar um pedido de emparelhamento de dispositivos pendente.

```
openclaw devices approve <requestId>
```

## #`openclaw devices reject <requestId>`

Rejeitar uma solicitação de emparelhamento de dispositivos pendente.

```
openclaw devices reject <requestId>
```

## #`openclaw devices rotate --device <id> --role <role> [--scope <scope...>]`

Rodar um token de dispositivo para um papel específico (opcionalmente atualizando escopos).

```
openclaw devices rotate --device <deviceId> --role operator --scope operator.read --scope operator.write
```

## #`openclaw devices revoke --device <id> --role <role>`

Revogue um token de dispositivo para um papel específico.

```
openclaw devices revoke --device <deviceId> --role node
```

## Opções comuns

-`--url <url>`: Gateway WebSocket URL (padrão para`gateway.remote.url`quando configurado).
-`--token <token>`: Ficha da porta (se necessário).
-`--password <password>`: Senha do portal (autenticação de senha).
- Tempo limite de RCP.
-`--json`: Saída JSON (recomendada para scripting).

## Notas

- A rotação do token devolve um novo token (sensível). Trata-o como um segredo.
- Estes comandos requerem`operator.pairing`(ou`operator.admin`.
