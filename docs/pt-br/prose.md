---
summary: "OpenProse: .prose workflows, slash commands, and state in OpenClaw"
read_when:
  - You want to run or write .prose workflows
  - You want to enable the OpenProse plugin
  - You need to understand state storage
---

OpenProse

OpenProse é um formato de fluxo de trabalho portátil, markdown-first para orquestrar sessões de IA. No OpenClaw, ele é enviado como um plugin que instala um pacote de habilidades OpenProse mais um comando de barra <<CODE0>>. Programas vivem em <<CODE1>>> arquivos e pode gerar vários sub-agentes com fluxo de controle explícito.

Sítio oficial: https://www.prose.md

# # O que pode fazer

- Pesquisa multiagente + síntese com paralelismo explícito.
- Fluxos de trabalho seguros de aprovação repetiveis (revisão de código, triagem de incidentes, gasodutos de conteúdo).
- Reutilizável <<CODE0>> programas que você pode executar através de agentes suportados runtimes.

# # Instalar + ativar

Os plug-ins agrupados estão desativados por padrão. Activar OpenProse:

```bash
openclaw plugins enable open-prose
```

Reinicie o Gateway após habilitar o plugin.

Dev/checkout local: <<CODE0>>

Documentos relacionados: [Plugins](<<<LINK0>>), [Plugin manifesto](<<LINK1>>>), [Skills](<<LINK2>>>>).

# # Comando Slash

OpenProse registra <<CODE0>> como um comando de habilidade invocável pelo usuário. Ele encaminha para as instruções OpenProse VM e usa ferramentas OpenClaw sob o capô.

Comandos comuns:

```
/prose help
/prose run <file.prose>
/prose run <handle/slug>
/prose run <https://example.com/file.prose>
/prose compile <file.prose>
/prose examples
/prose update
```

# # Exemplo: um arquivo simples <<CODE0>>

```prose
# Research + synthesis with two agents running in parallel.

input topic: "What should we research?"

agent researcher:
  model: sonnet
  prompt: "You research thoroughly and cite sources."

agent writer:
  model: opus
  prompt: "You write a concise summary."

parallel:
  findings = session: researcher
    prompt: "Research {topic}."
  draft = session: writer
    prompt: "Summarize {topic}."

session "Merge the findings + draft into a final answer."
context: { findings, draft }
```

# # Locais de arquivo

OpenProse mantém o estado em <<CODE0>> em seu espaço de trabalho:

```
.prose/
├── .env
├── runs/
│   └── {YYYYMMDD}-{HHMMSS}-{random}/
│       ├── program.prose
│       ├── state.md
│       ├── bindings/
│       └── agents/
└── agents/
```

Agentes persistentes de nível de usuário vivem em:

```
~/.prose/agents/
```

# # Modos estatais

O OpenProse suporta várias infra- estruturas de estado:

- ** filesystem** (padrão): <<CODE0>>
- ** em contexto**: transitório, para pequenos programas
- **sqlite** (experimental): requer <<CODE1>> binário
- **postgres** (experimental): requer <<CODE2>>> e uma cadeia de ligação

Notas:

- sqlite/postgres são opt-in e experimental.
- as credenciais pós-gres fluem para logs subagentes; use um DB dedicado e menos privilegiado.

# # Programas remotos

<<CODE0> resolve-se para <<CODE1>>.
URLs diretas são obtidas como está. Isto utiliza a ferramenta <<CODE2> (ou <<CODE3>> para POST).

# # Openclaw runtime mapping

Mapa de programas OpenProse para os primitivos OpenClaw:

• Conceito OpenProse • Ferramenta OpenClaw
----------------------------------------------------------
Sessão de spawn / Ferramenta de tarefas .. < <<CODE0> ..
□ Leitura/escrita do ficheiro □ <<CODE1>>/ <<CODE2>>
* Busca na Web * <<CODE3>>

Se sua ferramenta allowlist bloquear essas ferramentas, os programas OpenProse falharão. Veja [Skills config](<<<LINK0>>>).

# # Segurança + aprovações

Tratar <<CODE0>> arquivos como código. Reveja antes de correr. Use OpenClaw ferramenta allowlists e portões de aprovação para controlar efeitos colaterais.

Para fluxos de trabalho determinísticos, aprovados, compare com [Lobster](<<<LINK0>>>).
