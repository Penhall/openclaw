---
summary: "Linux support + companion app status"
read_when:
  - Looking for Linux companion app status
  - Planning platform coverage or contributions
---

# Aplicativo Linux

O Gateway é totalmente suportado no Linux. **Node é o tempo de execução recomendado**.
Bun não é recomendado para o Gateway (WhatsApp/Telegram bugs).

Aplicativos companheiras do Linux nativos são planejados. Contribuições são bem-vindas se você quiser ajudar a construir uma.

# # Caminho rápido iniciante (VPS)

1. Instalar o Nó 22+
2. <<CODE0>>
3. <<CODE1>>
4. Do seu laptop: <<CODE2>>
5. Abra <<CODE3>> e cole seu token

Guia passo a passo do VPS: [exe.dev] (<<<LINK0>>>)

Instalar

- [Começar] (<<<LINK0>>>)
- [Instalar e actualizar] (<<<LINK1>>>)
- Fluxos opcionais: [Bun (experimental)](<<<LINK2>>>), [Nix] (<<LINK3>>>>), [Docker](<<LINK4>>>)

# # Gateway

- [O livro de instruções do portal] (<<<LINK0>>>)
- [Configuração] (<<<LINK1>>>)

# # Serviço de gateway instalar (CLI)

Utilizar um destes:

```
openclaw onboard --install-daemon
```

Ou:

```
openclaw gateway install
```

Ou:

```
openclaw configure
```

Selecione **Serviço Gateway** quando solicitado.

Reparação/migração:

```
openclaw doctor
```

# # Controle de sistema (unidade de usuário sistemad)

OpenClaw instala um serviço systemd **user** por padrão. Usar um sistema **
serviço para servidores compartilhados ou sempre-em. Exemplo de unidade completa e orientação
(<<<LINK0>>>).

Configuração mínima:

Criar <<CODE0>>:

```
[Unit]
Description=OpenClaw Gateway (profile: <profile>, v<version>)
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/openclaw gateway --port 18789
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

Activar:

```
systemctl --user enable --now openclaw-gateway[-<profile>].service
```
