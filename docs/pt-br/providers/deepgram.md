---
summary: "Deepgram transcription for inbound voice notes"
read_when:
  - You want Deepgram speech-to-text for audio attachments
  - You need a quick Deepgram config example
---

# Deepgram (Audio Transcription)

Deepgram é uma API de discurso-texto. No OpenClaw é usado para ** entrada de nota de áudio / voz
transcrição** via `tools.media.audio`.

Quando habilitado, o OpenClaw envia o arquivo de áudio para Deepgram e injeta a transcrição
para o gasoduto de resposta (<`{{Transcript}}` + `[Audio]` bloco). Isto é ** not streaming**;
utiliza o endpoint de transcrição pré-gravado.

Sítio Web: https://deepgram.com
Docs: https://developers.deepgram.com

# # Começo rápido

1. Defina sua chave de API:

```
DEEPGRAM_API_KEY=dg_...
```

2. Habilitar o provedor:

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "deepgram", model: "nova-3" }],
      },
    },
  },
}
```

# # Opções

- <<CODE0>: Deepgram model id (padrão: `nova-3`)
- <<CODE2>: dica de idioma (opcional)
- `tools.media.audio.providerOptions.deepgram.detect_language`: habilitar a detecção de linguagem (opcional)
- <<CODE4>: habilitar pontuação (opcional)
- <<CODE5>: habilitar a formatação inteligente (opcional)

Exemplo com linguagem:

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [{ provider: "deepgram", model: "nova-3", language: "en" }],
      },
    },
  },
}
```

Exemplo com opções Deepgram:

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        providerOptions: {
          deepgram: {
            detect_language: true,
            punctuate: true,
            smart_format: true,
          },
        },
        models: [{ provider: "deepgram", model: "nova-3" }],
      },
    },
  },
}
```

# # Notas

- A autenticação segue a ordem de autenticação padrão do provedor; <<CODE0> é o caminho mais simples.
- Substituir endpoints ou cabeçalhos com `tools.media.audio.baseUrl` e `tools.media.audio.headers` ao utilizar um proxy.
- A saída segue as mesmas regras de áudio que os outros provedores (tapas de tamanho, timeouts, injeção de transcrição).
