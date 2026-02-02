---
summary: "Global voice wake words (Gateway-owned) and how they sync across nodes"
read_when:
  - Changing voice wake words behavior or defaults
  - Adding new node platforms that need wake word sync
---

# Voz Acordar (Palavras de Despertar Global)

Openclaw trata ** palavras wake como uma única lista global** de propriedade da ** Gateway**.

- Não há palavras de vigília personalizadas por nós.
- ** Qualquer interface de nó/app pode editar** a lista; as alterações são persistidas pelo Gateway e transmitidas para todos.
- Cada dispositivo ainda mantém o seu próprio **Voice Wake habilitado/desativado** alternar (UX local + permissões diferem).

# # Armazenamento (Host Gateway)

As palavras wake são armazenadas na máquina de gateway em:

- <<CODE0>>

Forma:

```json
{ "triggers": ["openclaw", "claude", "computer"], "updatedAtMs": 1730000000000 }
```

# # Protocolo

Métodos

- <<CODE0>> → <<CODE1>>>
- <<CODE2> com parâmetros <<CODE3>> → <<CODE4>>

Notas:

- Os gatilhos são normalizados (aparados, vazios caídos). Listas vazias são defaults.
- Os limites são aplicados para a segurança (contagem/comprimento).

Eventos

- <<CODE0>> carga útil <<CODE1>>

Quem o recebe:

- Todos os clientes do WebSocket (aplicativo macOS, WebChat, etc.)
- Todos os nós conectados (iOS/Android), e também no nó conectar como um “estado atual” inicial push.

# # Comportamento do cliente

## # app macOS

- Usa a lista global para os gatilhos <<CODE0>>.
- Edição "Trigger words" em configurações Voice Wake chamadas <<CODE1>> e, em seguida, depende da transmissão para manter outros clientes em sincronia.

Nó iOS

- Utiliza a lista global para detecção de gatilho <<CODE0>>.
- Edição Wake Words in Settings calls <<CODE1> (sobre o Gateway WS) e também mantém a detecção local wake-word responsiva.

## # Nó Android

- Expo um editor de Wake Words em Definições.
- Chamadas <<CODE0>> sobre o Gateway WS para que as edições sincronizem em todos os lugares.
