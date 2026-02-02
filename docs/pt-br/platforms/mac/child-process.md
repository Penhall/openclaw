---
summary: "Gateway lifecycle on macOS (launchd)"
read_when:
  - Integrating the mac app with the gateway lifecycle
---

Ciclo de vida do portal no macOS

O aplicativo macOS ** gerencia o Gateway via lançado** por padrão e não gera
O portal como processo infantil. Primeiro tenta anexar a um já em execução
Gateway na porta configurada; se nenhuma for acessível, permite o lançamento
serviço através do exterior <<CODE0>>> CLI (sem tempo de execução incorporado). Isto dá-te
auto-iniciar de forma confiável no login e reiniciar em falhas.

O modo processo infantil (Gateway gerado diretamente pelo aplicativo) é **não está em uso** hoje.
Se você precisar de acoplamento mais apertado para a UI, execute o Gateway manualmente em um terminal.

# # Comportamento padrão (lançado)

- A aplicação instala um LaunchAgent de per-usuário rotulado <<CODE0>
(ou <<CODE1>> ao usar <<CODE2>/<<CODE3>>; é suportado o legado <<CODE4>).
- Quando o modo Local está ativado, o aplicativo garante que o LaunchAgent está carregado e
Começa o portal, se necessário.
- Os logs são escritos no caminho de log do gateway lançado (visível nas Configurações de Depuração).

Comandos comuns:

```bash
launchctl kickstart -k gui/$UID/bot.molt.gateway
launchctl bootout gui/$UID/bot.molt.gateway
```

Substituir o rótulo por <<CODE0>> ao executar um perfil nomeado.

# # Dev não assinado constrói

<<CODE0>> é para construções locais rápidas quando você não tem
Chaves de assinatura. Para evitar que o lançamento aponte para um binário de relé não assinado, ele:

- Escreve <<CODE0>>>.

Correções assinadas de <<CODE0> desobstruídas se o marcador for
presente. Para reiniciar manualmente:

```bash
rm ~/.openclaw/disable-launchagent
```

# # Modo somente para anexar

Para forçar o aplicativo macOS a ** nunca instalar ou gerenciar lançado**, lançá-lo com
<<CODE0>> (ou <<CODE1>>>). Isto define <<CODE2>>>,
então o aplicativo só se liga a um Gateway já em execução. Você pode alternar o mesmo
comportamento nas configurações de depuração.

# # Modo remoto

O modo remoto nunca inicia um Gateway local. A aplicação utiliza um túnel SSH para
Host remoto e conecta-se sobre aquele túnel.

# # Porque preferimos lançar

- Iniciar automaticamente o login.
- Reiniciar/Manter a semântica viva.
- Registos previsíveis e supervisão.

Se um verdadeiro modo de processo-criança for necessário novamente, deve ser documentado como
modo separado e explícito apenas dev.
