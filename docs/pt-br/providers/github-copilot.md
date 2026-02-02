---
summary: "Sign in to GitHub Copilot from OpenClaw using the device flow"
read_when:
  - You want to use GitHub Copilot as a model provider
  - You need the `openclaw models auth login-github-copilot` flow
---

# Copiloto GitHub

# # O que é GitHub Copilot?

GitHub Copilot é o assistente de codificação de IA do GitHub. Fornece acesso ao Copiloto
modelos para sua conta e plano GitHub. Openclaw pode usar Copilot como modelo
provedor de duas maneiras diferentes.

# # Duas maneiras de usar o co-piloto no OpenClaw

### 1) Fornecedor de copiloto integrado do GitHub (`github-copilot`)

Use o fluxo de login nativo do dispositivo para obter um token GitHub, então troque- o por
Copilot API tokens quando OpenClaw é executado. Este é o caminho ** default** e mais simples
porque não requer código VS.

### 2) Plug-in de Proxy co-piloto (`copilot-proxy`)

Use a extensão **Copilot Proxy** VS Code como uma ponte local. Openclaw conversa com
O ponto final do proxy `/v1` e usa a lista de modelos que você configurar lá. Escolher
isso quando você já executa o Copilot Proxy em VS Code ou precisa roteá-lo.
Você deve habilitar o plugin e manter a extensão VS Code em execução.

Use o GitHub Copilot como fornecedor de modelos (<`github-copilot`). O comando de login é executado
o fluxo do dispositivo GitHub, salva um perfil de autenticação e atualiza sua configuração para usar isso
Perfil.

# # Configuração do CLI

```bash
openclaw models auth login-github-copilot
```

Você será solicitado a visitar um URL e inserir um código único. Manter o terminal
abrir até completar.

## # Bandeiras opcionais

```bash
openclaw models auth login-github-copilot --profile-id github-copilot:work
openclaw models auth login-github-copilot --yes
```

# # Definir um modelo padrão

```bash
openclaw models set github-copilot/gpt-4o
```

### Config snippet

```json5
{
  agents: { defaults: { model: { primary: "github-copilot/gpt-4o" } } },
}
```

# # Notas

- Requer um TTY interativo; executá-lo diretamente em um terminal.
- A disponibilidade do modelo co-piloto depende do seu plano; se um modelo for rejeitado, tente
outro ID (por exemplo, `github-copilot/gpt-4.1`).
- O login armazena um token GitHub no auth profile store e o troca por um
Copilot Token API quando o OpenClaw for executado.
