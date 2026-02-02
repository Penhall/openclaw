---
summary: "OpenClaw plugins/extensions: discovery, config, and safety"
read_when:
  - Adding or modifying plugins/extensions
  - Documenting plugin install or load rules
---

# Plugins (Extensões)

# # Início rápido (novo para plugins?)

Um plugin é apenas um **pequeno módulo de código** que estende OpenClaw com extra
funcionalidades (comandos, ferramentas e RPC Gateway).

Na maioria das vezes, você vai usar plugins quando você quer um recurso que não é construído
no núcleo OpenClaw ainda (ou você quer manter recursos opcionais fora do seu principal
instalar).

Caminho rápido:

1. Veja o que já está carregado:

```bash
openclaw plugins list
```

2. Instale um plugin oficial (exemplo: Voice Call):

```bash
openclaw plugins install @openclaw/voice-call
```

3. Reinicie o Gateway, depois configure em <<CODE0>>.

Veja [Voice Call](<<<LINK0>>) para um plugin de exemplo concreto.

# # Plugins disponíveis (oficial)

- Microsoft Teams é apenas plugin a partir de 2026.1.15; instalar <<CODE0>> se você usar Teams.
- Memória (Core) — 'plugin' de pesquisa de memória agrupada (activado por omissão via <<CODE1>>)
- Memória (LanceDB) — 'plugin' de memória de longo prazo (recuperação automática/captura; definido <<CODE2>>)
- [Chamada de voz] (<<<<LINK0>>>) — <<CODE3>>
- [Zalo Personal] (<<<LINK1>>) - <<CODE4>
- [Matrix] (<<<LINK2>>>) — <<CODE5>>
- [Nostr] (<<<LINK3>>) - <<CODE6>
- [Zalo] (<<<LINK4>>) - <<CODE7>
- [Equipes Microsoft] (<<<LINK5>>>) - <<CODE8>>
- Google Antigravity OAuth (providencial auth) — embalado como <<CODE9>> (desactivado por omissão)
- Gemini CLI OAuth (provider auth) — embalado como <<CODE10>> (desactivado por omissão)
- Qwen OAuth (autência do fornecedor) — embalado como <<CODE11> (desactivado por omissão)
- Copilot Proxy (provider auth) — VS Copilot Copilot Proxy bridge local; distinto de built-in <<CODE12>> login do dispositivo (abundado, desativado por padrão)

Os plugins OpenClaw são **TypeScript modules** carregados em tempo de execução via jiti. **Config
validação não executa código de plugin**; ele usa o manifesto de plugin e JSON
Esquema em vez disso. Ver [O manifesto de plugin] (<<<LINK0>>>).

Os plug-ins podem registrar:

- Métodos RPC Gateway
- Porta HTTP manipuladores
- Ferramentas de agente
- Comandos CLI
- Serviços de apoio
- Validação de configuração opcional
- ** Skills** (listando <<CODE0>> diretórios no manifesto do plugin)
- ** Comandos de resposta automática** (executar sem invocar o agente IA)

Plugins rodam **in-process** com o Gateway, então trate-os como código confiável.
Guia de criação de ferramentas: [Ferramentas de agente de plugin] (<<<LINK0>>>).

# # Ajudantes de corrida

Plugins podem acessar helpers selecionados através de <<CODE0>>. Para telefonia TTS:

```ts
const result = await api.runtime.tts.textToSpeechTelephony({
  text: "Hello from OpenClaw",
  cfg: api.config,
});
```

Notas:

- Usa núcleo <<CODE0>> configuração (OpenAI ou OnzeLabs).
- Retorna buffer de áudio PCM + taxa de amostra. Os 'plugins' devem ser reamostrados/codificados para os fornecedores.
- Edge TTS não é suportado para telefonia.

# # Descoberta e precedência

Escaneia Openclaw, em ordem:

1. Caminhos de configuração

- <<CODE0>> (ficheiro ou directório)

2. Extensões de espaço de trabalho

- <<CODE0>>
- <<CODE1>>

3. Extensões globais

- <<CODE0>>
- <<CODE1>>

4. Extensões agrupadas (enviadas com OpenClaw, ** desativadas por padrão**)

- <<CODE0>>

Plugins agrupados devem ser ativados explicitamente via <<CODE0>>
quer <<CODE1>>>. Plug-ins instalados estão habilitados por padrão,
mas pode ser desativado da mesma forma.

Cada plugin deve incluir um arquivo <<CODE0>> em sua raiz. Se um caminho
pontos em um arquivo, o plugin root é o diretório do arquivo e deve conter o
manifesto.

Se vários plugins resolverem para o mesmo ID, a primeira correspondência na ordem acima
vitórias e cópias de menor precedência são ignoradas.

Pacotes

Um diretório de plugins pode incluir um <<CODE0>> com <<CODE1>>:

```json
{
  "name": "my-pack",
  "openclaw": {
    "extensions": ["./src/safety.ts", "./src/tools.ts"]
  }
}
```

Cada entrada torna-se um plugin. Se o pacote lista várias extensões, o ID do plugin
torna-se <<CODE0>>>.

Se o seu plugin importar deps npm, instale-os nesse diretório assim
<<CODE0> está disponível (<<CODE1>>/ <<CODE2>>).

## # Metadados do catálogo de canais

Os plug-ins de canais podem anunciar metadados embarcados via <<CODE0>> e
instalar dicas via <<CODE1>>>>. Isto mantém o catálogo principal livre de dados.

Exemplo:

```json
{
  "name": "@openclaw/nextcloud-talk",
  "openclaw": {
    "extensions": ["./index.ts"],
    "channel": {
      "id": "nextcloud-talk",
      "label": "Nextcloud Talk",
      "selectionLabel": "Nextcloud Talk (self-hosted)",
      "docsPath": "/channels/nextcloud-talk",
      "docsLabel": "nextcloud-talk",
      "blurb": "Self-hosted chat via Nextcloud Talk webhook bots.",
      "order": 65,
      "aliases": ["nc-talk", "nc"]
    },
    "install": {
      "npmSpec": "@openclaw/nextcloud-talk",
      "localPath": "extensions/nextcloud-talk",
      "defaultChoice": "npm"
    }
  }
}
```

OpenClaw também pode mesclar ** catálogos de canais externos** (por exemplo, um MPM
exportação de registo). Solte um arquivo JSON em um dos seguintes:

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>

Ou ponto <<CODE0>> (ou <<CODE1>>>>) em
um ou mais ficheiros JSON (comma/semicolon/<<CODE2>>-delimitado). Cada arquivo deve
contém <<CODE3>>>>.

# # IDs de plug-in

IDs de plug-in padrão:

- Embalagens: <<CODE0>> <<CODE1>>>
- Ficheiro autónomo: nome da base de ficheiros (<<<CODE2>>> → <<CODE3>>>)

Se um plugin exporta <<CODE0>>, OpenClaw o usa, mas avisa quando ele não corresponde ao
ID configurado.

Configuração

```json5
{
  plugins: {
    enabled: true,
    allow: ["voice-call"],
    deny: ["untrusted-plugin"],
    load: { paths: ["~/Projects/oss/voice-call-extension"] },
    entries: {
      "voice-call": { enabled: true, config: { provider: "twilio" } },
    },
  },
}
```

Campos:

- <<CODE0>>: opção mestre (por omissão: true)
- <<CODE1>>: allowlist (opcional)
- <<CODE2>>: needlist (opcional; nega vitórias)
- <<CODE3>>: arquivos/dires de plugin extra
- <<CODE4>>: comutações por plug- in + configuração

Alterações de configuração **requer um reinício do gateway**.

Regras de validação (strict):

- IDs de plugin desconhecidos em <<CODE0>>, <<CODE1>>, <<CODE2>>, ou <<CODE3>> são **erros**.
- Desconhecido <<CODE4>> chaves são ** erros** a menos que um manifesto plugin declara
o ID do canal.
- A configuração do plugin é validada usando o esquema JSON incorporado
<<CODE5> (<<CODE6>>>).
- Se um plugin está desativado, sua configuração é preservada e um ** aviso** é emitido.

# # slots de plug-in (categorias exclusivas)

Algumas categorias de plugins são **exclusive** (apenas um ativo de cada vez). Utilização
<<CODE0> para selecionar qual plugin possui o slot:

```json5
{
  plugins: {
    slots: {
      memory: "memory-core", // or "none" to disable memory plugins
    },
  },
}
```

Se vários plugins declararem <<CODE0>>, somente o selecionado carrega. Outros
estão incapacitados com os diagnósticos.

# # Controlar UI (esquema + rótulos)

A interface de controle usa <<CODE0>> (Esquema JSON + <<CODE1>>>) para renderizar formas melhores.

OpenClaw aumenta <<CODE0>> em tempo de execução baseado em plugins descobertos:

- Adiciona rótulos por plug- in para <<CODE0>>/ <<CODE1>>/ <<CODE2>>
- Mergulha as dicas de campo de configuração facultativas fornecidas pelo plugin em:
<<CODE3>>

Se você quiser que seus campos de configuração do plugin mostrem bons rótulos/placeholders (e marquem segredos como sensíveis),
fornecer <<CODE0>> ao lado do seu esquema JSON no manifesto do plugin.

Exemplo:

```json
{
  "id": "my-plugin",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "apiKey": { "type": "string" },
      "region": { "type": "string" }
    }
  },
  "uiHints": {
    "apiKey": { "label": "API Key", "sensitive": true },
    "region": { "label": "Region", "placeholder": "us-east-1" }
  }
}
```

# # CLI

```bash
openclaw plugins list
openclaw plugins info <id>
openclaw plugins install <path>                 # copy a local file/dir into ~/.openclaw/extensions/<id>
openclaw plugins install ./extensions/voice-call # relative path ok
openclaw plugins install ./plugin.tgz           # install from a local tarball
openclaw plugins install ./plugin.zip           # install from a local zip
openclaw plugins install -l ./extensions/voice-call # link (no copy) for dev
openclaw plugins install @openclaw/voice-call # install from npm
openclaw plugins update <id>
openclaw plugins update --all
openclaw plugins enable <id>
openclaw plugins disable <id>
openclaw plugins doctor
```

<<CODE0> só funciona para instalações npm rastreadas em <<CODE1>>.

Plugins também podem registrar seus próprios comandos de topo (exemplo: <<CODE0>>>).

# # API de plug-in (overview)

Exportação de plug-ins:

- Função A: <<CODE0>>
- Um objeto: <<CODE1>>>

# # Ganchos de plug-in

Plugins podem enviar ganchos e registrá-los em tempo de execução. Isto permite que um pacote de plugins
Automação baseada em eventos sem uma instalação separada do hook pack.

Exemplo

```
import { registerPluginHooksFromDir } from "openclaw/plugin-sdk";

export default function register(api) {
  registerPluginHooksFromDir(api, "./hooks");
}
```

Notas:

- Os directórios do gancho seguem a estrutura normal do gancho (<<<CODE0>>> + <<CODE1>>>).
- Regras de elegibilidade do gancho ainda se aplicam (OS/bins/env/config requirements).
- Ganchos gerenciados por plug-in aparecem em <<CODE2>> com <<CODE3>>.
- Você não pode ativar/desativar ganchos gerenciados por plug-in via <<CODE4>>; habilitar/desativar o plugin em vez disso.

# # Plug-ins do provedor (autenticação do modelo)

Plugins podem registrar **model provider auth** fluxos para que os usuários possam executar OAuth ou
Configuração da chave API dentro do OpenClaw (sem scripts externos necessários).

Registre um provedor via <<CODE0>>>>. Cada provedor expõe um
ou mais métodos de autenticação (OAuth, chave API, código do dispositivo, etc.). Estes métodos de potência:

- <<CODE0>>

Exemplo:

```ts
api.registerProvider({
  id: "acme",
  label: "AcmeAI",
  auth: [
    {
      id: "oauth",
      label: "OAuth",
      kind: "oauth",
      run: async (ctx) => {
        // Run OAuth flow and return auth profiles.
        return {
          profiles: [
            {
              profileId: "acme:default",
              credential: {
                type: "oauth",
                provider: "acme",
                access: "...",
                refresh: "...",
                expires: Date.now() + 3600 * 1000,
              },
            },
          ],
          defaultModel: "acme/opus-1",
        };
      },
    },
  ],
});
```

Notas:

- <<CODE0> recebe uma <<CODE1>> com <<CODE2>>, <<CODE3>>,
<<CODE4>>, e <<CODE5>> auxiliares.
- Retornar <<CODE6>> quando você precisar adicionar modelos padrão ou configuração do provedor.
- Retorno <<CODE7>> assim <<CODE8> pode atualizar o padrão do agente.

## # Registre um canal de mensagens

Plugins podem registrar **plugins de canais** que se comportam como canais embutidos
(WhatsApp, Telegram, etc.). A configuração do canal vive em <<CODE0>> e é
validado pelo seu código de plugin do canal.

```ts
const myChannel = {
  id: "acmechat",
  meta: {
    id: "acmechat",
    label: "AcmeChat",
    selectionLabel: "AcmeChat (API)",
    docsPath: "/channels/acmechat",
    blurb: "demo channel plugin.",
    aliases: ["acme"],
  },
  capabilities: { chatTypes: ["direct"] },
  config: {
    listAccountIds: (cfg) => Object.keys(cfg.channels?.acmechat?.accounts ?? {}),
    resolveAccount: (cfg, accountId) =>
      cfg.channels?.acmechat?.accounts?.[accountId ?? "default"] ?? {
        accountId,
      },
  },
  outbound: {
    deliveryMode: "direct",
    sendText: async () => ({ ok: true }),
  },
};

export default function (api) {
  api.registerChannel({ plugin: myChannel });
}
```

Notas:

- Coloque a configuração em <<CODE0>> (não <<CODE1>>>).
- <<CODE2> é utilizado para etiquetas nas listas CLI/UI.
- <<CODE3> adiciona ids alternativos para normalização e entradas de CLI.
- <<CODE4>> lista os IDs do canal para saltar automaticamente quando ambos estiverem configurados.
- <<CODE5>> e <<CODE6> deixar que as UI mostrem rótulos/ícones de canais mais ricos.

## # Escreva um novo canal de mensagens (passo a passo)

Use isto quando quiser um **novo chat surface** (um “canal de mensagens”), não um fornecedor de modelos.
O fornecedor de modelos docs vive em <<CODE0>>>.

1. Escolha uma forma de id + configuração

- Toda a configuração do canal vive em <<CODE0>>.
- Prefere <<CODE1>> para configurações multi-conta.

2. Defina os metadados do canal

- <<CODE0>>, <<CODE1>>, <<CODE2>>, <<CODE3>listas de controlo CLI/UI.
- <<CODE4>> deve apontar para uma página de documentos como <<CODE5>>.
- <<CODE6> permite que um plugin substitua outro canal (auto-ativado prefere).
- <<CODE7>> e <<CODE8>> são utilizados pelas UI para texto/ícones detalhados.

3. Implementar os adaptadores necessários

- <<CODE0>> + <<CODE1>>>
- <<CODE2>> (tipos de conversação, mídia, threads, etc.)
- <<CODE3>> + <<CODE4>> (para envio de base)

4. Adicione adaptadores opcionais conforme necessário

- <<CODE0> (espectáculo), <<CODE1>> (política de DM), <<CODE2>> (saúde/diagnóstico)
- <<CODE3> (start/stop/login), <<CODE4>>, <<CODE5>>, <<CODE6>>
- <<CODE7> (ações de mensagens), <<CODE8>> (comportamento de comando nativo)

5. Registre o canal em seu plugin

- <<CODE0>>

Exemplo mínimo de configuração:

```json5
{
  channels: {
    acmechat: {
      accounts: {
        default: { token: "ACME_TOKEN", enabled: true },
      },
    },
  },
}
```

Plug- in de canal mínimo (somente de saída):

```ts
const plugin = {
  id: "acmechat",
  meta: {
    id: "acmechat",
    label: "AcmeChat",
    selectionLabel: "AcmeChat (API)",
    docsPath: "/channels/acmechat",
    blurb: "AcmeChat messaging channel.",
    aliases: ["acme"],
  },
  capabilities: { chatTypes: ["direct"] },
  config: {
    listAccountIds: (cfg) => Object.keys(cfg.channels?.acmechat?.accounts ?? {}),
    resolveAccount: (cfg, accountId) =>
      cfg.channels?.acmechat?.accounts?.[accountId ?? "default"] ?? {
        accountId,
      },
  },
  outbound: {
    deliveryMode: "direct",
    sendText: async ({ text }) => {
      // deliver `text` to your channel here
      return { ok: true };
    },
  },
};

export default function (api) {
  api.registerChannel({ plugin });
}
```

Carregar o plugin (dir extensões ou <<CODE0>>), reiniciar o gateway,
então configure <<CODE1>> em sua configuração.

# # Ferramentas de agente

Veja o guia dedicado: [Ferramentas de agente de plugin](<<<LINK0>>>).

## # Registre um método RPC gateway

```ts
export default function (api) {
  api.registerGatewayMethod("myplugin.status", ({ respond }) => {
    respond(true, { ok: true });
  });
}
```

## # Registre comandos CLI

```ts
export default function (api) {
  api.registerCli(
    ({ program }) => {
      program.command("mycmd").action(() => {
        console.log("Hello");
      });
    },
    { commands: ["mycmd"] },
  );
}
```

## # Registre comandos de resposta automática

Plugins podem registrar comandos de barra personalizados que executam ** sem invocar o
Agente de IA**. Isto é útil para alternar comandos, verificações de estado ou ações rápidas
que não precisam de processamento LLM.

```ts
export default function (api) {
  api.registerCommand({
    name: "mystatus",
    description: "Show plugin status",
    handler: (ctx) => ({
      text: `Plugin is running! Channel: ${ctx.channel}`,
    }),
  });
}
```

Contexto do manipulador de comandos:

- <<CODE0>>: ID do remetente (se disponível)
- <<CODE1>>: O canal para onde o comando foi enviado
- <<CODE2>>: Se o remetente é um utilizador autorizado
- <<CODE3>>: Argumentos passados após o comando (se <<CODE4>>>)
- <<CODE5>>: O texto de comando completo
- <<CODE6>>: A configuração atual do OpenClaw

Opções de comando:

- <<CODE0>>: Nome do comando (sem o líder <<CODE1>>>)
- <<CODE2>>: Texto de ajuda mostrado nas listas de comandos
- <<CODE3>>: Se o comando aceita argumentos (por omissão: false). Se false e argumentos forem fornecidos, o comando não corresponderá e a mensagem cai para outros manipuladores
- <<CODE4>>: Requerer o remetente autorizado (por omissão: true)
- <<CODE5>>: Função que retorna <<CODE6>>> (pode ser assinc)

Exemplo com autorização e argumentos:

```ts
api.registerCommand({
  name: "setmode",
  description: "Set plugin mode",
  acceptsArgs: true,
  requireAuth: true,
  handler: async (ctx) => {
    const mode = ctx.args?.trim() || "default";
    await saveMode(mode);
    return { text: `Mode set to: ${mode}` };
  },
});
```

Notas:

- Os comandos do Plugin são processados **antes de** comandos incorporados e o agente de IA
- Os comandos são registrados globalmente e funcionam em todos os canais
- Nomes de comandos são insensíveis (<<<CODE0>> correspondências <<CODE1>>>)
- Nomes de comando devem começar com uma letra e conter apenas letras, números, hífens, e sublinha
- Nomes de comandos reservados (como <<CODE2>>, <<CODE3>>, <<CODE4>>>, etc.) não podem ser substituídos por plugins
- Duplicar o registro de comando através de plugins irá falhar com um erro diagnóstico

## # Registro serviços de fundo

```ts
export default function (api) {
  api.registerService({
    id: "my-service",
    start: () => api.logger.info("ready"),
    stop: () => api.logger.info("bye"),
  });
}
```

# # Convenções de nomeação

- Métodos de gateway: <<CODE0>> (exemplo: <<CODE1>>)
- Ferramentas: <<CODE2>> (exemplo: <<CODE3>>)
- Comandos CLI: kebab ou camelo, mas evitar conflitos com comandos core

# # Habilidades

Plugins pode enviar uma habilidade no repo (<<<CODE0>>>).
Activar com <<CODE1>>> (ou outras portas de configuração) e garantir
está presente nos locais de trabalho/gestão de competências.

# # Distribuição (npm)

Embalagem recomendada:

- Pacote principal: <<CODE0>>> (este acordo)
- Plugins: pacotes npm separados em <<CODE1>> (exemplo: <<CODE2>>)

Contrato de publicação:

- Plugin <<CODE0> deve incluir <<CODE1>> com um ou mais arquivos de entrada.
- Os ficheiros de entrada podem ser <<CODE2>> ou <<CODE3>> (jiti carrega TS em tempo de execução).
- <<CODE4> usa <<CODE5>>, extrai para <<CODE6>>, e permite-o em configuração.
- Estabilidade da chave de configuração: pacotes com escopo são normalizados para o ** unscoped** id para <<CODE7>>.

# # Plug-in de exemplo: Chamada de voz

Este recurso inclui um plugin de chamada de voz (Twilio ou retrocesso de registo):

- Fonte: <<CODE0>>
- Habilidade: <<CODE1>>
- CLI: <<CODE2>>
- Ferramenta: <<CODE3>>>
- RPC: <<CODE4>>, <<CODE5>>
- Configuração (twilio): <<CODE6>> + <<CODE7>>> (opcional <<CODE8>>, <<CODE9>>)
- Configuração (dev): <<CODE10>> (sem rede)

Veja [Voice Call](<<<LINK0>>) e <<CODE0>> para configuração e uso.

# # Notas de segurança

Plugins são executados em processo com o Gateway. Trate-os como código confiável:

- Só instala plugins em que confia.
- Prefere <<CODE0>> allowlists.
- Reinicia o portal depois das mudanças.

# # Testando plugins

Os plug-ins podem (e devem) testar o navio:

- Os plugins In-repo podem manter os testes de Vitest em <<CODE0>> (exemplo: <<CODE1>>).
- Os plugins publicados separadamente devem executar seu próprio CI (lint/build/test) e validar <<CODE2> pontos no ponto de entrada construído (<<CODE3>>).
