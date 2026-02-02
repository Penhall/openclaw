---
summary: "Invoke a single tool directly via the Gateway HTTP endpoint"
read_when:
  - Calling tools without running a full agent turn
  - Building automations that need tool policy enforcement
---

# Ferramentas Invocar (HTTP)

O OpenClaw’s Gateway expõe um endpoint HTTP simples para invocar uma única ferramenta diretamente. É sempre habilitado, mas fechado por Gateway auth e política de ferramentas.

- <<CODE0>>
- Mesma porta do Gateway (WS + Multiplex HTTP): <<CODE1>>

O tamanho da carga máxima padrão é de 2 MB.

# # Autenticação

Usa a configuração de autenticação do Gateway. Enviar um símbolo ao portador:

- <<CODE0>>

Notas:

- Quando <<CODE0>, utilizar <<CODE1>> (ou <<CODE2>>>).
- Quando <<CODE3>, utilizar <<CODE4>> (ou <<CODE5>>).

# # Pedir corpo

```json
{
  "tool": "sessions_list",
  "action": "json",
  "args": {},
  "sessionKey": "main",
  "dryRun": false
}
```

Campos:

- <<CODE0>> (texto obrigatório): nome da ferramenta a invocar.
- <<CODE1> (string, opcional): mapeado em args se o esquema da ferramenta suporta <<CODE2>>> e a carga útil do args omitiu.
- <<CODE3>> (objeto, opcional): argumentos específicos da ferramenta.
- <<CODE4> (string, opcional): tecla de sessão alvo. Se omitido ou <<CODE5>>, o Gateway usa a chave de sessão principal configurada (honros <<CODE6>> e agente padrão, ou <<CODE7>> no escopo global).
- <<CODE8>> (booleano, opcional): reservado para uso futuro; atualmente ignorado.

# # Política + comportamento de roteamento

A disponibilidade de ferramentas é filtrada através da mesma cadeia de políticas utilizada pelos agentes Gateway:

- <<CODE0>>/ <<CODE1>>
- <<CODE2>>/ <<CODE3>>
- <<CODE4>>/ <<CODE5>>
- políticas de grupo (se a chave da sessão mapas para um grupo ou canal)
- política de subagente (quando invocando com uma chave de sessão de subagente)

Se uma ferramenta não for permitida pela política, o endpoint retorna **404**.

Para ajudar as políticas de grupo a resolver o contexto, você pode opcionalmente definir:

- <<CODE0>> (exemplo: <<CODE1>>, <<CODE2>>)
- <<CODE3>> (quando existem várias contas)

# # Respostas

- <<CODE0>> → <<CODE1>>>
- <<CODE2>> → <<CODE3>> (pedido inválido ou erro de ferramenta)
- <<CODE4> → não autorizado
- <<CODE5> → ferramenta não disponível (não encontrada ou não permitida)
- <<CODE6>> → método não autorizado

# # Exemplo

```bash
curl -sS http://127.0.0.1:18789/tools/invoke \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "tool": "sessions_list",
    "action": "json",
    "args": {}
  }'
```
