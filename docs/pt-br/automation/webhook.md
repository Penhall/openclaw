---
summary: "Webhook ingress for wake and isolated agent runs"
read_when:
  - Adding or changing webhook endpoints
  - Wiring external systems into OpenClaw
---

# Webhooks

Gateway pode expor um pequeno parâmetro HTTP webhook para gatilhos externos.

Activar

```json5
{
  hooks: {
    enabled: true,
    token: "shared-secret",
    path: "/hooks",
  },
}
```

Notas:

-`hooks.token`é exigido quando`hooks.enabled=true`.
-`hooks.path`defaults to`/hooks`.

## Auth

Cada pedido deve incluir o token gancho. Prefere cabeçalhos:

-`Authorization: Bearer <token>`(recomendado)
-`x-openclaw-token: <token>`-`?token=<token>`(depreciado; registra um aviso e será removido em uma liberação principal futura)

## Endpoints

## #`POST /hooks/wake`

Carga útil:

```json
{ "text": "System line", "mode": "now" }
```

-`text`**required** (string): A descrição do evento (por exemplo, "Novo e-mail recebido").
-`mode`opcional `now`ou`next-heartbeat`: Quer desencadeie um batimento cardíaco imediato (padrão`now` ou aguarde a próxima verificação periódica.

Efeito:

- Encaminha um evento de sistema para a sessão **main**
- Se`mode=now`, desencadeia um batimento cardíaco imediato

## #`POST /hooks/agent`

Carga útil:

```json
{
  "message": "Run this",
  "name": "Email",
  "sessionKey": "hook:email:msg-123",
  "wakeMode": "now",
  "deliver": true,
  "channel": "last",
  "to": "+15551234567",
  "model": "openai/gpt-5.2-mini",
  "thinking": "low",
  "timeoutSeconds": 120
}
```

-`message`**required** (string): O prompt ou mensagem para o agente processar.
-`name`opcional (texto): Nome legível para o gancho (por exemplo, "GitHub"), usado como prefixo em resumos de sessão.
-`sessionKey`opcional (texto): A chave usada para identificar a sessão do agente. O padrão é um`hook:<uuid>`aleatório. O uso de uma chave consistente permite uma conversação multi-volta dentro do contexto do gancho.
-`wakeMode`opcional `now`o`next-heartbeat`: Quer desencadeie um batimento cardíaco imediato (padrão`now` ou aguarde a próxima verificação periódica.
-`deliver`opcional (booleano): Se`true`, a resposta do agente será enviada para o canal de mensagens. Predefinição para`name`0. As respostas que são apenas agradecimentos cardíacos são automaticamente ignoradas.
-`name`1 opcional (texto): O canal de mensagens para entrega. Um de:`name`2,`name`3,`name`4,`name`5,`name`6,`name`7 (plugin),`name`8,`name`9,`sessionKey`0. Predefinição para`sessionKey`1.
-`sessionKey`2 opcional (string): Identificador do destinatário para o canal (por exemplo, número de telefone para WhatsApp/Sinal, ID de chat para Telegram, ID de canal para Discord/Slack/Mattermost (plugin), ID de conversação para MS Teams). O padrão é o último destinatário na sessão principal.
-`sessionKey`3 opcional (cadeia): sobreposição do modelo (por exemplo,`sessionKey`4 ou um apelido). Deve estar na lista de modelos permitidos se restrito.
-`sessionKey`5 opcional (corrente): sobreposição do nível de pensamento (por exemplo,`sessionKey`6,`sessionKey`7,`sessionKey`8).
-`sessionKey`9 opcional (número): Duração máxima do agente em segundos.

Efeito:

- Executa uma volta de agente** isolado (chave de sessão própria)
- Sempre posta um resumo na sessão **main**
- Se`wakeMode=now`, desencadeia um batimento cardíaco imediato

## #`POST /hooks/<name>`(mapeado)

Nomes de gancho personalizados são resolvidos via`hooks.mappings`(ver configuração). Um mapeamento pode
Transforme cargas arbitrárias em ações`wake`ou`agent`, com modelos opcionais ou
O código transforma-se.

Opções de mapeamento (síntese):

-`hooks.presets: ["gmail"]`permite o mapeamento integrado do Gmail.
-`hooks.mappings`permite definir`match`,`action`e modelos na configuração.
-`hooks.transformsDir`+`transform.module`carrega um módulo JS/TS para lógica personalizada.
- Use`match.source`para manter um endpoint genérico de ingestão (roteamento guiado por carga paga).
- As transformadas TS requerem um carregador TS (por exemplo,`bun`ou`tsx` ou o`.js`pré-compilado em tempo de execução.
- Definir`hooks.mappings`0 +`hooks.mappings`1/`hooks.mappings`2 para mapeamento das respostas de rota para uma superfície de bate-papo
`hooks.mappings`3 defaults to`hooks.mappings`4 e cai de volta para WhatsApp).
-`hooks.mappings`5 desativa o invólucro de segurança de conteúdo externo para esse gancho
(perigoso; apenas para fontes internas confiáveis).
-`hooks.mappings`6 escreve`hooks.mappings`7 config para`hooks.mappings`8.
Ver [Gmail Pub/Sub]/automation/gmail-pubsub para o fluxo completo do relógio do Gmail.

## Respostas

-`200`para`/hooks/wake`-`202`para`/hooks/agent`-`401`em caso de falha de autenticação
-`400`sobre carga útil inválida
-`413`sobre cargas úteis sobredimensionadas

## Exemplos

```bash
curl -X POST http://127.0.0.1:18789/hooks/wake \
  -H 'Authorization: Bearer SECRET' \
  -H 'Content-Type: application/json' \
  -d '{"text":"New email received","mode":"now"}'
```

```bash
curl -X POST http://127.0.0.1:18789/hooks/agent \
  -H 'x-openclaw-token: SECRET' \
  -H 'Content-Type: application/json' \
  -d '{"message":"Summarize inbox","name":"Email","wakeMode":"next-heartbeat"}'
```

## Usa um modelo diferente

Adicione`model`à carga útil do agente (ou mapeamento) para substituir o modelo para essa execução:

```bash
curl -X POST http://127.0.0.1:18789/hooks/agent \
  -H 'x-openclaw-token: SECRET' \
  -H 'Content-Type: application/json' \
  -d '{"message":"Summarize inbox","name":"Email","model":"openai/gpt-5.2-mini"}'
```

Se você aplicar`agents.defaults.models`, certifique-se de que o modelo de sobreposição está incluído lá.

```bash
curl -X POST http://127.0.0.1:18789/hooks/gmail \
  -H 'Authorization: Bearer SECRET' \
  -H 'Content-Type: application/json' \
  -d '{"source":"gmail","messages":[{"from":"Ada","subject":"Hello","snippet":"Hi"}]}'
```

## Segurança

- Mantenha os endpoints do gancho atrás de loopback, tailnet, ou proxy reverso confiável.
- Use um token de gancho dedicado; não reutilize os tokens de autenticação de gateway.
- Evite incluir cargas brutas sensíveis em logs webhook.
- Hook cargas são tratadas como não confiáveis e envolto com limites de segurança por padrão.
Se tiver de desactivar isto para um gancho específico, defina`allowUnsafeExternalContent: true`no mapeamento do gancho (perigoso).
