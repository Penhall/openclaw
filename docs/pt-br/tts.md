---
summary: "Text-to-speech (TTS) for outbound replies"
read_when:
  - Enabling text-to-speech for replies
  - Configuring TTS providers or limits
  - Using /tts commands
---

# Texto-para-fala (TTS)

OpenClaw pode converter respostas de saída em áudio usando OnzeLabs, OpenAI ou Edge TTS.
Funciona em qualquer lugar que o OpenClaw possa enviar áudio; o Telegram recebe uma bolha redonda de notas de voz.

# # Serviços suportados

- **ElevenLabs** (fornecedor primário ou secundário)
- ** OpenAI** (fornecedor primário ou secundário; também utilizado para resumos)
- **Edge TTS** (fornecedor primário ou fallback; usa <<CODE0>>, padrão quando não há chaves API)

# # Notas TTS borda

Edge TTS usa o serviço de TTS neural on-line da Microsoft Edge através do <<CODE0>
biblioteca. É um serviço hospedado (não local), usa endpoints da Microsoft, e faz
não requer uma chave API. <<CODE1>> expõe as opções de configuração de voz e
formatos de saída, mas nem todas as opções são suportadas pelo serviço Edge. Pesquisa por turnos

Porque Edge TTS é um serviço público web sem um SLA publicado ou quota, tratá-lo
Como melhor esforço. Se você precisar de limites garantidos e suporte, use OpenAI ou OnzeLabs.
Microsoft Speech REST API documenta um limite de áudio de 10 minutos por solicitação; Edge TTS
não publica limites, por isso assume limites semelhantes ou inferiores. Pesquisa por turnos

# # Teclas opcionais

Se você quiser OpenAI ou OnzeLabs:

- <<CODE0> (ou <<CODE1>>)
- <<CODE2>>

Edge TTS faz **not** requer uma chave API. Se não forem encontradas chaves de API, o OpenClaw é padrão
to Edge TTS (a menos que desabilitado via <<CODE0>>>).

Se vários provedores estão configurados, o provedor selecionado é usado primeiro e os outros são opções de backback.
Auto-síntese usa o configurado <<CODE0>> (ou <<CODE1>>>),
para que o provedor também deve ser autenticado se você permitir resumos.

# # Ligações de serviço

- [Guia Texto- para- Fala OpenAI] (<<<LINK0>>)
- [Referência da API de áudio OpenAI] (<<<LINK1>>>)
(<<<LINK2>>>)
- [Autenticação ElevenLabs] (<<<LINK3>>>)
- [node-edge-tts] (<<<LINK4>>>)
- [Formatos de saída Microsoft Speech] (<<<LINK5>>>)

# # Está habilitado por padrão?

Não. Auto-TTS é ** off** por padrão. Activar a configuração com
<<CODE0>> ou por sessão com <<CODE1>> (também conhecido por <<CODE2>>>).

Edge TTS ** é ** ativado por padrão uma vez que TTS está ligado, e é usado automaticamente
quando nenhuma chave OpenAI ou OnzeLabs API estão disponíveis.

Configuração

A configuração do TTS vive em <<CODE0>> em <<CODE1>>.
O esquema completo está na configuração [Gateway] (<<<LINK0>>>).

### Configuração mínima (activa + fornecedor)

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "elevenlabs",
    },
  },
}
```

## # OpenAI primário com Onze Labs back

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "openai",
      summaryModel: "openai/gpt-4.1-mini",
      modelOverrides: {
        enabled: true,
      },
      openai: {
        apiKey: "openai_api_key",
        model: "gpt-4o-mini-tts",
        voice: "alloy",
      },
      elevenlabs: {
        apiKey: "elevenlabs_api_key",
        baseUrl: "https://api.elevenlabs.io",
        voiceId: "voice_id",
        modelId: "eleven_multilingual_v2",
        seed: 42,
        applyTextNormalization: "auto",
        languageCode: "en",
        voiceSettings: {
          stability: 0.5,
          similarityBoost: 0.75,
          style: 0.0,
          useSpeakerBoost: true,
          speed: 1.0,
        },
      },
    },
  },
}
```

### Primário TTS de borda (sem chave API)

```json5
{
  messages: {
    tts: {
      auto: "always",
      provider: "edge",
      edge: {
        enabled: true,
        voice: "en-US-MichelleNeural",
        lang: "en-US",
        outputFormat: "audio-24khz-48kbitrate-mono-mp3",
        rate: "+10%",
        pitch: "-5%",
      },
    },
  },
}
```

Desactivar os TTS da borda

```json5
{
  messages: {
    tts: {
      edge: {
        enabled: false,
      },
    },
  },
}
```

### Limites personalizados + caminho prefs

```json5
{
  messages: {
    tts: {
      auto: "always",
      maxTextLength: 4000,
      timeoutMs: 30000,
      prefsPath: "~/.openclaw/settings/tts.json",
    },
  },
}
```

## # Apenas responda com áudio após uma nota de voz

```json5
{
  messages: {
    tts: {
      auto: "inbound",
    },
  },
}
```

Desactivar o resumo automático para respostas longas

```json5
{
  messages: {
    tts: {
      auto: "always",
    },
  },
}
```

Em seguida, executar:

```
/tts summary off
```

Notas sobre campos

- <<CODE0>>: modo auto-TTS (<<CODE1>>>, <<CODE2>>, <<CODE3>>, <<CODE4>>).
- <<CODE5> apenas envia áudio após uma nota de voz de entrada.
- <<CODE6> apenas envia áudio quando a resposta inclui <<CODE7> tags.
- <<CODE8>>: alternância legada (o médico migra isto para <<CODE9>>).
- <<CODE10>>: <<CODE11>> (padrão) ou <<CODE12>> (inclui a ferramenta/respostas em bloco).
- <<CODE13>>: <<CODE14>>, <<CODE15>>, ou <<CODE16>> (regresso é automático).
- Se <<CODE17>> for **inset**, OpenClaw prefere <<CODE18>> (se chave), então <<CODE19>> (se a chave),
Caso contrário <<CODE20>>>.
- <<CODE21>>: modelo opcional barato para auto-síntese; padrões para <<CODE22>>.
- Aceita <<CODE23>> ou um alias de modelo configurado.
- <<CODE24>>: permitir que o modelo emita directivas TTS (por omissão).
- <<CODE25>>: tampa dura para entrada TTS (chars). <<CODE26> falha se excedida.
- <<CODE27>>: tempo limite de solicitação (ms).
- <<CODE28>>: substituir o caminho local prefs JSON (fornecedor/limit/summary).
- <<CODE29>> os valores são inferiores aos valores env vars (<<CODE30>/<<CODE31>>, <<CODE32>>).
- <<CODE33>>: sobreponha o URL base da API OnzeLabs.
- <<CODE34>>:
- <<CODE35>>, <<CODE36>>, <<CODE37>>: <<CODE38>>
- <<CODE39>>: <<CODE40>>
- <<CODE41>>: <<CODE42>> (1,0 = normal)
- <<CODE43>>: <<CODE44>>
- <<CODE45>>: ISO 639-1 de 2 letras (por exemplo, <<CODE46>>, <<CODE47>>)
- <<CODE48>>: inteiro <<CODE49>> (melhor determinismo do esforço)
- <<CODE50>>: permitir o uso do TTS Edge (padrão <<CODE51>>; sem chave API).
- <<CODE52>>: Nome da voz neural da borda (por exemplo, <<CODE53>>>).
- <<CODE54>>: código linguístico (por exemplo, <<CODE55>>).
- <<CODE56>>: Formato de saída da borda (por exemplo, <<CODE57>>>).
- Veja os formatos de saída Microsoft Speech para valores válidos; nem todos os formatos são suportados pelo Edge.
- <<CODE58>>/ <<CODE59>>/ <<CODE60>>: cadeias por cento (por exemplo, <<CODE61>>, <<CODE62>>).
- <<CODE63>: escreva legendas JSON ao lado do arquivo de áudio.
- <<CODE64>>: URL proxy para pedidos TTS Edge.
- <<CODE65>>: sobreposição de tempo limite de solicitação (ms).

# # Substituições orientadas por modelos (por omissão)

Por padrão, o modelo ** pode emitir diretivas TTS para uma única resposta.
Quando <<CODE0> é <<CODE1>>, essas diretivas são necessárias para desencadear áudio.

Quando habilitado, o modelo pode emitir <<CODE0>> directivas para substituir a voz
para uma única resposta, mais um bloco opcional <<CODE1>> para
fornecer etiquetas expressivas (risos, pistas de canto, etc) que só devem aparecer em
O áudio.

Exemplo de carga útil de resposta:

```
Here you go.

[[tts:provider=elevenlabs voiceId=pMsXgVXv3BLzUgSXRplE model=eleven_v3 speed=1.1]]
[[tts:text]](laughs) Read the song once more.[[/tts:text]]
```

Chaves de diretiva disponíveis (quando habilitadas):

- < <<CODE0> (<<CODE1>>>
- <<CODE4> (voz do OpenAI) ou <<CODE5> (ElevenLabs)
- <<CODE6>> (Modelo OpenAI TTS ou modelo OnzeLabs id)
- <<CODE7>>, <<CODE8>>, <<CODE9>>, <<CODE10>>, <<CODE11>
- <<CODE12>> (<<CODE13>>>)
- <<CODE14> (ISO 639-1)
- <<CODE15>>

Desactivar todos os comandos do modelo:

```json5
{
  messages: {
    tts: {
      modelOverrides: {
        enabled: false,
      },
    },
  },
}
```

Lista de permissões opcional (desativar sobreposições específicas ao manter as etiquetas ativadas):

```json5
{
  messages: {
    tts: {
      modelOverrides: {
        enabled: true,
        allowProvider: false,
        allowSeed: false,
      },
    },
  },
}
```

# # Preferências por usuário

Comandos Slash escrevem sobreposições locais para <<CODE0>> (padrão:
<<CODE1>>, sobrepor com <<CODE2>> ou
<<CODE3>>).

Campos armazenados:

- <<CODE0>>
- <<CODE1>>
- <<CODE2>> (limiar resumo; por omissão 1500 caracteres)
- <<CODE3>> (padrão <<CODE4>>)

Estes sobrepõem <<CODE0>> para esse hospedeiro.

# # Formatos de saída (fixos)

- **Telegrama**: Opus (<<<CODE0>> de OnzeLabs, <<CODE1>> de OpenAI).
- 48kHz / 64kbps é uma boa troca de notas de voz e necessária para a bolha redonda.
- ** Outros canais**: MP3 (<<<CODE2>> de OnzeLabs, <<CODE3>> de OpenAI).
- 44.1kHz / 128kbps é o saldo padrão para a clareza da fala.
- **Edge TTS**: usa <<CODE4>> (padrão <<CODE5>>).
- <<CODE6> aceita um <<CODE7>>, mas nem todos os formatos estão disponíveis
do serviço Edge. Pesquisa por turnos
- Os valores do formato de saída seguem os formatos de saída Microsoft Speech (incluindo Ogg/WebM Opus). Pesquisa por turnos
- Telegrama <<CODE8> aceita OGG/MP3/M4A; use OpenAI/ElevenLabs se precisar
Garantiu notas de voz da Opus. Pesquisa 1
- Se o formato de saída Edge configurado falhar, OpenClaw retorna com MP3.

Os formatos OpenAI/ElevenLabs são fixos; Telegram espera Opus para a nota de voz UX.

# # Comportamento Auto-TTS

Quando habilitado, OpenClaw:

- ignora o TTS se a resposta já contém mídia ou uma diretiva <<CODE0>>.
- ignora respostas muito curtas (< 10 caracteres).
- resume as respostas longas quando activadas utilizando <<CODE1>> (ou <<CODE2>>>).
- liga o áudio gerado à resposta.

Se a resposta exceder <<CODE0>> e o resumo estiver desligado (ou nenhuma chave API para o
modelo sumário), áudio
é ignorada e a resposta de texto normal é enviada.

# # Diagrama de fluxo

```
Reply -> TTS enabled?
  no  -> send text
  yes -> has media / MEDIA: / short?
          yes -> send text
          no  -> length > limit?
                   no  -> TTS -> attach audio
                   yes -> summary enabled?
                            no  -> send text
                            yes -> summarize (summaryModel or agents.defaults.model.primary)
                                      -> TTS -> attach audio
```

# # Uso do comando Slash

Existe um único comando: <<CODE0>>>>.
Veja [Comandos Slash](<<<LINK0>>>) para detalhes de habilitação.

Nota de discórdia: <<CODE0> é um comando de discórdia embutido, então OpenClaw registra
<<CODE1>> como o comando nativo lá. O texto <<CODE2> ainda funciona.

```
/tts off
/tts always
/tts inbound
/tts tagged
/tts status
/tts provider openai
/tts limit 2000
/tts summary off
/tts audio Hello from OpenClaw
```

Notas:

- Os comandos exigem um remetente autorizado (as regras de lista de autorização/proprietário ainda se aplicam).
- <<CODE0>> ou registro de comando nativo deve ser ativado.
- <<CODE1> são alternações por sessão (<<CODE2>> é um apelido para <<CODE3>>).
- <<CODE4>> e <<CODE5>> são armazenados em prefs locais, não na configuração principal.
- <<CODE6> gera uma resposta de áudio única (não ativa o TTS).

# # Ferramenta de agente

A ferramenta <<CODE0> converte texto para fala e retorna um <<CODE1> caminho. Quando
resultado é compatível com Telegram, a ferramenta inclui <<CODE2>>> assim
O telegrama envia uma bolha de voz.

# # Porta RCP

Métodos do portal:

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>
- <<CODE3>>
- <<CODE4>>
- <<CODE5>>
