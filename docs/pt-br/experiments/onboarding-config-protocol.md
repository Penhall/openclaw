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

## Porta RCP

-`wizard.start`parâmetros:`{ mode?: "local"|"remote", workspace?: string }`-`wizard.next`parâmetros:`{ sessionId, answer?: { stepId, value? } }`-`wizard.cancel`parâmetros:`{ sessionId }`-`wizard.status`parâmetros:`{ sessionId }`-`config.schema`parâmetros:`{}`

Respostas (forma)

- Wizard:`{ sessionId, done, step?, status?, error? }`- Esquema de configuração:`{ schema, uiHints, version, generatedAt }`

## Dicas de UI

-`uiHints`chaveado pelo caminho; metadados opcionais (rótulo/ajuda/grupo/ordem/avançado/sensível/locatário).
- Campos sensíveis renderizam como entradas de senha; nenhuma camada de redação.
- Os nós de esquema não suportados voltam para o editor JSON bruto.

## Notas

- Este documento é o local único para rastrear os refatores de protocolo para a integração/configuração.
