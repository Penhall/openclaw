---
summary: "Use Qwen OAuth (free tier) in OpenClaw"
read_when:
  - You want to use Qwen with OpenClaw
  - You want free-tier OAuth access to Qwen Coder
---

# Qwen

Qwen fornece um fluxo de OAuth de nível livre para os modelos Qwen Coder e Qwen Vision
(2.000 pedidos/dia, sujeitos a limites de taxa Qwen).

# # Habilitar o plugin

```bash
openclaw plugins enable qwen-portal-auth
```

Reinicie o portal depois de activar.

# # Autenticar

```bash
openclaw models auth login --provider qwen-portal --set-default
```

Isto executa o fluxo OAuth do código do dispositivo Qwen e escreve uma entrada do provedor para o seu
`models.json` (mais um `qwen` alias para comutação rápida).

# # Identidades de modelos

- <<CODE0>
- <<CODE1>

Mudar modelos com:

```bash
openclaw models set qwen-portal/coder-model
```

# # Reutilizar o login do Código Qwen CLI

Se você já fez login com o Código Qwen CLI, o OpenClaw sincronizará credenciais
a partir de `~/.qwen/oauth_creds.json` quando carrega o armazém de autenticação. Ainda precisas de um...
<<CODE1> entrada (use o comando de login acima para criar um).

# # Notas

- Tokens auto-refresh; execute novamente o comando login se a atualização falhar ou o acesso for revogado.
- URL de base padrão: `https://portal.qwen.ai/v1` (substituir com
<<CODE1> se Qwen fornecer um objectivo diferente).
- Ver [Fornecedores de modelos] (</concepts/model-providers) para as regras gerais do prestador.
