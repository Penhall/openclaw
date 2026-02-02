---
summary: "How OpenClaw sandboxing works: modes, scopes, workspace access, and images"
title: Sandboxing
read_when: "You want a dedicated explanation of sandboxing or need to tune agents.defaults.sandbox."
status: active
---

# Sandboxing

OpenClaw pode executar **tools dentro de recipientes Docker** para reduzir o raio de explosão.
Isto é ** opcional** e controlado por configuração (<<<CODE0>> ou
<<CODE1>>). Se o Sandboxing estiver desligado, as ferramentas são executadas no host.
O Gateway permanece na máquina; a execução da ferramenta é executada em uma caixa de areia isolada
quando activado.

Este não é um limite de segurança perfeito, mas limita materialmente o sistema de arquivos
e processar o acesso quando o modelo faz algo mudo.

# # O que é enterrado

- Execução da ferramenta (<<<CODE0>>, <<CODE1>>, <<CODE2>>, <<CODE3>>, <<CODE4>>, <<CODE5>>, etc.).
- Navegador opcional sandboxed (<<<CODE6>>>).
- Por padrão, o navegador sandbox inicia automaticamente (ensure CDP é acessível) quando a ferramenta do navegador precisa dele.
Configurar via <<CODE7>> e <<CODE8>>>>>.
- <<CODE9>> permite que sessões sandboxed alvo do navegador host explicitamente.
- Porta opcional de listas de autorizações <<CODE10>>: <<CODE11>>, <<CODE12>>, <<CODE13>>.

Caixa de areia não:

- O processo do portal em si.
- Qualquer ferramenta explicitamente autorizada a ser executada na máquina (por exemplo, <<CODE0>>>).
- **Exec elevado corre no host e ignora sandboxing.**
- Se o sandboxing estiver desligado, <<CODE1> não altera a execução (já na máquina). Ver [Modo Elevado] (<<<LINK0>>>).

# # Modos

<<CODE0> controles **quando ** sandboxing é usado:

- <<CODE0>>: sem sandboxing.
- <<CODE1>>: sandbox somente **não-main** sessions (default if you want normal chats on host).
- <<CODE2>>: cada sessão é executada em uma caixa de areia.
Nota: <<CODE3> é baseado em <<CODE4>>> (padrão <<CODE5>>>), não no agente id.
Sessões de grupo/canal usam suas próprias chaves, então elas contam como não principais e serão sandboxed.

# # Escopo

<<CODE0> controles ** Quantos recipientes** são criados:

- <<CODE0> (padrão): um recipiente por sessão.
- <<CODE1>: um recipiente por agente.
- <<CODE2>: um recipiente partilhado por todas as sessões sandbox.

# # Acesso ao espaço de trabalho

<<CODE0> controles **o que a caixa de areia pode ver**:

- <<CODE0>> (default): ferramentas ver um espaço de trabalho sandbox em <<CODE1>>>.
- <<CODE2>: monta apenas o espaço de trabalho do agente em <<CODE3>> (desactivações <<CODE4>>/<<CODE5>/<<CODE6>>).
- <<CODE7>>: monta o espaço de trabalho do agente em <<CODE8>>.

A mídia de entrada é copiada para a área de trabalho da sandbox ativa (<<CODE0>>).
Nota de habilidades: a ferramenta <<CODE1> é enraizada em sandbox. Com <<CODE2>>,
OpenClaw espelha habilidades elegíveis para o espaço de trabalho sandbox (<<CODE3>>>) assim
eles podem ser lidos. Com <<CODE4>>, as habilidades de espaço de trabalho são legíveis a partir de
<<CODE5>>.

# # Montagens personalizadas

<<CODE0> monta diretórios de host adicionais no recipiente.
Formato: <<CODE1>> (p. ex., <<CODE2>>>).

As ligações globais e por agente são ** misturadas** (não substituídas). Em <<CODE0>>, as ligações por agente são ignoradas.

Exemplo (somente fonte de leitura + socket docker):

```json5
{
  agents: {
    defaults: {
      sandbox: {
        docker: {
          binds: ["/home/user/source:/source:ro", "/var/run/docker.sock:/var/run/docker.sock"],
        },
      },
    },
    list: [
      {
        id: "build",
        sandbox: {
          docker: {
            binds: ["/mnt/cache:/cache:rw"],
          },
        },
      },
    ],
  },
}
```

Notas de segurança:

- Binds bypass the sandbox filesystem: eles expõem caminhos de host com qualquer modo que você definir (<<CODE0>> ou <<CODE1>>).
- As montagens sensíveis (por exemplo, <<CODE2>>, segredos, chaves SSH) devem ser <<CODE3> A menos que seja absolutamente necessário.
- Combine com <<CODE4>> se você só precisa de acesso de leitura para o espaço de trabalho; vincular modos permanecer independente.
- Veja [Sandbox vs Tool Policy vs Elevated](<<<LINK0>>>) para como se liga interagir com a política de ferramenta e executivo elevado.

# # Imagens + configuração

Imagem padrão: <<CODE0>>>

Construir uma vez:

```bash
scripts/sandbox-setup.sh
```

Nota: a imagem padrão não ** inclui Node. Se uma habilidade precisa de Nó (ou
outros tempos de execução), quer cozer uma imagem personalizada ou instalar via
<<CODE0>> (necessita de saída de rede + raiz gravável +
root user).

Imagem do navegador Sandboxed:

```bash
scripts/sandbox-browser-setup.sh
```

Por padrão, os recipientes sandbox rodam com ** nenhuma rede**.
Substituir por <<CODE0>>>.

O Docker instala e o gateway contêiner vive aqui:
[Docker] (<<<LINK0>>)

## configuraçãoComando (uma vez configuração do recipiente)

<<CODE0> roda ** uma vez** depois que o recipiente sandbox é criado (não em cada execução).
Ele executa dentro do recipiente via <<CODE1>>>.

Caminhos:

- Global: <<CODE0>>
- Por agente: <<CODE1>>>

Inimigos comuns:

- O padrão <<CODE0>> é <<CODE1>> (sem saída), então as instalações do pacote falharão.
- <<CODE2> previne escrever; definir <<CODE3>> ou fazer uma imagem personalizada.
- <<CODE4>> deve ser root para instalações de pacotes (omite <<CODE5>> ou definido <<CODE6>>).
- Sandbox exec faz ** not** herdar host <<CODE7>>. Utilização
<<CODE8> (ou uma imagem personalizada) para chaves API de habilidade.

# # Política de ferramentas + escotilhas de escape

As políticas de allow/deny da ferramenta ainda se aplicam antes das regras do sandbox. Se uma ferramenta for negada
globalmente ou por agente, sandboxing não traz de volta.

<<CODE0> é uma escotilha de escape explícita que corre <<CODE1>> no hospedeiro.
<<CODE2> diretivas só se aplicam para remetentes autorizados e persistem por sessão; para desativação difícil
<<CODE3>, use a política de ferramentas nega (veja [Sandbox vs Tool Policy vs Elevated](<<LINK0>>)).

Depuração:

- Use <<CODE0>> para inspecionar o modo de sandbox efetivo, a política de ferramentas e as chaves de configuração de correção.
- Veja [Sandbox vs Tool Policy vs Elevated](<<<LINK0>>>) para o “por que isso está bloqueado?” modelo mental.
Mantém-na fechada.

# # Multi-agente substitui

Cada agente pode substituir sandbox + ferramentas:
<<CODE0>> e <<CODE1>> (mais <<CODE2>> para a política de ferramentas sandbox).
Veja [Multi-Agent Sandbox & Tools] (<<<LINK0>>>) para precedência.

# # Exemplo mínimo de habilitação

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        scope: "session",
        workspaceAccess: "none",
      },
    },
  },
}
```

# # Docs relacionados

- [Configuração da caixa de areia] (<<<LINK0>>)
- [Multi-Agent Sandbox & Tools] (<<<LINK1>>)
- [Segurança]
