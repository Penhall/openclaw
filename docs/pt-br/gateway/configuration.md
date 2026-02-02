---
summary: "All configuration options for ~/.openclaw/openclaw.json with examples"
read_when:
  - Adding or modifying config fields
---

Configuração

OpenClaw lê uma configuração opcional **JSON5** de <<CODE0>> (comentários + vírgulas de rastreamento permitidos).

Se o arquivo estiver faltando, o OpenClaw usa padrões seguros (embedded Pi agent + por-sender sessions + workspace <<CODE0>>). Você geralmente só precisa de uma configuração para:

- restringir quem pode desencadear o bot (<<<CODE0>>, <<CODE1>>>>, etc.)
- grupo de controlo allowlists + comportamento de menção (<<<CODE2>>, <<CODE3>>>, <<CODE4>>, <<CODE5>>)
- personalizar prefixos de mensagens (<<<CODE6>>)
- definir o espaço de trabalho do agente (<<<CODE7>>> ou <<CODE8>>>>>)
- ajustar os padrões do agente incorporado (<<<CODE9>>>) e o comportamento da sessão (<<CODE10>>>)
- definir a identidade por agente (<<<CODE11>>>)

> **Novo para a configuração?** Confira o guia [Exemplos de configuração](<<<LINK0>>>) para exemplos completos com explicações detalhadas!

# # Validação estrita da configuração

O OpenClaw só aceita configurações que correspondem totalmente ao esquema.
Chaves desconhecidas, tipos malformados ou valores inválidos fazem com que o Gateway se recuse a iniciar** por segurança.

Quando a validação falhar:

- O Gateway não arranca.
- São permitidos apenas comandos de diagnóstico (por exemplo: <<CODE0>>, <<CODE1>>, <<CODE2>>, <<CODE3>>, <<CODE4>>, <<CODE5>>).
- Executar <<CODE6> para ver os problemas exatos.
- Executar <<CODE7>> (ou <<CODE8>>>) para aplicar migrações/reparações.

O médico nunca escreve alterações a menos que você opte explicitamente por <<CODE0>>/<<CODE1>>>.

# # Esquema + dicas de UI

O Gateway expõe uma representação do esquema JSON da configuração via <<CODE0>> para editores de UI.
O Control UI renderiza um formulário deste esquema, com um editor **Raw JSON** como escotilha de escape.

Plugins de canal e extensões podem registrar esquema + dicas de UI para sua configuração, então configurações de canal
Mantenha o esquema orientado através de aplicativos sem formulários codificados.

Dicas (selos, agrupamento, campos sensíveis) enviam ao lado do esquema para que os clientes possam renderizar
melhores formas sem conhecimento de configuração de codificação.

# # Aplicar + reiniciar (RPC)

Use <<CODE0>> para validar + escreva a configuração completa e reinicie o Gateway em um passo.
Ele escreve um sentinela reiniciar e pings a última sessão ativa após o Gateway voltar.

Aviso: <<CODE0>> substitui a **configuração inteira**. Se você quiser mudar apenas algumas chaves,
utilizar <<CODE1>> ou <<CODE2>>>. Mantenha um backup de <<CODE3>>>>.

Parâmetros:

- <<CODE0> (string) — carga útil JSON5 para toda a configuração
- <<CODE1> (opcional) — hash de configuração de <<CODE2> (obrigatório quando já existe uma configuração)
- <<CODE3> (opcional) — última tecla de sessão activa para o ping de despertar
- <<CODE4> (opcional) — nota a incluir no sentinela de reiniciar
- <<CODE5> (opcional) — atraso antes de reiniciar (padrão 2000)

Exemplo (via <<CODE0>>>):

```bash
openclaw gateway call config.get --params '{}' # capture payload.hash
openclaw gateway call config.apply --params '{
  "raw": "{\\n  agents: { defaults: { workspace: \\"~/.openclaw/workspace\\" } }\\n}\\n",
  "baseHash": "<hash-from-config.get>",
  "sessionKey": "agent:main:whatsapp:dm:+15555550123",
  "restartDelayMs": 1000
}'
```

# # Atualizações parciais (RPC)

Use <<CODE0> para mesclar uma atualização parcial na configuração existente sem bater
Chaves não relacionadas. Aplica a semântica do patch de mesclagem JSON:

- os objetos se fundem recursivamente
- <<CODE0> apaga uma chave
- arrays substituir
Como <<CODE1>, ele valida, escreve a configuração, armazena uma sentinela reinicial e agenda
o Gateway reiniciar (com um wake opcional quando <<CODE2>> é fornecido).

Parâmetros:

- <<CODE0> (string) — JSON5 carga útil contendo apenas as chaves para mudar
- <<CODE1> (necessário) — hash de configuração de <<CODE2>
- <<CODE3> (opcional) — última tecla de sessão activa para o ping de despertar
- <<CODE4> (opcional) — nota a incluir no sentinela de reiniciar
- <<CODE5> (opcional) — atraso antes de reiniciar (padrão 2000)

Exemplo:

```bash
openclaw gateway call config.get --params '{}' # capture payload.hash
openclaw gateway call config.patch --params '{
  "raw": "{\\n  channels: { telegram: { groups: { \\"*\\": { requireMention: false } } } }\\n}\\n",
  "baseHash": "<hash-from-config.get>",
  "sessionKey": "agent:main:whatsapp:dm:+15555550123",
  "restartDelayMs": 1000
}'
```

## Configuração mínima (ponto de partida recomendado)

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

Compila a imagem padrão uma vez com:

```bash
scripts/sandbox-setup.sh
```

# # Modo de auto-conversa (recomendado para controle de grupo)

Para evitar que o bot responda ao WhatsApp @-menções em grupos (apenas responda a gatilhos de texto específicos):

```json5
{
  agents: {
    defaults: { workspace: "~/.openclaw/workspace" },
    list: [
      {
        id: "main",
        groupChat: { mentionPatterns: ["@openclaw", "reisponde"] },
      },
    ],
  },
  channels: {
    whatsapp: {
      // Allowlist is DMs only; including your own number enables self-chat mode.
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
}
```

Inclui (<<CODE0>>>)

Divida sua configuração em vários arquivos usando a diretiva <<CODE0>>. Isto é útil para:

- Organizar configs grandes (por exemplo, definições de agente por cliente)
- Compartilhando configurações comuns em ambientes
- Manter as configurações sensíveis separadas

Uso básico

```json5
// ~/.openclaw/openclaw.json
{
  gateway: { port: 18789 },

  // Include a single file (replaces the key's value)
  agents: { $include: "./agents.json5" },

  // Include multiple files (deep-merged in order)
  broadcast: {
    $include: ["./clients/mueller.json5", "./clients/schmidt.json5"],
  },
}
```

```json5
// ~/.openclaw/agents.json5
{
  defaults: { sandbox: { mode: "all", scope: "session" } },
  list: [{ id: "main", workspace: "~/.openclaw/workspace" }],
}
```

# # # Mesclar o comportamento

- **Ficheiro único**: Substitui o objeto contendo <<CODE0>>>
- ** Array de arquivos**: Deep-merges arquivos em ordem (mais tarde os arquivos sobrepõem os anteriores)
- ** Com chaves de irmãos**: Chaves de irmãos são mescladas após as inclusões (substituir valores incluídos)
- **Sibling keys + arrays/primitivos**: Não suportado (o conteúdo incluído deve ser um objeto)

```json5
// Sibling keys override included values
{
  $include: "./base.json5", // { a: 1, b: 2 }
  b: 99, // Result: { a: 1, b: 99 }
}
```

# # # Aninhado inclui

Os arquivos incluídos podem conter diretivas <<CODE0>> (até 10 níveis de profundidade):

```json5
// clients/mueller.json5
{
  agents: { $include: "./mueller/agents.json5" },
  broadcast: { $include: "./mueller/broadcast.json5" },
}
```

## # Resolução do caminho

- ** Caminhos relativos**: Resolvido em relação ao arquivo including
- ** Caminhos absolutos**: Usado como está
- ** Pastas parentais**: <<CODE0>> referências funcionam como esperado

```json5
{ "$include": "./sub/config.json5" }      // relative
{ "$include": "/etc/openclaw/base.json5" } // absolute
{ "$include": "../shared/common.json5" }   // parent dir
```

# # # Tratamento de erros

- **Ficheiro desaparecido**: Limpar o erro com o caminho resolvido
- ** Erro de processamento**: Mostra qual arquivo incluído falhou
- ** O círculo inclui **: Detectado e reportado com cadeia de inclusão

### Exemplo: Configuração legal multicliente

```json5
// ~/.openclaw/openclaw.json
{
  gateway: { port: 18789, auth: { token: "secret" } },

  // Common agent defaults
  agents: {
    defaults: {
      sandbox: { mode: "all", scope: "session" },
    },
    // Merge agent lists from all clients
    list: { $include: ["./clients/mueller/agents.json5", "./clients/schmidt/agents.json5"] },
  },

  // Merge broadcast configs
  broadcast: {
    $include: ["./clients/mueller/broadcast.json5", "./clients/schmidt/broadcast.json5"],
  },

  channels: { whatsapp: { groupPolicy: "allowlist" } },
}
```

```json5
// ~/.openclaw/clients/mueller/agents.json5
[
  { id: "mueller-transcribe", workspace: "~/clients/mueller/transcribe" },
  { id: "mueller-docs", workspace: "~/clients/mueller/docs" },
]
```

```json5
// ~/.openclaw/clients/mueller/broadcast.json5
{
  "120363403215116621@g.us": ["mueller-transcribe", "mueller-docs"],
}
```

# # Opções comuns

## # Env vars + <<CODE0>>

OpenClaw lê env vars do processo pai (shell, launchd/systemd, CI, etc.).

Além disso, carrega:

- <<CODE0>> da pasta de trabalho actual (se presente)
- um recuo global <<CODE1>> de <<CODE2>> (também conhecido por <<CODE3>>)

Nenhum arquivo <<CODE0> > substitui env vars existentes.

Você também pode fornecer env vars em linha na configuração. Estes só são aplicados se
processo env está faltando a chave (mesma regra não-superando):

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: {
      GROQ_API_KEY: "gsk-...",
    },
  },
}
```

Ver [/ambiente](<<<LINK0>>>) para precedência total e fontes.

## # <<CODE0>> (opcional)

Comodidade Opt-in: se habilitado e nenhuma das chaves esperadas ainda estiverem definidas, o OpenClaw executa sua shell de login e importa apenas as chaves que faltam (nunca sobrepõe).
Isso efetivamente fornece seu perfil de shell.

```json5
{
  env: {
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}
```

Env var equivalente:

- <<CODE0>>
- <<CODE1>>

## # Substituição do Env var na configuração

Você pode referenciar variáveis de ambiente diretamente em qualquer valor de string de configuração usando
<<CODE0>> sintaxe. Variáveis são substituídas no tempo de carga de configuração, antes da validação.

```json5
{
  models: {
    providers: {
      "vercel-gateway": {
        apiKey: "${VERCEL_GATEWAY_API_KEY}",
      },
    },
  },
  gateway: {
    auth: {
      token: "${OPENCLAW_GATEWAY_TOKEN}",
    },
  },
}
```

** Regras:**

- Apenas os nomes do env var maiúsculo correspondem: <<CODE0>>
- Faltando ou vazio env vars lançar um erro na carga de configuração
- Escapar com <<CODE1>> para produzir um literal <<CODE2>>
- Funciona com <<CODE3>> (os ficheiros incluídos também recebem substituição)

** Substituição em linha: **

```json5
{
  models: {
    providers: {
      custom: {
        baseUrl: "${CUSTOM_API_BASE}/v1", // → "https://api.example.com/v1"
      },
    },
  },
}
```

### Armazenamento de autenticação (chaves OAuth + API)

OpenClaw armazena **per-agent** perfis de autenticação (chaves OAuth + API) em:

- <<CODE0>> (padrão: <<CODE1>>)

Ver também: [/conceitos/outh](<<<LINK0>>>)

Importações de OAuth legado:

- <<CODE0> (ou <<CODE1>>)

O agente Pi incorporado mantém uma cache em tempo de execução em:

- <<CODE0>> (administrado automaticamente; não edite manualmente)

Dir Agente Legado (pré- multi- agente):

- <<CODE0> (migrado por <<CODE1>> para <<CODE2>)

Substituição:

- OAuth dir (apenas importação de legado): <<CODE0>>
- Dir agente (substituição da raiz do agente padrão): <<CODE1>> (preferido), <<CODE2>> (legacia)

Na primeira utilização, o OpenClaw importa <<CODE0> entradas em <<CODE1>>.

## # <<CODE0>>

Metadados opcionais para perfis de autenticação. Isto não ** armazena segredos; ele mapeia
IDs de perfil para um modo provedor + (e e-mail opcional) e define o provedor
ordem de rotação utilizada para failover.

```json5
{
  auth: {
    profiles: {
      "anthropic:me@example.com": { provider: "anthropic", mode: "oauth", email: "me@example.com" },
      "anthropic:work": { provider: "anthropic", mode: "api_key" },
    },
    order: {
      anthropic: ["anthropic:me@example.com", "anthropic:work"],
    },
  },
}
```

## # <<CODE0>>

Identidade opcional por agente usada para padrões e UX. Isto é escrito pelo assistente do macOS.

Se definido, OpenClaw deriva padrões (somente quando você não os definiu explicitamente):

- <<CODE0> do ** agente activo** <<CODE1>>> (cai de volta para o "")
- <<CODE2>> do agente <<CODE3>/<HTML4>>> (por isso “@Samantha” funciona em grupos através do Telegram/Slack/Discord/Google Chat/iMessage/WhatsApp)
- <<CODE5> aceita um caminho de imagem relacionado ao espaço de trabalho ou um URL/dados remotos. Os arquivos locais devem viver dentro da área de trabalho do agente.

<<CODE0> aceita:

- Caminho relativo ao espaço de trabalho (deve permanecer dentro do espaço de trabalho do agente)
- <<CODE0>> URL
- <<CODE1>> URI

```json5
{
  agents: {
    list: [
      {
        id: "main",
        identity: {
          name: "Samantha",
          theme: "helpful sloth",
          emoji: "🦥",
          avatar: "avatars/samantha.png",
        },
      },
    ],
  },
}
```

## # <<CODE0>>

Metadados escritos por assistentes de CLI (<<<CODE0>>, <<CODE1>>, <<CODE2>>).

```json5
{
  wizard: {
    lastRunAt: "2026-01-01T00:00:00.000Z",
    lastRunVersion: "2026.1.4",
    lastRunCommit: "abc1234",
    lastRunCommand: "configure",
    lastRunMode: "local",
  },
}
```

## # <<CODE0>>

- Ficheiro de registo por omissão: <<CODE0>>
- Se quiser um caminho estável, defina <<CODE1>> para <<CODE2>>>.
- Saída do console pode ser sintonizado separadamente através de:
- <<CODE3> (defaults to <<CODE4>>, colisões para <<CODE5>> quando <<CODE6>)
- < <<CODE7>> (<<CODE8>>>
- Resumos de ferramentas podem ser redigidos para evitar vazamento de segredos:
- <<CODE11> (<<CODE12>>> <<CODE13>>, por omissão: <<CODE14>>)
- <<CODE15>> (array de strings regex; substitui os padrões)

```json5
{
  logging: {
    level: "info",
    file: "/tmp/openclaw/openclaw.log",
    consoleLevel: "info",
    consoleStyle: "pretty",
    redactSensitive: "tools",
    redactPatterns: [
      // Example: override defaults with your own rules.
      "\\bTOKEN\\b\\s*[=:]\\s*([\"']?)([^\\s\"']+)\\1",
      "/\\bsk-[A-Za-z0-9_-]{8,}\\b/gi",
    ],
  },
}
```

## # <<CODE0>>

Controla como as conversas diretas do WhatsApp (DMs) são tratadas:

- <<CODE0> (padrão): remetentes desconhecidos recebem um código de pareamento; o proprietário deve aprovar
- <<CODE1>: apenas permite aos remetentes <<CODE2> (ou armazenamento de licenças emparelhado)
- <<CODE3>>: permitir que todos os DMs de entrada (**requer** <<CODE4>>> incluam <<CODE5>>)
- <<CODE6>>: ignorar todos os DM de entrada

Os códigos de pareamento expiram após 1 hora; o bot só envia um código de pareamento quando uma nova solicitação é criada. As requisições de emparelhamento de DM pendentes são **3 por canal** por padrão.

Aprovações emparelhadas:

- <<CODE0>>
- <<CODE1>>

## # <<CODE0>>

Allowlist de números de telefone E.164 que podem desencadear respostas automáticas do WhatsApp (**DMs apenas**).
Se vazio e <<CODE0>>, os remetentes desconhecidos receberão um código de pareamento.
Para grupos, utilizar <<CODE1>>+<HTML2>>>>>.

```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "pairing", // pairing | allowlist | open | disabled
      allowFrom: ["+15555550123", "+447700900123"],
      textChunkLimit: 4000, // optional outbound chunk size (chars)
      chunkMode: "length", // optional chunking mode (length | newline)
      mediaMaxMb: 50, // optional inbound media cap (MB)
    },
  },
}
```

## # <<CODE0>>

Controla se as mensagens do WhatsApp estão marcadas como lidas (marcações azuis). Padrão: <<CODE0>>>.

O modo de auto-conversa sempre ignora os recibos de leitura, mesmo quando ativado.

Substituição por conta: <<CODE0>>>>.

```json5
{
  channels: {
    whatsapp: { sendReadReceipts: false },
  },
}
```

## # <<CODE0> (multi-conta)

Execute várias contas do WhatsApp em um gateway:

```json5
{
  channels: {
    whatsapp: {
      accounts: {
        default: {}, // optional; keeps the default id stable
        personal: {},
        biz: {
          // Optional override. Default: ~/.openclaw/credentials/whatsapp/biz
          // authDir: "~/.openclaw/credentials/whatsapp/biz",
        },
      },
    },
  },
}
```

Notas:

- Comandos de saída padrão para conta <<CODE0>> se presente; caso contrário, o primeiro id de conta configurado (sortado).
- A conta única legado Baileys dir é migrada por <<CODE1>> para <<CODE2>>.

### <<CODE0>> / <<CODE1>>/ <<CODE2>>/ <<CODE3>>/ <<CODE4>/ <HTML5>>>/ <HTML6>>>

Executar várias contas por canal (cada conta tem sua própria <<CODE0>> e opcional <<CODE1>>>):

```json5
{
  channels: {
    telegram: {
      accounts: {
        default: {
          name: "Primary bot",
          botToken: "123456:ABC...",
        },
        alerts: {
          name: "Alerts bot",
          botToken: "987654:XYZ...",
        },
      },
    },
  },
}
```

Notas:

- <<CODE0>> é utilizado quando <<CODE1>> é omitido (CLI + roteamento).
- Tokens Env só se aplicam à conta **default**.
- Configurações de canal base (política de grupo, mencionando gating, etc.) aplicam-se a todas as contas, a menos que seja anulada por conta.
- Utilizar <<CODE2>> para encaminhar cada conta para um agente diferente. por omissão.

### Lista de bate-papo mencionam gating (<<<CODE0>> + <<CODE1>>)

Agrupar mensagens padrão para **requer menção** (quer mencione metadados ou padrões de regex). Aplica-se às conversas de grupo WhatsApp, Telegram, Discord, Google Chat e iMessage.

** Tipos de menção:**

- ** Menções de metadados**: plataforma nativa @-menções (por exemplo, WhatsApp tap-to-mention). Ignorado no modo de auto-conversa do WhatsApp (ver <<CODE0>>).
- **Padrões de texto**: Padrões Regex definidos em <<CODE1>>. Sempre verificado independentemente do modo de self-chat.
- Mencionar gating só é aplicado quando a detecção de menção é possível (menções nativas ou pelo menos um <<CODE2>>>).

```json5
{
  messages: {
    groupChat: { historyLimit: 50 },
  },
  agents: {
    list: [{ id: "main", groupChat: { mentionPatterns: ["@openclaw", "openclaw"] } }],
  },
}
```

<<CODE0> define o padrão global para o contexto do histórico do grupo. Os canais podem substituir com <<CODE1>> (ou <<CODE2>> para multi-conta). Definir <<CODE3>> para desativar o envolvimento do histórico.

Limites da história do DM

As conversas com DM usam o histórico baseado em sessão gerenciado pelo agente. Você pode limitar o número de turnos de usuário retidos por sessão de DM:

```json5
{
  channels: {
    telegram: {
      dmHistoryLimit: 30, // limit DM sessions to 30 user turns
      dms: {
        "123456789": { historyLimit: 50 }, // per-user override (user ID)
      },
    },
  },
}
```

Ordem de resolução:

1. Substituição por DM: <<CODE0>>
2. Predefinição do provedor: <<CODE1>>
3. Nenhum limite (toda a história retida)

Prestadores suportados: <<CODE0>>, <<CODE1>, <<CODE2>>, <<CODE3>, <<CODE4>>, <<CODE5>>, <<CODE6>>.

Substituição por agente (precede quando definido, mesmo <<CODE0>>>):

```json5
{
  agents: {
    list: [
      { id: "work", groupChat: { mentionPatterns: ["@workbot", "\\+15555550123"] } },
      { id: "personal", groupChat: { mentionPatterns: ["@homebot", "\\+15555550999"] } },
    ],
  },
}
```

Mencionar gating defaults live per canal (<<<CODE0>>, <<CODE1>>, <<CODE2>>, <<CODE3>>). Quando <<CODE4> é definido, ele também atua como uma lista de allowlist de grupo; incluem <<CODE5>> para permitir todos os grupos.

Para responder **apenas** a gatilhos de texto específicos (ignorando @-menções nativas):

```json5
{
  channels: {
    whatsapp: {
      // Include your own number to enable self-chat mode (ignore native @-mentions).
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
  agents: {
    list: [
      {
        id: "main",
        groupChat: {
          // Only these text patterns will trigger responses
          mentionPatterns: ["reisponde", "@openclaw"],
        },
      },
    ],
  },
}
```

## # Política de grupo (por canal)

Utilizar <<CODE0>> para controlar se as mensagens de grupo/quarto são aceites:

```json5
{
  channels: {
    whatsapp: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
    },
    telegram: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["tg:123456789", "@alice"],
    },
    signal: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
    },
    imessage: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["chat_id:123"],
    },
    msteams: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["user@org.com"],
    },
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        GUILD_ID: {
          channels: { help: { allow: true } },
        },
      },
    },
    slack: {
      groupPolicy: "allowlist",
      channels: { "#general": { allow: true } },
    },
  },
}
```

Notas:

- <<CODE0>>: grupos wift allowlists; ainda se aplica o mention-gating.
- <<CODE1>>: bloquear todas as mensagens de grupo/quarto.
- <<CODE2>>: só permite grupos/quartos que correspondam à lista de permissões configurada.
- <<CODE3> define o padrão quando o <<CODE4> de um provedor está desligado.
- WhatsApp/Telegram/Signal/iMessage/Microsoft Teams use <<CODE5>> (fallback: explícito <<CODE6>>).
- Discord/Slack use canal allowlists (<<<CODE7>>, <<CODE8>>>).
- Os DM do grupo (Discord/Slack) ainda são controlados por <<CODE9>> + <<CODE10>>.
- O padrão é <<CODE11>> (a menos que substituído por <<CODE12>>>>); se nenhuma allowlist estiver configurada, as mensagens de grupo são bloqueadas.

## Roteamento multiagentes (<<<CODE0>> + <<CODE1>>)

Execute vários agentes isolados (espaço de trabalho separado, <<CODE0>>, sessões) dentro de um Gateway.
As mensagens de entrada são encaminhadas para um agente através de ligações.

- <<CODE0>>: substituições por agente.
- <<CODE1>>: agente estável id (obrigatório).
- <<CODE2>>: opcional; quando múltiplos são definidos, as primeiras vitórias e um aviso é registrado.
Se nenhum estiver definido, o **primeiro item** na lista é o agente padrão.
- <<CODE3>>: nome do agente.
- <<CODE4>>: padrão <<CODE5>> (para <<CODE6>>, cai para <<CODE7>>).
- <<CODE8>>: padrão <<CODE9>>>.
- <<CODE10>>: modelo padrão por agente, substitui <<CODE11>> por esse agente.
- forma de texto: <<CODE12>>, substitui apenas <<CODE13>
- forma do objeto: <<CODE14>> (fallbacks overlain <<CODE15>>>; <<CODE16>> desactiva os fallbacks globais para esse agente)
- <<CODE17>>: nome do agente/tema/emoji (utilizado para padrões de menção + reações de ack).
- <<CODE18>>: por agente com indicação (<<CODE19>>>).
- <<CODE20>>: configuração da caixa de areia por agente (overrides <<CODE21>>).
- < <<CODE22>>: <<CODE23>>>
- <<CODE26>>: <<CODE27>>> <<CODE28>> <<CODE29>
- < <<CODE30>>: <<CODE31>>>
- <<CODE34>>: raiz de espaço de trabalho personalizada da caixa de areia
- <<CODE35>>: substituições por docker por agente (por exemplo, <<CODE36>>, <<CODE37>>, <<CODE38>>, <<CODE39>>, limites; ignorados quando <<CODE40>>)
- <<CODE41>>: substituições do navegador sandbox por agente (ignorado quando <<CODE42>>)
- <<CODE43>>: substituições por poda por agente da caixa de areia (ignorado quando <<CODE44>>)
- <<CODE45>>: padrões por sub- agente.
- <<CODE46>>: lista de ids de agente para <<CODE47>>> deste agente (<<CODE48>> = permitir qualquer; padrão: apenas mesmo agente)
- <<CODE49>>>: restrições de ferramentas por agente (aplicadas antes da política de ferramentas sandbox).
- <<CODE50>>: perfil da ferramenta base (aplicado antes de permitir/negar)
- <<CODE51>>: array de nomes de ferramentas permitidos
- <<CODE52>>: array de nomes de ferramentas negados (deny ganha)
- <<CODE53>>: padrão do agente compartilhado (modelo, espaço de trabalho, sandbox, etc.).
- <<CODE54>>: encaminha as mensagens de entrada para uma <<CODE55>>.
- <<CODE56> (obrigatório)
- <<CODE57>> (opcional; <<CODE58>> = qualquer conta; omitido = conta padrão)
- <<CODE59>> (opcional; <<CODE60>>)
- <<CODE61>/ <<CODE62>> (opcional; específico do canal)

Ordem de correspondência determinística:

1. <<CODE0>>
2. <<CODE1>>
3. <<CODE2>>
4. <<CODE3>> (exato, sem pares/pedreira/equipe)
5. <<CODE4>> (em todo o canal, sem pares/pedreira/equipe)
6. agente por omissão (<<<CODE5>>, caso contrário primeiro item da lista, caso contrário <<CODE6>>>)

Dentro de cada nível de jogo, a primeira entrada correspondente em <<CODE0> ganha.

### # Per-agente perfis de acesso (multi-agente)

Cada agente pode levar sua própria política sandbox + ferramenta. Usar isto para misturar o acesso
níveis num portal:

- ** Acesso completo** (agente pessoal)
- **Somente leitura** ferramentas + espaço de trabalho
- ** Nenhum acesso ao sistema de ficheiros** (apenas ferramentas de envio/sessão)

Ver [Multi-Agent Sandbox & Tools] (<<<LINK0>>>) para precedência e
exemplos adicionais.

Acesso completo (sem caixa de areia):

```json5
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: { mode: "off" },
      },
    ],
  },
}
```

Ferramentas somente para leitura + espaço de trabalho somente para leitura:

```json5
{
  agents: {
    list: [
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: {
          mode: "all",
          scope: "agent",
          workspaceAccess: "ro",
        },
        tools: {
          allow: [
            "read",
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
          ],
          deny: ["write", "edit", "apply_patch", "exec", "process", "browser"],
        },
      },
    ],
  },
}
```

Sem acesso ao sistema de arquivos (ferramentas de mensagens/sessões habilitadas):

```json5
{
  agents: {
    list: [
      {
        id: "public",
        workspace: "~/.openclaw/workspace-public",
        sandbox: {
          mode: "all",
          scope: "agent",
          workspaceAccess: "none",
        },
        tools: {
          allow: [
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
            "whatsapp",
            "telegram",
            "slack",
            "discord",
            "gateway",
          ],
          deny: [
            "read",
            "write",
            "edit",
            "apply_patch",
            "exec",
            "process",
            "browser",
            "canvas",
            "nodes",
            "cron",
            "gateway",
            "image",
          ],
        },
      },
    ],
  },
}
```

Exemplo: duas contas do WhatsApp → dois agentes:

```json5
{
  agents: {
    list: [
      { id: "home", default: true, workspace: "~/.openclaw/workspace-home" },
      { id: "work", workspace: "~/.openclaw/workspace-work" },
    ],
  },
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],
  channels: {
    whatsapp: {
      accounts: {
        personal: {},
        biz: {},
      },
    },
  },
}
```

## # <<CODE0>> (opcional)

As mensagens agente- agente são opt- in:

```json5
{
  tools: {
    agentToAgent: {
      enabled: false,
      allow: ["home", "work"],
    },
  },
}
```

## # <<CODE0>>

Controla como as mensagens de entrada se comportam quando um agente executado já está ativo.

```json5
{
  messages: {
    queue: {
      mode: "collect", // steer | followup | collect | steer-backlog (steer+backlog ok) | interrupt (queue=steer legacy)
      debounceMs: 1000,
      cap: 20,
      drop: "summarize", // old | new | summarize
      byChannel: {
        whatsapp: "collect",
        telegram: "collect",
        discord: "collect",
        imessage: "collect",
        webchat: "collect",
      },
    },
  },
}
```

## # <<CODE0>>

Denuncie mensagens de entrada rápidas do mesmo remetente** então multiple back-to-back
as mensagens tornam-se um único agente. Debouncing é escopo por canal + conversa
e usa a mensagem mais recente para resposta threading/IDs.

```json5
{
  messages: {
    inbound: {
      debounceMs: 2000, // 0 disables
      byChannel: {
        whatsapp: 5000,
        slack: 1500,
        discord: 1500,
      },
    },
  },
}
```

Notas:

- Denuncie lotes ** somente texto** mensagens; mídia/attachments flush imediatamente.
- Comandos de controle (por exemplo, <<CODE0>>, <<CODE1>>>>) desbocagem de bypass para que eles permaneçam autônomos.

#### <<CODE0>> (comando de bate-papo)

Controla como os comandos de chat são ativados entre conectores.

```json5
{
  commands: {
    native: "auto", // register native commands when supported (auto)
    text: true, // parse slash commands in chat messages
    bash: false, // allow ! (alias: /bash) (host-only; requires tools.elevated allowlists)
    bashForegroundMs: 2000, // bash foreground window (0 backgrounds immediately)
    config: false, // allow /config (writes to disk)
    debug: false, // allow /debug (runtime-only overrides)
    restart: false, // allow /restart + gateway restart tool
    useAccessGroups: true, // enforce access-group allowlists/policies for commands
  },
}
```

Notas:

- Os comandos de texto devem ser enviados como uma mensagem ** standalone** e usar os principais <<CODE0>> (sem plain-text aliases).
- <<CODE1> desactiva a análise de mensagens de chat para comandos.
- <<CODE2> (padrão) ativa comandos nativos para Discord/Telegram e deixa Slack desligado; canais não suportados permanecem somente texto.
- Definir <<CODE3>> para forçar todos, ou substituir por canal com <<CODE4>>>, <<CODE5>>, <<CODE6> (bool ou <<CODE7>>>). <<CODE8>> limpa comandos previamente registrados em Discord/Telegram na inicialização; os comandos Slack são gerenciados no aplicativo Slack.
- <<CODE9> adiciona entradas extras do menu de bots do Telegram. Os nomes são normalizados; os conflitos com comandos nativos são ignorados.
- <<CODE10>> permite <<CODE11>> executar comandos de shell do host (<<CODE12>> também funciona como um apelido). Requer <<CODE13>> e permite listar o remetente em <<CODE14>>.
- <<CODE15> > controla o tempo que o bash espera antes da formação. Enquanto um trabalho bash está em execução, novas solicitações <<CODE16>> são rejeitadas (uma de cada vez).
- <<CODE17> permite <<CODE18>> (leituras/escritas <<CODE19>>).
- <<CODE20>> as mutações de configuração de portas iniciadas por esse canal (padrão: true). Isto aplica-se a <<CODE21> mais auto-migrações específicas do provedor (alterações no ID do supergrupo do telegrama, alterações no ID do canal Slack).
- <<CODE22> activa <<CODE23>> (somente substituições de tempo de execução).
- <<CODE24> habilita <<CODE25>> e a ferramenta de gateway reinicia a ação.
- <<CODE26> permite que os comandos bypass access-group allowlists/policies.
- Comandos e diretrizes Slash só são honrados para ** remetentes autorizados**. A autorização é derivada de
Listas de autorizações/pares de canais mais <<CODE27>>.

## # <<CODE0>> (Hora de execução do canal Web WhatsApp)

WhatsApp é executado através do canal web do gateway (Baileys Web). Ele começa automaticamente quando existe uma sessão vinculada.
Definir <<CODE0>> para mantê-lo desligado por padrão.

```json5
{
  web: {
    enabled: true,
    heartbeatSeconds: 60,
    reconnect: {
      initialMs: 2000,
      maxMs: 120000,
      factor: 1.4,
      jitter: 0.2,
      maxAttempts: 0,
    },
  },
}
```

## # <<CODE0>> (transporte do robô)

OpenClaw inicia o Telegram somente quando existe uma seção de configuração <<CODE0>. O token bot é resolvido a partir de <<CODE1>> (ou <<CODE2>>>), com <<CODE3>>> como um retorno para a conta padrão.
Definir <<CODE4>> para desativar a inicialização automática.
O suporte multi-conta vive em <<CODE5>> (ver a seção multi-conta acima). Os tokens de Env só se aplicam à conta padrão.
Definir <<CODE6>> para bloquear a configuração iniciada pelo Telegram escreve (incluindo migrações de ID de supergrupo e <<CODE7>>>).

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "your-bot-token",
      dmPolicy: "pairing", // pairing | allowlist | open | disabled
      allowFrom: ["tg:123456789"], // optional; "open" requires ["*"]
      groups: {
        "*": { requireMention: true },
        "-1001234567890": {
          allowFrom: ["@admin"],
          systemPrompt: "Keep answers brief.",
          topics: {
            "99": {
              requireMention: false,
              skills: ["search"],
              systemPrompt: "Stay on topic.",
            },
          },
        },
      },
      customCommands: [
        { command: "backup", description: "Git backup" },
        { command: "generate", description: "Create an image" },
      ],
      historyLimit: 50, // include last N group messages as context (0 disables)
      replyToMode: "first", // off | first | all
      linkPreview: true, // toggle outbound link previews
      streamMode: "partial", // off | partial | block (draft streaming; separate from block streaming)
      draftChunk: {
        // optional; only for streamMode=block
        minChars: 200,
        maxChars: 800,
        breakPreference: "paragraph", // paragraph | newline | sentence
      },
      actions: { reactions: true, sendMessage: true }, // tool action gates (false disables)
      reactionNotifications: "own", // off | own | all
      mediaMaxMb: 5,
      retry: {
        // outbound retry policy
        attempts: 3,
        minDelayMs: 400,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
      network: {
        // transport overrides
        autoSelectFamily: false,
      },
      proxy: "socks5://localhost:9050",
      webhookUrl: "https://example.com/telegram-webhook",
      webhookSecret: "secret",
      webhookPath: "/telegram-webhook",
    },
  },
}
```

Rascunho de notas de streaming:

- Usa Telegram <<CODE0>> (bolha de desenho, não uma mensagem real).
- Requer ** tópicos de chat privados** (mensage thread id em DMs; bot tem tópicos ativados).
- <<CODE1> streams raciocinando no rascunho, então envia a resposta final.
Os padrões e comportamentos da política de repetição estão documentados em [Política de repetição] (<<<LINK0>>).

## # <<CODE0>> (transporte do robô)

Configure o bot Discord definindo o token do bot e o gating opcional:
O suporte multi-conta vive em <<CODE0>> (ver a seção multi-conta acima). Os tokens de Env só se aplicam à conta padrão.

```json5
{
  channels: {
    discord: {
      enabled: true,
      token: "your-bot-token",
      mediaMaxMb: 8, // clamp inbound media size
      allowBots: false, // allow bot-authored messages
      actions: {
        // tool action gates (false disables)
        reactions: true,
        stickers: true,
        polls: true,
        permissions: true,
        messages: true,
        threads: true,
        pins: true,
        search: true,
        memberInfo: true,
        roleInfo: true,
        roles: false,
        channelInfo: true,
        voiceStatus: true,
        events: true,
        moderation: false,
      },
      replyToMode: "off", // off | first | all
      dm: {
        enabled: true, // disable all DMs when false
        policy: "pairing", // pairing | allowlist | open | disabled
        allowFrom: ["1234567890", "steipete"], // optional DM allowlist ("open" requires ["*"])
        groupEnabled: false, // enable group DMs
        groupChannels: ["openclaw-dm"], // optional group DM allowlist
      },
      guilds: {
        "123456789012345678": {
          // guild id (preferred) or slug
          slug: "friends-of-openclaw",
          requireMention: false, // per-guild default
          reactionNotifications: "own", // off | own | all | allowlist
          users: ["987654321098765432"], // optional per-guild user allowlist
          channels: {
            general: { allow: true },
            help: {
              allow: true,
              requireMention: true,
              users: ["987654321098765432"],
              skills: ["docs"],
              systemPrompt: "Short answers only.",
            },
          },
        },
      },
      historyLimit: 20, // include last N guild messages as context
      textChunkLimit: 2000, // optional outbound text chunk size (chars)
      chunkMode: "length", // optional chunking mode (length | newline)
      maxLinesPerMessage: 17, // soft max lines per message (Discord UI clipping)
      retry: {
        // outbound retry policy
        attempts: 3,
        minDelayMs: 500,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
  },
}
```

OpenClaw inicia Discórdia somente quando existe uma seção de configuração <<CODE0>. O símbolo é resolvido a partir de <<CODE1>>, com <<CODE2>> como um recurso para a conta padrão (a menos que <<CODE3>> é <<CODE4>>>). Usar <<CODE5>> (DM) ou <<CODE6> (canal guild) ao especificar os alvos de entrega para comandos cron/CLI; IDs numéricos nus são ambíguos e rejeitados.
As lesmas são minúsculas, com espaços substituídos por <<CODE7>>>; as teclas de canal usam o nome do canal (sem levar <<CODE8>>>). Preferir IDs de guild como chaves para evitar renomear ambiguidade.
As mensagens de autor de bots são ignoradas por padrão. Activar com <<CODE9>> (as mensagens próprias ainda são filtradas para evitar loops de auto-resposta).
Modos de notificação de reacção:

- <<CODE0>: não existem reacções.
- <<CODE1>>: reações nas mensagens do próprio bot (padrão).
- <<CODE2>>: todas as reacções em todas as mensagens.
- <<CODE3>>: reacções de <<CODE4>> em todas as mensagens (a lista vazia desactiva).
O texto de saída é cortado por <<CODE5>> (padrão 2000). Definir <<CODE6>> para dividir em linhas em branco (limites de parágrafo) antes de blocos de comprimento. Os clientes de discórdia podem cortar mensagens muito altas, então <<CODE7>> (padrão 17) divide respostas longas de várias linhas mesmo quando abaixo de 2000 caracteres.
Os padrões e comportamentos da política de repetição estão documentados em [Política de repetição] (<<<LINK0>>).

## # <<CODE0>> (Chat API webhook)

O Google Chat executa webhooks HTTP com autenticação de nível de aplicativo (conta de serviço).
O suporte multi-conta vive em <<CODE0>> (ver a seção multi-conta acima). O Env vars só se aplica à conta por omissão.

```json5
{
  channels: {
    googlechat: {
      enabled: true,
      serviceAccountFile: "/path/to/service-account.json",
      audienceType: "app-url", // app-url | project-number
      audience: "https://gateway.example.com/googlechat",
      webhookPath: "/googlechat",
      botUser: "users/1234567890", // optional; improves mention detection
      dm: {
        enabled: true,
        policy: "pairing", // pairing | allowlist | open | disabled
        allowFrom: ["users/1234567890"], // optional; "open" requires ["*"]
      },
      groupPolicy: "allowlist",
      groups: {
        "spaces/AAAA": { allow: true, requireMention: true },
      },
      actions: { reactions: true },
      typingIndicator: "message",
      mediaMaxMb: 20,
    },
  },
}
```

Notas:

- Conta de serviço JSON pode ser em linha (<<<CODE0>>) ou baseada em arquivos (<<CODE1>>>).
- Retalhos do En para a conta padrão: <<CODE2>>> ou <<CODE3>>>>.
- <<CODE4>> + <<CODE5> deve corresponder à configuração de autenticação da aplicação Chat.
- Utilizar <<CODE6>> ou <<CODE7>> ao definir os alvos de entrega.

## # <<CODE0>> (modo soquete)

O Slack é executado no modo Socket e requer um token de bot e um token de app:

```json5
{
  channels: {
    slack: {
      enabled: true,
      botToken: "xoxb-...",
      appToken: "xapp-...",
      dm: {
        enabled: true,
        policy: "pairing", // pairing | allowlist | open | disabled
        allowFrom: ["U123", "U456", "*"], // optional; "open" requires ["*"]
        groupEnabled: false,
        groupChannels: ["G123"],
      },
      channels: {
        C123: { allow: true, requireMention: true, allowBots: false },
        "#general": {
          allow: true,
          requireMention: true,
          allowBots: false,
          users: ["U123"],
          skills: ["docs"],
          systemPrompt: "Short answers only.",
        },
      },
      historyLimit: 50, // include last N channel/group messages as context (0 disables)
      allowBots: false,
      reactionNotifications: "own", // off | own | all | allowlist
      reactionAllowlist: ["U123"],
      replyToMode: "off", // off | first | all
      thread: {
        historyScope: "thread", // thread | channel
        inheritParent: false,
      },
      actions: {
        reactions: true,
        messages: true,
        pins: true,
        memberInfo: true,
        emojiList: true,
      },
      slashCommand: {
        enabled: true,
        name: "openclaw",
        sessionPrefix: "slack:slash",
        ephemeral: true,
      },
      textChunkLimit: 4000,
      chunkMode: "length",
      mediaMaxMb: 20,
    },
  },
}
```

O suporte multi-conta vive em <<CODE0>> (ver a seção multi-conta acima). Os tokens de Env só se aplicam à conta padrão.

OpenClaw inicia Slack quando o provedor está habilitado e ambos os tokens são definidos (via config ou <<CODE0>> + <<CODE1>>). Utilizar <<CODE2>> (DM) ou <<CODE3>> ao especificar os alvos de entrega para comandos cron/CLI.
Definir <<CODE4>> para bloquear a configuração iniciada pelo Slack escreve (incluindo migrações do canal ID e <<CODE5>>).

As mensagens de autor de bots são ignoradas por padrão. Activar com <<CODE0>> ou <<CODE1>>>>.

Modos de notificação de reacção:

- <<CODE0>: não existem reacções.
- <<CODE1>>: reações nas mensagens do próprio bot (padrão).
- <<CODE2>>: todas as reacções em todas as mensagens.
- <<CODE3>>: reacções de <<CODE4>> em todas as mensagens (a lista vazia desactiva).

Isolamento da sessão de thread:

- <<CODE0> controla se o histórico de threads é por thread (<<CODE1>>, padrão) ou compartilhado através do canal (<<CODE2>>).
- <<CODE3> controla se novas sessões de thread herdam a transcrição do canal pai (padrão: false).

Grupos de ação Slack (gate <<CODE0> ações da ferramenta):
O grupo de ação O padrão
--- --- --- --- --- ---
Reações ativadas Reagir + listar reações
As mensagens estão activadas
• pinos activados • Pin/unpin/list
MembroInfo activado Informação do membro
EmojiList ativado emoji

# ## # <<CODE0> (botão)

Mattermost ships como um plugin e não é empacotado com a instalação do núcleo.
Instale-o primeiro: <<CODE0>> (ou <<CODE1>> de um git checkout).

Mattermost requer um token bot mais a URL base para o seu servidor:

```json5
{
  channels: {
    mattermost: {
      enabled: true,
      botToken: "mm-token",
      baseUrl: "https://chat.example.com",
      dmPolicy: "pairing",
      chatmode: "oncall", // oncall | onmessage | onchar
      oncharPrefixes: [">", "!"],
      textChunkLimit: 4000,
      chunkMode: "length",
    },
  },
}
```

O OpenClaw inicia Mattermost quando a conta está configurada (token bot + URL base) e habilitada. O símbolo + URL base é resolvido a partir de <<CODE0>> + <<CODE1>> ou <<CODE2>> + <<CODE3>> para a conta por omissão (a não ser <<CODE4>>> é <<CODE5>>>).

Modos de conversa:

- <<CODE0>> (por omissão): responder às mensagens do canal apenas quando @ mencionado.
- <<CODE1>>: responder a cada mensagem de canal.
- <<CODE2>>: responder quando uma mensagem começa com um prefixo de gatilho (<<CODE3>>, padrão <<CODE4>>).

Controlo de acesso:

- DM padrão: <<CODE0>> (os remetentes desconhecidos recebem um código de pareamento).
- DM públicos: <<CODE1>>> mais <<CODE2>>>>>.
- Grupos: <<CODE3>> por padrão (perioditado). Use <<CODE4>> para restringir os remetentes.

O suporte multi-conta vive em <<CODE0>> (ver a seção multi-conta acima). O Env vars só se aplica à conta por omissão.
Utilizar <<CODE1>> ou <<CODE2>> (ou <<CODE3>>>) ao especificar os alvos de entrega; os IDs desnudos são tratados como IDs de canal.

## # <<CODE0> (sinal-cli)

Reações de sinal podem emitir eventos do sistema (ferramenta de reação compartilhada):

```json5
{
  channels: {
    signal: {
      reactionNotifications: "own", // off | own | all | allowlist
      reactionAllowlist: ["+15551234567", "uuid:123e4567-e89b-12d3-a456-426614174000"],
      historyLimit: 50, // include last N group messages as context (0 disables)
    },
  },
}
```

Modos de notificação de reacção:

- <<CODE0>: não existem reacções.
- <<CODE1>>: reações nas mensagens do próprio bot (padrão).
- <<CODE2>>: todas as reacções em todas as mensagens.
- <<CODE3>>: reacções de <<CODE4>> em todas as mensagens (a lista vazia desactiva).

## # <<CODE0>> (imsg CLI)

OpenClaw gera <<CODE0>> (JSON-RPC sobre stdio). Nenhum servidor ou porto necessário.

```json5
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "imsg",
      dbPath: "~/Library/Messages/chat.db",
      remoteHost: "user@gateway-host", // SCP for remote attachments when using SSH wrapper
      dmPolicy: "pairing", // pairing | allowlist | open | disabled
      allowFrom: ["+15555550123", "user@example.com", "chat_id:123"],
      historyLimit: 50, // include last N group messages as context (0 disables)
      includeAttachments: false,
      mediaMaxMb: 16,
      service: "auto",
      region: "US",
    },
  },
}
```

O suporte multi-conta vive em <<CODE0>> (ver a seção multi-conta acima).

Notas:

- Requer acesso completo ao disco às mensagens DB.
- O primeiro envio irá pedir permissão de automação de mensagens.
- Preferir alvos <<CODE0>>. Use <<CODE1>> para listar chats.
- <<CODE2> pode apontar para um script wrapper (por exemplo <<CODE3>> para outro Mac que executa <<CODE4>>); use as chaves SSH para evitar prompts de senha.
- Para wrappers SSH remotos, definir <<CODE5> para obter anexos via SCP quando <<CODE6> estiver habilitado.

Embalagem de exemplo:

```bash
#!/usr/bin/env bash
exec ssh -T gateway-host imsg "$@"
```

## # <<CODE0>>

Define o diretório **single global workspace** usado pelo agente para operações de arquivos.

Padrão: <<CODE0>>>.

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}
```

Se <<CODE0>> estiver habilitada, sessões não principais podem sobrepor-se a isso
espaço de trabalho próprio por escopo em <<CODE1>>>.

## # <<CODE0>>

Root opcional do repositório para mostrar na linha Runtime do sistema. Se desactivado, OpenClaw
tenta detectar um diretório <<CODE0>> andando para cima a partir do espaço de trabalho (e atual
directório de trabalho). O caminho deve existir para ser usado.

```json5
{
  agents: { defaults: { repoRoot: "~/Projects/openclaw" } },
}
```

## # <<CODE0>>

Desativa a criação automática dos arquivos de inicialização do espaço de trabalho (<<<CODE0>>, <<CODE1>>, <<CODE2>>, <<CODE3>>, <<CODE4>>>, e <<CODE5>>>).

Use isso para implantações pré-semeadas onde seus arquivos de espaço de trabalho vêm de um repositório.

```json5
{
  agents: { defaults: { skipBootstrap: true } },
}
```

## # <<CODE0>>

Max caracteres de cada espaço de trabalho bootstrap arquivo injetado no prompt do sistema
antes da truncagem. Padrão: <<CODE0>>>.

Quando um arquivo excede este limite, o OpenClaw registra um aviso e injeta um truncado
cabeça/cauda com um marcador.

```json5
{
  agents: { defaults: { bootstrapMaxChars: 20000 } },
}
```

## # <<CODE0>>

Define o fuso horário do usuário para ** contexto de prompt do sistema** (não para datas em
envelopes de mensagens). Se não estiver definido, o OpenClaw usa o fuso- horário da máquina em tempo de execução.

```json5
{
  agents: { defaults: { userTimezone: "America/Chicago" } },
}
```

## # <<CODE0>>

Controla o formato ** time** mostrado na seção Data e Hora atual do sistema.
Padrão: <<CODE0>>> (Preferência OS).

```json5
{
  agents: { defaults: { timeFormat: "auto" } }, // auto | 12 | 24
}
```

## # <<CODE0>>

Controla prefixos de entrada/saída e reações opcionais.
Veja [Mensagens](<<<LINK0>>) para filas, sessões e contexto de streaming.

```json5
{
  messages: {
    responsePrefix: "🦞", // or "auto"
    ackReaction: "👀",
    ackReactionScope: "group-mentions",
    removeAckAfterReply: false,
  },
}
```

<<CODE0>> é aplicado a **todas as respostas de saída** (sínteses da ferramenta, bloco
transmissão, respostas finais) através de canais, a menos que já presentes.

Se <<CODE0> estiver desmarcado, nenhum prefixo é aplicado por padrão. WhatsApp self-chat
respostas são a exceção: eles default to <<CODE1> quando definido, caso contrário
<<CODE2>>, então as conversas do mesmo telefone permanecem legíveis.
Defina-o para <<CODE3> para derivar <<CODE4>> para o agente roteado (quando definido).

Variáveis de modelo

A string <<CODE0> pode incluir variáveis de modelo que resolvem dinamicamente:

* Variável * Descrição * Exemplo *
----------------- --------------------- --------------------- -----------------------------
* <<CODE0>> * Nome do modelo curto * <<CODE1>>, <<CODE2>>
Identificador completo do modelo
Nome do fornecedor
* < <<CODE8>> * Nível de pensamento atual * <<CODE9>>>, <<CODE10>>, <<CODE11>>
(mesmo que <<CODE13>>>

As variáveis são insensíveis ao caso (<<<CODE0>> = <<CODE1>>>). <<CODE2> é um apelido para <<CODE3>>>.
Variáveis não resolvidas permanecem como texto literal.

```json5
{
  messages: {
    responsePrefix: "[{model} | think:{thinkingLevel}]",
  },
}
```

Resultado do exemplo: <<CODE0>>>

O prefixo de entrada do WhatsApp está configurado via <<CODE0>> (revogado:
<<CODE1>>). Estadias padrão **não alteradas**: <<CODE2>> quando
<<CODE3> está vazio, caso contrário <<CODE4>> (sem prefixo). Ao utilizar
<<CODE5>, OpenClaw irá usar <<CODE6>> quando o roteado
o agente tem <<CODE7>> definido.

<<CODE0> envia uma reação emoji de melhor esforço para reconhecer mensagens de entrada
nos canais que suportam reações (Slack/Discord/Telegram/Google Chat). Padrões para o
<<CODE1>> do agente ativo, caso contrário <<CODE2>>. Defina-o para <<CODE3>> para desativar.

Quando as reacções dispararem:

- <<CODE0> (padrão): apenas quando um grupo/quarto requer menções **e** o bot foi mencionado
- <<CODE1>>: todas as mensagens de grupo/quarto
- <<CODE2>>: apenas mensagens directas
- <<CODE3>>: todas as mensagens

<<CODE0> remove a reação do bot após uma resposta ser enviada
(Lack/Discord/Telegram/Google Apenas conversa). Padrão: <<CODE1>>>.

#### <<CODE0>>

Activar texto- para- fala para respostas de saída. Quando ligado, OpenClaw gera áudio
usando o OnzeLabs ou OpenAI e prende-o às respostas. Telegram usa Opus
notas de voz; outros canais enviam áudio MP3.

```json5
{
  messages: {
    tts: {
      auto: "always", // off | always | inbound | tagged
      mode: "final", // final | all (include tool/block replies)
      provider: "elevenlabs",
      summaryModel: "openai/gpt-4.1-mini",
      modelOverrides: {
        enabled: true,
      },
      maxTextLength: 4000,
      timeoutMs: 30000,
      prefsPath: "~/.openclaw/settings/tts.json",
      elevenlabs: {
        apiKey: "elevenlabs_api_key",
        baseUrl: "https://api.elevenlabs.io",
        voiceId: "voice_id",
        modelId: "eleven_multilingual_v2",
        seed: 42,
        applyTextNormalization: "auto",
        languageCode: "en",
        voiceSettings: {
          stability: 0.5,
          similarityBoost: 0.75,
          style: 0.0,
          useSpeakerBoost: true,
          speed: 1.0,
        },
      },
      openai: {
        apiKey: "openai_api_key",
        model: "gpt-4o-mini-tts",
        voice: "alloy",
      },
    },
  },
}
```

Notas:

- <<CODE0>> controla auto- TTS (<<CODE1>>, <<CODE2>>, <<CODE3>>, <<CODE4>>>).
- <<CODE5> define o modo automático por sessão (overrides config).
- <<CODE6> é legado; o médico migra-o para <<CODE7>>.
- <<CODE8> armazena sobreposições locais (fornecedor/limit/summarize).
- <<CODE9>> é uma tampa dura para entrada TTS; os resumos são truncados para caber.
- <<CODE10> substitui <<CODE11> para auto-síntese.
- Aceita <<CODE12>> ou um alias de <<CODE13>>.
- <<CODE14>> permite sobreposições orientadas por modelos como <<CODE15>> tags (on por padrão).
- definições de resumo por utilizador.
- <<CODE18>> os valores diminuem para <<CODE19>>/<HTML20>> e <<CODE21>>.
- <<CODE22> > substitui a URL base da API OnzeLabs.
- <<CODE23>> suporta <<CODE24>/<<CODE25>/<<CODE26> (0,1),
<<CODE27>>, e <<CODE28>> (0,5..2.0).

## # <<CODE0>>

Por omissão para o modo de conversação (macOS/iOS/Android). Os IDs de voz voltam a <<CODE0>> ou <<CODE1>> quando desligados.
<<CODE2> diminui para <<CODE3>> (ou o perfil de shell do gateway) quando desligado.
<<CODE4> deixa que as directivas Talk usem nomes amigáveis (por exemplo, <<CODE5>>>).

```json5
{
  talk: {
    voiceId: "elevenlabs_voice_id",
    voiceAliases: {
      Clawd: "EXAVITQu4vr4xnSDxMaL",
      Roger: "CwhRBWXzGAHq8TQ4Fs17",
    },
    modelId: "eleven_v3",
    outputFormat: "mp3_44100_128",
    apiKey: "elevenlabs_api_key",
    interruptOnSpeech: true,
  },
}
```

## # <<CODE0>>

Controla o tempo de execução do agente incorporado (modelo/pensamento/verbose/timeouts).
<<CODE0> define o catálogo de modelos configurados (e atua como a lista de permissões para <<CODE1>>).
<<CODE2> define o modelo padrão; <<CODE3>> são failovers globais.
<<CODE4> é opcional e é **apenas usado se o modelo primário não tiver entrada de imagem**.
Cada entrada <<CODE5> pode incluir:

- <<CODE0>> (atalho opcional do modelo, por exemplo <<CODE1>>>).
- <<CODE2>> (Os parâmetros API específicos do provedor opcional passaram para o pedido do modelo).

<<CODE0> também é aplicado em execuções de streaming (agente incorporado + compactação). Chaves suportadas hoje: <<CODE1>>>, <<CODE2>>>>. Estes mesclam-se com as opções de tempo de chamada; os valores fornecidos pelo chamador ganham. <<CODE3> é um botão avançado — deixe por definir a menos que você conheça os padrões do modelo e precise de uma mudança.

Exemplo:

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-sonnet-4-5-20250929": {
          params: { temperature: 0.6 },
        },
        "openai/gpt-5.2": {
          params: { maxTokens: 8192 },
        },
      },
    },
  },
}
```

Modelos Z.AI GLM-4.x ativam automaticamente o modo de pensamento a menos que você:

- definido <<CODE0>>, ou
- Defina você mesmo <<CODE1>.

A Openclaw também envia algumas abreviações de nomes falsos. O padrão só se aplica quando o modelo
já está presente em <<CODE0>>>:

- <<CODE0> -> <<CODE1>>
- <<CODE2> -> <<CODE3>>
- <<CODE4> -> <<CODE5>>
- <<CODE6> -> <<CODE7>>
- <<CODE8> -> <<CODE9>>
- <<CODE10> -> <<CODE11>>

Se você configurar o mesmo nome de alias (caso-insensível) você mesmo, seu valor ganha (por padrão nunca sobrepõe).

Exemplo: Opus 4.5 primário com recurso MiniMax M2.1 (hosped MiniMax):

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-5": { alias: "opus" },
        "minimax/MiniMax-M2.1": { alias: "minimax" },
      },
      model: {
        primary: "anthropic/claude-opus-4-5",
        fallbacks: ["minimax/MiniMax-M2.1"],
      },
    },
  },
}
```

MiniMax auth: set <<CODE0> (env) ou configure <<CODE1>>>.

#### <<CODE0>> (regresso CLI)

Infra- estruturas CLI opcionais para execução apenas de texto (sem chamadas de ferramenta). Estes são úteis como
caminho de backup quando os provedores de API falham. A passagem da imagem é suportada quando você configura
um <<CODE0> que aceita caminhos de arquivos.

Notas:

- As infra-estruturas CLI são **text-first**; as ferramentas estão sempre desactivadas.
- As sessões são suportadas quando <<CODE0>> é definido; os IDs de sessão são persistidos por backend.
- Para <<CODE1>>, os padrões são conectados. Sobrescrever o caminho do comando se o PATH for mínimo
(lançado/sistemado).

Exemplo:

```json5
{
  agents: {
    defaults: {
      cliBackends: {
        "claude-cli": {
          command: "/opt/homebrew/bin/claude",
        },
        "my-cli": {
          command: "my-cli",
          args: ["--json"],
          output: "json",
          modelArg: "--model",
          sessionArg: "--session",
          sessionMode: "existing",
          systemPromptArg: "--system",
          systemPromptWhen: "first",
          imageArg: "--image",
          imageMode: "repeat",
        },
      },
    },
  },
}
```

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-5": { alias: "Opus" },
        "anthropic/claude-sonnet-4-1": { alias: "Sonnet" },
        "openrouter/deepseek/deepseek-r1:free": {},
        "zai/glm-4.7": {
          alias: "GLM",
          params: {
            thinking: {
              type: "enabled",
              clear_thinking: false,
            },
          },
        },
      },
      model: {
        primary: "anthropic/claude-opus-4-5",
        fallbacks: [
          "openrouter/deepseek/deepseek-r1:free",
          "openrouter/meta-llama/llama-3.3-70b-instruct:free",
        ],
      },
      imageModel: {
        primary: "openrouter/qwen/qwen-2.5-vl-72b-instruct:free",
        fallbacks: ["openrouter/google/gemini-2.0-flash-vision:free"],
      },
      thinkingDefault: "low",
      verboseDefault: "off",
      elevatedDefault: "on",
      timeoutSeconds: 600,
      mediaMaxMb: 5,
      heartbeat: {
        every: "30m",
        target: "last",
      },
      maxConcurrent: 3,
      subagents: {
        model: "minimax/MiniMax-M2.1",
        maxConcurrent: 1,
        archiveAfterMinutes: 60,
      },
      exec: {
        backgroundMs: 10000,
        timeoutSec: 1800,
        cleanupMs: 1800000,
      },
      contextTokens: 200000,
    },
  },
}
```

#### <<CODE0>> (poda de resultado da ferramenta)

<<CODE0>> ameixas ** resultados antigos da ferramenta** do contexto na memória logo antes de uma solicitação ser enviada para o LLM.
Ele faz **not** modificar o histórico de sessão no disco (<<<CODE1> permanece completo).

Isto pretende reduzir o uso de token para agentes chatty que acumulam grandes saídas de ferramentas ao longo do tempo.

Nível elevado:

- Nunca toque em mensagens de usuário/assistente.
- Protege as últimas mensagens de assistente <<CODE0>> (sem resultados de ferramenta após esse ponto são podados).
- Protege o prefixo bootstrap (nada antes da primeira mensagem do usuário ser podada).
- Modos:
- <<CODE1>>: resultados de ferramentas sobredimensionadas em pontos moles (manter cabeça/cauda) quando o rácio de contexto estimado se cruza <<CODE2>>.
Em seguida, limpa duramente os resultados mais antigos da ferramenta elegível quando a razão de contexto estimada cruza <<CODE3> **e **
há volume suficiente de resultados de ferramentas (<<<CODE4>>>>).
- <<CODE5>>: substitui sempre os resultados da ferramenta elegível antes do ponto de corte com o <<CODE6>> (sem verificação da relação).

Poda suave vs dura (o que muda no contexto enviado para o LLM):

- **Soft-trim**: somente para resultados de  oversized  ferramenta. Mantém o início + fim e insere <<CODE0>> no meio.
- Antes: <<CODE1>>
- Após: <<CODE2>>
- **Hard-clear**: substitui todo o resultado da ferramenta pelo placeholder.
- Antes: <<CODE3>>>
- Após: <<CODE4>>

Notas / limitações atuais:

- Os resultados da ferramenta contendo **blocos de imagem são ignorados** (nunca aparados/limpados) agora.
- A “razão de contexto” estimada é baseada em ** caracteres** (aproximado), não fichas exatas.
- Se a sessão ainda não contém pelo menos <<CODE0>> mensagens de assistente, a poda é ignorada.
- No modo <<CODE1>, <<CODE2>> é ignorado (os resultados da ferramenta elegível são sempre substituídos por <<CODE3>>).

Padrão (adaptativo):

```json5
{
  agents: { defaults: { contextPruning: { mode: "adaptive" } } },
}
```

Para desativar:

```json5
{
  agents: { defaults: { contextPruning: { mode: "off" } } },
}
```

Padrões (quando <<CODE0>> é <<CODE1>> ou <<CODE2>>>):

- <<CODE0>>: <<CODE1>>>
- <<CODE2>>: <<CODE3>> (apenas adaptativa)
- <<CODE4>>: <<CODE5>> (apenas adaptativo)
- <<CODE6>: <<CODE7>> (apenas adaptativa)
- <<CODE8>>: <<CODE9>>> (apenas adaptativo)
- <<CODE10>>: <<CODE11>>

Exemplo (agressivo, mínimo):

```json5
{
  agents: { defaults: { contextPruning: { mode: "aggressive" } } },
}
```

Exemplo (adaptativo sintonizado):

```json5
{
  agents: {
    defaults: {
      contextPruning: {
        mode: "adaptive",
        keepLastAssistants: 3,
        softTrimRatio: 0.3,
        hardClearRatio: 0.5,
        minPrunableToolChars: 50000,
        softTrim: { maxChars: 4000, headChars: 1500, tailChars: 1500 },
        hardClear: { enabled: true, placeholder: "[Old tool result content cleared]" },
        // Optional: restrict pruning to specific tools (deny wins; supports "*" wildcards)
        tools: { deny: ["browser", "canvas"] },
      },
    },
  },
}
```

Ver [/conceitos/sessão-pruning](<<<LINK0>>>) para detalhes do comportamento.

#### <<CODE0>> (reserve a sala de estar + flush de memória)

<<CODE0> selecciona a estratégia de síntese da compactação. Defaults to <<CODE1>>; set <<CODE2>> para permitir a síntese em blocos para histórias muito longas. Ver [/conceitos/compactação] (<<<LINK0>>>).

<<CODE0> impõe um mínimo <<CODE1>>
valor da compactação de Pi (padrão: <<CODE2>>>). Ajuste para <<CODE3>> para desativar o piso.

<<CODE0> executa uma volta agente **silent** antes
auto-compactação, instruindo o modelo a armazenar memórias duráveis no disco (p. ex.
<<CODE1>>). Activa quando a estimativa do token de sessão cruza uma
limiar suave abaixo do limite de compactação.

Por omissão do legado:

- <<CODE0>>: <<CODE1>>>
- <<CODE2>>: <<CODE3>>
- <<CODE4>> / <<CODE5>>: padrões incorporados com <<CODE6>>
- Nota: o flush da memória é ignorado quando a área de trabalho da sessão é somente leitura
(<<<CODE7>> ou <<CODE8>>>>).

Exemplo (ajustado):

```json5
{
  agents: {
    defaults: {
      compaction: {
        mode: "safeguard",
        reserveTokensFloor: 24000,
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 6000,
          systemPrompt: "Session nearing compaction. Store durable memories now.",
          prompt: "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store.",
        },
      },
    },
  },
}
```

Transmissão em bloco:

- <<CODE0>>: <<CODE1>/<<CODE2>> (default off).
- Substituição de canais: <<CODE3>> (e variantes por conta) para forçar a transmissão de blocos ligado/desligado.
Os canais de não-telegrama requerem um explícito <<CODE4>> para permitir respostas em bloco.
- <<CODE5>>: <<CODE6>> ou <<CODE7>>> (padrão: text end).
- <<CODE8>>: soft blocing para blocos em fluxo. Predefinições
800–1200 caracteres, prefere quebras de parágrafo (<<<CODE9>>), em seguida, linhas novas, em seguida, frases.
Exemplo:
  ```json5
  {
    agents: { defaults: { blockStreamingChunk: { minChars: 800, maxChars: 1200 } } },
  }
  ```
- <<CODE0>>: mesclar blocos transmitidos antes de enviar.
Defaults to <<CODE1> e herda <<CODE2>> de <<CODE3>
com <<CODE4> limitado ao limite de texto do canal. Padrão do sinal/slack/discord/Google Chat
a <<CODE5> a menos que seja anulada.
O canal substitui-se: <<CODE6>>, <<CODE7>>,
<<CODE8>>, <<CODE9>>, <<CODE10>>,
<<CODE11>>, <<CODE12>>, <<CODE13>>,
<<CODE14>>
(e variantes por conta).
- <<CODE15>>: pausa aleatória entre ** respostas em bloco** após a primeira.
Modos: <<CODE16>> (padrão), <<CODE17>> (800–2500ms), <<CODE18>> (usar <<CODE19>>/<<CODE20>>).
Substituição por agente: <<CODE21>>>>.
Exemplo:
  ```json5
  {
    agents: { defaults: { humanDelay: { mode: "natural" } } },
  }
  ```
Ver [/conceitos/streaming](<<<LINK0>>>) para comportamento + detalhes de blocos.

Indicadores de tipografia:

- <<CODE0>>: <<CODE1>>>. Predefinições
<<CODE2>> para chats diretos / menções e <<CODE3>> para chats de grupo não mencionados.
- <<CODE4>>: sobreposição por sessão para o modo.
- <<CODE5>>: com que frequência o sinal de digitação é atualizado (padrão: 6s).
- <<CODE6>>: sobreposição por sessão para o intervalo de atualização.
Ver [/conceitos/indicadores de tipagem](<<<LINK0>>>) para detalhes de comportamento.

<<CODE0>> deve ser definido como <<CODE1>>> (por exemplo, <<CODE2>>>).
Os nomes próprios provêm de <<CODE3>> (por exemplo, <<CODE4>>>>).
Se você omitir o provedor, OpenClaw assume atualmente <<CODE5>> como temporário
Retrocesso de depreciação.
Os modelos Z.AI estão disponíveis em <<CODE6>> (por exemplo, <<CODE7>>>) e requerem
<<CODE8>> (ou legado <<CODE9>>>) no ambiente.

<<CODE0> configura batimentos cardíacos periódicos:

- <<CODE0>>: cadeia de duração (<<CODE1>>, <<CODE2>, <<CODE3>>, <<CODE4>>); minutos unitários padrão. Predefinição:
<<CODE5>>. Defina <<CODE6>> para desativar.
- <<CODE7>>: modelo opcional de sobreposição para corridas cardíacas (<<CODE8>>).
- <<CODE9>>: quando <<CODE10>>, os batimentos cardíacos também fornecerão a mensagem separada <<CODE11>>> quando disponível (a mesma forma que <<CODE12>>>>). Padrão: <<CODE13>>>.
- <<CODE14>>: tecla de sessão opcional para controlar em que sessão o batimento cardíaco é executado. Padrão: <<CODE15>>>>.
- <<CODE16>>: sobreposição opcional do destinatário (ID específico do canal, por exemplo, E.164 para WhatsApp, chat id para Telegram).
- <<CODE17>>: canal opcional de entrega (<<CODE18>>, <<CODE19>>, <<CODE20>>, <<CODE21>>, <<CODE22>>, <<CODE23>>, <HTML24>>>, <<CODE25>>, <<CODE26>>>). Padrão: <<CODE27>>>.
- <<CODE28>>: sobreposição opcional para o corpo cardíaco (padrão: <<CODE29>>). As substituições são enviadas na íntegra; incluem um <<CODE30>> linha se você ainda quiser o arquivo lido.
- <<CODE31>>: caracteres máximos permitidos após <<CODE32>> antes da entrega (padrão: 300).

Batimentos cardíacos por agente:

- Definir <<CODE0>> para ativar ou substituir as configurações de batimento cardíaco para um agente específico.
- Se qualquer entrada do agente define <<CODE1>>, ** apenas esses agentes** executar batimentos cardíacos; padrões
tornar-se a base de referência partilhada para esses agentes.

Batimentos cardíacos fazem turnos de agente. Intervalos mais curtos queimam mais fichas; estejam atentos
<<CODE0>>, manter <<CODE1>>> minúsculo e/ou escolher um <<CODE2> mais barato.

<<CODE0> configura padrões de execução de fundo:

- <<CODE0>>: tempo antes do fundo automático (ms, por omissão 10000)
- <<CODE1>>: auto- kill após esta execução (segundos, padrão 1800)
- <<CODE2>>: quanto tempo para manter as sessões terminadas na memória (ms, padrão 1800000)
- <<CODE3>>: enquear um evento do sistema + requisição de batimento cardíaco quando as saídas executivas em segundo plano (verdadeiro padrão)
- <<CODE4>: habilitar experimental <<CODE5>> (OpenAI/OpenAI) Somente o codex; padrão false)
- <<CODE6>>: lista facultativa de ids do modelo (por exemplo, <<CODE7>> ou <<CODE8>>)
Nota: <<CODE9>> é apenas <<CODE10>>>.

<<CODE0>> configura ferramentas de busca + busca na web:

- <<CODE0>> (padrão: true quando a chave está presente)
- <<CODE1>> (recomendado: definido via <<CODE2>>, ou utilizado <<CODE3> env var)
- <<CODE4>> (1–10, padrão 5)
- <<CODE5> (padrão 30)
- <<CODE6> (padrão 15)
- <<CODE7>> (verdadeiro padrão)
- <<CODE8>> (padrão 50000)
- <<CODE9>> (padrão 30)
- <<CODE10> (padrão 15)
- <<CODE11> (sobreposição opcional)
- <<CODE12>> (por omissão true; desactiva para usar apenas a limpeza básica em HTML)
- <<CODE13>> (padrão true quando uma chave API é definida)
- <<CODE14>> (opcional; por omissão <<CODE15>>)
- <<CODE16>> (padrão https://api.firecrawl.dev)
- <<CODE17>> (verdadeiro padrão)
- <<CODE18>> (opcional)
- <<CODE19>> (opcional)

<<CODE0>> configura compreensão de mídia de entrada (imagem/áudio/vídeo):

- <<CODE0>>: lista de modelos partilhada (facultada para a capacidade; utilizada após listas por capítulo).
- <<CODE1>>: máxima capacidade concorrente roda (padrão 2).
- <<CODE2>>/ <<CODE3>>/ <<CODE4>:
- <<CODE5>>: opt-out switch (padrão true quando os modelos são configurados).
- <<CODE6>>: sobreposição de prompt opcional (imagem/vídeo anexar automaticamente uma dica <<CODE7>>).
- <<CODE8>>: caracteres de saída máxima (padrão 500 para imagem/vídeo; não definido para áudio).
- <<CODE9>>: tamanho máximo de mídia para enviar (por omissão: imagem 10MB, áudio 20MB, vídeo 50MB).
- <<CODE10>>: tempo limite de solicitação (padrão: imagem 60s, áudio 60s, vídeo 120s).
- <<CODE11>: dica de áudio opcional.
- <<CODE12>>: política de anexos (<<CODE13>>, <HTML14>>>, <<CODE15>>).
- <<CODE16>>: gating opcional (primeiro jogo ganha) com <<CODE17>>, <<CODE18>>, ou <<CODE19>>.
- <<CODE20>>: lista ordenada de entradas do modelo; falhas ou oversize media voltar para a próxima entrada.
- Cada entrada <<CODE21>>:
- Entrada do fornecedor (<<<CODE22>> ou omitida):
- <<CODE23>>: API provider id (<<CODE24>>, <<CODE25>>, <<CODE26>>/<<CODE27>>, <<CODE28>>, etc).
- <<CODE29>>: sobreposição do modelo id (necessário para imagem; predefinido para <<CODE30>/<<CODE31>> para provedores de áudio, e <<CODE32>>> para vídeo).
- <<CODE33>>/ <<CODE34>>: selecção do perfil de autenticação.
- Entrada CLI (<<<CODE35>>>):
- <<CODE36>>: executável a executar.
- <<CODE37>>: args modelados (suporta <<CODE38>>, <<CODE39>>, <<CODE40>, etc).
- <<CODE41>>: lista opcional (<<CODE42>>, <<CODE43>, <<CODE44>>) para bloquear uma entrada partilhada. Predefinições quando omitido: <<CODE45>/<<CODE46>/<HTML47>>> → imagem, <<CODE48>> → imagem+áudio+vídeo, <<CODE49>> → áudio.
- <<CODE50>>, <<CODE51>>, <<CODE52>>, <<CODE53>>, <<CODE54>> podem ser anulados por entrada.

Se nenhum modelo estiver configurado (ou <<CODE0>>), o entendimento é ignorado; o modelo ainda recebe os anexos originais.

A autenticação do fornecedor segue a ordem de autenticação do modelo padrão (perfis de autenticação, env vars como <<CODE0>>/<<CODE1>>/<<CODE2>>, ou <<CODE3>>>).

Exemplo:

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        maxBytes: 20971520,
        scope: {
          default: "deny",
          rules: [{ action: "allow", match: { chatType: "direct" } }],
        },
        models: [
          { provider: "openai", model: "gpt-4o-mini-transcribe" },
          { type: "cli", command: "whisper", args: ["--model", "base", "{{MediaPath}}"] },
        ],
      },
      video: {
        enabled: true,
        maxBytes: 52428800,
        models: [{ provider: "google", model: "gemini-3-flash-preview" }],
      },
    },
  },
}
```

<<CODE0> configura os padrões do sub- agente:

- <<CODE0>>: modelo padrão para subagentes desovados (string ou <<CODE1>>>). Se omitido, os subagentes herdam o modelo do chamador, a menos que seja anulado por agente ou por chamada.
- <<CODE2>>: máxima execução concorrente de subagentes (padrão 1)
- <<CODE3>>: sessões auto- arquivas de sub- agente após minutos N (padrão 60; definido <<CODE4>> para desactivar)
- Política de ferramentas per-subagent: <<CODE5>> / <<CODE6>> (vence)

<<CODE0> define uma lista de ferramentas de base** antes <<CODE1>>/<<CODE2>>:

- <<CODE0>>: <<CODE1>> apenas
- <<CODE2>>: <<CODE3>>, <<CODE4>>, <<CODE5>>, <<CODE6>>, <<CODE7>>>
- <<CODE8>>: <<CODE9>>, <<CODE10>>, <<CODE11>>, <<CODE12>>, <<CODE13>>>
- <<CODE14>>: nenhuma restrição (mesmo que não definida)

Substituição por agente: <<CODE0>>>>.

Exemplo (somente mensagens por padrão, permitir ferramentas Slack + Discord também):

```json5
{
  tools: {
    profile: "messaging",
    allow: ["slack", "discord"],
  },
}
```

Exemplo (perfil de codificação, mas negar exec/processo em toda parte):

```json5
{
  tools: {
    profile: "coding",
    deny: ["group:runtime"],
  },
}
```

<<CODE0> permite-lhe **mais restringir** ferramentas para provedores específicos (ou um único <<CODE1>>>).
Substituição por agente: <<CODE2>>>>.

Ordem: perfil de base → perfil do provedor → permitir / negar políticas.
As chaves dos fornecedores aceitam quer <<CODE0>> (por exemplo, <<CODE1>>>>) ou <<CODE2>>
(por exemplo, <<CODE3>>>).

Exemplo (mantenha o perfil de codificação global, mas ferramentas mínimas para o Google Antigravity):

```json5
{
  tools: {
    profile: "coding",
    byProvider: {
      "google-antigravity": { profile: "minimal" },
    },
  },
}
```

Exemplo (fornecedor/modelo-específico allowlist):

```json5
{
  tools: {
    allow: ["group:fs", "group:runtime", "sessions_list"],
    byProvider: {
      "openai/gpt-5.2": { allow: ["group:fs", "sessions_list"] },
    },
  },
}
```

<<CODE0>> / <<CODE1>> configure uma política global de allow/deny da ferramenta (vence).
A correspondência é insensível e suporta <<CODE2>> wildcards (<<CODE3>> significa todas as ferramentas).
Isto é aplicado mesmo quando a caixa de areia Docker é **off**.

Exemplo (desativar navegador/canvas em todo lugar):

```json5
{
  tools: { deny: ["browser", "canvas"] },
}
```

Grupos de ferramentas (shorthands) trabalham em **global** e **per-agent** políticas de ferramentas:

- <<CODE0>>: <<CODE1>>, <<CODE2>>, <<CODE3>>
- <<CODE4>>: <<CODE5>>, <<CODE6>>, <<CODE7>>, <<CODE8>
- <<CODE9>>: <<CODE10>>, <<CODE11>>, <<CODE12>>, <<CODE13>>, <<CODE14>>
- <<CODE15>>: <<CODE16>>, <<CODE17>>
- <<CODE18>>: <<CODE19>>, <<CODE20>>
- <<CODE21>>: <<CODE22>>>, <<CODE23>>
- <<CODE24>>: <<CODE25>>>, <<CODE26>>
- <<CODE27>>: <<CODE28>>
- <<CODE29>>: <<CODE30>>
- <<CODE31>>: todas as ferramentas OpenClaw incorporadas (exclui plugins de provedor)

<<CODE0> controla acesso executivo elevado (host):

- <<CODE0>>: permitir o modo elevado (padrão true)
- <<CODE1>>: allowlists por canal (vazio = desativado)
- <<CODE2>>: Números E.164
- <<CODE3>>: IDs de chat ou nomes de utilizador
- <<CODE4>>: IDs de utilizador ou nomes de utilizador (regressa a <<CODE5> se omitido)
- <<CODE6>>: Números E.164
- <<CODE7>>: manipuladores/ids de chat
- <<CODE8>>: IDs de sessão ou nomes de utilizador

Exemplo:

```json5
{
  tools: {
    elevated: {
      enabled: true,
      allowFrom: {
        whatsapp: ["+15555550123"],
        discord: ["steipete", "1234567890123"],
      },
    },
  },
}
```

Substituição por agente (restrição adicional):

```json5
{
  agents: {
    list: [
      {
        id: "family",
        tools: {
          elevated: { enabled: false },
        },
      },
    ],
  },
}
```

Notas:

- <<CODE0> é a linha de base global. <<CODE1> só pode restringir ainda mais (ambos devem permitir).
- <<CODE2> armazena o estado por chave de sessão; as diretivas em linha se aplicam a uma única mensagem.
- Elevado <<CODE3>> roda no hospedeiro e contorna o sandboxing.
- A política da ferramenta ainda se aplica; se <<CODE4> for negada, a elevação não pode ser usada.

<<CODE0> define o número máximo de execuções de agentes incorporados que podem
executar em paralelo através de sessões. Cada sessão ainda é serializada (uma execução
por tecla de sessão de cada vez). Padrão: 1.

## # <<CODE0>>

Opcional ** Docker sandboxing** para o agente incorporado. Destinado ao não principal
sessões para que eles não possam acessar o seu sistema host.

Detalhes: [Sandboxing](<<<LINK0>>)

Predefinição (se activado):

- âmbito: <<CODE0>> (um contentor + espaço de trabalho por agente)
- Debian bookworm-slim based image
- Acesso à área de trabalho do agente: <<CODE1>> (padrão)
- <<CODE2>>: utilizar um espaço de trabalho por câmara de areia em <<CODE3>
- <<CODE4>>: manter o espaço de trabalho da caixa de areia em <<CODE5>, e montar o espaço de trabalho do agente apenas para leitura em <<CODE6> (desactiva <<CODE7>>/<<CODE8>>/<HTML9>>>)
- <<CODE10>>: montar o espaço de trabalho do agente em <<CODE11>
- auto-pruno: inactivo > 24h OU idade > 7d
- política da ferramenta: permitir apenas <<CODE12>>>, <<CODE13>>, <<CODE14>>, <<CODE15>>, <<CODE16>>, <<CODE17>>>, <<CODE18>>, <<CODE19>>, <<CODE20>>, <<CODE21>>, <<CODE22>>> (vence)
- configurar via <<CODE23>>, substituir por agente via <<CODE24>>
- abreviaturas de grupos de ferramentas suportadas na política da sandbox: <<CODE25>>, <<CODE26>>, <<CODE27>>, <<CODE28>> (ver [Sandbox vs Tool Policy vs Elevated](<<LINK0>>>)
- navegador opcional sandboxed (Chromium + CDP, observador noVNC)
- botões de endurecimento: <<CODE29>>, <<CODE30>>, <<CODE31>>, <<CODE32>>, <<CODE33>>, <<CODE34>>, <<CODE35>>, <<CODE36>>

Aviso: <<CODE0>> significa um recipiente compartilhado e espaço de trabalho compartilhado. Não
isolamento transversal. Usar <<CODE1>> para isolamento por sessão.

Legado: <<CODE0>> é ainda suportado (<<CODE1>> → <<CODE2>>,
<<CODE3>> → <<CODE4>>>).

<<CODE0> roda ** uma vez** após a criação do recipiente (dentro do recipiente via <<CODE1>>).
Para instalar pacotes, assegure o egresso de rede, um FS root e um usuário root.

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
          containerPrefix: "openclaw-sbx-",
          workdir: "/workspace",
          readOnlyRoot: true,
          tmpfs: ["/tmp", "/var/tmp", "/run"],
          network: "none",
          user: "1000:1000",
          capDrop: ["ALL"],
          env: { LANG: "C.UTF-8" },
          setupCommand: "apt-get update && apt-get install -y git curl jq",
          // Per-agent override (multi-agent): agents.list[].sandbox.docker.*
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
          binds: ["/var/run/docker.sock:/var/run/docker.sock", "/home/user/source:/source:rw"],
        },
        browser: {
          enabled: false,
          image: "openclaw-sandbox-browser:bookworm-slim",
          containerPrefix: "openclaw-sbx-browser-",
          cdpPort: 9222,
          vncPort: 5900,
          noVncPort: 6080,
          headless: false,
          enableNoVnc: true,
          allowHostControl: false,
          allowedControlUrls: ["http://10.0.0.42:18791"],
          allowedControlHosts: ["browser.lab.local", "10.0.0.42"],
          allowedControlPorts: [18791],
          autoStart: true,
          autoStartTimeoutMs: 12000,
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
          "apply_patch",
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

Compilar a imagem padrão sandbox uma vez com:

```bash
scripts/sandbox-setup.sh
```

Nota: contentores de areia por omissão <<CODE0>>>; conjunto <<CODE1>>
para <<CODE2>> (ou sua rede personalizada) se o agente precisar de acesso de saída.

Nota: os anexos de entrada são encenados para o espaço de trabalho ativo em <<CODE0>>. Com <<CODE1>>, isso significa que os arquivos são escritos na área de trabalho do agente.

Nota: <<CODE0>> monta diretórios de host adicionais; ligações globais e por agente são mescladas.

Compilar a imagem opcional do navegador com:

```bash
scripts/sandbox-browser-setup.sh
```

Quando <<CODE0>>, a ferramenta do navegador usa um sandboxed
Exemplo de crómio (CDP). Se noVNC estiver activo (por omissão quando sem cabeça=false),
a URL noVNC é injetada no prompt do sistema para que o agente possa referenciar.
Isso não requer <<CODE1>> na configuração principal; o controle sandbox
O URL é injetado por sessão.

<<CODE0> (padrão: false) permite
sessões sandboxed para segmentar explicitamente o servidor de controle do navegador ** host**
através da ferramenta navegador (<<<CODE1>>>). Deixa isto fora, se quiseres ser rigoroso.
isolamento da caixa de areia.

Listas de permissões para controle remoto:

- <<CODE0>>: URLs de controlo exacto permitidas para <<CODE1>>.
- <<CODE2>>: são permitidos nomes de máquinas (apenas nome de máquina, nenhuma porta).
- <<CODE3>>: portas permitidas (por omissão: http=80, https=443).
Padrões: todas as listas de permissões estão desativadas (sem restrição). <<CODE4> defaults to false.

## # <<CODE0>> (fornecedores aduaneiros + URLs de base)

OpenClaw usa o catálogo **pi-coding-agent** modelo. Você pode adicionar provedores personalizados
(LiteLLM, servidores compatíveis com OpenAI locais, proxies antrópicos, etc.) escrevendo
<<CODE0>> ou definindo o mesmo esquema dentro do seu
Configuração do OpenClaw em <<CODE1>>>.
Visão geral do provedor por provedor + exemplos: [/conceitos/modelo-fornecedores](<<<LINK0>>>).

Quando <<CODE0> está presente, OpenClaw escreve/merge a <<CODE1>> em
<<CODE2> na inicialização:

- comportamento padrão: ** fusão** (mantém provedores existentes, substitui no nome)
- definir <<CODE0>> para substituir o conteúdo do arquivo

Selecione o modelo via <<CODE0>> (fornecedor/modelo).

```json5
{
  agents: {
    defaults: {
      model: { primary: "custom-proxy/llama-3.1-8b" },
      models: {
        "custom-proxy/llama-3.1-8b": {},
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      "custom-proxy": {
        baseUrl: "http://localhost:4000/v1",
        apiKey: "LITELLM_KEY",
        api: "openai-completions",
        models: [
          {
            id: "llama-3.1-8b",
            name: "Llama 3.1 8B",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 128000,
            maxTokens: 32000,
          },
        ],
      },
    },
  },
}
```

## # OpenCode Zen (proxy multimodelo)

OpenCode Zen é um gateway multimodelo com endpoints por modelo. Usos do Openclaw
o fornecedor incorporado <<CODE0>> do pi-ai; definido <<CODE1>> (ou
<<CODE2>>) de https://opencode.ai/auth.

Notas:

- Modelo de refs use <<CODE0>> (exemplo: <<CODE1>>>).
- Se ativar uma lista de permissões via <<CODE2>>, adicione cada modelo que planeja usar.
- Atalho: <<CODE3>>>.

```json5
{
  agents: {
    defaults: {
      model: { primary: "opencode/claude-opus-4-5" },
      models: { "opencode/claude-opus-4-5": { alias: "Opus" } },
    },
  },
}
```

## # Z.AI (GLM-4.7) — suporte alias do provedor

Os modelos Z.AI estão disponíveis através do fornecedor incorporado <<CODE0>>. Definir <<CODE1>>
no seu ambiente e referenciar o modelo por provedor/modelo.

Atalho: <<CODE0>>>.

```json5
{
  agents: {
    defaults: {
      model: { primary: "zai/glm-4.7" },
      models: { "zai/glm-4.7": {} },
    },
  },
}
```

Notas:

- <<CODE0>> e <<CODE1>> são aceites pseudónimos e normalizam- se para <<CODE2>>>.
- Se faltar <<CODE3>>, os pedidos para <<CODE4>> falharão com um erro de autenticação em tempo de execução.
- Erro de exemplo: <<CODE5>>>
- O objectivo geral da API do Z.AI é <<CODE6>>>>. Código GLM
As solicitações utilizam o endpoint de codificação dedicado <<CODE7>>>.
O fornecedor incorporado <<CODE8>> usa o endpoint de codificação. Se precisar do general
endpoint, defina um provedor personalizado em <<CODE9>> com o URL base
sobreposição (veja a seção de provedores personalizados acima).
- Use um placeholder falso em docs/configs; nunca commit chaves API reais.

AI Moonshot (Kimi)

Utilizar o ponto final compatível com o OpenAI do Moonshot:

```json5
{
  env: { MOONSHOT_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "moonshot/kimi-k2.5" },
      models: { "moonshot/kimi-k2.5": { alias: "Kimi K2.5" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      moonshot: {
        baseUrl: "https://api.moonshot.ai/v1",
        apiKey: "${MOONSHOT_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "kimi-k2.5",
            name: "Kimi K2.5",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 256000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

Notas:

- Definir <<CODE0>> no ambiente ou utilizar <<CODE1>>.
- Modelo ref: <<CODE2>>>>.
- Utilizar <<CODE3>> se necessitar do parâmetro final da China.

Kimi Coding

Usar o endpoint de codificação Kimi da Moonshot AI (fornecedor compatível com antrópicos e integrado):

```json5
{
  env: { KIMI_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "kimi-coding/k2p5" },
      models: { "kimi-coding/k2p5": { alias: "Kimi K2.5" } },
    },
  },
}
```

Notas:

- Definir <<CODE0>> no ambiente ou utilizar <<CODE1>>.
- Modelo ref: <<CODE2>>>>.

Sintético (Antrópico-compatível)

Utilizar o parâmetro de avaliação sintético compatível com antrópicos:

```json5
{
  env: { SYNTHETIC_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: { primary: "synthetic/hf:MiniMaxAI/MiniMax-M2.1" },
      models: { "synthetic/hf:MiniMaxAI/MiniMax-M2.1": { alias: "MiniMax M2.1" } },
    },
  },
  models: {
    mode: "merge",
    providers: {
      synthetic: {
        baseUrl: "https://api.synthetic.new/anthropic",
        apiKey: "${SYNTHETIC_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "hf:MiniMaxAI/MiniMax-M2.1",
            name: "MiniMax M2.1",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 192000,
            maxTokens: 65536,
          },
        ],
      },
    },
  },
}
```

Notas:

- Definir <<CODE0>> ou utilizar <<CODE1>>>>.
- Modelo ref: <<CODE2>>>>.
- URL base deve omitir <<CODE3>> porque o cliente Antrópico o adiciona.

### Modelos locais (LM Studio) — configuração recomendada

Ver [/gateway/local-models](<<<LINK0>>>) para as orientações locais atuais. TL;DR: execute MiniMax M2.1 através da API LM Studio Responses em hardware sério; mantenha os modelos hospedados mesclados para backback.

# # MiniMax M2.1

Use o MiniMax M2.1 diretamente sem o LM Studio:

```json5
{
  agent: {
    model: { primary: "minimax/MiniMax-M2.1" },
    models: {
      "anthropic/claude-opus-4-5": { alias: "Opus" },
      "minimax/MiniMax-M2.1": { alias: "Minimax" },
    },
  },
  models: {
    mode: "merge",
    providers: {
      minimax: {
        baseUrl: "https://api.minimax.io/anthropic",
        apiKey: "${MINIMAX_API_KEY}",
        api: "anthropic-messages",
        models: [
          {
            id: "MiniMax-M2.1",
            name: "MiniMax M2.1",
            reasoning: false,
            input: ["text"],
            // Pricing: update in models.json if you need exact cost tracking.
            cost: { input: 15, output: 60, cacheRead: 2, cacheWrite: 10 },
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

Notas:

- Definir <<CODE0>>> variável de ambiente ou uso <<CODE1>>.
- Modelo disponível: <<CODE2>> (padrão).
- Atualizar preços em <<CODE3>> se você precisar de monitoramento exato de custos.

## # Cerebras (GLM 4.6/4.7)

Utilizar Cerebras através do seu objectivo compatível com o OpenAI:

```json5
{
  env: { CEREBRAS_API_KEY: "sk-..." },
  agents: {
    defaults: {
      model: {
        primary: "cerebras/zai-glm-4.7",
        fallbacks: ["cerebras/zai-glm-4.6"],
      },
      models: {
        "cerebras/zai-glm-4.7": { alias: "GLM 4.7 (Cerebras)" },
        "cerebras/zai-glm-4.6": { alias: "GLM 4.6 (Cerebras)" },
      },
    },
  },
  models: {
    mode: "merge",
    providers: {
      cerebras: {
        baseUrl: "https://api.cerebras.ai/v1",
        apiKey: "${CEREBRAS_API_KEY}",
        api: "openai-completions",
        models: [
          { id: "zai-glm-4.7", name: "GLM 4.7 (Cerebras)" },
          { id: "zai-glm-4.6", name: "GLM 4.6 (Cerebras)" },
        ],
      },
    },
  },
}
```

Notas:

- Utilizar <<CODE0>> para Cerebras; utilizar <<CODE1>> para Z.AI directamente.
- Definir <<CODE2>> no ambiente ou configuração.

Notas:

- APIs suportadas: <<CODE0>>, <<CODE1>>>, <<CODE2>>,
<<CODE3>>
- Utilizar <<CODE4>> + <<CODE5>> para necessidades de autenticação personalizadas.
- Substituir a raiz de configuração do agente com <<CODE6>> (ou <<CODE7>>>)
e você quer <<CODE8>> armazenado em outro lugar (padrão: <<CODE9>>).

## # <<CODE0>>

Controla o escopo da sessão, a política de reset, os gatilhos de reset e onde a loja de sessão é escrita.

```json5
{
  session: {
    scope: "per-sender",
    dmScope: "main",
    identityLinks: {
      alice: ["telegram:123456789", "discord:987654321012345678"],
    },
    reset: {
      mode: "daily",
      atHour: 4,
      idleMinutes: 60,
    },
    resetByType: {
      thread: { mode: "daily", atHour: 4 },
      dm: { mode: "idle", idleMinutes: 240 },
      group: { mode: "idle", idleMinutes: 120 },
    },
    resetTriggers: ["/new", "/reset"],
    // Default is already per-agent under ~/.openclaw/agents/<agentId>/sessions/sessions.json
    // You can override with {agentId} templating:
    store: "~/.openclaw/agents/{agentId}/sessions/sessions.json",
    // Direct chats collapse to agent:<agentId>:<mainKey> (default: "main").
    mainKey: "main",
    agentToAgent: {
      // Max ping-pong reply turns between requester/target (0–5).
      maxPingPongTurns: 5,
    },
    sendPolicy: {
      rules: [{ action: "deny", match: { channel: "discord", chatType: "group" } }],
      default: "allow",
    },
  },
}
```

Campos:

- <<CODE0>>: tecla do balde de conversação directa (padrão: <<CODE1>>>). Útil quando você deseja “renomear” o fio principal do DM sem alterar <<CODE2>>.
- Nota da caixa de areia: <<CODE3> usa esta chave para detectar a sessão principal. Qualquer tecla de sessão que não corresponda a <<CODE4>> (grupos/canais) é sandboxed.
- <<CODE5>>: como as sessões de DM são agrupadas (padrão: <<CODE6>>>).
- <<CODE7>>: todos os DMs compartilham a sessão principal para a continuidade.
- <<CODE8>>: isolar DMs através do remetente id através de canais.
- <<CODE9>>: DM isolados por canal + remetente (recomendado para caixas de entrada multi- utilizador).
- <<CODE10>>: isolado DMs por conta + canal + remetente (recomendado para caixas de entrada multiconta).
- <<CODE11>>: mapas de id canónicos para pares prefixados por fornecedores, pelo que a mesma pessoa partilha uma sessão de DM entre canais ao utilizar <<CODE12>>, <<CODE13>>, ou <<CODE14>>>>.
- Exemplo: <<CODE15>>>.
- <<CODE16>>: política primária de reinstalação. O padrão é o reset diário às 4:00 AM hora local no host do gateway.
- <<CODE17>>: <<CODE18>> ou <<CODE19>> (padrão: <<CODE20>> quando <<CODE21>> está presente).
- <<CODE22>>: hora local (0-23) para o limite de reset diário.
- <<CODE23>>: janela ociosa em minutos. Quando diariamente + ocioso são configurados, o que expira primeiro ganha.
- <<CODE24>: substitui por sessão <<CODE25>>, <<CODE26>>, e <<CODE27>>>.
- Se você apenas definir legado <<CODE28>> sem qualquer <<CODE29>/<<CODE30>>, OpenClaw permanece em modo ocioso apenas para compatibilidade atrasada.
- <<CODE31>>: sobreposição ociosa opcional para verificações de batimentos cardíacos (o reset diário ainda se aplica quando ativado).
- <<CODE32>>: volta-reposta máxima entre solicitante/alvo (0-5, padrão 5).
- <<CODE33>>: <<CODE34>> ou <<CODE35>falta quando nenhuma regra corresponde.
- <<CODE36>>: correspondência por <<CODE37>>, <<CODE38>> (<<CODE39>>), ou <<CODE40>> (por exemplo, <<CODE41>>>>). Primeiro nega vitórias; caso contrário permitir.

## # <<CODE0>> (configuração de habilidades)

Controla a lista de permissões, instala preferências, pastas de habilidades extras e por habilidade
Ativações. Aplica-se a **competências **e <<CODE0>> (competências no espaço de trabalho)
ainda ganhar em conflitos de nomes).

Campos:

- <<CODE0>>: lista facultativa de autorizações apenas para **compilações**. Se definido, apenas aqueles
As competências agrupadas são elegíveis (competências geridas/espaço de trabalho não afectadas).
- <<CODE1>>: diretórios de habilidade adicionais para escanear (mais baixa precedência).
- <<CODE2>>: preferir instaladores de cerveja quando disponíveis (padrão: true).
- <<CODE3>>: preferência do instalador de nodos (<<CODE4>> <<CODE5>> <<CODE6>, por omissão: npm).
- <<CODE7>>: substitui a configuração por habilidade.

Domínios por qualificação:

- <<CODE0>>: definir <<CODE1>> para desactivar uma habilidade, mesmo que seja agrupada/instalada.
- <<CODE2>>: variáveis de ambiente injectadas para a execução do agente (apenas se não estiverem já definidas).
- <<CODE3>>: conveniência opcional para as competências que declaram um env var primário (por exemplo, <<CODE4>> → <<CODE5>).

Exemplo:

```json5
{
  skills: {
    allowBundled: ["gemini", "peekaboo"],
    load: {
      extraDirs: ["~/Projects/agent-scripts/skills", "~/Projects/oss/some-skill-pack/skills"],
    },
    install: {
      preferBrew: true,
      nodeManager: "npm",
    },
    entries: {
      "nano-banana-pro": {
        apiKey: "GEMINI_KEY_HERE",
        env: {
          GEMINI_API_KEY: "GEMINI_KEY_HERE",
        },
      },
      peekaboo: { enabled: true },
      sag: { enabled: false },
    },
  },
}
```

### <<CODE0> (extensões)

Controla a descoberta do plugin, allow/deny e a configuração por plug-in. Os plug- ins estão carregados
de <<CODE0>>, <<CODE1>>, mais qualquer
<<CODE2> entradas. ** As alterações de confiança requerem um reinício do gateway.**
Ver [/plugin](<<<LINK0>>>) para utilização completa.

Campos:

- <<CODE0>>: opção mestre para carregamento de plugins (padrão: true).
- <<CODE1>>: allowlist opcional de IDs de plugins; quando definido, apenas plugins listados carregam.
- <<CODE2>>: lista de negação opcional de IDs de plugins (vence).
- <<CODE3>>: arquivos ou diretórios adicionais para carregar (absoluto ou <<CODE4>>>).
- <<CODE5>>: substituições por 'plugin'.
- <<CODE6>>: definir <<CODE7>> para desactivar.
- <<CODE8>>: objeto de configuração específico do plugin (validado pelo plugin se fornecido).

Exemplo:

```json5
{
  plugins: {
    enabled: true,
    allow: ["voice-call"],
    load: {
      paths: ["~/Projects/oss/voice-call-extension"],
    },
    entries: {
      "voice-call": {
        enabled: true,
        config: {
          provider: "twilio",
        },
      },
    },
  },
}
```

## # <<CODE0>> (navegador gerenciado por Openclaw)

Openclaw pode iniciar um **dedicado, isolado** Chrome/Brave/Edge/Chromium instância para openclaw e expor um pequeno serviço de controle loopback.
Os perfis podem apontar para um **remote** navegador baseado em crómio via <<CODE0>>. Remoto
os perfis são somente anexados (start/stop/reset estão desativados).

<<CODE0> permanece para configs de perfil único legado e como base
esquema/host para perfis que apenas definiram <<CODE1>>>.

Predefinição:

- activado: <<CODE0>>
- avaliaçãoPermitido: <<CODE1>> (configurado <<CODE2>>> para desactivar <<CODE3>> e <<CODE4>>)
- serviço de controlo: apenas loopback (porta derivada de <<CODE5>>, padrão <<CODE6>>)
- URL CDP: <<CODE7>> (serviço de controle + 1, perfil único legado)
- cor do perfil: <<CODE8>>> (laranja-lobster)
- Nota: o servidor de controle é iniciado pelo gateway em execução (bar de menu OpenClaw.app, ou <<CODE9>>).
- Ordem de detecção automática: navegador padrão se baseado em Chromium; caso contrário Chrome → Brave → Edge → Chromium → Chrome Canary.

```json5
{
  browser: {
    enabled: true,
    evaluateEnabled: true,
    // cdpUrl: "http://127.0.0.1:18792", // legacy single-profile override
    defaultProfile: "chrome",
    profiles: {
      openclaw: { cdpPort: 18800, color: "#FF4500" },
      work: { cdpPort: 18801, color: "#0066CC" },
      remote: { cdpUrl: "http://10.0.0.42:9222", color: "#00AA00" },
    },
    color: "#FF4500",
    // Advanced:
    // headless: false,
    // noSandbox: false,
    // executablePath: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    // attachOnly: false, // set true when tunneling a remote CDP to localhost
  },
}
```

## # <<CODE0>> (Aparência)

Cor de acento opcional usada pelos aplicativos nativos para o cromo da UI (por exemplo, tom de bolha de modo de fala).

Se estiver desligado, os clientes voltam para um azul-claro mudo.

```json5
{
  ui: {
    seamColor: "#FF4500", // hex (RRGGBB or #RRGGBB)
    // Optional: Control UI assistant identity override.
    // If unset, the Control UI uses the active agent identity (config or IDENTITY.md).
    assistant: {
      name: "OpenClaw",
      avatar: "CB", // emoji, short text, or image URL/data URI
    },
  },
}
```

## # <<CODE0>> (Modo servidor de portaway + ligação)

Use <<CODE0> para declarar explicitamente se esta máquina deve executar o Gateway.

Predefinição:

- modo: **unset** (tratado como “não iniciar automaticamente”)
- ligação: <<CODE0>>
- porto: <<CODE1>>> (porta única para WS + HTTP)

```json5
{
  gateway: {
    mode: "local", // or "remote"
    port: 18789, // WS + HTTP multiplex
    bind: "loopback",
    // controlUi: { enabled: true, basePath: "/openclaw" }
    // auth: { mode: "token", token: "your-token" } // token gates WS + Control UI access
    // tailscale: { mode: "off" | "serve" | "funnel" }
  },
}
```

Controlar o caminho da base de IU:

- <<CODE0> define o prefixo URL onde a interface de controle é servida.
- Exemplos: <<CODE1>>, <<CODE2>>, <<CODE3>>>.
- Padrão: root (<<<CODE4>>) (sem alterações).
- <<CODE5> permite a autenticação apenas do símbolo para a interface de controlo quando
identidade do dispositivo é omitida (tipicamente sobre HTTP). Padrão: <<CODE6>>>. Preferir HTTPS
(Tailscale Serve) ou <<CODE7>>>.
- <<CODE8>> desactiva a verificação da identidade do dispositivo
Controlar a UI (somente a palavra-passe). Padrão: <<CODE9>>>>. Apenas vidro partido.

Documentos relacionados:

- [IU de controlo] (<<<LINK0>>>)
- [Observação Web] (<<<LINK1>>>)
- [Tailscale] (<<<LINK2>>>)
- [Acesso remoto] (<<<LINK3>>>)

Proxies confiáveis:

- <<CODE0>>: lista de IPs de proxy reversos que terminam o TLS em frente ao Gateway.
- Quando uma conexão vem de um desses IPs, o OpenClaw usa <<CODE1>> (ou <<CODE2>>>) para determinar o IP do cliente para verificação de emparelhamento local e verificação HTTP/local.
- Só lista proxies que você controla totalmente, e garantir que eles ** sobrescrever** entrada <<CODE3>>.

Notas:

- <<CODE0> se recusa a iniciar, excepto se <<CODE1> for definido como <<CODE2> (ou você passa a bandeira de substituição).
- <<CODE3> controla a porta multiplexada única usada para WebSocket + HTTP (controlar UI, ganchos, A2UI).
- Endpoint do OpenAI Chat Completions: **desactivado por padrão**; activar com <<CODE4>>.
- Precedência: <<CODE5>> > <<CODE6> > <<CODE7>> > por omissão <<CODE8>>.
- Gateway auth é exigida por padrão (token/password ou Tailscale Serve identity). As ligações sem loopback requerem um token/senha compartilhada.
- O assistente de onboarding gera um token de gateway por padrão (mesmo no loopback).
- <<CODE9> é **somente** para chamadas CLI remotas; não permite a autenticação de gateway local. <<CODE10>> é ignorado.

Auth and Tailscale:

- <<CODE0> define os requisitos de aperto de mão (<<CODE1>> ou <<CODE2>>>). Quando desactivado, a autenticação do token é assumida.
- <<CODE3> armazena o token compartilhado para o token auth (utilizado pelo CLI na mesma máquina).
- Quando <<CODE4> é definido, somente esse método é aceito (mais cabeçalhos de Tailscale opcionais).
- <<CODE5>> pode ser definido aqui, ou via <<CODE6>> (recomendado).
- <<CODE7> permite cabeçalhos de identidade Tailscale Serve
(<<<CODE8>>) para satisfazer a autenticação quando o pedido chega em loopback
com <<CODE9>>, <<CODE10>>>, e <<CODE11>>. Openclaw
verifica a identidade resolvendo o <<CODE12>>> endereço via
<<CODE13> antes de o aceitar. Quando <<CODE14>>, Pedidos de serviço não precisam
um token/password; definido <<CODE15>> para exigir credenciais explícitas. Predefinições
<<CODE16>> quando <<CODE17>> e modo de autenticação não é <<CODE18>>.
- <<CODE19> usa Tailscale Serve (tailnet only, loopback bond).
- <<CODE20> expõe o painel publicamente; requer autorização.
- <<CODE21> resets Serve/Funnel config no desligamento.

Por omissão do cliente remoto (CLI):

- <<CODE0> define o URL padrão Gateway WebSocket para chamadas CLI quando <<CODE1>>.
- <<CODE2> seleciona o transporte remoto do macOS (<<CODE3>> padrão, <<CODE4>> para ws/wss). Quando <<CODE5>, <<CODE6> deve ser <<CODE7>> ou <<CODE8>>. <<CODE9> por omissão para porta <<CODE10>>.
- <<CODE11> fornece o token para chamadas remotas (deixar desligado para nenhuma autorização).
- <<CODE12> fornece a senha para chamadas remotas (deixar desativada para nenhuma autenticação).

Comportamento do aplicativo macOS:

- OpenClaw.app observa <<CODE0>> e alterna os modos ao vivo quando <<CODE1>> ou <<CODE2> muda.
- Se <<CODE3> estiver desactivada, mas <<CODE4> estiver definida, a aplicação macOS trata-a como modo remoto.
- Quando você muda o modo de conexão no aplicativo macOS, ele escreve <<CODE5>> (e <<CODE6>> + <<CODE7>> em modo remoto) de volta ao arquivo de configuração.

```json5
{
  gateway: {
    mode: "remote",
    remote: {
      url: "ws://gateway.tailnet:18789",
      token: "your-token",
      password: "your-password",
    },
  },
}
```

Exemplo de transporte directo (aplicativo macOS):

```json5
{
  gateway: {
    mode: "remote",
    remote: {
      transport: "direct",
      url: "wss://gateway.example.ts.net",
      token: "your-token",
    },
  },
}
```

## # <<CODE0>> (Config recarga a quente)

O Gateway observa <<CODE0>> (ou <<CODE1>>>) e aplica alterações automaticamente.

Modos:

- <<CODE0>> (padrão): alterações seguras de aplicação quente; reinicie o Gateway para mudanças críticas.
- <<CODE1>>: aplicar apenas alterações em segurança quente; registar quando é necessário reiniciar.
- <<CODE2>: reiniciar o Gateway em qualquer alteração de configuração.
- <<CODE3>>: desativar a recarga quente.

```json5
{
  gateway: {
    reload: {
      mode: "hybrid",
      debounceMs: 300,
    },
  },
}
```

### # Matriz de recarga quente (arquivos + impacto)

Ficheiros observados:

- <<CODE0> (ou <<CODE1>>)

Aplicado a quente (sem reinicialização completa do gateway):

- <<CODE0> (auth/path/mappings) + <<CODE1> (Gmail watcher reiniciado)
- <<CODE2>> (o servidor de controlo do navegador é reiniciado)
- <<CODE3>> (início do serviço de cron + atualização de concorrência)
- <<CODE4>> (Coração do coração reiniciar)
- <<CODE5>> (Início do canal Web WhatsApp)
- <<CODE6>>, <<CODE7>>, <<CODE8>>, <<CODE9>> (reinicia o canal)
- <<CODE10>>, <<CODE11>>, <<CODE12>>, <<CODE13>>, <<CODE14>>, <<CODE15>>, <<CODE16>>, <<CODE17>>>, <<CODE18>>, <<CODE19>, <<CODE20>, <<CODE21>> (leituras dinâmicas)

Requer o reinício do Gateway completo:

- <<CODE0> (porta/bind/auth/control UI/tailscale)
- <<CODE1> (legacia)
- <<CODE2>>
- <<CODE3>>
- <<CODE4>>
- Qualquer caminho de configuração desconhecido/não suportado (por omissão para reiniciar por segurança)

Isolação multi-instance

Para executar múltiplos gateways em um host (para redundância ou um bot de resgate), isole o estado por instalação + config e use portas únicas:

- <<CODE0> (por instalação)
- <<CODE1> (sessões/credos)
- <<CODE2> (memórias)
- <<CODE3> (único por instância)

Bandeiras de conveniência (CLI):

- <<CODE0>> → usa <<CODE1>>> + portas de deslocamento da base <<CODE2>
- <<CODE3> → usa <<CODE4>> (porta via config/env/flags)

Veja [Gateway runbook] (<<<LINK0>>) para o mapeamento de portas derivado (gateway/browser/canvas).
Veja [Gateways múltiplos](<<<LINK1>>>) para detalhes de isolamento de portas navegador/CDP.

Exemplo:

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/a.json \
OPENCLAW_STATE_DIR=~/.openclaw-a \
openclaw gateway --port 19001
```

## # <<CODE0>> (Gateway webhooks)

Habilite um endpoint webhook HTTP simples no servidor HTTP Gateway.

Predefinição:

- activado: <<CODE0>>
- caminho: <<CODE1>>
- maxBodyBytes: <<CODE2>> (256 KB)

```json5
{
  hooks: {
    enabled: true,
    token: "shared-secret",
    path: "/hooks",
    presets: ["gmail"],
    transformsDir: "~/.openclaw/hooks",
    mappings: [
      {
        match: { path: "gmail" },
        action: "agent",
        wakeMode: "now",
        name: "Gmail",
        sessionKey: "hook:gmail:{{messages[0].id}}",
        messageTemplate: "From: {{messages[0].from}}\nSubject: {{messages[0].subject}}\n{{messages[0].snippet}}",
        deliver: true,
        channel: "last",
        model: "openai/gpt-5.2-mini",
      },
    ],
  },
}
```

Os pedidos devem incluir o token de gancho:

- <<CODE0> **ou **
- <<CODE1> **ou **
- <<CODE2>>

Pontos finais:

- <<CODE0>> → <<CODE1>>>
- <<CODE2>> → <<CODE3>>
- <<CODE4> → resolvido por <<CODE5>>

<<CODE0> sempre publica um resumo na sessão principal (e pode opcionalmente desencadear um batimento cardíaco imediato via <<CODE1>>).

Notas de mapeamento:

- <<CODE0> corresponde ao sub-caminho após <<CODE1>> (por exemplo, <<CODE2>> → <<CODE3>>).
- <<CODE4> corresponde a um campo de carga útil (por exemplo, <<CODE5>>) para que possa utilizar um caminho genérico <<CODE6>>.
- Modelos como <<CODE7>> lidos da carga útil.
- <<CODE8>> pode apontar para um módulo JS/TS que retorna uma ação de gancho.
- <<CODE9> envia a resposta final para um canal; <<CODE10>> defaults to <<CODE11> (regressa ao WhatsApp).
- Se não houver uma rota de entrega prévia, definir <<CODE12>> + <<CODE13>> explicitamente (necessário para Telegram/Discord/Google Chat/Slack/Signal/iMessage/MS Teams).
- <<CODE14>> substitui o LLM para esta execução de gancho (<<CODE15>> ou alias; deve ser permitido se <<CODE16>> for definido).

Configuração do helper do Gmail (utilizada por <<CODE0>> / <<CODE1>>>):

```json5
{
  hooks: {
    gmail: {
      account: "openclaw@gmail.com",
      topic: "projects/<project-id>/topics/gog-gmail-watch",
      subscription: "gog-gmail-watch-push",
      pushToken: "shared-push-token",
      hookUrl: "http://127.0.0.1:18789/hooks/gmail",
      includeBody: true,
      maxBytes: 20000,
      renewEveryMinutes: 720,
      serve: { bind: "127.0.0.1", port: 8788, path: "/" },
      tailscale: { mode: "funnel", path: "/gmail-pubsub" },

      // Optional: use a cheaper model for Gmail hook processing
      // Falls back to agents.defaults.model.fallbacks, then primary, on auth/rate-limit/timeout
      model: "openrouter/meta-llama/llama-3.3-70b-instruct:free",
      // Optional: default thinking level for Gmail hooks
      thinking: "off",
    },
  },
}
```

Substituição do modelo para ganchos Gmail:

- <<CODE0> especifica um modelo a usar para o processamento do gancho do Gmail (padrão para o primário da sessão).
- Aceita <<CODE1>> refs ou aliases de <<CODE2>>.
- Regressa a <<CODE3>, depois <<CODE4>, em casos de auth/rate-limit/timeouts.
- Se <<CODE5> for definido, inclua o modelo de ganchos na lista de permissão.
- Na inicialização, avisa se o modelo configurado não está no catálogo do modelo ou allowlist.
- <<CODE6> define o nível de pensamento padrão para ganchos Gmail e é substituído por per-hook <<CODE7>.

Auto- arranque da porta:

- Se <<CODE0> e <<CODE1>> for definido, o Gateway começa
<<CODE2> no arranque e renova automaticamente o relógio.
- Definir <<CODE3>> para desativar o início automático (para execução manual).
- Evite executar um separado <<CODE4>> ao lado do Gateway; ele irá
falhar com <<CODE5>>>.

Nota: quando <<CODE0>> está ligado, o OpenClaw defaults <<CODE1>> para <<CODE2> assim
Tailscale pode proxy <<CODE3> corretamente (ele tira o prefixo de set-path).
Se você precisar da infra- estrutura para receber o caminho prefixado, defina
<<CODE4>> para um URL completo (e alinhar <<CODE5>>>).

## # <<CODE0>> (LAN/tailnet Canvas file server + live reload)

O Gateway serve um diretório de HTML/CSS/JS sobre HTTP para que nós iOS/Android possam simplesmente <<CODE0>> para ele.

Raiz padrão: <<CODE0>>
Porta padrão: <<CODE1>>> (escolhido para evitar a porta CDP do navegador openclaw <<CODE2>>)
O servidor escuta no host **gateway vincular** (LAN ou Tailnet) para que nós possam alcançá-lo.

O servidor:

- serve arquivos em <<CODE0>>>
- injeta um pequeno cliente de recarga em HTML servido
- observa o directório e as emissões recarregam num ponto WebSocket em <<CODE1>>
- cria automaticamente um iniciador <<CODE2>> quando o diretório está vazio (assim você vê algo imediatamente)
- também serve A2UI em <<CODE3>> e é anunciado para nós como <<CODE4>>
(sempre usado por nós para Canvas/A2UI)

Desactivar a recarga ao vivo (e a visualização de ficheiros) se o directório for grande ou se carregar em <<CODE0>:

- configuração: <<CODE0>>>

```json5
{
  canvasHost: {
    root: "~/.openclaw/workspace/canvas",
    port: 18793,
    liveReload: true,
  },
}
```

As alterações para <<CODE0> requerem um reinício do gateway (o reload da configuração será reiniciado).

Desactivar com:

- configuração: <<CODE0>>>
- env: <<CODE1>>

#### <<CODE0>> (ponte TCP legada, removida)

As construções atuais não incluem mais o ouvinte de ponte TCP; <<CODE0>> chaves de configuração são ignoradas.
Os nós conectam-se sobre o WebSocket Gateway. Esta secção é mantida para referência histórica.

Comportamento legado:

- O Gateway poderia expor uma simples ponte TCP para nós (iOS/Android), tipicamente na porta <<CODE0>>.

Predefinição:

- activado: <<CODE0>>
- porto: <<CODE1>>>
- ligação: <<CODE2>> (ligação a <<CODE3>>)

Modos de ligação:

- <<CODE0>>: <<CODE1>>> (alcançável em qualquer interface, incluindo LAN/Wi-Fi e Tailscale)
- <<CODE2>>: ligar- se apenas ao IP da escala de cauda da máquina (recomendado para Viena □ Londres)
- <<CODE3>>: <<CODE4>> (apenas local)
- <<CODE5>: preferir IP tailnet se presente, caso contrário <<CODE6>>

TLS:

- <<CODE0>>: habilitar TLS para conexões de ponte (somente LTS quando ativado).
- <<CODE1>>: gerar um certificado auto-assinado quando nenhum certificado/chave estiver presente (padrão: true).
- <<CODE2>>/ <<CODE3>>: Caminhos PEM para o certificado de ponte + chave privada.
- <<CODE4>>: pacote opcional PEM CA (raízes personalizadas ou mTLS futuros).

Quando o TLS está habilitado, o Gateway anuncia <<CODE0>> e <<CODE1>> na descoberta TXT
registros para que nós possam fixar o certificado. Conexões manuais usam confiança na primeira utilização se não
A impressão digital ainda está guardada.
Certificados gerados automaticamente requerem <<CODE2>> no PATH; se a geração falhar, a ponte não começará.

```json5
{
  bridge: {
    enabled: true,
    port: 18790,
    bind: "tailnet",
    tls: {
      enabled: true,
      // Uses ~/.openclaw/bridge/tls/bridge-{cert,key}.pem when omitted.
      // certPath: "~/.openclaw/bridge/tls/bridge-cert.pem",
      // keyPath: "~/.openclaw/bridge/tls/bridge-key.pem"
    },
  },
}
```

## # <<CODE0>> (Modo de transmissão Bonjour / mDNS)

Controla as transmissões de descoberta da LAN mDNS (<<<CODE0>>).

- <<CODE0> (padrão): omitir <<CODE1>> + <HTML2>>> dos registos TXT
- <<CODE3>>: incluem <<CODE4>> + <<CODE5>> nos registos TXT
- <<CODE6>>: desactivar inteiramente as emissões mDNS
- Nome de máquina: padrão para <<CODE7>> (publicidades <<CODE8>>). Substituir por <<CODE9>>>>.

```json5
{
  discovery: { mdns: { mode: "minimal" } },
}
```

## # <<CODE0>> (Wide-Area Bonjour / unicast DNS-SD)

Quando habilitado, o Gateway escreve uma zona DNS-SD para <<CODE0>> em <<CODE1>> usando o domínio de descoberta configurado (exemplo: <<CODE2>>>).

Para fazer iOS/Android descobrir através de redes (Vienna em Londres), emparelhe isso com:

- um servidor DNS na máquina de gateway que serve o seu domínio escolhido (o CoreDNS é recomendado)
- Tailscale ** split DNS** para que os clientes resolvam esse domínio através do servidor DNS gateway

Ajudante de configuração única (host de porta):

```bash
openclaw dns setup --apply
```

```json5
{
  discovery: { wideArea: { enabled: true } },
}
```

# # Variáveis de modelo

Os substitutos do modelo são expandidos em <<CODE0>> e <<CODE1>> (e quaisquer campos futuros de argumentos modelados).

Descrição
------------------------------------------------------------------------- -----
* <<CODE0>> Corpo completo da mensagem de entrada
* <<CODE1>> * Corpo de mensagem de entrada bruto (sem embalagem de histórico/sender; melhor para análise de comandos)
<<CODE2>> Corpo com menções de grupo despojado (melhor padrão para agentes)
(E.164 para WhatsApp; pode diferir por canal)
<<CODE4>> Identificador do destino
(quando disponível)
<<CODE6>> □ UUID de sessão atual
Quando uma nova sessão foi criada
* < <<CODE9>> * Meios de entrada pseudo-URL (se presentes)
Localização da mídia local (se baixado)
Tipo de mídia (imagem/audio/documento/...)
(quando activada)
□ <<CODE13> > □ Prompt de mídia resolvido para entradas CLI
<<CODE14>> Caracteres de saída máximo resolvidos para entradas CLI
< <<CODE15>> <<CODE16>> ou <<CODE17>>
(melhor esforço)
Previsão dos membros do grupo (melhor esforço)
□ <<CODE20>>
Número de telefone do remetente (melhor esforço)
(Whatsapp, telegrama, discórdia, googlechat, folga, sinal)

# # Cron (grampeador de portas)

Cron é um agendador de Gateway para despertares e trabalhos agendados. Veja [Trabalhos Cron](<<<LINK0>>) para a visão geral do recurso e exemplos CLI.

```json5
{
  cron: {
    enabled: true,
    maxConcurrentRuns: 2,
  },
}
```

---

Próximo: [Agente Runtime](<<<LINK0>>) 
