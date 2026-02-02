---
summary: "How inbound audio/voice notes are downloaded, transcribed, and injected into replies"
read_when:
  - Changing audio transcription or media handling
---

# Notas de áudio / voz — 2026-01-17

# # O que funciona

- **Compreensão mediática (audio)**: Se o entendimento de áudio estiver habilitado (ou detectado automaticamente), OpenClaw:
1. Localiza o primeiro anexo de áudio (caminho local ou URL) e baixa-lo se necessário.
2. Força <<CODE0>> antes de enviar para cada entrada do modelo.
3. Executa a primeira entrada do modelo elegível em ordem (fornecedor ou CLI).
4. Se falhar ou saltar (tamanho/timeout), tenta a próxima entrada.
5. No sucesso, substitui <<CODE1>> por um bloco <<CODE2>>> e conjuntos <<CODE3>>.
- ** Processamento de comandos**: Quando a transcrição é bem-sucedida, <<CODE4>/<<CODE5> são ajustados para a transcrição de modo que os comandos slash ainda funcionam.
- **Verbose loging**: Em <<CODE6>>, registramos quando a transcrição é executada e quando ela substitui o corpo.

# # Detecção automática (padrão)

Se ** não configurar modelos** e <<CODE0>> não estiver ** definido para <<CODE1>,
O OpenClaw detecta automaticamente nesta ordem e pára na primeira opção de trabalho:

1. **CLIs locais** (se instalados)
- <<CODE0> (necessários <<CODE1>> com codificador/decodificador/juntar/pedras)
- <<CODE2> (a partir de <<CODE3>>; usa <<CODE4>> ou o modelo minúsculo empacotado)
- <<CODE5>> (Python CLI; baixa modelos automaticamente)
2. ** Gemini CLI** (<<<CODE6>>>) utilizando <<CODE7>>
3. ** Teclas do fornecedor** (OpenAI → Groq → Deepgram → Google)

Para desativar a detecção automática, defina <<CODE0>>.
Para personalizar, definir <<CODE1>>>>.
Nota: A detecção binária é o melhor esforço em macOS/Linux/Windows; certifique-se de que o CLI está em <<CODE2> (expandimos <<CODE3>>), ou definimos um modelo CLI explícito com um caminho de comando completo.

# # Exemplos de configuração

## # Fornecedor + retrocesso do CLI (OpenAI + Whisper CLI)

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        maxBytes: 20971520,
        models: [
          { provider: "openai", model: "gpt-4o-mini-transcribe" },
          {
            type: "cli",
            command: "whisper",
            args: ["--model", "base", "{{MediaPath}}"],
            timeoutSeconds: 45,
          },
        ],
      },
    },
  },
}
```

## # Apenas provedor com escala

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        scope: {
          default: "allow",
          rules: [{ action: "deny", match: { chatType: "group" } }],
        },
        models: [{ provider: "openai", model: "gpt-4o-mini-transcribe" }],
      },
    },
  },
}
```

## # Apenas para provedores (Deepgram)

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

# # Notas e limites

- Provider auth segue a ordem de autenticação do modelo padrão (perfis auth, env vars, <<CODE0>>>).
- Deepgram capta <<CODE1>> quando <<CODE2>> é utilizado.
- Detalhes de configuração do Deepgram: [Deepgram (tradução do áudio)] (<<<LINK0>>>).
- Os provedores de áudio podem substituir <<CODE3>>, <<CODE4>>, e <<CODE5>> via <<CODE6>>.
- A tampa de tamanho padrão é de 20MB (<<<CODE7>>>). Oversize audio é ignorado para esse modelo e a próxima entrada é tentada.
- O padrão <<CODE8>> para áudio é **unset** (tradução completa). Definir <<CODE9>> ou por entrada <<CODE10>> para reduzir a saída.
- OpenAI auto padrão é <<CODE11>>>; definido <<CODE12>> para maior precisão.
- Usar <<CODE13>> para processar múltiplas notas de voz (<<CODE14>>+<HTML16>>>).
- Transcrição está disponível para modelos como <<CODE16>>>.
- CLI stdout é tampado (5MB); manter saída CLI concisa.

# # Techas

As regras de alcance usam a primeira partida ganha. <<CODE0> é normalizada para <<CODE1>>, <<CODE2>>, ou <<CODE3>>.
- Certifique-se de que seu CLI sai 0 e imprime texto simples; JSON precisa ser massageado via <<CODE4>>.
- Mantenha o tempo razoável (<<<CODE5>>, padrão 60s) para evitar o bloqueio da fila de respostas.
