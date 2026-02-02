---
summary: "Move (migrate) a OpenClaw install from one machine to another"
read_when:
  - You are moving OpenClaw to a new laptop/server
  - You want to preserve sessions, auth, and channel logins (WhatsApp, etc.)
---

Migrando Openclaw para uma nova máquina

Este guia migra um OpenClaw Gateway de uma máquina para outra **sem refazer a bordo**.

A migração é simples conceitualmente:

- Copie o diretório **state** (<<<CODE0>>, padrão: <<CODE1>>) — isso inclui configuração, autenticação, sessões e estado do canal.
- Copie seu **workspace** (<<<CODE2>> por padrão) — isso inclui seus arquivos de agente (memória, prompts, etc.).

Mas existem armas comuns em torno de ** perfis**, ** licenças**, e ** cópias parciais**.

# # # Antes de começares (o que estás a migrar)

## # 1) Identifique seu diretório de estado

A maioria das instalações usa o padrão:

- **Dir Estado:** <<CODE0>>

Mas pode ser diferente se utilizar:

- <<CODE0> (muitas vezes torna-se <<CODE1>>)
- <<CODE2>>

Se você não tiver certeza, corra na máquina **old**:

```bash
openclaw status
```

Procure menções de <<CODE0>> / perfil na saída. Se você executar vários gateways, repita para cada perfil.

# # # 2) Identifique seu espaço de trabalho

Por omissão comum:

- <<CODE0>> (espaço de trabalho recomendado)
- uma pasta personalizada criada

Seu espaço de trabalho é onde arquivos como <<CODE0>>, <<CODE1>>>, e <<CODE2> vivem.

# # # 3) Entenda o que você vai preservar

Se você copiar ** tanto a dir estado e espaço de trabalho, você manter:

- Configuração do portal (<<<CODE0>>)
- Perfis de autenticação / teclas API / tokens OAuth
- Histórico de sessão + estado do agente
- Estado do canal (por exemplo, login/sessão do WhatsApp)
- Seus arquivos de espaço de trabalho (memória, notas de habilidades, etc.)

Se você copiar **apenas** a área de trabalho (por exemplo, via Git), você faz **não** preservar:

- sessões
- credenciais
- logins de canais

Os que vivem abaixo de <<CODE0>>>.

# # Passos de migração (recomendado)

Passo 0 - Faça um backup (máquina velha)

Na máquina **old**, pare o gateway primeiro para que os arquivos não mudem a cópia média:

```bash
openclaw gateway stop
```

(Opcional mas recomendado) arquivar a pasta de estado e espaço de trabalho:

```bash
# Adjust paths if you use a profile or custom locations
cd ~
tar -czf openclaw-state.tgz .openclaw

tar -czf openclaw-workspace.tgz .openclaw/workspace
```

Se você tem vários perfis/dires de estado (por exemplo, <<CODE0>>, <<CODE1>>>>>>>), arquivar cada um.

### Passo 1 — Instale OpenClaw na nova máquina

Na máquina **nova**, instale o CLI (e Node se necessário):

- Ver: [Instalar] (<<<LINK0>>>)

Nesta fase, tudo bem se a onboarding criar um novo <<CODE0>> — você irá sobrescrevê-lo no próximo passo.

### Passo 2 — Copie a dir estado + espaço de trabalho para a nova máquina

Copiar ** ambos**:

- <<CODE0>> (padrão <<CODE1>>)
- o seu espaço de trabalho (por omissão <<CODE2>>>)

Abordagens comuns:

- <<CODE0>> as bolas de alcatrão e extrato
- <<CODE1>> sobre SSH
- unidade externa

Após a cópia, garantir:

- Foram incluídos diretórios ocultos (por exemplo, <<CODE0>>>)
- A propriedade do arquivo está correta para o usuário executando o gateway

### Passo 3 — Executar Doutor (migrações + reparo de serviço)

Na nova máquina:

```bash
openclaw doctor
```

O médico é o comando “aborrecimento seguro”. Ele repara serviços, aplica migrações de configuração, e adverte sobre incompatibilidades.

Depois:

```bash
openclaw gateway restart
openclaw status
```

# # Armas comuns (e como evitá-las)

## Footgun: perfil / descompasso estado-dir

Se você executou o gateway antigo com um perfil (ou <<CODE0>>), e o novo gateway usa um diferente, você verá sintomas como:

- alterações de configuração que não tenham efeito
- canais em falta / logado
- histórico de sessão vazio

Corrigir: execute o gateway/service usando o **mesma** profile/state dir que você migrou, em seguida, reexecute:

```bash
openclaw doctor
```

## Footgun: copiando apenas <<CODE0>>

<<CODE0> não é suficiente. Muitos fornecedores armazenam o estado sob:

- <<CODE0>>
- <<CODE1>>

Migra sempre toda a pasta <<CODE0>>>.

Footgun: permissões / propriedade

Se você copiou como root ou usuários alterados, o gateway pode não ler credenciais/sessões.

Corrigir: garantir que a dir estado + espaço de trabalho são propriedade do usuário executando o gateway.

## Footgun: migrando entre modos remotos/locais

- Se o seu UI (WebUI/TUI) apontar para um gateway **remote**, o host remoto possui a loja de sessão + espaço de trabalho.
- Migrar seu laptop não moverá o estado do gateway remoto.

Se você estiver em modo remoto, migrar o host **gateway**.

Footgun: segredos em backups

<<CODE0> contém segredos (chaves API, fichas OAuth, credenciais WhatsApp). Tratar backups como segredos de produção:

- armazenar encriptado
- evitar a partilha de canais inseguros
- Rode as teclas se suspeitar de exposição

# # Lista de verificação

Na nova máquina, confirme:

- <<CODE0> mostra o gateway em execução
- Seus canais ainda estão conectados (por exemplo, WhatsApp não requer re-par)
- O painel abre e mostra sessões existentes
- Seus arquivos de espaço de trabalho (memória, configurações) estão presentes

# # Relacionado

- [Doctor] (<<<LINK0>>>)
- [Solução de problemas de Gateway] (<<< HTML1>>>>)
- [Onde é que o OpenClaw armazena os seus dados?] (<<<LINK2>>)
