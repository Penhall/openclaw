---
summary: "Diagnostics flags for targeted debug logs"
read_when:
  - You need targeted debug logs without raising global logging levels
  - You need to capture subsystem-specific logs for support
---

# Bandeiras de diagnóstico

Parâmetros de diagnóstico permitem ativar logs de depuração direcionados sem ligar o registro de verbose em qualquer lugar. As bandeiras são opt-in e só produzem efeitos se um subsistema as verificar.

# # Como funciona

- As bandeiras são strings (insensíveis ao caso).
- Você pode ativar sinalizadores em configuração ou através de um comando env.
- Wildcards são suportados:
- <<CODE0> corresponde <<CODE1>>
- <<CODE2>> permite todas as bandeiras

# # Activar através da configuração

```json
{
  "diagnostics": {
    "flags": ["telegram.http"]
  }
}
```

Múltiplas bandeiras:

```json
{
  "diagnostics": {
    "flags": ["telegram.http", "gateway.*"]
  }
}
```

Reinicie o gateway após mudar as bandeiras.

# # Env sobrepor (um-off)

```bash
OPENCLAW_DIAGNOSTICS=telegram.http,telegram.payload
```

Desactivar todas as bandeiras:

```bash
OPENCLAW_DIAGNOSTICS=0
```

# # Onde os troncos vão

Bandeiras emitem logs no arquivo de registro de diagnósticos padrão. Por padrão:

```
/tmp/openclaw/openclaw-YYYY-MM-DD.log
```

Se você definir <<CODE0>>, use esse caminho. Os logs são JSONL (um objeto JSON por linha). A Redação ainda se aplica com base em <<CODE1>>>.

# # Extrair logs

Escolha o último arquivo de registro:

```bash
ls -t /tmp/openclaw/openclaw-*.log | head -n 1
```

Filtro para os diagnósticos HTTP do Telegram:

```bash
rg "telegram http error" /tmp/openclaw/openclaw-*.log
```

Ou cauda durante a reprodução:

```bash
tail -f /tmp/openclaw/openclaw-$(date +%F).log | rg "telegram http error"
```

Para gateways remotos, você também pode usar <<CODE0>> (ver [/cli/logs](<<LINK0>>)).

# # Notas

- Se <<CODE0> for estabelecido acima de <<CODE1>>>, estes registos podem ser suprimidos. O padrão <<CODE2>> está ótimo.
- As bandeiras são seguras para deixar ativadas; elas só afetam o volume de log para o subsistema específico.
- Use [/logging](<<<LINK0>>>) para alterar os destinos, níveis e redação do log.
