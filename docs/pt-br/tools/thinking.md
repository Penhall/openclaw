---
summary: "Directive syntax for /think + /verbose and how they affect model reasoning"
read_when:
  - Adjusting thinking or verbose directive parsing or defaults
---

# Níveis de pensamento ( / directivas de pensamento)

# # O que faz

- Directiva em linha em qualquer corpo de entrada: `/t <level>`, `/think:<level>`, ou `/thinking <level>`.
- Níveis (aliases): `off | minimal | low | medium | high | xhigh` (apenas modelos GPT-5.2 + Codex)
- mínimo → “pensar”
- baixo → “pensar duro”
- médio → “pensar melhor”
- alto → “ultrathink” (orçamento máximo)
- xhigh → “ultrathink+” (apenas modelos GPT-5.2 + Codex)
- `highest`, <<CODE5> mapa para <<CODE6>.
- Notas do fornecedor:
- Z.AI (`zai/*`) só suporta pensamento binário (`on`/`off`). Qualquer nível não-`off` é tratado como `on` (mapeado para `low`).

# # Ordem de resolução

1. Diretriz em linha sobre a mensagem (aplica-se apenas a essa mensagem).
2. Substituição da sessão (configurado enviando uma mensagem somente de diretiva).
3. Padrão global (`agents.defaults.thinkingDefault` na configuração).
4. Fallback: baixo para modelos com capacidade de raciocínio; fora de outra forma.

# # Definir um padrão de sessão

- Enviar uma mensagem que seja ** apenas** a directiva (espaço em branco permitido), por exemplo `/think:medium` ou `/t high`.
- Isso fica para a sessão atual (por envio por padrão); limpa por `/think:off` ou reset de sessão ocioso.
- Resposta de confirmação (<`Thinking level set to high.`/ <CODE4>>). Se o nível for inválido (por exemplo, `/thinking big`), o comando é rejeitado com uma dica e o estado da sessão permanece inalterado.
- Enviar `/think` (ou `/think:`) sem argumento para ver o nível de pensamento atual.

# # Aplicação por agente

- **Embedded Pi**: o nível resolvido é passado para o tempo de execução do agente Pi em processo.

# # Directrizes verbais (/verbose ou /v)

- Níveis: <<CODE0> (mínimo) `full` `off` (padrão).
- A mensagem apenas com diretiva ativa a sessão verbose e responde `Verbose logging enabled.` / `Verbose logging disabled.`; níveis inválidos retornam uma dica sem alterar o estado.
- <<CODE5> armazena um cancelamento explícito de sessão; eliminá-lo através da UI Sessions escolhendo `inherit`.
- Diretriz em linha afeta apenas essa mensagem; sessão / padrões globais se aplicam de outra forma.
- Enviar `/verbose` (ou `/verbose:`) sem argumento para ver o nível de verbose atual.
- Quando o verbo está ligado, agentes que emitem resultados de ferramentas estruturadas (Pi, outros agentes JSON) enviam cada chamada de ferramenta como sua própria mensagem de metadados, prefixada com `<emoji> <tool-name>: <arg>` quando disponível (caminho/comando). Estes resumos de ferramentas são enviados assim que cada ferramenta começa (bolhas separadas), não como deltas de streaming.
- Quando a verbose é `full`, as saídas da ferramenta também são encaminhadas após a conclusão (bolha separada, truncada para um comprimento seguro). Se você alternar `/verbose on|full|off` enquanto uma execução está em voo, bolhas de ferramentas subsequentes honram a nova configuração.

# # Razão da visibilidade (/razão)

- Níveis: `on|off|stream`.
- A mensagem apenas com diretiva alterna se os blocos pensantes são mostrados nas respostas.
- Quando habilitado, o raciocínio é enviado como uma ** mensagem separada** prefixada com `Reasoning:`.
- <<CODE2> (Somente no Telegram): raciocina no rascunho do Telegram enquanto a resposta está gerando, então envia a resposta final sem raciocinar.
- Apelido: `/reason`.
- Enviar `/reasoning` (ou `/reasoning:`) sem argumento para ver o nível de raciocínio atual.

# # Relacionado

- Documentos de modo elevado ao vivo em [Modo elevado] (</tools/elevated).

# # Batimentos cardíacos

- Corpo de sonda de batimento cardíaco é o prompt cardíaco configurado (padrão: `Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.`). As diretivas em linha em uma mensagem de batimento cardíaco se aplicam como de costume (mas evite alterar os padrões de sessão de batimentos cardíacos).
- Entrega de batimentos cardíacos. Para enviar também a mensagem separada `Reasoning:` (quando disponível), definir `agents.defaults.heartbeat.includeReasoning: true` ou por agente `agents.list[].heartbeat.includeReasoning: true`.

# # Web chat UI

- O selector de pensamento de chat da web espelha o nível armazenado da sessão na loja/configuração de sessão de entrada quando a página é carregada.
- A escolha de outro nível aplica-se apenas à próxima mensagem (`thinkingOnce`); após o envio, o seletor volta ao nível da sessão armazenada.
- Para alterar o padrão da sessão, envie uma diretiva `/think:<level>` (como antes); o seletor irá refleti-la após o próximo reload.
