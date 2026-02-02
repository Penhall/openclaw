---
summary: "First-run onboarding flow for OpenClaw (macOS app)"
read_when:
  - Designing the macOS onboarding assistant
  - Implementing auth or identity setup
---

# Onboarding (macOS app)

Este documento descreve o fluxo de onboard **current**. O objectivo é um
experiência suave “dia 0”: escolha onde o Gateway corre, conecte a autenticação, execute o
Feiticeiro, e deixe o agente se amarrar.

# # Ordem da página (atual)

1. Bem-vindo + aviso de segurança
2. **Selecção de Gateway** (Local / Remoto / Configurar mais tarde)
3. ** Auth (OAuth antrópico)** — apenas local
4. ** Assistente de configuração** (Dirigido por Gateway)
5. **Permissões** (promessas TCC)
6. **CLI** (opcional)
7. **Conversa de bordo** (sessão dedicada)
8. Pronto

# # 1) Local vs Remoto

Onde é que o **Gateway** corre?

- **Local (este Mac):** onboarding pode executar fluxos de OAuth e escrever credenciais
localmente.
- ** Remote (sobre SSH/Tailnet):** onboarding does ** not** execute OAuth localmente;
As credenciais devem existir no host do portal.
- **Configure posterior:** pule a configuração e deixe o aplicativo não configurado.

Ponta de entrada:

- O assistente agora gera um **token** mesmo para loopback, então clientes WS locais devem autenticar.
- Se você desativar a autenticação, qualquer processo local pode se conectar; use isso apenas em máquinas totalmente confiáveis.
- Use um **token** para acesso multi-máquina ou liga não-loopback.

2) Auth apenas local (Auth antrópico)

O aplicativo macOS suporta Autthropic OAuth (Claude Pro/Max). O fluxo:

- Abre o navegador para OAuth (PKCE)
- Pede ao utilizador que cole o <<CODE0>> valor
- Escreve credenciais para <<CODE1>>>

Outros provedores (OpenAI, APIs personalizadas) são configurados através de variáveis de ambiente
ou arquivos de configuração por enquanto.

# # 3) Assistente de Configuração (dirigido pelo portal)

O aplicativo pode executar o mesmo assistente de configuração que o CLI. Isto continua em sincronia
com o comportamento de Gateway-side e evita duplicar a lógica em SwiftUI.

4) Permissões

Pedidos de integração TCC de permissões necessárias para:

- Notificações
Acessibilidade
- Gravação de tela
- Reconhecimento de Microfone / Fala
- Automação (AppleScript)

# # 5) CLI (opcional)

O aplicativo pode instalar o global <<CODE0>> CLI via npm/pnpm assim terminal
fluxos de trabalho e tarefas lançadas funcionam fora da caixa.

## 6) Conversa de bordo (sessão dedicada)

Após a configuração, o aplicativo abre uma sessão de chat dedicada para que o agente possa
apresentar-se e orientar os próximos passos. Isto mantém a orientação de primeira ordem separada
da sua conversa normal.

# # Ritual de bootstrap agente

Na primeira execução do agente, OpenClaw inicia uma área de trabalho (padrão <<CODE0>>>):

- Sementes <<CODE0>>, <<CODE1>>, <<CODE2>>, <<CODE3>>
- Realiza um pequeno ritual de perguntas e respostas (uma pergunta de cada vez)
- Escreve identidade + preferências para <<CODE4>>>, <<CODE5>>, <<CODE6>>
- Remove <<CODE7>> quando terminado para que só funcione uma vez

# # Opcional: ganchos Gmail (manual)

A configuração do Gmail Pub/Sub é atualmente um passo manual. Utilização:

```bash
openclaw webhooks gmail setup --account you@gmail.com
```

Ver [/automation/gmail-pubsub](<<<LINK0>>>) para mais detalhes.

# # Notas de modo remoto

Quando o Gateway é executado em outra máquina, credenciais e arquivos de espaço de trabalho ao vivo
** naquele hospedeiro**. Se precisar de OAuth em modo remoto, crie:

- <<CODE0>>
- <<CODE1>>

no anfitrião do portal.
