---
summary: "CLI reference for `openclaw update` (safe-ish source update + gateway auto-restart)"
read_when:
  - You want to update a source checkout safely
  - You need to understand `--update` shorthand behavior
---

#`openclaw update`

Atualizar com segurança OpenClaw e alternar entre canais estáveis/beta/dev.

Se você instalou via **npm/pnpm** (instalação global, sem metadados git), atualizações acontecem através do fluxo do gerenciador de pacotes em [Updating]/install/updating.

Utilização

```bash
openclaw update
openclaw update status
openclaw update wizard
openclaw update --channel beta
openclaw update --channel dev
openclaw update --tag beta
openclaw update --no-restart
openclaw update --json
openclaw --update
```

## Opções

-`--no-restart`: saltar reiniciar o serviço Gateway após uma atualização bem sucedida.
-`--channel <stable|beta|dev>`: definir o canal de atualização (git + npm; persistiu na configuração).
-`--tag <dist-tag|version>`: sobreponha a dist-tag npm ou versão apenas para esta atualização.
-`--json`: impressão legível por máquina`UpdateRunResult`JSON.
-`--timeout <seconds>`: tempo limite por etapa (o padrão é 1200s).

Nota: os graus baixos requerem confirmação porque versões mais antigas podem quebrar a configuração.

##`update status`

Mostrar o canal de atualização ativa + git tag/branch/SHA (para checkouts de origem), além de disponibilidade de atualização.

```bash
openclaw update status
openclaw update status --json
openclaw update status --timeout 10
```

Opções:

-`--json`: estado legível por máquina JSON.
-`--timeout <seconds>`: tempo limite para os controlos (padrão 3s).

##`update wizard`

Fluxo interativo para escolher um canal de atualização e confirmar se deve reiniciar o Gateway
após a atualização (o padrão é reiniciar). Se você selecionar`dev`sem um git checkout, ele
oferece para criar um.

## O que faz

Quando você muda de canal explicitamente `--channel ...`, OpenClaw também mantém o
método de instalação alinhado:

-`dev`→ garante um git checkout (padrão:`~/openclaw`, sobreposição com`OPENCLAW_GIT_DIR`,
atualiza-o e instala o CLI global a partir desse checkout.
-`stable`/`beta`→ instala do npm usando a dist-tag correspondente.

## Git checkout flow

Canais:

-`stable`: confira a última etiqueta não beta, em seguida, construir + médico.
-`beta`: confira a última etiqueta`-beta`, em seguida, construa + médico.
-`dev`: checkout`main`, então buscar + rebase.

Alto nível:

1. Requer uma árvore de trabalho limpa (sem alterações não comprometidas).
2. Muda para o canal selecionado (tag ou branch).
3. Fetches upstream (dev somente).
4. Dev only: pré-voo lint + TypeScript build in a temp worktree; se a dica falhar, caminha de volta até 10 commits para encontrar a mais nova construção limpa.
5. Rebase no commit selecionado (dev somente).
6. Instala deps (pnpm preferred; npm fallback).
7. Compila + constrói a interface de controle.
8. Executa`openclaw doctor`como a verificação final da “atualização segura”.
9. Sincroniza plugins para o canal ativo (dev usa extensões empacotadas; estável/beta usa npm) e atualizações plugins instalados no npm.

##`--update`taquigrafia

`openclaw --update`reescreve para`openclaw update`(útil para shells e scripts de lançamento).

## Veja também

-`openclaw doctor`(ofertas para executar a atualização primeiro em git checkouts)
- [Canais de desenvolvimento] /install/development-channels
- [Atualização] /install/updating
- [Referência CLI] /cli
