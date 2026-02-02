---
summary: "Doctor command: health checks, config migrations, and repair steps"
read_when:
  - Adding or modifying doctor migrations
  - Introducing breaking config changes
---

Doutor

<<CODE0> é a ferramenta de reparação + migração para OpenClaw. Corrige o estado
config/state, verifica a saúde e fornece etapas de reparo acionáveis.

# # Começo rápido

```bash
openclaw doctor
```

Sem cabeça/automatização

```bash
openclaw doctor --yes
```

Aceitar defaults sem alerta (incluindo etapas de reparação de reinício/serviço/sandbox quando aplicável).

```bash
openclaw doctor --repair
```

Aplicar reparos recomendados sem alerta (reparos + reinicia onde seguro).

```bash
openclaw doctor --repair --force
```

Aplicar reparos agressivos também (sobrescrever configurações de supervisor personalizado).

```bash
openclaw doctor --non-interactive
```

Executar sem prompts e apenas aplicar migrações seguras (normalização de configuração + movimentos de estado on-disk). Salta ações de reiniciar/serviço/sandbox que requerem confirmação humana.
As migrações de estados legados são executadas automaticamente quando detectadas.

```bash
openclaw doctor --deep
```

Digitalizar serviços de sistema para instalações de gateway extra (lançado/systemd/schtasks).

Se quiser rever as alterações antes de escrever, abra primeiro o ficheiro de configuração:

```bash
cat ~/.openclaw/openclaw.json
```

# # O que faz (síntese)

- Actualização opcional pré-voo para git installs (apenas interactiva).
- Verificação de frescura do protocolo de IU (reconstrui a interface de controle quando o esquema de protocolo é mais recente).
- Verificação de saúde + reiniciar prompt.
- Resumo do estatuto das competências (elegível/desaparecido/bloqueado).
- Normalização de configuração para valores legados.
- O provedor OpenCode Zen substitui os avisos (<<<CODE0>>>).
- Migração de estado no disco do legado (sessões/agente dir/WhatsApp auth).
- Integridade do Estado e verificações de permissões (sessões, transcrições, dir de estado).
- Verificação de permissão de arquivo de configuração (chmod 600) ao executar localmente.
- Modelo auth health: verifica expiração de OAuth, pode atualizar tokens expirando, e relata estados de resfriamento/desativação de perfil de autenticação.
- Detecção de dir extra no espaço de trabalho (<<<CODE1>>>).
- Sandbox reparação de imagem quando sandboxing é ativado.
- Migração de serviços legados e detecção de gateway extra.
- Gateway runtime checks (serviço instalado, mas não em execução; label lançado em cache).
- Avisos de estado do canal (procurados a partir do gateway em execução).
- Auditoria de configuração do supervisor (lançado/systemd/schtasks) com reparação opcional.
- Gateway runtime best-prática verifica (Node vs Bun, version-manager caminhos).
- Diagnóstico de colisão por porta de Gateway (padrão <<CODE2>>>).
- Avisos de segurança para políticas abertas de DM.
- Avisos de autenticação do Gateway quando nenhum <<CODE3> é definido (modo local; oferece geração de token).
- verificar o Linux.
- Verificações de instalação de código fonte (incompatibilidade de espaço de trabalho do pnpm, ativos de UI em falta, binário tsx em falta).
- Grava metadados atualizados de configuração + assistente.

# # Comportamento detalhado e lógica

# # # 0) Actualização opcional (instalações instantâneas)

Se este é um git checkout e o médico está executando interativamente, ele oferece
atualizar (procurar/rebase/build) antes de executar o médico.

# # # 1) Normalização de configuração

Se a configuração contém formas de valor legado (por exemplo <<CODE0>>>
sem uma sobreposição específica do canal), o médico normaliza-os para a corrente
Esquema.

## # 2) Migrações de chaves de configuração do legado

Quando a configuração contém chaves desactualizadas, outros comandos recusam-se a executar e perguntar
você deve executar <<CODE0>>>>.

O médico vai:

- Explica que chaves foram encontradas.
- Mostra a migração aplicada.
- Reescrever <<CODE0> com o esquema atualizado.

O Gateway também executa automaticamente migrações médicas na inicialização quando detecta uma
formato de configuração legado, então configs obsoletos são reparados sem intervenção manual.

Migrações atuais:

- <<CODE0>> → <<CODE1>>>
- <<CODE2>> → <<CODE3>>
- <<CODE4>> → <<CODE5>>
- <<CODE6>> → <<CODE7>>>
- <<CODE8>> → <<CODE9>>>
- <<CODE10>> → nível superior <<CODE11>>
- <<CODE12>>/<<CODE13>> → <<CODE14>>> + <<CODE15>>
- <<CODE16>> → <<CODE17>>>
- <<CODE18>> → <<CODE19>>
- <<CODE20>> → <<CODE21>>
- <<CODE22>> → <<CODE23>>
- <<CODE24>> → <<CODE25>> + <<CODE26>> (ferramentas/elevadas/exec/sandbox/subagentes)
- <<CODE27>>/<<CODE28>/<<CODE29>>/<<CODE30>/<HTML31>>
→ <<CODE32>> + <<CODE33>> + <<CODE34>>

### 2b) O provedor OpenCode Zen substitui

Se tiver adicionado manualmente <<CODE0>> (ou <<CODE1>>>)
substitui o catálogo OpenCode Zen integrado de <<CODE2>>>. Isso pode.
forçar cada modelo em uma única API ou zero para fora custa. Doutor adverte para que você possa
remover o cancelamento e restaurar o roteamento por modelo de API + custos.

### 3) Migrações de estados legados (disk layout)

O médico pode migrar layouts antigos no disco para a estrutura atual:

- Sessões armazenam + transcrições:
- de <<CODE0>> a <<CODE1>>>
- Agente Dir:
- de <<CODE2>> a <<CODE3>>>
- WhatsApp auth state (Bailes):
- do legado <<CODE4>> (excepto <<CODE5>>)
- a <<CODE6>> (ID da conta padrão: <<CODE7>>>>)

Estas migrações são o melhor esforço e idempotente; o médico emitirá avisos quando
deixa quaisquer pastas legados para trás como backups. O Gateway/CLI também auto-migra
as sessões legadas + dir agente na inicialização então history/auth/models
via por agente sem um médico manual. WhatsApp auth é somente intencionalmente
migrado via <<CODE0>>>>.

# # # 4) Verificação da integridade do Estado (persistência de sessão, roteamento e segurança)

O diretório estatal é o tronco cerebral operacional. Se desaparecer, perdes.
sessões, credenciais, logs e config (a menos que você tenha backups em outro lugar).

Controlo médico:

- ** State dir missing**: adverte sobre a perda catastrófica do estado, alerta para recriar
o diretório, e lembra que ele não pode recuperar dados em falta.
- **As permissões de dir de estado**: verifica a escrita; ofertas para reparar permissões
(e emite uma dica <<CODE0>> quando a descompatibilidade proprietário/grupo é detectada).
- ** Session dirs faltando**: <<CODE1>> e o diretório de armazenamento de sessão são
necessário para persistir na história e evitar falhas <<CODE2>>.
- ** Desvantagem de transcrição**: avisa quando faltam entradas recentes de sessão
ficheiros de transcrição.
- **Sessão principal “1-linha JSONL”**: sinaliza quando a transcrição principal tem apenas uma
linha (história não é acumulando).
- **Multiple state dirs**: adverte quando existem múltiplas pastas <<CODE3>>
diretórios domésticos ou quando <<CODE4>>> pontos noutro lugar (lata de história
dividido entre as instalações).
- ** Lembrete de modo remoto**: se <<CODE5>>, o médico relembra- lhe
ele no hospedeiro remoto (o estado vive lá).
- ** Permissões de ficheiros de confiança**: avisa se <<CODE6>> for
grupo/mundo legível e oferece apertar para <<CODE7>>>.

## # 5) Modelo de saúde (expiração da autorização)

O médico inspeciona os perfis de OAuth na loja de autenticação, avisa quando os tokens são
expirar/expirar, e pode atualizá-los quando for seguro. Se o Código Antrópico de Claude
o perfil está estagnado, o que sugere executar <<CODE0>> (ou colar uma configuração).
Atualizar os prompts somente aparecem quando rodando interativamente (TTY); <<CODE1>>
salta as tentativas de actualização.

O médico também relata perfis de autenticação que são temporariamente inutilizáveis devido a:

- curtos resfriamentos (limites/tempos/falhas)
- deficientes mais longos (falhas de atribuição/crédito)

## 6) Validação do modelo Hooks

Se <<CODE0>> for definido, o médico valida a referência do modelo contra a
catálogo e allowlist e adverte quando ele não vai resolver ou é proibido.

## # 7) Reparação de imagens da caixa de areia

Quando o sandboxing estiver habilitado, o médico verifica as imagens do Docker e oferece- se para construir ou
mudar para nomes legados se a imagem atual estiver faltando.

## # 8) Migrações de serviço de gateway e dicas de limpeza

O médico detecta serviços de gateway legados (lançados/systemd/schtasks) e
oferece para removê-los e instalar o serviço OpenClaw usando o gateway atual
Porto. Ele também pode procurar serviços como gateway extra e imprimir dicas de limpeza.
Serviços de gateway OpenClaw com nome de perfil são considerados de primeira classe e não são
marcado como "extra".

# # # 9) Advertências de segurança

O médico emite avisos quando um prestador está aberto a DM sem uma lista de autorizações, ou
quando uma política é configurada de forma perigosa.

### 10) systemd long (Linux)

Se rodando como um serviço de usuário systemd, o médico garante que a permanência está habilitada para que o
O portal mantém-se vivo após o encerramento.

## 11) Status das habilidades

O médico imprime um resumo rápido das competências elegíveis/faltas/bloqueadas para o actual
espaço de trabalho.

### 12) Verificações de acesso (toque local)

O médico avisa quando <<CODE0>> está faltando em um gateway local e oferece
gerar um símbolo. Utilizar <<CODE1>> para forçar o token
criação em automação.

### 13) Verificação de saúde do portal + reiniciar

O médico executa uma verificação de saúde e oferece para reiniciar o gateway quando parece
Não é saudável.

# # # 14) Avisos de status do canal

Se o gateway for saudável, o médico executa uma sonda de status do canal e relata
avisos com correções sugeridas.

# # # 15) Auditoria de configuração do supervisor + reparo

O médico verifica a configuração instalada do supervisor (lançado/sistemad/schtasks) para
defaults em falta ou desactualizados (por exemplo, dependências on-line de rede e
reiniciar o atraso). Quando encontra um descompasso, recomenda uma atualização e pode
reescreva o arquivo/tarefa de serviço para os padrões atuais.

Notas:

- <<CODE0> prompts antes de reescrever a configuração do supervisor.
- <<CODE1> aceita as instruções de reparo padrão.
- <<CODE2> aplica as correções recomendadas sem aviso prévio.
- <<CODE3> sobrepõe configurações personalizadas de supervisor.
- Você sempre pode forçar uma reescrita completa via <<CODE4>>>.

# # # 16) Gateway runtime + diagnóstico de porta

O médico inspeciona o tempo de execução do serviço (PID, status de última saída) e avisa quando o
o serviço está instalado mas não está em execução. Verifica igualmente as colisões portuárias
na porta de gateway (padrão <<CODE0>>>) e relata causas prováveis (porta já
Correndo, túnel SSH).

# # # 17) Melhores práticas de corrida no portal

O médico avisa quando o serviço de gateway é executado no Bun ou em um caminho Node gerenciado por versões
(<<<CODE0>>, <<CODE1>>, <<CODE2>>, <<CODE3>>, etc.). WhatsApp + Canais de Telegram requerem Node,
e os caminhos do gerenciador de versões podem quebrar após as atualizações porque o serviço não
Carregue o seu init shell. O médico oferece migrar para um nó do sistema quando
disponível (Homebrew/apt/choco).

# # # 18) Configuração escrever + metadados de assistente

O médico persiste quaisquer alterações de configuração e metadados do assistente de carimbos para gravar o
O médico corre.

## # 19) Dicas de espaço de trabalho (backup + sistema de memória)

O médico sugere um sistema de memória de espaço de trabalho quando falta e imprime uma dica de backup
se o espaço de trabalho ainda não está sob git.

Ver [/conceitos/agente-espaço de trabalho](<<<LINK0>>>) para um guia completo
estrutura de espaço de trabalho e backup git (recomendado privado GitHub ou GitLab).
