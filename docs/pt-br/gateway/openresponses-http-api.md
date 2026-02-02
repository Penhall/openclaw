---
summary: "Expose an OpenResponses-compatible /v1/responses HTTP endpoint from the Gateway"
read_when:
  - Integrating clients that speak the OpenResponses API
  - You want item-based inputs, client tool calls, or SSE events
---

# OpenResponses API (HTTP)

O OpenClaw’s Gateway pode servir um objetivo compatível com o OpenResponses <<CODE0>>.

Este endpoint é ** desactivado por padrão**. Activar a configuração primeiro.

- <<CODE0>>
- Mesma porta do Gateway (WS + Multiplex HTTP): <<CODE1>>

Sob o capô, as requisições são executadas como um agente normal do Gateway executado (mesmo codepath como
<<CODE0>>), então roteamento/permissões/config correspondem ao seu Gateway.

# # Autenticação

Usa a configuração de autenticação do Gateway. Enviar um símbolo ao portador:

- <<CODE0>>

Notas:

- Quando <<CODE0>, utilizar <<CODE1>> (ou <<CODE2>>>).
- Quando <<CODE3>, utilizar <<CODE4>> (ou <<CODE5>>).

# # Escolhendo um agente

Não são necessários cabeçalhos personalizados: codificar o ID do agente no campo OpenResponses <<CODE0>:

- <<CODE0>> (exemplo: <<CODE1>>, <<CODE2>>)
- <<CODE3> (também conhecido por)

Ou alvo de um agente OpenClaw específico pelo cabeçalho:

- <<CODE0>> (padrão: <<CODE1>>)

Avançado:

- <<CODE0> para controlar completamente o roteamento da sessão.

# # Habilitando o ponto final

Definir <<CODE0>> para <<CODE1>>:

```json5
{
  gateway: {
    http: {
      endpoints: {
        responses: { enabled: true },
      },
    },
  },
}
```

# # Desactivar o ponto final

Definir <<CODE0>> para <<CODE1>>:

```json5
{
  gateway: {
    http: {
      endpoints: {
        responses: { enabled: false },
      },
    },
  },
}
```

# # Comportamento da sessão

Por padrão, o endpoint é **sem estado por solicitação** (uma nova chave de sessão é gerada cada chamada).

Se a solicitação incluir uma string OpenResponses <<CODE0>>, o Gateway deriva uma chave de sessão estável
a partir dele, para chamadas repetidas podem compartilhar uma sessão de agente.

# # Pedido de forma (suportado)

A requisição segue a API OpenResponses com entrada baseada em itens. Suporte atual:

- <<CODE0>>: string ou array de objetos de item.
- <<CODE1>>: fundida no prompt do sistema.
- <<CODE2>>: definições de ferramenta cliente (ferramentas funcionais).
- <<CODE3>>: filtrar ou exigir ferramentas do cliente.
- <<CODE4>>: permite a transmissão SSE.
- <<CODE5>>: limite de saída do melhor esforço (dependente do fornecedor).
- <<CODE6>>: roteamento estável da sessão.

Aceito, mas ** actualmente ignorado**:

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>
- <<CODE3>>
- <<CODE4>>
- <<CODE5>>

# # Itens (entrada)

## # <<CODE0>>

Funções: <<CODE0>>, <<CODE1>>, <<CODE2>>, <<CODE3>>.

- <<CODE0>> e <<CODE1>> são anexados ao prompt do sistema.
- O item mais recente <<CODE2>> ou <<CODE3>> torna-se a “mensagem atual”.
- Mensagens anteriores de usuário/assistente são incluídas como histórico para o contexto.

## # <<CODE0>> (ferramentas baseadas em turnos)

Envie os resultados da ferramenta para o modelo:

```json
{
  "type": "function_call_output",
  "call_id": "call_123",
  "output": "{\"temperature\": \"72F\"}"
}
```

## # <<CODE0> e <<CODE1>>

Aceito para compatibilidade de esquema, mas ignorado ao construir o prompt.

# # Ferramentas (ferramentas de função do lado do cliente)

Fornecer ferramentas com <<CODE0>>>>.

Se o agente decidir chamar uma ferramenta, a resposta retorna um item de saída <<CODE0>>.
Em seguida, você envia uma solicitação de acompanhamento com <<CODE1>> para continuar o turno.

# # Imagens (<<<CODE0>>)

Suporta fontes base64 ou URL:

```json
{
  "type": "input_image",
  "source": { "type": "url", "url": "https://example.com/image.png" }
}
```

Tipos MIME permitidos (atual): <<CODE0>>, <<CODE1>>, <<CODE2>>, <<CODE3>>.
Tamanho máximo (atual): 10MB.

# # Arquivos (<<<CODE0>>)

Suporta fontes base64 ou URL:

```json
{
  "type": "input_file",
  "source": {
    "type": "base64",
    "media_type": "text/plain",
    "data": "SGVsbG8gV29ybGQh",
    "filename": "hello.txt"
  }
}
```

Tipos MIME autorizados (atual): <<CODE0>>>, <<CODE1>>>, <<CODE2>>>, <<CODE3>>,
<<CODE4>>, <<CODE5>>.

Tamanho máximo (atual): 5MB.

Comportamento atual:

- O conteúdo do arquivo é decodificado e adicionado ao prompt do sistema**, não a mensagem do usuário,
por isso permanece efêmero (não persistiu na história da sessão).
- Os PDFs são analisados para texto. Se for encontrado pouco texto, as primeiras páginas são rasterizadas
em imagens e passou para o modelo.

A análise em PDF usa a compilação legendária do nó <<CODE0>> (sem trabalhador). O moderno
PDF.js build espera trabalhadores de navegador / DOM globals, por isso não é usado no Gateway.

Por omissão da obtenção do URL:

- <<CODE0>>: <<CODE1>>>
- <<CODE2>>: <<CODE3>>
- Pedidos são guardados (resolução DNS, bloqueio de IP privado, limites de redirecionamento, timeouts).

# # Arquivo + limites de imagem (config)

Os padrões podem ser sintonizados em <<CODE0>>:

```json5
{
  gateway: {
    http: {
      endpoints: {
        responses: {
          enabled: true,
          maxBodyBytes: 20000000,
          files: {
            allowUrl: true,
            allowedMimes: [
              "text/plain",
              "text/markdown",
              "text/html",
              "text/csv",
              "application/json",
              "application/pdf",
            ],
            maxBytes: 5242880,
            maxChars: 200000,
            maxRedirects: 3,
            timeoutMs: 10000,
            pdf: {
              maxPages: 4,
              maxPixels: 4000000,
              minTextChars: 200,
            },
          },
          images: {
            allowUrl: true,
            allowedMimes: ["image/jpeg", "image/png", "image/gif", "image/webp"],
            maxBytes: 10485760,
            maxRedirects: 3,
            timeoutMs: 10000,
          },
        },
      },
    },
  },
}
```

Predefinição quando omitido:

- <<CODE0>>: 20MB
- <<CODE1>>: 5MB
- <<CODE2>>: 200k
- <<CODE3>>: 3
- <<CODE4>>: 10s
- <<CODE5>: 4
- <<CODE6>>: 4.000.000
- <<CODE7>>: 200
- <<CODE8>>: 10MB
- <<CODE9>>: 3
- <<CODE10>>: 10s

# # Streaming (SSE)

Definir <<CODE0>> para receber Eventos Enviados pelo Servidor (SSE):

- <<CODE0>>
- Cada linha de eventos é <<CODE1>> e <<CODE2>>>
- O fluxo termina com <<CODE3>>>

Tipos de eventos atualmente emitidos:

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>
- <<CODE3>>
- <<CODE4>>
- <<CODE5>>
- <<CODE6>>
- <<CODE7>>
- <<CODE8>>
- <<CODE9>> (em caso de erro)

Utilização

<<CODE0>> é preenchido quando o fornecedor subjacente relata a contagem do token.

# # Erros

Erros usam um objeto JSON como:

```json
{ "error": { "message": "...", "type": "invalid_request_error" } }
```

Casos frequentes:

- <<CODE0>
- <<CODE1>> organismo de pedido inválido
- <<CODE2>> método errado

# # Exemplos

Sem transmissão:

```bash
curl -sS http://127.0.0.1:18789/v1/responses \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{
    "model": "openclaw",
    "input": "hi"
  }'
```

Streaming:

```bash
curl -N http://127.0.0.1:18789/v1/responses \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{
    "model": "openclaw",
    "stream": true,
    "input": "hi"
  }'
```
