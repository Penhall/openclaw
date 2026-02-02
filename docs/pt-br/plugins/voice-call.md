---
summary: "Voice Call plugin: outbound + inbound calls via Twilio/Telnyx/Plivo (plugin install + config + CLI)"
read_when:
  - You want to place an outbound voice call from OpenClaw
  - You are configuring or developing the voice-call plugin
---

Chamada de Voz (plugin)

Chamadas de voz para OpenClaw através de um plugin. Apoia notificações de saída e
Conversas multiturnos com políticas de entrada.

Prestadores actuais:

- <<CODE0> (Voz programável + Fluxos de mídia)
- <<CODE1> (controlo de chamada v2)
- <<CODE2> (Voz API + transferência XML + discurso de entrada)
- <<CODE3> (dev/sem rede)

Modelo mental rápido:

- Instalar plugin
- Reinicia o portal.
- Configurar em <<CODE0>
- Utilizar <<CODE1> ou a ferramenta <<CODE2>

# # Onde corre (local vs remoto)

O plugin Voice Call é executado ** dentro do processo Gateway**.

Se você usar um Gateway remoto, instale/configure o plugin na máquina ** rodando o Gateway**, então reinicie o Gateway para carregá-lo.

Instalar

# # # Opção A: instalar a partir do npm (recomendado)

```bash
openclaw plugins install @openclaw/voice-call
```

Reinicie o portal depois.

## # Opção B: instalar a partir de uma pasta local (dev, sem cópia)

```bash
openclaw plugins install ./extensions/voice-call
cd ./extensions/voice-call && pnpm install
```

Reinicie o portal depois.

Configuração

Definir configuração em `plugins.entries.voice-call.config`:

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        enabled: true,
        config: {
          provider: "twilio", // or "telnyx" | "plivo" | "mock"
          fromNumber: "+15550001234",
          toNumber: "+15550005678",

          twilio: {
            accountSid: "ACxxxxxxxx",
            authToken: "...",
          },

          plivo: {
            authId: "MAxxxxxxxxxxxxxxxxxxxx",
            authToken: "...",
          },

          // Webhook server
          serve: {
            port: 3334,
            path: "/voice/webhook",
          },

          // Public exposure (pick one)
          // publicUrl: "https://example.ngrok.app/voice/webhook",
          // tunnel: { provider: "ngrok" },
          // tailscale: { mode: "funnel", path: "/voice/webhook" }

          outbound: {
            defaultMode: "notify", // notify | conversation
          },

          streaming: {
            enabled: true,
            streamPath: "/voice/stream",
          },
        },
      },
    },
  },
}
```

Notas:

- Twilio/Telnyx exigem uma URL ** publicamente acessível** webhook.
- Plivo requer uma URL ** publicamente acessível** webhook.
- <<CODE0> é um provedor local de dev (sem chamadas de rede).
- <<CODE1> é apenas para testes locais.
- Se você usar o ngrok free layer, defina `publicUrl` para o URL exato do ngrok; a verificação da assinatura é sempre executada.
- <<CODE3> permite que Twilio webhooks com assinaturas inválidas **apenas** quando `tunnel.provider="ngrok"` e <<CODE5> é loopback (agente local ngrok). Usar apenas para o dev local.
- URLs livres de Ngrok podem alterar ou adicionar comportamento intersticial; se `publicUrl` deriva, as assinaturas Twilio falharão. Para a produção, prefira um domínio estável ou funil Tailscale.

# # TTS para chamadas

Voice Call usa a configuração do núcleo <<CODE0> (OpenAI ou OnzeLabs) para
A transmitir o discurso nas chamadas. Você pode substituí-lo sob a configuração do plugin com o
**A mesma forma** — ela se funde com `messages.tts`.

```json5
{
  tts: {
    provider: "elevenlabs",
    elevenlabs: {
      voiceId: "pMsXgVXv3BLzUgSXRplE",
      modelId: "eleven_multilingual_v2",
    },
  },
}
```

Notas:

- **Edge TTS é ignorado para chamadas de voz** (necessidades de áudio de telefonia PCM; saída de borda não é confiável).
- Core TTS é usado quando a transmissão de mídia Twilio está habilitada; caso contrário chamadas voltar para provedor vozes nativas.

# # Mais exemplos

Usar apenas o núcleo TTS (sem sobreposição):

```json5
{
  messages: {
    tts: {
      provider: "openai",
      openai: { voice: "alloy" },
    },
  },
}
```

Sobrescrever para OnzeLabs apenas para chamadas (mantenha o padrão do núcleo em outro lugar):

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          tts: {
            provider: "elevenlabs",
            elevenlabs: {
              apiKey: "elevenlabs_key",
              voiceId: "pMsXgVXv3BLzUgSXRplE",
              modelId: "eleven_multilingual_v2",
            },
          },
        },
      },
    },
  },
}
```

Substituir apenas o modelo OpenAI para chamadas (exemplo de fusão profunda):

```json5
{
  plugins: {
    entries: {
      "voice-call": {
        config: {
          tts: {
            openai: {
              model: "gpt-4o-mini-tts",
              voice: "marin",
            },
          },
        },
      },
    },
  },
}
```

# # Chamadas de entrada

Política de entrada padrão para `disabled`. Para ativar chamadas de entrada, defina:

```json5
{
  inboundPolicy: "allowlist",
  allowFrom: ["+15550001234"],
  inboundGreeting: "Hello! How can I help?",
}
```

As respostas automáticas usam o sistema do agente. Sintonizar com:

- <<CODE0>
- <<CODE1>
- <<CODE2>

# # CLI

```bash
openclaw voicecall call --to "+15555550123" --message "Hello from OpenClaw"
openclaw voicecall continue --call-id <id> --message "Any questions?"
openclaw voicecall speak --call-id <id> --message "One moment"
openclaw voicecall end --call-id <id>
openclaw voicecall status --call-id <id>
openclaw voicecall tail
openclaw voicecall expose --mode funnel
```

# # Ferramenta de agente

Nome da ferramenta: `voice_call`

Acções:

- <<CODE0> (mensagem, para?, modo?)
- <<CODE1> (chamada, mensagem)
- <<CODE2> (chamada, mensagem)
- <<CODE3> (chamada Id)
- <<CODE4> (chamada Id)

Este repo envia um documento de habilidade correspondente em `skills/voice-call/SKILL.md`.

# # Porta RCP

- <<CODE0> (`to?`, `message`, `mode?`)
- <<CODE4> (`callId`, `message`)
- `voicecall.speak` (`callId`, `message`)
- `voicecall.end` (`callId`)
- `voicecall.status` (`callId`)
