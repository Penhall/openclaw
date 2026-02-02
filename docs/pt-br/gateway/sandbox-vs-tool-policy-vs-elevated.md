---
title: Sandbox vs Tool Policy vs Elevated
summary: "Why a tool is blocked: sandbox runtime, tool allow/deny policy, and elevated exec gates"
read_when: "You hit 'sandbox jail' or see a tool/elevated refusal and want the exact config key to change."
status: active
---

# Sandbox vs Tool Policy vs Elevated

Openclaw tem três controles relacionados (mas diferentes):

1. **Sandbox** (<<<CODE0>> / <<CODE1>>>) decide **onde as ferramentas são executadas** (Docker vs host).
2. **A política da ferramenta** (<<<CODE2>>, <<CODE3>>, <<CODE4>>) decide **que ferramentas estão disponíveis/permitidas**.
3. **Elevado** (<<<CODE5>, <<CODE6>>) é uma escotilha de escape **exec-somente** para funcionar no hospedeiro quando você é sandboxed.

# # Depurar rapidamente

Use o inspetor para ver o que OpenClaw é  na verdade  fazendo:

```bash
openclaw sandbox explain
openclaw sandbox explain --session agent:main:main
openclaw sandbox explain --agent work
openclaw sandbox explain --json
```

Imprime:

- modo de sandbox/scópio/espaço de trabalho eficaz
- se a sessão está atualmente em sandbox (principal vs não principal)
- ferramenta de sandbox eficaz permitir/negar (e se veio de agente/global/default)
- portões elevados e caminhos chave fixo

# # Caixa de areia: onde as ferramentas funcionam

O Sandboxing é controlado por <<CODE0>>:

- <<CODE0>>: tudo é executado no host.
- <<CODE1>>: apenas sessões não principais são sandboxed (surpresa comum para grupos/canais).
- <<CODE2>>: tudo está em caixa de areia.

Veja [Sandboxing](<<<LINK0>>>) para a matriz completa (scópio, montagens de espaço de trabalho, imagens).

Montes de ligação (verificação rápida de segurança)

- <<CODE0>  pierces  o sistema de ficheiros sandbox: o que quer que monte é visível dentro do recipiente com o modo definido (<<CODE1>> ou <<CODE2>>>).
- O padrão é ler-escrever se você omitir o modo; prefira <<CODE3>> para fonte/segredos.
- <<CODE4>> ignora as ligações por agente (só se aplicam ligações globais).
- Ligando <<CODE5> efetivamente mãos host controle para a caixa de areia; apenas fazê-lo intencionalmente.
- O acesso ao espaço de trabalho (<<<CODE6>/<HTML7>>>>) é independente dos modos de ligação.

# # Política de ferramentas: quais ferramentas existem/são chamadas

Duas camadas de matéria:

- ** Perfil da ferramenta**: <<CODE0>> e <<CODE1>> (lista de licenças de base)
- ** Perfil da ferramenta fornecido**: <<CODE2>> e <<CODE3>>
- ** Política da ferramenta global/peragente**: <<CODE4>>/<<CODE5>> e <<CODE6>>/<<CODE7>>
- **Política de ferramentas de fornecimento**: <<CODE8>> e <<CODE9>>
- ** Política da ferramenta da caixa de areia** (apenas se aplica quando sandboxed): <<CODE10>/<<CODE11>> e <<CODE12>>

Regras do polegar:

- <<CODE0> sempre vence.
- Se <<CODE1> não for vazio, todo o resto é tratado como bloqueado.
- Política de ferramenta é a parada difícil: <<CODE2> não pode substituir uma ferramenta negada <<CODE3>>.
- <<CODE4> apenas altera os padrões de sessão para remetentes autorizados; não concede acesso à ferramenta.
As chaves da ferramenta do fornecedor aceitam ou <<CODE5> (por exemplo, <<CODE6>>>) ou <<CODE7>> (por exemplo, <<CODE8>>>>).

Grupos de ferramentas (shorthands)

Políticas de ferramentas (global, agente, sandbox) suportam <<CODE0> entradas que se expandem para múltiplas ferramentas:

```json5
{
  tools: {
    sandbox: {
      tools: {
        allow: ["group:runtime", "group:fs", "group:sessions", "group:memory"],
      },
    },
  },
}
```

Grupos disponíveis:

- <<CODE0>>: <<CODE1>>, <<CODE2>>, <<CODE3>>
- <<CODE4>>: <<CODE5>>, <<CODE6>>, <<CODE7>>, <<CODE8>
- <<CODE9>>: <<CODE10>>, <<CODE11>>, <<CODE12>>, <<CODE13>>, <<CODE14>>
- <<CODE15>>: <<CODE16>>, <<CODE17>>
- <<CODE18>>: <<CODE19>>, <<CODE20>>
- <<CODE21>>: <<CODE22>>>, <<CODE23>>
- <<CODE24>>: <<CODE25>>
- <<CODE26>>: <<CODE27>>
- <<CODE28>>: todas as ferramentas OpenClaw incorporadas (exclui plugins de provedores)

# # Elevado: exec-somente “run on host”

Elevado faz **not** concede ferramentas extras; afeta apenas <<CODE0>>>.

- Se tiver uma caixa de areia, <<CODE0>> (ou <<CODE1>>> com <<CODE2>>) é executado no hospedeiro (podem ainda ser aplicadas homologações).
- Utilizar <<CODE3> para ignorar as aprovações executivas para a sessão.
- Se você já está correndo direto, elevado é efetivamente um no-op (ainda fechado).
- Elevado é **not** habilidade-escoberto e não ** ferramenta de sobreposição permitir / negar.
- <<CODE4> está separado do elevado. Ele só ajusta os padrões de execução por sessão para os remetentes autorizados.

Gates:

- Habilitação: <<CODE0>> (e opcionalmente <<CODE1>>)
- Listas de permissões do remetente: <<CODE2>> (e opcionalmente <<CODE3>>)

Ver [Modo Elevado] (<<<LINK0>>>).

# # Correções comuns da “caixa de areia”

### “Ferramenta X bloqueada pela política de ferramentas sandbox”

Chaves de correção (escolha uma):

- Desactivar a caixa de areia: <<CODE0>> (ou por agente <<CODE1>>>)
- Permitir a ferramenta dentro da caixa de areia:
- removê- la de <<CODE2>> (ou por agente <<CODE3>>)
- ou adicioná- lo a <<CODE4> (ou por agente permitir)

## # “Pensei que isto era principal, por que é sandboxed?”

No modo <<CODE0>, as teclas de grupo/canal são  not  main. Use a tecla de sessão principal (mostrada por <<CODE1>>>) ou mude para <<CODE2>>>.
