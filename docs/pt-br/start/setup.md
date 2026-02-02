---
summary: "Setup guide: keep your OpenClaw setup tailored while staying up-to-date"
read_when:
  - Setting up a new machine
  - You want “latest + greatest” without breaking your personal setup
---

Configuração

Última actualização: 2026-01-01

# # TL;DR

- **Tailoring vive fora do repo:** <<CODE0>> (espaço de trabalho) + <<CODE1> (configuração).
- ** Fluxo de trabalho estável:** instale o aplicativo macOS; deixe-o executar o Gateway empacotado.
- **Bleeding edge workflow:** execute você mesmo o Gateway via <<CODE2>, em seguida, deixe o aplicativo macOS anexar no modo Local.

# # Prereqs (da fonte)

- Nó < < HTML0>>>
- <<CODE1>>
- Acoplamento (opcional; apenas para configuração/e2e em contentores — ver [Acoplamento](<<LINK0>>>))

# # # Estratégia de alfaiataria (assim as atualizações não doem)

Se você quer “100% adaptado a mim”  e  atualizações fáceis, mantenha sua personalização em:

- **Config:** <<CODE0>> (JSON/JSON5-ish)
- ** Espaço de trabalho:** <<CODE1>> (competências, alertas, memórias; torná-lo um repo privado)

Bootstrap uma vez:

```bash
openclaw setup
```

De dentro deste repo, use a entrada CLI local:

```bash
openclaw setup
```

Se você ainda não tem uma instalação global, execute-a via <<CODE0>>.

# # Fluxo de trabalho estável (macOS app first)

1. Instalar + lançamento ** OpenClaw.app** (barra do menu).
2. Complete a lista de verificação de onboarding/permissions (promoções TCC).
3. Certifique-se Gateway é ** Local** e executando (o aplicativo gerencia).
4. Superfícies de ligação (exemplo: WhatsApp):

```bash
openclaw channels login
```

5. Verificação de sanidade:

```bash
openclaw health
```

Se onboarding não estiver disponível em sua compilação:

- Executar <<CODE0>, em seguida, <<CODE1>>, em seguida, iniciar o Gateway manualmente (<<CODE2>>).

# # Fluxo de trabalho de borda de sangramento (Gateway em um terminal)

Objetivo: trabalhar no TypeScript Gateway, obter recarga quente, manter o aplicativo macOS UI anexado.

# # # 0) (Opcional) Execute o aplicativo macOS da fonte também

Se você também quiser o aplicativo macOS na borda sangrando:

```bash
./scripts/restart-mac.sh
```

# # # 1) Iniciar o Dev Gateway

```bash
pnpm install
pnpm gateway:watch
```

<<CODE0> executa o gateway no modo watch e recarrega em mudanças TypeScript.

# # # 2) Aponte o aplicativo macOS em seu Gateway em execução

Em ** OpenClaw.app**:

- Modo de conexão: **Local**
A aplicação irá anexar ao gateway em execução na porta configurada.

# # # 3) Verificar

- No aplicativo O status do gateway deve ler **“Usando gateway existente ...” **
- Ou via CLI:

```bash
openclaw health
```

Armas comuns

- ** Porta errada:** Gateway WS defaults to <<CODE0>>; keep app + CLI on the mesma porta.
- ** Onde vive o estado:**
- Credenciais: <<CODE1>>
- Sessões: <<CODE2>>
- Registos: <<CODE3>>

# # Mapa de armazenamento credencial

Use isto ao depurar a autenticação ou decidir o que fazer backup:

- ** WhatsApp**: <<CODE0>>
- **Telegram bot token**: config/env ou <<CODE1>
- **Discord bot token**: config/env (arquivo de porta ainda não suportado)
- ** Tokens de folga**: config/env (<<CODE2>>)
- ** Listas de autorizações de embalagem**: <<CODE3>>
- **Modelo de perfis de autenticação**: <<CODE4>>
- ** Importação de OAuth legado**: <<CODE5>>
Mais detalhes: [Segurança] (<<<LINK0>>>).

# # Atualizando (sem destruir sua configuração)

- Mantenha <<CODE0>> e <<CODE1>> como “suas coisas”; não coloque prompts/config pessoais no <<CODE2>>repo.
- Fonte de actualização: <<CODE3>> + <<CODE4>> (quando o lockfile mudou) + continue usando <<CODE5>>>.

# # Linux (serviço de usuário sistematizado)

As instalações Linux usam um serviço systemd ** user**. Por padrão, systemd stops user
serviços em logout/idle, que mata o Gateway. Tentativas de integração para habilitar
Permaneça para você (pode pedir sudo). Se ainda estiver desligado, corra:

```bash
sudo loginctl enable-linger $USER
```

Para servidores sempre ligados ou multi-usuários, considere um serviço **system** em vez de um
serviço de usuário (sem necessidade de demora). Veja [Runbook Gateway](<<<LINK0>>>) para as notas systemd.

# # Docs relacionados

- [O livro de instruções do portal] (<<<LINK0>>>) (bancos, supervisão, portos)
- [Configuração do portal] (<<<LINK1>>>) (esquema de configuração + exemplos)
- [Discórdia] (<<<LINK2>>) e [Telegrama] (<<LINK3>>>) (reply tags + replicaToMode settings)
- [Configuração do assistente OpenClaw] (<<<LINK4>>)
- [aplicativo macOS] (<<<LINK5>>) (ciclo de vida no portal)
