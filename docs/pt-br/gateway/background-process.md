---
summary: "Background exec execution and process management"
read_when:
  - Adding or modifying background exec behavior
  - Debugging long-running exec tasks
---

# Fundo Exec + Ferramenta de Processo

OpenClaw executa comandos shell através da ferramenta <<CODE0>> e mantém tarefas de longa duração na memória. A ferramenta <<CODE1> gerencia essas sessões de fundo.

## ferramenta executiva

Parâmetros chave:

- <<CODE0> (necessário)
- <<CODE1> (padrão 10000): auto- background após este atraso
- <<CODE2> (bool): fundo imediatamente
- <<CODE3>> (segundos, padrão 1800): matar o processo após este tempo limite
- <<CODE4> (bool): correr na máquina se o modo elevado estiver activado/permitido
- Precisas de um TTY verdadeiro? Definir <<CODE5>>>.
- <<CODE6>>, <<CODE7>>>

Comportamento:

- O primeiro plano executa a saída de retorno diretamente.
- Quando em segundo plano (explicativo ou tempo- limite), a ferramenta retorna <<CODE0>> + <<CODE1>>> e uma cauda curta.
- A saída é mantida em memória até que a sessão seja pesquisada ou limpa.
- Se a ferramenta <<CODE2> for proibida, <<CODE3>> Funciona síncrona e ignora <<CODE4>>/<<CODE5>>.

# # Processo infantil em ponte

Ao gerar processos infantis de longa duração fora das ferramentas de execução/processo (por exemplo, respawns CLI ou ajudantes de gateway), anexe o auxiliar de ponte de processo-criança para que os sinais de terminação sejam enviados e os ouvintes sejam separados na saída/erro. Isso evita processos órfãos em systemd e mantém o comportamento de desligamento consistente entre plataformas.

O ambiente substitui- se:

- <<CODE0>>: rendimento por omissão (ms)
- <<CODE1>>: tampa de saída em memória (chars)
- <<CODE2>>: limite de stdout/stderr pendente por fluxo (chars)
- <<CODE3>>: TTL para sessões terminadas (ms, limitada a 1m-3h)

Configuração (preferido):

- <<CODE0> (padrão 10000)
- <<CODE1> (padrão 1800)
- <<CODE2> (padrão 1800000)
- <<CODE3>> (padrão true): coloque um evento do sistema + pedido de batimento cardíaco quando um executivo de fundo sair.

## ferramenta de processo

Acções:

- <<CODE0>>: execução + sessões terminadas
- <<CODE1>>: dreno de nova saída para uma sessão (também informa o estado de saída)
- <<CODE2>>: ler a saída agregada (suporta <<CODE3>>> + <<CODE4>>)
- <<CODE5>: enviar stdin (<<CODE6>>, opcional <<CODE7>>)
- <<CODE8>: terminar uma sessão de fundo
- <<CODE9>: remover uma sessão terminada da memória
- <<CODE10>>: matar se estiver em execução, caso contrário, limpar se terminar

Notas:

- Apenas as sessões de fundo são listadas/persistidas na memória.
- Sessões são perdidas ao reiniciar o processo (sem persistência do disco).
- Os logs de sessão só são salvos no histórico de chat se você executar <<CODE0>> e o resultado da ferramenta for gravado.
- <<CODE1> é escopo por agente; ele só vê sessões iniciadas por esse agente.
- <<CODE2> inclui uma derivada <<CODE3>> (verbo de comando + alvo) para scans rápidos.
- <<CODE4> usa linha <<CODE5>>/<HTML6>>> (omite <<CODE7>> para agarrar as últimas linhas N).

# # Exemplos

Executar uma longa tarefa e pesquisa mais tarde:

```json
{ "tool": "exec", "command": "sleep 5 && echo done", "yieldMs": 1000 }
```

```json
{ "tool": "process", "action": "poll", "sessionId": "<id>" }
```

Iniciar imediatamente em segundo plano:

```json
{ "tool": "exec", "command": "npm run build", "background": true }
```

Enviar 'stdin':

```json
{ "tool": "process", "action": "write", "sessionId": "<id>", "data": "y\n" }
```
