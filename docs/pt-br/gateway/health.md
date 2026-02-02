---
summary: "Health check steps for channel connectivity"
read_when:
  - Diagnosing WhatsApp channel health
---

# Controlos de Saúde (CLI)

Guia curto para verificar a conectividade do canal sem adivinhar.

# # Verificação rápida

- <<CODE0>> — resumo local: alcance/modo de gateway, dica de atualização, idade de autenticação do canal vinculada, sessões + atividade recente.
- <<CODE1>> — diagnóstico local completo (apenas leitura, cor, seguro para colar para depuração).
- <<CODE2>> — também sonda o Gateway em execução (sondas por canal quando suportadas).
- <<CODE3>> — pede ao Gateway em execução um snapshot completo de saúde (somente WS; nenhum soquete direto Baileys).
- Enviar <<CODE4>> como uma mensagem independente no WhatsApp/WebChat para obter uma resposta de status sem invocar o agente.
- Logs: cauda <<CODE5>> e filtro para <<CODE6>>, <<CODE7>>, <<CODE8>>, <<CODE9>>>.

# # Diagnósticos profundos

- Credes no disco: <<CODE0>> (mtime deve ser recente).
- Loja de sessões: <<CODE1>> (o caminho pode ser substituído na configuração). A contagem e os recetores recentes são observados via <<CODE2>>>.
- Fluxo de ligação: <<CODE3>> quando os códigos de estado 409-515 ou <<CODE4> aparecem em logs. (Nota: o fluxo de login QR reinicia automaticamente uma vez para o status 515 após emparelhamento.)

# # Quando algo falha

- <<CODE0> ou status 409–515 → relink com <<CODE1> então <<CODE2>.
- Gateway inalcançável → inicie-o: <<CODE3>> (use <<CODE4>> se a porta estiver ocupada).
- Nenhuma mensagem de entrada → confirmar que o telefone ligado está online e o remetente é permitido (<<<CODE5>>>); para chats de grupo, garantir que a allowlist + regras de menção correspondem (<<CODE6>>>, <<CODE7>>>).

# # Comando dedicado de "saúde"

<<CODE0> pergunta ao Gateway em execução para o seu snapshot de saúde (nenhuma tomada direta do canal do CLI). Relata credos/auth age quando disponíveis, resumos de sonda por canal, resumo de loja de sessão e duração da sonda. Sai não-zero se o Gateway for inacessível ou a sonda falhar/desligar. Use <<CODE1>> para substituir o padrão 10s.
