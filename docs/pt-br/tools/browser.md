---
summary: "Integrated browser control service + action commands"
read_when:
  - Adding agent-controlled browser automation
  - Debugging why openclaw is interfering with your own Chrome
  - Implementing browser settings + lifecycle in the macOS app
---

# Navegador (gerido por Openclaw)

OpenClaw pode executar um **dedicado Chrome/Brave/Edge/Chromium perfil** que o agente controla.
É isolado do seu navegador pessoal e é gerido através de um pequeno local
serviço de controle dentro da Gateway (apenas loopback).

Vista inicial:

- Pense nisso como um navegador **separado, somente para agentes**.
- O perfil <<CODE0> não toca no seu perfil do navegador pessoal.
- O agente pode abrir abas, ler páginas, clicar e digitar** em uma faixa segura.
- O perfil padrão <<CODE1> usa o navegador Chromium ** padrão do sistema
relé de extensão; mude para <<CODE2> para o navegador gerenciado isolado.

# # O que tens

- Um perfil de navegador separado chamado ** openclaw** (acento laranja por padrão).
- Controle de tabulação determinístico (lista/aberto/foco/fechar).
- Ações de agente (clique/tipo/drag/selecionar), instantâneos, capturas de tela, PDFs.
- Apoio opcional multi-perfis (`openclaw`, <CODE1>>, < <CODE2>>, ...).

Este navegador é ** not** seu driver diário. É uma superfície segura e isolada para
Automação e verificação do agente.

# # Começo rápido

```bash
openclaw browser --browser-profile openclaw status
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

Se você conseguir “desactivar o navegador”, ative-o na configuração (veja abaixo) e reinicie o
Gateway.

Perfil: `openclaw` vs `chrome`

- <<CODE0>: navegador isolado e gerido (sem necessidade de extensão).
- <<CODE1>: relé de extensão para o seu navegador ** do sistema** (requer a OpenClaw
extensão a ser anexada a uma aba).

Definir `browser.defaultProfile: "openclaw"` se você quiser modo gerenciado por padrão.

Configuração

As configurações do navegador vivem em `~/.openclaw/openclaw.json`.

```json5
{
  browser: {
    enabled: true, // default: true
    // cdpUrl: "http://127.0.0.1:18792", // legacy single-profile override
    remoteCdpTimeoutMs: 1500, // remote CDP HTTP timeout (ms)
    remoteCdpHandshakeTimeoutMs: 3000, // remote CDP WebSocket handshake timeout (ms)
    defaultProfile: "chrome",
    color: "#FF4500",
    headless: false,
    noSandbox: false,
    attachOnly: false,
    executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    profiles: {
      openclaw: { cdpPort: 18800, color: "#FF4500" },
      work: { cdpPort: 18801, color: "#0066CC" },
      remote: { cdpUrl: "http://10.0.0.42:9222", color: "#00AA00" },
    },
  },
}
```

Notas:

- O serviço de controle do navegador se liga ao loopback em uma porta derivada de <<CODE0>
(padrão: `18791`, que é gateway + 2). O relé usa a porta seguinte (<`18792`).
- Se substituir a porta Gateway (`gateway.port` ou <CODE4>>),
as portas derivadas do navegador mudam para permanecer na mesma “família”.
- <<CODE5> defaults to the relé port when unset.
- <<CODE6> é aplicável aos controlos de acessibilidade à distância (não- loopback) CDP.
- `remoteCdpHandshakeTimeoutMs` aplica- se a verificações remotas de acessibilidade do WebSocket CDP.
- `attachOnly: true` significa “nunca lançar um navegador local; só anexar se já estiver em execução.”
- `color` + por perfil `color` pintar a interface do navegador para que você possa ver qual perfil está ativo.
- O perfil padrão é `chrome` (relé de extensão). Use `defaultProfile: "openclaw"` para o navegador gerenciado.
- Ordem de detecção automática: navegador padrão do sistema se baseado em Chromium; caso contrário Chrome → Brave → Edge → Chromium → Chrome Canary.
- Perfis locais <<CODE13> auto-atribuições `cdpPort`/<CODE15> – definir os perfis apenas para CDP remoto.

# # Use Bravo (ou outro navegador baseado em Chromium)

Se seu navegador **default do sistema** for baseado em Chromium (Chrome/Brave/Edge/etc),
Openclaw usa-o automaticamente. Definir `browser.executablePath` para sobrepor
detecção automática:

Exemplo de CLI:

```bash
openclaw config set browser.executablePath "/usr/bin/google-chrome"
```

```json5
// macOS
{
  browser: {
    executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
  }
}

// Windows
{
  browser: {
    executablePath: "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
  }
}

// Linux
{
  browser: {
    executablePath: "/usr/bin/brave-browser"
  }
}
```

# # Controle local vs remoto

- ** Controle local (padrão):** o Gateway inicia o serviço de controle loopback e pode lançar um navegador local.
- ** Controle remoto (node host):** execute um host de nó na máquina que tem o navegador; o gateway proxies navegador ações para ele.
- ** CDP remoto:** definido `browser.profiles.<name>.cdpUrl` (ou < <CODE1>>) a
anexar a um navegador remoto baseado em Chromium. Neste caso, o OpenClaw não lançará um navegador local.

URLs CDP remotas podem incluir autenticação:

- Fichas de consulta (por exemplo, `https://provider.example?token=<token>`)
- Autorização HTTP Basic (por exemplo, `https://user:pass@provider.example`)

OpenClaw preserva a autenticação ao chamar <<CODE0> e ao conectar
to CDP WebSocket. Prefere variáveis de ambiente ou gerenciadores de segredos para
tokens em vez de os enviar para arquivos de configuração.

# # Proxy do navegador Nó (padrão zero-config)

Se você executar um host **node** na máquina que tem seu navegador, OpenClaw pode
ferramenta de navegador de rota automática chama para esse nó sem qualquer configuração do navegador extra.
Este é o caminho padrão para gateways remotos.

Notas:

- O host do nó expõe seu servidor de controle de navegador local através de um comando **proxy**.
- Os perfis vêm da própria configuração `browser.profiles` do nó (mesmo que local).
- Desactivar se não o quiser:
- No nó: `nodeHost.browserProxy.enabled=false`
- No portal: `gateway.nodes.browser.mode="off"`

# # Navegador sem (alojado remoto CDP)

[Browserless](<https://browserless.io) é um serviço de Chromium hospedado que expõe
Endpoints CDP sobre HTTPS. Você pode apontar um perfil de navegador OpenClaw em um
Endpoint de região sem navegador e autentice-se com sua chave API.

Exemplo:

```json5
{
  browser: {
    enabled: true,
    defaultProfile: "browserless",
    remoteCdpTimeoutMs: 2000,
    remoteCdpHandshakeTimeoutMs: 4000,
    profiles: {
      browserless: {
        cdpUrl: "https://production-sfo.browserless.io?token=<BROWSERLESS_API_KEY>",
        color: "#00AA00",
      },
    },
  },
}
```

Notas:

- Substituir `<BROWSERLESS_API_KEY>` por seu verdadeiro token Navegador.
- Escolha o ponto final da região que corresponde à sua conta do Browserless (veja seus documentos).

# # Segurança

Ideias-chave:

- Controle de navegador é loopback-only; fluxos de acesso através do auth ou emparelhamento de nó do Gateway.
- Mantenha o Gateway e qualquer host de nós em uma rede privada (tailscale); evite a exposição pública.
- Trate URLs CDP remotas / tokens como segredos; prefira env vars ou um gerenciador de segredos.

Dicas CDP remotas:

- Prefere endpoints HTTPS e tokens de curta duração sempre que possível.
- Evite incorporar tokens de longa duração diretamente em arquivos de configuração.

## Perfil (multi-browser)

O OpenClaw suporta vários perfis nomeados (configurações de rota). Os perfis podem ser:

- **Openclaw-gerenciado**: uma instância de navegador dedicada baseada em Chromium com seu próprio diretório de dados do usuário + porta CDP
- ** Remote**: um URL CDP explícito (navegador baseado em crimium em execução em outro lugar)
- **Relé de extensão**: sua guia de Chrome existente através do relé local + Extensão de Chrome

Predefinição:

- O perfil <<CODE0> é criado automaticamente se faltar.
- O perfil <<CODE1> é incorporado para o relé de extensão do Chrome (pontos `http://127.0.0.1:18792` por padrão).
- Portas CDP locais alocar de **18800-1889** por padrão.
- Excluindo um perfil move seu diretório de dados local para Lixo.

Todos os objetivos de controle aceitam `?profile=<name>`; o CLI usa `--browser-profile`.

# # Relé de extensão Chrome (use o seu Chrome existente)

O OpenClaw também pode dirigir **suas abas Chrome existentes** (sem "openclaw" instância Chrome separada) através de um relé CDP local + uma extensão Chrome.

Guia completo: [Extensão do cromo] (</tools/chrome-extension)

Fluxo:

- O Gateway é executado localmente (mesma máquina) ou um host de nó é executado na máquina do navegador.
- Um servidor local **relay** escuta em um loopback `cdpUrl` (padrão: `http://127.0.0.1:18792`).
- Você clica no ícone de extensão **OpenClaw Browser Relay** em uma aba para anexar (não se encaixa automaticamente).
- O agente controla essa guia através da ferramenta normal `browser`, selecionando o perfil certo.

Se o Gateway for executado em outro lugar, execute um host de nó na máquina do navegador para que o Gateway possa proxy das ações do navegador.

Sessões de areia

Se a sessão do agente for sandbox, a ferramenta <<CODE0> pode ser padrão para `target="sandbox"` (navegador sandbox).
A aquisição do relé de extensão do Chrome requer o controle do navegador host, então:

- executar a sessão sem areia, ou
- definir `agents.defaults.sandbox.browser.allowHostControl: true` e utilizar `target="host"` ao chamar a ferramenta.

Configuração

1. Carregar a extensão (dev/desembalado):

```bash
openclaw browser extension install
```

- Chrome → `chrome://extensions` → activar “Modo de desenvolvimento”
- “Carregado desempacotado” → selecione o diretório impresso por `openclaw browser extension path`
- Pin a extensão, em seguida, clique na aba que você deseja controlar (bodge mostra `ON`).

2. Use-o:

- CLI: `openclaw browser --browser-profile chrome tabs`
- Ferramenta agente: `browser` com `profile="chrome"`

Opcional: se você quiser um nome diferente ou porta relé, crie seu próprio perfil:

```bash
openclaw browser create-profile \
  --name my-chrome \
  --driver extension \
  --cdp-url http://127.0.0.1:18792 \
  --color "#00AA00"
```

Notas:

- Este modo depende de Playwright-on-CDP para a maioria das operações (fotos de tela/snapshots/actions).
- Desanexar clicando novamente no ícone da extensão.

# # Garantias de isolamento

- **Dir de dados do usuário dedicado**: nunca toque no seu perfil de navegador pessoal.
- **Portas dedicadas**: evita `9222` para evitar colisões com fluxos de trabalho dev.
- **Controlo de tabulação determinístico**: tabulações alvo por `targetId`, não por “último tabulação”.

# # Seleção do navegador

Ao lançar localmente, o OpenClaw escolhe o primeiro disponível:

1. Chrome
2. Corajosa
3. Borda
4. Crómio
5. Cromo Canário

Você pode substituir com `browser.executablePath`.

Plataformas:

- macOS: verificações `/Applications` e `~/Applications`.
- Linux: procura `google-chrome`, `brave`, `microsoft-edge`, `chromium`, etc.
- Windows: verifica locais comuns de instalação.

# # API de controle (opcional)

Para integrações locais apenas, o Gateway expõe uma pequena API HTTP loopback:

- Status/start/stop: `GET /`, `POST /start`, `POST /stop`
- Tabs: `GET /tabs`, `POST /tabs/open`, `POST /tabs/focus`, <<CODE6>
- Instantâneo/ecrã: `GET /snapshot`, `POST /screenshot`
- Acções: `POST /navigate`, `POST /act`
- Ganchos: `POST /hooks/file-chooser`, `POST /hooks/dialog`
- Downloads: `POST /download`, `POST /wait/download`
- Depuração: `GET /console`, `POST /pdf`
- Depuração: `GET /errors`, `GET /requests`, `POST /trace/start`, `POST /trace/stop`, `POST /highlight`
- Rede: `POST /response/body`
- Estado: `GET /cookies`, `POST /cookies/set`, `POST /cookies/clear`
- Estado: `GET /storage/:kind`, `POST /storage/:kind/set`, `POST /storage/:kind/clear`
- Definições: `POST /set/offline`, <<CODE30>, `POST /set/credentials`, `POST /set/geolocation`, <<CODE33>, `POST /set/timezone`, <<CODE35>, `POST /set/device`

Todos os objetivos aceitam `?profile=<name>`.

## # Exigência de dramaturgo

Algumas características (navigar/act/AI snapshot/role snapshot, screenshots de elementos, PDF) requerem
Dramaturgo. Se o Playwright não estiver instalado, esses terminais devolvem um 501 claro
erro. Instantâneos ARIA e imagens básicas ainda funcionam para o Chrome gerenciado por openclaw.
Para o driver de relé de extensão Chrome, instantâneos e capturas de tela ARIA requerem Playwright.

Se você ver `Playwright is not available in this gateway build`, instale o
Pacote Playwright (não `playwright-core`) e reinicie o gateway, ou reinstale
Openclaw com suporte ao navegador.

# # Como funciona (interno)

Fluxo de alto nível:

- Um pequeno **control server** aceita solicitações HTTP.
- Liga-se a navegadores baseados em Chromium (Chrome/Brave/Edge/Chromium) via **CDP**.
- Para ações avançadas (click/type/snapshot/PDF), usa **Playwright** no topo
de CDP.
- Quando falta o Playwright, só estão disponíveis operações não-Playwright.

Este design mantém o agente em uma interface estável, determinística, deixando
você troca navegadores e perfis locais/remotos.

# # CLI referência rápida

Todos os comandos aceitam <<CODE0> para direcionar um perfil específico.
Todos os comandos também aceitam `--json` para saída legível por máquina (carga útil estável).

Básicos:

- <<CODE0>
- <<CODE1>
- <<CODE2>
- `openclaw browser tabs`
- `openclaw browser tab`
- <<CODE5>
- <<CODE6>
- <<CODE7>
- <<CODE8>
- `openclaw browser focus abcd1234`
- `openclaw browser close abcd1234`

Inspecção:

- <<CODE0>
- <<CODE1>
- <<CODE2>
- `openclaw browser screenshot --ref e12`
- `openclaw browser snapshot`
- <<CODE5>
- <<CODE6>
- <<CODE7>
- <<CODE8>
- `openclaw browser snapshot --selector "#main" --interactive`
- `openclaw browser snapshot --frame "iframe#main" --interactive`
- <<CODE11>
- `openclaw browser errors --clear`
- <<CODE13>
- `openclaw browser pdf`
- <<CODE15>

Acções:

- <<CODE0>
- <<CODE1>
- <<CODE2>
- `openclaw browser click e12 --double`
- `openclaw browser type 23 "hello" --submit`
- <<CODE5>
- <<CODE6>
- <<CODE7>
- <<CODE8>
- `openclaw browser select 9 OptionA OptionB`
- `openclaw browser download e12 /tmp/report.pdf`
- <<CODE11>
- `openclaw browser upload /tmp/file.pdf`
- <<CODE13>
- `openclaw browser dialog --accept`
- <<CODE15>
- <<CODE16>
- <<CODE17>
- `openclaw browser highlight e12`
- `openclaw browser trace start`
- <<CODE20>

Estado:

- <<CODE0>
- <<CODE1>
- <<CODE2>
- `openclaw browser storage local get`
- `openclaw browser storage local set theme dark`
- <<CODE5>
- <<CODE6>
- <<CODE7>
- <<CODE8>
- `openclaw browser set credentials --clear`
- `openclaw browser set geo 37.7749 -122.4194 --origin "https://example.com"`
- <<CODE11>
- `openclaw browser set media dark`
- <<CODE13>
- `openclaw browser set locale en-US`
- <<CODE15>

Notas:

- `upload` e <<CODE1> são **armamento** chamadas; executá-las antes do clique / imprensa
que desencadeia o seletor/dialogo.
- <<CODE2> também pode definir entradas de arquivos diretamente via `--input-ref` ou `--element`.
- <<CODE5>:
- `--format ai` (padrão quando o Playwright está instalado): retorna um instantâneo de IA com refs numéricos (`aria-ref="<n>"`).
- `--format aria`: retorna a árvore de acessibilidade (sem refs; apenas inspeção).
- `--efficient` (ou `--mode efficient`): predefinição do instantâneo compacto (interactivo + compacto + profundidade + maxChars inferior).
- Config default (tool/CLI only): set `browser.snapshotDefaults.mode: "efficient"` para usar snapshots eficientes quando o chamador não passa por um modo (veja [Gateway configuration](</gateway/configuration#browser-openclaw-managed-browser)).
- Opções de instantâneo (`--interactive`, <CODE13>, `--depth`, `--selector`) forçam um instantâneo baseado em funções com refs como `ref=e12`.
- `--frame "<iframe selector>"` scopes role snapshots to an iframe (pars with role refs like `e12`).
- `--interactive` produz uma lista plana e fácil de escolher de elementos interativos (melhor para ações de condução).
- <<CODE20> adiciona uma imagem viewport-only com etiquetas ref sobrepostas (prints `MEDIA:<path>`).
- <<CODE22>/<<CODE23>/etc requerem um `ref` de `snapshot` ( quer numérico `12` ou ref `e12`).
Selectores CSS não são intencionalmente suportados para ações.

# # Instantâneos e árbitros

OpenClaw suporta dois estilos “snapshot”:

- Snapshot AI (refs numéricos)**: `openclaw browser snapshot` (padrão; `--format ai`)
- Saída: um instantâneo de texto que inclui refs numéricos.
- Acções: `openclaw browser click 12`, `openclaw browser type 23 "hello"`.
- Internamente, o ref é resolvido via Playwright `aria-ref`.

- ** Snapshot Role (refs como `e12`)**: `openclaw browser snapshot --interactive` (ou `--compact`, `--depth`, `--selector`, `--frame`)
- Saída: uma lista/árvore baseada em funções com `[ref=e12]` (e opcional `[nth=1]`).
- Acções: `openclaw browser click e12`, `openclaw browser highlight e12`.
- Internamente, o ref é resolvido via `getByRole(...)` (mais `nth()` para duplicatas).
- Adicionar `--labels` para incluir uma imagem do viewport com rótulos sobrepostos `e12`.

Comportamento de referência:

- Refs são ** não estável entre as navegações**; se algo falhar, re-run `snapshot` e usar um ref fresco.
- Se o snapshot de papel foi tirado com <<CODE1>, os refs de papel são escopos para esse iframe até o próximo snapshot de papel.

# # Esperar power-ups

Você pode esperar mais do que apenas tempo/texto:

- Aguarde pelo URL (globos suportados pelo Playwright):
- <<CODE0>
- Aguardar o estado de carga:
- <<CODE1>
- Espera por um predicado JS.
- <<CODE2>
- Aguarde que um seletor se torne visível:
- `openclaw browser wait "#main"`

Estes podem ser combinados:

```bash
openclaw browser wait "#main" \
  --url "**/dash" \
  --load networkidle \
  --fn "window.ready===true" \
  --timeout-ms 15000
```

## Depurar fluxos de trabalho

Quando uma ação falha (por exemplo, “não visível”, “violação de modo restrito”, “coberto”):

1. <<CODE0>
2. Utilização `click <ref>` / `type <ref>` (prefere refs de papel em modo interativo)
3. Se ainda falhar: `openclaw browser highlight <ref>` para ver o que o dramaturgo está mirando
4. Se a página se comportar de forma estranha:
- `openclaw browser errors --clear`
- <<CODE5>
5. Para depuração profunda: gravar um traço:
- <<CODE6>
- reproduzir a questão
- `openclaw browser trace stop` (impressões `TRACE:<path>`)

# # Saída JSON

`--json` é para scripts e ferramentas estruturadas.

Exemplos:

```bash
openclaw browser status --json
openclaw browser snapshot --interactive --json
openclaw browser requests --filter api --json
openclaw browser cookies --json
```

Os instantâneos de papéis em JSON incluem `refs` mais um pequeno bloco <<CODE1> (linhas/chars/refs/interativo) para que as ferramentas possam raciocinar sobre o tamanho e densidade da carga útil.

# # Botões de estado e ambiente

Estes são úteis para "fazer o site se comportar como X" fluxos de trabalho:

- Cookies: <<CODE0>, <<CODE1>, <<CODE2>
- Armazenamento: `storage local|session get|set|clear`
- Desligado: `set offline on|off`
- Cabeçalhos: `set headers --json '{"X-Debug":"1"}'` (ou `--clear`)
- Autorização básica HTTP: `set credentials user pass` (ou < <CODE8>>)
- Geolocalização: `set geo <lat> <lon> --origin "https://example.com"` (ou `--clear`)
- Mídia: `set media dark|light|no-preference|none`
- Timezone / locale: `set timezone ...`, `set locale ...`
- Dispositivo / viewport:
- `set device "iPhone 14"` (O dispositivo Playwright é predefinido)
- <<CODE15>

# # Segurança e privacidade

- O perfil do navegador openclaw pode conter sessões de login; trate-o como sensível.
- <<CODE0>/ `openclaw browser evaluate` e <<CODE2>
execute JavaScript arbitrário no contexto da página. A injecção imediata pode conduzir
Isto. Desative-o com `browser.evaluateEnabled=false` se você não precisar.
- Para logins e notas anti-bot (X/Twitter, etc.), consulte [Login do navegador + Posting do X/Twitter] (</tools/browser-login).
- Mantenha o Gateway/Node host privado (loopback ou tailnet-only).
- Endpoints remotos CDP são poderosos; túnel e protegê-los.

# # Resolução de problemas

Para problemas específicos do Linux (especialmente o Chromium), consulte
[Problemas do navegador] (</tools/browser-linux-troubleshooting).

# # Ferramentas de agente + como o controle funciona

O agente obtém ** uma ferramenta** para automação do navegador:

- `browser` — status/start/stop/tabs/open/focus/close/close/snapshot/screenshot/navigate/act

Como se mapeia:

- <<CODE0> retorna uma árvore de UI estável (AI ou ARIA).
- <<CODE1> utiliza o instantâneo `ref` IDs para clicar/tipo/drag/selecionar.
- <<CODE3> captura pixels (página completa ou elemento).
- <<CODE4> aceita:
- <<CODE5> para escolher um perfil de navegador nomeado (openclaw, cromo ou CDP remoto).
- `target` (`sandbox` `host` `node`) para selecionar onde o navegador vive.
- Nas sessões em caixas de areia, `target: "host"` requer `agents.defaults.sandbox.browser.allowHostControl=true`.
- Se `target` for omitido: sessões sandboxe padrão para `sandbox`, sessões não sandbox padrão para `host`.
- Se um nó com capacidade para navegador estiver conectado, a ferramenta pode direcionar automaticamente para ele, a menos que você pin `target="host"` ou `target="node"`.

Isso mantém o agente determinístico e evita seletores quebradiços.
