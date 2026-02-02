---
summary: "Setup guide for developers working on the OpenClaw macOS app"
read_when:
  - Setting up the macOS development environment
---

Configuração do desenvolvedor do macOS

Este guia cobre as etapas necessárias para construir e executar o aplicativo MacOS OpenClaw a partir do código fonte.

# # Pré-requisitos

Antes de construir o aplicativo, certifique-se de ter o seguinte instalado:

1. **Xcode 26.2+**: Necessário para o desenvolvimento Swift.
2. **Node.js 22+ & pnpm**: Necessário para o gateway, CLI e scripts de embalagem.

# # 1. Instalar dependências

Instalar as dependências de todo o projeto:

```bash
pnpm install
```

# # 2. Construir e embalar o aplicativo

Para construir o aplicativo macOS e empacotá-lo em <<CODE0>>, execute:

```bash
./scripts/package-mac-app.sh
```

Se você não tiver um certificado de ID Apple Developer, o script usará automaticamente **ad-hoc signing** (<<CODE0>>).

Para modos de execução dev, sinalizadores de assinatura e solução de problemas de identificação de equipe, consulte o aplicativo macOS README:
https://github.com/openclaw/openclaw/blob/main/apps/macos/README.md

> **Nota**: Aplicativos assinados com o Ad-hoc podem desencadear avisos de segurança. Se o aplicativo falhar imediatamente com "Abort trap 6", veja a seção [Troubleshooting](<<LINK0>>>).

3. Instale o CLI

O aplicativo macOS espera um global <<CODE0> CLI instalar para gerenciar tarefas de fundo.

** Para instalá-lo (recomendado):**

1. Abra o aplicativo OpenClaw.
2. Vá para a guia **General** settings.
3. Clique em **"Instalar CLI"**.

Alternativamente, instale-o manualmente:

```bash
npm install -g openclaw@<version>
```

# # Resolução de problemas

Falhas de Construção: Toolchain ou SDK Mismatch

O macOS app build espera os mais recentes macOS SDK e Swift 6.2 toolchain.

**Dependências do sistema (obrigatórias): **

- ** Última versão do macOS disponível em Atualização de Software** (obrigatório pelo Xcode 26.2 SDKs)
- **Xcode 26.2** (Swift 6.2 toolchain)

** Verificações:**

```bash
xcodebuild -version
xcrun swift --version
```

Se as versões não corresponderem, atualize o macOS/Xcode e execute novamente a compilação.

# # App Crashes on Permission Grant

Se o aplicativo falhar quando você tentar permitir o reconhecimento de voz** ou o acesso de microfone**, ele pode ser devido a um cache TCC corrompido ou incompatibilidade de assinatura.

**Fix:**

1. Reinicie as permissões do TCC:
   ```bash
   tccutil reset All bot.molt.mac.debug
   ```
2. Se isso falhar, altere o <<CODE0>> temporariamente em [<<CODE1>>](<<LINK0>>>) para forçar uma "ardósia limpa" do macOS.

Portão a começar indefinidamente

Se o status do gateway permanecer em "Iniciar...", verifique se um processo zumbi está segurando a porta:

```bash
openclaw gateway status
openclaw gateway stop

# If you’re not using a LaunchAgent (dev mode / manual runs), find the listener:
lsof -nP -iTCP:18789 -sTCP:LISTEN
```

Se uma execução manual estiver segurando a porta, pare esse processo (Ctrl+C). Como último recurso, mate o PID que encontrou acima.
