---
summary: "Menu bar status logic and what is surfaced to users"
read_when:
  - Tweaking mac menu UI or status logic
---

# Lógica de status da barra de menu

# # O que é mostrado

- Surge o estado de trabalho do agente atual no ícone da barra de menus e na primeira linha de status do menu.
- O estado de saúde está oculto enquanto o trabalho está ativo; ele retorna quando todas as sessões estão ociosas.
- O bloco “Nodes” na lista de menus **dispositivos** apenas (nós pareados via <<CODE0>>>), não entradas cliente/presença.
- Uma seção “Usagem” aparece no contexto quando os instantâneos de uso do provedor estão disponíveis.

# # Modelo estatal

- Sessões: os eventos chegam com <<CODE0>> (por execução) mais <<CODE1>> na carga útil. A “sessão principal” é a chave <<CODE2>>; se ausente, voltamos à sessão mais atualizada.
Prioridade: o principal ganha sempre. Se o principal estiver ativo, seu estado é mostrado imediatamente. Se o main estiver ocioso, a sessão não principal mais recente é mostrada. Não mudamos a atividade média; só mudamos quando a sessão atual fica ociosa ou a principal fica ativa.
- Tipos de actividade:
- <<CODE3>>: execução de comandos de alto nível (<<CODE4>>>).
- <<CODE5>>: <<CODE6>> com <<CODE7>> e <<CODE8>>.

# # IconState enum (Swift)

- <<CODE0>>
- <<CODE1>>
- <<CODE2>>
- <<CODE3> (sobreposição de depuração)

## # AtividadeKind → glifo

- <<CODE0> →
- <<CODE1> →
- <<CODE2>> →
- <<CODE3> →
- <<CODE4> →
- predefinir →

## # Mapeamento visual

- <<CODE0>>: criatura normal.
- <<CODE1>>: emblema com glifo, tonalidade completa, animação “trabalhando” na perna.
- <<CODE2>>: emblema com glifo, cor muda, sem correr.
- <<CODE3>>: utiliza o glifo/tinto escolhido, independentemente da actividade.

# # Texto da linha do estado (menu)

- Enquanto o trabalho está activo: <<CODE0>>
- Exemplos: <<CODE1>>, <<CODE2>>>>.
- Quando ocioso: volta para o resumo de saúde.

# # Ingestão de eventos

- Fonte: canal de controlo <<CODE0>> acontecimentos (<<CODE1>>).
- Campos analisados:
- <<CODE2>> com <<CODE3>> para iniciar/ parar.
- <<CODE4>> com <<CODE5>>, <<CODE6>>, opcional <<CODE7>>/<<CODE8>.
- Etiquetas:
- <<CODE9>>: primeira linha de <<CODE10>>.
- <<CODE11>/<<CODE12>>: caminho encurtado.
- <<CODE13>>: caminho mais mudança inferida tipo de <<CODE14>>/diff contagens.
- Retrocesso: nome da ferramenta.

# # Sobreposição de depuração

- Configurações de Depuração do escolhedor de “arranque de ícone”:
- <<CODE0> (padrão)
- <<CODE1> (por tipo de ferramenta)
- <<CODE2> (por tipo de ferramenta)
- <<CODE3>>
- Armazenada via <<CODE4>>; mapeada para <<CODE5>>.

# # Lista de testes

- Activar a tarefa principal da sessão: verificar os interruptores de ícones imediatamente e a linha de estado mostra a legenda principal.
- Activar o trabalho de sessão não principal enquanto o ícone/status principal estiver inactivo: o ícone/status mostra o não-main; mantém-se estável até terminar.
- Iniciar principal enquanto outro ativo: ícone gira para principal instantaneamente.
- Explosões rápidas de ferramentas: garantir que o crachá não tremula (graça TTL nos resultados da ferramenta).
- O corredor de saúde reaparece uma vez que todas as sessões ocioso.
