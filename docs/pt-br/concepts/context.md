---
summary: "Context: what the model sees, how it is built, and how to inspect it"
read_when:
  - You want to understand what “context” means in OpenClaw
  - You are debugging why the model “knows” something (or forgot it)
  - You want to reduce context overhead (/context, /status, /compact)
---

Contexto

“Contexto” é **tudo que OpenClaw envia para o modelo para uma execução**. Ele é limitado pela janela de contexto ** do modelo (limite de token).

Modelo mental inicial:

- **System prompt** (OpenClaw-built): regras, ferramentas, lista de habilidades, tempo/runtime e arquivos de espaço de trabalho injetados.
- ** Histórico de conversa**: suas mensagens + mensagens do assistente para esta sessão.
- **Tool calls/results + attachments**: saída de comando, leituras de arquivos, imagens/áudio, etc.

Contexto é  não a mesma coisa  que “memória”: a memória pode ser armazenada no disco e recarregada mais tarde; contexto é o que está dentro da janela atual do modelo.

## Início rápido (inspecionar contexto)

-`/status`→ rápido “Quão cheio está minha janela?” view + configurações de sessão.
-`/context list`→ o que é injetado + tamanhos brutos (por arquivo + totais).
-`/context detail`→ desagregação mais profunda: por arquivo, tamanhos de esquema por ferramenta, tamanhos de entrada por habilidade e tamanho do sistema.
-`/usage tokens`→ adicionar o rodapé de uso por resposta às respostas normais.
-`/compact`→ resume a história antiga em uma entrada compacta para espaço de janela livre.

Ver também: [Comandos Slash]/tools/slash-commands, [Uso & Custos Token]/token-use, [Compactação]/concepts/compaction.

## Saída de exemplo

Os valores variam de acordo com o modelo, provedor, política de ferramentas e o que está em seu espaço de trabalho.

## #`/context list`

```
🧠 Context breakdown
Workspace: <workspaceDir>
Bootstrap max/file: 20,000 chars
Sandbox: mode=non-main sandboxed=false
System prompt (run): 38,412 chars (~9,603 tok) (Project Context 23,901 chars (~5,976 tok))

Injected workspace files:
- AGENTS.md: OK | raw 1,742 chars (~436 tok) | injected 1,742 chars (~436 tok)
- SOUL.md: OK | raw 912 chars (~228 tok) | injected 912 chars (~228 tok)
- TOOLS.md: TRUNCATED | raw 54,210 chars (~13,553 tok) | injected 20,962 chars (~5,241 tok)
- IDENTITY.md: OK | raw 211 chars (~53 tok) | injected 211 chars (~53 tok)
- USER.md: OK | raw 388 chars (~97 tok) | injected 388 chars (~97 tok)
- HEARTBEAT.md: MISSING | raw 0 | injected 0
- BOOTSTRAP.md: OK | raw 0 chars (~0 tok) | injected 0 chars (~0 tok)

Skills list (system prompt text): 2,184 chars (~546 tok) (12 skills)
Tools: read, edit, write, exec, process, browser, message, sessions_send, …
Tool list (system prompt text): 1,032 chars (~258 tok)
Tool schemas (JSON): 31,988 chars (~7,997 tok) (counts toward context; not shown as text)
Tools: (same as above)

Session tokens (cached): 14,250 total / ctx=32,000
```

## #`/context detail`

```
🧠 Context breakdown (detailed)
…
Top skills (prompt entry size):
- frontend-design: 412 chars (~103 tok)
- oracle: 401 chars (~101 tok)
… (+10 more skills)

Top tools (schema size):
- browser: 9,812 chars (~2,453 tok)
- exec: 6,240 chars (~1,560 tok)
… (+N more tools)
```

## O que conta para a janela de contexto

Tudo o que o modelo recebe conta, incluindo:

- Prompt de sistema (todas as secções).
- História da conversa.
- Chamadas de ferramenta + resultados de ferramenta.
- Anexos/transcritos (imagens/audio/arquivos).
- Resumos de compactação e artefactos de poda.
- Fornecedor “embrulhadores” ou cabeçalhos ocultos (não visíveis, ainda contados).

## Como OpenClaw constrói o prompt do sistema

O prompt do sistema é **OpenClaw pertence a ** e reconstruiu cada execução. Inclui:

- Lista de ferramentas + descrições curtas.
- Lista de competências (apenas metadados; ver abaixo).
- Local de trabalho.
- Tempo (UTC + tempo de usuário convertido se configurado).
- Metadados em tempo de execução (host/OS/model/thinking).
- Injetado workspace bootstrap arquivos em **Project Context**.

Discriminação completa: [Prompt do sistema] /concepts/system-prompt.

### Arquivos de espaço de trabalho injetados (Contexto do Projeto)

Por padrão, o OpenClaw injeta um conjunto fixo de arquivos de espaço de trabalho (se presentes):

-`AGENTS.md`-`SOUL.md`-`TOOLS.md`-`IDENTITY.md`-`USER.md`-`HEARTBEAT.md`-`BOOTSTRAP.md`(apenas de primeira ordem)

Arquivos grandes são truncados por arquivo usando`agents.defaults.bootstrapMaxChars`(carros padrão`20000`.`/context`mostra ** tamanho raw vs injetado** e se houve truncamento.

## Habilidades: o que é injetado vs carregado sob demanda

O prompt do sistema inclui uma lista compacta de habilidades ** (nome + descrição + localização). Esta lista tem despesas reais.

Instruções de habilidade estão  não  incluídas por padrão. O modelo é esperado para`read`a habilidade`SKILL.md`** somente quando necessário**.

## Ferramentas: há dois custos

As ferramentas afetam o contexto de duas maneiras:

1. ** Texto da lista de ferramentas** no prompt do sistema (o que você vê como “Ferramenta”).
2. **Esquemas de ferramentas** (JSON). Estes são enviados para o modelo para que possa chamar ferramentas. Eles contam para o contexto, mesmo que você não os veja como texto simples.

`/context detail`quebra os maiores esquemas de ferramentas para que você possa ver o que domina.

## Comandos, diretivas e “atalhos em linha”

Os comandos Slash são manuseados pelo Gateway. Existem alguns comportamentos diferentes:

- ** Comandos padrão**: uma mensagem que é apenas`/...`é executada como um comando.
- ** Directivas**:`/think`,`/verbose`,`/reasoning`,`/elevated`,`/model`,`/queue`são despojados antes de o modelo ver a mensagem.
- As mensagens só de ordem persistem nas configurações da sessão.
- Diretrizes em linha em uma mensagem normal funcionam como sugestões por mensagem.
- **Atalhos em linha** (apenas remetentes listados): certos tokens`/...`dentro de uma mensagem normal podem ser executados imediatamente (exemplo: “hey /status”), e são despojados antes que o modelo veja o texto restante.

Detalhes: [Comandos de linha] /tools/slash-commands.

### Sessões, compactação e poda (o que persiste)

O que persiste entre as mensagens depende do mecanismo:

- **O histórico normal** persiste na transcrição da sessão até compactado/pruned pela política.
- **Compaction** persiste um resumo na transcrição e mantém as mensagens recentes intactas.
- **Pruning** remove resultados antigos da ferramenta  in-memory  prompt para uma execução, mas não reescreve a transcrição.

Docs: [Sessão]/concepts/session, [Compactação]/concepts/compaction, [Sessão de poda]/concepts/session-pruning.

## O que`/context`realmente relata

`/context`prefere o mais recente relatório de prompt do sistema ** executado quando disponível:

-`System prompt (run)`= capturada da última execução incorporada (capaz de ferramentas) e persistiu na loja de sessão.
-`System prompt (estimate)`= calculado na hora em que nenhum relatório de execução existe (ou quando executado através de uma infra-estrutura CLI que não gera o relatório).

De qualquer forma, ele relata tamanhos e principais contribuintes; ele não ** descarta o prompt completo do sistema ou esquemas de ferramentas.
