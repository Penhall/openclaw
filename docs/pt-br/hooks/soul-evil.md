---
summary: "SOUL Evil hook (swap SOUL.md with SOUL_EVIL.md)"
read_when:
  - You want to enable or tune the SOUL Evil hook
  - You want a purge window or random-chance persona swap
---

O Gancho Maléfico

O gancho SOUL Evil troca o conteúdo ** injetado** <<CODE0>> com <<CODE1> durante
uma janela de purga ou por acaso. Ele faz **not** modificar arquivos no disco.

# # Como Funciona

Quando <<CODE0> correr, o gancho pode substituir o <<CODE1> conteúdo na memória
antes de o sistema ser montado. Se <<CODE2> estiver ausente ou vazio,
OpenClaw registra um aviso e mantém o normal <<CODE3>>>.

As execuções de sub-agentes fazem **not** incluem <<CODE0>> em seus arquivos bootstrap, então este gancho
não produz efeitos nos subagentes.

Activar

```bash
openclaw hooks enable soul-evil
```

Em seguida, defina a configuração:

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "soul-evil": {
          "enabled": true,
          "file": "SOUL_EVIL.md",
          "chance": 0.1,
          "purge": { "at": "21:00", "duration": "15m" }
        }
      }
    }
  }
}
```

Criar <<CODE0>> na raiz do espaço de trabalho do agente (próximo a <<CODE1>>>).

# # Opções

- <<CODE0> (cadeia): nome alternativo do ficheiro SOUL (por omissão: <<CODE1>>>)
- <<CODE2> (número 0–1): probabilidade aleatória por corrida de utilização <<CODE3>>
- <<CODE4> (HH:mm): início diário da purga (relógio de 24 horas)
- <<CODE5>> (duração): comprimento da janela (por exemplo, <<CODE6>>>, <<CODE7>>, <<CODE8>>)

**Precedência:** janela de purga ganha sobre o acaso.

** Fuso horário:** usa <<CODE0> quando definido; caso contrário, hospede fuso horário.

# # Notas

- Nenhum arquivo é escrito ou modificado no disco.
- Se <<CODE0> não estiver na lista de bootstrap, o gancho não faz nada.

# # Veja também

- [Hooks] (<<<LINK0>>>)
