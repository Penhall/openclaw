---
summary: "Usage tracking surfaces and credential requirements"
read_when:
  - You are wiring provider usage/quota surfaces
  - You need to explain usage tracking behavior or auth requirements
---

# Rastreio de uso

## O que é

- Puxa o uso/quota do provedor diretamente de seus terminais de uso.
- Sem custos estimados; apenas as janelas comunicadas pelo fornecedor.

## Onde aparece

-`/status`em chats: cartão de status emoji-rich com tokens de sessão + custo estimado (chave API apenas). O uso do provedor mostra para o provedor de modelo ** atual** quando disponível.
-`/usage off|tokens|full`em chats: rodapé de uso por resposta (OAuth mostra apenas fichas).
-`/usage cost`em chats: resumo de custos local agregado a partir de registros de sessão OpenClaw.
- CLI:`openclaw status --usage`imprime uma quebra total por provedor.
- CLI:`openclaw channels list`imprime o mesmo instantâneo de uso ao lado da configuração do provedor (use`--no-usage`para pular).
- barra de menu macOS: “Usar” seção em Contexto (apenas se disponível).

## Provedores + credenciais

- **Antrópico (Claude)**: Tokens OAuth em perfis de autenticação.
- **GitHub Copilot**: Tokens OAuth em perfis de autenticação.
- ** Gemini CLI**: Tokens OAuth em perfis de autenticação.
- ** Antigravidade**: Tokens OAuth em perfis de autenticação.
- **OpenAI Codex**: Tokens OAuth em perfis de autenticação (accountId usado quando presente).
- **MiniMax**: Chave API (chave do plano de codificação;`MINIMAX_CODE_PLAN_KEY`ou`MINIMAX_API_KEY`; usa a janela do plano de codificação de 5 horas.
- **z.ai**: Chave API via env/config/auth store.

O uso está oculto se não existirem credenciais OAuth/API correspondentes.
