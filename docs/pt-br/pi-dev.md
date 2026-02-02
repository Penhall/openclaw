# Pi Desenvolvimento Workflow

Este guia resume um fluxo de trabalho são para trabalhar na integração pi no OpenClaw.

# # Verificação do tipo e revestimento

- Verificação e compilação do tipo: <<CODE0>>
- Lint: <<CODE1>>
- Verificação do formato: <<CODE2>>>
- Porta completa antes de empurrar: <<CODE3>>>

# # Realizando testes de Pi

Use o script dedicado para o conjunto de testes de integração pi:

```bash
scripts/pi/run-tests.sh
```

Incluir o teste ao vivo que exerce o comportamento real do provedor:

```bash
scripts/pi/run-tests.sh --live
```

O script executa todos os testes de unidade relacionados ao pi através destes globs:

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>
- <<CODE3>>
- <<CODE4>>
- <<CODE5>>

# # Teste manual

Fluxo recomendado:

- Execute o gateway no modo dev:
- <<CODE0>>
- Activar o agente directamente:
- <<CODE1>>
- Use o TUI para depuração interativa:
- <<CODE2>>

Para o comportamento da chamada da ferramenta, prompt para um <<CODE0>> ou <<CODE1>> ação para que você possa ver streaming de ferramentas e manuseio de carga útil.

# # Reiniciar Ardósia Limpa

O Estado vive sob o directório estatal OpenClaw. O padrão é <<CODE0>>>. Se <<CODE1> estiver definido, use esse diretório.

Para reiniciar tudo:

- <<CODE0> para configuração
- <<CODE1>> para perfis e fichas de autenticação
- <<CODE2> para o histórico de sessões do agente
- <<CODE3> para o índice de sessão
- <<CODE4> se existirem caminhos legados
- <<CODE5> se quiser um espaço de trabalho em branco

Se você só quer reiniciar as sessões, exclua <<CODE0>> e <<CODE1>>> para esse agente. Mantenha <<CODE2> se não quiser reautenticar.

# # Referências

- https://docs.openclaw.ai/testing
- https://docs.openclaw.ai/start/getting-started
