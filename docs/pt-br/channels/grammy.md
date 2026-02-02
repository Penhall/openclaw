---
summary: "Telegram Bot API integration via grammY with setup notes"
read_when:
  - Working on Telegram or grammY pathways
---

# Integração gramamY (Telegram Bot API)

# Por que GrammY

- TS-first Bot cliente API com built-in longo-poll + webhook helpers, middleware, manipulação de erros, limitador de taxa.
- Ajudadores de mídia mais limpos do que obter + FormData; suporta todos os métodos Bot API.
- Extensível: suporte proxy via busca personalizada, middleware de sessão (opcional), contexto tipo seguro.

O que enviamos

- **Single client path:** fetch-based implementation removido; GrammY é agora o único cliente do Telegram (enviar + gateway) com o grammY throttler ativado por padrão.
- **Gateway:**`monitorTelegramProvider`constrói um`Bot`gramamY, fios mention/allowlist gating, mídia download via`getFile`/`download`, e fornece respostas com`sendMessage/sendPhoto/sendVideo/sendAudio/sendDocument`. Suporta cabo longo ou webhook via`webhookCallback`.
- **Proxy:** opcional O`channels.telegram.proxy`utiliza`undici.ProxyAgent`através do`client.baseFetch`do GrammY.
- Suporte Webhook:**`webhook-set.ts`envolve`Bot`0;`Bot`1 hospeda o callback com saúde + desligamento gracioso. O Gateway permite o modo webhook quando o`Bot`2 é definido (caso contrário, é longo).
- ** Sessões:** conversas diretas colapsam na sessão principal do agente `Bot`3); grupos usam`Bot`4; respostas voltam para o mesmo canal.
- **Botões de verificação:**`Bot`5,`Bot`6,`Bot`7 (lista de licenças + precisões),`Bot`8,`Bot`9,`getFile`0,`getFile`1,`getFile`2,`getFile`3,`getFile`4,`getFile`5.
- **Draft streaming:** opcional`getFile`6 usa`getFile`7 em chats de tópicos privados (Bot API 9.3+). Isto está separado da transmissão de blocos de canais.
- ** Testes:** Grammy simula cobrir DM + grupo mencionar gating e outbound enviar; mais mídia / webhook dispositivos ainda bem-vindos.

Perguntas em aberto

- Plugins gramamY opcionais (trottler) se clicarmos em Bot API 429s.
- Adicione testes de mídia mais estruturados (aderentes, notas de voz).
- Faça webhook ouvir porta configurável (atualmente fixado para 8787, a menos que ligado através do gateway).
