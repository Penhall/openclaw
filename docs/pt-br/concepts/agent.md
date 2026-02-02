---
summary: "Agent runtime (embedded pi-mono), workspace contract, and session bootstrap"
read_when:
  - Changing agent runtime, workspace bootstrap, or session behavior
---

Agente Runtime

OpenClaw executa um único agente incorporado runtime derivado de **pi-mono**.

## Espaço de trabalho (obrigatório)

OpenClaw usa um diretório de espaço de trabalho de agente único `agents.defaults.workspace` como diretório de trabalho **only** do agente `cwd` para ferramentas e contexto.

Recomendado: use`openclaw setup`para criar`~/.openclaw/openclaw.json`se faltar e inicializar os arquivos de espaço de trabalho.

layout completo do espaço de trabalho + guia de backup: [Espaço de trabalho do agente] /concepts/agent-workspace

Se o`agents.defaults.sandbox`estiver activo, as sessões não principais podem sobrepor- se a isto com
Espaços de trabalho por sessão no âmbito do`agents.defaults.sandbox.workspaceRoot`(ver
[Configuração do portal] /gateway/configuration.

## Arquivos de bootstrap (injetados)

Dentro do`agents.defaults.workspace`, OpenClaw espera esses arquivos editáveis pelo usuário:

-`AGENTS.md`— instruções de funcionamento + “memória”
-`SOUL.md`— persona, limites, tom
-`TOOLS.md`— Notas de ferramentas mantidas pelo utilizador (por exemplo,`imsg`,`sag`, convenções)
-`BOOTSTRAP.md`— ritual de primeira execução (suprimido após conclusão)
-`IDENTITY.md`— nome do agente/vibe/emoji
-`USER.md`— perfil de utilizador + endereço preferido

No primeiro turno de uma nova sessão, o OpenClaw injeta o conteúdo desses arquivos diretamente no contexto do agente.

Os ficheiros em branco são ignorados. Arquivos grandes são aparados e truncados com um marcador, então prompts permanecem lean (leia o arquivo para obter conteúdo completo).

Se um arquivo estiver faltando, OpenClaw injeta uma única linha de marcador “arquivo ausente” (e`openclaw setup`criará um modelo padrão seguro).

`BOOTSTRAP.md`só é criado para uma ** marca de novo espaço de trabalho** (sem outros arquivos bootstrap presentes). Se você excluí-lo após completar o ritual, ele não deve ser recriado em reinícios posteriores.

Para desativar completamente a criação de arquivos bootstrap (para espaços de trabalho pré-semeados), definido:

```json5
{ agent: { skipBootstrap: true } }
```

## Ferramentas incorporadas

As ferramentas principais (leitura/exec/edição/escrita e ferramentas de sistema relacionadas) estão sempre disponíveis,
sujeito à política de ferramentas.`apply_patch`é opcional e fechado por`tools.exec.applyPatch`. O`TOOLS.md`não controla as ferramentas existentes; é
orientação para como  você  quer que eles sejam usados.

## Habilidades

OpenClaw carrega habilidades de três locais (o espaço de trabalho ganha no conflito de nomes):

- Conjunto (enviou com a instalação)
- Gerenciado/local:`~/.openclaw/skills`- Espaço de trabalho:`<workspace>/skills`

As habilidades podem ser fechadas por config/env (ver`skills`em [Configuração do portal]/gateway/configuration.

## integração pi-mono

OpenClaw reutiliza peças da base de código pi-mono (modelos/tools), mas ** gerenciamento de sessão, descoberta e fiação de ferramentas são propriedade do OpenClaw**.

- Nada de pi-codificador.
- Não são consultadas as definições`~/.pi/agent`ou`<workspace>/.pi`.

## Sessãos

As transcrições das sessões são armazenadas como JSONL em:

-`~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl`

O ID da sessão é estável e escolhido pelo OpenClaw.
As pastas de sessão Legacy Pi/Tau são **not** read.

## Direção durante a transmissão

Quando o modo de fila é`steer`, as mensagens de entrada são injetadas na execução atual.
A fila é marcada ** após cada chamada de ferramenta**; se uma mensagem em fila estiver presente,
as chamadas de ferramentas restantes da mensagem assistente atual são ignoradas (error tool
resultados com "Skipped due to listed user message."), então o usuário em fila
a mensagem é injectada antes da próxima resposta do assistente.

Quando o modo de fila é`followup`ou`collect`, as mensagens de entrada são mantidas até que o
o turn atual termina, então um novo agente gira começa com as cargas em fila. Ver
[Fila]/concepts/queue para o modo + comportamento de desbounce/cap.

A transmissão em bloco envia blocos assistentes completos assim que terminarem; é
** off por padrão** `agents.defaults.blockStreamingDefault: "off"`.
Ajustar o limite através do`agents.defaults.blockStreamingBreak``text_end`vs`message_end`; por omissão para o fim  texto).
Controlar o bloco macio com o`agents.defaults.blockStreamingChunk`(por omissão para
800–1200 caracteres; prefere quebras de parágrafos, em seguida, novas linhas; sentenças últimas).
Coalesce fluxos de pedaços com`agents.defaults.blockStreamingCoalesce`para reduzir
spam de linha única (fusão baseada em idle antes do envio). Os canais não- telegramas requerem`*.blockStreaming: true`explícito para permitir respostas em bloco.
Resumos de ferramentas verbose são emitidos no início da ferramenta (sem desbouncer); UI de controle
streams de saída da ferramenta através de eventos de agente quando disponíveis.
Mais detalhes: [Streaming + blocking] /concepts/streaming.

## Modelo de árbitros

Os refs de modelo na configuração (por exemplo,`agents.defaults.model`e`agents.defaults.models` são analisados dividindo no **primeiro**`/`.

- Use`provider/model`ao configurar modelos.
- Se o próprio ID do modelo contém`/`(estilo OpenRouter), inclua o prefixo do provedor (exemplo:`openrouter/moonshotai/kimi-k2`.
- Se você omitir o provedor, OpenClaw trata a entrada como um alias ou um modelo para o provedor **default** (apenas funciona quando não há`/`no ID do modelo).

## Configuração (mínimo)

No mínimo, definido:

-`agents.defaults.workspace`-`channels.whatsapp.allowFrom`(com forte recomendação)

---

Próximo: [Conversas em grupo]/concepts/group-messages  .
