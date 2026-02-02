---
summary: "Reference: provider-specific transcript sanitization and repair rules"
read_when:
  - You are debugging provider request rejections tied to transcript shape
  - You are changing transcript sanitization or tool-call repair logic
  - You are investigating tool-call id mismatches across providers
---

# Transcrição Higiene (fornecedores)

Este documento descreve **as correções específicas do provedor** aplicadas às transcrições antes de uma execução
(contexto do modelo de construção). Estes são **em memória** ajustamentos utilizados para satisfazer estritamente
Requisitos do prestador. Eles fazem **not** reescrever a transcrição JSONL armazenada no disco.

O âmbito de aplicação inclui:

- Limpeza de id de chamada de ferramenta
- Reparação de emparelhamento de resultados da ferramenta
- Validação de turnos/ordenação
- Limpeza da assinatura do pensamento
- Limpeza da carga útil da imagem

Se você precisar de detalhes de armazenamento transcrito, consulte:

- [/reference/session-management-compaction] (</reference/session-management-compaction)

---

# # Onde isto corre

Toda a higiene da transcrição é centralizada no corredor incorporado:

- Seleção de políticas: `src/agents/transcript-policy.ts`
- Aplicação de saneamento/reparação: <<CODE1> em <<CODE2>

A política utiliza `provider`, `modelApi` e `modelId` para decidir o que aplicar.

---

# # Regra global: higienização da imagem

As cargas de imagem são sempre higienizadas para evitar a rejeição do lado do provedor devido ao tamanho
limites (downscale/recomprimir imagens sobredimensionadas da base64).

Execução:

- <<CODE0> em <<CODE1>
- <<CODE2> em <<CODE3>

---

# # Matriz do provedor (comportamento atual)

** OpenAI / OpenAI Codex

- Só higienização por imagem.
- No modelo mude para OpenAI Responses/Codex, solte assinaturas de raciocínio órfão (itens de raciocínio standalone sem um bloco de conteúdo seguinte).
- Nada de limpeza de id.
- Nenhum resultado de reparação de emparelhamento.
- Sem validação de turnos ou reordenação.
- Não há resultados sintéticos.
- Nada de strip-tease.

**Google (IA Generativa / Gemini CLI / Antigravidade)**

- Ferramenta de limpeza de id: alfanumérico estrito.
- Resultado da ferramenta emparelhamento reparação e resultados de ferramenta sintética.
- Validação de turnos (alternação de turnos estilo Gemini).
- Google grow order fixup (prepend um pequeno usuário bootstrap se o histórico começa com assistente).
- Antigravidade Claude: normalizar assinaturas de pensamento; soltar blocos de pensamento sem assinatura.

**Antrópico / Minimax (Antrópico- compatível) **

- Resultado da ferramenta emparelhamento reparação e resultados de ferramenta sintética.
- Validação de turnos (mergulhar turnos de usuário consecutivos para satisfazer alternância estrita).

**Mistral (incluindo detecção baseada no ID do modelo) **

- Ferramenta chamada id higienização: strict9 (comprimento alfanumérico 9).

** OpenRouter Gemini**

- Limpeza da assinatura do pensamento: strip non-base64 `thought_signature` valores (manter base64).

* Tudo o resto *

- Só higienização por imagem.

---

# # Comportamento histórico (pré-2026.1.22)

Antes da libertação de 2026.1.22, o OpenClaw aplicou várias camadas de higiene transcripta:

- Uma extensão **transcript-sanitize** executado em cada compilação de contexto e poderia:
- Uso de ferramenta de reparo / resultado emparelhamento.
- Sanitar IDs de chamadas de ferramentas (incluindo um modo não restrito que preservou `_`/`-`).
- O corredor também realizava higienização específica do provedor, que duplicava o trabalho.
- Ocorreram mutações adicionais fora da política do prestador, incluindo:
- Striping <<CODE2> tags do texto assistente antes da persistência.
- A largar o erro de assistente vazio.
- Aparar conteúdo assistente após chamadas de ferramentas.

Esta complexidade causou regressões entre fornecedores (nomeadamente `openai-responses`
<<CODE1> emparelhamento). A limpeza 2026.1.22 removeu a extensão, centralizada
lógica no corredor, e fez OpenAI **no-touch** além da higienização da imagem.
