---
summary: "Stable, beta, and dev channels: semantics, switching, and tagging"
read_when:
  - You want to switch between stable/beta/dev
  - You are tagging or publishing prereleases
---

# Canais de desenvolvimento

Última actualização: 2026-01-21

OpenClaw envia três canais de atualização:

- ** estável**: npm dist-tag <<CODE0>>.
- **beta**: npm dist-tag <<CODE1>> (construi sob teste).
- **dev**: cabeça móvel de <<CODE2>> (git). (quando publicado).

Enviamos construções para **beta**, testamo-las, depois **promovemos uma construção vetada para <<CODE0>**
sem alterar o número da versão — dist-tags são a fonte da verdade para as instalações do npm.

# # Trocando de canais

Saída do Git:

```bash
openclaw update --channel stable
openclaw update --channel beta
openclaw update --channel dev
```

- <<CODE0>>/<<CODE1>verifique a última etiqueta correspondente (frequentemente a mesma etiqueta).
- <<CODE2> muda para <<CODE3> e rebase no montante.

instalação global do npm/pnpm:

```bash
openclaw update --channel stable
openclaw update --channel beta
openclaw update --channel dev
```

Isto atualiza através da dist-tag npm correspondente (<<<CODE0>>, <<CODE1>>, <<CODE2>>>).

Quando você **explicitamente** alternar canais com <<CODE0>>, OpenClaw também se alinha
O método de instalação:

- <<CODE0> assegura uma saída git (padrão <<CODE1>>, sobreposição com <<CODE2>>),
atualiza-o e instala o CLI global a partir desse checkout.
- <<CODE3>>/<<CODE4>> instala a partir do npm usando a dist-tag correspondente.

Dica: se você quer estável + dev em paralelo, mantenha dois clones e aponte seu gateway para o stable.

# # Plugins e canais

Quando você muda de canal com <<CODE0>>, OpenClaw também sincroniza fontes de plugins:

- <<CODE0> prefere 'plugins' empacotados do git checkout.
- <<CODE1>> e <<CODE2> restaurar os pacotes de plugins instalados no npm.

# # Marcar as melhores práticas

- Releases de tag que você quer que git checkouts pousem (<<CODE0>> ou <<CODE1>>>>).
- Manter etiquetas imutáveis: nunca mover ou reutilizar uma etiqueta.
- as dist-tags npm continuam a ser a fonte de verdade para as instalações npm:
- <<CODE2> → estável
- <<CODE3>> → compilação de candidatos
- <<CODE4> → snapshot principal (opcional)

# # disponibilidade do aplicativo macOS

Beta e dev builds podem **não** incluir uma versão do aplicativo macOS. Tudo bem:

- O git tag e o npm dist-tag ainda podem ser publicados.
- Chame “nenhum macOS build para este beta” em notas de lançamento ou changelog.
