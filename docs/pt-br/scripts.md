---
summary: "Repository scripts: purpose, scope, and safety notes"
read_when:
  - Running scripts from the repo
  - Adding or changing scripts under ./scripts
---

Programas

O diretório <<CODE0> contém scripts helper para tarefas locais de fluxo de trabalho e ops.
Use estes quando uma tarefa estiver claramente ligada a um script; caso contrário, prefira o CLI.

# # Convenções

- Scripts são **opcional** a menos que referenciados em documentos ou listas de verificação de lançamento.
- Prefere superfícies CLI quando existem (exemplo: monitoração de autenticação usa <<CODE0>>>).
- Assuma que os scripts são específicos do host; leia-os antes de correr em uma nova máquina.

# # Git ganchos

- <<CODE0>>: configuração do melhor esforço para <<CODE1>> quando dentro de um repo git.
- <<CODE2>: formatação pré-comprometida para ficheiros em fase <<CODE3>> e <<CODE4>.

# # Roteiros de monitorização de autenticação

Os scripts de monitoramento de autenticação estão documentados aqui:
[/automatização/acompanhamento](<<<LINK0>>)

# # Ao adicionar scripts

- Mantenha os scripts focados e documentados.
- Adicionar um pequeno item no documento relevante (ou criar um se faltar).
