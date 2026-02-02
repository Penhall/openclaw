# Criando habilidades personalizadas

OpenClaw é projetado para ser facilmente extensível. "Skills" são a principal maneira de adicionar novas capacidades ao seu assistente.

# # O que é uma habilidade?

Uma habilidade é um diretório contendo um arquivo `SKILL.md` (que fornece instruções e definições de ferramenta para o LLM) e opcionalmente alguns scripts ou recursos.

# # Passo a passo: sua primeira habilidade

# # # 1. Crie o Diretório

As habilidades vivem em seu espaço de trabalho, geralmente `~/.openclaw/workspace/skills/`. Crie uma nova pasta para sua habilidade:

```bash
mkdir -p ~/.openclaw/workspace/skills/hello-world
```

###2. Defina o `SKILL.md`

Crie um arquivo `SKILL.md` nesse diretório. Este arquivo usa a matéria frontal YAML para metadados e Markdown para instruções.

```markdown
---
name: hello_world
description: A simple skill that says hello.
---

# Hello World Skill

When the user asks for a greeting, use the `echo` tool to say "Hello from your custom skill!".
```

# # # 3. Adicionar Ferramentas (Opcional)

Você pode definir ferramentas personalizadas na matéria frontal ou instruir o agente a usar ferramentas de sistema existentes (como `bash` ou `browser`).

# # # 4. Atualizar Openclaw

Peça ao seu agente para "atualizar as habilidades" ou reinicie o gateway. OpenClaw descobrirá o novo diretório e indexará o <<CODE0>.

# # Melhores Práticas

- ** Seja conciso**: Instrua o modelo em  o que  fazer, não como ser uma IA.
- **Safety First**: Se sua habilidade usar `bash`, certifique-se de que as prompts não permitam injeção arbitrária de comando de entrada de usuário não confiável.
- ** Teste Local**: Utilizar `openclaw agent --message "use my new skill"` para testar.

# # Habilidades Compartilhadas

Você também pode navegar e contribuir com habilidades para [ClawHub](https://clawhub.com).
