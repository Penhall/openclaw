---
summary: "Usage tracking surfaces and credential requirements"
read_when:
  - You are wiring provider usage/quota surfaces
  - You need to explain usage tracking behavior or auth requirements
---

# Rastreio de uso

# # O que é

- Puxa o uso/quota do provedor diretamente de seus terminais de uso.
- Sem custos estimados; apenas as janelas comunicadas pelo fornecedor.

# # Onde aparece

- <<CODE0> em chats: cartão de estado emoji-rich com tokens de sessão + custo estimado (chave API apenas). O uso do provedor mostra para o provedor de modelo ** atual** quando disponível.
- <<CODE1> em chats: rodapé de utilização por resposta (OAuth mostra apenas fichas).
- <<CODE2> em chats: resumo de custos local agregado a partir de logs de sessão OpenClaw.
- CLI: <<CODE3>> imprime uma avaria total por fornecedor.
- CLI: <<CODE4> imprime o mesmo instantâneo de uso ao lado da configuração do provedor (use <<CODE5> para pular).
- barra de menu macOS: “Usar” seção em Contexto (apenas se disponível).

# # Provedores + credenciais

- **Antrópico (Claude)**: Tokens OAuth em perfis de autenticação.
- **GitHub Copilot**: Tokens OAuth em perfis de autenticação.
- ** Gemini CLI**: Tokens OAuth em perfis de autenticação.
- ** Antigravidade**: Tokens OAuth em perfis de autenticação.
- **OpenAI Codex**: Tokens OAuth em perfis de autenticação (accountId usado quando presente).
- **MiniMax**: chave API (chave de plano de codificação; <<CODE0> ou <<CODE1>>>); usa a janela de plano de codificação de 5 horas.
- **z.ai**: Chave API via env/config/auth store.

O uso está oculto se não existirem credenciais OAuth/API correspondentes.
