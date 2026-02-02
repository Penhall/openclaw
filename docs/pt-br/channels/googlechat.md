---
summary: "Google Chat app support status, capabilities, and configuration"
read_when:
  - Working on Google Chat channel features
---

# Google Chat (A API do Chat)

Estado: pronto para DMs + espaços através do Google Chat API webhooks (HTTP somente).

## Montagem rápida (início)

1. Crie um projeto do Google Cloud e habilite a API do Google Chat**.
- Ir para: [Google Chat API Credenciais] https://console.cloud.google.com/apis/api/chat.googleapis.com/credentials
- Habilite a API se ela ainda não estiver habilitada.
2. Criar uma Conta de Serviço**:
- Pressione **Criar Credenciais** > **Conta de Serviço**.
- Diga o que quiser (por exemplo,`openclaw-chat`.
- Deixe as permissões em branco (pressione **Continue **).
- Deixe os principais com acesso em branco (pressione **Feito**).
3. Crie e baixe a chave **JSON**:
- Na lista de contas de serviço, clique na que você acabou de criar.
- Vai para a guia **Keys**.
- Clique em **Adicionar chave** > ** Criar nova chave**.
- Selecione **JSON** e pressione **Criar **.
4. Armazene o arquivo JSON baixado em seu host gateway (por exemplo,`~/.openclaw/googlechat-service-account.json`.
5. Crie um aplicativo de Google Chat na configuração de Chat [Google Cloud Console] https://console.cloud.google.com/apis/api/chat.googleapis.com/hangouts-chat:
- Preencha a informação de aplicação**:
- **Nome da aplicação**: (por exemplo,`OpenClaw`
- ** URL do Avatar**: (por exemplo,`https://openclaw.ai/logo.png`
- **Descrição**: (por exemplo,`Personal AI Assistant`
- Activar ** Características interactivas **.
- Em **Funcionalidade**, verifique **Junte-se a espaços e conversas em grupo**.
- Em **Connection settings**, selecione **HTTP endpoint URL**.
- Sob **Triggers**, selecione **Use um URL de endpoint HTTP comum para todos os gatilhos** e defina-o para o URL público do seu gateway seguido pelo`/googlechat`.
-  Dica: Execute`openclaw status`para encontrar o URL público do seu gateway. 
- Em **Visibilidade**, verifique **Faça esta aplicação de Chat disponível para pessoas e grupos específicos em &lt;Your Domain&gt;**.
- Digite seu endereço de e-mail (por exemplo,`user@example.com` na caixa de texto.
- Clique em **Salvar** na parte inferior.
6. **Ativar o status do aplicativo**:
- Depois de salvar, ** atualizar a página**.
- Procure a seção ** Status do aplicativo** (geralmente perto do topo ou inferior após salvar).
- Mude o status para **Live - disponível para usuários**.
- Clique em **Salvar** novamente.
7. Configure OpenClaw com o caminho da conta de serviço + público webhook:
- Env:`GOOGLE_CHAT_SERVICE_ACCOUNT_FILE=/path/to/service-account.json`- Ou configuração:`channels.googlechat.serviceAccountFile: "/path/to/service-account.json"`.
8. Defina o tipo de público + valor do webhook (conforme sua configuração do aplicativo Chat).
9. Inicie o portal. Google Chat irá POST para o seu caminho webhook.

## Adicionar ao Google Chat

Uma vez que o gateway está em execução e seu e-mail é adicionado à lista de visibilidade:

1. Vá para [Google Chat] https://chat.google.com/.
2. Clique no ícone **+** (plus) ao lado de **Mensagens Diretas**.
3. Na barra de pesquisa (onde normalmente você adiciona pessoas), digite o nome ** App** que você configurou no Console da Google Cloud.
- **Nota**: O bot irá  not  aparecer na lista de navegação "Marketplace" porque é um aplicativo privado. Tem de procurar pelo nome.
4. Selecione seu bot a partir dos resultados.
5. Clique em ** Adicionar** ou ** Chat** para iniciar uma conversa 1:1.
6. Envie "Olá" para ativar o assistente!

## URL público (somente para webhook)

Os webhooks do Google Chat exigem um endpoint público do HTTPS. Por segurança, **exponha apenas o caminho`/googlechat`** para a internet. Mantenha o painel OpenClaw e outros terminais sensíveis em sua rede privada.

Opção A: Funil em escala de cauda (recomendado)

Use Tailscale Serve para o painel privado e Funnel para o caminho público webhook. Isto mantém`/`privado enquanto expondo apenas`/googlechat`.

1. ** Verifique em que endereço seu gateway está vinculado:**

   ```bash
   ss -tlnp | grep 18789
   ```

Note o endereço IP (por exemplo,`127.0.0.1`,`0.0.0.0`, ou o seu IP em escala de cauda como`100.x.x.x`.

2. **Exponha o painel apenas para a tailnet (port 8443):**

   ```bash
   # If bound to localhost (127.0.0.1 or 0.0.0.0):
   tailscale serve --bg --https 8443 http://127.0.0.1:18789

   # If bound to Tailscale IP only (e.g., 100.106.161.80):
   tailscale serve --bg --https 8443 http://100.106.161.80:18789
   ```

3. **Exponha apenas o caminho webhook publicamente:**

   ```bash
   # If bound to localhost (127.0.0.1 or 0.0.0.0):
   tailscale funnel --bg --set-path /googlechat http://127.0.0.1:18789/googlechat

   # If bound to Tailscale IP only (e.g., 100.106.161.80):
   tailscale funnel --bg --set-path /googlechat http://100.106.161.80:18789/googlechat
   ```

4. ** Autorize o nó para o acesso ao funil:**
Se solicitado, visite o URL de autorização mostrado na saída para habilitar o Funnel para este nó na sua política de tailnet.

5. **Verificar a configuração:**
   ```bash
   tailscale serve status
   tailscale funnel status
   ```

Seu URL webhook público será:`https://<node-name>.<tailnet>.ts.net/googlechat`

O seu painel privado fica apenas na rede de caudas:`https://<node-name>.<tailnet>.ts.net:8443/`

Use o URL público (sem`:8443` na configuração do aplicativo Google Chat.

> Nota: Esta configuração persiste através de reinicialização. Para removê-lo mais tarde, execute`tailscale funnel reset`e`tailscale serve reset`.

Opção B: Proxy Reverso (Caddy)

Se você usar um proxy reverso como o Caddy, apenas proxy o caminho específico:

```caddy
your-domain.com {
    reverse_proxy /googlechat* localhost:18789
}
```

Com esta configuração, qualquer pedido ao`your-domain.com/`será ignorado ou devolvido como 404, enquanto o`your-domain.com/googlechat`está em segurança encaminhado para OpenClaw.

Opção C: Túnel Cloudflare

Configure as regras de entrada do seu túnel para apenas rotear o caminho do webhook:

- ** Caminho**:`/googlechat`->`http://localhost:18789/googlechat`- ** Regra padrão**: HTTP 404 (Não Encontrado)

## Como funciona

1. Google Chat envia posts webhook para o gateway. Cada pedido inclui um cabeçalho`Authorization: Bearer <token>`.
2. OpenClaw verifica o token contra o`audienceType`configurado +`audience`:
-`audienceType: "app-url"`→ público é o seu URL HTTPS webhook.
-`audienceType: "project-number"`→ público é o número do projeto Cloud.
3. As mensagens são roteadas pelo espaço:
- Os DM utilizam a chave de sessão`agent:<agentId>:googlechat:dm:<spaceId>`.
- Espaços usam a chave de sessão`agent:<agentId>:googlechat:group:<spaceId>`.
4. Acesso DM é pareamento por padrão. Os remetentes desconhecidos recebem um código de pareamento; aprove com:
-`openclaw pairing approve googlechat <code>`5. Espaços de grupo requerem @-menton por padrão. Use`botUser`se a detecção de menção precisar do nome de usuário do aplicativo.

## Alvos

Utilizar estes identificadores para a entrega e listas de autorizações:

- Mensagens directas:`users/<userId>`ou`users/<email>`(endereços de correio electrónico aceites).
- Espaços:`spaces/<spaceId>`.

## Destaques de configuração

```json5
{
  channels: {
    googlechat: {
      enabled: true,
      serviceAccountFile: "/path/to/service-account.json",
      audienceType: "app-url",
      audience: "https://gateway.example.com/googlechat",
      webhookPath: "/googlechat",
      botUser: "users/1234567890", // optional; helps mention detection
      dm: {
        policy: "pairing",
        allowFrom: ["users/1234567890", "name@example.com"],
      },
      groupPolicy: "allowlist",
      groups: {
        "spaces/AAAA": {
          allow: true,
          requireMention: true,
          users: ["users/1234567890"],
          systemPrompt: "Short answers only.",
        },
      },
      actions: { reactions: true },
      typingIndicator: "message",
      mediaMaxMb: 20,
    },
  },
}
```

Notas:

- Credenciais de conta de serviço também podem ser passados em linha com`serviceAccount`(cadeia JSON).
- O caminho padrão do webhook é`/googlechat`se`webhookPath`não estiver definido.
- As reacções estão disponíveis através da ferramenta`reactions`e`channels action`quando o`actions.reactions`estiver activado.
-`typingIndicator`apoia`none`,`message`(por omissão) e`reaction`(reacção requer o utilizador OAuth).
- Os anexos são baixados através da API do Chat e armazenados no pipeline de mídia (tamanho capped by`/googlechat`0).

## Resolução de problemas

## 405 Método não permitido

Se o Google Cloud Logs Explorer mostrar erros como:

```
status code: 405, reason phrase: HTTP error response: HTTP/1.1 405 Method Not Allowed
```

Isto significa que o webhook não está registado. Causas comuns:

1. **Canal não configurado**: A seção`channels.googlechat`está faltando em sua configuração. Verificar com:

   ```bash
   openclaw config get channels.googlechat
   ```

Se ele retornar "O caminho do Config não foi encontrado", adicione a configuração (veja #config-highlights.

2. **Plugin não habilitado**: Verificar o estado do plugin:

   ```bash
   openclaw plugins list | grep googlechat
   ```

Se mostrar "desactivado", adicione`plugins.entries.googlechat.enabled: true`à sua configuração.

3. **Gateway não reiniciado**: Após adicionar a configuração, reinicie o gateway:
   ```bash
   openclaw gateway restart
   ```

Verificar se o canal está em execução:

```bash
openclaw channels status
# Should show: Google Chat default: enabled, configured, ...
```

### Outras questões

- Verifique`openclaw channels status --probe`para erros de autenticação ou falta de configuração do público.
- Se não chegarem mensagens, confirme a URL do Webhook do aplicativo Chat + assinaturas de eventos.
- Se mencionar as respostas dos blocos de gating, defina`botUser`para o nome do recurso de usuário do aplicativo e verifique`requireMention`.
- Use`openclaw logs --follow`enquanto envia uma mensagem de teste para ver se os pedidos chegam ao gateway.

Documentos relacionados:

- [Configuração do portal] /gateway/configuration
- [Segurança] /gateway/security
/tools/reactions
