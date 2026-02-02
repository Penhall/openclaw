---
summary: "Apply multi-file patches with the apply_patch tool"
read_when:
  - You need structured file edits across multiple files
  - You want to document or debug patch-based edits
---

# ferramenta apply patch

Aplique alterações de arquivo usando um formato de patch estruturado. Isto é ideal para multi-arquivos
ou edições multi-hunk onde uma única chamada `edit` seria frágil.

A ferramenta aceita uma única string `input` que envolve uma ou mais operações de arquivo:

```
*** Begin Patch
*** Add File: path/to/file.txt
+line 1
+line 2
*** Update File: src/app.ts
@@
-old line
+new line
*** Delete File: obsolete.txt
*** End Patch
```

# # Parâmetros

- <<CODE0> (obrigatório): Conteúdo total do sistema, incluindo `*** Begin Patch` e `*** End Patch`.

# # Notas

- Os caminhos são resolvidos em relação à raiz do espaço de trabalho.
- Use `*** Move to:` dentro de um <<CODE1> para renomear arquivos.
- <<CODE2> marca uma inserção de EOF apenas quando necessário.
- Experimental e desativado por padrão. Activar com `tools.exec.applyPatch.enabled`.
- OpenAI-only (incluindo OpenAI Codex). Porta opcional por modelo via
`tools.exec.applyPatch.allowModels`.
- A configuração está apenas em `tools.exec`.

# # Exemplo

```json
{
  "tool": "apply_patch",
  "input": "*** Begin Patch\n*** Update File: src/index.ts\n@@\n-const foo = 1\n+const foo = 2\n*** End Patch"
}
```
