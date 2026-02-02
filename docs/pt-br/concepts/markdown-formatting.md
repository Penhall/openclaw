---
summary: "Markdown formatting pipeline for outbound channels"
read_when:
  - You are changing markdown formatting or chunking for outbound channels
  - You are adding a new channel formatter or style mapping
  - You are debugging formatting regressions across channels
---

# Formatação Markdown

Formatos OpenClaw que saem do Markdown convertendo-o em um intermediário compartilhado
representação (IR) antes de renderizar saída específica do canal. A IR mantém o
texto fonte intacto enquanto carrega estilo / link spans de modo que o bloco e renderização pode
Mantenha-se consistente entre os canais.

## Objetivos

- ** Consistência:** uma etapa de análise, múltiplos renderizadores.
- **Blocagem segura:** texto dividido antes de renderizar a formatação em linha nunca
rompe-se entre pedaços.
- **Canal fit:** mapeia a mesma IR para Slack mrkdwn, Telegram HTML e Signal
intervalos de estilo sem re-parsing Markdown.

## Pipeline

1. **Parse Markdown -> IR**
- IR é texto simples mais spans de estilo (bold/italic/strike/code/spoiler) e spans de ligação.
- Offsets são unidades de código UTF-16, então as faixas de estilo Signal se alinham com sua API.
- As tabelas só são analisadas quando um canal opta pela conversão de tabelas.
2. ** Chunk IR (formato-primeiro)
- Chunking acontece no texto de IR antes de renderizar.
- A formatação em linha não se divide entre pedaços; os spans são cortados por pedaço.
3. **Render por canal**
- ** Slack:** mrkdwn tokens (bold/italic/strike/code), links como`<url|label>`.
- **Telegrama:** Tags HTML `<b>`,`<i>`,`<s>`,`<code>`,`<pre><code>`,`<a href>`.
- **Signal:** texto simples +`text-style`ranges; links tornam-se`label (url)`quando o rótulo difere.

## Exemplo de IR

Marcação de entrada:

```markdown
Hello **world** — see [docs](https://docs.openclaw.ai).
```

RI (esquemático):

```json
{
  "text": "Hello world — see docs.",
  "styles": [{ "start": 6, "end": 11, "style": "bold" }],
  "links": [{ "start": 19, "end": 23, "href": "https://docs.openclaw.ai" }]
}
```

## Onde é usado

- Adaptadores de saída Slack, Telegram e Signal da IR.
- Outros canais (WhatsApp, iMessage, MS Teams, Discord) ainda usam texto simples ou
suas próprias regras de formatação, com conversão de tabela Markdown aplicado antes
bloco quando activado.

## Manuseamento de mesa

As tabelas de marcação não são consistentemente suportadas entre clientes de chat. Utilização`markdown.tables`para controlar a conversão por canal (e por conta).

-`code`: renderize tabelas como blocos de código (padrão para a maioria dos canais).
-`bullets`: converter cada linha em pontos de bala (padrão para Signal + WhatsApp).
-`off`: desactivar a análise e conversão da tabela; o texto bruto da tabela passa.

Chaves de configuração:

```yaml
channels:
  discord:
    markdown:
      tables: code
    accounts:
      work:
        markdown:
          tables: off
```

## Regras de execução

- Os limites de chunk vêm de adaptadores/config de canal e são aplicados ao texto IR.
- As cercas de código são preservadas como um único bloco com uma nova linha trilhando assim canais
processá-los corretamente.
- Prefixos de lista e prefixos de blockquote fazem parte do texto de IR, então, o bloco
não divide o prefixo médio.
- Os estilos em linha (bold/italic/trike/inline-code/spoiler) nunca são divididos entre
blocos; o renderizador reabre estilos dentro de cada bloco.

Se você precisar de mais sobre o comportamento de blocos entre os canais, consulte
[Streaming + blocking] /concepts/streaming.

## Política de ligação

- ** Slack:**`[label](OCTXLINK0)`->`<url|label>`; URLs nuas permanecem nuas. Ligação automática
está desactivado durante o processamento para evitar ligações duplas.
- **Telegrama:**`[label](OCTXLINK1)`->`<a href="url">label</a>`(modo de processamento HTML).
- **Signal:**`[label](OCTXLINK2)`->`label (url)`a menos que o rótulo corresponda ao URL.

## Spoilers

Os marcadores de spoiler `||spoiler||` são analisados apenas para Signal, onde eles mapeiam para
Faixas de estilo SPOILER. Outros canais tratam-nos como texto simples.

## Como adicionar ou atualizar um formatador de canal

1. **Parse uma vez:** use o ajudante`markdownToIR(...)`compartilhado com canal apropriado
opções (autolink, estilo de cabeçalho, prefixo blockquote).
2. **Render:** implementar um renderizador com`renderMarkdownWithMarkers(...)`e um
mapa marcador de estilo (ou intervalos de estilo Sinal).
3. ** Chunk:** chame`chunkMarkdownIR(...)`antes de renderizar; renderize cada bloco.
4. ** Adaptador de fio:** atualizar o adaptador de saída do canal para usar o novo bloco
e renderizador.
5. **Teste:** adicionar ou atualizar testes de formato e um teste de entrega de saída se o
O canal usa blocos.

## Gotchas comuns

- As fichas de fecho de ângulos de folga `<@U123>`,`<#C123>`,`<https://...>` devem ser
preservado; escape do HTML em bruto com segurança.
- Telegram HTML requer escapar texto fora tags para evitar a marcação quebrada.
- Os intervalos de estilo de sinal dependem de deslocamentos UTF-16; não use deslocamentos de ponto de código.
- Preservar novas linhas para blocos de código vedados, por isso, fechar os marcadores.
A sua própria linha.
