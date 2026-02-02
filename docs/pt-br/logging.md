---
summary: "Logging overview: file logs, console output, CLI tailing, and the Control UI"
read_when:
  - You need a beginner-friendly overview of logging
  - You want to configure log levels or formats
  - You are troubleshooting and need to find logs quickly
---

# Logging

Registros OpenClaw em dois lugares:

- ** Registros de arquivos** (linhas JSON) escritos pelo Gateway.
- **Saída da consola** mostrada em terminais e na interface de controlo.

Esta página explica onde os logs vivem, como lê-los e como configurar o log
níveis e formatos.

# # Onde vivem os troncos

Por padrão, o Gateway escreve um arquivo de registro rolando em:

<<CODE0>>

A data usa o fuso horário local da máquina de gateway.

Você pode substituir isso em <<CODE0>>>:

```json
{
  "logging": {
    "file": "/path/to/openclaw.log"
  }
}
```

# # Como ler logs

CLI: cauda viva (recomendada)

Use o CLI para seguir o arquivo de log do gateway via RPC:

```bash
openclaw logs --follow
```

Modos de saída:

- **TTTY sessões**: bonita, colorida, estruturada linhas de log.
- **Sessões Não-TTY**: texto simples.
- <<CODE0>>: JSON delimitado por linha (um evento log por linha).
- <<CODE1>>: forçar texto simples em sessões de TTY.
- <<CODE2>: desactivar as cores ANSI.

No modo JSON, o CLI emite objetos <<CODE0>>-tagged:

- <<CODE0>>: metadados de fluxo (arquivo, cursor, tamanho)
- <<CODE1>>: entrada de registo por análise
- <<CODE2>>: dicas de truncamento/rotação
- <<CODE3>>: linha de registo sem tratamento

Se o Gateway é inacessível, o CLI imprime uma pequena dica para executar:

```bash
openclaw doctor
```

UI de controle (web)

A guia **Logs** do Control UI segue o mesmo arquivo usando <<CODE0>>.
Ver [/web/control-ui](<<<LINK0>>>) para como abri-lo.

# # Apenas registos de canal

Para filtrar a atividade do canal (WhatsApp/Telegram/etc), use:

```bash
openclaw channels logs --channel whatsapp
```

# # Formatos de log

## # Registros de arquivos (JSONL)

Cada linha no arquivo de log é um objeto JSON. O CLI e a UI de controle analisam estes
entradas para renderizar saída estruturada (tempo, nível, subsistema, mensagem).

# # # Saída do console

Os logs do console são **TTY-aware** e formatados para legibilidade:

- Prefixos do subsistema (por exemplo, <<CODE0>>>)
- Coloração de nível (info/warn/error)
- Modo compacto opcional ou JSON

A formatação da consola é controlada por <<CODE0>>>.

# # Configurando o registro

Todas as configurações de registro vivem em <<CODE0>> em <<CODE1>>>.

```json
{
  "logging": {
    "level": "info",
    "file": "/tmp/openclaw/openclaw-YYYY-MM-DD.log",
    "consoleLevel": "info",
    "consoleStyle": "pretty",
    "redactSensitive": "tools",
    "redactPatterns": ["sk-.*"]
  }
}
```

# # # Níveis de registo

- <<CODE0>: **registros de ficheiros** (JSONL) nível.
- <<CODE1>>: ** nível de verbosidade.

<<CODE0> só afeta a saída do console; ele não altera os níveis de registro de arquivos.

Estilos de consola

<<CODE0>:

- <<CODE0>>: humano-amigável, colorido, com timestamps.
- <<CODE1>>: saída mais apertada (melhor para sessões longas).
- <<CODE2>>: JSON por linha (para processadores de log).

Redação

Resumos de ferramentas podem redigir fichas sensíveis antes de atingir o console:

- < <<CODE0>>: <<CODE1>>>
- <<CODE4>>: lista de strings regex para substituir o conjunto padrão

Redaction afeta **console output only** e não altera registros de arquivos.

# # Diagnósticos + OpenTelemetria

Os diagnósticos são eventos estruturados, legíveis por máquina para execução de modelos **e**
telemetria de fluxo de mensagens (webhooks, fila, estado da sessão). Eles não **
substituir logs; eles existem para alimentar métricas, traços e outros exportadores.

Os eventos de diagnóstico são emitidos em processo, mas os exportadores só anexam quando
diagnóstico + o plugin exportador estão habilitados.

OpenTelemetria vs OTLP

- ** OpenTelemetry (Otel)**: o modelo de dados + SDKs para traços, métricas e logs.
- **OTLP**: o protocolo de fio usado para exportar dados OTel para um coletor / backend.
- Exportações OpenClaw via **OTLP/HTTP (protobuf)** hoje.

# # # Sinais exportados

- ** Métricas**: contadores + histogramas (uso do token, fluxo de mensagens, fila).
- **Traces**: spans for model use + webhook / processamento de mensagens.
- **Logs**: exportado sobre a OTLP quando <<CODE0> é ativado. Registo
volume pode ser alto; manter <<CODE1>>> e exportar filtros em mente.

Catálogo de eventos de diagnóstico

Utilização do modelo:

- <<CODE0>>: tokens, custo, duração, contexto, provedor/modelo/canal, IDs de sessão.

Fluxo da mensagem:

- <<CODE0>>: entrada do webhook por canal.
- <<CODE1>>: webhook manuseado + duração.
- <<CODE2>>: erros do manipulador webhook.
- <<CODE3>>: mensagem em espera para processamento.
- <<CODE4>>: resultado + duração + erro opcional.

Fila + sessão:

- <<CODE0>>: fila de comandos em espera + profundidade.
- <<CODE1>>: deque de fila de comandos + espera.
- <<CODE2>>: transição do estado da sessão + razão.
- <<CODE3>>: sessão emperrada aviso + idade.
- <<CODE4>>: executar metadados de repetição/tentativa.
- <<CODE5>>: contadores agregados (webhooks/queue/session).

Ativar diagnósticos (sem exportador)

Use isto se quiser eventos de diagnóstico disponíveis para plugins ou pias personalizadas:

```json
{
  "diagnostics": {
    "enabled": true
  }
}
```

## # Bandeiras de diagnóstico (registros direcionados)

Use sinalizadores para ativar logs de depuração extra, sem levantar <<CODE0>>.
As bandeiras são insensíveis a casos e suportam caracteres selvagens (por exemplo, <<CODE1>>> ou <<CODE2>>>>).

```json
{
  "diagnostics": {
    "flags": ["telegram.http"]
  }
}
```

Ativação do Env (um-off):

```
OPENCLAW_DIAGNOSTICS=telegram.http,telegram.payload
```

Notas:

- Registros de bandeira vão para o arquivo de registro padrão (o mesmo que <<CODE0>>).
- A saída ainda é redigida de acordo com <<CODE1>>.
- Guia completo: [/diagnostics/flags] (<<<LINK0>>>).

## # Exportar para OpenTelemetria

Os diagnósticos podem ser exportados através do plugin <<CODE0>> (OTLP/HTTP). Isto
funciona com qualquer coletor OpenTelemetry/backend que aceita OTLP/HTTP.

```json
{
  "plugins": {
    "allow": ["diagnostics-otel"],
    "entries": {
      "diagnostics-otel": {
        "enabled": true
      }
    }
  },
  "diagnostics": {
    "enabled": true,
    "otel": {
      "enabled": true,
      "endpoint": "http://otel-collector:4318",
      "protocol": "http/protobuf",
      "serviceName": "openclaw-gateway",
      "traces": true,
      "metrics": true,
      "logs": true,
      "sampleRate": 0.2,
      "flushIntervalMs": 60000
    }
  }
}
```

Notas:

- Você também pode ativar o plugin com <<CODE0>>.
- <<CODE1> atualmente suporta <<CODE2> somente. <<CODE3>> é ignorado.
- Métricas incluem uso de token, custo, tamanho do contexto, duração de execução e fluxo de mensagens
contadores/histogramas (webhooks, filas, estado da sessão, profundidade da fila/espera).
- Traces/metrics pode ser alternado com <<CODE4>> / <<CODE5>> (padrão: on). Traços
incluir spans de uso do modelo mais spans de processamento webhook/mensage quando habilitados.
- Definir <<CODE6>> quando o seu colector necessitar de autorização.
- Variáveis ambientais suportadas: <<CODE7>>>,
<<CODE8>>, <<CODE9>>.

### métricas exportadas (nomes + tipos)

Utilização do modelo:

- <<CODE0> (contador, attrs: <<CODE1>>, <<CODE2>>,
<<CODE3>>, <<CODE4>>)
- <<CODE5> (contra, attrs: <<CODE6>>, <<CODE7>>,
<<CODE8>>)
- <<CODE9>> (histograma, attrs: <<CODE10>>
<<CODE11>>, <<CODE12>>>)
- <<CODE13> (histograma, attrs: <<CODE14>>>,
<<CODE15>>, <<CODE16>>, <<CODE17>>)

Fluxo da mensagem:

- <<CODE0> (contador, attrs: <<CODE1>>>,
<<CODE2>>)
- <<CODE3> (contador, attrs: <<CODE4>>>,
<<CODE5>>)
- <<CODE6> (histograma, attrs: <<CODE7>>>,
<<CODE8>>)
- <<CODE9>> (contador, attrs: <<CODE10>>>,
<<CODE11>>)
- <<CODE12>> (contador, attrs: <<CODE13>>>,
<<CODE14>>)
- <<CODE15>> (histograma, attrs: <<CODE16>>>,
<<CODE17>>)

Filas + sessões:

- <<CODE0> (contador, attrs: <<CODE1>>)
- <<CODE2> (contador, attrs: <<CODE3>>)
- <<CODE4>> (histograma, attrs: <<CODE5>> ou
<<CODE6>>)
- <<CODE7>> (histograma, attrs: <<CODE8>>>)
- <<CODE9>> (contador, attrs: <<CODE10>>>, <<CODE11>>)
- <<CODE12>> (contador, attrs: <<CODE13>>)
- <<CODE14>> (histograma, attrs: <<CODE15>>)
- <<CODE16>> (contador, attrs: <<CODE17>>)

### Exportado spans (nomes + atributos chave)

- <<CODE0>>
- <<CODE1>>, <<CODE2>>>, <<CODE3>>
- <<CODE4>>, <<CODE5>>
- <<CODE6> (input/output/cache read/cache write/total)
- <<CODE7>>
- <<CODE8>>, <<CODE9>>, <<CODE10>>
- <<CODE11>>
- <<CODE12>>, <<CODE13>>, <<CODE14>>,
<<CODE15>>
- <<CODE16>>
- <<CODE17>>, <<CODE18>>, <<CODE19>>,
<<CODE20>>, <<CODE21>>, <<CODE22>>,
<<CODE23>>
- <<CODE24>>
- <<CODE25>>, <<CODE26>>, <<CODE27>>,
<<CODE28>>, <<CODE29>>

Amostragem + rubor

- Amostragem de vestígios: <<CODE0> (0,0–1,0, apenas espaçamentos de raiz).
- Intervalo métrico de exportação: <<CODE1>> (min 1000ms).

# # Notas do protocolo

- Os objectivos OTLP/HTTP podem ser definidos através de <<CODE0>> ou
<<CODE1>>>.
- Se o endpoint já contiver <<CODE2>> ou <<CODE3>>>>, é utilizado como se encontra.
- Se o endpoint já contiver <<CODE4>>, é utilizado como- é para registos.
- <<CODE5>> habilita a exportação de log da OTLP para a saída principal do registrador.

## # Comportamento de exportação de log

- Os logs de OTLP usam os mesmos registros estruturados escritos para <<CODE0>>.
- Respeito <<CODE1>> (nível de registo do ficheiro). A redefinição da consola não se aplica
aos registos da OTLP.
- As instalações de alto volume devem preferir a amostragem/filtragem do coletor OTLP.

# # Dicas de resolução de problemas

- **Gateway não acessível?** Executar <<CODE0>> primeiro.
- Os logs estão vazios? Verifique se o Gateway está em execução e escrevendo no caminho do arquivo
em <<CODE1>>>.
- ** Precisa de mais detalhes?** Define <<CODE2>> para <<CODE3>>> ou <<CODE4>>> e tente novamente.
