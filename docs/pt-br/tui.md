---
summary: "Terminal UI (TUI): connect to the Gateway from any machine"
read_when:
  - You want a beginner-friendly walkthrough of the TUI
  - You need the complete list of TUI features, commands, and shortcuts
---

# TUI (UI Terminal)

# # Começo rápido

1. Inicie o portal.

```bash
openclaw gateway
```

2. Abra o TUI.

```bash
openclaw tui
```

3. Digite uma mensagem e pressione Enter.

Porta remota:

```bash
openclaw tui --url ws://<host>:<port> --token <gateway-token>
```

Use <<CODE0>> se o seu Gateway usar senha.

# # O que vês

- Cabeçalho: URL de conexão, agente atual, sessão atual.
- Chat log: mensagens do usuário, respostas do assistente, avisos do sistema, cartões de ferramentas.
- Linha de estado: estado de ligação/run (ligar, executar, transmitir, inactivo, erro).
- Rodapé: estado de conexão + agente + sessão + modelo + think/verbose/raciocing + contagem de tokens + entrega.
- Entrada: editor de texto com autocompletar.

# # Modelo mental: agentes + sessões

- Os agentes são lesmas únicas (por exemplo, <<CODE0>>>, <<CODE1>>>). O portal expõe a lista.
- As sessões pertencem ao agente actual.
- Chaves de sessão são armazenadas como <<CODE2>>>.
- Se escrever <<CODE3>>, o TUI expande-o para <<CODE4>>.
- Se você digitar <<CODE5>>, você muda para aquela sessão do agente explicitamente.
- Âmbito da sessão:
- <<CODE6>> (padrão): cada agente tem muitas sessões.
- <<CODE7>>: o TUI usa sempre a sessão <<CODE8>> (o coletor pode estar vazio).
- O agente atual + sessão são sempre visíveis no rodapé.

# # Envio + entrega

- As mensagens são enviadas para o Gateway; a entrega aos provedores está desligada por padrão.
- Ligar a entrega:
- <<CODE0>>
- ou o painel de ajustes
- ou iniciar com <<CODE1>>>

# # Catadores + sobreposições

- Selector de modelos: listar modelos disponíveis e definir o cancelamento da sessão.
- Escolha um agente diferente.
- Selector de sessão: mostra apenas sessões para o agente atual.
- Configurações: alternar entrega, expansão de saída da ferramenta e visibilidade de pensamento.

# # Teclado atalhos

- Digite: enviar mensagem
- Esc: abortar execução ativa
- Ctrl+C: limpar a entrada (premir duas vezes para sair)
- Ctrl+D: sair
- Ctrl+L: escolhedor de modelos
- Ctrl+G: selecionador de agentes
- Selector de sessão Ctrl+P
- Ctrl+O: comutar a expansão da saída da ferramenta
- Ctrl+T: comutar a visibilidade do pensamento (recarrega o histórico)

# # Comandos de corte

Núcleo:

- <<CODE0>>
- <<CODE1>>
- <<CODE2> (ou <<CODE3>>)
- <<CODE4> (ou <<CODE5>>)
- <<CODE6> (ou <<CODE7>>)

Controles de sessão:

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>
- <<CODE3>>
- <<CODE4> (também conhecido por <<CODE5>)
- <<CODE6>>
- <<CODE7>>

Ciclo de vida da sessão:

- <<CODE0>> ou <<CODE1>> (repor a sessão)
- <<CODE2> (abortar a execução activa)
- <<CODE3>>
- <<CODE4>>

Outros comandos de barra Gateway (por exemplo, <<CODE0>>) são encaminhados para o Gateway e mostrados como saída do sistema. Ver [Comandos Slash] (<<<LINK0>>>).

# # Comandos de shell locais

- Prefixe uma linha com <<CODE0>> para executar um comando de shell local na máquina TUI.
- O TUI pede uma vez por sessão para permitir a execução local; o declínio mantém <<CODE1> desabilitado para a sessão.
- Os comandos são executados em um shell fresco, não-interativo no diretório de trabalho TUI (sem persistente <<CODE2>/env).
- Um solitário <<CODE3>> é enviado como uma mensagem normal; os espaços principais não disparam o executivo local.

# # Saída da ferramenta

- As chamadas de ferramenta mostram como cartões com args + resultados.
- Ctrl+ O alterna entre as vistas colapsadas/expandidas.
- Enquanto as ferramentas são executadas, atualizações parciais passam para o mesmo cartão.

# # História + transmissão

- Ao conectar, o TUI carrega o histórico mais recente (padrão 200 mensagens).
- A actualizar as respostas até à finalização.
- O TUI também ouve eventos de ferramentas de agentes para cartões de ferramentas mais ricos.

# # Detalhes da conexão

- O TUI registra com o Gateway como <<CODE0>>.
- Reconectas mostram uma mensagem do sistema; as lacunas de eventos estão emergidas no log.

# # Opções

- <<CODE0>>: URL do Gateway WebSocket (por omissão para configurar ou <<CODE1>>)
- <<CODE2>>: Token do portal (se necessário)
- <<CODE3>>: Senha do gateway (se necessário)
- <<CODE4>>: Chave de sessão (padrão: <<CODE5>>, ou <<CODE6>> quando o escopo é global)
- <<CODE7>>: Forneça respostas de assistente ao provedor (off padrão)
- <<CODE8>>: Substituir o nível de pensamento para envios
- <<CODE9>>: Tempo limite do agente em ms (por omissão <<CODE10>>>)

# # Resolução de problemas

Sem saída após enviar uma mensagem:

- Executar <<CODE0>> na TUI para confirmar que o Gateway está conectado e ocioso/ocupado.
- Verifique os registos do portal: <<CODE1>>>.
- Confirmar que o agente pode ser executado: <<CODE2>>> e <<CODE3>>>>.
- Se esperar mensagens num canal de chat, habilite a entrega (<<<CODE4>> ou <<CODE5>>>).
- <<CODE6>>: Entradas do histórico a carregar (padrão 200)

# # Resolução de problemas

- <<CODE0>>: garantir que o Gateway está a funcionar e que o seu <<CODE1> está correcto.
- Nenhum agente no catador: check <<CODE2>> e sua configuração de roteamento.
- Selector de sessão vazio: você pode estar no escopo global ou ainda não ter sessões.
