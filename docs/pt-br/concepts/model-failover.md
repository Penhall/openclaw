---
summary: "How OpenClaw rotates auth profiles and falls back across models"
read_when:
  - Diagnosing auth profile rotation, cooldowns, or model fallback behavior
  - Updating failover rules for auth profiles or models
---

Modelo failover

Openclaw lida com falhas em duas etapas:

1. **Rotação de perfil de autenticação** dentro do provedor atual.
2. **Modelo backback** para o próximo modelo em <<CODE0>>.

Este documento explica as regras de execução e os dados que os apoiam.

# # Armazenamento de autenticação (chaves + OAuth)

OpenClaw usa **auth profiles** para chaves API e tokens OAuth.

- Os segredos vivem em <<CODE0>> (legado: <<CODE1>>).
- Config <<CODE2>> / <<CODE3> são **metadados + roteamento apenas** (sem segredos).
- Ficheiro OAuth apenas para importação legativa: <<CODE4>> (importado para <<CODE5>> na primeira utilização).

Mais detalhes: [/conceitos/auth](<<<LINK0>>)

Tipos de credenciais:

- <<CODE0>> → <<CODE1>>>
- <<CODE2>> → <<CODE3>> (+ <<CODE4>>/<<CODE5> para alguns prestadores)

# # Identidades de perfil

Os logins do OAuth criam perfis distintos para que várias contas possam coexistir.

- Padrão: <<CODE0>> quando não há e-mail disponível.
- OAuth com e- mail: <<CODE1>> (por exemplo <<CODE2>>>).

Os perfis vivem em <<CODE0>> <<CODE1>>.

# # Ordem de rotação

Quando um provedor tem vários perfis, o OpenClaw escolhe uma ordem como esta:

1. **Configuração explícita**: <<CODE0>> (se definido).
2. **Perfis configurados**: <<CODE1> filtrados pelo provedor.
3. **Perfis armazenados**: entradas em <<CODE2>> para o provedor.

Se nenhuma ordem explícita for configurada, o OpenClaw usa uma ordem round-robin:

- ** Chave primária:** Tipo de perfil (**OAuth before API keys**).
- **Chave secundária:** <<CODE0>> (primeiro mais antigo, dentro de cada tipo).
- **Perfis cooldown/desabled** são movidos para o fim, ordenados pela expiração mais rápida.

## # Fissura da sessão (friendly cache)

OpenClaw **pina o perfil de autenticação escolhido por sessão** para manter caches de provedor aquecidos.
Ele faz ** not** girar em cada pedido. O perfil preso é reutilizado até:

- a sessão é reiniciada (<<<CODE0>/ <HTML1>>>>)
- uma compactação completa (incrementos de contagem de compactação)
- o perfil está em arrefecimento/desactivado

Seleção manual via <<CODE0>> define uma sobreposição do usuário** para essa sessão
e não é auto-rotado até que uma nova sessão comece.

Perfis montados automaticamente (selecionados pelo roteador de sessão) são tratados como uma **preferência**:
eles são tentados primeiro, mas OpenClaw pode girar para outro perfil em limites de taxa/tempo limite.
Perfis marcados pelo utilizador ficam bloqueados nesse perfil; se falhar e se o modelo falhar
são configurados, OpenClaw move para o próximo modelo em vez de mudar perfis.

# # # Porque OAuth pode "parece perdido"

Se você tiver tanto um perfil OAuth quanto um perfil de chave de API para o mesmo provedor, o round-robin pode alternar entre eles através de mensagens, a menos que esteja preso. Para forçar um único perfil:

- Pin com <<CODE0>>, ou
- Use uma sobreposição por sessão via <<CODE1> com uma sobreposição de perfil (quando suportada pela sua superfície UI/chat).

# # Refrigeração

Quando um perfil falha devido a erros de auth/rate-limit (ou um tempo limite que parece
como limite de taxa), OpenClaw marca-lo em arrefecimento e move-se para o próximo perfil.
Erros de formato/invalid-request (por exemplo Cloud Code Assist tool call ID
as falhas de validação) são tratadas como failover-worthy e usam os mesmos refrigeradores.

Cooldowns usam backoff exponencial:

- 1 minuto
- 5 minutos
- 25 minutos
- 1 hora (cap)

O estado é armazenado em <<CODE0>> em <<CODE1>>:

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

# # A facturação desactiva

As falhas de faturamento/crédito (por exemplo, “créditos insuficientes” / “equilíbrio de crédito muito baixo”) são tratadas como failover-worthy, mas geralmente não são transitórios. Em vez de um curto arrefecer, OpenClaw marca o perfil como ** desactivado** (com um retrocesso mais longo) e gira para o próximo perfil/fornecedor.

O estado é armazenado em <<CODE0>>:

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

# # Modelo de recuo

Se todos os perfis de um provedor falharem, o OpenClaw irá para o próximo modelo
<<CODE0>>. Isto aplica-se a falhas de autenticação, limites de taxa e
timeouts que esgotaram a rotação do perfil (outros erros não adiantam o retorno).

Quando uma execução começa com uma sobreposição do modelo (ganchos ou CLI), as falhas ainda terminam em
<<CODE0>> após tentar qualquer recurso configurado.

Configuração relacionada

Ver [Configuração do portal](<<<LINK0>>>) para:

- <<CODE0>>/ <<CODE1>>
- <<CODE2>>/ <<CODE3>>
- <<CODE4>>/ <<CODE5>>
- <<CODE6>>/ <<CODE7>>
- <<CODE8>> roteamento

Veja [Modelos](<<<LINK0>>) para a seleção mais ampla do modelo e visão geral de retrocesso.
