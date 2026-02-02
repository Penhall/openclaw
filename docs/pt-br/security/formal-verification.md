---
title: Formal Verification (Security Models)
summary: Machine-checked security models for OpenClaw’s highest-risk paths.
permalink: /security/formal-verification/
---

# Verificação formal (modelos de segurança)

Esta página rastreia os **modelos formais de segurança da OpenClaw** (TLA+/TLC hoje; mais conforme necessário).

> Nota: alguns links mais antigos podem se referir ao nome do projeto anterior.

** Goal (norte estrela):** fornecer um argumento verificado por máquina que OpenClaw
política de segurança pretendida (autorização, isolamento de sessão, gating de ferramentas, e
Segurança de configuração incorreta), sob suposições explícitas.

** O que é isto (hoje):** um executável, orientado por atacante ** suite de regressão de segurança**:

- Cada reivindicação tem um modelo de verificação executável sobre um espaço de estado finito.
- Muitas alegações têm um modelo emparelhado **negativo** que produz um traço contraexemplo para uma classe de bug realista.

**O que isso não é (ainda):** uma prova de que "OpenClaw é seguro em todos os aspectos" ou que a implementação completa do TypeScript está correta.

# # Onde vivem os modelos

Os modelos são mantidos em um repositório separado: [vignesh07/openclaw-formal-models](<https://github.com/vignesh07/openclaw-formal-models).

# # Advertências importantes

- Estes são **models**, não a implementação completa TypeScript. A deriva entre o modelo e o código é possível.
- Os resultados são limitados pelo espaço estatal explorado pela TLC; “verde” não implica segurança além dos pressupostos e limites modelados.
- Algumas alegações dependem de pressupostos ambientais explícitos (por exemplo, implantação correta, entradas de configuração corretas).

# # Reproduzir resultados

Hoje, os resultados são reproduzidos clonando os modelos de repo localmente e executando TLC (ver abaixo). Uma iteração futura poderia oferecer:

- Modelos CI-run com artefatos públicos (traços de contraexemplo, registros de execução)
- um fluxo de trabalho hospedado “run this model” para verificações pequenas e limitadas

Começar:

```bash
git clone https://github.com/vignesh07/openclaw-formal-models
cd openclaw-formal-models

# Java 11+ required (TLC runs on the JVM).
# The repo vendors a pinned `tla2tools.jar` (TLA+ tools) and provides `bin/tlc` + Make targets.

make <target>
```

## # Exposição do portal e má configuração do portal aberto

**Claim:** vincular além do loopback sem auth pode tornar possível o comprometimento remoto / aumenta a exposição; blocos token/password unauth atacantes (por os pressupostos do modelo).

- Green corre:
- <<CODE0>
- <<CODE1>
- Vermelho (esperado):
- <<CODE2>

Ver também: <<CODE0> nos modelos repo.

## # Nodes.run pipeline (capacidade de maior risco)

** Claim:** `nodes.run` requer (a) comando de nó allowlist mais comandos declarados e (b) aprovação ao vivo quando configurado; as aprovações são tokenizadas para evitar replay (no modelo).

- Green corre:
- <<CODE0>
- <<CODE1>
- Vermelho (esperado):
- <<CODE2>
- `make approvals-token-negative`

Loja de emparelhamento (DM gating)

**Claim:** pedidos de emparelhamento respeitam TTL e pendentes-request caps.

- Green corre:
- <<CODE0>
- <<CODE1>
- Vermelho (esperado):
- <<CODE2>
- `make pairing-cap-negative`

## # Entrada de gating (menções + bypass controle-comando)

**Claim:** em contextos de grupo que exigem menção, um “control command” não autorizado não pode ignorar a menção gating.

- Verde:
- <<CODE0>
- Vermelho (esperado):
- <<CODE1>

Roteamento/sessão de isolamento

**Claim:** DMs de pares distintos não colapsam na mesma sessão a menos que explicitamente ligados/configurados.

- Verde:
- <<CODE0>
- Vermelho (esperado):
- <<CODE1>

# # # v1++: modelos limites adicionais (concorrencia, repetições, correção de traços)

Estes são modelos de continuação que reforçam a fidelidade em torno dos modos de falha do mundo real (atualizações não-atômicas, repetições e fãs de mensagens).

# # # Emparelhamento concordante/idempotência

**Claim:** uma loja de emparelhamento deve impor `MaxPending` e idempotência mesmo sob interleavings (ou seja, "check-then-write" deve ser atômica / bloqueada; atualização não deve criar duplicatas).

O que significa:

- Sob solicitações simultâneas, você não pode exceder `MaxPending` para um canal.
- Os pedidos/refrescos repetidos para o mesmo <<CODE1> não devem criar linhas ao vivo duplicadas pendentes.

- Green corre:
- <<CODE0> (verificação da tampa atómica/locked)
- <<CODE1>
- <<CODE2>
- `make pairing-refresh-race`
- Vermelho (esperado):
- <<CODE4> (raça de início/compromisso não atómico)
- <<CODE5>
- <<CODE6>
- <<CODE7>

## # Correlação de traços de entrada/idempotência

**Claim:** a ingestão deve preservar a correlação de traços através do leque-out e ser idempotente sob repetições do provedor.

O que significa:

- Quando um evento externo se torna várias mensagens internas, cada parte mantém a mesma identidade de traço/evento.
- As repetições não resultam em duplo processamento.
- Se não existirem IDs de eventos de provedores, o dedupe cai de volta para uma chave segura (por exemplo, Trace ID) para evitar a perda de eventos distintos.

- Verde:
- <<CODE0>
- <<CODE1>
- <<CODE2>
- `make ingress-dedupe-fallback`
- Vermelho (esperado):
- `make ingress-trace-negative`
- <<CODE5>
- <<CODE6>
- <<CODE7>

## # Roteando precedência dmScope + identityLinks

**Claim:** roteamento deve manter sessões de DM isoladas por padrão, e somente sessões de colapso quando explicitamente configuradas (prioridade de canal + links de identidade).

O que significa:

- As sobreposições do dmScope específicas do canal devem ganhar os padrões globais.
- identityLinks devem entrar em colapso apenas dentro de grupos ligados explícitos, não entre pares não relacionados.

- Verde:
- <<CODE0>
- <<CODE1>
- Vermelho (esperado):
- <<CODE2>
- `make routing-identitylinks-negative`
