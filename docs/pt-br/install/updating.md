---
summary: "Updating OpenClaw safely (global install or source), plus rollback strategy"
read_when:
  - Updating OpenClaw
  - Something breaks after an update
---

A actualizar

Openclaw está se movendo rápido (pré “1.0”). Tratar atualizações como infra de envio: update → executar verificações → reiniciar (ou usar <<CODE0>>, que reinicia) → verificar.

# # # Recomendado: executar novamente o instalador do site (atualizar no lugar)

O caminho de atualização ** preferido** é executar novamente o instalador do site. Ele
detecta instalações existentes, atualizações no local e executa <<CODE0>> quando
Necessário.

```bash
curl -fsSL https://openclaw.bot/install.sh | bash
```

Notas:

- Adicione <<CODE0>> se você não quiser que o assistente de onboarding execute novamente.
- Para **installs fonte**, use:
  ```bash
  curl -fsSL https://openclaw.bot/install.sh | bash -s -- --install-method git --no-onboard
  ```
O instalador do programa é chamado geralmente de <<CODE0>> ** somente** se o repo estiver limpo.
- Para **instalações globais**, o script usa <<CODE1>> sob o capô.
- Nota de legado: <<CODE2>>> permanece disponível como um shim compatibilidade.

# # Antes de atualizar

- Saiba como você instalou: **global** (npm/pnpm) vs **do source** (git clone).
- Saiba como seu Gateway está rodando: **foreground terminal** vs ** supervised service** (lançado/systemd).
- Dispara a tua alfaiataria:
- Configuração: <<CODE0>>
- Credenciais: <<CODE1>>
- Espaço de trabalho: <<CODE2>>

# # Atualização (instalação global)

Instalação global (escolha um):

```bash
npm i -g openclaw@latest
```

```bash
pnpm add -g openclaw@latest
```

Nós fazemos **not** recomendamos Bun para o tempo de execução Gateway (WhatsApp/Telegram bugs).

Para alternar canais de atualização (git + npm instala):

```bash
openclaw update --channel beta
openclaw update --channel dev
openclaw update --channel stable
```

Use <<CODE0>> para uma única instalação tag/versão.

Veja [Canais de desenvolvimento](<<<LINK0>>) para semântica de canal e notas de lançamento.

Nota: no npm instala, o gateway registra uma dica de atualização na inicialização (verifica a tag do canal atual). Desactivar via <<CODE0>>>.

Depois:

```bash
openclaw doctor
openclaw gateway restart
openclaw health
```

Notas:

- Se o seu Gateway for executado como serviço, <<CODE0>> é preferível sobre matar PIDs.
- Se estiver preso a uma versão específica, consulte “Rollback / pinning” abaixo.

## Atualização (<<<CODE0>>)

Para **installs de código** (git checkout), prefira:

```bash
openclaw update
```

Ele executa um fluxo de atualização seguro:

- Requer uma árvore limpa.
- Muda para o canal seleccionado (marca ou ramo).
- Fetches + rebases contra o upstream configurado (canal de dev).
- Instala deps, compila, constrói a interface de controle e executa <<CODE0>>.
- Reinicia o gateway por padrão (use <<CODE1> para pular).

Se você instalou via **npm/pnpm** (sem metadados git), <<CODE0>> irá tentar atualizar através do seu gerenciador de pacotes. Se não conseguir detectar a instalação, use “Atualizar (instalar global)” em vez disso.

# # Atualização (UI de controle / RPC)

A interface de controle tem **Update & Reirt** (RPC: <<CODE0>>). Ele:

1. Executa o mesmo fluxo fonte-atualização que <<CODE0>> (apenas checkout git).
2. Escreve uma sentinela reinicial com um relatório estruturado (stdout/stderr tail).
3. Reinicia o gateway e pings a última sessão ativa com o relatório.

Se o rebase falhar, o gateway aborta e reinicia sem aplicar a atualização.

# # Atualização (da fonte)

A partir do repo checkout:

Preferido:

```bash
openclaw update
```

Manual (equivalente-ish):

```bash
git pull
pnpm install
pnpm build
pnpm ui:build # auto-installs UI deps on first run
openclaw doctor
openclaw health
```

Notas:

- <<CODE0> importa quando executa o pacote <<CODE1>>binário ([<<CODE2>>](<<LINK0>>) ou usa Node para executar <<CODE3>>>>>.
- Se você correr a partir de um repo checkout sem uma instalação global, use <<CODE4>> para comandos CLI.
- Se você correr diretamente do TypeScript (<<<CODE5>>), uma reconstrução é geralmente desnecessária, mas ** migrações de configuração ainda se aplicam** → executar doutor.
- Alternar entre instalações globais e git é fácil: instale o outro sabor, então execute <<CODE6>> para que o ponto de entrada do serviço de gateway seja reescrito para a instalação atual.

# # Sempre Executar: <<CODE0>>

O médico é o comando “atualização segura”. É intencionalmente chato: reparação + migrar + avisar.

Nota: se você estiver em uma instalação **source** (git checkout), <<CODE0>> vai oferecer para executar <<CODE1>> Primeiro.

Coisas típicas que faz:

- Migrar chaves de configuração deprecadas / locais de arquivos de configuração legados.
- Auditoria de políticas de DM e alertar sobre as configurações de risco “aberto”.
- Verifique a saúde do portal e pode oferecer-se para reiniciar.
- Detectar e migrar serviços de gateway antigos (lançados/sistemas; schtasks legados) para serviços OpenClaw atuais.
- No Linux, garanta a permanência do usuário do sistema (assim o Gateway sobrevive ao logout).

Detalhes: [Doctor](<<<LINK0>>>)

# # Começar / parar / reiniciar o portal

CLI (trabalha independentemente do sistema operacional):

```bash
openclaw gateway status
openclaw gateway stop
openclaw gateway restart
openclaw gateway --port 18789
openclaw logs --follow
```

Se você é supervisionado:

- macOS lançado (app-bundled LaunchAgent): <<CODE0>> (use <<CODE1>>>; legado <<CODE2> ainda funciona)
- Serviço de usuário do sistema Linux: <<CODE3>>
- Windows (WSL2): <<CODE4>>
- <<CODE5>>/<<CODE6>> só funciona se o serviço estiver instalado; caso contrário, execute <<CODE7>>>.

Runbook + etiquetas de serviço exatas: [Runbook de Gateway] (<<<LINK0>>)

# # Retroceder / girar (quando algo quebra)

Pin (instalação global)

Instale uma versão conhecida-boa (substitua <<CODE0>> com a última versão funcional):

```bash
npm i -g openclaw@<version>
```

```bash
pnpm add -g openclaw@<version>
```

Dica: para ver a versão atual publicada, execute <<CODE0>>>.

Em seguida, reiniciar + re- executar médico:

```bash
openclaw doctor
openclaw gateway restart
```

## # Pin (fonte) por data

Escolha um commit a partir de uma data (exemplo: “estado do principal a partir de 2026-01-01”):

```bash
git fetch origin
git checkout "$(git rev-list -n 1 --before=\"2026-01-01\" origin/main)"
```

Em seguida, reinstalar deps + reiniciar:

```bash
pnpm install
pnpm build
openclaw gateway restart
```

Se você quiser voltar para o último mais tarde:

```bash
git checkout main
git pull
```

# # Se você está preso

- Executar <<CODE0>> novamente e ler a saída com cuidado (que muitas vezes lhe diz a correção).
- Verificar: [Respondência de problemas] (<<<LINK0>>>)
- Perguntar na Discórdia: https://canals.discord.gg/clawd
