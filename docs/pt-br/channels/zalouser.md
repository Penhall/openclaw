---
summary: "Zalo personal account support via zca-cli (QR login), capabilities, and configuration"
read_when:
  - Setting up Zalo Personal for OpenClaw
  - Debugging Zalo Personal login or message flow
---

# Zalo Personal (não oficial)

Situação: experimental. Esta integração automatiza uma conta **pessoal Zalo** via`zca-cli`.

> **Aviso: ** Esta é uma integração não oficial e pode resultar em suspensão da conta / proibição. Use por sua própria conta e risco.

## Plugin necessário

Zalo Personal ships como um plugin e não é empacotado com a instalação do núcleo.

- Instalar via CLI:`openclaw plugins install @openclaw/zalouser`- Ou de uma saída de origem:`openclaw plugins install ./extensions/zalouser`- Detalhes: [Plugins]/plugin

## Pré-requisito: zca-cli

A máquina Gateway deve ter o binário`zca`disponível em`PATH`.

- Verificar:`zca --version`- Se faltar, instale o zca-cli (ver`extensions/zalouser/README.md`ou os documentos zca-cli a montante).

## Montagem rápida (início)

1. Instale o plugin (veja acima).
2. Login (QR, na máquina Gateway):
-`openclaw channels login --channel zalouser`- Analise o código QR no terminal com a aplicação móvel Zalo.
3. Habilite o canal:

```json5
{
  channels: {
    zalouser: {
      enabled: true,
      dmPolicy: "pairing",
    },
  },
}
```

4. Reinicie o Gateway (ou termine a bordo).
5. O acesso do DM defaults ao emparelhamento; aprova o código do emparelhamento no primeiro contato.

## O que é

- Utiliza`zca listen`para receber mensagens de entrada.
- Utiliza`zca msg ...`para enviar respostas (texto/media/link).
- Projetado para "conta pessoal" casos de uso onde Zalo Bot API não está disponível.

## Nomeação

Canal id é`zalouser`para torná-lo explícito isso automatiza uma ** conta pessoal do usuário Zalo** (não oficial). Mantemos`zalo`reservado para uma futura integração oficial da API Zalo.

## Encontrar IDs (diretório)

Use o diretório CLI para descobrir pares/grupos e seus IDs:

```bash
openclaw directory self --channel zalouser
openclaw directory peers list --channel zalouser --query "name"
openclaw directory groups list --channel zalouser --query "work"
```

## Limites

- O texto de saída é dividido em ~2000 caracteres (limites do cliente Zalo).
- O fluxo está bloqueado por defeito.

## Controle de acesso (DMs)

`channels.zalouser.dmPolicy`apoia:`pairing | allowlist | open | disabled`(padrão:`pairing`.`channels.zalouser.allowFrom`aceita IDs de usuário ou nomes. O assistente resolve nomes para IDs via`zca friend find`quando disponível.

Aprovar através de:

-`openclaw pairing list zalouser`-`openclaw pairing approve zalouser <code>`

## Acesso em grupo (opcional)

- Predefinição:`channels.zalouser.groupPolicy = "open"`(grupos permitidos). Use`channels.defaults.groupPolicy`para substituir o padrão quando desativado.
- Restrinja-se a uma lista com:
-`channels.zalouser.groupPolicy = "allowlist"`-`channels.zalouser.groups`(chaves são identidades de grupo ou nomes)
- Bloqueie todos os grupos:`channels.zalouser.groupPolicy = "disabled"`.
- O assistente de configuração pode solicitar listas de allowlists de grupo.
- Na inicialização, o OpenClaw resolve nomes de grupos/usuários em listas de permissões para IDs e registra o mapeamento; entradas não resolvidas são mantidas como digitadas.

Exemplo:

```json5
{
  channels: {
    zalouser: {
      groupPolicy: "allowlist",
      groups: {
        "123456789": { allow: true },
        "Work Chat": { allow: true },
      },
    },
  },
}
```

## Multi-conta

As contas mapeiam para perfis zca. Exemplo:

```json5
{
  channels: {
    zalouser: {
      enabled: true,
      defaultAccount: "default",
      accounts: {
        work: { enabled: true, profile: "work" },
      },
    },
  },
}
```

## Resolução de problemas

**`zca`não encontrado:**

- Instalar zca-cli e garantir que está no`PATH`para o processo Gateway.

**Login não cola:**

-`openclaw channels status --probe`- Re-login:`openclaw channels logout --channel zalouser && openclaw channels login --channel zalouser`
