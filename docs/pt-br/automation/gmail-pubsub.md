---
summary: "Gmail Pub/Sub push wired into OpenClaw webhooks via gogcli"
read_when:
  - Wiring Gmail inbox triggers to OpenClaw
  - Setting up Pub/Sub push for agent wake
---

# Gmail Pub/Sub -> Openclaw

Objetivo: Gmail watch -> Pub/Sub push ->`gog gmail watch serve`-> OpenClaw webhook.

## Pré-reques

-`gcloud`instalado e conectado ([guia de instalação]https://docs.cloud.google.com/sdk/docs/install-sdk.
-`gog`(gogcli) instalado e autorizado para a conta Gmail ([gogcli.sh]https://gogcli.sh/.
- Ganchos OpenClaw ativados (ver [Webhooks] /automation/webhook.
-`tailscale`conectado ([tailscale.com]https://tailscale.com/. A configuração suportada usa o Funnel Tailscale para o endpoint público HTTPS.
Outros serviços de túnel podem funcionar, mas são DIY / não suportado e requerem fiação manual.
Neste momento, Tailscale é o que apoiamos.

Configuração do gancho de exemplo (ativar mapeamento predefinido do Gmail):

```json5
{
  hooks: {
    enabled: true,
    token: "OPENCLAW_HOOK_TOKEN",
    path: "/hooks",
    presets: ["gmail"],
  },
}
```

Para entregar o resumo do Gmail a uma superfície de bate-papo, sobreponha a predefinição com um mapeamento
que define`deliver`+`channel`/`to`opcional:

```json5
{
  hooks: {
    enabled: true,
    token: "OPENCLAW_HOOK_TOKEN",
    presets: ["gmail"],
    mappings: [
      {
        match: { path: "gmail" },
        action: "agent",
        wakeMode: "now",
        name: "Gmail",
        sessionKey: "hook:gmail:{{messages[0].id}}",
        messageTemplate: "New email from {{messages[0].from}}\nSubject: {{messages[0].subject}}\n{{messages[0].snippet}}\n{{messages[0].body}}",
        model: "openai/gpt-5.2-mini",
        deliver: true,
        channel: "last",
        // to: "+15551234567"
      },
    ],
  },
}
```

Se quiser um canal fixo, defina`channel`+`to`. Caso contrário,`channel: "last"`usa a última rota de entrega (cai de volta para WhatsApp).

Para forçar um modelo mais barato para execução do Gmail, defina`model`no mapeamento
`provider/model`ou alias). Se você aplicar`agents.defaults.models`, incluí-lo lá.

Para definir um modelo padrão e nível de pensamento especificamente para ganchos Gmail, adicione`hooks.gmail.model`/`hooks.gmail.thinking`na sua configuração:

```json5
{
  hooks: {
    gmail: {
      model: "openrouter/meta-llama/llama-3.3-70b-instruct:free",
      thinking: "off",
    },
  },
}
```

Notas:

- Per-hook`model`/`thinking`no mapeamento ainda substitui esses padrões.
- Ordem de retirada:`hooks.gmail.model`→`agents.defaults.model.fallbacks`→ primário (auth/rate-limit/timeouts).
- Se o`agents.defaults.models`estiver definido, o modelo Gmail deve estar na lista de permissões.
- O conteúdo do gancho Gmail é embrulhado com limites de segurança de conteúdo externo por padrão.
Para desativar (perigoso), configure`hooks.gmail.allowUnsafeExternalContent: true`.

Para personalizar ainda mais o manuseio de carga útil, adicione`hooks.mappings`ou um módulo de transformação JS/TS`hooks.transformsDir`(ver [Webhooks]/automation/webhook.

## Wizard (recomendado)

Use o helper OpenClaw para juntar tudo (instala deps no macOS via brew):

```bash
openclaw webhooks gmail setup \
  --account openclaw@gmail.com
```

Predefinição:

- Usa Funil Tailscale para o ponto final público.
- Escreve configuração`hooks.gmail`para`openclaw webhooks gmail run`.
- Activa a predefinição do gancho Gmail `hooks.presets: ["gmail"]`.

Nota de localização: quando o`tailscale.mode`está activo, o OpenClaw define automaticamente`hooks.gmail.serve.path`a`/``hooks.gmail.tailscale.path`(padrão`/gmail-pubsub` porque escala de cauda
strips o prefixo set-path antes de proxy.
Se você precisar da infra- estrutura para receber o caminho prefixado, defina`hooks.gmail.tailscale.target`(ou`--tailscale-target` para um URL completo como`http://127.0.0.1:8788/gmail-pubsub`e correspondem ao`hooks.gmail.serve.path`.

Quer um endpoint personalizado? Utilizar`--push-endpoint <url>`ou`--tailscale off`.

Nota da plataforma: no macOS o assistente instala`gcloud`,`gogcli`e`tailscale`via Homebrew; no Linux instale-os manualmente primeiro.

Auto- arranque do Gateway (recomendado):

- Quando o`hooks.enabled=true`e o`hooks.gmail.account`são definidos, o portal começa`gog gmail watch serve`no arranque e renova automaticamente o relógio.
- Defina o`OPENCLAW_SKIP_GMAIL_WATCHER=1`para optar por fora (útil se você mesmo executar o daemon).
- Não executar o daemon manual ao mesmo tempo, ou você irá bater`listen tcp 127.0.0.1:8788: bind: address already in use`.

Servidor manual (inicia`gog gmail watch serve`+ renovação automática):

```bash
openclaw webhooks gmail run
```

## Uma vez

1. Selecione o projeto GCP ** que possui o cliente OAuth** usado pelo`gog`.

```bash
gcloud auth login
gcloud config set project <project-id>
```

Nota: O Gmail watch requer que o tópico Pub/Sub viva no mesmo projeto que o cliente OAuth.

2. Habilitar APIs:

```bash
gcloud services enable gmail.googleapis.com pubsub.googleapis.com
```

3. Criar um tópico:

```bash
gcloud pubsub topics create gog-gmail-watch
```

4. Permitir que o Gmail push publique:

```bash
gcloud pubsub topics add-iam-policy-binding gog-gmail-watch \
  --member=serviceAccount:gmail-api-push@system.gserviceaccount.com \
  --role=roles/pubsub.publisher
```

## Começa o relógio

```bash
gog gmail watch start \
  --account openclaw@gmail.com \
  --label INBOX \
  --topic projects/<project-id>/topics/gog-gmail-watch
```

Salve o`history_id`da saída (para depuração).

## Corre o manipulador de empurrar

Exemplo local (autenticação partilhada):

```bash
gog gmail watch serve \
  --account openclaw@gmail.com \
  --bind 127.0.0.1 \
  --port 8788 \
  --path /gmail-pubsub \
  --token <shared> \
  --hook-url http://127.0.0.1:18789/hooks/gmail \
  --hook-token OPENCLAW_HOOK_TOKEN \
  --include-body \
  --max-bytes 20000
```

Notas:

-`--token`protege o endpoint de impulso `x-gog-token`ou`?token=`.
-`--hook-url`aponta para OpenClaw`/hooks/gmail`(mapeado; execução isolada + resumo para o principal).
-`--include-body`e`--max-bytes`controlam o trecho do corpo enviado para OpenClaw.

Recomendado:`openclaw webhooks gmail run`envolve o mesmo fluxo e renova automaticamente o relógio.

## Expor o manipulador (avançado, não suportado)

Se você precisar de um túnel não-tailscale, rode-o manualmente e use o URL público no push
subscrição (não suportada, sem guardas):

```bash
cloudflared tunnel --url http://127.0.0.1:8788 --no-autoupdate
```

Use o URL gerado como o ponto final do push:

```bash
gcloud pubsub subscriptions create gog-gmail-watch-push \
  --topic gog-gmail-watch \
  --push-endpoint "https://<public-url>/gmail-pubsub?token=<shared>"
```

Produção: use um endpoint HTTPS estável e configure Pub/Sub OIDC JWT, então execute:

```bash
gog gmail watch serve --verify-oidc --oidc-email <svc@...>
```

Teste

Enviar uma mensagem para a caixa de entrada vigiada:

```bash
gog gmail send \
  --account openclaw@gmail.com \
  --to openclaw@gmail.com \
  --subject "watch test" \
  --body "ping"
```

Verifique o estado e o histórico do relógio:

```bash
gog gmail watch status --account openclaw@gmail.com
gog gmail history --account openclaw@gmail.com --since <historyId>
```

## Resolução de problemas

-`Invalid topicName`: descompasso do projecto (não no projecto cliente OAuth).
-`User not authorized`: Falta o`roles/pubsub.publisher`sobre o tema.
- Mensagens vazias: O Gmail push apenas fornece`historyId`; buscar via`gog gmail history`.

## Limpeza

```bash
gog gmail watch stop --account openclaw@gmail.com
gcloud pubsub subscriptions delete gog-gmail-watch-push
gcloud pubsub topics delete gog-gmail-watch
```
