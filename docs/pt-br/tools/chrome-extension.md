---
summary: "Chrome extension: let OpenClaw drive your existing Chrome tab"
read_when:
  - You want the agent to drive an existing Chrome tab (toolbar button)
  - You need remote Gateway + local browser automation via Tailscale
  - You want to understand the security implications of browser takeover
---

# Extensão do Chrome (relé navegador)

A extensão OpenClaw Chrome permite que o agente controle suas abas ** existentes do Chrome** (sua janela normal do Chrome) em vez de lançar um perfil separado do Chrome gerenciado pelo openclaw.

Anexar/destacar acontece através de um botão ** único da barra de ferramentas Chrome**.

# # O que é (conceito)

Há três partes:

- ** Serviço de controle do navegador** (Gateway ou nó): a API que o agente / ferramenta chama (através do Gateway)
- ** Servidor local de relé** (loopback CDP): pontes entre o servidor de controle e a extensão (`http://127.0.0.1:18792` por padrão)
- ** Extensão Chrome MV3**: liga- se à aba activa utilizando `chrome.debugger` e canaliza as mensagens CDP ao relé

OpenClaw então controla a guia anexada através da superfície normal da ferramenta <<CODE0> (selecionando o perfil certo).

# # Instalar / carregar (não embalado)

1. Instale a extensão para um caminho local estável:

```bash
openclaw browser extension install
```

2. Imprima o caminho do diretório de extensão instalado:

```bash
openclaw browser extension path
```

3. Chrome → `chrome://extensions`

- Activar o “modo de desenvolvimento”
- “Carregar desempacotado” → selecione o diretório impresso acima

4. Pin a extensão.

# # Atualizações (sem passo de compilação)

A extensão é enviada dentro do pacote OpenClaw (npm) como arquivos estáticos. Não há nenhum passo separado “construir”.

Após atualizar o OpenClaw:

- Repetir `openclaw browser extension install` para atualizar os arquivos instalados sob seu diretório de estado OpenClaw.
- Chrome → <<CODE1> → clique em "Recarregar" na extensão.

# # Usar (sem configuração extra)

Naves OpenClaw com um perfil de navegador integrado chamado <<CODE0> que visa o relé de extensão na porta padrão.

Use-o:

- CLI: `openclaw browser --browser-profile chrome tabs`
- Ferramenta agente: `browser` com `profile="chrome"`

Se você quiser um nome diferente ou uma porta de relé diferente, crie seu próprio perfil:

```bash
openclaw browser create-profile \
  --name my-chrome \
  --driver extension \
  --cdp-url http://127.0.0.1:18792 \
  --color "#00AA00"
```

# # Anexar / desconectar (botão da barra de ferramentas)

- Abra a aba que quer que o Openclaw controle.
- Clique no ícone da extensão.
- O distintivo mostra `ON` quando anexado.
- Clique novamente para separar.

# # Que tabulação controla?

- Faz **not** controlar automaticamente “qualquer tabulação que você está olhando”.
- Ele controla **apenas as abas que você anexa explicitamente** clicando no botão da barra de ferramentas.
- Para alternar: abra a outra guia e clique no ícone de extensão.

# # Distintivo + erros comuns

- `ON`: anexado; OpenClaw pode conduzir essa guia.
- <<CODE1>: ligação ao relé local.
- <<CODE2>: relé não acessível (mais comum: servidor de relé do navegador não está rodando nesta máquina).

Se vir <<CODE0>:

- Certifique-se de que o Gateway está executando localmente (configuração padrão), ou execute um host de nós nesta máquina se o Gateway correr em outro lugar.
- Abra a página Opções da extensão; mostra se o relé é acessível.

# # Gateway remoto (use uma máquina de nós)

### Gateway local (mesma máquina do Chrome) - geralmente ** sem passos extras**

Se o Gateway for executado na mesma máquina que o Chrome, ele inicia o serviço de controle do navegador em loopback
e inicia automaticamente o servidor de retransmissão. A extensão fala com o relé local; as chamadas CLI / ferramenta ir para o Gateway.

### Gateway remoto (Gateway corre em outro lugar) - ** execute um host de nós**

Se seu Gateway for executado em outra máquina, inicie um host de nó na máquina que executa o Chrome.
O Gateway irá proxy de ações do navegador para esse nó; a extensão + relé permanecer local para a máquina do navegador.

Se vários nós estiverem conectados, pingue um com `gateway.nodes.browser.node` ou set `gateway.nodes.browser.mode`.

# # Sandboxing (contêineres de ferramentas)

Se a sua sessão de agente for sandbox (`agents.defaults.sandbox.mode != "off"`), a ferramenta `browser` pode ser restrita:

- Por padrão, as sessões sandbox muitas vezes visam o navegador ** sandbox** (`target="sandbox"`), não seu Chrome host.
- A aquisição do relé de extensão do Chrome requer o controle do servidor de controle do navegador **host**.

Opções:

- Fácil: use a extensão de uma sessão/agente** não-sandboxed.
- Ou permitir o controle do navegador host para sessões sandboxed:

```json5
{
  agents: {
    defaults: {
      sandbox: {
        browser: {
          allowHostControl: true,
        },
      },
    },
  },
}
```

Em seguida, garantir que a ferramenta não é negada pela política de ferramentas, e (se necessário) chamada `browser` com `target="host"`.

Depuração: `openclaw sandbox explain`

# # Dicas de acesso remoto

- Mantenha o Gateway e host de nó na mesma tailnet; evite expor portas de relé para LAN ou Internet pública.
- Emparelhar nós intencionalmente; desabilitar roteamento proxy do navegador se você não quiser controle remoto (<<CODE0>).

# # Como funciona o “caminho de extensão”

<<CODE0> imprime o diretório ** instalado no disco contendo os arquivos de extensão.

O CLI intencionalmente não ** imprime um caminho `node_modules`. Execute sempre primeiro <<CODE1> para copiar a extensão para um local estável sob seu diretório de estado OpenClaw.

Se você mover ou excluir esse diretório de instalação, o Chrome marcará a extensão como quebrada até que você o reload de um caminho válido.

# # Implicações de segurança (leia isto)

Isto é poderoso e arriscado. Trate-o como dando o modelo "mãos no seu navegador".

- A extensão utiliza a API do depurador do Chrome (`chrome.debugger`). Quando anexado, o modelo pode:
- clique/tipo/navegar nessa aba
- ler o conteúdo da página
- acessar qualquer sessão de login da aba pode acessar
- ** Isto não é isolado** como o perfil dedicado ao openclaw.
- Se você anexar ao seu perfil/tab driver diário, você está concedendo acesso a esse estado de conta.

Recomendações:

- Prefere um perfil Chrome dedicado (separado de sua navegação pessoal) para uso de relé de extensão.
- Mantenha o Gateway e qualquer nó hosts tailnet-only; confie em Gateway auth + emparelhamento de nó.
- Evite expor portas de retransmissão sobre a LAN (`0.0.0.0`) e evitar Funil (público).

Relacionados:

- Visão geral da ferramenta do navegador: [Browser] (</tools/browser)
- Auditoria de segurança: [Segurança] (</gateway/security)
- Configuração da escala de cauda: [Tailscale] (</gateway/tailscale)
