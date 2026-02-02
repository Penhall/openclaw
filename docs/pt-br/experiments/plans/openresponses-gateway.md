---
summary: "Plan: Add OpenResponses /v1/responses endpoint and deprecate chat completions cleanly"
owner: "openclaw"
status: "draft"
last_updated: "2026-01-19"
---

# OpenResponses Gateway Integration Plan

# # Contexto

OpenClaw Gateway atualmente expõe um endpoint de completações de chat compatível com OpenAI mínimo em
<<CODE0>> (ver [Complementos de Chat OpenAI](<<LINK0>>>)).

O Open Responses é um padrão de inferência aberto baseado na API OpenAI Responses. É projetado
para fluxos de trabalho agenticos e utiliza entradas baseadas em itens mais eventos de streaming semântico. As Respostas Abertas
spec define <<CODE0>>, não <<CODE1>>>>.

# # Objetivos

- Adicionar um ponto final <<CODE0>> que adere à semântica OpenResponses.
- Mantenha o Chat Completions como uma camada de compatibilidade que é fácil de desativar e eventualmente remover.
- Padronizar validação e análise com esquemas isolados e reutilizáveis.

# # Não-objetivos

- OpenResponses completo apresentam paridade na primeira passagem (imagens, arquivos, ferramentas hospedadas).
- Substituindo lógica de execução de agentes internos ou orquestração de ferramentas.
- Alteração do comportamento existente <<CODE0>> durante a primeira fase.

# # Resumo da Pesquisa

Fontes: OpenResponses OpenAPI, site de especificação OpenResponses e o post do blog Hugging Face.

Pontos chave extraídos:

- <<CODE0> aceita <<CODE1>> campos como <<CODE2>>, <<CODE3>> (cadeia ou
<<CODE4>>), <<CODE5>>, <<CODE6>>>, <<CODE7>>, <<CODE8>>, <<CODE9>>, e
<<CODE10>>>.
- <<CODE11> é uma união discriminada de:
- <<CODE12>> itens com papéis <<CODE13>>, <<CODE14>>, <<CODE15>>, <<CODE16>>
- <<CODE17>> e <<CODE18>>>
- <<CODE19>>
- <<CODE20>>
- Respostas bem sucedidas retornam a <<CODE21>> com <<CODE22>>>, <<CODE23>>>, e
<<CODE24>> itens.
- Streaming usa eventos semânticos como:
- <<CODE25>>, <<CODE26>>, <<CODE27>>, <<CODE28>>
- <<CODE29>>, <<CODE30>>
- <<CODE31>>, <<CODE32>>
- <<CODE33>, <<CODE34>>
- A especificação requer:
- <<CODE35>>
- <<CODE36> deve corresponder ao campo JSON <<CODE37>>
- evento terminal deve ser literal <<CODE38>>>
- Os itens justificativos podem expor <<CODE39>>, <HTML40>>>> e <<CODE41>>>.
- Os exemplos de HF incluem <<CODE42>> em requisições (header opcional).

# # Arquitectura Proposta

- Adicionar <<CODE0>> contendo apenas esquemas Zod (sem importação de gateway).
- Adicionar <<CODE1>> (ou <<CODE2>>>>) para <<CODE3>>>.
- Manter <<CODE4>> intacto como adaptador de compatibilidade legado.
- Adicionar configuração <<CODE5>> (padrão <<CODE6>>>).
- Manter <<CODE7>> independente; permitir que ambos os objectivos sejam
Alternado separadamente.
- Emite um aviso de inicialização quando o Chat Completions estiver habilitado para sinalizar status legado.

# # Caminho de Deprecação para Completações de Chat

- Manter limites rígidos do módulo: nenhum tipo de esquema compartilhado entre respostas e completações de chat.
- Tornar o Chat Completions opt-in by config para que ele possa ser desativado sem alterações de código.
- Atualizar documentos para etiquetar Completações de Chat como legado uma vez <<CODE0> é estável.
- Passo futuro opcional: mapa Completações de Chat solicitações para o manipulador Responses para um mais simples
caminho de remoção.

# # Subset de suporte da fase 1

- Aceitar <<CODE0>> como string ou <<CODE1> com papéis de mensagem e <<CODE2>>.
- Extrair mensagens do sistema e do desenvolvedor em <<CODE3>>>.
- Use a mensagem mais recente <<CODE4>> ou <<CODE5>> como a mensagem atual para agentes.
- Rejeitar partes de conteúdo não suportadas (imagem/file) com <<CODE6>>.
- Devolver uma única mensagem assistente com <<CODE7>> conteúdo.
- Retorno <<CODE8>> com valores zeroados até que a contabilidade token esteja ligada.

# # Estratégia de validação (sem SDK)

- Implementar esquemas de Zod para o subconjunto suportado de:
- <<CODE0>>
- <<CODE1>> + sindicações de partes de conteúdo de mensagens
- <<CODE2>>
- Formas de eventos de transmissão usadas pelo gateway
- Mantenha esquemas em um único módulo isolado para evitar deriva e permitir o futuro codegen.

# # Implementação de Streaming (Fase 1)

- Linhas de SSE com <<CODE0>> e <HTML1>>>>.
- Sequência necessária (mínimo viável):
- <<CODE2>>
- <<CODE3>>
- <<CODE4>>
- <<CODE5>> (repetir se necessário)
- <<CODE6>>
- <<CODE7>>
- <<CODE8>>
- <<CODE9>>

# # Testes e plano de verificação

- Adicionar cobertura e2e para <<CODE0>>:
- Autorização necessária
- Forma de resposta não-stream
- Ordenação de eventos de fluxo e <<CODE1>>
- Roteamento de sessão com cabeçalhos e <<CODE2>>
- Manter <<CODE3>> inalterado.
- Manual: enrolar para <<CODE4>> com <<CODE5>> e verificar a ordenação de eventos e terminal
<<CODE6>>.

# # Atualizações de documentos (seguimento)

- Adicionar uma nova página de documentos para <<CODE0>> uso e exemplos.
- Actualização <<CODE1>> com uma nota e ponteiro legados para <<CODE2>>>.
