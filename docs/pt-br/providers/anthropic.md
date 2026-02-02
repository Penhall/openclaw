---
summary: "Use Anthropic Claude via API keys or setup-token in OpenClaw"
read_when:
  - You want to use Anthropic models in OpenClaw
  - You want setup-token instead of API keys
---

# Antrópico (Claude)

Anthropic constrói a família de modelos **Claude** e fornece acesso através de uma API.
No OpenClaw você pode autenticar com uma chave API ou uma **setup-token**.

# # Opção A: Chave de API antrópica

**Melhor para:** acesso padrão à API e faturamento baseado no uso.
Crie sua chave API na Consola Antrópica.

Configuração do CLI

```bash
openclaw onboard
# choose: Anthropic API key

# or non-interactive
openclaw onboard --anthropic-api-key "$ANTHROPIC_API_KEY"
```

### Config snippet

```json5
{
  env: { ANTHROPIC_API_KEY: "sk-ant-..." },
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-5" } } },
}
```

# # Caching rápido (A API antrópica)

O OpenClaw não ** substitui o cache padrão TTL da Anthropic a menos que você o defina.
Esta é **API-only**; assinatura auth não honra configurações TTL.

Para definir o TTL por modelo, utilizar <<CODE0> no modelo <<CODE1>:

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-5": {
          params: { cacheControlTtl: "5m" }, // or "1h"
        },
      },
    },
  },
}
```

OpenClaw inclui a bandeira beta <<CODE0> para API antrópica
requests; mantenha-o se você substituir os cabeçalhos do provedor (veja [/gateway/configuration](/gateway/configuration)).

# # Opção B: Claude setup-token

** Melhor para:** usando sua assinatura Claude.

# # Onde arranjar uma ficha

As configurações são criadas pelo código **Claude CLI**, não o Console Antrópico. Você pode executar isso em ** qualquer máquina**:

```bash
claude setup-token
```

Colar o token no OpenClaw (wizard: **Token antrópico (paste setup-token)**), ou executá-lo na máquina gateway:

```bash
openclaw models auth setup-token --provider anthropic
```

Se você gerou o token em uma máquina diferente, cole-o:

```bash
openclaw models auth paste-token --provider anthropic
```

Configuração do CLI

```bash
# Paste a setup-token during onboarding
openclaw onboard --auth-choice setup-token
```

### Config snippet

```json5
{
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-5" } } },
}
```

# # Notas

- Gere a configuração com `claude setup-token` e cole-a, ou execute `openclaw models auth setup-token` no host gateway.
- Se você ver “OAuth token release failed ...” em uma assinatura Claude, reauth com uma configuração-token. Ver [/gateway/trubleshooting#oauth-token-refresh-failed-anthropic-claude-subscription](</gateway/troubleshooting#oauth-token-refresh-failed-anthropic-claude-subscription).
- Detalhes de autenticação + regras de reutilização estão em [/conceitos/outh] (</concepts/oauth).

# # Resolução de problemas

**401 erros / token subitamente inválidos**

- A assinatura Claude pode expirar ou ser revogada. Repetição `claude setup-token`
e colá-lo no host ** gateway**.
- Se o login Claude CLI vive em uma máquina diferente, use
<<CODE1> na máquina de gateway.

** Nenhuma chave de API encontrada para provedor "antrópico"**

- Auth é ** por agente **. Novos agentes não herdam as chaves do agente principal.
- Re-executar onboarding para esse agente, ou colar uma chave de configuração / API na
gateway host, então verifique com `openclaw models status`.

** Nenhuma credencial encontrada para perfil `anthropic:default`**

- Executar <<CODE0> para ver qual perfil de autenticação está activo.
- Re-executar onboarding, ou colar uma chave de configuração / API para esse perfil.

** Nenhum perfil de autenticação disponível (tudo em arrefecimento/indisponível)**

- Verificar `openclaw models status --json` para <<CODE1>.
- Adicione outro perfil Antrópico ou aguarde o resfriamento.

Mais: [/gateway/trubleshooting] (</gateway/troubleshooting) e [/help/faq] (</help/faq).
