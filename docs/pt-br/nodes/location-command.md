---
summary: "Location command for nodes (location.get), permission modes, and background behavior"
read_when:
  - Adding location node support or permissions UI
  - Designing background location + push flows
---

# Comando de localização (nós)

# # TL;DR

- <<CODE0> é um comando de nó (via <<CODE1>>).
- Desligado por defeito.
- As configurações usam um seletor: Desligado / Ao Usar / Sempre.
- Alternar separadamente: Localização precisa.

# # Por que um seletor (não apenas um interruptor)

As permissões do SO são multi-nível. Podemos expor um seletor no aplicativo, mas o SO ainda decide a concessão real.

- iOS/macOS: o usuário pode escolher **Usando** ou **Sempre** em prompts/Configurações do sistema. O aplicativo pode solicitar atualização, mas o sistema operacional pode exigir Configurações.
- Android: localização de fundo é uma permissão separada; no Android 10+ muitas vezes requer um fluxo de configurações.
- Localização precisa é uma subvenção separada (iOS 14+ "Preciso", Android "fino" vs "coarse").

Seletor em UI drives nosso modo solicitado; real conceder vidas em configurações do sistema operacional.

# # Modelo de configurações

Dispositivo por nó:

- <<CODE0>>: <<CODE1>>>
- <<CODE2>>: bool

Comportamento da IU:

- Selecionar <<CODE0>> solicita permissão de primeiro plano.
- Selecionando <<CODE1>> primeiramente garante <<CODE2>>, então solicita fundo (ou envia o usuário para Configurações se necessário).
- Se o sistema operacional negar o nível solicitado, reverta para o nível mais elevado concedido e mostre o estado.

# # Permissões de mapeamento (node.permissions)

Opcional. macOS node reports <<CODE0>> através do mapa de permissões; iOS/Android pode omiti-lo.

Comando: <<CODE0>>

Chamada via <<CODE0>>>>.

Parâmetros (sugeridos):

```json
{
  "timeoutMs": 10000,
  "maxAgeMs": 15000,
  "desiredAccuracy": "coarse|balanced|precise"
}
```

Carga útil de resposta:

```json
{
  "lat": 48.20849,
  "lon": 16.37208,
  "accuracyMeters": 12.5,
  "altitudeMeters": 182.0,
  "speedMps": 0.0,
  "headingDeg": 270.0,
  "timestamp": "2026-01-03T12:34:56.000Z",
  "isPrecise": true,
  "source": "gps|wifi|cell|unknown"
}
```

Erros (códigos estáveis):

- <<CODE0>>: o seletor está desligado.
- <<CODE1>>: falta permissão para o modo solicitado.
- <<CODE2>: app é de fundo, mas somente enquanto o uso permitido.
- <<CODE3>>: nenhuma correção no tempo.
- <<CODE4>>: falha do sistema / nenhum provedor.

# # Comportamento de fundo (futuro)

Objectivo: o modelo pode solicitar a localização mesmo quando o nó está em segundo plano, mas apenas quando:

- Usuário selecionado **Sempre**.
- O sistema operacional concede a localização.
- App é permitido executar em segundo plano para localização (iOS modo de fundo / Android serviço de primeiro plano ou subsídio especial).

Fluxo desencadeado por impulso (futuro):

1. Gateway envia um push para o nó (silent push ou dados FCM).
2. O nó acorda brevemente e solicita a localização do dispositivo.
3. Node avança carga útil para Gateway.

Notas:

- iOS: Sempre é necessário permissão + modo de localização de fundo. O impulso silencioso pode ser estrangulado; espere falhas intermitentes.
- Android: localização de fundo pode exigir um serviço de primeiro plano; caso contrário, esperar negação.

# # Integração modelo/ferramentas

- Superfície da ferramenta: <<CODE0>> ferramenta adiciona <<CODE1>> ação (nó requerido).
- CLI: <<CODE2>>>.
- Orientações do agente: só ligue quando o usuário habilitado localização e compreende o escopo.

# # Cópia UX (sugerida)

- Desligado: “A partilha de localização está desactivada.”
- Ao usar: “Só quando OpenClaw está aberto.”
- Sempre: “Permitir localização de fundo. Requer permissão do sistema.”
- Preciso: “Use localização GPS precisa. Desactivar para partilhar a localização aproximada.”
