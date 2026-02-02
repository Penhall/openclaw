---
summary: "macOS permission persistence (TCC) and signing requirements"
read_when:
  - Debugging missing or stuck macOS permission prompts
  - Packaging or signing the macOS app
  - Changing bundle IDs or app install paths
---

# permissões do macOS (TCC)

Os subsídios de autorização do macOS são frágeis. TCC associa uma concessão de permissão com o
assinatura de código do aplicativo, identificador do pacote, e caminho no disco. Se alguma delas mudar,
macOS trata o aplicativo como novo e pode soltar ou ocultar prompts.

# # Requisitos para permissões estáveis

- Mesmo caminho: execute o aplicativo a partir de um local fixo (para OpenClaw, <<CODE0>>).
- Identificador do mesmo pacote: alterar o ID do pacote cria uma nova identidade de permissão.
- Aplicativo assinado: builds assinados sem assinatura ou ad-hoc não persistem permissões.
- Assinatura consistente: use um certificado verdadeiro do Apple Development ou do Developer ID
Por isso, a assinatura mantém-se estável nas reconstruções.

Assinaturas ad hoc geram uma nova identidade a cada compilação. macOS esquecerá o anterior
subvenções, e prompts podem desaparecer completamente até que as entradas antigas sejam limpas.

# # Lista de verificação de recuperação quando alertas desaparecem

1. Saia do aplicativo.
2. Remova a entrada do aplicativo em Configurações do Sistema -> Privacidade e Segurança.
3. Relacione o aplicativo do mesmo caminho e re-grand permissões.
4. Se o prompt ainda não aparecer, reset entradas TCC com <<CODE0>> e tentar novamente.
5. Algumas permissões só reaparecem depois de um macOS completo reiniciar.

Exemplo resets (substituir o ID do pacote conforme necessário):

```bash
sudo tccutil reset Accessibility bot.molt.mac
sudo tccutil reset ScreenCapture bot.molt.mac
sudo tccutil reset AppleEvents
```

Se você estiver testando permissões, sempre assine com um certificado real. Ad-hoc
builds são apenas aceitáveis para corridas locais rápidas onde permissões não importam.
