---
summary: "Inbound image/audio/video understanding (optional) with provider + CLI fallbacks"
read_when:
  - Designing or refactoring media understanding
  - Tuning inbound audio/video/image preprocessing
---

# Compreensão de mídia (inbound) — 2026-01-17

OpenClaw pode **summarize inbound media** (image/audio/video) antes que o pipeline de resposta seja executado. Ele detecta automaticamente quando ferramentas locais ou chaves de provedor estão disponíveis, e pode ser desativado ou personalizado. Se o entendimento estiver desligado, os modelos ainda recebem os arquivos/URLs originais como de costume.

# # Objetivos

- Opcional: digerir pré-digerir mídias de entrada em texto curto para roteamento mais rápido + melhor análise de comando.
- Preservar a entrega de mídia original para o modelo (sempre).
- Suporte ** APIs provedor** e **fallbacks CLI**.
- Permitir vários modelos com backback ordenado (error/size/timeout).

# # Comportamento de alto nível

1. Recolha anexos (<<<CODE0>>, <<CODE1>>, <<CODE2>>>).
2. Para cada capacidade ativada (imagem/áudio/vídeo), selecione anexos por política (padrão: **primeiro**).
3. Escolha a primeira entrada do modelo elegível (tamanho + capacidade + autenticação).
4. Se um modelo falhar ou a mídia for muito grande, **regressa à próxima entrada**.
5. Sobre o sucesso:
- <<CODE3>> torna-se <<CODE4>>, <<CODE5>>>, ou <<CODE6>>bloqueio.
- Conjuntos de áudio <<CODE7>>; análise de comandos usa texto de legenda quando presente,
Caso contrário, a transcrição.
- As legendas são preservadas como <<CODE8>> dentro do bloco.

Se o entendimento falhar ou estiver desativado, **o fluxo de resposta continua** com o corpo original + anexos.

# # Visão geral da configuração

<<CODE0> suporta ** modelos compartilhados** mais sobreposições de capacidade:

- <<CODE0>>: lista de modelos partilhada (usar <<CODE1>> para porta).
- <<CODE2>>/ <<CODE3>>/ <<CODE4>:
- padrões (<<<CODE5>>, <<CODE6>>, <<CODE7>>, <<CODE8>>, <<CODE9>>)
- o fornecedor substitui (<<<CODE10>>, <<CODE11>>, <<CODE12>>)
- Opções de áudio Deepgram via <<CODE13>>
- lista opcional **percapabilidade <<CODE14>>** (preferidos antes de modelos partilhados)
- <<CODE15>> política (<<CODE16>>, <<CODE17>>, <<CODE18>>)
- <<CODE19>> (portagem opcional por canal/tipo de conversação/sessão)
- <<CODE20>>: máxima capacidade concorrente roda (padrão **2**).

```json5
{
  tools: {
    media: {
      models: [
        /* shared list */
      ],
      image: {
        /* optional overrides */
      },
      audio: {
        /* optional overrides */
      },
      video: {
        /* optional overrides */
      },
    },
  },
}
```

## # Modelo de entradas

Cada entrada <<CODE0> pode ser **fornecedor** ou **CLI**:

```json5
{
  type: "provider", // default if omitted
  provider: "openai",
  model: "gpt-5.2",
  prompt: "Describe the image in <= 500 chars.",
  maxChars: 500,
  maxBytes: 10485760,
  timeoutSeconds: 60,
  capabilities: ["image"], // optional, used for multi‑modal entries
  profile: "vision-profile",
  preferredProfile: "vision-fallback",
}
```

```json5
{
  type: "cli",
  command: "gemini",
  args: [
    "-m",
    "gemini-3-flash",
    "--allowed-tools",
    "read_file",
    "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
  ],
  maxChars: 500,
  maxBytes: 52428800,
  timeoutSeconds: 120,
  capabilities: ["video", "image"],
}
```

Os modelos CLI também podem usar:

- <<CODE0>> (diretório que contém o ficheiro multimédia)
- <<CODE1>> (direcção de scratch criada para esta execução)
- <<CODE2>> (scratch arquivo caminho base, sem extensão)

# # Predefinições e limites

Predefinição recomendada:

- <<CODE0>: **500** para imagem/vídeo (curto, amigável a comandos)
- <<CODE1>: **unset** para áudio (transcrição completa, a menos que você defina um limite)
- <<CODE2>>:
- imagem: **10MB**
- áudio: **20MB**
- vídeo: **50MB**

Regras:

- Se a mídia exceder <<CODE0>>, esse modelo é ignorado e o **próximo modelo é tentado**.
- Se o modelo retornar mais do que <<CODE1>>, a saída é aparada.
- <<CODE2> defaults to simple “Descreva o {media}.” mais a orientação <<CODE3> (imagem/vídeo somente).
- Se <<CODE4> mas nenhum modelo está configurado, OpenClaw tenta o
** modelo de resposta ativa** quando seu provedor suporta a capacidade.

## # Detectar automaticamente a compreensão da mídia (por omissão)

Se <<CODE0> não estiver ** definido para <<CODE1>> e não tiver
modelos configurados, OpenClaw detecta automaticamente nesta ordem e ** para no primeiro
opção de trabalho**:

1. **CLIs locais** (audio somente; se instalado)
- <<CODE0> (necessários <<CODE1>> com codificador/decodificador/juntar/pedras)
- <<CODE2>> (<<CODE3>>; usa <<CODE4>> ou o modelo minúsculo empacotado)
- <<CODE5>> (Python CLI; baixa modelos automaticamente)
2. ** Gemini CLI** (<<<CODE6>>>) utilizando <<CODE7>>
3. ** Chaves do fornecedor**
- Áudio: OpenAI → Groq → Deepgram → Google
- Imagem: OpenAI → Antrópico → Google → MiniMax
- Vídeo: Google

Para desactivar a detecção automática, definir:

```json5
{
  tools: {
    media: {
      audio: {
        enabled: false,
      },
    },
  },
}
```

Nota: A detecção binária é o melhor esforço em macOS/Linux/Windows; garanta que o CLI esteja em <<CODE0>> (expandimos <<CODE1>>), ou definimos um modelo CLI explícito com um caminho de comando completo.

# # Capacidades (opcional)

Se você definir <<CODE0>>, a entrada só será executada para esses tipos de mídia. Para compartilhado
listas, OpenClaw pode inferir padrões:

- <<CODE0>>, <<CODE1>>, <<CODE2>>: ** imagem**
- <<CODE3> (A API Gemini): **imagem + áudio + vídeo**
- <<CODE4>: **audio**
- <<CODE5>: **audio**

Para as entradas CLI, **set <<CODE0>> explicitamente** para evitar coincidências.
Se omitir <<CODE1>>, a entrada é elegível para a lista em que aparece.

# # Matriz de suporte do provedor (integrações OpenClaw)

Capacidade Integração do fornecedor Notas
□ ----------------------------------------------------------------------------------------------------------------------------------------------------------
□ Imagem □ OpenAI / Anthropic / Google / others via <<CODE0> Qualquer modelo capaz de imagem no registro funciona. □
□ Áudio • OpenAI, Groq, Deepgram, Google • Transcrição do provedor (Whisper/Deepgram/Gemini).
Vídeo do Google (A API Gemini)

# # Fornecedores recomendados

**Imagem**

- Prefere o seu modelo ativo se ele suporta imagens.
- Bons padrões: <<CODE0>>, <<CODE1>>, <<CODE2>>.

**Audio**

- <<CODE0>>, <<CODE1>>>, ou <<CODE2>>>.
- Retrocesso do CLI: <<CODE3> (whisper- cpp) ou <<CODE4>>.
- Configuração do Deepgram: [Deepgram (tradução do áudio)] (<<<LINK0>>>).

**Vídeo**

- <<CODE0> (rápido), <<CODE1>> (mais rico).
- Retrocesso CLI: <<CODE2>> CLI (suporta <<CODE3>> em vídeo/áudio).

# # Política de anexo

Controlos de capacidade <<CODE0>> que processam os anexos:

- <<CODE0>>: <<CODE1>> (padrão) ou <<CODE2>>
- <<CODE3>>: tampar o número processado (padrão **1**)
- <<CODE4>>: <<CODE5>>, <<CODE6>>, <<CODE7>>, <<CODE8>

Quando <<CODE0>>, as saídas são marcadas <<CODE1>>, <<CODE2>>, etc.

# # Exemplos de configuração

# # # 1) Lista de modelos compartilhados + sobreposições

```json5
{
  tools: {
    media: {
      models: [
        { provider: "openai", model: "gpt-5.2", capabilities: ["image"] },
        {
          provider: "google",
          model: "gemini-3-flash-preview",
          capabilities: ["image", "audio", "video"],
        },
        {
          type: "cli",
          command: "gemini",
          args: [
            "-m",
            "gemini-3-flash",
            "--allowed-tools",
            "read_file",
            "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
          ],
          capabilities: ["image", "video"],
        },
      ],
      audio: {
        attachments: { mode: "all", maxAttachments: 2 },
      },
      video: {
        maxChars: 500,
      },
    },
  },
}
```

### 2) Áudio + Vídeo apenas (imagem desligada)

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [
          { provider: "openai", model: "gpt-4o-mini-transcribe" },
          {
            type: "cli",
            command: "whisper",
            args: ["--model", "base", "{{MediaPath}}"],
          },
        ],
      },
      video: {
        enabled: true,
        maxChars: 500,
        models: [
          { provider: "google", model: "gemini-3-flash-preview" },
          {
            type: "cli",
            command: "gemini",
            args: [
              "-m",
              "gemini-3-flash",
              "--allowed-tools",
              "read_file",
              "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
            ],
          },
        ],
      },
    },
  },
}
```

# # # 3) compreensão opcional da imagem

```json5
{
  tools: {
    media: {
      image: {
        enabled: true,
        maxBytes: 10485760,
        maxChars: 500,
        models: [
          { provider: "openai", model: "gpt-5.2" },
          { provider: "anthropic", model: "claude-opus-4-5" },
          {
            type: "cli",
            command: "gemini",
            args: [
              "-m",
              "gemini-3-flash",
              "--allowed-tools",
              "read_file",
              "Read the media at {{MediaPath}} and describe it in <= {{MaxChars}} characters.",
            ],
          },
        ],
      },
    },
  },
}
```

# # # 4) Entrada única multimodal (capacidades explícitas)

```json5
{
  tools: {
    media: {
      image: {
        models: [
          {
            provider: "google",
            model: "gemini-3-pro-preview",
            capabilities: ["image", "video", "audio"],
          },
        ],
      },
      audio: {
        models: [
          {
            provider: "google",
            model: "gemini-3-pro-preview",
            capabilities: ["image", "video", "audio"],
          },
        ],
      },
      video: {
        models: [
          {
            provider: "google",
            model: "gemini-3-pro-preview",
            capabilities: ["image", "video", "audio"],
          },
        ],
      },
    },
  },
}
```

# # Saída de status

Quando o entendimento da mídia é executado, <<CODE0>> inclui uma breve linha sumária:

```
📎 Media: image ok (openai/gpt-5.2) · audio skipped (maxBytes)
```

Isto mostra resultados de capacidade e o provedor/modelo escolhido quando aplicável.

# # Notas

- Entender é ** melhor-esforço**. Os erros não bloqueiam as respostas.
- Os anexos ainda são passados para modelos mesmo quando o entendimento é desativado.
- Utilizar <<CODE0>> para limitar a compreensão (por exemplo, apenas DM).

# # Docs relacionados

- [Configuração] (<<<<LINK0>>)
- [Suporte de Imagem e Mídia] (<<<LINK1>>>)
