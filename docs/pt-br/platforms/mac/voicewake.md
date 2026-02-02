---
summary: "Voice wake and push-to-talk modes plus routing details in the mac app"
read_when:
  - Working on voice wake or PTT pathways
---

Voz Acordar e empurrar para falar

# # Modos

- **Modo wake-word** (padrão): sempre- on Speech reconhecedor espera por tokens gatilho (`swabbleTriggerWords`). Na partida começa a captura, mostra a sobreposição com texto parcial, e envia automaticamente após o silêncio.
- **Push-to-talk (Opção Direita)**: segure a tecla Opção certa para capturar imediatamente – nenhum gatilho necessário. A sobreposição aparece enquanto segura; o lançamento finaliza e avança após um pequeno atraso para que você possa ajustar o texto.

# # Comportamento em tempo de execução (palavra desperta)

- Reconhecedor de fala vive em`VoiceWakeRuntime`.
- Activar apenas dispara quando há uma pausa **significativa** entre a palavra wake e a palavra seguinte (~0.55s gap). A sobreposição/chime pode começar na pausa mesmo antes do comando começar.
- Janelas de silêncio: 2.0s quando a fala está fluindo, 5.0s se apenas o gatilho foi ouvido.
- Parada difícil: 120s para evitar sessões de fuga.
- Depoimento entre sessões: 350ms.
- Sobreposição é conduzida através`VoiceWakeOverlayController`com coloração comprometida/volátil.
- Depois de enviar, o reconhecedor reinicia de forma limpa para ouvir o próximo gatilho.

# # Invariantes do ciclo de vida

- Se o Voice Wake estiver habilitado e as permissões forem concedidas, o reconhecedor de wake-word deve estar ouvindo (exceto durante uma captura explícita push-to-talk).
- Sobreposição de visibilidade (incluindo descarte manual através do botão X) nunca deve impedir o reconhecedor de retomar.

# # # Modo de falha de sobreposição pegajosa (anterior)

Anteriormente, se a sobreposição ficou presa visível e você fechou manualmente, Voice Wake poderia aparecer "morta", porque a tentativa de reiniciar do tempo de execução poderia ser bloqueada pela visibilidade de sobreposição e nenhum reinício subsequente foi agendado.

Endurecimento:

- O reinício do tempo de execução wake já não é bloqueado pela visibilidade de sobreposição.
- Sobreposição dispensa conclusão desencadeia um`VoiceWakeRuntime.refresh(...)`via`VoiceSessionCoordinator`, então o dispositivo X manual sempre retoma a escuta.

# # Específicos de empurrar para falar

- Detecção de teclas de atalho usa um global`.flagsChanged`monitor para a opção ** direita (`keyCode 61`+`.option`). Observamos apenas eventos (sem engolir).
- Capture pipeline vive em`VoicePushToTalk`: começa Fala imediatamente, transmite parciais para a sobreposição, e chamadas`VoiceWakeForwarder`em liberdade.
- Quando o push-to-talk começa, nós pausamos o wake-word tempo de execução para evitar duelar toques de áudio; ele reinicia automaticamente após o lançamento.
- Permissões: requer Microfone + Fala; ver eventos precisa Acessibilidade / Entrada Monitoramento aprovação.
- Teclados externos: alguns podem não expor a opção certa como esperado - oferecer um atalho de retorno se o relatório dos usuários falhar.

# # Configurações voltadas para o usuário

- ** Voice Wake** alternar: permite wake-word tempo de execução.
- ** Hold Cmd+Fn to talk**: habilita o monitor push-to-talk. Desactivado em macOS < 26.
- Linguagem & microfones, medidor de nível ao vivo, tabela de palavras gatilho, testador (somente local; não encaminha).
- O coletor de microfones preserva a última seleção se um dispositivo desconectar, mostrar uma dica desconectada, e temporariamente voltar ao padrão do sistema até que ele retorne.
- ** Sons**: sinos no gatilho detectam e no envio; padrões para o som do sistema “Glass” do macOS. Você pode escolher qualquer`NSSound`- arquivo carregável (por exemplo, MP3/WAV/AIFF) para cada evento ou escolher **No Sound**.

# # Comportamento de encaminhamento

- Quando o Voice Wake está habilitado, as transcrições são encaminhadas para o gateway/agent ativo (o mesmo modo local vs remoto usado pelo resto do aplicativo mac).
- As respostas são entregues ao **último fornecedor usado** (WhatsApp/Telegram/Discord/WebChat). Se a entrega falhar, o erro é registrado e a execução ainda é visível através do WebChat/session logs.

# # Encaminhando carga útil

- Não.`VoiceWakeForwarder.prefixedTranscript(_:)`prepara a dica da máquina antes de enviar. Partilhado entre wake-word e push-to-talk caminhos.

# # Verificação rápida

- Comutar push-to-talk ligado, segurar Cmd+Fn, falar, lançar: sobreposição deve mostrar parciais em seguida, enviar.
- Enquanto segura, as orelhas da barra de menu devem permanecer aumentadas (usa`triggerVoiceEars(ttl:nil)`); eles caem após o lançamento.
