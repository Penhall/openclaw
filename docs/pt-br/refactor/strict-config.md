---
summary: "Strict config validation + doctor-only migrations"
read_when:
  - Designing or implementing config validation behavior
  - Working on config migrations or doctor workflows
  - Handling plugin config schemas or plugin load gating
---

# Validação de configuração estrita (migrações somente para médicos)

# # Objetivos

- **Rejeitar chaves de configuração desconhecidas em toda parte** (root + aninhado).
- **Rejeitar a configuração do plugin sem um esquema**; não carregue esse plugin.
- **Remover a auto-migração legada na carga**; migrações executadas apenas através do médico.
- **Auto-run doctor (dry-run) na inicialização**; se inválido, bloquear comandos não diagnósticos.

# # Não-objetivos

- Compatibilidade traseira na carga (chaves de legado não auto-migrar).
- Gotas silenciosas de chaves não reconhecidas.

# # Regras estritas de validação

- A configuração deve corresponder ao esquema em todos os níveis.
- Chaves desconhecidas são erros de validação (sem passagem na raiz ou aninhada).
- `plugins.entries.<id>.config` deve ser validado pelo esquema do plugin.
- Se um plugin não tem um esquema, **rejeitar carga de plugin** e superfície de um erro claro.
- Chaves desconhecidas `channels.<id>` são erros, a menos que um manifesto de plugin declare o ID do canal.
- Manifestações de plug-in (`openclaw.plugin.json`) são necessárias para todos os plugins.

# # Aplicação do esquema de plug-in

- Cada plugin fornece um rigoroso esquema JSON para sua configuração (inline no manifesto).
- Fluxo de carga do plug-in:
1. Resolver manifesto plugin + esquema (`openclaw.plugin.json`).
2. Validar a configuração contra o esquema.
3. Se faltar esquema ou configuração inválida: bloco carga plugin, erro de registro.
- Mensagem de erro inclui:
- Plugin ID
- Razão (esquema em falta / configuração inválida)
- Caminho( s) que falhou na validação
- Plugins desativados mantêm sua configuração, mas o Doctor + registra um aviso.

# # Fluxo médico

- Doutor executa ** toda vez** configuração é carregada (run seco por padrão).
- Se a configuração for inválida:
- Imprima um resumo + erros acionáveis.
- Instrução: `openclaw doctor --fix`.
- <<CODE1>:
- Aplica migrações.
- Remove chaves desconhecidas.
- Grava a configuração actualizada.

# # Aplicação de comandos (quando a configuração é inválida)

Permitido (somente diagnóstico):

- <<CODE0>
- <<CODE1>
- <<CODE2>
- `openclaw help`
- `openclaw status`
- <<CODE5>

Todo o resto deve falhar com: “Config inválido. Executar `openclaw doctor --fix`.”

# # Formato UX de erro

- Um único cabeçalho sumário.
- Seções agrupadas:
- Chaves desconhecidas (caminhos completos)
- Chaves de legado / migrações necessárias
- Falhas de carga do plug-in (id do plug-in + razão + caminho)

# # Pontos de contacto de implementação

- <<CODE0>: remover a passagem da raiz; objetos rígidos em toda parte.
- <<CODE1>: assegurar esquemas rigorosos de canais.
- <<CODE2>: falhar em teclas desconhecidas; não aplicar migrações legadas.
- <<CODE3>: remover auto- migrações legadas; executar sempre o médico de corrida seca.
- <<CODE4>: apenas para uso médico.
- <<CODE5>: adicionar esquema de registo + gating.
- Comando CLI ligado em `src/cli`.

# # Testes

- Rejeição de chave desconhecida (raiz + aninhada).
- Plugin faltando esquema → carga do plugin bloqueado com erro claro.
- Configuração inválida → startup gateway bloqueada exceto comandos de diagnóstico.
- Dr. Dry-run auto; <<CODE0> escreve configuração corrigida.
