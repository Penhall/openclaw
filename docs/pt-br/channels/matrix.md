---
summary: "Matrix support status, capabilities, and configuration"
read_when:
  - Working on Matrix channel features
---

Matriz (plugin)

Matrix é um protocolo de mensagens aberto e descentralizado. Openclaw se conecta como uma Matrix **user**
em qualquer servidor doméstico, então você precisa de uma conta Matrix para o bot. Uma vez que está logado, você pode DM
o bot diretamente ou convidá-lo para salas (Matrix "grupos"). Beeper também é uma opção de cliente válida,
mas exige que a E2EE seja activada.

Estado: suportado através de plugin (@ vector-im/matrix-bot-sdk). Mensagens diretas, salas, fios, mídia, reações,
enquetes (enviar + enquete-iniciar como texto), localização e E2EE (com suporte a criptografia).

## Plugin necessário

Matrix ships como um plugin e não é empacotado com o núcleo instalar.

Instalar via CLI (registro npm):

```bash
openclaw plugins install @openclaw/matrix
```

Obtenção local (quando em execução a partir de um git repo):

```bash
openclaw plugins install ./extensions/matrix
```

Se você escolher Matrix durante a configuração/onboarding e um git checkout for detectado,
OpenClaw irá oferecer o caminho de instalação local automaticamente.

Detalhes: [Plugins]/plugin

Configuração

1. Instale o plugin Matrix:
- A partir de npm:`openclaw plugins install @openclaw/matrix`- De um checkout local:`openclaw plugins install ./extensions/matrix`2. Crie uma conta Matrix em um servidor home:
- Procurar opções de hospedagem em [https://matrix.org/ecosystem/hosting/]https://matrix.org/ecosystem/hosting/
- Ou ser o anfitrião.
3. Obter um token de acesso para a conta bot:
- Use a API de login Matrix com`curl`em seu servidor doméstico:

   ```bash
   curl --request POST \
     --url https://matrix.example.org/_matrix/client/v3/login \
     --header 'Content-Type: application/json' \
     --data '{
     "type": "m.login.password",
     "identifier": {
       "type": "m.id.user",
       "user": "your-user-name"
     },
     "password": "your-password"
   }'
   ```

- Substituir`matrix.example.org`por seu URL homeserver.
- Ou definir`channels.matrix.userId`+`channels.matrix.password`: OpenClaw chama o mesmo
endpoint de login, armazena o token de acesso em`~/.openclaw/credentials/matrix/credentials.json`,
e reutiliza-o no próximo início.

4. Configurar credenciais:
- Env:`MATRIX_HOMESERVER`,`MATRIX_ACCESS_TOKEN`(ou`MATRIX_USER_ID`+`MATRIX_PASSWORD`
- Ou configuração:`channels.matrix.*`- Se ambos estiverem definidos, a configuração tem precedência.
- Com token de acesso: ID do usuário é obtido automaticamente via`/whoami`.
- Quando estabelecido, o`channels.matrix.userId`deve ser o ID Matrix completo (exemplo:`@bot:example.org`.
5. Reinicie o gateway (ou termine a integração).
6. Iniciar um DM com o bot ou convidá-lo para um quarto de qualquer cliente Matrix
(Elemento, Beeper, etc.; ver https://matrix.org/ecosystem/clients/). Beeper requer E2EE,
Por isso, defina`channels.matrix.encryption: true`e verifique o dispositivo.

Configuração mínima (toque de acesso, ID de usuário automaticamente:

```json5
{
  channels: {
    matrix: {
      enabled: true,
      homeserver: "https://matrix.example.org",
      accessToken: "syt_***",
      dm: { policy: "pairing" },
    },
  },
}
```

Configuração do E2EE (end to end encriptation enabled):

```json5
{
  channels: {
    matrix: {
      enabled: true,
      homeserver: "https://matrix.example.org",
      accessToken: "syt_***",
      encryption: true,
      dm: { policy: "pairing" },
    },
  },
}
```

## Encriptação (E2EE)

A criptografia de ponta a ponta é suportada** através do SDK criptográfico Rust.

Activar com`channels.matrix.encryption: true`:

- Se o módulo criptográfico for carregado, as salas criptografadas são descriptografadas automaticamente.
Os meios de comunicação estão encriptados ao enviar para salas encriptadas.
- Na primeira conexão, OpenClaw solicita verificação do dispositivo de suas outras sessões.
- Verifique o dispositivo em outro cliente Matrix (Elemento, etc.) para permitir o compartilhamento de chaves.
- Se o módulo cripto não puder ser carregado, o E2EE está desativado e as salas criptografadas não serão descriptografadas;
O Open Claw regista um aviso.
- Se você vir erros no módulo de criptografia em falta (por exemplo,`@matrix-org/matrix-sdk-crypto-nodejs-*`,
permitir scripts de compilação para`@matrix-org/matrix-sdk-crypto-nodejs`e executar`pnpm rebuild @matrix-org/matrix-sdk-crypto-nodejs`ou obter o binário com`node node_modules/@matrix-org/matrix-sdk-crypto-nodejs/download-lib.js`.

O estado de criptografia é armazenado por conta + token de acesso`~/.openclaw/matrix/accounts/<account>/<homeserver>__<user>/<token-hash>/crypto/`(Base de dados SQLite). O Sync vive ao lado dele no`bot-storage.json`.
Se o token de acesso (dispositivo) mudar, uma nova loja é criada e o bot deve ser
Verificado para salas criptografadas.

** Verificação do dispositivo:**
Quando o E2EE estiver habilitado, o bot solicitará verificação de suas outras sessões na inicialização.
Abrir elemento (ou outro cliente) e aprovar o pedido de verificação para estabelecer confiança.
Uma vez verificado, o bot pode descriptografar mensagens em salas criptografadas.

## Modelo de rota

- Respostas voltam sempre à Matrix.
- DMs compartilham a sessão principal do agente; salas mapeiam as sessões em grupo.

## Controle de acesso (DMs)

- Predefinição:`channels.matrix.dm.policy = "pairing"`. Os remetentes desconhecidos recebem um código de pareamento.
- Aprovar via:
-`openclaw pairing list matrix`-`openclaw pairing approve matrix <CODE>`- DM públicos:`channels.matrix.dm.policy="open"`mais`channels.matrix.dm.allowFrom=["*"]`.
-`channels.matrix.dm.allowFrom`aceita IDs de usuário ou nomes de exibição. O assistente resolve os nomes de exibição para IDs de usuário quando a pesquisa de diretório está disponível.

## Quartos (grupos)

- Predefinição:`channels.matrix.groupPolicy = "allowlist"`(perioditado). Use`channels.defaults.groupPolicy`para substituir o padrão quando desativado.
- Allowlist quartos com`channels.matrix.groups`( IDs de quarto, apelidos, ou nomes):

```json5
{
  channels: {
    matrix: {
      groupPolicy: "allowlist",
      groups: {
        "!roomId:example.org": { allow: true },
        "#alias:example.org": { allow: true },
      },
      groupAllowFrom: ["@owner:example.org"],
    },
  },
}
```

-`requireMention: false`permite responder automaticamente naquela sala.
-`groups."*"`pode definir padrões para mencionar gating em todos os quartos.
-`groupAllowFrom`restringe que remetentes podem ativar o bot em salas (opcional).
- Por quarto`users`allowlists pode restringir ainda mais os remetentes dentro de uma sala específica.
- O assistente configure prompts para allowlists de sala (IDs de sala, apelidos, ou nomes) e resolve nomes quando possível.
- Na inicialização, o OpenClaw resolve nomes de sala/usuário em listas de permissões para IDs e registra o mapeamento; entradas não resolvidas são mantidas como digitadas.
- Os convites são conectados automaticamente por padrão; controle com`channels.matrix.autoJoin`e`channels.matrix.autoJoinAllowlist`.
- Para permitir ** nenhum quarto**, definir`channels.matrix.groupPolicy: "disabled"`(ou manter uma lista de permissão vazia).
- Chave de legado:`channels.matrix.rooms`(da mesma forma que`groups`.

## Linhas

- Responder threading é suportado.
-`channels.matrix.threadReplies`controla se as respostas permanecem em linhas:
-`off`,`inbound`(padrão),`always`-`channels.matrix.replyToMode`controla a resposta aos metadados ao não responder em um tópico:
-`off`(default),`first`,`all`

## Capacidades

Característica
----------------- ----------------------------------------------------------------------------------------------------
Mensagens diretas Suportadas
Quartos Suportados
• Threads
* Media * Suportado *
• E2EE • Suportado (módulo de criptografia necessário)
Reacções Suportadas (enviar/ler através de ferramentas)
• Pesquisadores • Enviar suporte; inícios de pesquisa são convertidos em texto (respostas/fim ignorados)
Localização Suportada (Geo URI; altitude ignorada)
Comandos nativos

## Referência de configuração (Matrix)

Configuração completa: [Configuração]/gateway/configuration

Opções do fornecedor:

-`channels.matrix.enabled`: activar/desactivar a inicialização do canal.
- URL`channels.matrix.homeserver`: servidor doméstico.
-`channels.matrix.userId`: Matrix ID de usuário (opcional com token de acesso).
-`channels.matrix.accessToken`: token de acesso.
-`channels.matrix.password`: senha para login (token armazenado).
-`channels.matrix.deviceName`: nome do dispositivo.
-`channels.matrix.encryption`: habilitar E2EE (padrão: false).
Limite inicial de sincronização.
-`channels.matrix.threadReplies`:`off | inbound | always`(por omissão: entrada).
-`channels.matrix.homeserver`0: tamanho de pedaço de texto de saída (chars).
-`channels.matrix.homeserver`1:`channels.matrix.homeserver`2 (padrão) ou`channels.matrix.homeserver`3 para dividir em linhas em branco (limites de parágrafos) antes do corte de comprimento.
-`channels.matrix.homeserver`4:`channels.matrix.homeserver`5 (por omissão: emparelhamento).
-`channels.matrix.homeserver`6: DM allowlist (IDs de usuário ou nomes de exibição).`channels.matrix.homeserver`7 exige`channels.matrix.homeserver`8. O assistente resolve nomes para IDs quando possível.
-`channels.matrix.homeserver`9:`channels.matrix.userId`0 (default: allowlist).
-`channels.matrix.userId`1: remetentes autorizados para mensagens de grupo.
-`channels.matrix.userId`2: regras de allowlist de força para DMs + salas.
-`channels.matrix.userId`3: grupo allowlist + mapa de configurações por sala.
-`channels.matrix.userId`4: lista de permissões/configuração do grupo legado.
-`channels.matrix.userId`5: resposta ao modo para threads/tags.
-`channels.matrix.userId`6: capa de suporte de entrada/saída (MB).
-`channels.matrix.userId`7: manipulação de convites `channels.matrix.userId`8, padrão: sempre).
-`channels.matrix.userId`9: IDs/aliases de quarto permitidos para se juntarem automaticamente.
-`channels.matrix.accessToken`0: gating de ferramentas por ação (reacções/mensagens/pins/memberInfo/canalInfo).
