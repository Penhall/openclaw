---
summary: "Gateway runtime on macOS (external launchd service)"
read_when:
  - Packaging OpenClaw.app
  - Debugging the macOS gateway launchd service
  - Installing the gateway CLI for macOS
---

# Gateway no macOS (lançado externo)

Openclaw.app não mais pacotes Node/Bun ou o tempo de execução Gateway. A aplicação macOS
espera um ** externo** <<CODE0>> CLI instalar, não cria o Gateway como um
processo infantil, e gerencia um serviço lançado por usuário para manter o Gateway
em execução (ou anexa-se a um Gateway local existente se já estiver em execução).

# # Instalar o CLI (obrigatório para o modo local)

Você precisa de Node 22+ no Mac, em seguida, instalar <<CODE0>> globalmente:

```bash
npm install -g openclaw@<version>
```

O botão **Install CLI** do aplicativo macOS executa o mesmo fluxo via npm/pnpm (bun não recomendado para o tempo de execução do Gateway).

# # Lançado (Portão como Agente de Lançamento)

Legenda:

- <<CODE0>> (ou <<CODE1>>; pode permanecer o legado <<CODE2>>>)

Localização da lista (por utilizador):

- <<CODE0>>
(ou <<CODE1>>>)

Gestor:

- O aplicativo macOS possui o LaunchAgent install/update no modo Local.
- O CLI também pode instalá-lo: <<CODE0>>.

Comportamento:

- “OpenClaw Active” permite/desativa o LaunchAgent.
- App quit does **not** stop the gateway (lançado mantém vivo).
- Se um Gateway já estiver em execução na porta configurada, a aplicação
em vez de começar um novo.

Registo:

- stdout/err lançado: <<CODE0>>

# # Compatibilidade com versões

O aplicativo macOS verifica a versão gateway em sua própria versão. Se eles são
incompatível, atualizar o CLI global para corresponder à versão do aplicativo.

# # Verificação de fumo

```bash
openclaw --version

OPENCLAW_SKIP_CHANNELS=1 \
OPENCLAW_SKIP_CANVAS_HOST=1 \
openclaw gateway --port 18999 --bind loopback
```

Depois:

```bash
openclaw gateway call health --url ws://127.0.0.1:18999 --timeout 3000
```
