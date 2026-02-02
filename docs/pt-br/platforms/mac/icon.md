---
summary: "Menu bar icon states and animations for OpenClaw on macOS"
read_when:
  - Changing menu bar icon behavior
---

# Menu Bar Icon Estados

Autor: steipete · Atualizado em: 2025-12-06 · Escopo: app macOS (<<CODE0>>)

- ** Ocioso:** Animação normal de ícones (brilho, movimento ocasional).
- ** Pausado:** O item Status usa <<CODE0>>; nenhum movimento.
- ** Voz gatilho (orelhas grandes): ** O detector de voz chama <<CODE1>> quando a palavra wake é ouvida, mantendo <<CODE2>>> enquanto o enunciado é capturado. Orelhas escalam (1,9x), obter orifícios de orelha circulares para legibilidade, em seguida, cair via <<CODE3>> após 1s de silêncio. Só foi disparado do oleoduto de voz.
- **Trabalhando (agente em execução):** <<CODE4> conduz uma micro-moção "tail/leg scurry": movimento mais rápido da perna e offset leve enquanto o trabalho é em voo. Atualmente alternado em torno de WebChat agent corre; adicione o mesmo alternância em torno de outras tarefas longas quando você as liga.

Pontos de ligação

- Voz wake: chamada de tempo de execução/tester <<CODE0> no gatilho e <<CODE1>> após 1s de silêncio para corresponder à janela de captura.
- Atividade do agente: definido <<CODE2>> em torno de períodos de trabalho (já feito na chamada do agente WebChat). Mantenha spans curtos e reset em blocos <<CODE3>> para evitar animações emperradas.

Formas e tamanhos

- Ícone base desenhado em <<CODE0>>>.
- Escala de ouvido defaults to <<CODE1>>; conjuntos de aumento de voz <<CODE2>>> e alternâncias <<CODE3>> sem alterar o quadro geral (18×18 pt template image renderized into a 36×36 px Retina backing store).
- Curry usa a perna balançar até ~1.0 com um pequeno balanço horizontal; é aditivo para qualquer movimento ocioso existente.

Notas comportamentais

- Nenhum CLI externo / corretor alternar para ouvidos / trabalho; mantê-lo interno para os próprios sinais do aplicativo para evitar flapping acidental.
- Mantenha os TTLs curtos (&lt;10s) para que o ícone retorne rapidamente à linha de base se um trabalho for suspenso.
