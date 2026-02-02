---
summary: "Voice overlay lifecycle when wake-word and push-to-talk overlap"
read_when:
  - Adjusting voice overlay behavior
---

# Ciclo de vida de Overlay Voz (macOS)

Público: contribuidores de aplicativos macOS. Objetivo: manter a voz sobreposta previsível quando wake-word e push-to-talk sobreposição.

Intenção atual

- Se a sobreposição já estiver visível da palavra wake e o usuário pressionar a tecla de atalho, a sessão de tecla de atalho  adopts  o texto existente em vez de redefini-lo. A sobreposição fica para cima enquanto a tecla de atalho é realizada. Quando o usuário libera: envie se houver texto aparado, caso contrário descarte.
- Wake-word sozinho ainda envia automaticamente em silêncio; push-to-talk envia imediatamente no lançamento.

Implementado (Dez 9, 2025)

- As sessões de sobreposição agora carregam um token por captura (wake-word ou push-to-talk). As atualizações parciais/finais/enviar/despedir/nível são retiradas quando o token não corresponde, evitando callbacks obsoletos.
- Push-to-talk adota qualquer texto sobreposto visível como um prefixo (assim pressionando a tecla de atalho enquanto a sobreposição wake está acima mantém o texto e adiciona novo discurso). Ele espera até 1.5s para uma transcrição final antes de voltar para o texto atual.
- Quime/overlay loging é emitido em`info`em categorias`voicewake.overlay`,`voicewake.ptt`, e`voicewake.chime`(início da sessão, parcial, final, envio, dispensa, razão sinistra).

Próximos passos

1. **VoiceSessionCoordenador (ator) **
- Possui exactamente um.`VoiceSession`de cada vez.
- API (com base no token):`beginWakeCapture`,`beginPushToTalk`,`updatePartial`,`endCapture`,`cancel`,`applyCooldown`.
- Drops callbacks que carregam fichas antigas (preveni velhos reconhecedores de reabrir a sobreposição).
2. **VoiceSession (modelo) **
- Campos:`token`,`source`(wakeWord, pushToTalk), texto compromissado/volátil, sinalizadores de sino, temporizadores (enviar automaticamente, ocioso),`overlayMode`(exibição, edição, envio), prazo de arrefecimento.
3. **Overlay binding**
- Não.`VoiceSessionPublisher`(`ObservableObject`) espelha a sessão ativa em SwiftUI.
- Não.`VoiceWakeOverlayView`produz apenas através do editor; nunca muda os singletons globais diretamente.
- Sobrepor as acções do utilizador (`sendNow`,`dismiss`,`edit`) voltar ao coordenador com o token da sessão.
4. ** Caminho de envio unificado**
- Ligado.`endCapture`: se o texto aparado estiver vazio → descarte; caso contrário`performSend(session:)`(jogos enviar chime uma vez, para frente, descarta).
- Push-to-talk: sem atraso; wake-word: atraso opcional para auto-enviar.
- Aplique um pequeno arrefecer para o wake runtime após push-to-talk terminar para wake-word não é imediatamente retrigger.
5. **Logging**
- Coordenador emite`.info`Registos no subsistema`bot.molt`, categorias`voicewake.overlay`e`voicewake.chime`.
- Eventos chave:`session_started`,`adopted_by_push_to_talk`,`partial`,`finalized`,`send`,`dismiss`,`cancel`,`cooldown`.

Lista de verificação de depuração

- Fluxo de logs ao reproduzir uma sobreposição pegajosa:

  ```bash
  sudo log stream --predicate 'subsystem == "bot.molt" AND category CONTAINS "voicewake"' --level info --style compact
  ```

- Verifique apenas um token de sessão ativa; callbacks obsoletos devem ser deixados de lado pelo coordenador.
- Garantir a libertação push-to-talk sempre chama`endCapture`com o token ativo; se o texto estiver vazio, espere`dismiss`sem tocar ou enviar.

Passos de migração (sugeridos)

1. Adicionar`VoiceSessionCoordinator`,`VoiceSession`, e`VoiceSessionPublisher`.
2. Refactor`VoiceWakeRuntime`criar/atualizar/fim de sessões em vez de tocar`VoiceWakeOverlayController`directamente.
3. Refactor`VoicePushToTalk`para adotar sessões existentes e chamar`endCapture`no momento da libertação; aplicar arrefecimento em tempo de execução.
4. Fio`VoiceWakeOverlayController`para o editor; remova chamadas diretas de tempo de execução/PTT.
5. Adicione testes de integração para adoção de sessão, resfriamento e demissão de texto vazio.
