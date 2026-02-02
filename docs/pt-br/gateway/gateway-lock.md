---
summary: "Gateway singleton guard using the WebSocket listener bind"
read_when:
  - Running or debugging the gateway process
  - Investigating single-instance enforcement
---

Fechamento da porta

Última actualização: 2025-12-11

# # Porque

- Garantir que apenas uma instância de gateway é executada por porta base no mesmo host; gateways adicionais devem usar perfis isolados e portas únicas.
- Sobreviver a quebras/SIGKILL sem deixar arquivos de bloqueio.
- Falha rapidamente com um erro claro quando a porta de controlo já está ocupada.

# # Mecanismo

- O gateway liga o ouvinte WebSocket (padrão <<CODE0>>) imediatamente na inicialização usando um ouvinte TCP exclusivo.
- Se a ligação falhar com <<CODE1>>, a inicialização lança <<CODE2>>>.
- O sistema operacional libera o ouvinte automaticamente em qualquer saída do processo, incluindo falhas e SIGKILL – nenhum arquivo de bloqueio separado ou passo de limpeza é necessário.
- Ao desligar o gateway fecha o servidor WebSocket e o servidor HTTP subjacente para liberar a porta prontamente.

# # Superfície de erro

- Se outro processo segura a porta, a inicialização lança <<CODE0>>>.
- Outras falhas de ligação à superfície como <<CODE1>>>>.

# # Notas operacionais

- Se a porta é ocupada por  outro processo , o erro é o mesmo; liberte a porta ou escolha outra com <<CODE0>>.
- O aplicativo macOS ainda mantém sua própria proteção PID leve antes de gerar o gateway; o bloqueio de tempo de execução é forçado pelo WebSocket vincular.
