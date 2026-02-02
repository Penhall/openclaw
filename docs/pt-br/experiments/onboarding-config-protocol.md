---
summary: "RPC protocol notes for onboarding wizard and config schema"
read_when: "Changing onboarding wizard steps or config schema endpoints"
---

# Onboarding + Protocolo de configuração

Objetivo: integração compartilhada + superfícies de configuração em CLI, aplicativo macOS e interface Web.

Componentes

- Wizard Engine (sessão compartilhada + prompts + estado de onboarding).
- CLI onboarding usa o mesmo fluxo assistente que os clientes de UI.
- Gateway RPC expõe assistente + esquema de configuração endpoints.
- o macOS a bordo usa o modelo passo assistente.
- Web UI renderiza formulários de configuração de JSON Schema + dicas de UI.

# # Porta RCP

- <<CODE0> parâmetros: <<CODE1>>
- <<CODE2> parâmetros: <<CODE3>>
- <<CODE4> params: <<CODE5>
- <<CODE6> parâmetros: <<CODE7>>
- <<CODE8>> parâmetros: <<CODE9>>

Respostas (forma)

- Assistente: <<CODE0>>
- Esquema de configuração: <<CODE1>>

# # Dicas de UI

- <<CODE0> keyed by path; metadados opcionais (label/help/group/order/avanced/sensível/placeholder).
- Campos sensíveis renderizam como entradas de senha; nenhuma camada de redação.
- Os nós de esquema não suportados voltam para o editor JSON bruto.

# # Notas

- Este documento é o local único para rastrear os refatores de protocolo para a integração/configuração.
