---
summary: "Troubleshooting hub: symptoms → checks → fixes"
read_when:
  - You see an error and want the fix path
  - The installer says “success” but the CLI doesn’t work
---

# Resolução de problemas

# # Primeiros 60 segundos

Execute isto em ordem:

```bash
openclaw status
openclaw status --all
openclaw gateway probe
openclaw logs --follow
openclaw doctor
```

Se o portal for acessível, sondas profundas:

```bash
openclaw status --deep
```

# # Comum “quebrou” casos

## # <<CODE0>>

Quase sempre uma questão de NODE/NPM PATH. Comece aqui:

- [Instalar (Node/npm PATH sanity)] (<<<<LINK0>>>)

## # O instalador falha (ou você precisa de logs completos)

Executar novamente o instalador em modo verbose para ver o traço completo e saída npm:

```bash
curl -fsSL https://openclaw.bot/install.sh | bash -s -- --verbose
```

Para instalações beta:

```bash
curl -fsSL https://openclaw.bot/install.sh | bash -s -- --beta --verbose
```

Você também pode definir <<CODE0>> em vez da bandeira.

## # Gateway “não autorizado”, não pode conectar, ou continua reconectando

- [Solução de problemas de Gateway] (<<< HTML0>>>)
- [Autenticação do portal] (<<<<LINK1>>>)

### A interface de controle falha em HTTP (identidade do dispositivo necessária)

- [Solução de problemas de Gateway] (<<< HTML0>>>)
- [IU de controlo] (<<<LINK1>>>)

#### <<CODE0> mostra um erro SSL (Comcast/Xfinity)

Alguns blocos de conexões Comcast/Xfinity <<CODE0>> via Xfinity Advanced Security.
Desabilitar Segurança Avançada ou adicionar <<CODE1>> à lista de allowlist, então tente novamente.

- Xfinity Advanced Security help: https://www.xfinity.com/suport/articles/using-xfinity-xfi-avanced-security
- Verificação rápida da sanidade mental: tente um hotspot móvel ou VPN para confirmar sua filtragem nível ISP

# # # Serviço diz execução, mas a sonda RPC falha

- [Solução de problemas de Gateway] (<<< HTML0>>>)
- [Processo de fundo / serviço] (<<<LINK1>>>)

### Falhas no modelo/auth (limite de taxa, faturamento, “todos os modelos falharam”)

- [Modelos] (<<<LINK0>>)
- [conceitos de Auth / Auth] (<<<LINK1>>>)

## # <<CODE0> diz <<CODE1>>

Isso geralmente significa que <<CODE0>> é configurado como uma lista de permissões. Quando não estiver vazio,
Só podem ser seleccionadas as chaves fornecedor/modelo.

- Verifique a lista de permissões: <<CODE0>>
- Adicione o modelo que deseja (ou limpe a lista de permissões) e tente novamente <<CODE1>>
- Use <<CODE2>> para navegar pelos provedores/modelos permitidos

# # Ao arquivar um problema

Colar um relatório seguro:

```bash
openclaw status --all
```

Se puder, inclua a cauda de log relevante de <<CODE0>>>.
