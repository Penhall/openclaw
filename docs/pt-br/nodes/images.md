---
summary: "Image and media handling rules for send, gateway, and agent replies"
read_when:
  - Modifying media pipeline or attachments
---

# Image & Media Support — 2025-12-05

O canal WhatsApp é executado via **Baileys Web**. Este documento captura as regras atuais de manipulação de mídia para respostas de envio, gateway e agente.

# # Objetivos

- Enviar mídia com legendas opcionais via <<CODE0>>.
- Permitir respostas automáticas da caixa de entrada web para incluir mídia ao lado do texto.
- Manter os limites por tipo sãos e previsíveis.

# # Superfície CLI

- <<CODE0>>
- <<CODE1> opcional; a legenda pode estar vazia apenas para envios de mídia.
- <<CODE2> imprime a carga útil resolvida; <<CODE3> emite <<CODE4>>.

# # Comportamento do canal WhatsApp Web

- Entrada: local file path **ou** HTTP(S) URL.
- Fluxo: carregar em um buffer, detectar o tipo de mídia, e construir a carga útil correta:
- **Imagens:** redimensionar e recomprimir para JPEG (max side 2048px) segmentando <<CODE0>> (padrão 5 MB), com 6 MB.
- **Audio/Voz/Vídeo:** passe-através até 16 MB; áudio é enviado como uma nota de voz (<<CODE1>>).
- **Documentos:** qualquer outra coisa, até 100 MB, com nome de arquivo preservado quando disponível.
- Reprodução do estilo WhatsApp GIF: envie um MP4 com <<CODE2>> (CLI: <<CODE3>>>) para que os clientes móveis façam a ligação.
- Detecção MIME prefere bytes mágicos, em seguida, cabeçalhos, em seguida, extensão de arquivo.
- Legendagem vem de <<CODE4>> ou <<CODE5>>>; legenda vazia é permitida.
- Logging: não-verbose mostra <<CODE6>/<<CODE7>>; verbose inclui tamanho e caminho de origem/URL.

# # Auto-Reply Pipeline

- <<CODE0> retorna <<CODE1>>.
- Quando a mídia está presente, o remetente web resolve caminhos locais ou URLs usando o mesmo pipeline que <<CODE2>>.
- Múltiplas entradas de mídia são enviadas sequencialmente se for fornecida.

# # Mídia de entrada para comandos (Pi)

- Quando as mensagens da web inbound incluem mídia, o OpenClaw baixa para um arquivo temporário e expõe variáveis templáveis:
- <<CODE0>> pseudo-URL para os suportes de entrada.
- <<CODE1>> caminho temporário local escrito antes de executar o comando.
- Quando uma caixa de areia Docker por sessão está habilitada, os meios de entrada são copiados para o espaço de trabalho da caixa de areia e <<CODE2>/<<CODE3>> são reescritos para um caminho relativo como <<CODE4>>>.
- A compreensão dos meios de comunicação (se configurada através de <<CODE5>> ou partilhada <<CODE6>>) é executada antes da templagem e pode inserir <<CODE7>>>, <<CODE8>>>>, e <<CODE9>>blocos em <<CODE10>>>.
- Conjuntos de áudio <<CODE11>> e usa a transcrição para análise de comandos para que os comandos slash ainda funcionam.
- Descrições de vídeo e imagem preservar qualquer texto legenda para análise de comandos.
- Por padrão, apenas o primeiro anexo imagem/áudio/vídeo é processado; definir <<CODE12>> para processar vários anexos.

# # Limites e erros

**Outbound enviar caps (WhatsApp web send)**

- Imagens: ~6 MB cap após recompressão.
- Áudio/voz/vídeo: 16 MB cap; documentos: 100 MB cap.
- Oversize ou mídia ilegível → erro claro em logs e a resposta é ignorada.

**Capas de compreensão da mídia (transcrição/descrição)

- Padrão da imagem: 10 MB (<<<CODE0>>).
- Áudio padrão: 20 MB (<<<CODE1>>>).
- Padrão do vídeo: 50 MB (<<<CODE2>>).
- Oversize mídia ignora compreensão, mas as respostas continuam com o corpo original.

# # Notas para testes

- Capa enviar + fluxos de resposta para casos de imagem/audio/documento.
- Validar recompressão para imagens (tamanho encadernado) e sinal de nota de voz para áudio.
- Assegure-se de que as respostas multi-mídias se espalhem em sequência.
