---
summary: "Agent workspace: location, layout, and backup strategy"
read_when:
  - You need to explain the agent workspace or its file layout
  - You want to back up or migrate an agent workspace
---

# Espaço de trabalho agente

O espaço de trabalho é a casa do agente. É a única pasta de trabalho usada para
ferramentas de arquivo e para o contexto de espaço de trabalho. Mantenha-o privado e trate-o como memória.

Isto é separado do`~/.openclaw/`, que armazena config, credenciais e
sessões.

**Importante:** o espaço de trabalho é o **default cwd**, não uma caixa de areia dura. Ferramentas
resolver caminhos relativos contra o espaço de trabalho, mas caminhos absolutos ainda podem chegar
em outro lugar na máquina, a menos que o sandboxing esteja habilitado. Se necessitar de isolamento, utilize
`agents.defaults.sandbox` /gateway/sandboxing (e/ou configuração da caixa de areia por agente).
Quando o sandboxing está ativado e`workspaceAccess`não é`"rw"`, as ferramentas operam
dentro de um espaço de trabalho sandbox sob`~/.openclaw/sandboxes`, não seu espaço de trabalho host.

## Localização padrão

- Predefinição:`~/.openclaw/workspace`- Se o`OPENCLAW_PROFILE`estiver definido e não o`"default"`, o valor por omissão torna-se`~/.openclaw/workspace-<profile>`.
- Substituição no`~/.openclaw/openclaw.json`:

```json5
{
  agent: {
    workspace: "~/.openclaw/workspace",
  },
}
```

`openclaw onboard`,`openclaw configure`ou`openclaw setup`criará o
espaço de trabalho e semeie os arquivos bootstrap se eles estiverem faltando.

Se você já gerenciar os arquivos de espaço de trabalho você mesmo, você pode desativar o bootstrap
criação de ficheiros:

```json5
{ agent: { skipBootstrap: true } }
```

## Pastas extra de espaço de trabalho

Instalações mais antigas podem ter criado`~/openclaw`. Manter múltiplos espaços de trabalho
diretórios ao redor pode causar confusão auth ou estado drif, porque apenas um
O espaço de trabalho está activo de cada vez.

**Recomendação:** manter um único espaço de trabalho ativo. Se já não utilizar o
pastas extras, arquivar ou movê-las para Lixo (por exemplo`trash ~/openclaw`.
Se você intencionalmente manter vários espaços de trabalho, certifique-se`agents.defaults.workspace`aponta para o ativo.

`openclaw doctor`avisa quando detecta diretórios extra de espaço de trabalho.

## Mapa de arquivos do espaço de trabalho (o que cada arquivo significa)

Estes são os arquivos padrão que OpenClaw espera dentro da área de trabalho:

-`AGENTS.md`- Instruções de funcionamento para o agente e como deve usar a memória.
- Carregado no início de cada sessão.
- Bom lugar para regras, prioridades e detalhes de "como se comportar".

-`SOUL.md`- Persona, tom e limites.
- Carreguei todas as sessões.

-`USER.md`- Quem é o utilizador e como os tratar.
- Carreguei todas as sessões.

-`IDENTITY.md`- O nome do agente, vibe e emoji.
- Criado/atualizado durante o ritual de bootstrap.

-`TOOLS.md`- Notas sobre suas ferramentas e convenções locais.
- Não controla a disponibilidade da ferramenta; é apenas orientação.

-`HEARTBEAT.md`- Verificação opcional para batimentos cardíacos.
- Seja breve para evitar queimaduras.

-`BOOT.md`- Lista de verificação de inicialização opcional executada ao reiniciar gateway quando os ganchos internos estão habilitados.
- Seja breve; use a ferramenta de mensagem para envios de saída.

-`BOOTSTRAP.md`- Ritual de primeira.
- Só criado para um novo espaço de trabalho.
- Apaga-o depois do ritual estar completo.

-`memory/YYYY-MM-DD.md`- Diário de memória (um arquivo por dia).
- Recomendado para ler hoje + ontem no início da sessão.

-`MEMORY.md`(facultativo)
- Memória de longo prazo.
- Só carregar na sessão principal, privada (contextos não compartilhados/grupo).

Veja [Memory]/concepts/memory para o fluxo de trabalho e flush automático de memória.

-`skills/`(facultativo)
- Habilidades específicas do espaço de trabalho.
- Substitui as competências geridas/abundadas quando os nomes colidem.

-`canvas/`(facultativo)
- Arquivos de interface de tela para telas de nó (por exemplo`canvas/index.html`.

Se algum arquivo de bootstrap estiver faltando, o OpenClaw injeta um marcador de "arquivo em falta"
a sessão e continua. Arquivos grandes bootstrap são truncados quando injetados;
ajustar o limite com`agents.defaults.bootstrapMaxChars`(padrão: 20000).`openclaw setup`pode recriar padrões em falta sem sobrescrever existentes
ficheiros.

## O que NÃO está no espaço de trabalho

Estes vivem ao abrigo do`~/.openclaw/`e não devem ser comprometidos com o plano de trabalho:

-`~/.openclaw/openclaw.json`(configuração)
-`~/.openclaw/credentials/`(toques OAuth, teclas API)
-`~/.openclaw/agents/<agentId>/sessions/`(transcrições de sessão + metadados)
-`~/.openclaw/skills/`(competências de gestão)

Se você precisar migrar sessões ou config, copie- as separadamente e mantenha- as
fora de controle de versão.

## Git backup (recomendado, privado)

Tratar o espaço de trabalho como memória privada. Coloque em um **private** git repo para que seja
Recuado e recuperável.

Execute estes passos na máquina onde o Gateway corre (que é onde o
vida no espaço de trabalho).

## # 1) Inicializar o repo

Se git estiver instalado, novos espaços de trabalho são inicializados automaticamente. Se isto
workspace não é já um repo, execute:

```bash
cd ~/.openclaw/workspace
git init
git add AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md memory/
git commit -m "Add agent workspace"
```

## # 2) Adicione um comando privado (opções amigáveis ao início)

Opção A: UI Web do GitHub

1. Crie um novo repositório **private** no GitHub.
2. Não inicializar com um README (evoids merge conflicts).
3. Copie o URL remoto HTTPS.
4. Adicione o controle remoto e empurre:

```bash
git branch -M main
git remote add origin <https-url>
git push -u origin main
```

Opção B: GitHub CLI `gh`

```bash
gh auth login
gh repo create openclaw-workspace --private --source . --remote origin --push
```

Opção C: UI Web GitLab

1. Crie um novo repositório **private** no GitLab.
2. Não inicializar com um README (evoids merge conflicts).
3. Copie o URL remoto HTTPS.
4. Adicione o controle remoto e empurre:

```bash
git branch -M main
git remote add origin <https-url>
git push -u origin main
```

### 3) Atualizações em andamento

```bash
git status
git add .
git commit -m "Update memory"
git push
```

## Não cometa segredos

Mesmo num repositório privado, evite guardar segredos no espaço de trabalho:

- chaves API, tokens OAuth, senhas ou credenciais privadas.
- Qualquer coisa sob`~/.openclaw/`.
- Despejos de conversas ou anexos sensíveis.

Se você deve armazenar referências sensíveis, use placeholders e manter o real
segredo em outro lugar (password manager, variáveis de ambiente, ou`~/.openclaw/`.

Iniciador`.gitignore`sugerido:

```gitignore
.DS_Store
.env
**/*.key
**/*.pem
**/secrets*
```

## Movendo o espaço de trabalho para uma nova máquina

1. Clone o repo para o caminho desejado (padrão`~/.openclaw/workspace`.
2. Defina`agents.defaults.workspace`para esse caminho em`~/.openclaw/openclaw.json`.
3. Execute`openclaw setup --workspace <path>`para semear quaisquer arquivos em falta.
4. Se você precisa de sessões, copie`~/.openclaw/agents/<agentId>/sessions/`do
máquina antiga separadamente.

## Notas avançadas

- Roteamento multiagentes pode usar diferentes espaços de trabalho por agente. Ver
[Roteamento do canal] /concepts/channel-routing para configuração de roteamento.
- Se o`agents.defaults.sandbox`estiver activo, as sessões não principais poderão usar a caixa de areia por sessão
Espaços de trabalho ao abrigo do`agents.defaults.sandbox.workspaceRoot`.
