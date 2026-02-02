---
summary: "ClawHub guide: public skills registry + CLI workflows"
read_when:
  - Introducing ClawHub to new users
  - Installing, searching, or publishing skills
  - Explaining ClawHub CLI flags and sync behavior
---

GarraHub

ClawHub é o ** registro público de habilidades para OpenClaw**. É um serviço gratuito: todas as habilidades são públicas, abertas e visíveis para todos para compartilhar e reutilizar. Uma habilidade é apenas uma pasta com um arquivo `SKILL.md` (mais arquivos de texto de suporte). Você pode navegar habilidades no aplicativo web ou usar o CLI para pesquisar, instalar, atualizar e publicar habilidades.

Site: [clawhub.com] (<https://clawhub.com)

# # Quem é este para

Se você quiser adicionar novos recursos ao seu agente OpenClaw, ClawHub é a maneira mais fácil de encontrar e instalar habilidades. Você não precisa saber como a infraestrutura funciona. Você pode:

- Procurar habilidades por linguagem simples.
- Instale uma habilidade no seu espaço de trabalho.
- Atualizar as habilidades mais tarde com um comando.
- Recua as tuas habilidades publicando-as.

# # Início rápido (não técnico)

1. Instale o CLI (veja a próxima seção).
2. Procure por algo que você precisa:
- <<CODE0>
3. Instale uma habilidade:
- <<CODE1>
4. Inicie uma nova sessão OpenClaw para que ele pegue a nova habilidade.

# # Instalar o CLI

Escolha um:

```bash
npm i -g clawhub
```

```bash
pnpm add -g clawhub
```

# # Como se encaixa no OpenClaw

Por padrão, o CLI instala habilidades em <<CODE0> sob seu diretório de trabalho atual. Se um espaço de trabalho OpenClaw estiver configurado, <<CODE1> volta para esse espaço de trabalho a menos que você sobreponha `--workdir` (ou `CLAWHUB_WORKDIR`). OpenClaw carrega habilidades de espaço de trabalho de `<workspace>/skills` e as pegará na próxima sessão**. Se você já usar `~/.openclaw/skills` ou habilidades agrupadas, as habilidades de espaço de trabalho têm precedência.

Para mais detalhes sobre como as habilidades são carregadas, compartilhadas e fechadas, veja
[Habilidades] (</tools/skills).

# # O que o serviço oferece (características)

- ** Navegação pública** de competências e seu conteúdo <<CODE0>.
- **Search** alimentado por incorporações (pesquisa de vetor), não apenas palavras-chave.
- **Versioning** com semver, changelogs e tags (incluindo `latest`).
- **Downloads** como um zip por versão.
- ** Estrelas e comentários** para feedback comunitário.
- **Moderação** ganchos para aprovações e auditorias.
- ** API amigável a CLI** para automação e scripting.

# # Comandos e parâmetros CLI

Opções globais (aplicar a todos os comandos):

- <<CODE0>: Diretório de trabalho (padrão: dir atual; cai para o espaço de trabalho OpenClaw).
- <<CODE1>: Diretório de habilidades, relativo ao workdir (padrão: `skills`).
- <<CODE3>: URL da base do site (início do navegador).
- <<CODE4>: URL base da API de registro.
- <<CODE5>: Desactivar as mensagens (não- interactivas).
- <<CODE6>: Imprima a versão CLI.

Auth:

- <<CODE0> (fluxo de navegação) ou <<CODE1>
- <<CODE2>
- `clawhub whoami`

Opções:

- <<CODE0>: Colar um token API.
- <<CODE1>: Rótulo armazenado para tokens de login do navegador (por omissão: `CLI token`).
- <<CODE3>: Não abrir um navegador (requer `--token`).

Procurar:

- <<CODE0>
- <<CODE1>: Resultados máximos.

Instalar:

- <<CODE0>
- <<CODE1>: Instale uma versão específica.
- <<CODE2>: Sobrescrever se a pasta já existe.

Actualização:

- <<CODE0>
- <<CODE1>
- <<CODE2>: Atualizar para uma versão específica (somente slug).
- <<CODE3>: Sobrescrever quando os arquivos locais não correspondem a nenhuma versão publicada.

Lista:

- `clawhub list` (lenças `.clawhub/lock.json`)

Publicar:

- <<CODE0>
- <<CODE1>: Uma lesma.
- <<CODE2>: Mostrar o nome.
- <<CODE3>: Versão Semver.
- <<CODE4>: Texto do Changelog (pode estar vazio).
- <<CODE5>: Marcas separadas por vírgulas (padrão: `latest`).

Eliminação/não-eleito (somente proprietário/admin):

- <<CODE0>
- <<CODE1>

Sincronização (scan local skills + publique new/updated):

- <<CODE0>
- <<CODE1>: Raízes extra de varredura.
- <<CODE2>: Envie tudo sem avisos.
- <<CODE3>: Mostrar o que seria enviado.
- `--bump <type>`: `patch|minor|major` para actualizações (padrão: `patch`).
- <<CODE7>: Changelog para atualizações não interativas.
- <<CODE8>: Tags separadas por vírgulas (por omissão: `latest`).
- `--concurrency <n>`: Controlos de registo (por omissão: 4).

# # Fluxos de trabalho comuns para agentes

# # Procurar por habilidades

```bash
clawhub search "postgres backups"
```

# # Baixe novas habilidades

```bash
clawhub install my-skill-pack
```

Atualizar as habilidades instaladas

```bash
clawhub update --all
```

Recua as tuas habilidades (publicar ou sincronizar)

Para uma única pasta de habilidades:

```bash
clawhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.0.0 --tags latest
```

Para analisar e fazer backup de muitas habilidades ao mesmo tempo:

```bash
clawhub sync --all
```

# # Detalhes avançados (técnicos)

Versão e etiquetas

- Cada publicação cria um novo **semever** `SkillVersion`.
- Tags (como `latest`) apontam para uma versão; as tags móveis permitem que você volte.
- Changelogs são anexados por versão e podem ser vazios ao sincronizar ou publicar atualizações.

### Mudanças locais vs versões de registro

Atualizações comparam o conteúdo de habilidade local com versões de registro usando um hash de conteúdo. Se os arquivos locais não corresponderem a nenhuma versão publicada, o CLI pergunta antes de sobrescrever (ou requer `--force` em execuções não-interativas).

Sincroniza as raízes de digitalização e recuo

<<CODE0> scans seu workdir atual primeiro. Se nenhuma habilidade for encontrada, ela cai de volta para locais legados conhecidos (por exemplo `~/openclaw/skills` e `~/.openclaw/skills`). Este é projetado para encontrar instalações de habilidade mais antigas sem bandeiras extras.

## # Armazenamento e arquivo de bloqueio

- As habilidades instaladas são registradas em `.clawhub/lock.json` sob o seu diretório de trabalho.
- Os tokens de autenticação são armazenados no arquivo de configuração ClawHub CLI (override via `CLAWHUB_CONFIG_PATH`).

## # Telemetria (contagens de instalação)

Quando você executa `clawhub sync` enquanto faz login, o CLI envia um instantâneo mínimo para calcular contagens de instalação. Você pode desabilitar isso completamente:

```bash
export CLAWHUB_DISABLE_TELEMETRY=1
```

# # Variáveis de ambiente

- <<CODE0>: Sobrescrever o URL do site.
- <<CODE1>: Sobrescrever o URL da API de registro.
- <<CODE2>: Sobrescrever onde o CLI armazena o token/config.
- <<CODE3>: Sobrescrever a pasta de trabalho padrão.
- <<CODE4>: Desactivar a telemetria em `sync`.
