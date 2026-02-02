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

# # A pia do símbolo (por que existe)

Os provedores de OAuth geralmente mentam um **novo token de atualização** durante os fluxos de login/refresh. Alguns provedores (ou clientes OAuth) podem invalidar tokens de atualização antigos quando um novo é emitido para o mesmo usuário/app.

Sintoma prático:

- você faz login via OpenClaw  and  via Claude Code / Codex CLI → um deles aleatoriamente fica “logged out” mais tarde

Para reduzir isso, OpenClaw trata <<CODE0>> como um lavatório **token**:

- o tempo de execução lê credenciais de ** um lugar**
- podemos manter vários perfis e roteá-los deterministicamente

# # Armazenamento (onde as fichas vivem)

Os segredos são guardados ** por agente**:

- Perfis de autenticação (chaves OAuth + API): <<CODE0>>
- Cache Runtime (gerido automaticamente; não edite): <<CODE1>>

Arquivo só de importação legado (ainda suportado, mas não a loja principal):

- <<CODE0> (importado para <<CODE1> na primeira utilização)

Todos os acima também respeitam <<CODE0>> (supressão dir estado). Referência completa: [/gateway/configuration](<<<LINK0>>>)

# # Token de configuração antrópica (autorização de inscrição)

Executar <<CODE0>> em qualquer máquina, em seguida, colar em OpenClaw:

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

Os fluxos interativos de login do OpenClaw são implementados em <<CODE0>> e conectados aos assistentes/comandos.

## # Antropic (Claude Pro/Max) configure-token

Forma de fluxo:

1. executar <<CODE0>>
2. colar o token em OpenClaw
3. armazenar como um perfil de autenticação token (sem atualização)

O caminho do assistente é <<CODE0>> → escolha de autenticação <<CODE1> (Antrópico).

## # Codex OpenAI (ChatGPT OAuth)

Forma de fluxo (PKCE):

1. gerar verificador/desafio PKCE + aleatório <<CODE0>>
2. abrir <<CODE1>>>
3. tente capturar o retorno de chamada em <<CODE2>>
4. se callback não pode vincular (ou você é remoto / sem cabeça), colar o URL de redirecionamento / código
5. troca em <<CODE3>>>
6. extrair <<CODE4>> do token de acesso e armazenar <<CODE5>>

O caminho do assistente é <<CODE0>> → escolha da autenticação <<CODE1>>.

# # Atualizar + expirar

Os perfis armazenam uma data <<CODE0>>.

Em tempo de execução:

- se <<CODE0> for no futuro → use o token de acesso armazenado
- se expirado → atualizar (sob um bloqueio de arquivo) e substituir as credenciais armazenadas

O fluxo de atualização é automático; você geralmente não precisa gerenciar tokens manualmente.

# # Contas múltiplas (perfis) + roteamento

Dois padrões:

# # # 1) Preferido: agentes separados

Se você quiser que “pessoal” e “trabalho” nunca interaja, use agentes isolados (sessões separadas + credenciais + espaço de trabalho):

```bash
openclaw agents add work
openclaw agents add personal
```

Em seguida, configure auth per-agent (wizard) e route chats para o agente certo.

# # # 2) Avançado: vários perfis em um agente

<<CODE0> suporta múltiplos IDs de perfil para o mesmo provedor.

Escolha qual perfil é usado:

- globalmente através da ordem de configuração (<<<CODE0>>)
- por sessão via <<CODE1>>>

Exemplo (sobreposição da sessão):

- <<CODE0>>

Como ver quais IDs de perfil existem:

- <<CODE0>> (mostra <<CODE1>>)

Documentos relacionados:

- [/conceitos/modelo-fracasso] (<<<LINK0>>>) (rotação + regras de arrefecimento)
- [/tools/slash-comandos](<<<LINK1>>) (superfície de comando)
