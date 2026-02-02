---
summary: "Camera capture (iOS node + macOS app) for agent use: photos (jpg) and short video clips (mp4)"
read_when:
  - Adding or modifying camera capture on iOS nodes or macOS
  - Extending agent-accessible MEDIA temp-file workflows
---

# Captura de câmera (agente)

Openclaw suporta captura de câmera** para fluxos de trabalho de agentes:

- ** nó iOS** (emparelhado via Gateway): capturar uma ** foto** (<<<CODE0>>) ou ** videoclipe curto** (<<CODE1>>, com áudio opcional) via <<CODE2>>>.
- ** Nó Android** (emparelhado via Gateway): capturar uma **foto** (<<<CODE3>>>) ou **clipe de vídeo curto** (<<CODE4>>, com áudio opcional) via <<CODE5>>>.
- **macOS app** (node via Gateway): capturar uma **photo** (<<<CODE6>>>) ou **curto videoclipe** (<<CODE7>>>, com áudio opcional) via <<CODE8>>>>.

Todo o acesso à câmera é fechado atrás de ** configurações controladas pelo usuário**.

# # nó iOS

## # Configuração do usuário (por omissão)

- Página Configurações do iOS → ** Câmera** → **Permitir câmera** (<<CODE0>>)
- Por omissão: **on** (a chave em falta é tratada como activada).
- Quando desligado: <<CODE1>> Os comandos retornam <<CODE2>>>.

### Comandos (via Gateway <<CODE0>>)

- <<CODE0>>
- Carga útil de resposta:
- <<CODE1>>: matriz de <<CODE2>>

- <<CODE0>>
- Params:
- <<CODE1>>: <<CODE2>> (padrão: <<CODE3>>)
- <<CODE4>>: número (opcional; padrão <<CODE5>> no nó iOS)
- <<CODE6>>: <<CODE7>> (opcional; por omissão <<CODE8>>)
- <<CODE9>>: atualmente <<CODE10>>
- <<CODE11>>: número (opcional; padrão <<CODE12>>)
- <<CODE13>>: string (opcional; de <HTML14>>>)
- Carga útil de resposta:
- <<CODE15>>
- <<CODE16>>
- <<CODE17>>, <<CODE18>>
- Guarda de carga: as fotos são recomprimidas para manter a carga base64 em 5 MB.

- <<CODE0>>
- Params:
- <<CODE1>>: <<CODE2>> (padrão: <<CODE3>>)
- <<CODE4>>: número (default <<CODE5>>, fixado até um máximo de <<CODE6>)
- <<CODE7>>: booleano (padrão <<CODE8>>)
- <<CODE9>>: atualmente <<CODE10>>
- <<CODE11>>: string (opcional; de <<CODE12>>)
- Carga útil de resposta:
- <<CODE13>>
- <<CODE14>>
- <<CODE15>>
- <<CODE16>>

Previsão do primeiro plano

Como <<CODE0>>, o nó iOS só permite <<CODE1>> comandos no **foreground**. As invocações de fundo retornam <<CODE2>>>.

## # Ajudante CLI (arquivos de tempo + MEDIA)

A maneira mais fácil de obter anexos é através do helper CLI, que escreve mídia decodificada para um arquivo temporário e imprime <<CODE0>>.

Exemplos:

```bash
openclaw nodes camera snap --node <id>               # default: both front + back (2 MEDIA lines)
openclaw nodes camera snap --node <id> --facing front
openclaw nodes camera clip --node <id> --duration 3000
openclaw nodes camera clip --node <id> --no-audio
```

Notas:

- <<CODE0> por omissão para ** ambas as facetas** para dar ao agente ambas as vistas.
- Os arquivos de saída são temporários (no diretório de temperatura do sistema operacional) a menos que você construa seu próprio invólucro.

# # nó Android

## # Configuração do usuário (por omissão)

- Folha de configurações do Android → ** Câmera** → **Permitir câmera** (<<CODE0>>)
- Por omissão: **on** (a chave em falta é tratada como activada).
- Quando desligado: <<CODE1>> Os comandos retornam <<CODE2>>>.

Permissões

- Android requer permissões de execução:
- <<CODE0>> para ambos <<CODE1>> e <<CODE2>>>.
- <<CODE3>> para <<CODE4> quando <<CODE5>>.

Se não houver permissões, o aplicativo solicitará quando possível; se negado, <<CODE0> os pedidos falham com uma
<<CODE1> erro.

Previsão do primeiro plano

Como <<CODE0>>, o nó Android só permite <<CODE1>> comandos no **foreground**. As invocações de fundo retornam <<CODE2>>>.

Guarda de carga

As fotos são recomprimidas para manter a carga útil base64 em 5 MB.

# # app macOS

## # Configuração do usuário (por omissão desligada)

O aplicativo companheiro do macOS expõe uma caixa de seleção:

- **Configurações → Geral → Permitir câmera** (<<CODE0>>)
- Padrão: **off**
- Quando desligado: as solicitações da câmera retornam “Câmera desabilitada pelo usuário”.

Ajudante CLI (node invoy)

Utilizar o principal <<CODE0>> CLI para invocar comandos de câmera no nó macOS.

Exemplos:

```bash
openclaw nodes camera list --node <id>            # list camera ids
openclaw nodes camera snap --node <id>            # prints MEDIA:<path>
openclaw nodes camera snap --node <id> --max-width 1280
openclaw nodes camera snap --node <id> --delay-ms 2000
openclaw nodes camera snap --node <id> --device-id <id>
openclaw nodes camera clip --node <id> --duration 10s          # prints MEDIA:<path>
openclaw nodes camera clip --node <id> --duration-ms 3000      # prints MEDIA:<path> (legacy flag)
openclaw nodes camera clip --node <id> --device-id <id>
openclaw nodes camera clip --node <id> --no-audio
```

Notas:

- <<CODE0> defaults to <<CODE1> a menos que seja anulada.
- No macOS, <<CODE2>> espera <<CODE3>> (padrão 2000ms) após aquecimento/exposição resolver antes de capturar.
- As cargas de foto são recomprimidas para manter a base64 abaixo de 5 MB.

# # Segurança + limites práticos

- O acesso à câmera e ao microfone desencadeia as instruções de permissão do sistema operacional (e requer strings de uso no Info.plist).
- Os clipes de vídeo são tampados (atualmente <<CODE0>>) para evitar cargas de nó superdimensionadas (base64 overhead + limite de mensagem).

# # vídeo de tela do macOS (nível OS)

Para vídeo  screen  (não câmera), use o companheiro macOS:

```bash
openclaw nodes screen record --node <id> --duration 10s --fps 15   # prints MEDIA:<path>
```

Notas:

- Requer macOS **Screen Recording** permission (TCC).
