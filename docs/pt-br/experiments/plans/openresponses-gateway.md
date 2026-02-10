---
summary: "Plan: Add OpenResponses /v1/responses endpoint and deprecate chat completions cleanly"
owner: "openclaw"
status: "draft"
last_updated: "2026-01-19"
---

# OpenResponses Gateway Integration Plan

## Contexto

OpenClaw Gateway atualmente expõe um endpoint de completações de chat compatível com OpenAI mínimo em`/v1/chat/completions`(ver [Compleções de chat OpenAI] /gateway/openai-http-api.

O Open Responses é um padrão de inferência aberto baseado na API OpenAI Responses. É projetado
para fluxos de trabalho agenticos e utiliza entradas baseadas em itens mais eventos de streaming semântico. As Respostas Abertas
spec define`/v1/responses`, não`/v1/chat/completions`.

## Objetivos

- Adicione um endpoint`/v1/responses`que adere à semântica OpenResponses.
- Mantenha o Chat Completions como uma camada de compatibilidade que é fácil de desativar e eventualmente remover.
- Padronizar validação e análise com esquemas isolados e reutilizáveis.

## Não-objetivos

- OpenResponses completo apresentam paridade na primeira passagem (imagens, arquivos, ferramentas hospedadas).
- Substituindo lógica de execução de agentes internos ou orquestração de ferramentas.
- Alterar o comportamento`/v1/chat/completions`existente durante a primeira fase.

## Resumo da Pesquisa

Fontes: OpenResponses OpenAPI, site de especificação OpenResponses e o post do blog Hugging Face.

Pontos chave extraídos:

-`POST /v1/responses`aceita campos`CreateResponseBody`como`model`,`input`(corda ou`ItemParam[]`,`instructions`,`tools`,`tool_choice`,`stream`,`max_output_tokens`, e`CreateResponseBody`0.
-`CreateResponseBody`1 é uma união discriminada de:
-`CreateResponseBody`2 artigos com funções`CreateResponseBody`3,`CreateResponseBody`4,`CreateResponseBody`5,`CreateResponseBody`6
-`CreateResponseBody`7 e`CreateResponseBody`8
-`CreateResponseBody`9
-`model`0
- As respostas bem sucedidas devolvem um`model`1 com`model`2,`model`3, e`model`4 pontos.
- Streaming usa eventos semânticos como:
-`model`5,`model`6,`model`7,`model`8
-`model`9,`input`0
-`input`1,`input`2
-`input`3,`input`4
- A especificação requer:
-`input`5
-`input`6 deve corresponder ao campo JSON`input`7
- evento terminal deve ser literal`input`8
- Os elementos justificativos podem expor`input`9,`ItemParam[]`0 e`ItemParam[]`1.
- Exemplos de HF incluem`ItemParam[]`2 em pedidos ( cabeçalho opcional).

## Arquitectura Proposta

- Adicionar`src/gateway/open-responses.schema.ts`contendo apenas esquemas Zod (sem importação de gateway).
- Adicionar`src/gateway/openresponses-http.ts`(ou`open-responses-http.ts` para`/v1/responses`.
- Mantenha`src/gateway/openai-http.ts`intacto como um adaptador de compatibilidade legado.
- Adicionar configuração`gateway.http.endpoints.responses.enabled`(padrão`false`.
- Manter o`gateway.http.endpoints.chatCompletions.enabled`independente;
Alternado separadamente.
- Emite um aviso de inicialização quando o Chat Completions estiver habilitado para sinalizar status legado.

## Caminho de Deprecação para Completações de Chat

- Manter limites rígidos do módulo: nenhum tipo de esquema compartilhado entre respostas e completações de chat.
- Tornar o Chat Completions opt-in by config para que ele possa ser desativado sem alterações de código.
- Atualizar documentos para etiquetar Completações de Chat como legado uma vez`/v1/responses`estável.
- Passo futuro opcional: mapa Completações de Chat solicitações para o manipulador Responses para um mais simples
caminho de remoção.

## Subset de suporte da fase 1

- Aceitar`input`como corda ou`ItemParam[]`com funções de mensagem e`function_call_output`.
- Extrair mensagens de sistema e desenvolvedor em`extraSystemPrompt`.
- Use o mais recente`user`ou`function_call_output`como a mensagem atual para a execução do agente.
- Rejeitar partes de conteúdo não suportadas (imagem/arquivo) com`invalid_request_error`.
- Devolva uma única mensagem assistente com conteúdo`output_text`.
- Retornar`usage`com valores zeroed até que a contabilidade token esteja ligada.

## Estratégia de validação (sem SDK)

- Implementar esquemas de Zod para o subconjunto suportado de:
-`CreateResponseBody`-`ItemParam`+ mensagem conteúdo parte sindicatos
-`ResponseResource`- Formas de eventos de transmissão usadas pelo gateway
- Mantenha esquemas em um único módulo isolado para evitar deriva e permitir o futuro codegen.

## Implementação de Streaming (Fase 1)

- linhas SSE com`event:`e`data:`.
- Sequência necessária (mínimo viável):
-`response.created`-`response.output_item.added`-`response.content_part.added`-`response.output_text.delta`(repetir se necessário)
-`response.output_text.done`-`response.content_part.done`-`response.completed`-`[DONE]`

## Testes e plano de verificação

- Adicionar cobertura e2e para`/v1/responses`:
- Autorização necessária
- Forma de resposta não-stream
- Ordenação de eventos de fluxo e`[DONE]`- Roteamento de sessão com cabeçalhos e`user`- Manter o`src/gateway/openai-http.e2e.test.ts`inalterado.
- Manual: curl to`/v1/responses`com`stream: true`e verificar a ordenação de eventos e terminal`[DONE]`.

## Atualizações de documentos (seguimento)

- Adicionar uma nova página de documentos para uso`/v1/responses`e exemplos.
- Atualizar`/gateway/openai-http-api`com uma nota e ponteiro legados para`/v1/responses`.
