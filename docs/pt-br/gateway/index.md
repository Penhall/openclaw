---
summary: "Runbook for the Gateway service, lifecycle, and operations"
read_when:
  - Running or debugging the gateway process
---

# Manual de serviço de Gateway

Última atualização: 2025-12-09

# # O que é

- O processo de sempre que é dono da ligação Baileys/Telegrama e do plano de controlo/evento.
- Substitui o comando legado <<CODE0>>>. Ponto de entrada CLI: <<CODE1>>>>.
- Corre até parar; sai não-zero em erros fatais para que o supervisor reiniciá-lo.

# # Como correr (local)

```bash
openclaw gateway --port 18789
# for full debug/trace logs in stdio:
openclaw gateway --port 18789 --verbose
# if the port is busy, terminate listeners then start:
openclaw gateway --force
# dev loop (auto-reload on TS changes):
pnpm gateway:watch
```

- Relógios de recarga a quente de configuração <<CODE0>> (ou <<CODE1>>>).
- Modo padrão: <<CODE2>>> (alterações seguras de aplicação quente, reiniciar em crítico).
- A recarga quente usa o reinício do processo via **SIGUSR1** quando necessário.
- Desactivar com <<CODE3>>>.
- Plano de controlo Binds WebSocket para <<CODE4>> (padrão 18789).
- A mesma porta também serve HTTP (controlar UI, ganchos, A2UI). Multiplex de porta única.
- OpenAI Chat Completions (HTTP): [<<<CODE5>>>](<<LINK0>>>>).
- OpenResponses (HTTP): [<<<CODE6>>>](<HTML8>>>>>>).
- Ferramentas Invocar (HTTP): [<<<CODE7>>>](<<LINK2>>>>).
- Inicia um servidor de arquivos Canvas por padrão em <<CODE8>> (padrão <<CODE9>>), servindo <<CODE10>> de <<CODE11>>. Desactivar com <<CODE12>> ou <<CODE13>>>.
- Logs para stdout; use launched/systemd para mantê-lo vivo e girar logs.
- Passe <<CODE14>> para registro de depuração de espelhos (shakes, req/res, eventos) do arquivo de registro para stdio quando solução de problemas.
- <<CODE15>> usa <<CODE16>> para encontrar ouvintes na porta escolhida, envia o SIGTERM, registra o que ele matou, então inicia o gateway (falha rapidamente se <<CODE17>> estiver faltando).
- Se você correr sob um supervisor (leanchd/systemd/mac app child-process mode), uma parada/reiniciação normalmente envia **SIGTERM**; construções mais antigas podem aparecer como <<CODE18>> <<CODE19>> código de saída **143** (SIGTERM), que é um desligamento normal, não um acidente.
- ** SIGUSR1** desencadeia um reinício em processo quando autorizado (aplicação/atualização da ferramenta de porta/configuração ou habilita <<CODE20>> para reinicialização manual).
- A autorização do Gateway é exigida por omissão: definida <<CODE21>> (ou <<CODE22>>>) ou <<CODE23>>. Os clientes devem enviar <<CODE24>> a menos que usem a identidade Tailscale Serve.
- O assistente agora gera um token por padrão, mesmo em loopback.
- Precedência da porta: <<CODE25>> > <<CODE26> > <<CODE27>> > padrão <<CODE28>>>.

# # Acesso remoto

- Tailscale/VPN preferido; caso contrário túnel SSH:
  ```bash
  ssh -N -L 18789:127.0.0.1:18789 user@host
  ```
- Os clientes então se conectam a <<CODE0>> através do túnel.
- Se um token estiver configurado, os clientes devem incluí- lo em <<CODE1>> até mesmo por cima do túnel.

# # Vários gateways (mesma máquina)

Geralmente desnecessário: um Gateway pode servir vários canais de mensagens e agentes. Use vários Gateways apenas para redundância ou isolamento rigoroso (ex: bot de resgate).

Suportado se você isolar estados + config e usar portas únicas. Guia completo: [Gateways múltiplos](<<<LINK0>>>).

Os nomes dos serviços estão cientes do perfil:

- macOS: <<CODE0>> (pode ainda existir legado <<CODE1>>)
- Linux: <<CODE2>>
- Windows: <<CODE3>>>

Instalar metadados está incorporado na configuração do serviço:

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>

Padrão Rescue-Bot: mantenha um segundo Gateway isolado com seu próprio perfil, dir de estado, espaço de trabalho e espaçamento de porta base. Guia completo: [Guia de resgate-bot] (<<<LINK0>>>).

### Perfil do Dev (<<CODE0>>)

Caminho rápido: execute uma instância dev totalmente isolada (config/state/workspace) sem tocar na sua configuração primária.

```bash
openclaw --dev setup
openclaw --dev gateway --allow-unconfigured
# then target the dev instance:
openclaw --dev status
openclaw --dev health
```

Por omissão (pode ser substituído através do env/flags/config):

- <<CODE0>>
- <<CODE1>>
- <<CODE2>> (Gateway WS + HTTP)
- porta de serviço de controlo do navegador = <<CODE3>> (derivada: <<CODE4>>, loopback apenas)
- <<CODE5> (derivado: <<CODE6>>)
- <<CODE7> o padrão torna-se <<CODE8> quando executa <<CODE9>>/<HTML10>> <<CODE11>.

Portas derivadas (regras de polegar):

- Porta base = <<CODE0>> (ou <<CODE1>> / <HTML2>>>>)
- porta de serviço de controle do navegador = base + 2 (apenas loopback)
- <<CODE3> (ou <<CODE4>>/ sobreposição de configuração)
- Perfil de navegador Portas CDP auto-alocar de <<CODE5>> (persistido por perfil).

Lista de verificação por instância:

- único <<CODE0>>
- único <<CODE1>>
- único <<CODE2>>
- único <<CODE3>>
- números WhatsApp separados (se usar WA)

Instalação do serviço por perfil:

```bash
openclaw --profile main gateway install
openclaw --profile rescue gateway install
```

Exemplo:

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/a.json OPENCLAW_STATE_DIR=~/.openclaw-a openclaw gateway --port 19001
OPENCLAW_CONFIG_PATH=~/.openclaw/b.json OPENCLAW_STATE_DIR=~/.openclaw-b openclaw gateway --port 19002
```

# # Protocolo (visão do operador)

- Documentos completos: [Protocolo Gateway] (<<<LINK0>>) e [Protocolo Ponte (legacia)](<<LINK1>>).
- Primeiro quadro obrigatório do cliente: <<CODE0>>>.
- Respostas do gateway <<CODE1>> (ou <<CODE2>> com um erro, então fecha).
- Depois do aperto de mão:
- Pedidos: <<CODE3>> → <<CODE4>>
- Eventos: <<CODE5>>>
- Entradas de presença estruturadas: <<CODE6>> (para clientes WS, <<CODE7>> vem de <<CODE8>>).
- <<CODE9> as respostas são duas fases: primeiro <<CODE10>> ack <<CODE11>>, em seguida, uma final <<CODE12>> <<CODE13>> após o fim da execução; saída transmitida chega como <<CODE14>>>.

# # Métodos (set inicial)

- <<CODE0>> — snapshot de saúde completa (a mesma forma que <<CODE1>>>).
- <<CODE2>> — resumo curto.
- <<CODE3>> — lista de presenças actuais.
- <<CODE4>> — publicar uma nota de presença/sistema (estruturada).
- <<CODE5>> — envie uma mensagem através dos canais activos.
- <<CODE6>> — execute uma volta de agente (streams events back on mesma conexão).
- <<CODE7>> — lista emparelhada + nós actualmente ligados (inclui <<CODE8>>, <<CODE9>>, <<CODE10>>, <<CODE11>, <<CODE12>>, e anunciado <<CODE13>>).
- <<CODE14>> — descrever um nó (capacidades + comandos suportados <<CODE15>>; funciona para nós pareados e para nós não pareados atualmente conectados).
- <<CODE16>> — invocar um comando num nó (por exemplo, <<CODE17>>>, <<CODE18>>>).
- <<CODE19>> — ciclo de vida de pareamento (<<CODE20>>, <<CODE21>>, <<CODE22>>, <<CODE23>>, <<CODE24>>).

Ver também: [Presência](<<<LINK0>>>) para a forma como a presença é produzida/desidratada e por que um estável <<CODE0> importa.

# # Eventos

- <<CODE0>> — eventos de ferramentas/saídas a partir da execução do agente (seq-tagged).
- <<CODE1>> — atualizações de presença (deltas com statusVersion) empurradas para todos os clientes conectados.
- <<CODE2>> — manutenção periódica/sem operação para confirmar a vida.
- <<CODE3>> – O Gateway está a sair; a carga útil inclui <<CODE4>>> e opcional <<CODE5>>. Os clientes devem voltar a ligar-se.

# # Integração WebChat

- WebChat é uma UI SwiftUI nativa que fala diretamente com o Gateway WebSocket para história, envia, aborta e eventos.
- O uso remoto passa pelo mesmo túnel SSH/Tailscale; se um token de gateway estiver configurado, o cliente o inclui durante <<CODE0>>.
- app macOS se conecta através de um único WS (conexão compartilhada); ele hidrata a presença do instantâneo inicial e escuta para <<CODE1> eventos para atualizar a UI.

# # Datilografia e validação

- O servidor valida todos os quadros de entrada com AJV contra o esquema JSON emitido a partir das definições de protocolo.
- Clientes (TS/Swift) consomem tipos gerados (TS diretamente; Swift através do gerador do repo).
- As definições de protocolo são a fonte da verdade; regenerar esquema/modelos com:
- <<CODE0>>
- <<CODE1>>

# # Instantâneo de conexão

- <<CODE0> inclui <<CODE1>> com <<CODE2>>, <<CODE3>>, <<CODE4>>, e <<CODE5>> mais <<CODE6>> para que os clientes possam renderizar imediatamente sem pedidos adicionais.
- <<CODE7>>/<<CODE8>> permanecer disponível para atualização manual, mas não são necessários no momento da conexão.

# # Códigos de erro (forma res.error)

- Os erros utilizam <<CODE0>>>.
- Códigos normalizados:
- <<CODE1>> — WhatsApp não autenticado.
- <<CODE2>> — o agente não respondeu dentro do prazo configurado.
- <<CODE3>> – a validação esquema/param falhou.
- <<CODE4> O Gateway está a desligar-se ou uma dependência não está disponível.

# # Comportamento vivo

- <<CODE0>> os eventos (ou WS ping/pong) são emitidos periodicamente para que os clientes saibam que o Gateway está vivo mesmo quando não ocorre tráfego.
- Os avisos de envio/agente permanecem respostas separadas; não sobrecarregue os tiques para os envios.

# # Repetir / lacunas

- Os eventos não são repetidos. Os clientes detectam lacunas seguintes e devem atualizar (<<<CODE0>> + <<CODE1>>>>) antes de continuar. Os clientes WebChat e macOS atualizam automaticamente o gap.

# # Supervisão (exemplo macOS)

- Usar lançado para manter o serviço vivo:
- Programa: caminho para <<CODE0>>
- Argumentos: <<CODE1>>
- KeepAlive: verdade
- StandardOut/Err: caminhos de arquivos ou <<CODE2>>
- Em caso de falha, o lançamento reinicia; o erro fatal deve continuar a sair para que o operador note.
- LaunchAgents são por usuário e requerem uma sessão de login; para configurações sem cabeça usar um LaunchDaemon personalizado (não enviado).
- <<CODE3> escreve <<CODE4>>
(ou <<CODE5>>; legado <<CODE6>> é limpo).
- <<CODE7>Audita a configuração do LaunchAgent e pode atualizá-la para os padrões atuais.

# # Gestão de serviços de Gateway (CLI)

Use o CLI Gateway para instalar/start/stop/reirt/status:

```bash
openclaw gateway status
openclaw gateway install
openclaw gateway stop
openclaw gateway restart
openclaw logs --follow
```

Notas:

- <<CODE0>> sonda o PCR Gateway por padrão usando a porta/configuração resolvida do serviço (sobreposta com <<CODE1>>).
- <<CODE2> adiciona scans de nível de sistema (LaunchDaemons/unidades de sistema).
- <<CODE3> pula a sonda RPC (útil quando a rede está desligada).
- <<CODE4> é estável para scripts.
- <<CODE5> relatórios **supervisor runtime** (lançado/sistema em execução) separadamente de **RPC alcançábility** (WS connect + status RPC).
- <<CODE6>> imprime caminho de configuração + alvo da sonda para evitar confusão “localhost vs LAN bind” e descompassos de perfil.
- <<CODE7>> inclui a última linha de erro de gateway quando o serviço parece em execução, mas a porta está fechada.
- <<CODE8> acompanha o registo do ficheiro Gateway via RPC (não é necessário nenhum manual <<CODE9>>/<<CODE10>>).
- Se outros serviços semelhantes a gateway forem detectados, o CLI avisa a menos que sejam serviços de perfil OpenClaw.
Ainda recomendamos **um gateway por máquina** para a maioria das configurações; use perfis/ports isolados para redundância ou um bot de resgate. Ver [Multiplos gateways](<<<LINK0>>>).
- Limpeza: <<CODE11>> (serviço atual) e <<CODE12>> (migrações de legado).
- <<CODE13> é um no-op quando já instalado; use <<CODE14>> para reinstalar (alterações de perfil/env/caminho).

Aplicativo Mac agrupado:

- Openclaw.app pode agrupar um relé de gateway baseado em nós e instalar um LaunchAgent por usuário rotulado
<<CODE0>> (ou <<CODE1>>>; os rótulos legados <<CODE2>> ainda descarregam de forma limpa).
- Para o parar de forma limpa, utilize <<CODE3>> (ou <<CODE4>>>).
- Para reiniciar, utilize <<CODE5>> (ou <<CODE6>>>).
- <<CODE7> só funciona se o LaunchAgent estiver instalado; caso contrário use <<CODE8>> Primeiro.
- Substituir o rótulo por <<CODE9>> ao executar um perfil nomeado.

# # Supervisão (unidade de usuário sistema)

OpenClaw instala um serviço de usuário ** systemd** por padrão no Linux/WSL2. Nós
recomendar serviços de usuário para máquinas monousuárias (simplesr env, per-usuário config).
Use um serviço de sistema ** para servidores multi-usuários ou sempre- em (sem demora
supervisão obrigatória e partilhada).

<<CODE0> escreve a unidade de usuário. <<CODE1>Auditorias
unidade e pode atualizá-lo para corresponder aos padrões recomendados atualmente.

Criar <<CODE0>>:

```
[Unit]
Description=OpenClaw Gateway (profile: <profile>, v<version>)
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/openclaw gateway --port 18789
Restart=always
RestartSec=5
Environment=OPENCLAW_GATEWAY_TOKEN=
WorkingDirectory=/home/youruser

[Install]
WantedBy=default.target
```

Activar a permanência (necessária para que o serviço do utilizador sobreviva ao logout/idle):

```
sudo loginctl enable-linger youruser
```

Onboarding executa isso no Linux/WSL2 (pode solicitar sudo; escreve <<CODE0>>).
Em seguida, habilite o serviço:

```
systemctl --user enable --now openclaw-gateway[-<profile>].service
```

** Alternativo (serviço do sistema)** - para servidores sempre-on ou multi-usuários, você pode
instalar uma unidade systemd ** system** em vez de uma unidade de usuário (sem necessidade de demora).
Criar <<CODE0>> (copiar a unidade acima,
alternar <<CODE1>>, definir <<CODE2>>> + <<CODE3>>>), em seguida:

```
sudo systemctl daemon-reload
sudo systemctl enable --now openclaw-gateway[-<profile>].service
```

# # Windows (WSL2)

As instalações do Windows devem usar **WSL2** e seguir a seção Linux systemd acima.

# # Controlos operacionais

- Vida: WS aberto e enviar <<CODE0>> → esperar <<CODE1>> com <<CODE2>> (com instantâneo).
- Preparação: chamada <<CODE3>> → espera <<CODE4>>> e um canal ligado em <<CODE5> (quando aplicável).
- Depuração: assinar <<CODE6>>> e <<CODE7>> eventos; garantir <<CODE8>> mostra a idade vinculada/auth; entradas de presença mostram Host Gateway e clientes conectados.

# # Garantias de segurança

- Assumir um Gateway por máquina por padrão; se você executar vários perfis, isole portas/estado e alvo da instância certa.
- Não há recuo para direcionar ligações Baileys; se o Gateway está para baixo, envia falha rapidamente.
- Primeiros quadros não conectados ou JSON malformado são rejeitados e o soquete é fechado.
- Desligamento gracioso: emite <<CODE0> evento antes de fechar; os clientes devem lidar com close + reconectar.

# # Ajudantes de CLI

- <<CODE0>> — solicitar saúde/status sobre o portal WS.
- <<CODE1>> — enviar via Gateway (idempotente para WhatsApp).
- <<CODE2>> — executar uma volta do agente (espera por final por padrão).
- <<CODE3>> — invocador de método bruto para depuração.
- <<CODE4>> – parar/reiniciar o serviço de gateway supervisionado (lançado/systemd).
- Os subcomandos do helper do Gateway assumem um gateway em execução em <<CODE5>>; eles não mais passam automaticamente um.

# # Guia sobre migração

- Retire os usos de <<CODE0>> e a porta de controle TCP legada.
- Atualizar clientes para falar o protocolo WS com conexão obrigatória e presença estruturada.
