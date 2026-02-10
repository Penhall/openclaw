---
summary: "Models CLI: list, set, aliases, fallbacks, scan, status"
read_when:
  - Adding or modifying models CLI (models list/set/scan/aliases/fallbacks)
  - Changing model fallback behavior or selection UX
  - Updating model scan probes (tools/images)
---

Modelos CLI

Ver [/conceitos/modelo-fracasso]/concepts/model-failover para o perfil de autenticação
rotação, arrefecimentos, e como isso interage com as falhas.
Visão geral rápida do provedor + exemplos: [/conceitos/modelo-fornecedores]/concepts/model-providers.

## Como funciona a seleção do modelo

OpenClaw seleciona modelos nesta ordem:

1. **Primário** modelo `agents.defaults.model.primary`ou`agents.defaults.model`.
2. **Fallbacks** em`agents.defaults.model.fallbacks`(por ordem).
3. ** Provider auth failover** acontece dentro de um provedor antes de se mover para o
Próximo modelo.

Relacionados:

-`agents.defaults.models`é a lista de allowlist/catalog dos modelos que o OpenClaw pode usar (mais aliases).
-`agents.defaults.imageModel`é usado apenas quando** o modelo primário não pode aceitar imagens.
- Os padrões por agente podem substituir`agents.defaults.model`via`agents.list[].model`mais ligações (ver [/conceitos/multi-agente]/concepts/multi-agent.

## Escolhas rápidas de modelos (anecdotal)

- ** GLM**: um pouco melhor para codificação/chamada de ferramentas.
- **MiniMax**: melhor para escrever e vibes.

## Assistente de configuração (recomendado)

Se não quiser editar manualmente, execute o assistente de onboarding:

```bash
openclaw onboard
```

Ele pode configurar modelo + autenticação para provedores comuns, incluindo **OpenAI Code (Codex)
assinatura** (OAuth) e **Antrópico** (chave API recomendada;`claude
setup-token`também suportado).

## Teclas de configuração (overview)

-`agents.defaults.model.primary`e`agents.defaults.model.fallbacks`-`agents.defaults.imageModel.primary`e`agents.defaults.imageModel.fallbacks`-`agents.defaults.models`(allowlist + aliases + params de fornecedores)
-`models.providers`(prestadores aduaneiros inscritos no`models.json`

Os refs do modelo são normalizados para minúsculas. Aliases de provedor como`z.ai/*`normalizam
ao`zai/*`.

Exemplos de configuração de provedores (incluindo OpenCode Zen) ao vivo
[/porta/configuração] /gateway/configuration#opencode-zen-multi-model-proxy.

## “Modelo não é permitido” (e por que as respostas param)

Se`agents.defaults.models`for definido, torna-se a ** lista de licenças** para`/model`e para
sessão anulada. Quando um usuário seleciona um modelo que não está nessa lista de permissões,
OpenClaw retorna:

```
Model "provider/model" is not allowed. Use /model to list available models.
```

Isso acontece **antes de** uma resposta normal é gerada, então a mensagem pode sentir
como ele “não respondeu.” A solução é:

- Adicionar o modelo ao`agents.defaults.models`, ou
- Limpar a lista de autorizações (remover`agents.defaults.models`, ou
- Escolha um modelo do`/model list`.

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

## Mudando modelos no chat `/model`

Você pode alternar modelos para a sessão atual sem reiniciar:

```
/model
/model list
/model 3
/model openai/gpt-5.2
/model status
```

Notas:

-`/model`(e`/model list` é um coletor compacto e numerado (família modelo + fornecedores disponíveis).
-`/model <#>`seleciona a partir desse catador.
-`/model status`é a visão detalhada (auth candidatos e, quando configurado, terminal de provedor`baseUrl`+ modo`api`.
- Os refs de modelos são analisados dividindo-se no primeiro **`/`. Use`provider/model`ao digitar`/model <ref>`.
- Se o próprio ID do modelo contém`/`(estilo OpenRouter), você deve incluir o prefixo do provedor (exemplo:`/model list`0).
- Se você omitir o provedor, OpenClaw trata a entrada como um alias ou um modelo para o provedor **default** (apenas funciona quando não há`/model list`1 no ID do modelo).

Comportamento/configuração completo do comando: [Comandos de linha] /tools/slash-commands.

## Comandos CLI

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

`openclaw models`(sem subcomando) é um atalho para`models status`.

## #`models list`

Mostra modelos configurados por padrão. Bandeiras úteis:

-`--all`: catálogo completo
-`--local`: apenas prestadores locais
-`--provider <name>`: filtro por fornecedor
-`--plain`: um modelo por linha
-`--json`: saída legível por máquina

## #`models status`

Mostra o modelo primário resolvido, os retrocessos, o modelo de imagem e uma visão geral da autenticação
de fornecedores configurados. Ele também apresenta status de expiração OAuth para perfis encontrados
no auth store (avisa dentro de 24h por padrão).`--plain`imprime apenas o
modelo primário resolvido.
O status OAuth é sempre mostrado (e incluído na saída`--json`. Se um configurado
provedor não tem credenciais,`models status`imprime uma ** Faltando auth** seção.
JSON inclui`auth.oauth`(janela de aviso + perfis) e`auth.providers`(autorização eficaz por fornecedor).
Usar`--check`para automação (sair`1`quando falta / expirado,`2`quando expirar).

Autenticação antrópica preferida é a configuração CLI do Código Claude (corrida em qualquer lugar; cole na máquina de gateway, se necessário):

```bash
claude setup-token
openclaw models status
```

## Digitalização (modelos livres OpenRouter)

`openclaw models scan`inspeciona o catálogo de modelos **free da OpenRouter e pode
opcionalmente modelos de sonda para ferramenta e suporte de imagem.

Parâmetros das teclas:

-`--no-probe`: sondas vivas (apenas metadados)
-`--min-params <b>`: tamanho mínimo dos parâmetros (biliões)
-`--max-age-days <days>`: saltar modelos antigos
-`--provider <name>`: filtro de prefixo do provedor
-`--max-candidates <n>`: tamanho da lista
-`--set-default`: fixar o`agents.defaults.model.primary`para a primeira selecção
-`--set-image`: definir`agents.defaults.imageModel.primary`para a primeira seleção de imagens

A sondagem requer uma chave de API OpenRouter (de perfis de autenticação ou`OPENROUTER_API_KEY`. Sem uma chave, use`--no-probe`apenas para listar os candidatos.

Os resultados da digitalização são classificados por:

1. Suporte à imagem
2. Latência da ferramenta
3. Tamanho do contexto
4. Contagem de parâmetros

Entrada

- Lista OpenRouter`/models`(filtro`:free`
- Requer chave API OpenRouter de perfis de autenticação ou`OPENROUTER_API_KEY`(ver [/ambiente]/environment
- Filtros opcionais:`--max-age-days`,`--min-params`,`--provider`,`--max-candidates`- Controlos de sondas:`--timeout`,`--concurrency`

Quando executado em um TTY, você pode selecionar backbacks interativamente. Em não-interactivo
modo, passe`--yes`para aceitar padrões.

## Registro de modelos `models.json`

Os prestadores personalizados em`models.providers`são inscritos em`models.json`sob o
diretório do agente (padrão`~/.openclaw/agents/<agentId>/models.json`. Este ficheiro
é fundida por padrão, a menos que`models.mode`seja definido como`replace`.
