---
summary: "CLI reference for `openclaw system` (system events, heartbeat, presence)"
read_when:
  - You want to enqueue a system event without creating a cron job
  - You need to enable or disable heartbeats
  - You want to inspect system presence entries
---

#`openclaw system`

Ajudantes de nível de sistema para o Gateway: enqueue eventos do sistema, controlar batimentos cardíacos,
e ver a presença.

## Comandos comuns

```bash
openclaw system event --text "Check for urgent follow-ups" --mode now
openclaw system heartbeat enable
openclaw system heartbeat last
openclaw system presence
```

##`system event`

Coloque um evento de sistema na sessão **main**. O próximo batimento cardíaco irá injectar
como uma linha`System:`no prompt. Use`--mode now`para desencadear o batimento cardíaco
imediatamente;`next-heartbeat`espera pelo próximo tique agendado.

Bandeiras:

-`--text <text>`: texto de evento exigido do sistema.
-`--mode <mode>`:`now`ou`next-heartbeat`(padrão).
-`--json`: saída legível por máquina.

##`system heartbeat last|enable|disable`

Controlos cardíacos:

-`last`: mostrar o último evento cardíaco.
-`enable`: ligar os batimentos cardíacos (use isto se estiverem desactivados).
-`disable`: pausar batimentos cardíacos.

Bandeiras:

-`--json`: saída legível por máquina.

##`system presence`

Listar as entradas de presença do sistema atual que o Gateway conhece (nós,
exemplos e linhas de estado semelhantes).

Bandeiras:

-`--json`: saída legível por máquina.

## Notas

- Requer um Gateway em execução acessível pela sua configuração atual (local ou remota).
- Os eventos do sistema são efêmeros e não persistiram em reinícios.
