---
summary: "Optional Docker-based setup and onboarding for OpenClaw"
read_when:
  - You want a containerized gateway instead of local installs
  - You are validating the Docker flow
---

# Docker (opcional)

Docker é ** opcional**. Use-o apenas se você quiser um gateway contêinerizado ou para validar o fluxo do Docker.

# # É o Docker certo para mim?

- **Sim**: você quer um ambiente de gateway isolado e descartável ou executar OpenClaw em um host sem instalações locais.
- **Não**: você está rodando em sua própria máquina e só quer o loop dev mais rápido. Use o fluxo de instalação normal.
- **Nota de sandboxing**: o agente sandboxing também usa o Docker, mas não ** requer o gateway completo para ser executado no Docker. Ver [Sandboxing] (<<<LINK0>>>).

O presente guia abrange:

- Gateway Containerizado (Total Openclaw em Docker)
- Agent Sandbox por sessão (gateway de máquina + ferramentas de agente isoladas por docker)

Detalhes do Sandboxing: [Sandboxing](<<<LINK0>>)

# # Requisitos

- Ecrã de Acoplagem (ou Motor de Acoplagem) + Composição de Acoplagem v2
- Disco suficiente para imagens + logs

# # Gateway Containerizado (Docker Compose)

Início rápido (recomendado)

Da raiz do repo:

```bash
./docker-setup.sh
```

Este programa:

- constrói a imagem de gateway
- executa o assistente de bordo
- imprime dicas de configuração opcional do provedor
- inicia o gateway via Docker Compose
- gera um token de gateway e o escreve para <<CODE0>>

Env vars opcionais:

- <<CODE0>> — instalar pacotes apt extra durante a compilação
- <<CODE1>> — adicionar montagens de ligação extra da máquina
- <<CODE2> – persistir <<CODE3>> num volume denominado

Após terminar:

- Abra <<CODE0>> no seu navegador.
- Colar o token na interface de controle (Configurações → token).

Escreve config/workspace na máquina:

- <<CODE0>>
- <<CODE1>>

Correndo em um VPS? Ver [Hetzner (Docker VPS)](<<<LINK0>>>).

## # Fluxo manual (compor)

```bash
docker build -t openclaw:local -f Dockerfile .
docker compose run --rm openclaw-cli onboard
docker compose up -d openclaw-gateway
```

## # Montes extras (opcional)

Se quiser montar diretórios de máquinas adicionais nos recipientes, defina
<<CODE0>> antes de correr <<CODE1>>>. Isto aceita
lista separada por vírgula das montagens de ligação do Docker e aplica- as a ambos
<<CODE2>> e <<CODE3>> gerando <<CODE4>>.

Exemplo:

```bash
export OPENCLAW_EXTRA_MOUNTS="$HOME/.codex:/home/node/.codex:ro,$HOME/github:/home/node/github:rw"
./docker-setup.sh
```

Notas:

- Os caminhos devem ser compartilhados com o Docker Desktop no macOS/Windows.
- Se editar <<CODE0>>, repetir <<CODE1>> para regenerar
arquivo de composição extra.
- <<CODE2>> é gerado. Não edite à mão.

## # Persista em todo o recipiente para casa (opcional)

Se você quer que <<CODE0>> persista em toda a recreação do recipiente, defina um nome
volume via <<CODE1>>>>. Isto cria um volume do Docker e monta- o em
<<CODE2>, mantendo a configuração padrão/espaço de trabalho vincular montagens. Usar um
volume nomeado aqui (não é um caminho de ligação); para vincular montagens, use
<<CODE3>>>.

Exemplo:

```bash
export OPENCLAW_HOME_VOLUME="openclaw_home"
./docker-setup.sh
```

Você pode combinar isso com montagens extras:

```bash
export OPENCLAW_HOME_VOLUME="openclaw_home"
export OPENCLAW_EXTRA_MOUNTS="$HOME/.codex:/home/node/.codex:ro,$HOME/github:/home/node/github:rw"
./docker-setup.sh
```

Notas:

- Se alterar <<CODE0>>, repetir <<CODE1>> para regenerar
arquivo de composição extra.
- O volume mencionado persiste até ser removido com <<CODE2>>.

## # Instalar pacotes apt extra (opcional)

Se você precisar de pacotes de sistema dentro da imagem (por exemplo, construir ferramentas ou mídia
bibliotecas), definido <<CODE0>>> antes de executar <<CODE1>>>>.
Isto instala os pacotes durante a compilação da imagem, por isso eles persistem mesmo se o
O recipiente é suprimido.

Exemplo:

```bash
export OPENCLAW_DOCKER_APT_PACKAGES="ffmpeg build-essential"
./docker-setup.sh
```

Notas:

- Isto aceita uma lista separada por espaços de nomes de pacotes.
- Se alterar <<CODE0>>, repetir <<CODE1>> para reconstruir
a imagem.

Reconstruções mais rápidas (recomendado)

Para acelerar as reconstruções, peça seu arquivo Docker para que as camadas de dependência sejam armazenadas em cache.
Isto evita a repetição <<CODE0>> a menos que os ficheiros de bloqueio mudem:

```dockerfile
FROM node:22-bookworm

# Install Bun (required for build scripts)
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:${PATH}"

RUN corepack enable

WORKDIR /app

# Cache dependencies unless package metadata changes
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./
COPY ui/package.json ./ui/package.json
COPY scripts ./scripts

RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build
RUN pnpm ui:install
RUN pnpm ui:build

ENV NODE_ENV=production

CMD ["node","dist/index.js"]
```

## # Configuração do canal (opcional)

Use o recipiente CLI para configurar os canais e reinicie o gateway se necessário.

WhatsApp (QR):

```bash
docker compose run --rm openclaw-cli channels login
```

Telegrama (botão do símbolo):

```bash
docker compose run --rm openclaw-cli channels add --channel telegram --token "<token>"
```

Discórdia (botão do símbolo):

```bash
docker compose run --rm openclaw-cli channels add --channel discord --token "<token>"
```

Docs: [WhatsApp](<<<LINK0>>), [Telegrama](<<LINK1>>>>), [Discord](<<LINK2>>>>)

Teste de saúde

```bash
docker compose exec openclaw-gateway node dist/index.js health --token "$OPENCLAW_GATEWAY_TOKEN"
```

Teste de fumo E2E

```bash
scripts/e2e/onboard-docker.sh
```

## # Teste de importação de fumo QR (Docker)

```bash
pnpm test:docker:qr
```

Notas

- Gateway liga- se por omissão a <<CODE0>> para utilização em contentores.
- O recipiente de gateway é a fonte de verdade para sessões (<<<CODE1>>>).

# # Agent Sandbox (gateway do host + ferramentas do Docker)

Mergulho profundo: [Sandboxing] (<<<LINK0>>>)

O que ele faz

Quando <<CODE0> é ativado, ** sessões não principais** executar ferramentas dentro de um Docker
recipiente. O gateway permanece no seu host, mas a execução da ferramenta está isolada:

- âmbito: <<CODE0>> por omissão (um contentor + espaço de trabalho por agente)
- âmbito: <<CODE1>> para isolamento por sessão
- pasta por workspace montada em <<CODE2>>
- acesso opcional à área de trabalho do agente (<<<CODE3>>>)
- permitir/negar política de ferramentas (negar vitórias)
- meios de entrada são copiados para o espaço de trabalho da caixa de areia ativa (<<CODE4>>) para que as ferramentas possam lê-lo (com <<CODE5>>, isto pousa no espaço de trabalho do agente)

Aviso: <<CODE0>> desativa o isolamento de sessão cruzada. Todas as sessões partilham
um contentor e um espaço de trabalho.

## # Per-agente sandbox perfis (multi-agente)

Se você usar roteamento multi-agente, cada agente pode substituir sandbox + configurações de ferramenta:
<<CODE0>> e <<CODE1>> (mais <<CODE2>>>). Isto permite-te correr
níveis de acesso mistos num portal:

- Acesso total (agente pessoal)
- Ferramentas somente leitura + espaço de trabalho somente leitura (família / agente de trabalho)
- Sem sistema de arquivos / shell tools (agente público)

Ver [Multi-Agent Sandbox & Tools] (<<<LINK0>>>) para exemplos,
precedência e solução de problemas.

# # Comportamento padrão

- Imagem: <<CODE0>>
- Um recipiente por agente
- Acesso ao espaço de trabalho do agente: <<CODE1> (padrão) usa <<CODE2>>
- <<CODE3> mantém o espaço de trabalho da caixa de areia em <<CODE4> e monta o espaço de trabalho do agente apenas para leitura em <<CODE5>> (desactiva <<CODE6>/<<CODE7>>/<HTML8>>>)
- <<CODE9> monta o espaço de trabalho do agente em <<CODE10>>
- Auto-prune: ocioso > 24h OU idade > 7d
- Rede: <<CODE11>> por padrão (explicativamente opt-in se precisar de saída)
- Permissão padrão: <<CODE12>>, <<CODE13>, <<CODE14>>, <<CODE15>>, <<CODE16>>, <<CODE17>>, <<CODE18>>, <<CODE19>>, <<CODE20>>, <<CODE21>>
- Negação por omissão: <<CODE22>>, <<CODE23>>, <<CODE24>>, <<CODE25>>, <<CODE26>>, <<CODE27>>>

Activar sandboxing

Se você planeja instalar pacotes em <<CODE0>>>, note:

- O padrão <<CODE0>> é <<CODE1>> (sem saída).
- <<CODE2>> bloqueia o pacote instala.
- <<CODE3>> deve ser a raiz para <<CODE4>> (omite <<CODE5>> ou definido <<CODE6>>).
OpenClaw recria automaticamente os recipientes quando <<CODE7>> (ou configuração do docker) muda
a menos que o recipiente fosse ** recentemente utilizado** (em ~5 minutos). Recipientes quentes
registar um aviso com o comando exato <<CODE8>>>.

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main", // off | non-main | all
        scope: "agent", // session | agent | shared (agent is default)
        workspaceAccess: "none", // none | ro | rw
        workspaceRoot: "~/.openclaw/sandboxes",
        docker: {
          image: "openclaw-sandbox:bookworm-slim",
          workdir: "/workspace",
          readOnlyRoot: true,
          tmpfs: ["/tmp", "/var/tmp", "/run"],
          network: "none",
          user: "1000:1000",
          capDrop: ["ALL"],
          env: { LANG: "C.UTF-8" },
          setupCommand: "apt-get update && apt-get install -y git curl jq",
          pidsLimit: 256,
          memory: "1g",
          memorySwap: "2g",
          cpus: 1,
          ulimits: {
            nofile: { soft: 1024, hard: 2048 },
            nproc: 256,
          },
          seccompProfile: "/path/to/seccomp.json",
          apparmorProfile: "openclaw-sandbox",
          dns: ["1.1.1.1", "8.8.8.8"],
          extraHosts: ["internal.service:10.0.0.5"],
        },
        prune: {
          idleHours: 24, // 0 disables idle pruning
          maxAgeDays: 7, // 0 disables max-age pruning
        },
      },
    },
  },
  tools: {
    sandbox: {
      tools: {
        allow: [
          "exec",
          "process",
          "read",
          "write",
          "edit",
          "sessions_list",
          "sessions_history",
          "sessions_send",
          "sessions_spawn",
          "session_status",
        ],
        deny: ["browser", "canvas", "nodes", "cron", "discord", "gateway"],
      },
    },
  },
}
```

Os botões de endurecimento vivem sob <<CODE0>>:
<<CODE1>>, <<CODE2>>, <<CODE3>>, <<CODE4>>, <<CODE5>>, <<CODE6>>, <<CODE7>>,
<<CODE8>>, <<CODE9>>, <<CODE10>>, <<CODE11>>.

Multiagente: substituição <<CODE0>> por agente via <<CODE1>>
(ignorado quando <<CODE2>/ <<CODE3> é <<CODE4>>>).

## # Construir a imagem padrão sandbox

```bash
scripts/sandbox-setup.sh
```

Isto constrói <<CODE0>> usando <<CODE1>>>>.

### Imagem comum da caixa de areia (opcional)

Se quiser uma imagem sandbox com ferramentas de compilação comuns (Node, Go, Rust, etc.), construa a imagem comum:

```bash
scripts/sandbox-common-setup.sh
```

Isto constrói <<CODE0>>>>. Para usá-lo:

```json5
{
  agents: {
    defaults: {
      sandbox: { docker: { image: "openclaw-sandbox-common:bookworm-slim" } },
    },
  },
}
```

## # Imagem do navegador Sandbox

Para executar a ferramenta do navegador dentro da caixa de areia, crie a imagem do navegador:

```bash
scripts/sandbox-browser-setup.sh
```

Isto compila <<CODE0>> usando
<<CODE1>>>. O recipiente roda Chromium com CDP ativado e
um observador opcional noVNC (headful via Xvfb).

Notas:

- Cabeça cheia (Xvfb) reduz o bloqueio do bot vs sem cabeça.
- O sem- cabeça ainda pode ser usado ao definir <<CODE0>>.
- Nenhum ambiente de trabalho completo (GNOME) é necessário; Xvfb fornece a exibição.

Usar a configuração:

```json5
{
  agents: {
    defaults: {
      sandbox: {
        browser: { enabled: true },
      },
    },
  },
}
```

Imagem personalizada do navegador:

```json5
{
  agents: {
    defaults: {
      sandbox: { browser: { image: "my-openclaw-browser" } },
    },
  },
}
```

Quando habilitado, o agente recebe:

- URL de controlo do navegador sandbox (para a ferramenta <<CODE0>>)
- uma URL noVNC (se activada e sem cabeça=false)

Lembre-se: se você usar uma lista de ferramentas, adicione <<CODE0>> (e removê-lo de
negá-lo) ou a ferramenta permanece bloqueada.
Regras de Prune (<<CODE1>>) também se aplicam aos recipientes do navegador.

Imagem personalizada da caixa de areia

Crie sua própria imagem e configure o ponto para ela:

```bash
docker build -t my-openclaw-sbx -f Dockerfile.sandbox .
```

```json5
{
  agents: {
    defaults: {
      sandbox: { docker: { image: "my-openclaw-sbx" } },
    },
  },
}
```

Política de ferramentas (permitir/negar)

- <<CODE0>> vence <<CODE1>>.
- Se <<CODE2> estiver vazio: todas as ferramentas (exceto negar) estão disponíveis.
- Se <<CODE3> não for vazio: apenas estão disponíveis ferramentas em <<CODE4>> (menos negação).

## # Estratégia de poda

Dois botões:

- <<CODE0>>: remover os recipientes não utilizados em horas X (0 = desactivar)
- <<CODE1>>: remover recipientes com mais de X dias (0 = desactivar)

Exemplo:

- Manter sessões ocupadas, mas vida útil:
<<CODE0>, <<CODE1>>
- Nunca podar.
<<CODE2>>, <<CODE3>>

Notas de segurança

- Parede dura só se aplica a **tools** (exec/read/write/edit/apply patch).
- Ferramentas somente de host como navegador/câmera/canvas são bloqueadas por padrão.
- Permitindo <<CODE0>> na caixa de areia ** quebra o isolamento** (o navegador corre no hospedeiro).

# # Resolução de problemas

- Imagem em falta: compilação com [<<<CODE0>>](<<LINK0>>>>) ou conjunto <<CODE1>>.
- Container não em execução: ele irá criar automaticamente por sessão sob demanda.
- Erros de permissão na sandbox: definir <<CODE2> para um UID:GID que corresponda ao seu
propriedade do espaço de trabalho montado (ou chown a pasta do espaço de trabalho).
- Ferramentas personalizadas não encontradas: OpenClaw executa comandos com <<CODE3>> (login shell), que
fontes <<CODE4> e pode reiniciar PATH. Definir <<CODE5>> para preparar o seu
caminhos de ferramentas personalizados (por exemplo, <<CODE6>>>), ou adicionar
um script em <<CODE7>> no seu arquivo Docker.
