---
summary: "Testing kit: unit/e2e/live suites, Docker runners, and what each test covers"
read_when:
  - Running tests locally or in CI
  - Adding regressions for model/provider bugs
  - Debugging gateway + agent behavior
---

Teste

OpenClaw tem três suítes Vitest (unit/integration, e2e, live) e um pequeno conjunto de corredores Docker.

Este documento é um guia “como testamos”:

- O que cada suite cobre (e o que faz deliberadamente  not  cover)
- Quais comandos para executar para fluxos de trabalho comuns (local, pré-push, depuração)
- Como testes ao vivo descobrem credenciais e selecionam modelos/fornecedores
- Como adicionar regressões para problemas de modelo/fornecedor do mundo real

# # Começo rápido

Na maioria dos dias:

- Porta cheia (esperada antes de empurrar): <<CODE0>>

Quando você toca testes ou quer confiança extra:

- Porta de cobertura: <<CODE0>>
- suite E2E: <<CODE1>>

Ao depurar provedores/modelos reais (requer créditos reais):

- Conjunto ao vivo (modelos + ferramenta de gateway / sondas de imagem): <<CODE0>

Dica: quando você só precisa de um caso de falha, prefira reduzir os testes ao vivo através do env vars allowlist descrito abaixo.

# # Suítes de teste (o que corre onde)

Pense nas suítes como “realismo crescente” (e crescente flakiness/custo):

## # Unidade / integração (padrão)

- Comando: <<CODE0>>>
- Configuração: <<CODE1>>
- Ficheiros: <<CODE2>>
- Âmbito:
- Testes unitários puros
- Testes de integração no processo (autenticação, roteamento, ferramentas, análise, configuração)
- Regressões determinísticas para bugs conhecidos
- Esperanças:
- Corre em CI
- Não são necessárias chaves reais.
- Deve ser rápido e estável.

# # E2E (fumo de portal)

- Comando: <<CODE0>>>
- Configuração: <<CODE1>>
- Ficheiros: <<CODE2>>
- Âmbito:
- Comportamento multi-porta de entrada de ponta a ponta
- Superfícies WebSocket/HTTP, emparelhamento de nó e rede mais pesada
- Esperanças:
- Corre em CI (quando habilitado no oleoduto)
- Não são necessárias chaves reais.
- Mais peças móveis do que testes unitários (pode ser mais lento)

## # Live (fornecedores reais + modelos reais)

- Comando: <<CODE0>>>
- Configuração: <<CODE1>>
- Ficheiros: <<CODE2>>
- Padrão: ** habilitado** por <<CODE3>> (sets <<CODE4>>)
- Âmbito:
- “Este provedor/modelo realmente funciona  hoje  com credos reais?”
- Mudanças no formato do provedor de captura, peculiaridades de chamada de ferramentas, problemas de autenticação e comportamento limite de taxa
- Esperanças:
- Não CI-stable by design (redes reais, políticas de fornecedores reais, quotas, interrupções)
- Custa dinheiro / usa limites de taxa
- Prefere executar subconjuntos limitados em vez de “tudo”
- Live runs irá fonte <<CODE5>> para pegar chaves de API faltando
- Rotação da chave antrópica: definida <<CODE6>> (ou <<CODE7>>>>) ou múltipla <<CODE8>> vars; os testes tentarão novamente sobre os limites de taxa

# # Que suite devo gerir?

Utilizar esta tabela de decisão:

- Editando lógica/testes: executar <<CODE0>> (e <<CODE1>> se você mudou muito)
- Tocing gateway networking / protocolo WS / pareamento: add <<CODE2>
- Depuração “meu bot está para baixo” / falhas específicas do provedor / chamada de ferramenta: executar um estreitado <<CODE3>

# # Vivo: fumo modelo (chaves de perfil)

Testes ao vivo são divididos em duas camadas para que possamos isolar falhas:

- "Modelo direto" nos diz que o provedor / modelo pode responder em tudo com a chave dada.
- “Fumo de Gateway” nos diz que o gasoduto completo gateway+agent funciona para esse modelo (sessões, história, ferramentas, política sandbox, etc.).

### Camada 1: Completação direta do modelo (sem gateway)

- Teste: <<CODE0>>
- Objectivo:
- enumerar modelos descobertos
- Use <<CODE1>> para selecionar modelos que você tem credos para
- Execute uma pequena conclusão por modelo (e regressões direcionadas onde necessário)
- Como habilitar:
- <<CODE2> (ou <<CODE3>> se invocar Vitest directamente)
- Definir <<CODE4>> (ou <<CODE5>, alias para moderno) para realmente executar esta suite; caso contrário, ele salta para manter <<CODE6> focado no fumo de gateway
- Como selecionar modelos:
- <<CODE7>> para executar a lista de permissões moderna (Opus/Sonnet/Haiku 4.5, GPT-5.x + Codex, Gemini 3, GLM 4.7, MiniMax M2.1, Grok 4)
- <<CODE8> é um apelido para a lista de permissões moderna
- ou <<CODE9>> (comma allowlist)
- Como selecionar fornecedores:
- <<CODE10> (comma allowlist)
- De onde vêm as chaves:
- Por padrão: loja de perfil e backbacks env
- Definir <<CODE11>> para executar **profile store** apenas
- Porque é que isto existe?
- Separa “a API do provedor é quebrada / a chave é inválida” de “o gasoduto do agente do portal é quebrado”
- Contém pequenas regressões isoladas (exemplo: OpenAI Responses/Codex Responses raciocine replay + tool-call flows)

### Camada 2: Gateway + agente dev fumaça (o que “@openclaw” realmente faz)

- Teste: <<CODE0>>
- Objectivo:
- Rode um gateway em processo
- Criar/patch a <<CODE1>> sessão (modelo de substituição por execução)
- Iterar modelos com chaves e afirmar:
- resposta “significativa” (sem ferramentas)
- uma verdadeira ferramenta de invocação funciona (ler sonda)
- sondas adicionais opcionais (exec+read probe)
- Caminhos de regressão OpenAI (tool-call-only → follow-up)
- Detalhes da sonda (para que você possa explicar falhas rapidamente):
- <<CODE2>> sonda: o teste escreve um arquivo nonce no espaço de trabalho e pede ao agente para <<CODE3>> ele e ecoar o nonce de volta.
- <<CODE4>> sonda: o teste pede ao agente para <<CODE5>-escrever um nonce em um arquivo temporário, em seguida, <<CODE6>> ele de volta.
- sonda de imagem: o teste liga um PNG gerado (cat + código aleatório) e espera que o modelo retorne <<CODE7>>.
- Referência de implementação: <<CODE8>> e <<CODE9>>>>.
- Como habilitar:
- <<CODE10>> (ou <<CODE11>> se invocar Vitest directamente)
- Como selecionar modelos:
- Padrão: allowlist moderna (Opus/Sonnet/Haiku 4.5, GPT-5.x + Codex, Gemini 3, GLM 4.7, MiniMax M2.1, Grok 4)
- <<CODE12> é um apelido para a lista de permissões moderna
- Ou definido <<CODE13>> (ou lista de vírgulas) para estreitar
- Como selecionar provedores (evitar “OpenRouter everything”):
- <<CODE14> (comma allowlist)
- Ferramentas + sondas de imagem estão sempre ligadas neste teste ao vivo:
- <<CODE15>> sonda + <<CODE16>> sonda (stress da ferramenta)
- sonda de imagem roda quando o modelo anuncia suporte de entrada de imagem
- Fluxo (alto nível):
- O teste gera um pequeno PNG com “CAT” + código aleatório (<<CODE17>>>)
- Envia- o por <<CODE18>> <<CODE19>>
- O Gateway analisa os anexos em <<CODE20>> (<<CODE21>>> + <<CODE22>>)
- Agente incorporado encaminha uma mensagem de usuário multimodal para o modelo
- Asserção: resposta contém <<CODE23>>> + o código (tolerância OCR: pequenos erros permitidos)

Dica: para ver o que você pode testar em sua máquina (e o exato <<CODE0>> IDs), execute:

```bash
openclaw models list
openclaw models list --json
```

# # Vivo: Fumaça antrópica

- Teste: <<CODE0>>
- Objetivo: verificar Claude Code CLI setup-token (ou um perfil de configuração colado) pode completar um prompt Anthropic.
- Activar:
- <<CODE1> (ou <<CODE2> se invocar Vitest directamente)
- <<CODE3>>
- Fontes de identificação:
- Perfil: <<CODE4>>
- Token bruto: <<CODE5>>
- Substituição do modelo (opcional):
- <<CODE6>>

Exemplo de configuração:

```bash
openclaw models auth paste-token --provider anthropic --profile-id anthropic:setup-token-test
OPENCLAW_LIVE_SETUP_TOKEN=1 OPENCLAW_LIVE_SETUP_TOKEN_PROFILE=anthropic:setup-token-test pnpm test:live src/agents/anthropic.setup-token.live.test.ts
```

# # Ao vivo: fumaça de infra-estrutura CLI (Claude Code CLI ou outros CLI locais)

- Teste: <<CODE0>>
- Objetivo: validar o gasoduto Gateway + agente usando uma infra-estrutura CLI local, sem tocar na configuração padrão.
- Activar:
- <<CODE1> (ou <<CODE2> se invocar Vitest directamente)
- <<CODE3>>
- Predefinição:
- Modelo: <<CODE4>>>
- Comando: <<CODE5>>>
- Arg: <<CODE6>>
- Substituição (opcional):
- <<CODE7>>
- <<CODE8>>
- <<CODE9>>
- <<CODE10>>
- <<CODE11>>
- <<CODE12>> para enviar um anexo real à imagem (os caminhos são injectados no prompt).
- <<CODE13>> para passar os caminhos dos ficheiros de imagem como args CLI em vez de injecção imediata.
- <<CODE14>> (ou <<CODE15>>>) para controlar a forma como as imagens são passadas quando <<CODE16> é definido.
- <<CODE17>> para enviar uma segunda volta e validar o fluxo de currículo.
- <<CODE18>> para manter a configuração Claude Code CLI MCP ativada (o padrão desativa a configuração MCP com um arquivo vazio temporário).

Exemplo:

```bash
OPENCLAW_LIVE_CLI_BACKEND=1 \
  OPENCLAW_LIVE_CLI_BACKEND_MODEL="claude-cli/claude-sonnet-4-5" \
  pnpm test:live src/gateway/gateway-cli-backend.live.test.ts
```

# # Receitas ao vivo recomendadas

Listas de permissões explícitas e estreitas são mais rápidas e menos flácidas:

- Modelo único, directo (sem gateway):
- <<CODE0>>

- Modelo único, fumo de portal:
- <<CODE0>>

- Ferramenta de chamada entre vários fornecedores:
- <<CODE0>>

- Foco no Google (chave Gemini API + Antigravidade):
- Gemini (chave API): <<CODE0>>
- Antigravidade (OAuth): <<CODE1>>

Notas:

- <<CODE0> usa a API Gemini (chave API).
- <<CODE1> usa a ponte Antigravity OAuth (endpoint do agente do tipo Cloud Code Assist).
- <<CODE2> usa o CLI Gemini local em sua máquina (separar auth + ferramentas).
- API Gemini vs CLI Gemini:
- API: OpenClaw chama a API Gemini hospedada do Google sobre HTTP (chave API / perfil auth); é isso que a maioria dos usuários quer dizer com "Gemini".
- CLI: OpenClaw shells para um binário local <<CODE3>>; ele tem sua própria autenticação e pode se comportar de forma diferente (streaming/tool support/version skew).

# # Vivo: matriz modelo (o que cobrimos)

Não existe uma “lista de modelos IC” fixa (ao vivo é opt-in), mas estes são os ** modelos recomendados** para cobrir regularmente em uma máquina de dev com chaves.

Fumaça moderna (chamada de ferramentas + imagem)

Este é o “modelos comuns” que esperamos continuar trabalhando:

- OpenAI (não- código): <<CODE0>> (opcional: <<CODE1>>)
- Código OpenAI: <<CODE2>> (opcional: <<CODE3>>>)
- Antrópico: <<CODE4>> (ou <<CODE5>>)
- Google (Gemini API): <<CODE6>> e <<CODE7>>> (evitar modelos Gemini 2.x mais antigos)
- Google (Antigravidade): <<CODE8>>> e <<CODE9>>>
- Z.AI (GLM): <<CODE10>>
- MiniMax: <<CODE11>>

Execute o fumo do gateway com ferramentas + imagem:
<<CODE0>>

## # Baseline: chamada de ferramentas (Leia + Exec opcional)

Escolha pelo menos um por família de fornecedores:

- OpenAI: <<CODE0>> (ou <<CODE1>>)
- Antrópico: <<CODE2>> (ou <<CODE3>>)
- Google: <<CODE4>> (ou <<CODE5>>)
- Z.AI (GLM): <<CODE6>>
- MiniMax: <<CODE7>>

Cobertura adicional opcional (bom ter):

- xAI: <<CODE0>> (ou mais recente disponível)
- Mistral: <<CODE1>>>... (Escolha uma “ferramenta” modelo capaz que você ativou)
- Cerebras: <<CODE2>>>... (se tiver acesso)
- LM Studio: <<CODE3>>>... (a chamada local da ferramenta depende do modo API)

## # Visão: imagem enviar (anexação → mensagem multimodal)

Incluir pelo menos um modelo capaz de imagem em <<CODE0>> (Vantagens com capacidade de visão de Claude/Gemini/OpenAI, etc.) para exercer a sonda de imagem.

## # Agregadores / gateways alternativos

Se você tem as chaves habilitadas, também suportamos testes via:

- OpenRouter: <<CODE0>> (centenas de modelos; use <<CODE1>> para encontrar candidatos com capacidade de imagem)
- OpenCode Zen: <<CODE2>> (auth via <<CODE3>>>/ <<CODE4>>)

Mais provedores que você pode incluir na matriz ao vivo (se você tem creds/config):

- Incorporado: <<CODE0>>, <<CODE1>, <<CODE2>>, <<CODE3>>, <<CODE4>>, <<CODE5>>, <<CODE6>>, <<CODE7>>, <<CODE8>>>, <<CODE9>>, <<CODE10>>, <<CODE11>>, <<CODE12>>>>, <<CODE13>>>, <<CODE14>>
- Via <<CODE15> (endpoints personalizados): <<CODE16>> (nuvem/API), mais qualquer proxy compatível com OpenAI/Anthropic (LM Studio, vLLM, LiteLLM, etc.)

Dica: não tente codificar “todos os modelos” em documentos. A lista autoritária é qualquer que seja <<CODE0> retorna em sua máquina + quaisquer chaves disponíveis.

# # Credenciais (nunca cometer)

Testes ao vivo descobrem credenciais da mesma forma que a CLI. Implicações práticas:

- Se o CLI funcionar, os testes ao vivo devem encontrar as mesmas chaves.
- Se um teste ao vivo diz “sem créditos”, depura da mesma forma que você depuraria <<CODE0>> / seleção de modelo.

- Loja de perfil: <<CODE0>> (preferido; o que significa “chaves de perfil” nos testes)
- Configuração: <<CODE1>> (ou <<CODE2>>)

Se você quiser confiar em chaves env (por exemplo, exportadas em seu <<CODE0>>), execute testes locais após <<CODE1>>>, ou use os corredores Docker abaixo (eles podem montar <<CODE2>>>> no recipiente).

## Deepgram ao vivo (transcrição de áudio)

- Teste: <<CODE0>>
- Activar: <<CODE1>>

# # # Corredores de docker (cheques opcionais “funciona em Linux”)

Estes rodam <<CODE0>> dentro da imagem do repo Docker, montando sua dir de configuração local e espaço de trabalho (e sourcing <<CODE1> se montado):

- Modelos directos: <<CODE0>> (escrito: <<CODE1>>)
- Gateway + agente dev: <<CODE2>> (escritório: <<CODE3>>)
- Assistente de bordo (TTY, andaimes completos): <<CODE4>>> (escritório: <<CODE5>>)
- Rede Gateway (dois contentores, WS auth + health): <<CODE6>>> (escritório: <<CODE7>>)
- Plugins (carga de extensão personalizada + fumo de registo): <<CODE8>>> (escritório: <<CODE9>>>)

Env vars úteis:

- <<CODE0> (padrão: <<CODE1>>) montado em <<CODE2>>
- <<CODE3> (padrão: <<CODE4>>) montado em <<CODE5>
- <<CODE6>> (por omissão: <<CODE7>>>) montado em <<CODE8>>>> e originado antes da realização dos testes
- <<CODE9>> / <<CODE10>> para estreitar a corrida
- <<CODE11> para garantir que os créditos provêm da loja de perfil (não env)

# # Doutores sanidade

Execute verificações de documentos após as edições de documentos: <<CODE0>>.

# # Regressão off-line (segura em IC)

Estas são regressões “real pipeline” sem provedores reais:

- Ferramenta de gateway chamando (mock OpenAI, gateway real + loop de agente): <<CODE0>>
- Assistente Gateway (WS <<CODE1>/<<CODE2>>, escreve config + auth executed): <<CODE3>>

# # Avaliação de confiabilidade do agente (competências)

Já temos alguns testes CI-safe que se comportam como “avaliações de confiabilidade do agente”:

- Mock tool-chaming através do gateway real + agente loop (<<CODE0>>).
- End-to-end assistente fluxos que validam a fiação da sessão e efeitos de configuração (<<CODE1>>).

O que ainda falta para as competências (ver [HTML0>>>>>)):

- **Decisioning:** quando as habilidades são listadas no prompt, o agente escolhe a habilidade certa (ou evita as irrelevantes)?
- **Compliance:** o agente lê <<CODE0>> antes de usar e seguir os passos/args necessários?
- ** Contratos de fluxo de trabalho:** cenários multi-turnos que afirmam ordem de ferramenta, histórico de sessão e limites sandbox.

As avaliações futuras devem permanecer determinísticas primeiro:

- Um corredor de cenário usando provedores simulados para afirmar chamadas de ferramenta + ordem, leituras de arquivos de habilidade, e fiação de sessão.
- Um pequeno conjunto de cenários focados em habilidades (usar vs evitar, atar, injecção rápida).
- Avales opcionais ao vivo (opt-in, env-gated) apenas após o CI-safe suite está no lugar.

# # Adicionando regressões (orientação)

Quando você corrigir um problema de provedor/modelo descoberto ao vivo:

- Adicionar uma regressão CI-safe se possível (fornecedor de mock/stub, ou capturar a transformação exata em forma de pedido)
- Se é inerentemente live-only (limites de taxa, políticas de autenticação), manter o teste ao vivo estreito e opt-in via env vars
- Prefere mirar na camada mais pequena que pega o bug:
- provedor solicita conversão/replay bug → teste de modelos diretos
- gateway session/history/tool pipeline bug → gateway live smoke ou CI-safe gateway mock test
