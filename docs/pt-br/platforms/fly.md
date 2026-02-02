---
title: Fly.io
description: Deploy OpenClaw on Fly.io
---

# Fly.io Implantação

**Objetivo:** OpenClaw Gateway rodando em uma máquina [Fly.io](<<<LINK0>>) com armazenamento persistente, HTTPS automático e Discord/canal de acesso.

# # O que precisas

- [flyctl CLI] (<<<LINK0>>>) instalado
- conta Fly.io (trabalhos de nível livre)
- Autenticação do modelo: Chave antrópica da API (ou outras chaves de provedor)
- Credenciais de canal: Discord bot token, Telegram token, etc.

# # Caminho rápido iniciante

1. Repo clone → personalizar <<CODE0>>
2. Criar aplicativo + volume → definir segredos
3. Implantar com <<CODE1>>
4. SSH em para criar config ou usar Control UI

# # 1) Criar o aplicativo Fly

```bash
# Clone the repo
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# Create a new Fly app (pick your own name)
fly apps create my-openclaw

# Create a persistent volume (1GB is usually enough)
fly volumes create openclaw_data --size 1 --region iad
```

**Dica: ** Escolha uma região perto de você. Opções comuns: <<CODE0>> (Londres), <<CODE1>> (Virginia), <<CODE2>> (San Jose).

# # 2) Configurar fly.toml

Editar <<CODE0>> para corresponder ao nome e requisitos do seu aplicativo.

** Nota de segurança: ** A configuração padrão expõe um URL público. Para uma implantação endurecida sem IP público, ver [Deployment Private](<<<LINK0>>>) ou usar <<CODE0>>.

```toml
app = "my-openclaw"  # Your app name
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[env]
  NODE_ENV = "production"
  OPENCLAW_PREFER_PNPM = "1"
  OPENCLAW_STATE_DIR = "/data"
  NODE_OPTIONS = "--max-old-space-size=1536"

[processes]
  app = "node dist/index.js gateway --allow-unconfigured --port 3000 --bind lan"

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = false
  auto_start_machines = true
  min_machines_running = 1
  processes = ["app"]

[[vm]]
  size = "shared-cpu-2x"
  memory = "2048mb"

[mounts]
  source = "openclaw_data"
  destination = "/data"
```

** Configuração das chaves:**

Configurando
----------------------------------- -------------------------------------------------------------------------------------------
* <<CODE0>> * Ligações <<CODE1> para que o proxy da Fly possa chegar ao gateway .
Começa sem um arquivo de configuração (você vai criar um depois)
* < <<CODE3>>
512MB é demasiado pequeno; 2GB recomendado
* <<CODE7>>

# # 3) Definir segredos

```bash
# Required: Gateway token (for non-loopback binding)
fly secrets set OPENCLAW_GATEWAY_TOKEN=$(openssl rand -hex 32)

# Model provider API keys
fly secrets set ANTHROPIC_API_KEY=sk-ant-...

# Optional: Other providers
fly secrets set OPENAI_API_KEY=sk-...
fly secrets set GOOGLE_API_KEY=...

# Channel tokens
fly secrets set DISCORD_BOT_TOKEN=MTQ...
```

**Notas:**

- As ligações não- loopback (<<<CODE0>>) requerem <<CODE1>>>> para segurança.
- Trata estes tokens como senhas.
- **Prefer env vars sobre o arquivo de configuração** para todas as chaves e tokens da API. Isso mantém segredos fora de <<CODE2>> onde eles podem ser acidentalmente expostos ou registrados.

4) Preparar

```bash
fly deploy
```

O primeiro implante constrói a imagem do Docker (~2-3 minutos). Implantes posteriores são mais rápidos.

Após a implantação, verificar:

```bash
fly status
fly logs
```

Devias ver:

```
[gateway] listening on ws://0.0.0.0:3000 (PID xxx)
[discord] logged in to discord as xxx
```

## 5) Criar arquivo de configuração

SSH na máquina para criar uma configuração adequada:

```bash
fly ssh console
```

Criar o diretório e arquivo de configuração:

```bash
mkdir -p /data
cat > /data/openclaw.json << 'EOF'
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-5",
        "fallbacks": ["anthropic/claude-sonnet-4-5", "openai/gpt-4o"]
      },
      "maxConcurrent": 4
    },
    "list": [
      {
        "id": "main",
        "default": true
      }
    ]
  },
  "auth": {
    "profiles": {
      "anthropic:default": { "mode": "token", "provider": "anthropic" },
      "openai:default": { "mode": "token", "provider": "openai" }
    }
  },
  "bindings": [
    {
      "agentId": "main",
      "match": { "channel": "discord" }
    }
  ],
  "channels": {
    "discord": {
      "enabled": true,
      "groupPolicy": "allowlist",
      "guilds": {
        "YOUR_GUILD_ID": {
          "channels": { "general": { "allow": true } },
          "requireMention": false
        }
      }
    }
  },
  "gateway": {
    "mode": "local",
    "bind": "auto"
  },
  "meta": {
    "lastTouchedVersion": "2026.1.29"
  }
}
EOF
```

**Nota:** Com <<CODE0>>, o caminho de configuração é <<CODE1>>.

**Nota:** O símbolo Discórdia pode vir de:

- Variável ambiente: <<CODE0>> (recomendado para segredos)
- Ficheiro de configuração: <<CODE1>>

Se usar o env var, não há necessidade de adicionar token à configuração. O gateway lê <<CODE0>> automaticamente.

Reiniciar para aplicar:

```bash
exit
fly machine restart <machine-id>
```

# # 6) Acesse o portal

# # Controlar a UI

Abrir no navegador:

```bash
fly open
```

Ou visite <<CODE0>>

Colar seu token de gateway ( aquele de <<CODE0>>) para autenticar.

Diários

```bash
fly logs              # Live logs
fly logs --no-tail    # Recent logs
```

Consola SSH

```bash
fly ssh console
```

# # Resolução de problemas

### "App não está a ouvir no endereço esperado"

O gateway é ligado a <<CODE0>> em vez de <<CODE1>>>.

**Fix:** Adicionar <<CODE0>>> ao seu comando de processo em <<CODE1>>>.

## # Verificações de saúde falhando / conexão recusada

Voar não pode alcançar o gateway na porta configurada.

**Fix:** Assegure-se que <<CODE0> corresponde à porta de gateway (set <<CODE1>> ou <<CODE2>>).

OOM / Questões de memória

O contentor continua a reiniciar ou a morrer. Sinais: <<CODE0>>, <<CODE1>>, ou reiniciações silenciosas.

**Fix:** Aumentar a memória em <<CODE0>>:

```toml
[[vm]]
  memory = "2048mb"
```

Ou atualizar uma máquina existente:

```bash
fly machine update <machine-id> --vm-memory 2048 -y
```

**Nota:** 512MB é muito pequeno. 1GB pode funcionar, mas pode OOM sob carga ou com registro de verbose. ** 2GB é recomendado. **

## # Questões de bloqueio de porta

Gateway se recusa a começar com erros "já em execução".

Isso acontece quando o recipiente reinicia, mas o arquivo de bloqueio PID persiste no volume.

**Fix:** Apagar o ficheiro de bloqueio:

```bash
fly ssh console --command "rm -f /data/gateway.*.lock"
fly machine restart <machine-id>
```

O arquivo de bloqueio está em <<CODE0>> (não em um subdiretório).

## # Config não ser lido

Se usar <<CODE0>>, o gateway cria uma configuração mínima. Sua configuração personalizada em <<CODE1>> deve ser lida ao reiniciar.

Verificar a configuração existe:

```bash
fly ssh console --command "cat /data/openclaw.json"
```

### Gravando configuração via SSH

O comando <<CODE0> não suporta redirecionamento de shell. Para gravar um arquivo de configuração:

```bash
# Use echo + tee (pipe from local to remote)
echo '{"your":"config"}' | fly ssh console -C "tee /data/openclaw.json"

# Or use sftp
fly sftp shell
> put /local/path/config.json /data/openclaw.json
```

**Nota:** <<CODE0>> pode falhar se o arquivo já existir. Apagar primeiro:

```bash
fly ssh console --command "rm /data/openclaw.json"
```

# # Não Persiste

Se você perder credenciais ou sessões após um reinício, a dir estado está escrevendo para o sistema de arquivos de contêiner.

**Fix:** Assegure-se de que <<CODE0>> está definido em <<CODE1>>> e resetloy.

# # Atualizações

```bash
# Pull latest changes
git pull

# Redeploy
fly deploy

# Check health
fly status
fly logs
```

Comando da Máquina de Actualização

Se você precisar alterar o comando de inicialização sem uma reinstalação completa:

```bash
# Get machine ID
fly machines list

# Update command
fly machine update <machine-id> --command "node dist/index.js gateway --port 3000 --bind lan" -y

# Or with memory increase
fly machine update <machine-id> --vm-memory 2048 --command "node dist/index.js gateway --port 3000 --bind lan" -y
```

**Nota:** Após <<CODE0>>, o comando da máquina pode reiniciar para o que está em <<CODE1>>. Se você fez alterações manuais, volte a aplicá-las após a implantação.

# # Implantação privada (reforçada)

Por padrão, Fly aloca IPs públicos, tornando seu gateway acessível em <<CODE0>>. Isso é conveniente, mas significa que sua implantação é detectável por scanners de internet (Shodan, Censys, etc.).

Para uma implantação endurecida com ** nenhuma exposição pública**, use o modelo privado.

## # Quando usar a implantação privada

- Você só faz **outbound** chamadas / mensagens (sem webhooks de entrada)
- Você usa **ngrok ou Tailscale** túneis para qualquer chamada webhook
- Você acessa o gateway via **SSH, proxy ou WireGuard** em vez de navegador
- Você quer a implantação ** escondida de scanners de internet**

Configuração

Usar <<CODE0>> em vez da configuração padrão:

```bash
# Deploy with private config
fly deploy -c fly.private.toml
```

Ou converter uma implantação existente:

```bash
# List current IPs
fly ips list -a my-openclaw

# Release public IPs
fly ips release <public-ipv4> -a my-openclaw
fly ips release <public-ipv6> -a my-openclaw

# Switch to private config so future deploys don't re-allocate public IPs
# (remove [http_service] or deploy with the private template)
fly deploy -c fly.private.toml

# Allocate private-only IPv6
fly ips allocate-v6 --private -a my-openclaw
```

Depois disto, <<CODE0>> deve mostrar apenas um IP do tipo <<CODE1>:

```
VERSION  IP                   TYPE             REGION
v6       fdaa:x:x:x:x::x      private          global
```

A aceder a uma implantação privada

Como não há URL pública, use um desses métodos:

**Opção 1: Proxy local (simples)**

```bash
# Forward local port 3000 to the app
fly proxy 3000:3000 -a my-openclaw

# Then open http://localhost:3000 in browser
```

** Opção 2: WireGuard VPN**

```bash
# Create WireGuard config (one-time)
fly wireguard create

# Import to WireGuard client, then access via internal IPv6
# Example: http://[fdaa:x:x:x:x::x]:3000
```

**Opção 3: SSH apenas

```bash
fly ssh console -a my-openclaw
```

## # Webhooks com implantação privada

Se você precisar de callbacks webhook (Twilio, Telnyx, etc.) sem exposição pública:

1. ** túnel ngrok** - Corre ngrok dentro do recipiente ou como um sidecar
2. ** Funil Tailscale** - Expor caminhos específicos via Tailscale
3. **Outbound-only** - Alguns provedores (Twilio) funcionam bem para chamadas de saída sem webhooks

Configuração da chamada de voz de exemplo com ngrok:

```json
{
  "plugins": {
    "entries": {
      "voice-call": {
        "enabled": true,
        "config": {
          "provider": "twilio",
          "tunnel": { "provider": "ngrok" }
        }
      }
    }
  }
}
```

O túnel ngrok é executado dentro do recipiente e fornece uma URL webhook pública sem expor o aplicativo Fly em si.

# # Benefícios de segurança

Aspectos Públicos
----------------- ---------------------------
Varredores de Internet □ Descoberta
Ataques diretos Possíveis Bloqueados
Controle o acesso à interface .. Navegador ..
Entrega do Webhook diretamente via túnel

# # Notas

- Fly.io usa arquitetura **x86** (não ARM)
- O arquivo Docker é compatível com ambas as arquiteturas
- Para WhatsApp/Telegram a bordo, utilizar <<CODE0>
- Os dados persistentes vivem no volume em <<CODE1>>
- Sinal requer Java + sinal-cli; use uma imagem personalizada e manter a memória em 2GB+.

# # Custo

Com a configuração recomendada (<<<CODE0>>, 2GB de RAM):

- ~$10-15/mês dependendo do uso
- Nível livre inclui algum subsídio

Ver [Preços de voo](<<<LINK0>>>) para mais pormenores.
