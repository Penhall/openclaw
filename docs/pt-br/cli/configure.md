---
summary: "CLI reference for `openclaw configure` (interactive configuration prompts)"
read_when:
  - You want to tweak credentials, devices, or agent defaults interactively
---

#`openclaw configure`

Prompt interativo para configurar credenciais, dispositivos e padrões de agentes.

Nota: A seção **Modelo** agora inclui um multi-selecionado para o`agents.defaults.models`allowlist (o que aparece no`/model`e no seletor de modelos).

Dica:`openclaw config`sem um subcomando abre o mesmo assistente. Utilização`openclaw config get|set|unset`para edições não interativas.

Relacionados:

- Referência da configuração do portal: [Configuração] /gateway/configuration
- Config CLI: [Config] /cli/config

Notas:

- Escolher onde o Gateway corre sempre actualiza`gateway.mode`. Você pode selecionar "Continuar" sem outras seções, se isso é tudo que você precisa.
- Serviços orientados para canais (Slack/Discord/Matrix/Microsoft Teams) prompt para canais/room allowlists durante a configuração. Você pode digitar nomes ou IDs; o assistente resolve nomes para IDs quando possível.

## Exemplos

```bash
openclaw configure
openclaw configure --section models --section channels
```
