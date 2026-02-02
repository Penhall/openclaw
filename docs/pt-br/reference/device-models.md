---
summary: "How OpenClaw vendors Apple device model identifiers for friendly names in the macOS app."
read_when:
  - Updating device model identifier mappings or NOTICE/license files
  - Changing how Instances UI displays device names
---

# Banco de dados de modelos de dispositivos (nomes amigos)

O app companheiro do macOS mostra nomes de modelos de dispositivos Apple amigáveis na **Instances** UI mapeando identificadores de modelos Apple (por exemplo, `iPad16,6`, `Mac16,6`) para nomes legíveis por humanos.

O mapeamento é vendido como JSON em:

- <<CODE0>

# # Fonte de dados

Atualmente vendemos o mapeamento do repositório licenciado pelo MIT:

- <<CODE0>

Para manter builds deterministic, os arquivos JSON são fixados a commits upstream específicos (gravados em `apps/macos/Sources/OpenClaw/Resources/DeviceModels/NOTICE.md`).

# # Atualizando a base de dados

1. Pegue os commits upstream que você deseja fixar (um para iOS, um para macOS).
2. Atualizar os hashes do commit em `apps/macos/Sources/OpenClaw/Resources/DeviceModels/NOTICE.md`.
3. Re-download os arquivos JSON, presos a esses commits:

```bash
IOS_COMMIT="<commit sha for ios-device-identifiers.json>"
MAC_COMMIT="<commit sha for mac-device-identifiers.json>"

curl -fsSL "https://raw.githubusercontent.com/kyle-seongwoo-jun/apple-device-identifiers/${IOS_COMMIT}/ios-device-identifiers.json" \
  -o apps/macos/Sources/OpenClaw/Resources/DeviceModels/ios-device-identifiers.json

curl -fsSL "https://raw.githubusercontent.com/kyle-seongwoo-jun/apple-device-identifiers/${MAC_COMMIT}/mac-device-identifiers.json" \
  -o apps/macos/Sources/OpenClaw/Resources/DeviceModels/mac-device-identifiers.json
```

4. Certifique-se de <<CODE0> ainda corresponde upstream (substituir se a licença upstream muda).
5. Verifique o aplicativo macOS constrói de forma limpa (sem avisos):

```bash
swift build --package-path apps/macos
```
