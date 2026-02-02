---
summary: "Bridge protocol (legacy nodes): TCP JSONL, pairing, scoped RPC"
read_when:
  - Building or debugging node clients (iOS/Android/macOS node mode)
  - Investigating pairing or bridge auth failures
  - Auditing the node surface exposed by the gateway
---

# Protocolo de ponte (transporte de nó legado)

O protocolo Bridge é um **legacy** transporte de nós (TCP JSONL). Novos clientes de nó
deve usar o protocolo unificado Gateway WebSocket.

Se você está construindo um operador ou cliente de nó, use o
[Protocolo Gateway](<<<LINK0>>>).

**Observação:** OpenClaw atual constrói não mais envia o ouvinte de ponte TCP; este documento é mantido para referência histórica.
Legado <<CODE0>>> chaves de configuração não fazem mais parte do esquema de configuração.

# # Porque temos ambos

- ** Limite de segurança**: a ponte expõe uma pequena lista
superfície API do gateway completo.
- **Pairing + identidade do nó**: entrada do nó é de propriedade do gateway e amarrado
para um símbolo por nós.
- **Discovery UX**: nós podem descobrir gateways via Bonjour na LAN, ou conectar
directamente sobre uma rede traseira.
- ** Loopback WS**: o plano de controle WS completo permanece local, a menos que tunelamento via SSH.

# # Transporte

- TCP, um objecto JSON por linha (JSONL).
- TLS opcional (quando <<CODE0>> é verdadeiro).
- Legacy porta padrão ouvinte foi <<CODE1>> (as construções atuais não iniciam uma ponte TCP).

Quando o TLS está habilitado, os registros de descoberta TXT incluem <<CODE0>> mais
<<CODE1> para que os nós possam fixar o certificado.

# # Aperto de mão + emparelhamento

1. Cliente envia <<CODE0>> com metadados de nó + token (se já emparelhado).
2. Se não for emparelhado, respostas de gateway <<CODE1> (<<CODE2>/<<CODE3>>).
3. O cliente envia <<CODE4>>>>.
4. Gateway espera pela aprovação, em seguida, envia <<CODE5>> e <<CODE6>>>.

<<CODE0> retorna <<CODE1> e pode incluir <<CODE2>>.

# # Quadros

Cliente → Gateway:

- <<CODE0>>/ <<CODE1>>: gateway de alcance RPC (conferência, sessões, configuração, saúde, sonoridade, habilidades.bins)
- <<CODE2>>: sinais de nó (transcrição de voz, pedido do agente, assinatura do chat, ciclo de vida executivo)

Gateway → Cliente:

- <<CODE0>>/ <<CODE1>>: comandos de nó (<<CODE2>>, <<CODE3>>, <<CODE4>>,
<<CODE5>>, <<CODE6>>>)
- <<CODE7>>: atualizações de chat para sessões subscritas
- <<CODE8>>/ <<CODE9>>: manter- se vivo

Legacy allowlist execution viveu em <<CODE0>> (removido).

# # Eventos de ciclo de vida exec

Os nós podem emitir <<CODE0>> ou <<CODE1> eventos para a atividade de superfície system.run.
Estes são mapeados para eventos de sistema no gateway. (Os nós de Legacy ainda podem emitir <<CODE2>>>>).

Campos de carga útil (todos opcionais, salvo indicação em contrário):

- <<CODE0>> (necessário): sessão do agente para receber o evento do sistema.
- <<CODE1>>: id executivo único para agrupamento.
- <<CODE2>>: texto de comando bruto ou formatado.
- <<CODE3>>, <<CODE4>>, <<CODE5>>, <<CODE6>>: detalhes de conclusão (apenas terminados).
- <<CODE7>>: razão de negação (negado apenas).

# # Uso de tailnet

- Ligar a ponte a um IP tailnet: <<CODE0> em
<<CODE1>>>.
- Clientes se conectam através do nome MagicDNS ou IP tailnet.
- Bonjour faz **not** cross networks; use máquina manual/porta ou DNS-SD de área larga
quando necessário.

# # Versionamento

Ponte é atualmente **implicito v1** (sem negociação min/max). Compat para trás
é esperado; adicione um campo de versão do protocolo bridge antes de qualquer alteração de quebra.
