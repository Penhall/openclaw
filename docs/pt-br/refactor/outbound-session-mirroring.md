---
title: Outbound Session Mirroring Refactor (Issue #1520)
description: Track outbound session mirroring refactor notes, decisions, tests, and open items.
---

# Refator de Refletor de Sessão de Saída (Issue #1520)

# # Situação

- Em progresso.
- Core + roteamento de canal plugin atualizado para outbound espelhando.
- O envio do Gateway agora deriva a sessão de destino quando a chave de sessão é omitida.

# # Contexto

Os envios de saída foram espelhados na sessão  current  agent (chave de sessão da ferramenta) em vez da sessão do canal alvo. O roteamento inbound usa as teclas de sessão canal / peer, então as respostas outbound pousaram na sessão errada e os alvos de primeiro contato muitas vezes faltavam entradas de sessão.

# # Objetivos

- Mirror mensagens de saída para a tecla de sessão do canal alvo.
- Criar entradas de sessão na saída quando faltando.
- Mantenha a linha/tema de localização alinhada com as teclas de sessão de entrada.
- Cobrir canais principais e extensões agrupadas.

# # Resumo da Implementação

- Novo assistente de roteamento de sessão:
- <<CODE0>
- <<CODE1> compila a sessão-alvoChave usando `buildAgentSessionKey` (dmScope + identityLinks).
- <<CODE3> escreve o mínimo `MsgContext` via `recordSessionMetaFromInbound`.
- <<CODE6> (enviar) deriva sessionKey alvo e passa para `executeSendAction` para espelhamento.
- `message-tool` não mais espelhos diretamente; só resolve agentId da chave de sessão atual.
- Plugin enviar mirrors caminho via `appendAssistantMessageToSessionTranscript` usando a chave de sessão derivada.
- Gateway send deriva uma chave de sessão alvo quando nenhum é fornecido (agente padrão), e garante uma entrada de sessão.

# # Manuseamento de Fios/Tópicos

- Slack: replyTo/threadId -> `resolveThreadSessionKeys` (sufixo).
- Discórdia: threadId/replyTo -> `resolveThreadSessionKeys` com `useSuffix=false` para corresponder à entrada (a sessão do id do canal de thread já abrange).
- Telegrama: mapa de IDs tópicos para `chatId:topic:<id>` via `buildTelegramGroupPeerId`.

# # Extensões cobertas

- Matrix, MS Teams, Mattermost, BlueBubbles, Nextcloud Talk, Zalo, Zalo Personal, Nostr, Tlon.
- Notas:
- Os alvos mais importantes agora tiram <<CODE0> para roteamento da chave da sessão de DM.
- Zalo Personal usa o tipo de par DM para 1:1 alvos (grupo somente quando `group:` está presente).
- BlueBubbles group targets strip <<CODE2> prefixos para combinar com as teclas de sessão de entrada.
- Slack auto-thread espelhando correspondências canal IDs caso-insensível.
- Gateway enviar minúsculas chaves de sessão fornecidas antes de espelhar.

# # Decisões

- **Gateway enviar derivação de sessão**: se <<CODE0> é fornecido, use-o. Se omitido, derivar uma sessionKey do alvo + agente padrão e espelho lá.
- ** Criação de entradas de sessão**: usar sempre `recordSessionMetaFromInbound` com <<CODE2> alinhado aos formatos de entrada.
- ** Normalização do alvo**: roteamento de saída usa alvos resolvidos (post `resolveChannelTarget`) quando disponível.
- **Session key caughing**: canonicalize session keys to mindcase on write and during migrations.

# # Testes Adicionados/Atualizados

- <<CODE0>
- Chave de sessão de linha.
- Tecla de sessão de tópicos de telegrama.
- identidade dmScopeLinks com Discórdia.
- <<CODE1>
- Derives agentId da chave da sessão (sem sessãoA chave passou).
- <<CODE2>
- Deriva a tecla de sessão quando omitido e cria a entrada de sessão.

# # Abrir itens / acompanhamentos

- Plug-in de chamada de voz usa teclas de sessão personalizadas `voice:<phone>`. O mapeamento de saída não está padronizado aqui; se a ferramenta de mensagem deve suportar o envio de chamadas de voz, adicione mapeamento explícito.
- Confirme se algum plugin externo usa formatos não padrão `From/To` além do conjunto empacotado.

# # Arquivos Tocados

- <<CODE0>
- <<CODE1>
- <<CODE2>
- `src/agents/tools/message-tool.ts`
- `src/gateway/server-methods/send.ts`
- Testes em:
- <<CODE5>
- <<CODE6>
- <<CODE7>
