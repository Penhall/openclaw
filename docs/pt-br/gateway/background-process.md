---
summary: "Background exec execution and process management"
read_when:
  - Adding or modifying background exec behavior
  - Debugging long-running exec tasks
---

# Fundo Exec + Ferramenta de Processo

O OpenClaw executa comandos shell através da ferramenta`exec`e mantém tarefas de longa duração na memória. A ferramenta`process`gerencia essas sessões de fundo.

## ferramenta executiva

Parâmetros chave:

-`command`(obrigatório)
-`yieldMs`(padrão 10000): auto-background após este atraso
-`background`(bool): fundo imediatamente
-`timeout`(segundos, padrão 1800): matar o processo após este tempo limite
-`elevated`(bool): correr na máquina se o modo elevado estiver activado/permitido
- Precisas de um TTY verdadeiro? Preparar`pty: true`.
-`workdir`,`env`

Comportamento:

- O primeiro plano executa a saída de retorno diretamente.
- Quando em backgrounded (explicit ou timeout), a ferramenta retorna`status: "running"`+`sessionId`e uma cauda curta.
- A saída é mantida em memória até que a sessão seja pesquisada ou limpa.
- Se a ferramenta`process`for proibida, o`exec`é executado de forma sincronizada e ignora o`yieldMs`/`background`.

## Processo infantil em ponte

Ao gerar processos infantis de longa duração fora das ferramentas de execução/processo (por exemplo, respawns CLI ou ajudantes de gateway), anexe o auxiliar de ponte de processo-criança para que os sinais de terminação sejam enviados e os ouvintes sejam separados na saída/erro. Isso evita processos órfãos em systemd e mantém o comportamento de desligamento consistente entre plataformas.

O ambiente substitui- se:

-`PI_BASH_YIELD_MS`: rendimento por defeito (ms)
-`PI_BASH_MAX_OUTPUT_CHARS`: tampa de saída em memória (chars)
-`OPENCLAW_BASH_PENDING_MAX_OUTPUT_CHARS`: tampa pendente de stdout/stderr por fluxo (chars)
-`PI_BASH_JOB_TTL_MS`: TTL para sessões concluídas (ms, limitado a 1m-3h)

Configuração (preferido):

-`tools.exec.backgroundMs`(padrão 10000)
-`tools.exec.timeoutSec`(padrão 1800)
-`tools.exec.cleanupMs`(padrão 1800000)
-`tools.exec.notifyOnExit`(padrão true): coloque um evento do sistema + solicitação de batimento cardíaco quando um executivo de fundo sai.

## ferramenta de processo

Acções:

-`list`: execução + sessões terminadas
-`poll`: dreno de nova saída para uma sessão (também reporta status de saída)
-`log`: leia a produção agregada (apoia`offset`+`limit`
-`write`: enviar stdin `data`, opcional`eof`
-`kill`: encerrar uma sessão de fundo
-`clear`: remover uma sessão terminada da memória
-`poll`0: matar se correr, caso contrário limpar se terminar

Notas:

- Apenas as sessões de fundo são listadas/persistidas na memória.
- Sessões são perdidas ao reiniciar o processo (sem persistência do disco).
- Os logs de sessão só são salvos no histórico de chat se você executar`process poll/log`e o resultado da ferramenta for gravado.
-`process`é avaliado por agente; ele só vê sessões iniciadas por esse agente.
-`process list`inclui um`name`derivado (verbo de comando + alvo) para varreduras rápidas.
-`process log`utiliza linhas`offset`/`limit`(omite`offset`para agarrar as últimas linhas N).

## Exemplos

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
