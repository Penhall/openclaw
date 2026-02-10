---
summary: "How OpenClaw rotates auth profiles and falls back across models"
read_when:
  - Diagnosing auth profile rotation, cooldowns, or model fallback behavior
  - Updating failover rules for auth profiles or models
---

Modelo failover

Openclaw lida com falhas em duas etapas:

1. **Rotação de perfil de autenticação** dentro do provedor atual.
2. **Modelo de retrocesso** para o próximo modelo em`agents.defaults.model.fallbacks`.

Este documento explica as regras de execução e os dados que os apoiam.

## Armazenamento de autenticação (chaves + OAuth)

OpenClaw usa **auth profiles** para chaves API e tokens OAuth.

- Os segredos vivem em`~/.openclaw/agents/<agentId>/agent/auth-profiles.json`(legacia:`~/.openclaw/agent/auth-profiles.json`.
- Config`auth.profiles`/`auth.order`são ** metadados + roteamento apenas** (sem segredos).
- Arquivo OAuth só para importação de legado:`~/.openclaw/credentials/oauth.json`(importado para`auth-profiles.json`na primeira utilização).

Mais detalhes: [/conceitos/outh]/concepts/oauth

Tipos de credenciais:

-`type: "api_key"`→`{ provider, key }`-`type: "oauth"`→`{ provider, access, refresh, expires, email? }`(+`projectId`/`enterpriseUrl`para alguns prestadores)

## Identidades de perfil

Os logins do OAuth criam perfis distintos para que várias contas possam coexistir.

- Padrão:`provider:default`quando não há e-mail disponível.
- OAut com e-mail:`provider:<email>`(por exemplo,`google-antigravity:user@gmail.com`.

Os perfis vivem em`~/.openclaw/agents/<agentId>/agent/auth-profiles.json`sob`profiles`.

## Ordem de rotação

Quando um provedor tem vários perfis, o OpenClaw escolhe uma ordem como esta:

1. **Explicit config**:`auth.order[provider]`(se definido).
2. **Perfis configurados**:`auth.profiles`filtrado pelo provedor.
3. **Perfis armazenados**: entradas em`auth-profiles.json`para o provedor.

Se nenhuma ordem explícita for configurada, o OpenClaw usa uma ordem round-robin:

- ** Chave primária:** Tipo de perfil (**OAuth before API keys**).
- ** Chave secundária:**`usageStats.lastUsed`(primeiro mais antigo, dentro de cada tipo).
- **Perfis cooldown/desabled** são movidos para o fim, ordenados pela expiração mais rápida.

## # Fissura da sessão (friendly cache)

OpenClaw **pina o perfil de autenticação escolhido por sessão** para manter caches de provedor aquecidos.
Ele faz ** not** girar em cada pedido. O perfil preso é reutilizado até:

- a sessão é reiniciada `/new`/`/reset`
- uma compactação completa (incrementos de contagem de compactação)
- o perfil está em arrefecimento/desactivado

Selecção manual via`/model …@<profileId>`define uma sobreposição do utilizador** para essa sessão
e não é auto-rotado até que uma nova sessão comece.

Perfis montados automaticamente (selecionados pelo roteador de sessão) são tratados como uma **preferência**:
eles são tentados primeiro, mas OpenClaw pode girar para outro perfil em limites de taxa/tempo limite.
Perfis marcados pelo utilizador ficam bloqueados nesse perfil; se falhar e se o modelo falhar
são configurados, OpenClaw move para o próximo modelo em vez de mudar perfis.

### Porque OAuth pode "parece perdido"

Se você tiver tanto um perfil OAuth quanto um perfil de chave de API para o mesmo provedor, o round-robin pode alternar entre eles através de mensagens, a menos que esteja preso. Para forçar um único perfil:

- Pino com`auth.order[provider] = ["provider:profileId"]`, ou
- Use uma sobreposição por sessão via`/model …`com uma sobreposição de perfil (quando suportada pela sua superfície UI/chat).

## Refrigeração

Quando um perfil falha devido a erros de auth/rate-limit (ou um tempo limite que parece
como limite de taxa), OpenClaw marca-lo em arrefecimento e move-se para o próximo perfil.
Erros de formato/invalid-request (por exemplo Cloud Code Assist tool call ID
as falhas de validação) são tratadas como failover-worthy e usam os mesmos refrigeradores.

Cooldowns usam backoff exponencial:

- 1 minuto
- 5 minutos
- 25 minutos
- 1 hora (cap)

O Estado está armazenado em`auth-profiles.json`ao abrigo do`usageStats`:

```json
{
  "usageStats": {
    "provider:profile": {
      "lastUsed": 1736160000000,
      "cooldownUntil": 1736160600000,
      "errorCount": 2
    }
  }
}
```

## A facturação desactiva

As falhas de faturamento/crédito (por exemplo, “créditos insuficientes” / “equilíbrio de crédito muito baixo”) são tratadas como failover-worthy, mas geralmente não são transitórios. Em vez de um curto arrefecer, OpenClaw marca o perfil como ** desactivado** (com um retrocesso mais longo) e gira para o próximo perfil/fornecedor.

O Estado está armazenado em`auth-profiles.json`:

```json
{
  "usageStats": {
    "provider:profile": {
      "disabledUntil": 1736178000000,
      "disabledReason": "billing"
    }
  }
}
```

Predefinição:

- Retirada de contas começa em **5 horas**, dobra por falha de faturamento, e tampas em **24 horas**.
- Contadores Backoff reset se o perfil não tiver falhado por **24 horas** (configurável).

## Modelo de recuo

Se todos os perfis de um provedor falharem, o OpenClaw irá para o próximo modelo`agents.defaults.model.fallbacks`. Isto aplica-se a falhas de autenticação, limites de taxa e
timeouts que esgotaram a rotação do perfil (outros erros não adiantam o retorno).

Quando uma execução começa com uma sobreposição do modelo (ganchos ou CLI), as falhas ainda terminam em`agents.defaults.model.primary`após tentar qualquer recurso configurado.

Configuração relacionada

Ver [Configuração do portal]/gateway/configuration para:

-`auth.profiles`/`auth.order`-`auth.cooldowns.billingBackoffHours`/`auth.cooldowns.billingBackoffHoursByProvider`-`auth.cooldowns.billingMaxHours`/`auth.cooldowns.failureWindowHours`-`agents.defaults.model.primary`/`agents.defaults.model.fallbacks`-`agents.defaults.imageModel`roteamento

Ver [Modelos]/concepts/models para a seleção mais ampla do modelo e visão geral de retrocesso.
