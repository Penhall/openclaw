---
summary: "macOS app flow for controlling a remote OpenClaw gateway over SSH"
read_when:
  - Setting up or debugging remote mac control
---

# OpenClaw remoto (macOS - máquina remota)

Este fluxo permite que o aplicativo macOS atue como um controle remoto completo para um gateway OpenClaw rodando em outro host (desktop/servidor). É o recurso ** Remote over SSH** (remote run). Todos os recursos—cheques de saúde, encaminhamento de Voz Wake e Web Chat—reutilize a mesma configuração remota de SSH a partir de  Configurações → Geral .

# # Modos

- ** Local (este Mac)**: Tudo funciona no portátil. Não há SSH envolvido.
- **Remote sobre SSH (padrão)**: Os comandos OpenClaw são executados na máquina remota. A aplicação Mac abre uma ligação SSH com <<CODE0>> mais a sua identidade/chave escolhida e uma porta local.
- ** Sem túnel SSH. O aplicativo mac se conecta diretamente à URL do gateway (por exemplo, via Tailscale Serve ou um proxy reverso HTTPS público).

# # Transportes remotos

O modo remoto suporta dois transportes:

- ** Túnel SSH** (padrão): Usa <<CODE0>> para encaminhar a porta de gateway para localhost. O gateway verá o IP do nó como <<CODE1>> porque o túnel é loopback.
- **Direct (ws/wss)**: Conecta diretamente ao URL do gateway. O gateway vê o verdadeiro IP do cliente.

# # Prereqs no hospedeiro remoto

1. Instalar Node + pnpm e construir/instalar o OpenClaw CLI (<<<CODE0>>).
2. Certifique-se de que <<CODE1> está em PATH para conchas não-interativas (ligação em <<CODE2>> ou <<CODE3> se necessário).
3. Abra o SSH com a autenticação da chave. Recomendamos **Tailscale** IPs para alcance estável off-LAN.

Configuração da aplicação ## macOS

1. Abrir  Configurações → Geral .
2. Em ** OpenClaw corre**, escolha ** Remote sobre SSH** e definir:
- ** Transporte**: ** Túnel SHS** ou ** Direct (ws/wss)**.
- ** Alvo SHSS**: <<CODE0>> (opcional <<CODE1>>>).
- Se o gateway estiver na mesma LAN e anunciar Bonjour, escolha-o da lista descoberta para preencher automaticamente este campo.
- ** URL de Gateway** (apenas directa): <<CODE2>> (ou <<CODE3>> para local/LAN).
- ** Arquivo de identidade** (avançado): caminho para sua chave.
- **Project root** (avançado): caminho de saída remoto usado para comandos.
- ** Caminho CLI** (avançado): caminho opcional para um ponto de entrada/binário <<CODE4> executável (preenchido automaticamente quando anunciado).
3. Toque em **Teste remoto**. O sucesso indica que o remoto <<CODE5> funciona corretamente. Falhas geralmente significam problemas PATH/CLI; saída 127 significa que o CLI não é encontrado remotamente.
4. Verificações de saúde e Web Chat agora será executado através deste túnel SSH automaticamente.

Conversa Web

- ** Túnel SSH**: Web Chat conecta-se ao gateway sobre a porta de controle WebSocket encaminhada (padrão 18789).
- **Direct (ws/wss)**: Web Chat conecta diretamente à URL configurada do gateway.
- Já não existe servidor HTTP WebChat separado.

# # Permissões

- O host remoto precisa das mesmas aprovações TCC locais (Automação, Acessibilidade, Gravação de Tela, Microfone, Reconhecimento de Fala, Notificações). Corre a bordo da máquina para os conceder uma vez.
- Os nós anunciam seu estado de permissão via <<CODE0>>/ <<CODE1>> para que os agentes saibam o que está disponível.

# # Notas de segurança

- Prefere loopback liga-se no host remoto e conectar através de SSH ou Tailscale.
- Se você ligar o Gateway a uma interface não-loopback, exigir token/password auth.
- Ver [Segurança] (<<<LINK0>>) e [Tailscale] (<<LINK1>>).

# # WhatsApp fluxo de login (remote)

- Executar <<CODE0>> ** no host remoto**. Examine o QR com o WhatsApp no seu telefone.
- Refazer o login na máquina se a autorização expirar. O exame de saúde irá ligar problemas à superfície.

# # Resolução de problemas

- ** saída 127 / não encontrado**: <<CODE0>> não está em PATH para shells não-login. Adicione-o a <<CODE1>>, seu shell rc, ou ligação simbólica em <<CODE2>/<<CODE3>.
- ** Sonda de saúde falhou**: verifique a acessibilidade do SSH, PATH, e que Baileys está logado (<<CODE4>>).
- **Web Chat encravado**: confirme que o gateway está rodando no host remoto e a porta encaminhada corresponde à porta WS gateway; a UI requer uma conexão WS saudável.
- **Node IP mostra 127.0.0.1**: esperado com o túnel SSH. Alternar **Transport** para **Direct (ws/wss)** se você quiser que o gateway veja o IP do cliente real.
- **Voice Wake**: frases de gatilho são enviadas automaticamente em modo remoto; nenhum encaminhador separado é necessário.

# # Sons de notificação

Escolha sons por notificação de scripts com <<CODE0>> e <<CODE1>>>, por exemplo:

```bash
openclaw nodes notify --node <id> --title "Ping" --body "Remote gateway ready" --sound Glass
```

Não há mais nenhuma opção global de "som padrão" no aplicativo; os usuários escolhem um som (ou nenhum) por solicitação.
