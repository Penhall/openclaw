---
summary: "Talk mode: continuous speech conversations with ElevenLabs TTS"
read_when:
  - Implementing Talk mode on macOS/iOS/Android
  - Changing voice/TTS/interrupt behavior
---

Modo de conversa

O modo de fala é um loop de conversação de voz contínuo:

1. Ouça o discurso
2. Enviar transcrição para o modelo (sessão principal, chat.send)
3. Espere pela resposta
4. Fale através de OnzeLabs (reprodução de streaming)

# # Comportamento (macOS)

- ** Sobreposição sempre- em** enquanto o modo Talk está habilitado.
- **Ouvir → Pensar → Falar** transições de fase.
- Numa breve pausa** (janela silenciosa), a transcrição atual é enviada.
- As respostas são **escritas para WebChat** (mesmo que digitando).
- ** Interromper na fala** (por omissão): se o usuário começa a falar enquanto o assistente está falando, paramos a reprodução e notamos a hora de interrupção para o próximo prompt.

# # Directrizes de voz em respostas

O assistente pode prefixar sua resposta com uma linha ** única JSON** para controlar a voz:

```json
{ "voice": "<voice-id>", "once": true }
```

Regras:

- A primeira linha não vazia.
- Chaves desconhecidas são ignoradas.
- <<CODE0>> aplica- se apenas à resposta actual.
- Sem <<CODE1>>, a voz torna-se o novo padrão para o modo Talk.
- A linha JSON é removida antes da reprodução do TTS.

Chaves suportadas:

- <<CODE0>>/ <<CODE1>>/ <<CODE2>>
- <<CODE3>>/ <<CODE4>>/ <<CODE5>>
- <<CODE6>>, <<CODE7>> (WPM), <<CODE8>>, <<CODE9>>, <<CODE10>>, <<CODE11>>
- <<CODE12>>, <<CODE13>>, <<CODE14>>, <<CODE15>>, <<CODE16>
- <<CODE17>>

Configuração (<<<CODE0>>)

```json5
{
  talk: {
    voiceId: "elevenlabs_voice_id",
    modelId: "eleven_v3",
    outputFormat: "mp3_44100_128",
    apiKey: "elevenlabs_api_key",
    interruptOnSpeech: true,
  },
}
```

Predefinição:

- <<CODE0>>: verdadeiro
- <<CODE1>: diminui para <<CODE2>>/ <HTML3>>> (ou primeira voz OnzeLabs quando a chave API está disponível)
- <<CODE4>>: predefinido para <<CODE5>> quando desactivado
- <<CODE6>: diminui para <<CODE7>> (ou perfil da consola de gateway, se disponível)
- <<CODE8>>: padrões para <<CODE9>> no macOS/iOS e <<CODE10>> no Android (set <<CODE11>> para forçar a transmissão de MP3)

# # macOS UI

- Comutar a barra de menus: ** Conversar**
- Página de configuração: ** Talk Mode** group (voice id + interromper a opção)
- Sobreposição:
- **Ouvir**: pulsos de nuvem com nível de microfone
- **Pensando**: afundando animação
- **Falando**: anéis de radiação
- Clique nuvem: pare de falar
- Clique em X: saída do modo de conversa

# # Notas

- Requer permissão de fala + microfone.
- Utiliza <<CODE0>> contra a tecla de sessão <<CODE1>>.
- TTS usa API de streaming OnzeLabs com <<CODE2>> e reprodução incremental no macOS/iOS/Android para menor latência.
- <<CODE3>> para <<CODE4> é validado para <<CODE5>>, <<CODE6>>, ou <<CODE7>>; outros modelos aceitam <<CODE8>>>>>.
- <<CODE9>> é validado para <<CODE10>> quando estabelecido.
- Android suporta <<CODE11>>, <<CODE12>>, <<CODE13>>, e <<CODE14> formatos de saída para transmissão AudioTrack de baixa latência.
