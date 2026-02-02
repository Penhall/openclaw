---
summary: "Use Claude Max/Pro subscription as an OpenAI-compatible API endpoint"
read_when:
  - You want to use Claude Max subscription with OpenAI-compatible tools
  - You want a local API server that wraps Claude Code CLI
  - You want to save money by using subscription instead of API keys
---

Claude Max API Proxy

**claude-max-api-proxy** é uma ferramenta comunitária que expõe sua assinatura Claude Max/Pro como um endpoint de API compatível com OpenAI. Isso permite que você use sua assinatura com qualquer ferramenta que suporte o formato API OpenAI.

# # Por que usar isso?

Abordagem
------------------------ ----------------------------------------------------------------------------------- ------------------------------------------
□ API antrópica • Pagar por token (~$15/M entrada, $75/M saída para Opus)
□ Claude Max subscrição > $200/mês plano > Uso pessoal, desenvolvimento, uso ilimitado

Se você tiver uma assinatura Claude Max e quiser usá-la com ferramentas compatíveis com OpenAI, este proxy pode economizar dinheiro significativo.

# # Como Funciona

```
Your App → claude-max-api-proxy → Claude Code CLI → Anthropic (via subscription)
     (OpenAI format)              (converts format)      (uses your login)
```

O proxy:

1. Aceita pedidos em formato OpenAI em <<CODE0>
2. Converte-os para comandos CLI Código Claude
3. Retorna respostas no formato OpenAI (streaming suportado)

Instalação

```bash
# Requires Node.js 20+ and Claude Code CLI
npm install -g claude-max-api-proxy

# Verify Claude CLI is authenticated
claude --version
```

Utilização

Iniciar o servidor

```bash
claude-max-api
# Server runs at http://localhost:3456
```

Testa-o

```bash
# Health check
curl http://localhost:3456/health

# List models
curl http://localhost:3456/v1/models

# Chat completion
curl http://localhost:3456/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-opus-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

Com a Open Claw

Você pode apontar OpenClaw no proxy como um endpoint compatível com OpenAI personalizado:

```json5
{
  env: {
    OPENAI_API_KEY: "not-needed",
    OPENAI_BASE_URL: "http://localhost:3456/v1",
  },
  agents: {
    defaults: {
      model: { primary: "openai/claude-opus-4" },
    },
  },
}
```

# # Modelos Disponíveis

Mapas Para
--------------
Claude Opus 4
Claude Sonnet 4
* <<CODE2>* Claude Haiku 4

# # Iniciar automaticamente no macOS

Criar um LaunchAgent para executar o proxy automaticamente:

```bash
cat > ~/Library/LaunchAgents/com.claude-max-api.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.claude-max-api</string>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/local/bin/node</string>
    <string>/usr/local/lib/node_modules/claude-max-api-proxy/dist/server/standalone.js</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/usr/local/bin:/opt/homebrew/bin:~/.local/bin:/usr/bin:/bin</string>
  </dict>
</dict>
</plist>
EOF

launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.claude-max-api.plist
```

# # Links

- **npm:** https://www.npmjs.com/pacote/claude-max-api-proxy
- **GitHub:** https://github.com/atalovesyou/claude-max-api-proxy
- ** Questões:** https://github.com/atalovesyou/claude-max-api-proxy/issues

# # Notas

- Esta é uma ferramenta **community**, não suportada oficialmente por Anthropic ou OpenClaw
- Requer uma subscrição activa de Claude Max/Pro com Claude Code CLI autenticada
- O proxy é executado localmente e não envia dados para nenhum servidor de terceiros
- As respostas de transmissão são totalmente suportadas

# # Veja também

- [Fornecedor antrópico] (</providers/anthropic) - Integração OpenClaw nativa com chaves de configuração ou API Claude
- [OpenAI provider] (</providers/openai) - Assinaturas OpenAI/Codex
