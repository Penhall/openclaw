---
summary: "How the macOS app reports gateway/Baileys health states"
read_when:
  - Debugging mac app health indicators
---

Controlos de saúde no macOS

Como ver se o canal ligado é saudável a partir da aplicação da barra de menus.

Barra de menus

- O estado reflete a saúde de Bailey.
- Verde: ligação + tomada aberta recentemente.
- Laranja: ligação/retentação.
- Saiu ou a sonda falhou.
- Linha secundária lê "linked · auth 12m" ou mostra a razão da falha.
- O item de menu "Execute a Verificação de Saúde" desencadeia uma sonda sob demanda.

Configuração

- A guia geral ganha um cartão de saúde mostrando: idade de autenticação vinculada, caminho/conta de armazenamento de sessão, última hora de verificação, último erro/código de status e botões para Executar verificação de saúde / Revelar registros.
- Usa um snapshot em cache para que a UI carregue instantaneamente e caia graciosamente quando estiver offline.
- ** Guia de canais** status do canal de superfícies + controles para WhatsApp/Telegram (login QR, logout, sonda, última desconexão/erro).

# # Como a sonda funciona

- Funciona <<CODE0>> via <<CODE1>>> A cada 60 e a pedido. A sonda carrega créditos e reporta status sem enviar mensagens.
- Cache o último snapshot bom e o último erro separadamente para evitar o flicker; mostrar a hora de cada.

# # Na dúvida

- Você ainda pode usar o fluxo de CLI em [Saúde de Gateway] (<<<LINK0>>) (<<CODE0>>, <<CODE1>>, <<CODE2>>) e cauda <<CODE3>> para <<CODE4>> / <<CODE5>>.
