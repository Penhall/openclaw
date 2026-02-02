---
summary: "What the OpenClaw system prompt contains and how it is assembled"
read_when:
  - Editing system prompt text, tools list, or time/heartbeat sections
  - Changing workspace bootstrap or skills injection behavior
---

"Projecto do Sistema"

O OpenClaw constrói um prompt de sistema personalizado para cada execução de agente. O prompt é **OpenClaw de propriedade** e não usa o prompt padrão p-coding-agent.

O prompt é montado pelo OpenClaw e injetado em cada agente executado.

# # Estrutura

O prompt é intencionalmente compacto e usa seções fixas:

- **Ferramenta**: lista de ferramentas atual + descrições curtas.
- **Segurança**: lembrete de guarda curta para evitar o comportamento de busca de energia ou a supervisão.
- ** Skills** (quando disponível): diz ao modelo como carregar instruções de habilidade sob demanda.
- ** OpenClaw Self-Update**: como executar <<CODE0>> e <<CODE1>>>.
- ** Espaço de trabalho**: directório de trabalho (<<<CODE2>>>).
- **Documentação**: caminho local para os documentos OpenClaw (pacote repo ou npm) e quando lê-los.
- **Workspace Files (injeted)**: indica que os arquivos bootstrap estão incluídos abaixo.
- **Sandbox** (quando habilitado): indica o tempo de execução sandboxed, caminhos sandbox, e se exec elevado está disponível.
- ** Data & Hora atual**: hora local do usuário, fuso horário e formato de hora.
- **Reply Tags**: sintaxe opcional de tag de resposta para provedores suportados.
- ** Batimentos cardíacos**: batimentos cardíacos rápidos e comportamento ack.
- **Runtime**: host, OS, nó, modelo, repo root (quando detectado), nível de pensamento (uma linha).
- **Razão**: nível de visibilidade atual + /razão para alternar a dica.

Os guardas de segurança no sistema são aconselhados. Guiam o comportamento do modelo, mas não impõem políticas. Use a política de ferramentas, aprovações executivas, sandboxing e listas de allowlists de canais para aplicação difícil; os operadores podem desativá-los pelo design.

# # Modos de alerta

OpenClaw pode renderizar prompts de sistema menores para subagentes. O tempo de execução define um
<<CODE0>> para cada execução (não uma configuração virada para o utilizador):

- <<CODE0>> (padrão): inclui todas as secções acima.
- <<CODE1>: utilizado para sub- agentes; omite ** Skills**, **Memory Recall**, **OpenClaw
Auto-Atualização**, **Modelo Aliases**, ** Identidade do Usuário**, **Reply Tags**,
**Mensagem**, **Replicas Silenciosas**, e **Heartbeats**. Ferramentas, **Segurança**,
Área de trabalho, Sandbox, Data atual e hora (quando conhecido), Runtime, e injetado
contexto permanecer disponível.
- <<CODE2>>: retorna apenas a linha de identidade base.

Quando <<CODE0>>, são marcadas instruções extra injectadas ** Subagente
Contexto** em vez de **Contexto de Chat de Grupo**.

# # Espaço de trabalho inicia injeção

Os arquivos Bootstrap são aparados e adicionados em **Contexto de Projeto** para que o modelo veja o contexto de identidade e perfil sem precisar de leituras explícitas:

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>
- <<CODE3>>
- <<CODE4>>
- <<CODE5>>
- <<CODE6> (apenas em novos espaços de trabalho)

Arquivos grandes são truncados com um marcador. O tamanho máximo por arquivo é controlado por
<<CODE0>> (padrão: 20000). Arquivos em falta injetam uma
Marcador curto de ficheiros em falta.

Ganchos internos podem interceptar esta etapa via <<CODE0>> para mutar ou substituir
os ficheiros de arranque injectados (por exemplo, troca de <<CODE1>> por uma pessoa alternativa).

Para inspeccionar quanto cada arquivo injetado contribui (raw vs injetado, truncamento, mais esquema de ferramenta em cima), use <<CODE0>> ou <<CODE1>>>>. Veja [Contexto](<<LINK0>>>>).

# # Manuseamento do tempo

O prompt do sistema inclui uma seção dedicada ** Data & Hora atual** quando o
é conhecido o fuso- horário do utilizador. Para manter o pronto cache-estável, agora só inclui
o ** fuso horário** (sem relógio dinâmico ou formato de tempo).

Use <<CODE0>> quando o agente precisar da hora atual; o cartão de status
inclui uma linha de timestamp.

Configurar com:

- <<CODE0>>
- <<CODE1>> (<<CODE2>>>

Veja [Data & Tempo](<<<LINK0>>>) para detalhes completos do comportamento.

# # Habilidades

Quando existem competências elegíveis, o OpenClaw injecta uma lista compacta de competências disponíveis**
(<<<CODE0>>) que inclui o caminho do arquivo** para cada habilidade. A
prompt instrui o modelo a usar <<CODE1>> para carregar o SKILL.md na lista
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

# # Documentação

Quando disponível, o prompt do sistema inclui uma seção **Documentação** que aponta para
diretório local docs OpenClaw (tanto <<CODE0>> na área de trabalho do repo quanto no pacote npm
pacote docs) e também observa o espelho público, fonte repo, comunidade Discórdia, e
ClawHub (https://clawhub.com) para a descoberta de habilidades. O prompt instrui o modelo a consultar primeiro os documentos locais
para o comportamento, comandos, configuração ou arquitetura OpenClaw, e para executar
<<CODE1> em si, quando possível (perguntando ao usuário apenas quando não tem acesso).
