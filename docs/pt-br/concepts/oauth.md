---
summary: "OAuth in OpenClaw: token exchange, storage, and multi-account patterns"
read_when:
  - You want to understand OpenClaw OAuth end-to-end
  - You hit token invalidation / logout issues
  - You want setup-token or OAuth auth flows
  - You want multiple accounts or profile routing
---

# OAuth

OpenClaw suporta "assinatura auth" via OAuth para provedores que o oferecem (nomeadamente **OpenAI Codex (ChatGPT OAuth)**). Para assinaturas antrópicas, use o fluxo **setup-token**. Esta página explica:

- como funciona a troca OAuth ** token ** (PKCE)
- onde as fichas são ** armazenadas ** (e porquê)
- como lidar com **contas múltiplas** (perfis + sobreposições por sessão)

O OpenClaw também suporta plugins ** que enviam o seu próprio OAuth ou API-key
flui. Execute-os através de:

```bash
openclaw models auth login --provider <id>
```

## A pia do símbolo (por que existe)

Os provedores de OAuth geralmente mentam um **novo token de atualização** durante os fluxos de login/refresh. Alguns provedores (ou clientes OAuth) podem invalidar tokens de atualização antigos quando um novo é emitido para o mesmo usuário/app.

Sintoma prático:

- você faz login via OpenClaw  and  via Claude Code / Codex CLI → um deles aleatoriamente fica “logged out” mais tarde

Para reduzir isso, OpenClaw trata`auth-profiles.json`como um lavatório ** token**:

- o tempo de execução lê credenciais de ** um lugar**
- podemos manter vários perfis e roteá-los deterministicamente

## Armazenamento (onde as fichas vivem)

Os segredos são guardados ** por agente**:

- Perfis de autenticação (chaves OAuth + API):`~/.openclaw/agents/<agentId>/agent/auth-profiles.json`- Cache Runtime (gerido automaticamente; não edite):`~/.openclaw/agents/<agentId>/agent/auth.json`

Arquivo só de importação legado (ainda suportado, mas não a loja principal):

-`~/.openclaw/credentials/oauth.json`(importado para o`auth-profiles.json`na primeira utilização)

Todos os acima também respeito`$OPENCLAW_STATE_DIR`(state dir sobreposição). Referência completa: [/porta/configuração]/gateway/configuration#auth-storage-oauth--api-keys

## Token de configuração antrópica (autorização de inscrição)

Executar`claude setup-token`em qualquer máquina, em seguida, colá-lo em OpenClaw:

```bash
openclaw models auth setup-token --provider anthropic
```

Se você gerou o token em outro lugar, cole-o manualmente:

```bash
openclaw models auth paste-token --provider anthropic
```

Verificar:

```bash
openclaw models status
```

## OAuth troca (como funciona o login)

Os fluxos de login interativos do OpenClaw são implementados em`@mariozechner/pi-ai`e conectados aos assistentes/comandos.

## # Antropic (Claude Pro/Max) configure-token

Forma de fluxo:

1. executar`claude setup-token`2. colar o token em OpenClaw
3. armazenar como um perfil de autenticação token (sem atualização)

O caminho do assistente é`openclaw onboard`→ auth choice`setup-token`(Anthropic).

## # Codex OpenAI (ChatGPT OAuth)

Forma de fluxo (PKCE):

1. gerar verificador/desafio PKCE +`state`aleatório
2.`https://auth.openai.com/oauth/authorize?...`aberto
3. tentar capturar callback em`http://127.0.0.1:1455/auth/callback`4. se callback não pode vincular (ou você é remoto / sem cabeça), colar o URL de redirecionamento / código
5. Intercâmbio no`https://auth.openai.com/oauth/token`6. extrair`accountId`do token de acesso e armazenar`{ access, refresh, expires, accountId }`

Wizard path is`openclaw onboard`→ auth choice`openai-codex`.

## Atualizar + expirar

Os perfis guardam uma marca`expires`.

Em tempo de execução:

- se`expires`estiver no futuro → use o token de acesso armazenado
- se expirado → atualizar (sob um bloqueio de arquivo) e substituir as credenciais armazenadas

O fluxo de atualização é automático; você geralmente não precisa gerenciar tokens manualmente.

## Contas múltiplas (perfis) + roteamento

Dois padrões:

### 1) Preferido: agentes separados

Se você quiser que “pessoal” e “trabalho” nunca interaja, use agentes isolados (sessões separadas + credenciais + espaço de trabalho):

```bash
openclaw agents add work
openclaw agents add personal
```

Em seguida, configure auth per-agent (wizard) e route chats para o agente certo.

### 2) Avançado: vários perfis em um agente

`auth-profiles.json`suporta vários IDs de perfil para o mesmo provedor.

Escolha qual perfil é usado:

- globalmente através da ordem de configuração `auth.order`
- por sessão via`/model ...@<profileId>`

Exemplo (sobreposição da sessão):

-`/model Opus@anthropic:work`

Como ver quais IDs de perfil existem:

-`openclaw channels list --json`(mostra`auth[]`

Documentos relacionados:

- [/conceitos/modelo-fracasso] /concepts/model-failover (rotação + regras de arrefecimento)
- [/tools/slash-comandos] /tools/slash-commands (superfície de comando)
