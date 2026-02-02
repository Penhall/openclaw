---
summary: "Gateway dashboard (Control UI) access and auth"
read_when:
  - Changing dashboard authentication or exposure modes
---

# Painel (Control UI)

O painel Gateway é o navegador Control UI servido em <<CODE0> por padrão
(substituir com `gateway.controlUi.basePath`).

Abertura rápida (porta local):

- http://127.0.0.1:18789/ (ou http://localhost:18789/)

Principais referências:

- [Control UI](</web/control-ui) para utilização e capacidades de UI.
- [Tailscale] (</gateway/tailscale) para automação Serve/Funnel.
- [Superfícies Web] (</web) para modos de ligação e notas de segurança.

A autenticação é aplicada no aperto de mão WebSocket via `connect.params.auth`
(toque ou senha). Ver <<CODE1> na configuração de [Gateway](/gateway/configuration).

Nota de segurança: a interface de controle é uma superfície de administração** (chat, config, exec aprovations).
Não exponha isso publicamente. A UI armazena o token em `localStorage` após a primeira carga.
Prefere localhost, Tailscale Serve, ou um túnel SSH.

# # Caminho rápido (recomendado)

- Depois de embarcar, o CLI agora abre automaticamente o painel com o seu token e imprime o mesmo link tokenized.
- Reabrir a qualquer momento: `openclaw dashboard` (copia o link, abre o navegador se possível, mostra a dica SSH se sem cabeça).
- O token permanece local (pergunte apenas param); o UI tira-o após a primeira carga e salva-o no localStorage.

# # Token basics (local vs remoto)

- ** Localhost**: aberto `http://127.0.0.1:18789/`. Se você vir “não autorizado”, execute `openclaw dashboard` e use o link tokenizado (`?token=...`).
- ** Fonte do item**: `gateway.auth.token` (ou <CODE4>>); a IU armazena-o após a primeira carga.
- ** Não localhost**: use Tailscale Serve (sem token se `gateway.auth.allowTailscale: true`), tailnet se liga com um token, ou um túnel SSH. Ver [Superfícies Web] (</web).

# # # Se você ver “não autorizado” / 1008

- Executar <<CODE0> para obter um novo link tokenized.
- Certifique-se de que o gateway é acessível (local: `openclaw status`; remoto: túnel SSH `ssh -N -L 18789:127.0.0.1:18789 user@host` então aberto `http://127.0.0.1:18789/?token=...`).
- Nas configurações do painel, cole o mesmo token que você configurou em `gateway.auth.token` (ou <CODE5>>).
