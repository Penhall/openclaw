---
summary: "Plugin manifest + JSON schema requirements (strict config validation)"
read_when:
  - You are building a OpenClaw plugin
  - You need to ship a plugin config schema or debug plugin validation errors
---

# Manifesto do plugin (openclaw.plugin.json)

Cada plugin **deve** enviar um arquivo `openclaw.plugin.json` na raiz **plugin**.
Openclaw usa este manifesto para validar a configuração **sem executar o plugin
código**. Manifestantes ausentes ou inválidos são tratados como erros de plugin e bloco
validação de configuração.

Veja o guia completo do sistema de plugins: [Plugins](</plugin).

# # Campos obrigatórios

```json
{
  "id": "voice-call",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```

Chaves necessárias:

- `id` (string): canônico plugin id.
- <<CODE1> (objeto): Esquema JSON para configuração do plugin (inline).

Teclas opcionais:

- <<CODE0> (texto): tipo de plugin (exemplo: `"memory"`).
- `channels` (array): IDs de canal registrados por este plugin (exemplo: `["matrix"]`).
- `providers` (array): IDs de provedor registrados por este plugin.
- `skills` (array): diretórios de habilidade para carregar (relativo à raiz do plugin).
- <<CODE6> (string): exibir o nome do plugin.
- `description` (string): resumo curto do plugin.
- `uiHints` (objeto): etiquetas de campo de configuração/placeholders/marcas sensíveis para renderização de UI.
- `version` (string): versão do plugin (informacional).

# # Requisitos de esquema JSON

- ** Todo plugin deve enviar um esquema JSON**, mesmo que ele não aceite nenhuma configuração.
- Um esquema vazio é aceitável (por exemplo, `{ "type": "object", "additionalProperties": false }`).
- Os esquemas são validados em tempo de leitura/gravação de configuração, não em tempo de execução.

# # Comportamento de validação

- As teclas desconhecidas <<CODE0> são ** erros**, a menos que o ID do canal seja declarado por
um manifesto de plugin.
- `plugins.entries.<id>`, `plugins.allow`, `plugins.deny` e `plugins.slots.*`
deve referenciar **descobrible** plugin ids. IDs desconhecidos são ** erros**.
- Se um plugin estiver instalado mas tiver um manifesto ou esquema quebrado ou ausente,
a validação falhou e o Doctor relata o erro do plugin.
- Se a configuração do plugin existe, mas o plugin é **desactivado**, a configuração é mantida e
a ** aviso** é aflorado em Doctor + logs.

# # Notas

- O manifesto é **necessário para todos os plugins**, incluindo cargas locais do sistema de arquivos.
- Runtime ainda carrega o módulo de plugin separadamente; o manifesto é apenas para
descoberta + validação.
- Se o seu plugin depende de módulos nativos, documento as etapas de compilação e qualquer
requisitos de allowlist do gestor de pacotes (por exemplo, pnpm `allow-build-scripts`
- `pnpm rebuild <package>`).
