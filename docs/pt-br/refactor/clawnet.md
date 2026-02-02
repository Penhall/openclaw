---
summary: "Clawnet refactor: unify network protocol, roles, auth, approvals, identity"
read_when:
  - Planning a unified network protocol for nodes + operator clients
  - Reworking approvals, pairing, TLS, and presence across devices
---

# Refactor de Clawnet (protocolo + unificação de autenticação)

# # Olá

Oi Peter — ótima direção; isso desbloqueia UX mais simples + segurança mais forte.

# # Finalidade

Documento único e rigoroso para:

- Estado actual: protocolos, fluxos, limites de confiança.
- Pontos de dor: aprovações, roteamento multi-hop, duplicação de IU.
- Proposto novo estado: um protocolo, papéis de escopo, auth/pairing unificado, TLS pinning.
- Modelo de identidade: IDs estáveis + lesmas bonitos.
Plano de migração, riscos, perguntas abertas.

# # Objetivos (da discussão)

- Um protocolo para todos os clientes (mac app, CLI, iOS, Android, nó sem cabeça).
- Cada participante de rede autenticado + emparelhado.
- clareza de papel: nós vs operadores.
- aprovações centrais encaminhadas para onde o utilizador está.
- Criptografia TLS + opcional para todo o tráfego remoto.
- Duplicação mínima de código.
- Uma única máquina deve aparecer uma vez (sem entrada duplicada de UI/nó).

# # Não-objetivos (explico)

- Remover a separação de capacidade (ainda precisa de menos privilégios).
- Expor o avião de controlo sem controlo de alcance.
- Faça a autorização depender de rótulos humanos (slugs permanecem não-segurança).

---

# Estado atual (como-is)

# # Dois protocolos

###1) Gateway WebSocket (plano de controle)

- Superfície API completa: configuração, canais, modelos, sessões, operações de agente, registros, nós, etc.
- Ligação padrão: loopback. Acesso remoto via SSH/Tailscale.
- Auth: token/password via `connect`.
- Sem pinning TLS (recorre em loopback/tunel).
- Código:
- <<CODE1>
- <<CODE2>
- `docs/gateway/protocol.md`

### 2) Ponte (transporte de nós)

- Superfície de lista de permissão estreita, identidade de nó + emparelhamento.
- JSONL sobre TCP; TLS opcional + fixação de impressão digital.
O TLS anuncia impressões digitais na descoberta do TXT.
- Código:
- <<CODE0>
- <<CODE1>
- <<CODE2>
- `docs/gateway/bridge-protocol.md`

# # Controlar os clientes do avião hoje

- CLI → Gateway WS via `callGateway` (`src/gateway/call.ts`).
- app macOS UI → Gateway WS (`GatewayConnection`).
- Web Control UI → Gateway WS.
ACP → Gateway WS.
- O controle do navegador usa seu próprio servidor de controle HTTP.

# # Nós hoje

- app macOS em modo nó se conecta à ponte Gateway (`MacNodeBridgeSession`).
- Aplicativos iOS/Android se conectam à ponte Gateway.
- Emparelhamento + token por nós armazenado no gateway.

# # Fluxo de aprovação atual (exec)

- O agente utiliza `system.run` via Gateway.
- O portal invoca o nó sobre a ponte.
- O tempo de execução decide a aprovação.
- Prompt de IU mostrado pelo aplicativo mac (quando o nó == app mac).
- Node retorna <<CODE1> ao Gateway.
- Multi-hop, UI ligada ao hospedeiro.

# # # Presença + identidade hoje

- Entradas de presença da WS clientes.
- Entradas de presença de nós da ponte.
- app mac pode mostrar duas entradas para uma mesma máquina (UI + nó).
- Identidade do nó armazenada na loja de emparelhamento; identidade da interface separada.

---

Problemas / pontos de dor

- Duas pilhas de protocolo para manter (WS + Ponte).
- Aprovação em nós remotos: prompt aparece no host do nó, não onde o usuário está.
- TLS pinning só existe para ponte; WS depende de SSH/Tailscale.
- Duplicação de identidade: mesma máquina mostra como várias instâncias.
- Funções ambíguas: UI + nó + capacidades CLI não claramente separadas.

---

# Novo estado proposto (Clawnet)

# # # Um protocolo, dois papéis

Protocolo WS único com função + escopo.

- **Role: nó** (capability host)
- **Role: operador** (plano de controlo)
- Opcional **scope** para operador:
- <<CODE0> (estado + visualização)
- <<CODE1> (execução do agente, envio)
- <<CODE2> (config, canais, modelos)

## # Comportamentos de papéis

**Node**

- Pode registrar capacidades (`caps`, <CODE1>>, permissões).
- Pode receber comandos <<CODE2> (`system.run`, `camera.*`, `canvas.*`, `screen.record`, etc).
- Pode enviar eventos: `voice.transcript`, `agent.request`, `chat.subscribe`.
- Não é possível chamar a configuração/modelos/canais/sessões/plano de controle de agentes APIs.

**Operador **

- A API do avião de controlo completo.
- Recebe todas as aprovações.
- Não executa diretamente as ações do SO; rotas para nós.

Regra chave

O papel é por ligação, não por dispositivo. Um dispositivo pode abrir ambas as funções, separadamente.

---

# Autenticação unificada + emparelhamento

# # Identidade do cliente

Cada cliente fornece:

- `deviceId` (estável, derivado da chave do dispositivo).
- <<CODE1> (nome humano).
- `role` + `scope` + `caps` + <<CODE5>.

# # Fluxo de emparelhamento (unificado)

- Cliente não autenticado.
- Gateway cria um pedido de ** par para que `deviceId`.
- Operador recebe imediato; aprova / nega.
- O portal emite credenciais ligadas a:
- chave pública do dispositivo
- funções
- âmbito de aplicação
- capacidades/comandos
- Cliente persiste token, reconecta autenticado.

# # Autenticação ligada ao dispositivo (evitar repetição do token ao portador)

Preferido: keypairs do dispositivo.

- O dispositivo gera keypair uma vez.
- `deviceId = fingerprint(publicKey)`.
- Gateway envia nonce; sinais de dispositivo; gateway verifica.
- Os tokens são emitidos para uma chave pública (prova de posse), não uma corda.

Alternativas:

- mTLS (certes de clientes): mais forte, mais complexidade de operações.
- Tokens ao portador de curta duração apenas como uma fase temporária (rotar + revogar cedo).

# # Aprovação silenciosa (heurística SHS)

Defina-o precisamente para evitar um elo fraco. Preferir um:

- **Local-only**: auto-parer quando o cliente se conecta via loopback/Soquete Unix.
- **Challenge via SSH**: gateway issues nonce; cliente prova SSH por buscá-lo.
- ** Janela de presença física**: após uma aprovação local na interface do servidor de gateway, permita um par automático para uma janela curta (por exemplo, 10 minutos).

Sempre log + gravar auto-aprovações.

---

# TLS em toda parte (dev + prod)

# # Reutilizar TLS de ponte existente

Usar o tempo de execução TLS atual + pinning de impressão digital:

- <<CODE0>
- lógica de verificação das impressões digitais em <<CODE1>

# # Aplicar no WS

- O servidor WS suporta TLS com o mesmo certificado/chave + impressão digital.
- Os clientes WS podem fixar a impressão digital (opcional).
- Discovery anuncia TLS + impressão digital para todos os terminais.
- Discovery é apenas dicas localizadoras; nunca uma âncora de confiança.

# # Porque

- Reduzir a confiança em SSH/Tailscale para confidencialidade.
- Tornar as conexões móveis remotas seguras por padrão.

---

# Aprovações redesenhadas (centralizado)

# # Atual

A aprovação acontece no host do nó (mac app node runtime). O prompt aparece onde o nó corre.

# # Proposto

A aprovação é **gateway-hosted**, UI entregue aos clientes do operador.

Novo fluxo

1. Gateway recebe `system.run` intenção (agente).
2. Gateway cria registro de aprovação: `approval.requested`.
3. O operador UI (s) mostrar prompt.
4. Decisão de aprovação enviada ao portal: `approval.resolve`.
5. Gateway invoca o comando do nó se aprovado.
6. O nó executa, retorna `invoke-res`.

## # Semântica de aprovação (endurecimento)

- Transmitir para todos os operadores; apenas a UI ativa mostra um modal (outros recebem um brinde).
- Primeira resolução ganha; gateway rejeita soluções subsequentes como já está resolvido.
- Tempo limite padrão: negar após N segundos (por exemplo, 60s), razão do log.
- A resolução requer um âmbito `operator.approvals`.

# # Benefícios

- O prompt aparece onde o usuário está (mac/phone).
- Aprovação consistente para nós remotos.
- Node Runtime fica sem cabeça, sem dependência de IU.

---

# Exemplos de clareza de papéis

# # App iPhone

- **Node role** para: microfone, câmera, chat de voz, localização, push-to-talk.
- Opcional **operator.read** para status e chat view.
- Opcional **operator.write/admin** somente quando explicitamente habilitado.

# # app macOS

- Papel do operador por padrão (UI de controle).
- Role do nó quando "Node Mac" ativado (system.run, tela, câmera).
- Mesmo dispositivoId para ambas as conexões → entrada de UI fundida.

# # CLI

- O papel de operador sempre.
- Âmbito de aplicação derivado do subcomando:
- <<CODE0>, `logs` → ler
- `agent`, `message` → escrever
- `config`, `channels` → admin
- aprovações + pareamento → `operator.approvals` / `operator.pairing`

---

Identidade + lesmas

# # ID estável

Necessário para autenticação; nunca muda.
Preferido:

- Impressões digitais Keypair (hash chave pública).

# # Lesma gira (tema de lobo)

Apenas rótulo humano.

- Exemplo: <<CODE0>, <<CODE1>, <<CODE2>.
- Armazenado no registo de gateway, editável.
- Tratamento da colisão: `-2`, `-3`.

# # Grupo de IU

Mesmo `deviceId` em todos os papéis → linha única “Instance”:

- Distintivo: `operator`, `node`.
- Mostra capacidades + vista pela última vez.

---

Estratégia de migração

## Fase 0: Documento + alinhamento

- Publique este doutor.
- Inventário todas as chamadas de protocolo + fluxos de aprovação.

## Fase 1: Adicione papéis/escopos ao WS

- Estender <<CODE0> params com `role`, `scope`, <<CODE3>.
- Adicionar lista de allowlist para o papel do nó.

## Fase 2: Compatibilidade da ponte

- Continua a ligar a ponte.
- Adicionar suporte de nó WS em paralelo.
- Características do portal atrás da bandeira de configuração.

## Fase 3: aprovações centrais

- Adicionar pedido de aprovação + resolver eventos em WS.
- Atualizar a interface do aplicativo Mac para solicitar + responder.
- O tempo de execução do nó pára de provocar a IU.

## Fase 4: unificação do TLS

- Adicionar configuração TLS para WS usando ponte TLS tempo de execução.
- Acrescentem os clientes.

## Fase 5: Ponte despreparada

- Migrar o nó iOS/Android/mac para WS.
- Manter ponte como recuo; remover uma vez estável.

## Fase 6: Autenticação ligada ao dispositivo

- Requer uma identidade baseada em chaves para todas as ligações não locais.
- Adicionar revogação + rotação UI.

---

Notas de segurança

- Papel/allowlist aplicado no limite do portal.
- Nenhum cliente recebe API “completa” sem escopo de operador.
- Emparelhamento necessário para  all  conexões.
- TLS + pinning reduz o risco MITM para celular.
- A aprovação silenciosa SSH é uma conveniência; ainda gravado + revogável.
- Discovery nunca é uma âncora de confiança.
- Reclamações de capacidade são verificadas contra listas de servidores por plataforma/tipo.

# Streaming + grandes cargas (node media)

O plano de controle WS é bom para mensagens pequenas, mas nós também fazem:

- clipes de câmera
- gravações de ecrã
- fluxos de áudio

Opções:

1. Quadros binários WS + quebra + regras de contrapressão.
2. Endpoint de streaming separado (ainda TLS + autenticação).
3. Mantenha a ponte por mais tempo para comandos pesados de mídia, migrar por último.

Escolha um antes da implementação para evitar deriva.

# Capabilidade + política de comando

- As tampas/comandos node-referidos são tratadas como **clamações**.
- A Gateway impõe listas de autorização de plataforma.
- Qualquer novo comando requer aprovação do operador ou alteração explícita da lista de autorizações.
- A auditoria muda com as datas.

# Auditoria + limitação de taxa

- Log: pedidos de pareamento, aprovações/negações, emissão/rotação/recusa de fichas.
- Limite de taxa de emparelhamento spam e avisos de aprovação.

# Higiene do protocolo

- Versão de protocolo explícito + códigos de erro.
- Reconectar regras + política de batimento cardíaco.
- Presença TTL e semântica vista pela última vez.

---

Perguntas abertas

1. Dispositivo único executando ambas as funções: modelo de token
- Recomendar fichas separadas por função (nó vs operador).
- Mesmo dispositivoId; diferentes escopos; revogação mais clara.

2. Âmbito do operador granularidade
- leitura/escrita/admin + aprovações + emparelhamento (mínimo viável).
- Considere os escopos perfeitos mais tarde.

3. Token rotation + revogação UX
- Auto-rotar sobre mudança de papel.
- IU para revogar por dispositivoId + papel.

4. Descoberta
- Estenda o Bonjour TXT atual para incluir impressões digitais TLS WS + dicas de função.
- Tratar apenas como pistas de localização.

5. Aprovação da rede cruzada
- Transmissão para todos os clientes operador; UI ativa mostra modal.
- A primeira resposta ganha; o portal impõe a atomidade.

---

# Resumo (TL;DR)

- Hoje: plano de controle WS + transporte de nó de ponte.
- Dor: aprovações + duplicação + duas pilhas.
- Proposta: um protocolo WS com funções explícitas + escopos, emparelhamento unificado + pinning TLS, aprovações hospedadas por gateway, IDs de dispositivos estáveis + less bonitos.
- Resultado: UX mais simples, segurança mais forte, menos duplicação, melhor roteamento móvel.
