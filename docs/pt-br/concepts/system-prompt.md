---
summary: "What the OpenClaw system prompt contains and how it is assembled"
read_when:
  - Editing system prompt text, tools list, or time/heartbeat sections
  - Changing workspace bootstrap or skills injection behavior
---

"Projecto do Sistema"

O OpenClaw constrói um prompt de sistema personalizado para cada execução de agente. O prompt é **OpenClaw de propriedade** e não usa o prompt padrão p-coding-agent.

O prompt é montado pelo OpenClaw e injetado em cada agente executado.

## Estrutura

O prompt é intencionalmente compacto e usa seções fixas:

- **Ferramenta**: lista de ferramentas atual + descrições curtas.
- **Segurança**: lembrete de guarda curta para evitar o comportamento de busca de energia ou a supervisão.
- ** Skills** (quando disponível): diz ao modelo como carregar instruções de habilidade sob demanda.
- ** OpenClaw Self-Update**: como executar`config.apply`e`update.run`.
- ** Espaço de trabalho**: directório de trabalho `agents.defaults.workspace`.
- **Documentação**: caminho local para os documentos OpenClaw (pacote repo ou npm) e quando lê-los.
- **Workspace Files (injeted)**: indica que os arquivos bootstrap estão incluídos abaixo.
- **Sandbox** (quando habilitado): indica o tempo de execução sandboxed, caminhos sandbox, e se exec elevado está disponível.
- ** Data & Hora atual**: hora local do usuário, fuso horário e formato de hora.
- **Reply Tags**: sintaxe opcional de tag de resposta para provedores suportados.
- ** Batimentos cardíacos**: batimentos cardíacos rápidos e comportamento ack.
- **Runtime**: host, OS, nó, modelo, repo root (quando detectado), nível de pensamento (uma linha).
- **Razão**: nível de visibilidade atual + /razão para alternar a dica.

Os guardas de segurança no sistema são aconselhados. Guiam o comportamento do modelo, mas não impõem políticas. Use a política de ferramentas, aprovações executivas, sandboxing e listas de allowlists de canais para aplicação difícil; os operadores podem desativá-los pelo design.

## Modos de alerta

OpenClaw pode renderizar prompts de sistema menores para subagentes. O tempo de execução define um`promptMode`para cada execução (não uma configuração virada para o utilizador):

-`full`(padrão): inclui todas as secções acima.
-`minimal`: utilizado para sub- agentes; omite ** Skills**, ** Memory Recall**, ** OpenClaw
Auto-Atualização**, **Modelo Aliases**, ** Identidade do Usuário**, **Reply Tags**,
**Mensagem**, **Replicas Silenciosas**, e **Heartbeats**. Ferramentas, **Segurança**,
Área de trabalho, Sandbox, Data atual e hora (quando conhecido), Runtime, e injetado
contexto permanecer disponível.
-`none`: devolve apenas a linha de identidade base.

Quando`promptMode=minimal`, as instruções adicionais injectadas são marcadas com ** Subagente
Contexto** em vez de **Contexto de Chat de Grupo**.

## Espaço de trabalho inicia injeção

Os arquivos Bootstrap são aparados e adicionados em **Contexto de Projeto** para que o modelo veja o contexto de identidade e perfil sem precisar de leituras explícitas:

-`AGENTS.md`-`SOUL.md`-`TOOLS.md`-`IDENTITY.md`-`USER.md`-`HEARTBEAT.md`-`BOOTSTRAP.md`(apenas em novos espaços de trabalho)

Arquivos grandes são truncados com um marcador. O tamanho máximo por arquivo é controlado por`agents.defaults.bootstrapMaxChars`(por omissão: 20000). Arquivos em falta injetam uma
Marcador curto de ficheiros em falta.

Ganchos internos podem interceptar esta etapa via`agent:bootstrap`para mutar ou substituir
Os ficheiros de arranque injectados (por exemplo, troca de`SOUL.md`por uma pessoa alternativa).

Para verificar quanto cada arquivo injetado contribui (raw vs injetado, truncamento, além de esquema de ferramenta em cima), use`/context list`ou`/context detail`. Ver [Contexto] /concepts/context.

## Manuseamento do tempo

O prompt do sistema inclui uma seção dedicada ** Data & Hora atual** quando o
é conhecido o fuso- horário do utilizador. Para manter o pronto cache-estável, agora só inclui
o ** fuso horário** (sem relógio dinâmico ou formato de tempo).

Use`session_status`quando o agente precisar da hora atual; o cartão de status
inclui uma linha de timestamp.

Configurar com:

-`agents.defaults.userTimezone`-`agents.defaults.timeFormat``auto`

Veja [Data & Tempo]/date-time para detalhes completos do comportamento.

## Habilidades

Quando existem competências elegíveis, o OpenClaw injecta uma lista compacta de competências disponíveis**
`formatSkillsForPrompt` que inclui o caminho do arquivo** para cada habilidade. A
prompt instrui o modelo a usar`read`para carregar o SKILL.md na lista
localização (espaço de trabalho, gerido ou agrupado). Se não forem elegíveis competências, o
A secção de competências é omitida.

```
<available_skills>
  <skill>
    <name>...</name>
    <description>...</description>
    <location>...</location>
  </skill>
</available_skills>
```

Isso mantém a base prompt pequeno, enquanto ainda permitindo o uso de habilidades direcionadas.

## Documentação

Quando disponível, o prompt do sistema inclui uma seção **Documentação** que aponta para
diretório local docs OpenClaw (tanto`docs/`na área de trabalho do repo quanto no pacote npm
pacote docs) e também observa o espelho público, fonte repo, comunidade Discórdia, e
ClawHub (https://clawhub.com) para a descoberta de habilidades. O prompt instrui o modelo a consultar primeiro os documentos locais
para o comportamento, comandos, configuração ou arquitetura OpenClaw, e para executar`openclaw status`em si, quando possível (perguntando ao usuário apenas quando não tem acesso).
