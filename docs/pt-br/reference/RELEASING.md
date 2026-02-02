---
summary: "Step-by-step release checklist for npm + macOS app"
read_when:
  - Cutting a new npm release
  - Cutting a new macOS app release
  - Verifying metadata before publishing
---

# Lista de Verificação de Lançamento (npm + macOS)

Usar `pnpm` (Node 22+) da raiz do repo. Mantenha a árvore de trabalho limpa antes de marcar/publicar.

# # Operador gatilho

Quando o operador diz “libertar”, faça imediatamente este pré-voo (sem perguntas extras, a menos que bloqueado):

- Leia este documento e `docs/platforms/mac/release.md`.
- Env de carga de `~/.profile` e confirmar `SPARKLE_PRIVATE_KEY_FILE` + App Store Connect vars são definidos (SPARKLE PRIVATE KEY FILE deve viver em `~/.profile`).
- Utilizar as teclas Sparkle de <<CODE4>, se necessário.

1. ** Versão & metadados**

- [ ] Bump `package.json` versão (por exemplo, `2026.1.29`).
- [ ] Executar `pnpm plugins:sync` para alinhar versões de pacotes de extensão + changelogs.
- [ ] Actualizar as cadeias de caracteres CLI/versão: [<`src/cli/program.ts`](https://github.com/openclaw/openclaw/blob/main/src/cli/program.ts) e o agente de utilizador Baileys em [`src/provider-web.ts`](https://github.com/openclaw/openclaw/blob/main/src/provider-web.ts).
- [ ] Confirmar os metadados do pacote (nome, descrição, repositório, palavras-chave, licença) e `bin` aponta para [`openclaw.mjs`](https://github.com/openclaw/openclaw/blob/main/openclaw.mjs) para `openclaw`.
- [ ] Se as dependências mudaram, execute `pnpm install` então `pnpm-lock.yaml` é atual.

2. **Construir & artefatos**

- [ ] Se as entradas de A2UI mudarem, execute `pnpm canvas:a2ui:bundle` e commit qualquer atualização [`src/canvas-host/a2ui/a2ui.bundle.js`](https://github.com/openclaw/openclaw/blob/main/src/canvas-host/a2ui/a2ui.bundle.js).
- [ ] `pnpm run build` (regenera `dist/`).
- [ ] Verificar o pacote npm `files` inclui todas as pastas necessárias `dist/*` (nomeadamente `dist/node-host/**` e `dist/acp/**` para nó sem cabeça + CLI ACP).
- [ ] Confirmar `dist/build-info.json` existe e inclui o esperado `commit` hash (banner CLI usa isso para instalações npm).
- [ ] Opcional: `npm pack --pack-destination /tmp` após a compilação; inspecione o conteúdo do tarball e mantenha-o acessível para o lançamento do GitHub (do **not** commit it).

3. ** Changelog & docs **

- [ ] Atualizar `CHANGELOG.md` com destaques voltados para o usuário (criar o arquivo se faltar); manter as entradas estritamente decrescente por versão.
- [ ] Certifique-se de README exemplos / flags correspondem ao comportamento CLI atual (nomeadamente novos comandos ou opções).

4. **Validação**

- [ ] <<CODE0>
- [ ] `pnpm test` (ou `pnpm test:coverage` se você precisar de saída de cobertura)
- [ ] `pnpm run build` (último controlo de sanidade após testes)
- [ ] `pnpm release:check` (verifica o conteúdo da embalagem npm)
- [ ] `OPENCLAW_INSTALL_SMOKE_SKIP_NONROOT=1 pnpm test:install:smoke` (Docker instalar teste de fumaça, caminho rápido; necessário antes da liberação)
- Se a libertação imediata anterior do npm for conhecida como ruptura, definir `OPENCLAW_INSTALL_SMOKE_PREVIOUS=<last-good-version>` ou `OPENCLAW_INSTALL_SMOKE_SKIP_PREVIOUS=1` para a etapa de pré-instalação.
- [ ] (Opcional) Fumaça total do instalador (adiciona cobertura não root + CLI): `pnpm test:install:smoke`
- [ ] (Opcional) Installer E2E (Docker, executa `curl -fsSL https://openclaw.bot/install.sh | bash`, a bordo, em seguida, executa chamadas de ferramentas reais):
- `pnpm test:install:e2e:openai` (requisitos `OPENAI_API_KEY`)
- `pnpm test:install:e2e:anthropic` (requisitos `ANTHROPIC_API_KEY`)
- `pnpm test:install:e2e` (necessita de ambas as chaves; executa ambos os fornecedores)
- [ ] (Opcional) Verifique o gateway da web se suas mudanças afetam os caminhos de envio/receção.

5. ** app macOS (Sparkle)**

- [ ] Build + assine o aplicativo macOS e, em seguida, zip-lo para distribuição.
- [ ] Gerar a aplicação Sparkle (notas HTML via [`scripts/make_appcast.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/make_appcast.sh)] e actualizar `appcast.xml`.
- [ ] Mantenha o app zip (e opcional dSYM zip) pronto para anexar à versão GitHub.
- [ ] Siga [macOS release](/platforms/mac/release) para os comandos exatos e env vars necessários.
- <<CODE2> deve ser numérico + monotónico (não `-beta`), pelo que o Sparkle compara correctamente as versões.
- Se notarizar, use o perfil `openclaw-notary` keychain criado a partir do App Store Connect API env vars (veja [macOS release](/platforms/mac/release)).

6. **Publicar (npm)**

- [ ] Confirmar git status está limpo; commit e push conforme necessário.
- [ ] `npm login` (verificar 2FA) se necessário.
- [ ] `npm publish --access public` (usar `--tag beta` para pré- libertações).
- [ ] Verificar o registo: `npm view openclaw version`, `npm view openclaw dist-tags` e `npx -y openclaw@X.Y.Z --version` (ou `--help`).

### Solução de problemas (notas de versão 2.0.0-beta2)

- **npm pack/publish hangs or produces enorme tarball**: o pacote de aplicativos do macOS em `dist/OpenClaw.app` (e zips de lançamento) são varridos para o pacote. Fixar por whitelisting publicar conteúdo via `package.json` `files` (incluir subdires, documentos, competências; excluir pacotes de aplicações). Confirmar com `npm pack --dry-run` que `dist/OpenClaw.app` não está listado.
- **npm auth web loop para dist-tags**: use auth legado para obter um prompt OTP:
- <<CODE5>
- **<`npx` a verificação falhou com <<CODE7>**: voltar a tentar com uma cache nova:
- <<CODE8>
- **Tag precisa remarcar após uma correção tardia**: force-update e push a tag, em seguida, garantir que os ativos de lançamento do GitHub ainda correspondam:
- `git tag -f vX.Y.Z && git push -f origin vX.Y.Z`

7. **GitHub release + appcast**

- [ ] Marcar e empurrar: `git tag vX.Y.Z && git push origin vX.Y.Z` (ou `git push --tags`).
- [ ] Crie/refresque a versão do GitHub para `vX.Y.Z` com ** título `openclaw X.Y.Z`** (não apenas a tag); corpo deve incluir a seção **full** changelog para essa versão (Highlights + Changes + Fixes), em linha (sem links nus), e ** não deve repetir o título dentro do corpo**.
- [ ] Anexar artefatos: `npm pack` tarball (opcional), `OpenClaw-X.Y.Z.zip`, e `OpenClaw-X.Y.Z.dSYM.zip` (se gerado).
- [ ] Persistir a actualização `appcast.xml` e empurrá-la (Sparkle feeds from main).
- [ ] De um directório de temperatura limpa (não `package.json`), execute `npx -y openclaw@X.Y.Z send --help` para confirmar o funcionamento dos pontos de entrada de instalação/CLI.
- [ ] Anunciar/compartilhar notas de lançamento.

# # Plugin publicar escopo (npm)

Nós só publicamos ** plugins npm existentes** sob o escopo `@openclaw/*`. Conjuntos
plugins que não estão no npm stay **disk-tree only** (ainda enviados
<<CODE1>).

Processo para derivar a lista:

1. <<CODE0> e capturar os nomes dos pacotes.
2. Compare com `extensions/*/package.json` nomes.
3. Publicar apenas a ** intersecção** (já no npm).

Lista de plug-ins npm atual (atualizar conforme necessário):

- @openclaw/bobbles
- @openclaw/diagnostics-otel
- @openclaw/discord
- @openclaw/lobster
- @openclaw/matriz
- @openclaw/msteams
- @openclaw/nextcloud-talk
- @openclaw/nostr
- @openclaw/voice-call
- @openclaw/zalo
- @openclaw/zalouser

Notas de lançamento também devem chamar **novos plugins opcionais empacotados** que não são **
em por omissão** (exemplo: `tlon`).
