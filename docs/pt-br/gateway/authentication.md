---
summary: "Model authentication: OAuth, API keys, and setup-token"
read_when:
  - Debugging model auth or OAuth expiry
  - Documenting authentication or credential storage
---

Autenticação

OpenClaw suporta chaves OAuth e API para provedores de modelos. Para o Antrópico
contas, recomendamos usar uma chave **API **. Para acesso à assinatura de Claude,
utilizar o símbolo de longa duração criado pelo`claude setup-token`.

Ver [/conceitos/outh]/concepts/oauth para o fluxo e armazenamento de OAuth
Disposição.

## Configuração antrópica recomendada (chave API)

Se você estiver usando o Anthropic diretamente, use uma chave API.

1. Crie uma chave API na Consola Antrópica.
2. Coloque-o no host **gateway** (a máquina que executa`openclaw gateway`.

```bash
export ANTHROPIC_API_KEY="..."
openclaw models status
```

3. Se o Gateway é executado sob systemd/lançamento, prefira colocar a chave em`~/.openclaw/.env`para que o daemon possa lê-lo:

```bash
cat >> ~/.openclaw/.env <<'EOF'
ANTHROPIC_API_KEY=...
EOF
```

Em seguida, reinicie o daemon (ou reinicie seu processo Gateway) e verifique novamente:

```bash
openclaw models status
openclaw doctor
```

Se você preferir não gerenciar env vars você mesmo, o assistente de onboarding pode armazenar
Chaves de API para uso do servidor:`openclaw onboard`.

Ver [Ajuda]/help para mais pormenores sobre a herança env `env.shellEnv`,`~/.openclaw/.env`, sistemad/lançado).

## Antrópico: configuração-token (autorização de inscrição)

Para Anthropic, o caminho recomendado é uma chave ** API. Se você estiver usando um Claude
assinatura, o fluxo de configuração-token também é suportado. Execute- o no host ** gateway**:

```bash
claude setup-token
```

Em seguida, cole-o em OpenClaw:

```bash
openclaw models auth setup-token --provider anthropic
```

Se o token foi criado em outra máquina, cole-o manualmente:

```bash
openclaw models auth paste-token --provider anthropic
```

Se vir um erro Antrópico como:

```
This credential is only authorized for use with Claude Code and cannot be used for other API requests.
```

...usar uma chave de API antrópica.

Entrada de token manual (qualquer provedor; escreve`auth-profiles.json`+ configuração de atualizações):

```bash
openclaw models auth paste-token --provider anthropic
openclaw models auth paste-token --provider openrouter
```

Verificação amigável à automação (saída`1`quando expirada/falta,`2`quando expirada):

```bash
openclaw models status --check
```

Os scripts ops ops ops (systemd/Termux) estão documentados aqui:
[/automatização/monitoramento automático] /automation/auth-monitoring

>`claude setup-token`requer um TTY interativo.

## Verificando o estado de autenticação do modelo

```bash
openclaw models status
openclaw doctor
```

## Controlando qual credencial é usado

## # Por sessão (comando chat)

Use`/model <alias-or-id>@<profileId>`para fixar uma credencial de provedor específico para a sessão atual (ids de perfil exemplo:`anthropic:default`,`anthropic:work`.

Use`/model`(ou`/model list` para um seletor compacto; use`/model status`para a visão completa (candidatas + próximo perfil de autenticação, além de detalhes do terminal do provedor quando configurado).

## Per-agente (substituir CLI)

Define um sobreposição explícita da ordem do perfil de autenticação para um agente (armazenado no`auth-profiles.json`desse agente):

```bash
openclaw models auth order get --provider anthropic
openclaw models auth order set --provider anthropic anthropic:default
openclaw models auth order clear --provider anthropic
```

Use`--agent <id>`para direcionar um agente específico; omiti-lo para usar o agente padrão configurado.

## Resolução de problemas

## # Não foram encontradas credenciais

Se o perfil do símbolo Antrópico estiver ausente, execute`claude setup-token`no
** máquina de gateway**, então verifique novamente:

```bash
openclaw models status
```

Token expirando/expirando

Execute`openclaw models status`para confirmar qual perfil está expirando. Se o perfil
está faltando, repetir`claude setup-token`e colar o token novamente.

## Requisitos

- assinatura Claude Max ou Pro (para`claude setup-token`
- Claude Code CLI instalado (comando`claude`disponível)
