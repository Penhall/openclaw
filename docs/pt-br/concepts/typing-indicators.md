---
summary: "When OpenClaw shows typing indicators and how to tune them"
read_when:
  - Changing typing indicator behavior or defaults
---

# Indicadores de digitação

Os indicadores de digitação são enviados para o canal de chat enquanto uma execução está ativa. Utilização
<<CODE0> para controlar ** quando ** a digitação começa e <<CODE1>
para controlar ** quantas vezes** ele se atualiza.

Padrões

Quando <<CODE0> é **unset**, OpenClaw mantém o comportamento legado:

- **Conversas diretas**: a digitação começa imediatamente quando o loop do modelo começa.
- **Conversas de grupo com uma menção**: a digitação começa imediatamente.
- **Conversas de grupo sem menção**: a digitação só começa quando o texto da mensagem começa a ser transmitido.
- **Heartbeat runs**: digitar está desativado.

# # Modos

Definir <<CODE0>> para um dos seguintes:

- <<CODE0>> – nenhum indicador de tipografia, nunca.
- <<CODE1>> — comece a digitar ** assim que o loop do modelo começar**, mesmo que a execução
mais tarde retorna apenas o token de resposta silenciosa.
- <<CODE2>> — comece a digitar no **primeiro delta de raciocínio** (requisitos
<<CODE3>> para a corrida).
- <<CODE4>> — comece a escrever no delta do texto ** primeiro não silencioso** (ignoros
o símbolo silencioso <<CODE5>).

Ordem de “Quão cedo dispara”:
<<CODE0>> → <<CODE1>> → <<CODE2>> → <<CODE3>>

Configuração

```json5
{
  agent: {
    typingMode: "thinking",
    typingIntervalSeconds: 6,
  },
}
```

Você pode substituir o modo ou cadência por sessão:

```json5
{
  session: {
    typingMode: "message",
    typingIntervalSeconds: 4,
  },
}
```

# # Notas

- <<CODE0>> modo não mostrará a digitação para respostas apenas em silêncio (por exemplo, o <<CODE1>>
token usado para suprimir o resultado).
- <<CODE2>> apenas dispara se o raciocínio de fluxos de execução (<<CODE3>>>).
Se o modelo não emite deltas de raciocínio, a digitação não começa.
- Batimentos cardíacos nunca mostram digitação, independentemente do modo.
- <<CODE4>> controla a cadência **refresh**, não a hora de início.
O padrão é de 6 segundos.
