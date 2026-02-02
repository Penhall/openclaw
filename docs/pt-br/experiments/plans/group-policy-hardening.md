---
summary: "Telegram allowlist hardening: prefix + whitespace normalization"
read_when:
  - Reviewing historical Telegram allowlist changes
---

# Telegram Allowlist Endurecimento

**Data**: 2026-01-05
** Status**: Completo
**PR**: #216

# # Resumo

Listas de licenças de telegrama agora aceitam <<CODE0>> e <<CODE1>> prefixos insensíveis e toleram
espaço em branco acidental. Isto alinha as verificações de lista de allowlist com a normalização de envio de saída.

# # O que mudou

- Os prefixos <<CODE0>> e <<CODE1>> são tratados da mesma forma (insensíveis ao caso).
- Os itens da lista de permissões são aparados; os itens vazios são ignorados.

# # Exemplos

Todos estes são aceitos para o mesmo ID:

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>

# # Porque importa

Copiar/colar de logs ou IDs de bate-papo muitas vezes inclui prefixos e espaço em branco. Normalização evita
falsos negativos ao decidir se responder em DM ou grupos.

# # Docs relacionados

- [Conversas de grupo] (<<<LINK0>>)
- [Fornecedor de Telegramas] (<<< HTML1>>>>)
