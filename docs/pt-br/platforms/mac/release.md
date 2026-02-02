---
summary: "OpenClaw macOS release checklist (Sparkle feed, packaging, signing)"
read_when:
  - Cutting or validating a OpenClaw macOS release
  - Updating the Sparkle appcast or feed assets
---

# OpenClaw lançamento macOS (Sparkle)

Este aplicativo agora envia as atualizações automáticas da Sparkle. Compilações de lançamento devem ser assinadas, zipadas e publicadas com uma entrada de appcast assinada.

# # Pré-reques

- Certificado de ID do desenvolvedor instalado (exemplo: <<CODE0>>>).
- Caminho da chave privada Sparkle definido no ambiente como <<CODE1>> (caminho para a sua chave privada Sparkle ed25519; chave pública assada no Info.plist). Se faltar, verifique <<CODE2>>>>.
- Credenciais notários (perfil de chaveiro ou chave API) para <<CODE3>> se você quiser distribuição DMG/zip segura Gatekeeper.
- Usamos um perfil Keychain chamado <<CODE4>>, criado a partir do app Store Connect API chave env vars em seu perfil shell:
- <<CODE5>>, <<CODE6>>, <<CODE7>>
- <<CODE8>>
- <<CODE9>>
- <<CODE10>> deps instalados (<<CODE11>>>).
- As ferramentas Sparkle são obtidas automaticamente via SwiftPM em <<CODE12>> (<<CODE13>>, <<CODE14>>>, etc.).

# # Compilar & pacote

Notas:

- <<CODE0>> mapas para <<CODE1>>/<<CODE2>>; mantê-lo numérico + monotónico (não <<CODE3>>), ou Sparkle compara-o como igual.
- Padrão para a arquitetura atual (<<<CODE4>>>). Para lançamento/compilações universais, definir <<CODE5>> (ou <<CODE6>>>).
- Usar <<CODE7>> para artefatos de liberação (zip + DMG + notarização). Utilizar <<CODE8>> para embalagem local/dev.

```bash
# From repo root; set release IDs so Sparkle feed is enabled.
# APP_BUILD must be numeric + monotonic for Sparkle compare.
BUNDLE_ID=bot.molt.mac \
APP_VERSION=2026.1.27-beta.1 \
APP_BUILD="$(git rev-list --count HEAD)" \
BUILD_CONFIG=release \
SIGN_IDENTITY="Developer ID Application: <Developer Name> (<TEAMID>)" \
scripts/package-mac-app.sh

# Zip for distribution (includes resource forks for Sparkle delta support)
ditto -c -k --sequesterRsrc --keepParent dist/OpenClaw.app dist/OpenClaw-2026.1.27-beta.1.zip

# Optional: also build a styled DMG for humans (drag to /Applications)
scripts/create-dmg.sh dist/OpenClaw.app dist/OpenClaw-2026.1.27-beta.1.dmg

# Recommended: build + notarize/staple zip + DMG
# First, create a keychain profile once:
#   xcrun notarytool store-credentials "openclaw-notary" \
#     --apple-id "<apple-id>" --team-id "<team-id>" --password "<app-specific-password>"
NOTARIZE=1 NOTARYTOOL_PROFILE=openclaw-notary \
BUNDLE_ID=bot.molt.mac \
APP_VERSION=2026.1.27-beta.1 \
APP_BUILD="$(git rev-list --count HEAD)" \
BUILD_CONFIG=release \
SIGN_IDENTITY="Developer ID Application: <Developer Name> (<TEAMID>)" \
scripts/package-mac-dist.sh

# Optional: ship dSYM alongside the release
ditto -c -k --keepParent apps/macos/.build/release/OpenClaw.app.dSYM dist/OpenClaw-2026.1.27-beta.1.dSYM.zip
```

# # Entrada do Appcast

Use o gerador de notas de lançamento para que Sparkle renderize notas HTML formatadas:

```bash
SPARKLE_PRIVATE_KEY_FILE=/path/to/ed25519-private-key scripts/make_appcast.sh dist/OpenClaw-2026.1.27-beta.1.zip https://raw.githubusercontent.com/openclaw/openclaw/main/appcast.xml
```

Gera notas de lançamento HTML de <<CODE0>> (via [<<CODE1>>](<<LINK0>>>) e as incorpora na entrada do appcast.
Persistir o atualizado <<CODE2>> ao lado dos ativos de lançamento (zip + dSYM) ao publicar.

# # Publicar & verificar

- Enviar <<CODE0>> (e <<CODE1>>) para a versão GitHub para tag <<CODE2>.
- Assegure-se de que o URL do appcast bruto corresponde ao feed cozido: <<CODE3>>.
- Controlos de sanidade:
- <<CODE4> retorna 200.
- <<CODE5> retorna 200 após o upload dos ativos.
- Em uma compilação pública anterior, execute “Verificar atualizações...” da aba Sobre e verifique se Sparkle instala a nova compilação de forma limpa.

Definição de feito: app + appcast assinado são publicados, o fluxo de atualização funciona a partir de uma versão mais antiga instalada, e os ativos de lançamento são anexados à versão GitHub.
