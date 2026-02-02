---
summary: "Models CLI: list, set, aliases, fallbacks, scan, status"
read_when:
  - Adding or modifying models CLI (models list/set/scan/aliases/fallbacks)
  - Changing model fallback behavior or selection UX
  - Updating model scan probes (tools/images)
---

Modelos CLI

Ver [/conceitos/modelo-fracasso](<<<LINK0>>>) para o perfil de autenticação
rotação, arrefecimentos, e como isso interage com as falhas.
Visão geral rápida do provedor + exemplos: [/conceitos/modelo-fornecedores](<<<LINK1>>>).

# # Como funciona a seleção do modelo

OpenClaw seleciona modelos nesta ordem:

1. ** Modelo primário** (<<<<CODE0>> ou <<CODE1>>>).
2. **Fallbacks** em <<CODE2>> (em ordem).
3. ** Provider auth failover** acontece dentro de um provedor antes de se mover para o
Próximo modelo.

Relacionados:

- <<CODE0> é o allowlist/catalog de modelos que OpenClaw pode usar (mais aliases).
- <<CODE1>> é utilizado apenas quando** o modelo primário não pode aceitar imagens.
- Os padrões por agente podem substituir <<CODE2>> via <<CODE3>> mais ligações (ver [/conceitos/multi-agente](<<LINK0>>)).

# # Escolhas rápidas de modelos (anecdotal)

- ** GLM**: um pouco melhor para codificação/chamada de ferramentas.
- **MiniMax**: melhor para escrever e vibes.

# # Assistente de configuração (recomendado)

Se não quiser editar manualmente, execute o assistente de onboarding:

```bash
openclaw onboard
```

Ele pode configurar modelo + autenticação para provedores comuns, incluindo **OpenAI Code (Codex)
assinatura** (OAuth) e **Antrópico** (chave API recomendada; <<CODE0>> também suportado).

## Teclas de configuração (overview)

- <<CODE0>> e <<CODE1>>>
- <<CODE2>> e <<CODE3>>>
- <<CODE4>> (allowlist + aliases + parâmetros do fornecedor)
- <<CODE5>> (prestadores aduaneiros inscritos em <<CODE6>>>)

Os refs do modelo são normalizados para minúsculas. Aliases de provedor como <<CODE0>> normalizar
a <<CODE1>>>.

Exemplos de configuração de provedores (incluindo OpenCode Zen) ao vivo
[/porta/configuração] (<<<LINK0>>>).

## “Modelo não é permitido” (e por que as respostas param)

Se <<CODE0>> for definido, torna-se a ** lista de licenças** para <<CODE1>> e para
sessão anulada. Quando um usuário seleciona um modelo que não está nessa lista de permissões,
OpenClaw retorna:

```
Model "provider/model" is not allowed. Use /model to list available models.
```

Isso acontece **antes de** uma resposta normal é gerada, então a mensagem pode sentir
como ele “não respondeu.” A solução é:

- Adicionar o modelo a <<CODE0>>>, ou
- Limpar a lista de autorizações (remover <<CODE1>>>), ou
- Escolha um modelo de <<CODE2>>>.

Configuração da lista de permissões de exemplo:

```json5
{
  agent: {
    model: { primary: "anthropic/claude-sonnet-4-5" },
    models: {
      "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
      "anthropic/claude-opus-4-5": { alias: "Opus" },
    },
  },
}
```

# # Mudando modelos em chat (<<CODE0>>)

Você pode alternar modelos para a sessão atual sem reiniciar:

```
/model
/model list
/model 3
/model openai/gpt-5.2
/model status
```

Notas:

- <<CODE0>> (e <<CODE1>>) é um coletor compacto numerado (família modelo + fornecedores disponíveis).
- <<CODE2> seleciona a partir desse seletor.
- <<CODE3> é a visão detalhada (candidatos e, quando configurados, endpoint do provedor <<CODE4>> + <<CODE5> modo).
- Os refs do modelo são analisados dividindo-se no ** primeiro** <<CODE6>>>. Use <<CODE7>>> ao digitar <<CODE8>>.
- Se o próprio ID do modelo contiver <<CODE9>>> (OpenRouter-style), você deve incluir o prefixo do provedor (exemplo: <<CODE10>>).
- Se você omitir o provedor, OpenClaw trata a entrada como um alias ou um modelo para o provedor **default** (apenas funciona quando não há <<CODE11>> no ID do modelo).

Comportamento/configuração de comando completo: [Comandos de linha](<<<LINK0>>>).

# # Comandos CLI

```bash
openclaw models list
openclaw models status
openclaw models set <provider/model>
openclaw models set-image <provider/model>

openclaw models aliases list
openclaw models aliases add <alias> <provider/model>
openclaw models aliases remove <alias>

openclaw models fallbacks list
openclaw models fallbacks add <provider/model>
openclaw models fallbacks remove <provider/model>
openclaw models fallbacks clear

openclaw models image-fallbacks list
openclaw models image-fallbacks add <provider/model>
openclaw models image-fallbacks remove <provider/model>
openclaw models image-fallbacks clear
```

<<CODE0> (sem subcomando) é um atalho para <<CODE1>>>.

## # <<CODE0>>

Mostra modelos configurados por padrão. Bandeiras úteis:

- <<CODE0>>: catálogo completo
- <<CODE1>>: apenas prestadores locais
- <<CODE2>>: filtro por fornecedor
- <<CODE3>>: um modelo por linha
- <<CODE4>>: saída legível por máquina

## # <<CODE0>>

Mostra o modelo primário resolvido, os retrocessos, o modelo de imagem e uma visão geral da autenticação
de fornecedores configurados. Ele também apresenta status de expiração OAuth para perfis encontrados
no auth store (avisa dentro de 24h por padrão). <<CODE0>> apenas as impressões
modelo primário resolvido.
O status de OAuth é sempre mostrado (e incluído em <<CODE1> saída). Se um configurado
provedor não tem credenciais, <<CODE2>>> imprime uma seção de **Auth ausente**.
JSON inclui <<CODE3>> (janela de aviso + perfis) e <<CODE4>>
(autorização eficaz por fornecedor).
Utilizar <<CODE5>> para automatização (saída <<CODE6>> quando ausente/expirado, <<CODE7>> quando expirado).

Autenticação antrópica preferida é a configuração CLI do Código Claude (corrida em qualquer lugar; cole na máquina de gateway, se necessário):

```bash
claude setup-token
openclaw models status
```

# # Digitalização (modelos livres OpenRouter)

<<CODE0> inspeciona o catálogo de modelos livre da OpenRouter** e pode
opcionalmente modelos de sonda para ferramenta e suporte de imagem.

Parâmetros das teclas:

- <<CODE0>>: sondas vivas (apenas metadados)
- <<CODE1>>: tamanho mínimo dos parâmetros (biliões)
- <<CODE2>: saltar modelos antigos
- <<CODE3>>: filtro de prefixo do fornecedor
- <<CODE4>>: tamanho da lista de emergência
- <<CODE5>>: definido <<CODE6>>> para a primeira selecção
- <<CODE7>>: definido <<CODE8>>> para a primeira selecção de imagens

A sondagem requer uma chave de API OpenRouter (de perfis de autenticação ou
<<CODE0>>). Sem uma chave, use <<CODE1>> apenas para listar candidatos.

Os resultados da digitalização são classificados por:

1. Suporte à imagem
2. Latência da ferramenta
3. Tamanho do contexto
4. Contagem de parâmetros

Entrada

- Lista OpenRouter <<CODE0>> (filtro <<CODE1>>)
- Requer chave de API OpenRouter de perfis de autenticação ou <<CODE2>> (ver [/ambiente](<<LINK0>>))
- Filtros opcionais: <<CODE3>>, <<CODE4>>, <<CODE5>>, <<CODE6>
- Controlos das sondas: <<CODE7>>, <<CODE8>>

Quando executado em um TTY, você pode selecionar backbacks interativamente. Em não-interactivo
modo, passe <<CODE0>> para aceitar padrões.

# # Registro de modelos (<<<CODE0>>)

Os fornecedores personalizados em <<CODE0>> são escritos em <<CODE1> sob a
diretório do agente (padrão <<CODE2>>>). Este ficheiro
é fundido por padrão, a menos que <<CODE3>> seja definido como <<CODE4>>.
