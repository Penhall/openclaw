---
summary: "macOS Skills settings UI and gateway-backed status"
read_when:
  - Updating the macOS Skills settings UI
  - Changing skills gating or install behavior
---

# Habilidades (macOS)

O aplicativo macOS enfrenta habilidades OpenClaw através do gateway; ele não analisa habilidades localmente.

# # Fonte de dados

- <<CODE0>> (porta) retorna todas as habilidades mais elegibilidade e requisitos em falta
(incluindo blocos de lista de licenças para competências agrupadas).
- Os requisitos são derivados de <<CODE1>> em cada <<CODE2>>.

# # Instalar ações

- <<CODE0> define opções de instalação (brew/node/go/uv).
- O aplicativo chama <<CODE1>> para executar instaladores no host gateway.
- As superfícies de gateway apenas um instalador preferido quando múltiplos são fornecidos
(brew quando disponível, caso contrário gerenciador de nó de <<CODE2>>, padrão npm).

# # Chaves Env/API

- A aplicação guarda as chaves em <<CODE0>> em <<CODE1>>.
- <<CODE2>> sistemas <<CODE3>>, <<CODE4>>, e <<CODE5>>.

# # Modo remoto

- Instalar + atualizações de configuração acontecem no host gateway (não no Mac local).
