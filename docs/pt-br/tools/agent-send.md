---
summary: "Direct `openclaw agent` CLI runs (with optional delivery)"
read_when:
  - Adding or modifying the agent CLI entrypoint
---

# `openclaw agent` (funções de agente direto)

<<CODE0> roda um único agente sem precisar de uma mensagem de chat.
Por padrão, vai ** através do Gateway**; adicionar `--local` para forçar o incorporado
tempo de execução na máquina atual.

# # Comportamento

- Requerido: <<CODE0>
- Seleção da sessão:
- <<CODE1> deriva a chave de sessão (os alvos do grupo/canal preservam o isolamento; as conversas directas colapsam para `main`), **ou **
- <<CODE3> reutiliza uma sessão existente por id, **ou **
- <<CODE4> tem como alvo um agente configurado diretamente (usa a chave de sessão <<CODE5> desse agente)
- Corre o mesmo tempo de execução do agente incorporado que as respostas normais.
- As bandeiras de pensamento/verbose persistem na loja de sessões.
- Saída:
- padrão: imprime texto de resposta (mais `MEDIA:<url>` linhas)
- <<CODE7>: imprime carga útil estruturada + metadados
- Entrega opcional para um canal com `--deliver` + `--channel` (formatos-alvo correspondem `openclaw message --target`).
- Usar <<CODE11>/<<CODE12>/`--reply-account` para substituir a entrega sem alterar a sessão.

Se o Gateway é inacessível, o CLI ** volta** para a execução local incorporada.

# # Exemplos

```bash
openclaw agent --to +15555550123 --message "status update"
openclaw agent --agent ops --message "Summarize logs"
openclaw agent --session-id 1234 --message "Summarize inbox" --thinking medium
openclaw agent --to +15555550123 --message "Trace logs" --verbose on --json
openclaw agent --to +15555550123 --message "Summon reply" --deliver
openclaw agent --agent ops --message "Generate report" --deliver --reply-channel slack --reply-to "#reports"
```

# # Bandeiras

- `--local`: executar localmente (exige chaves API do fornecedor do modelo em seu shell)
- <<CODE1>: enviar a resposta ao canal escolhido
- <<CODE2>: canal de entrega (`whatsapp|telegram|discord|googlechat|slack|signal|imessage`, por omissão: <<CODE4>)
- <<CODE5>: sobreposição do alvo de entrega
- <<CODE6>: substituição do canal de entrega
- `--reply-account`: sobreposição do ID da conta de entrega
- <<CODE8>: nível de pensamento persistente (apenas modelos GPT-5.2 + Codex)
- <<CODE9>: persistir no nível de verbose
- `--timeout <seconds>`: tempo limite do agente de substituição
- <<CODE11>: JSON estruturado de saída
