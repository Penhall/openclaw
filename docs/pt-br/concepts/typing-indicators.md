---
summary: "When OpenClaw shows typing indicators and how to tune them"
read_when:
  - Changing typing indicator behavior or defaults
---

# Indicadores de digitação

Os indicadores de digitação são enviados para o canal de chat enquanto uma execução está ativa. Utilização`agents.defaults.typingMode`para controlar **quando** começa a digitação e`typingIntervalSeconds`para controlar ** quantas vezes** ele se atualiza.

Padrões

Quando`agents.defaults.typingMode`é **unset**, OpenClaw mantém o comportamento legado:

- **Conversas diretas**: a digitação começa imediatamente quando o loop do modelo começa.
- **Conversas de grupo com uma menção**: a digitação começa imediatamente.
- **Conversas de grupo sem menção**: a digitação só começa quando o texto da mensagem começa a ser transmitido.
- **Heartbeat runs**: digitar está desativado.

## Modos

Definir`agents.defaults.typingMode`como um dos seguintes:

-`never`— sem indicador de tipografia, nunca.
-`instant`— comece a digitar ** assim que o loop do modelo começar**, mesmo que a execução
mais tarde retorna apenas o token de resposta silenciosa.
-`thinking`— comece a digitar o delta do primeiro raciocínio** (requisitos`reasoningLevel: "stream"`para a corrida).
-`message`— comece a escrever no delta do texto ** primeiro texto não silencioso** (ignoros)
o símbolo silencioso`NO_REPLY`.

Ordem de “Quão cedo dispara”:`never`→`message`→`thinking`→`instant`

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

## Notas

- O modo`message`não mostrará a digitação para respostas somente em silêncio (por exemplo, o`NO_REPLY`token usado para suprimir o resultado).
-`thinking`só dispara se o raciocínio dos fluxos de circulação `reasoningLevel: "stream"`.
Se o modelo não emite deltas de raciocínio, a digitação não começa.
- Batimentos cardíacos nunca mostram digitação, independentemente do modo.
-`typingIntervalSeconds`controla a cadência **refresh**, não a hora de início.
O padrão é de 6 segundos.
